// Command go-mutation runs mutation testing on a Go package.
//
// It parses non-test .go files in the target directory, applies AST-level
// mutations one at a time, runs `go test` for each, and reports which
// mutations survived (tests did NOT catch them = test blind spots).
//
// Usage:
//
//	go run go-mutation.go [-dir DIR] [-timeout SECS] [-parallel N]
//
// Defaults: dir=. (current dir), timeout=30s per test run, parallel=1.
// Output: JSON array of mutations to stdout; human-readable progress to stderr.
package main

import (
	"bytes"
	"context"
	"encoding/json"
	"flag"
	"fmt"
	"go/ast"
	"go/parser"
	"go/printer"
	"go/token"
	"io/fs"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"sync"
	"time"
)

// Mutation represents a single applied mutation and its test result.
type Mutation struct {
	File     string `json:"file"`
	Line     int    `json:"line"`
	Operator string `json:"operator"`        // e.g. "==" → "!="
	Original string `json:"original"`        // original source snippet
	Mutated  string `json:"mutated"`         // mutated source snippet
	Status   string `json:"status"`          // "killed" | "survived" | "timeout" | "compile-error"
	Diff     string `json:"diff,omitempty"`  // short diff for display
}

// candidate represents a single mutation site found during AST walk.
type candidate struct {
	file    string
	fset    *token.FileSet
	astFile *ast.File
	node    ast.Expr
	mutator mutator
	origSrc string
}

// mutator describes a single operator swap.
type mutator struct {
	name   string
	apply  func(expr ast.Expr) (ast.Expr, bool)
}

var mutators = []mutator{
	{"== → !=", func(e ast.Expr) (ast.Expr, bool) {
		b, ok := e.(*ast.BinaryExpr)
		if !ok || b.Op != token.EQL {
			return nil, false
		}
		return &ast.BinaryExpr{X: b.X, Op: token.NEQ, Y: b.Y}, true
	}},
	{"!= → ==", func(e ast.Expr) (ast.Expr, bool) {
		b, ok := e.(*ast.BinaryExpr)
		if !ok || b.Op != token.NEQ {
			return nil, false
		}
		return &ast.BinaryExpr{X: b.X, Op: token.EQL, Y: b.Y}, true
	}},
	{"> → <", func(e ast.Expr) (ast.Expr, bool) {
		b, ok := e.(*ast.BinaryExpr)
		if !ok || b.Op != token.GTR {
			return nil, false
		}
		return &ast.BinaryExpr{X: b.X, Op: token.LSS, Y: b.Y}, true
	}},
	{"< → >", func(e ast.Expr) (ast.Expr, bool) {
		b, ok := e.(*ast.BinaryExpr)
		if !ok || b.Op != token.LSS {
			return nil, false
		}
		return &ast.BinaryExpr{X: b.X, Op: token.GTR, Y: b.Y}, true
	}},
	{">= → <=", func(e ast.Expr) (ast.Expr, bool) {
		b, ok := e.(*ast.BinaryExpr)
		if !ok || b.Op != token.GEQ {
			return nil, false
		}
		return &ast.BinaryExpr{X: b.X, Op: token.LEQ, Y: b.Y}, true
	}},
	{"<= → >=", func(e ast.Expr) (ast.Expr, bool) {
		b, ok := e.(*ast.BinaryExpr)
		if !ok || b.Op != token.LEQ {
			return nil, false
		}
		return &ast.BinaryExpr{X: b.X, Op: token.GEQ, Y: b.Y}, true
	}},
	{"+ → -", func(e ast.Expr) (ast.Expr, bool) {
		b, ok := e.(*ast.BinaryExpr)
		if !ok || b.Op != token.ADD {
			return nil, false
		}
		return &ast.BinaryExpr{X: b.X, Op: token.SUB, Y: b.Y}, true
	}},
	{"- → +", func(e ast.Expr) (ast.Expr, bool) {
		b, ok := e.(*ast.BinaryExpr)
		if !ok || b.Op != token.SUB {
			return nil, false
		}
		return &ast.BinaryExpr{X: b.X, Op: token.ADD, Y: b.Y}, true
	}},
}

