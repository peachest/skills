---
name: write-gomega-matcher
description: Write custom Gomega matchers using gcustom.MakeMatcher with proper type assertion, error handling, and failure messages. Use when creating test matchers, adding assertions for CRD types, or when user mentions "matcher", "gomega matcher", or "custom assertion".
---

# Write Gomega Custom Matcher

## Quick start

Create a matcher function that returns `types.GomegaMatcher`, using `gcustom.MakeMatcher`:

```go
package matcher

import (
    "github.com/bsm/gomega/gcustom"
    "github.com/onsi/gomega/types"
    "github.com/pkg/errors"
)

// HaveFieldName returns a matcher that verifies MyType has a specific field value.
func HaveFieldName(expected string) types.GomegaMatcher {
    return gcustom.MakeMatcher(func(actual any) (bool, error) {
        obj, err := toMyType(actual)
        if err != nil {
            return false, err
        }
        return obj.FieldName == expected, nil
    }).WithTemplate(
        "Expected {{.Actual}} to {{if .Negate}}not {{end}}have FieldName {{format .Data 0}}",
    ).WithTemplateData(expected)
}
```

## Workflows

### 1. Plan the matcher

- Identify the **target type** (e.g., `*v1alpha1.NodeXpu`, `resource.Quantity`)
- Identify the **assertion** (field check, status check, condition check)
- Decide: single-parameter or multi-parameter matcher?
- Decide: does the assertion need a type-conversion helper?

### 2. Write the matcher function

Follow this checklist:

- [ ] Function returns `types.GomegaMatcher`
- [ ] Uses `gcustom.MakeMatcher` with `func(actual any) (bool, error)`
- [ ] Type-asserts `actual` via a `toXxx` helper (never inline the switch)
- [ ] Returns `false, err` on type mismatch
- [ ] Returns `false, nil` for logical mismatch (not an error)
- [ ] Adds `.WithTemplate(...)` for clear failure messages
- [ ] Adds `.WithTemplateData(...)` for parameterized messages
- [ ] Godoc starts with "// XxxMatcher returns a matcher that verifies..."

### 3. Write the type-assertion helper

Pattern for CRD types — accept both value and pointer:

```go
func toMyType(actual any) (*v1alpha1.MyType, error) {
    switch v := actual.(type) {
    case v1alpha1.MyType:
        return &v, nil
    case *v1alpha1.MyType:
        return v, nil
    default:
        return nil, errors.Errorf("expected v1alpha1.MyType or *v1alpha1.MyType, got %T", actual)
    }
}
```

For non-CRD types (e.g., `resource.Quantity`), handle the relevant input forms directly in the matcher.

### 4. Write tests

Follow the existing pattern from `pkg/test/matcher/`:

- Use Ginkgo `It` for positive and negative cases
- Test both `Should` and `ShouldNot` (via `NotTo`)
- Test type error (pass wrong type, expect failure)
- Test both value and pointer forms of the target type

```go
var _ = Describe("HaveFieldName", func() {
    It("should match when field has expected value", func() {
        obj := &v1alpha1.MyType{FieldName: "expected"}
        Expect(obj).To(matcher.HaveFieldName("expected"))
    })

    It("should not match when field has different value", func() {
        obj := &v1alpha1.MyType{FieldName: "other"}
        Expect(obj).NotTo(matcher.HaveFieldName("expected"))
    })

    It("should match value type", func() {
        obj := v1alpha1.MyType{FieldName: "expected"}
        Expect(obj).To(matcher.HaveFieldName("expected"))
    })
})
```

## Patterns

### Simple boolean check

```go
func BeHealthy() types.GomegaMatcher {
    return gcustom.MakeMatcher(func(actual any) (bool, error) {
        nx, err := toNodeXpu(actual)
        if err != nil { return false, err }
        return nx.Status.Health, nil
    })
}
```

### Parameterized check

```go
func HaveConditionStatus(conditionType string, status metav1.ConditionStatus) types.GomegaMatcher {
    return gcustom.MakeMatcher(func(actual any) (bool, error) {
        nx, err := toNodeXpu(actual)
        if err != nil { return false, err }
        cond := findCondition(nx.Status.Conditions, conditionType)
        if cond == nil { return false, nil }
        return cond.Status == status, nil
    }).WithTemplate(
        "Expected {{.Actual}} to {{if .Negate}}not {{end}}have condition {{format .Data 0}} with status {{format .Data 1}}",
    ).WithTemplateData([]any{conditionType, status})
}
```

### Helper function for nested lookups

Keep helper functions unexported in the same package. They can be shared across matchers:

```go
func findCondition(conditions []metav1.Condition, condType string) *metav1.Condition {
    for i := range conditions {
        if conditions[i].Type == condType {
            return &conditions[i]
        }
    }
    return nil
}
```

## Key rules

1. **Never return `true, err`** — errors mean the match couldn't be evaluated, not that it succeeded
2. **Return `false, nil`** when the assertion logically fails (wrong value, condition not found)
3. **Return `false, err`** only for type errors or unexpected failures
4. **Heavy parameters** (structs > ~80 bytes like `metav1.Condition`) must be passed by pointer to avoid `hugeParam` lint errors
5. **Reuse `toXxx` helpers** across matchers for the same target type — they're unexported and package-scoped
6. **Template format**: use `{{format .Data N}}` for the Nth template data item; use `{{if .Negate}}not {{end}}` for negation support
7. **Keep matchers in `pkg/test/matcher/`** package, co-located with existing matchers
8. **Test file naming**: `<matcher_name>_test.go` in the same package (`matcher_test`)