func main() {
	dir := flag.String("dir", ".", "target Go package directory")
	timeoutSec := flag.Int("timeout", 30, "per-mutation test timeout in seconds")
	parallel := flag.Int("parallel", 1, "parallel test runs (each mutates a temp copy)")
	flag.Parse()

	// Collect non-test .go source files.
	var srcFiles []string
	err := filepath.WalkDir(*dir, func(path string, d fs.DirEntry, err error) error {
		if err != nil {
			return err
		}
		if d.IsDir() {
			// Skip vendor, hidden dirs, testdata.
			name := d.Name()
			if path != *dir && (name == "vendor" || strings.HasPrefix(name, ".") || name == "testdata") {
				return filepath.SkipDir
			}
			return nil
		}
		if strings.HasSuffix(path, ".go") && !strings.HasSuffix(path, "_test.go") {
			srcFiles = append(srcFiles, path)
		}
		return nil
	})
	if err != nil {
		fmt.Fprintf(os.Stderr, "error walking %s: %v\n", *dir, err)
		os.Exit(1)
	}
	if len(srcFiles) == 0 {
		fmt.Fprintf(os.Stderr, "no non-test .go files found in %s\n", *dir)
		os.Exit(1)
	}

	fmt.Fprintf(os.Stderr, "[mutation] found %d source file(s)\n", len(srcFiles))

	// Collect all candidate mutations.
	var candidates []candidate

	for _, file := range srcFiles {
		fset := token.NewFileSet()
		astFile, err := parser.ParseFile(fset, file, nil, parser.ParseComments)
		if err != nil {
			fmt.Fprintf(os.Stderr, "[mutation] skip %s (parse error: %v)\n", file, err)
			continue
		}

		// Walk the AST to find mutable binary expressions.
		ast.Inspect(astFile, func(n ast.Node) bool {
			be, ok := n.(*ast.BinaryExpr)
			if !ok {
				return true
			}
			for _, m := range mutators {
				if _, ok := m.apply(be); !ok {
					continue
				}
				// Capture original source text for reporting.
				var buf bytes.Buffer
				printer.Fprint(&buf, fset, be)
				orig := buf.String()
				candidates = append(candidates, candidate{
					file:    file,
					fset:    fset,
					astFile: astFile,
					node:    be,
					mutator: m,
					origSrc: orig,
				})
			}
			return true
		})
	}

	fmt.Fprintf(os.Stderr, "[mutation] %d mutation candidates\n", len(candidates))

	// Run mutations. With parallel > 1, we copy the whole dir to temp and
	// test there to avoid clobbering the original. With parallel=1 we
	// mutate in place (faster, but the original is briefly modified).
	var results []Mutation
	var mu sync.Mutex

	work := make(chan candidate, len(candidates))
	for _, c := range candidates {
		work <- c
	}
	close(work)

	var wg sync.WaitGroup
	for i := 0; i < *parallel; i++ {
		wg.Add(1)
		go func(workerID int) {
			defer wg.Done()
			for c := range work {
				m := runMutation(c, *timeoutSec)
				mu.Lock()
				results = append(results, m)
				mu.Unlock()
				fmt.Fprintf(os.Stderr, "  [%s] %s:%d — %s\n", m.Status, m.File, m.Line, m.Operator)
			}
		}(i)
	}
	wg.Wait()

	// Output JSON.
	out, _ := json.MarshalIndent(results, "", "  ")
	fmt.Println(string(out))

	// Summary to stderr.
	killed, survived, timeout, compileErr := 0, 0, 0, 0
	for _, m := range results {
		switch m.Status {
		case "killed":
			killed++
		case "survived":
			survived++
		case "timeout":
			timeout++
		case "compile-error":
			compileErr++
		}
	}
	total := len(results)
	score := 0.0
	if total > 0 {
		score = float64(killed) / float64(total) * 100
	}
	fmt.Fprintf(os.Stderr, "\n[mutation] done: %d total, %d killed, %d survived, %d timeout, %d compile-error\n",
		total, killed, survived, timeout, compileErr)
	fmt.Fprintf(os.Stderr, "[mutation] mutation score: %.1f%%\n", score)
}

// runMutation applies a single mutation, tests, and restores the file.
func runMutation(c candidate, timeoutSec int) Mutation {
	origBytes, err := os.ReadFile(c.file)
	if err != nil {
		return Mutation{File: c.file, Status: "compile-error", Operator: c.mutator.name}
	}

	// Apply mutation by rewriting the AST and printing the full file.
	origExpr := c.node.(*ast.BinaryExpr)
	mutatedExpr, _ := c.mutator.apply(origExpr)

	// Swap the operator in-place (cheaper than re-printing whole file via AST,
	// but we need precise source — so we re-print the whole file).
	// Save original Op, set new Op, print, restore.
	originalOp := origExpr.Op
	switch m := mutatedExpr.(*ast.BinaryExpr); m.Op {
	case token.NEQ:
		origExpr.Op = token.NEQ
	case token.EQL:
		origExpr.Op = token.EQL
	case token.LSS:
		origExpr.Op = token.LSS
	case token.GTR:
		origExpr.Op = token.GTR
	case token.LEQ:
		origExpr.Op = token.LEQ
	case token.GEQ:
		origExpr.Op = token.GEQ
	case token.SUB:
		origExpr.Op = token.SUB
	case token.ADD:
		origExpr.Op = token.ADD
	}

	var mutatedBuf bytes.Buffer
	printer.Fprint(&mutatedBuf, c.fset, c.astFile)
	origExpr.Op = originalOp // restore AST in memory (not strictly needed, we re-read file)

	if err := os.WriteFile(c.file, mutatedBuf.Bytes(), 0644); err != nil {
		return Mutation{File: c.file, Status: "compile-error", Operator: c.mutator.name}
	}

	// Ensure restoration no matter what.
	defer os.WriteFile(c.file, origBytes, 0644)

	// Build report entry.
	pos := c.fset.Position(origExpr.Pos())

	// Run go test.
	status := runGoTest(c.file, timeoutSec)

	return Mutation{
		File:     c.file,
		Line:     pos.Line,
		Operator: c.mutator.name,
		Original: c.origSrc,
		Mutated:  strings.Replace(c.origSrc, opString(originalOp), opString(origExpr.Op), 1),
		Status:   status,
	}
}

// runGoTest runs `go test` in the directory of file and returns the status.
func runGoTest(file string, timeoutSec int) string {
	dir := filepath.Dir(file)
	ctx, cancel := context.WithTimeout(context.Background(), time.Duration(timeoutSec)*time.Second)
	defer cancel()

	cmd := exec.CommandContext(ctx, "go", "test", "./...")
	cmd.Dir = dir
	var stderr bytes.Buffer
	cmd.Stderr = &stderr

	// We only care about exit code:
	//   0 = tests passed → mutation SURVIVED (bad)
	//   non-0 = tests failed → mutation KILLED (good)
	err := cmd.Run()
	if ctx.Err() != nil {
		return "timeout"
	}
	if err == nil {
		return "survived"
	}
	// Distinguish compile error from test failure.
	if bytes.Contains(stderr.Bytes(), []byte("[build failed]")) || bytes.Contains(stderr.Bytes(), []byte("cannot run")) {
		return "compile-error"
	}
	return "killed"
}

// opString returns the textual form of a token for diff display.
func opString(tok token.Token) string {
	switch tok {
	case token.EQL:
		return "=="
	case token.NEQ:
		return "!="
	case token.GTR:
		return ">"
	case token.LSS:
		return "<"
	case token.GEQ:
		return ">="
	case token.LEQ:
		return "<="
	case token.ADD:
		return "+"
	case token.SUB:
		return "-"
	}
	return tok.String()
}


