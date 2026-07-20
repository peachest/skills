# Language Server Extension Guide

> 源文档: [https://code.visualstudio.com/api/language-extensions/language-server-extension-guide](https://code.visualstudio.com/api/language-extensions/language-server-extension-guide)

<main id="main-content"><div class="body-content docs docs-github-layout">
	<div class="docs-layout-wrapper">
		
		<aside class="docs-left-sidebar"><nav id="docs-navbar" aria-label="Topics" class="docs-nav visible-md visible-lg"><h4>Extension API</h4>
			  <ul class="nav" id="main-nav"><li>
			    <a href="/api">Overview</a>
			  </li>
			  
			<li class="panel collapsed">
			  <a class="area" role="button" href="#get-started-articles" data-parent="#main-nav" data-toggle="collapse">Get Started</a>
			  <ul id="get-started-articles" class="collapse "><li>
			          <a href="/api/get-started/your-first-extension">Your First Extension</a>
			        </li>
			          
			        <li>
			          <a href="/api/get-started/extension-anatomy">Extension Anatomy</a>
			        </li>
			          
			        <li>
			          <a href="/api/get-started/wrapping-up">Wrapping Up</a>
			        </li>
			          
			  </ul></li>
			    
			<li class="panel collapsed">
			  <a class="area" role="button" href="#extension-capabilities-articles" data-parent="#main-nav" data-toggle="collapse">Extension Capabilities</a>
			  <ul id="extension-capabilities-articles" class="collapse "><li>
			          <a href="/api/extension-capabilities/overview">Overview</a>
			        </li>
			          
			        <li>
			          <a href="/api/extension-capabilities/common-capabilities">Common Capabilities</a>
			        </li>
			          
			        <li>
			          <a href="/api/extension-capabilities/theming">Theming</a>
			        </li>
			          
			        <li>
			          <a href="/api/extension-capabilities/extending-workbench">Extending Workbench</a>
			        </li>
			          
			  </ul></li>
			    
			<li class="panel collapsed">
			  <a class="area" role="button" href="#extension-guides-articles" data-parent="#main-nav" data-toggle="collapse">Extension Guides</a>
			  <ul id="extension-guides-articles" class="collapse "><li>
			          <a href="/api/extension-guides/overview">Overview</a>
			        </li>
			          
			<li class="panel collapsed">
			  <a class="area" role="button" href="#extension-guides-ai-articles" data-parent="#extension-guides-articles" data-toggle="collapse">AI</a>
			  <ul id="extension-guides-ai-articles" class="collapse "><li>
			          <a href="/api/extension-guides/ai/ai-extensibility-overview">AI Extensibility</a>
			        </li>
			          
			        <li>
			          <a href="/api/extension-guides/ai/tools">Language Model Tool</a>
			        </li>
			          
			        <li>
			          <a href="/api/extension-guides/ai/mcp">MCP Dev Guide</a>
			        </li>
			          
			        <li>
			          <a href="/api/extension-guides/ai/chat">Chat Participant</a>
			        </li>
			          
			        <li>
			          <a href="/api/extension-guides/ai/chat-tutorial">Chat Tutorial</a>
			        </li>
			          
			        <li>
			          <a href="/api/extension-guides/ai/language-model">Language Model</a>
			        </li>
			          
			        <li>
			          <a href="/api/extension-guides/ai/language-model-tutorial">Language Model Tutorial</a>
			        </li>
			          
			        <li>
			          <a href="/api/extension-guides/ai/language-model-chat-provider">Language Model Chat Provider</a>
			        </li>
			          
			        <li>
			          <a href="/api/extension-guides/ai/prompt-tsx">Prompt TSX</a>
			        </li>
			          
			  </ul></li>
			        
			        <li>
			          <a href="/api/extension-guides/command">Command</a>
			        </li>
			          
			        <li>
			          <a href="/api/extension-guides/color-theme">Color Theme</a>
			        </li>
			          
			        <li>
			          <a href="/api/extension-guides/file-icon-theme">File Icon Theme</a>
			        </li>
			          
			        <li>
			          <a href="/api/extension-guides/product-icon-theme">Product Icon Theme</a>
			        </li>
			          
			        <li>
			          <a href="/api/extension-guides/tree-view">Tree View</a>
			        </li>
			          
			        <li>
			          <a href="/api/extension-guides/webview">Webview</a>
			        </li>
			          
			        <li>
			          <a href="/api/extension-guides/notebook">Notebook</a>
			        </li>
			          
			        <li>
			          <a href="/api/extension-guides/custom-editors">Custom Editors</a>
			        </li>
			          
			        <li>
			          <a href="/api/extension-guides/virtual-documents">Virtual Documents</a>
			        </li>
			          
			        <li>
			          <a href="/api/extension-guides/virtual-workspaces">Virtual Workspaces</a>
			        </li>
			          
			        <li>
			          <a href="/api/extension-guides/web-extensions">Web Extensions</a>
			        </li>
			          
			        <li>
			          <a href="/api/extension-guides/workspace-trust">Workspace Trust</a>
			        </li>
			          
			        <li>
			          <a href="/api/extension-guides/task-provider">Task Provider</a>
			        </li>
			          
			        <li>
			          <a href="/api/extension-guides/scm-provider">Source Control</a>
			        </li>
			          
			        <li>
			          <a href="/api/extension-guides/debugger-extension">Debugger Extension</a>
			        </li>
			          
			        <li>
			          <a href="/api/extension-guides/markdown-extension">Markdown Extension</a>
			        </li>
			          
			        <li>
			          <a href="/api/extension-guides/testing">Test Extension</a>
			        </li>
			          
			        <li>
			          <a href="/api/extension-guides/custom-data-extension">Custom Data Extension</a>
			        </li>
			          
			        <li>
			          <a href="/api/extension-guides/telemetry">Telemetry</a>
			        </li>
			          
			  </ul></li>
			    
			<li class="panel collapsed">
			  <a class="area" role="button" href="#ux-guidelines-articles" data-parent="#main-nav" data-toggle="collapse">UX Guidelines</a>
			  <ul id="ux-guidelines-articles" class="collapse "><li>
			          <a href="/api/ux-guidelines/overview">Overview</a>
			        </li>
			          
			        <li>
			          <a href="/api/ux-guidelines/activity-bar">Activity Bar</a>
			        </li>
			          
			        <li>
			          <a href="/api/ux-guidelines/sidebars">Sidebars</a>
			        </li>
			          
			        <li>
			          <a href="/api/ux-guidelines/panel">Panel</a>
			        </li>
			          
			        <li>
			          <a href="/api/ux-guidelines/status-bar">Status Bar</a>
			        </li>
			          
			        <li>
			          <a href="/api/ux-guidelines/views">Views</a>
			        </li>
			          
			        <li>
			          <a href="/api/ux-guidelines/editor-actions">Editor Actions</a>
			        </li>
			          
			        <li>
			          <a href="/api/ux-guidelines/quick-picks">Quick Picks</a>
			        </li>
			          
			        <li>
			          <a href="/api/ux-guidelines/command-palette">Command Palette</a>
			        </li>
			          
			        <li>
			          <a href="/api/ux-guidelines/notifications">Notifications</a>
			        </li>
			          
			        <li>
			          <a href="/api/ux-guidelines/webviews">Webviews</a>
			        </li>
			          
			        <li>
			          <a href="/api/ux-guidelines/context-menus">Context Menus</a>
			        </li>
			          
			        <li>
			          <a href="/api/ux-guidelines/walkthroughs">Walkthroughs</a>
			        </li>
			          
			        <li>
			          <a href="/api/ux-guidelines/settings">Settings</a>
			        </li>
			          
			  </ul></li>
			    
			<li class="panel active expanded">
			  <a class="area" role="button" href="#language-extensions-articles" data-parent="#main-nav" data-toggle="collapse">Language Extensions</a>
			  <ul id="language-extensions-articles" class="collapse in"><li>
			          <a href="/api/language-extensions/overview">Overview</a>
			        </li>
			          
			        <li>
			          <a href="/api/language-extensions/syntax-highlight-guide">Syntax Highlight Guide</a>
			        </li>
			          
			        <li>
			          <a href="/api/language-extensions/semantic-highlight-guide">Semantic Highlight Guide</a>
			        </li>
			          
			        <li>
			          <a href="/api/language-extensions/snippet-guide">Snippet Guide</a>
			        </li>
			          
			        <li>
			          <a href="/api/language-extensions/language-configuration-guide">Language Configuration Guide</a>
			        </li>
			          
			        <li>
			          <a href="/api/language-extensions/programmatic-language-features">Programmatic Language Features</a>
			        </li>
			          
			        <li class="active">
			          <a href="/api/language-extensions/language-server-extension-guide" aria-label="Current Page: Language Server Extension Guide">Language Server Extension Guide</a>
			        </li>
			          
			        <li>
			          <a href="/api/language-extensions/embedded-languages">Embedded Languages</a>
			        </li>
			          
			  </ul></li>
			    
			<li class="panel collapsed">
			  <a class="area" role="button" href="#working-with-extensions-articles" data-parent="#main-nav" data-toggle="collapse">Testing and Publishing</a>
			  <ul id="working-with-extensions-articles" class="collapse "><li>
			          <a href="/api/working-with-extensions/testing-extension">Testing Extensions</a>
			        </li>
			          
			        <li>
			          <a href="/api/working-with-extensions/publishing-extension">Publishing Extensions</a>
			        </li>
			          
			        <li>
			          <a href="/api/working-with-extensions/bundling-extension">Bundling Extensions</a>
			        </li>
			          
			        <li>
			          <a href="/api/working-with-extensions/continuous-integration">Continuous Integration</a>
			        </li>
			          
			  </ul></li>
			    
			<li class="panel collapsed">
			  <a class="area" role="button" href="#advanced-topics-articles" data-parent="#main-nav" data-toggle="collapse">Advanced Topics</a>
			  <ul id="advanced-topics-articles" class="collapse "><li>
			          <a href="/api/advanced-topics/extension-host">Extension Host</a>
			        </li>
			          
			        <li>
			          <a href="/api/advanced-topics/remote-extensions">Remote Development and Codespaces</a>
			        </li>
			          
			        <li>
			          <a href="/api/advanced-topics/using-proposed-api">Using Proposed API</a>
			        </li>
			          
			        <li>
			          <a href="/api/advanced-topics/tslint-eslint-migration">Migrate from TSLint to ESLint</a>
			        </li>
			          
			        <li>
			          <a href="/api/advanced-topics/python-extension-template">Python Extension Template</a>
			        </li>
			          
			  </ul></li>
			    
			<li class="panel collapsed">
			  <a class="area" role="button" href="#references-articles" data-parent="#main-nav" data-toggle="collapse">References</a>
			  <ul id="references-articles" class="collapse "><li>
			          <a href="/api/references/vscode-api">VS Code API</a>
			        </li>
			          
			        <li>
			          <a href="/api/references/contribution-points">Contribution Points</a>
			        </li>
			          
			        <li>
			          <a href="/api/references/activation-events">Activation Events</a>
			        </li>
			          
			        <li>
			          <a href="/api/references/extension-manifest">Extension Manifest</a>
			        </li>
			          
			        <li>
			          <a href="/api/references/commands">Built-In Commands</a>
			        </li>
			          
			        <li>
			          <a href="/api/references/when-clause-contexts">When Clause Contexts</a>
			        </li>
			          
			        <li>
			          <a href="/api/references/theme-color">Theme Color</a>
			        </li>
			          
			        <li>
			          <a href="/api/references/icons-in-labels">Product Icon Reference</a>
			        </li>
			          
			        <li>
			          <a href="/api/references/document-selector">Document Selector</a>
			        </li>
			          
			  </ul></li>
			    
			  </ul></nav><nav id="small-nav" aria-label="Topics" class="docs-nav hidden-md hidden-lg"><label class="faux-h4" for="small-nav-dropdown">Topics</label>
				<select id="small-nav-dropdown" aria-label="topics"><option value="/api">Overview</option><optgroup label="Get Started"><option value="/api/get-started/your-first-extension">Your First Extension</option><option value="/api/get-started/extension-anatomy">Extension Anatomy</option><option value="/api/get-started/wrapping-up">Wrapping Up</option></optgroup><optgroup label="Extension Capabilities"><option value="/api/extension-capabilities/overview">Overview</option><option value="/api/extension-capabilities/common-capabilities">Common Capabilities</option><option value="/api/extension-capabilities/theming">Theming</option><option value="/api/extension-capabilities/extending-workbench">Extending Workbench</option></optgroup><optgroup label="Extension Guides"><option value="/api/extension-guides/overview">Overview</option><optgroup label="Extension Guides - AI"><option value="/api/extension-guides/ai/ai-extensibility-overview">AI Extensibility</option><option value="/api/extension-guides/ai/tools">Language Model Tool</option><option value="/api/extension-guides/ai/mcp">MCP Dev Guide</option><option value="/api/extension-guides/ai/chat">Chat Participant</option><option value="/api/extension-guides/ai/chat-tutorial">Chat Tutorial</option><option value="/api/extension-guides/ai/language-model">Language Model</option><option value="/api/extension-guides/ai/language-model-tutorial">Language Model Tutorial</option><option value="/api/extension-guides/ai/language-model-chat-provider">Language Model Chat Provider</option><option value="/api/extension-guides/ai/prompt-tsx">Prompt TSX</option></optgroup><option value="/api/extension-guides/command">Command</option><option value="/api/extension-guides/color-theme">Color Theme</option><option value="/api/extension-guides/file-icon-theme">File Icon Theme</option><option value="/api/extension-guides/product-icon-theme">Product Icon Theme</option><option value="/api/extension-guides/tree-view">Tree View</option><option value="/api/extension-guides/webview">Webview</option><option value="/api/extension-guides/notebook">Notebook</option><option value="/api/extension-guides/custom-editors">Custom Editors</option><option value="/api/extension-guides/virtual-documents">Virtual Documents</option><option value="/api/extension-guides/virtual-workspaces">Virtual Workspaces</option><option value="/api/extension-guides/web-extensions">Web Extensions</option><option value="/api/extension-guides/workspace-trust">Workspace Trust</option><option value="/api/extension-guides/task-provider">Task Provider</option><option value="/api/extension-guides/scm-provider">Source Control</option><option value="/api/extension-guides/debugger-extension">Debugger Extension</option><option value="/api/extension-guides/markdown-extension">Markdown Extension</option><option value="/api/extension-guides/testing">Test Extension</option><option value="/api/extension-guides/custom-data-extension">Custom Data Extension</option><option value="/api/extension-guides/telemetry">Telemetry</option></optgroup><optgroup label="UX Guidelines"><option value="/api/ux-guidelines/overview">Overview</option><option value="/api/ux-guidelines/activity-bar">Activity Bar</option><option value="/api/ux-guidelines/sidebars">Sidebars</option><option value="/api/ux-guidelines/panel">Panel</option><option value="/api/ux-guidelines/status-bar">Status Bar</option><option value="/api/ux-guidelines/views">Views</option><option value="/api/ux-guidelines/editor-actions">Editor Actions</option><option value="/api/ux-guidelines/quick-picks">Quick Picks</option><option value="/api/ux-guidelines/command-palette">Command Palette</option><option value="/api/ux-guidelines/notifications">Notifications</option><option value="/api/ux-guidelines/webviews">Webviews</option><option value="/api/ux-guidelines/context-menus">Context Menus</option><option value="/api/ux-guidelines/walkthroughs">Walkthroughs</option><option value="/api/ux-guidelines/settings">Settings</option></optgroup><optgroup label="Language Extensions"><option value="/api/language-extensions/overview">Overview</option><option value="/api/language-extensions/syntax-highlight-guide">Syntax Highlight Guide</option><option value="/api/language-extensions/semantic-highlight-guide">Semantic Highlight Guide</option><option value="/api/language-extensions/snippet-guide">Snippet Guide</option><option value="/api/language-extensions/language-configuration-guide">Language Configuration Guide</option><option value="/api/language-extensions/programmatic-language-features">Programmatic Language Features</option><option value="/api/language-extensions/language-server-extension-guide" selected>Language Server Extension Guide</option><option value="/api/language-extensions/embedded-languages">Embedded Languages</option></optgroup><optgroup label="Testing and Publishing"><option value="/api/working-with-extensions/testing-extension">Testing Extensions</option><option value="/api/working-with-extensions/publishing-extension">Publishing Extensions</option><option value="/api/working-with-extensions/bundling-extension">Bundling Extensions</option><option value="/api/working-with-extensions/continuous-integration">Continuous Integration</option></optgroup><optgroup label="Advanced Topics"><option value="/api/advanced-topics/extension-host">Extension Host</option><option value="/api/advanced-topics/remote-extensions">Remote Development and Codespaces</option><option value="/api/advanced-topics/using-proposed-api">Using Proposed API</option><option value="/api/advanced-topics/tslint-eslint-migration">Migrate from TSLint to ESLint</option><option value="/api/advanced-topics/python-extension-template">Python Extension Template</option></optgroup><optgroup label="References"><option value="/api/references/vscode-api">VS Code API</option><option value="/api/references/contribution-points">Contribution Points</option><option value="/api/references/activation-events">Activation Events</option><option value="/api/references/extension-manifest">Extension Manifest</option><option value="/api/references/commands">Built-In Commands</option><option value="/api/references/when-clause-contexts">When Clause Contexts</option><option value="/api/references/theme-color">Theme Color</option><option value="/api/references/icons-in-labels">Product Icon Reference</option><option value="/api/references/document-selector">Document Selector</option></optgroup></select></nav></aside><div class="docs-content-wrapper">
			
			<main class="docs-main-content body"><h1>Language Server Extension Guide</h1>
<p>As you have seen in the <a href="/api/language-extensions/programmatic-language-features">Programmatic Language Features</a> topic, it's possible to implement Language Features by directly using <code>languages.*</code> API. Language Server Extension, however, provides an alternative way of implementing such language support.</p>
<p>This topic:</p>
<ul><li>Explains the benefits of Language Server Extension.</li>
<li>Walks you through building a Language Server using the <a href="https://github.com/microsoft/vscode-languageserver-node" class="external-link" target="_blank"><code>Microsoft/vscode-languageserver-node</code></a> library. You can also jump directly to the code in <a href="https://github.com/microsoft/vscode-extension-samples/tree/main/lsp-sample" class="external-link" target="_blank">lsp-sample</a>.</li>
</ul><h2 id="why-language-server" data-needslink="why-language-server">Why Language Server?</h2>
<p>Language Server is a special kind of Visual Studio Code extension that powers the editing experience for many programming languages. With Language Servers, you can implement autocomplete, error-checking (diagnostics), jump-to-definition, and many other <a href="/api/language-extensions/programmatic-language-features">language features</a> supported in VS Code.</p>
<p>However, while implementing support for language features in VS Code, we found three common problems:</p>
<p>First, Language Servers are usually implemented in their native programming languages, and that presents a challenge in integrating them with VS Code, which has a Node.js runtime.</p>
<p>Additionally, language features can be resource intensive. For example, to correctly validate a file, Language Server needs to parse a large amount of files, build up Abstract Syntax Trees for them and perform static program analysis. Those operations could incur significant CPU and memory usage and we need to ensure that VS Code's performance remains unaffected.</p>
<p>Finally, integrating multiple language toolings with multiple code editors could involve significant effort. From language toolings' perspective, they need to adapt to code editors with different APIs. From code editors' perspective, they cannot expect any uniform API from language toolings. This makes implementing language support for <code>M</code> languages in <code>N</code> code editors the work of <code>M * N</code>.</p>
<p>To solve those problems, Microsoft specified <a href="https://microsoft.github.io/language-server-protocol" class="external-link" target="_blank">Language Server Protocol</a>, which standardizes the communication between language tooling and code editor. This way, Language Servers can be implemented in any language and run in their own process to avoid performance cost, as they communicate with the code editor through the Language Server Protocol. Furthermore, any LSP-compliant language toolings can integrate with multiple LSP-compliant code editors, and any LSP-compliant code editors can easily pick up multiple LSP-compliant language toolings. LSP is a win for both language tooling providers and code editor vendors!</p>
<p><img src="/assets/api/language-extensions/language-server-extension-guide/lsp-languages-editors.png" alt="LSP Languages and Editors" loading="lazy"></p>
<p>In this guide, we will:</p>
<ul><li>Explain how to build a Language Server extension in VS Code using the provided <a href="https://github.com/microsoft/vscode-languageserver-node" class="external-link" target="_blank">Node SDK</a>.</li>
<li>Explain how to run, debug, log, and test the Language Server extension.</li>
<li>Point you to some advanced topics on Language Servers.</li>
</ul><h2 id="implementing-a-language-server" data-needslink="implementing-a-language-server">Implementing a Language Server</h2>
<h3 id="overview" data-needslink="overview">Overview</h3>
<p>In VS Code, a language server has two parts:</p>
<ul><li>Language Client: A normal VS Code extension written in JavaScript / TypeScript. This extension has access to all <a href="/api/references/vscode-api">VS Code Namespace API</a>.</li>
<li>Language Server: A language analysis tool running in a separate process.</li>
</ul><p>As briefly stated above there are two benefits of running the Language Server in a separate process:</p>
<ul><li>The analysis tool can be implemented in any languages, as long as it can communicate with the Language Client following the Language Server Protocol.</li>
<li>As language analysis tools are often heavy on CPU and Memory usage, running them in separate process avoids performance cost.</li>
</ul><p>Here is an illustration of VS Code running two Language Server extensions. The HTML Language Client and PHP Language Client are normal VS Code extensions written in TypeScript. Each of them instantiates a corresponding Language Server and communicates with them through LSP. Although the PHP Language Server is written in PHP, it can still communicate with the PHP Language Client through LSP.</p>
<p><img src="/assets/api/language-extensions/language-server-extension-guide/lsp-illustration.png" alt="LSP Illustration" loading="lazy"></p>
<p>This guide will teach you how to build a Language Client / Server using our <a href="https://github.com/microsoft/vscode-languageserver-node" class="external-link" target="_blank">Node SDK</a>. The remaining document assumes that you are familiar with VS Code <a href="/api">Extension API</a>.</p>
<h3 id="lsp-sample-a-simple-language-server-for-plain-text-files" data-needslink="lsp-sample-a-simple-language-server-for-plain-text-files">LSP Sample - A simple Language Server for plain text files</h3>
<p>Let's build a simple Language Server extension that implements autocomplete and diagnostics for plain text files. We will also cover the syncing of configurations between Client / Server.</p>
<p>If you prefer to jump right into the code:</p>
<ul><li><strong><a href="https://github.com/microsoft/vscode-extension-samples/tree/main/lsp-sample" class="external-link" target="_blank">lsp-sample</a></strong>: Heavily documented source code for this guide.</li>
<li><strong><a href="https://github.com/microsoft/vscode-extension-samples/tree/main/lsp-multi-server-sample" class="external-link" target="_blank">lsp-multi-server-sample</a></strong>: A heavily documented, advanced version of <strong>lsp-sample</strong> that starts a different server instance per workspace folder to support the <a href="/docs/editor/multi-root-workspaces">multi-root workspace</a> feature in VS Code.</li>
</ul><p>Clone the repository <a href="https://github.com/microsoft/vscode-extension-samples" class="external-link" target="_blank">Microsoft/vscode-extension-samples</a> and open the sample:</p>
<pre class="shiki" data-lang="bash" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">&gt; git clone https://github.com/microsoft/vscode-extension-samples.git</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">&gt; cd vscode-extension-samples/lsp-sample</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">&gt; npm install</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">&gt; npm run compile</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">&gt; code </span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">.</span></span>
<span class="line"></span></code></pre>
<p>The above installs all dependencies and opens the <strong>lsp-sample</strong> workspace containing both the client and server code. Here is a rough overview of the structure of <strong>lsp-sample</strong>:</p>
<pre class="shiki" data-lang="text" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span>.</span></span>
<span class="line"><span>├── client // Language Client</span></span>
<span class="line"><span>│   ├── src</span></span>
<span class="line"><span>│   │   ├── test // End to End tests for Language Client / Server</span></span>
<span class="line"><span>│   │   └── extension.ts // Language Client entry point</span></span>
<span class="line"><span>├── package.json // The extension manifest</span></span>
<span class="line"><span>└── server // Language Server</span></span>
<span class="line"><span>    └── src</span></span>
<span class="line"><span>        └── server.ts // Language Server entry point</span></span>
<span class="line"><span></span></span></code></pre>
<h3 id="explaining-the-language-client" data-needslink="explaining-the-language-client">Explaining the 'Language Client'</h3>
<p>Let's first take a look at <code>/package.json</code>, which describes the capabilities of the Language Client. There are two interesting sections:</p>
<p>First, look at the <a href="/api/references/contribution-points#contributes.configuration"><code>configuration</code></a> section:</p>
<pre class="shiki" data-lang="json" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"configuration"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "type"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"object"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "title"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"Example configuration"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "properties"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">        "languageServerExample.maxNumberOfProblems"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">            "scope"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"resource"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">            "type"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"number"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">            "default"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#B5CEA8;--shiki-light:#098658">100</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">            "description"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"Controls the maximum number of problems produced by the server."</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">        }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<p>This section contributes <code>configuration</code> settings to VS Code. The example will explain how these settings are sent over to the language server on startup and on every change of the settings.</p>
<blockquote><p><strong>Note</strong>: If your extension is compatible with VS Code versions prior to 1.74.0, you must declare <code>onLanguage:plaintext</code> in the <a href="/api/references/activation-events"><code>activationEvents</code></a>  field of <code>/package.json</code> to tell VS Code to activate the extension as soon as a plain text file is opened (for example a file with the extension <code>.txt</code>):</p>
<pre class="shiki" data-lang="json" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"activationEvents"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: []</span></span>
<span class="line"></span></code></pre>
</blockquote><p>The actual Language Client source code and the corresponding <code>package.json</code> are in the <code>/client</code> folder. The interesting part in the <code>/client/package.json</code> file is that it references the <code>vscode</code> extension host API through the <code>engines</code> field and adds a dependency to the <code>vscode-languageclient</code> library:</p>
<pre class="shiki" data-lang="json" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"engines"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "vscode"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"^1.52.0"</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">},</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"dependencies"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "vscode-languageclient"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"^7.0.0"</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<p>As mentioned, the client is implemented as a normal VS Code extension, and it has access to all VS Code namespace API.</p>
<p>Below is the content of the corresponding extension.ts file, which is the entry of the <strong>lsp-sample</strong> extension:</p>
<pre class="shiki" data-lang="typescript" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">import</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> *</span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB"> as</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> path</span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB"> from</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'path'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">import</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> { </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">workspace</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">ExtensionContext</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> } </span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">from</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'vscode'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">import</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  LanguageClient</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  LanguageClientOptions</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  ServerOptions</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  TransportKind</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">} </span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">from</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'vscode-languageclient/node'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">let</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> client</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">LanguageClient</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> | </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">undefined</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">export</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> async</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> function</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> activate</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">context</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">ExtensionContext</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">  // The server is implemented in node</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">  let</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> serverModule</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">context</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">asAbsolutePath</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">path</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">join</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'server'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'out'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'server.js'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">));</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">  // The debug options for the server</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">  // --inspect=6009: runs the server in Node's Inspector mode so VS Code can attach to the server for debugging</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">  let</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> debugOptions</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = { </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">execArgv:</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> [</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'--nolazy'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'--inspect=6009'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">] };</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">  // If the extension is launched in debug mode then the debug server options are used</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">  // Otherwise the run options are used</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">  let</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> serverOptions</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">ServerOptions</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    run:</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> { </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">module:</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> serverModule</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">transport:</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> TransportKind</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">ipc</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> },</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    debug:</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">      module:</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> serverModule</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">      transport:</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> TransportKind</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">ipc</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">      options:</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> debugOptions</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  };</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">  // Options to control the language client</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">  let</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> clientOptions</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">LanguageClientOptions</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = {</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">    // Register the server for plain text documents</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    documentSelector:</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> [{ </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">scheme:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'file'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">language:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'plaintext'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> }],</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    synchronize:</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">      // Notify the server about file changes to '.clientrc files contained in the workspace</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">      fileEvents:</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> workspace</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">createFileSystemWatcher</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'**/.clientrc'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">)</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  };</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">  // Create the language client and start the client.</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  client</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">new</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> LanguageClient</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">    'languageServerExample'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">    'Language Server Example'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    serverOptions</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    clientOptions</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  );</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">  // Start the client. This will also launch the server</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">  await</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> client</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">start</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">();</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">export</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> async</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> function</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> deactivate</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">() {</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">  await</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> client</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">?.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">dispose</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">();</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  client</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">undefined</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<h3 id="explaining-the-language-server" data-needslink="explaining-the-language-server">Explaining the 'Language Server'</h3>
<blockquote><p><strong>Note:</strong> The 'Server' implementation cloned from the GitHub repository has the final walkthrough implementation. To follow the walkthrough, you can create a new <code>server.ts</code> or modify the contents of the cloned version.</p>
</blockquote><p>In the example, the server is also implemented in TypeScript and executed using Node.js. Since VS Code already ships with a Node.js runtime, there is no need to provide your own, unless you have specific requirements for the runtime.</p>
<p>The source code for the Language Server is at <code>/server</code>. The interesting section in the server's <code>package.json</code> file is:</p>
<pre class="shiki" data-lang="json" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"dependencies"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "vscode-languageserver"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"^7.0.0"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "vscode-languageserver-textdocument"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"^1.0.1"</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<p>This pulls in the <code>vscode-languageserver</code> libraries.</p>
<p>Below is a server implementation that uses the provided text document manager that synchronizes text documents by always sending incremental deltas from VS Code to the server.</p>
<pre class="shiki" data-lang="typescript" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">import</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  createConnection</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  TextDocuments</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  Diagnostic</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  DiagnosticSeverity</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  ProposedFeatures</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  InitializeParams</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  DidChangeConfigurationNotification</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  CompletionItem</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  CompletionItemKind</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  TextDocumentPositionParams</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  TextDocumentSyncKind</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  InitializeResult</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">} </span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">from</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'vscode-languageserver/node'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">import</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> { </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">TextDocument</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> } </span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">from</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'vscode-languageserver-textdocument'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">// Create a connection for the server, using Node's IPC as a transport.</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">// Also include all preview / proposed LSP features.</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">let</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> connection</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">createConnection</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">ProposedFeatures</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">all</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">// Create a simple text document manager.</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">let</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> documents</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">TextDocuments</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">&lt;</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">TextDocument</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">&gt; = </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">new</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> TextDocuments</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">TextDocument</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">let</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> hasConfigurationCapability</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">boolean</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">false</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">let</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> hasWorkspaceFolderCapability</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">boolean</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">false</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">let</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> hasDiagnosticRelatedInformationCapability</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">boolean</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">false</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">connection</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">onInitialize</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">((</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">params</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">InitializeParams</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">=&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">  let</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> capabilities</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">params</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">capabilities</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">  // Does the client support the `workspace/configuration` request?</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">  // If not, we fall back using global settings.</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  hasConfigurationCapability</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = !!(</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    capabilities</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">workspace</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> &amp;&amp; !!</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">capabilities</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">workspace</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">configuration</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  );</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  hasWorkspaceFolderCapability</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = !!(</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    capabilities</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">workspace</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> &amp;&amp; !!</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">capabilities</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">workspace</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">workspaceFolders</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  );</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  hasDiagnosticRelatedInformationCapability</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = !!(</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    capabilities</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">textDocument</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> &amp;&amp;</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    capabilities</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">textDocument</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">publishDiagnostics</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> &amp;&amp;</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    capabilities</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">textDocument</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">publishDiagnostics</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">relatedInformation</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  );</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">  const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> result</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">InitializeResult</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    capabilities:</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">      textDocumentSync:</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> TextDocumentSyncKind</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">Incremental</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">      // Tell the client that this server supports code completion.</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">      completionProvider:</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">        resolveProvider:</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> true</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  };</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">  if</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> (</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">hasWorkspaceFolderCapability</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    result</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">capabilities</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">workspace</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">      workspaceFolders:</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">        supported:</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> true</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    };</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  }</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">  return</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> result</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">});</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">connection</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">onInitialized</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(() </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">=&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">  if</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> (</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">hasConfigurationCapability</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">    // Register for all configuration changes.</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    connection</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">client</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">register</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">DidChangeConfigurationNotification</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">type</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">undefined</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  }</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">  if</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> (</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">hasWorkspaceFolderCapability</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    connection</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">workspace</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">onDidChangeWorkspaceFolders</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">_event</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> =&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">      connection</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">console</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">log</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'Workspace folder change event received.'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    });</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">});</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">// The example settings</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">interface</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99"> ExampleSettings</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  maxNumberOfProblems</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">number</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">// The global settings, used when the `workspace/configuration` request is not supported by the client.</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">// Please note that this is not the case when using this server with the client provided in this example</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">// but could happen with other clients.</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> defaultSettings</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">ExampleSettings</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = { </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">maxNumberOfProblems:</span><span style="--shiki-dark:#B5CEA8;--shiki-light:#098658"> 1000</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> };</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">let</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> globalSettings</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">ExampleSettings</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">defaultSettings</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">// Cache the settings of all open documents</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">let</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> documentSettings</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">Map</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">&lt;</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">string</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">Thenable</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">&lt;</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">ExampleSettings</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">&gt;&gt; = </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">new</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> Map</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">();</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">connection</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">onDidChangeConfiguration</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">change</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> =&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">  if</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> (</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">hasConfigurationCapability</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">    // Reset all cached document settings</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    documentSettings</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">clear</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">();</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  } </span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">else</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">    globalSettings</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = &lt;</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">ExampleSettings</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">&gt;(</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      (</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">change</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">settings</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">languageServerExample</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> || </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">defaultSettings</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">)</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    );</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  }</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">  // Revalidate all open text documents</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  documents</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">all</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">().</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">forEach</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">validateTextDocument</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">});</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">function</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> getDocumentSettings</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">resource</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">string</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">): </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">Thenable</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">&lt;</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">ExampleSettings</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">&gt; {</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">  if</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> (!</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">hasConfigurationCapability</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">    return</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99"> Promise</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">resolve</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">globalSettings</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  }</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">  let</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> result</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">documentSettings</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">get</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">resource</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">  if</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> (!</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">result</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    result</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">connection</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">workspace</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">getConfiguration</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">({</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">      scopeUri:</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> resource</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">      section:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'languageServerExample'</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    });</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    documentSettings</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">set</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">resource</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">result</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  }</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">  return</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> result</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">// Only keep settings for open documents</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">documents</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">onDidClose</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">e</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> =&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  documentSettings</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">delete</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">e</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">document</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">uri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">});</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">// The content of a text document has changed. This event is emitted</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">// when the text document first opened or when its content has changed.</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">documents</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">onDidChangeContent</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">change</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> =&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">  validateTextDocument</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">change</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">document</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">});</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">async</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> function</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> validateTextDocument</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">textDocument</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">TextDocument</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">): </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">Promise</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">&lt;</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">void</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">&gt; {</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">  // In this simple example we get the settings for every validate run.</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">  let</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> settings</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">await</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> getDocumentSettings</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">textDocument</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">uri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">  // The validator creates diagnostics for all uppercase words length 2 and more</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">  let</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> text</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">textDocument</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">getText</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">();</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">  let</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> pattern</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> =</span><span style="--shiki-dark:#D16969;--shiki-light:#811F3F"> /</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#EE0000">\b</span><span style="--shiki-dark:#CE9178;--shiki-light:#D16969">[</span><span style="--shiki-dark:#D16969;--shiki-light:#811F3F">A-Z</span><span style="--shiki-dark:#CE9178;--shiki-light:#D16969">]</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#000000">{2,}</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#EE0000">\b</span><span style="--shiki-dark:#D16969;--shiki-light:#811F3F">/</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">g</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">  let</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> m</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">RegExpExecArray</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> | </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">null</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">  let</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> problems</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#B5CEA8;--shiki-light:#098658">0</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">  let</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> diagnostics</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">Diagnostic</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">[] = [];</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">  while</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> ((</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">m</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">pattern</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">exec</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">text</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">)) &amp;&amp; </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">problems</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> &lt; </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">settings</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">maxNumberOfProblems</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    problems</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">++;</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">    let</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> diagnostic</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">Diagnostic</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">      severity:</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> DiagnosticSeverity</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">Warning</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">      range:</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">        start:</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> textDocument</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">positionAt</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">m</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">index</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">),</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">        end:</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> textDocument</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">positionAt</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">m</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">index</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> + </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">m</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">[</span><span style="--shiki-dark:#B5CEA8;--shiki-light:#098658">0</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">].</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">length</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">)</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      },</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">      message:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> `</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">${</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">m</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">[</span><span style="--shiki-dark:#B5CEA8;--shiki-light:#098658">0</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">]</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> is all uppercase.`</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">      source:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'ex'</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    };</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">    if</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> (</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">hasDiagnosticRelatedInformationCapability</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">      diagnostic</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">relatedInformation</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = [</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">        {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">          location:</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">            uri:</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> textDocument</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">uri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">            range:</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> Object</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">assign</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">({}, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">diagnostic</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">range</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">)</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">          },</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">          message:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'Spelling matters'</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">        },</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">        {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">          location:</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">            uri:</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> textDocument</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">uri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">            range:</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> Object</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">assign</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">({}, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">diagnostic</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">range</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">)</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">          },</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">          message:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'Particularly for names'</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">        }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      ];</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    }</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    diagnostics</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">push</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">diagnostic</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  }</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">  // Send the computed diagnostics to VS Code.</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  connection</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">sendDiagnostics</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">({ </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">uri:</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> textDocument</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">uri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">diagnostics</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> });</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">connection</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">onDidChangeWatchedFiles</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">_change</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> =&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">  // Monitored files have change in VS Code</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  connection</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">console</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">log</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'We received a file change event'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">});</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">// This handler provides the initial list of the completion items.</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">connection</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">onCompletion</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  (</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">_textDocumentPosition</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">TextDocumentPositionParams</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">): </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">CompletionItem</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">[] </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">=&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">    // The pass parameter contains the position of the text document in</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">    // which code complete got requested. For the example we ignore this</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">    // info and always provide the same completion items.</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">    return</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> [</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">        label:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'TypeScript'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">        kind:</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> CompletionItemKind</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">Text</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">        data:</span><span style="--shiki-dark:#B5CEA8;--shiki-light:#098658"> 1</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      },</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">        label:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'JavaScript'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">        kind:</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> CompletionItemKind</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">Text</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">        data:</span><span style="--shiki-dark:#B5CEA8;--shiki-light:#098658"> 2</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    ];</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">// This handler resolves additional information for the item selected in</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">// the completion list.</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">connection</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">onCompletionResolve</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  (</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">item</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">CompletionItem</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">): </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">CompletionItem</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> =&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">    if</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> (</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">item</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">data</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> === </span><span style="--shiki-dark:#B5CEA8;--shiki-light:#098658">1</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">      item</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">detail</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'TypeScript details'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">      item</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">documentation</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'TypeScript documentation'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    } </span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">else</span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB"> if</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> (</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">item</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">data</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> === </span><span style="--shiki-dark:#B5CEA8;--shiki-light:#098658">2</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">      item</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">detail</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'JavaScript details'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">      item</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">documentation</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'JavaScript documentation'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    }</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">    return</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> item</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">// Make the text document manager listen on the connection</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">// for open, change and close text document events</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">documents</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">listen</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">connection</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">// Listen on the connection</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">connection</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">listen</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">();</span></span>
<span class="line"></span></code></pre>
<h3 id="adding-a-simple-validation" data-needslink="adding-a-simple-validation">Adding a Simple Validation</h3>
<p>To add document validation to the server, we add a listener to the text document manager that gets called whenever the content of a text document changes. It is then up to the server to decide when the best time is to validate a document. In the example implementation, the server validates the plain text document and flags all occurrences of words that use ALL CAPS. The corresponding code snippet looks like this:</p>
<pre class="shiki" data-lang="typescript" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">// The content of a text document has changed. This event is emitted</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">// when the text document first opened or when its content has changed.</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">documents</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">onDidChangeContent</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">async</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> change</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> =&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">  let</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> textDocument</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">change</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">document</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">  // In this simple example we get the settings for every validate run.</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">  let</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> settings</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">await</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> getDocumentSettings</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">textDocument</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">uri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">  // The validator creates diagnostics for all uppercase words length 2 and more</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">  let</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> text</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">textDocument</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">getText</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">();</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">  let</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> pattern</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> =</span><span style="--shiki-dark:#D16969;--shiki-light:#811F3F"> /</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#EE0000">\b</span><span style="--shiki-dark:#CE9178;--shiki-light:#D16969">[</span><span style="--shiki-dark:#D16969;--shiki-light:#811F3F">A-Z</span><span style="--shiki-dark:#CE9178;--shiki-light:#D16969">]</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#000000">{2,}</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#EE0000">\b</span><span style="--shiki-dark:#D16969;--shiki-light:#811F3F">/</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">g</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">  let</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> m</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">RegExpExecArray</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> | </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">null</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">  let</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> problems</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#B5CEA8;--shiki-light:#098658">0</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">  let</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> diagnostics</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">Diagnostic</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">[] = [];</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">  while</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> ((</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">m</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">pattern</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">exec</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">text</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">)) &amp;&amp; </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">problems</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> &lt; </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">settings</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">maxNumberOfProblems</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    problems</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">++;</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">    let</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> diagnostic</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">Diagnostic</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">      severity:</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> DiagnosticSeverity</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">Warning</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">      range:</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">        start:</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> textDocument</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">positionAt</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">m</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">index</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">),</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">        end:</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> textDocument</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">positionAt</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">m</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">index</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> + </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">m</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">[</span><span style="--shiki-dark:#B5CEA8;--shiki-light:#098658">0</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">].</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">length</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">)</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      },</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">      message:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> `</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">${</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">m</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">[</span><span style="--shiki-dark:#B5CEA8;--shiki-light:#098658">0</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">]</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> is all uppercase.`</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">      source:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'ex'</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    };</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">    if</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> (</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">hasDiagnosticRelatedInformationCapability</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">      diagnostic</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">relatedInformation</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = [</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">        {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">          location:</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">            uri:</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> textDocument</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">uri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">            range:</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> Object</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">assign</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">({}, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">diagnostic</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">range</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">)</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">          },</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">          message:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'Spelling matters'</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">        },</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">        {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">          location:</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">            uri:</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> textDocument</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">uri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">            range:</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> Object</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">assign</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">({}, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">diagnostic</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">range</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">)</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">          },</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">          message:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'Particularly for names'</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">        }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      ];</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    }</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    diagnostics</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">push</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">diagnostic</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  }</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">  // Send the computed diagnostics to VS Code.</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  connection</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">sendDiagnostics</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">({ </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">uri:</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> textDocument</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">uri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">diagnostics</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> });</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">});</span></span>
<span class="line"></span></code></pre>
<h3 id="diagnostics-tips-and-tricks" data-needslink="diagnostics-tips-and-tricks">Diagnostics Tips and Tricks</h3>
<ul><li>If the start and end positions are the same, VS Code will underline with a squiggle the word at that position.</li>
<li>If you want to underline with a squiggle until the end of the line, then set the character of the end position to Number.MAX_VALUE.</li>
</ul><p>To run the Language Server, do the following steps:</p>
<ul><li>Press <span class="dynamic-keybinding" data-commandid="workbench.action.tasks.build" data-osx="⇧⌘B" data-win="Ctrl+Shift+B" data-linux="Ctrl+Shift+B"><span class="keybinding">⇧⌘B</span> (Windows, Linux <span class="keybinding">Ctrl+Shift+B</span>)</span> to start the build task. The task compiles both the client and the server.</li>
<li>Open the <strong>Run</strong> view, select the <strong>Launch Client</strong> launch configuration, and press the <strong>Start Debugging</strong> button to launch an additional <strong>Extension Development Host</strong> instance of VS Code that executes the extension code.</li>
<li>Create a <code>test.txt</code> file in the root folder and paste the following content:</li>
</ul><pre class="shiki" data-lang="text" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span>TypeScript lets you write JavaScript the way you really want to.</span></span>
<span class="line"><span>TypeScript is a typed superset of JavaScript that compiles to plain JavaScript.</span></span>
<span class="line"><span>ANY browser. ANY host. ANY OS. Open Source.</span></span>
<span class="line"><span></span></span></code></pre>
<p>The <strong>Extension Development Host</strong> instance will then look like this:</p>
<p><img src="/assets/api/language-extensions/language-server-extension-guide/validation.png" alt="Validating a text file" loading="lazy"></p>
<h3 id="debugging-both-client-and-server" data-needslink="debugging-both-client-and-server">Debugging both Client and Server</h3>
<p>Debugging the client code is as easy as debugging a normal extension. Set a breakpoint in the client code and debug the extension by pressing <span class="dynamic-keybinding" data-commandid="workbench.action.debug.start" data-osx="F5" data-win="F5" data-linux="F5"><span class="keybinding">F5</span></span>.</p>
<p><img src="/assets/api/language-extensions/language-server-extension-guide/debugging-client.png" alt="Debugging the client" loading="lazy"></p>
<p>Since the server is started by the <code>LanguageClient</code> running in the extension (client), we need to attach a debugger to the running server. To do so, switch to the <strong>Run and Debug</strong> view and select the launch configuration <strong>Attach to Server</strong> and press <span class="dynamic-keybinding" data-commandid="workbench.action.debug.start" data-osx="F5" data-win="F5" data-linux="F5"><span class="keybinding">F5</span></span>. This will attach the debugger to the server.</p>
<p><img src="/assets/api/language-extensions/language-server-extension-guide/debugging-server.png" alt="Debugging the server" loading="lazy"></p>
<h3 id="logging-support-for-language-server" data-needslink="logging-support-for-language-server">Logging Support for Language Server</h3>
<p>If you are using <code>vscode-languageclient</code> to implement the client, you can specify a setting <code>[langId].trace.server</code> that instructs the Client to log communications between Language Client / Server to a channel of the Language Client's <code>name</code>.</p>
<p>For <strong>lsp-sample</strong>, you can set this setting: <code>"languageServerExample.trace.server": "verbose"</code>. Now head to the channel "Language Server Example". You should see the logs:</p>
<p><img src="/assets/api/language-extensions/language-server-extension-guide/lsp-log.png" alt="LSP Log" loading="lazy"></p>
<h3 id="using-configuration-settings-in-the-server" data-needslink="using-configuration-settings-in-the-server">Using Configuration Settings in the Server</h3>
<p>When writing the client part of the extension, we already defined a setting to control the maximum numbers of problems reported. We also wrote code on the server side to read these settings from the client:</p>
<pre class="shiki" data-lang="typescript" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">function</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> getDocumentSettings</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">resource</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">string</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">): </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">Thenable</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">&lt;</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">ExampleSettings</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">&gt; {</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">  if</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> (!</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">hasConfigurationCapability</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">    return</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99"> Promise</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">resolve</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">globalSettings</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  }</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">  let</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> result</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">documentSettings</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">get</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">resource</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">  if</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> (!</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">result</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    result</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">connection</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">workspace</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">getConfiguration</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">({</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">      scopeUri:</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> resource</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">      section:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'languageServerExample'</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    });</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    documentSettings</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">set</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">resource</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">result</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  }</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">  return</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> result</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<p>The only thing we need to do now is to listen to configuration changes on the server side and if a setting changes, revalidate the open text documents. To be able to reuse the validate logic of the document change event handling, we extract the code into a <code>validateTextDocument</code> function and modify the code to honor a <code>maxNumberOfProblems</code> variable:</p>
<pre class="shiki" data-lang="typescript" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">async</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> function</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> validateTextDocument</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">textDocument</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">TextDocument</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">): </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">Promise</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">&lt;</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">void</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">&gt; {</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">  // In this simple example we get the settings for every validate run.</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">  let</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> settings</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">await</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> getDocumentSettings</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">textDocument</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">uri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">  // The validator creates diagnostics for all uppercase words length 2 and more</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">  let</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> text</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">textDocument</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">getText</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">();</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">  let</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> pattern</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> =</span><span style="--shiki-dark:#D16969;--shiki-light:#811F3F"> /</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#EE0000">\b</span><span style="--shiki-dark:#CE9178;--shiki-light:#D16969">[</span><span style="--shiki-dark:#D16969;--shiki-light:#811F3F">A-Z</span><span style="--shiki-dark:#CE9178;--shiki-light:#D16969">]</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#000000">{2,}</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#EE0000">\b</span><span style="--shiki-dark:#D16969;--shiki-light:#811F3F">/</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">g</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">  let</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> m</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">RegExpExecArray</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> | </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">null</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">  let</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> problems</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#B5CEA8;--shiki-light:#098658">0</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">  let</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> diagnostics</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">Diagnostic</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">[] = [];</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">  while</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> ((</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">m</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">pattern</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">exec</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">text</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">)) &amp;&amp; </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">problems</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> &lt; </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">settings</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">maxNumberOfProblems</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    problems</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">++;</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">    let</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> diagnostic</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">Diagnostic</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">      severity:</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> DiagnosticSeverity</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">Warning</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">      range:</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">        start:</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> textDocument</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">positionAt</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">m</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">index</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">),</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">        end:</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> textDocument</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">positionAt</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">m</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">index</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> + </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">m</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">[</span><span style="--shiki-dark:#B5CEA8;--shiki-light:#098658">0</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">].</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">length</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">)</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      },</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">      message:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> `</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">${</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">m</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">[</span><span style="--shiki-dark:#B5CEA8;--shiki-light:#098658">0</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">]</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> is all uppercase.`</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">      source:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'ex'</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    };</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">    if</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> (</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">hasDiagnosticRelatedInformationCapability</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">      diagnostic</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">relatedInformation</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = [</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">        {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">          location:</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">            uri:</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> textDocument</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">uri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">            range:</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> Object</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">assign</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">({}, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">diagnostic</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">range</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">)</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">          },</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">          message:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'Spelling matters'</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">        },</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">        {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">          location:</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">            uri:</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> textDocument</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">uri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">            range:</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> Object</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">assign</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">({}, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">diagnostic</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">range</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">)</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">          },</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">          message:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'Particularly for names'</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">        }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      ];</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    }</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    diagnostics</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">push</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">diagnostic</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  }</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">  // Send the computed diagnostics to VS Code.</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  connection</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">sendDiagnostics</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">({ </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">uri:</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> textDocument</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">uri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">diagnostics</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> });</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<p>The handling of the configuration change is done by adding a notification handler for configuration changes to the connection. The corresponding code looks like this:</p>
<pre class="shiki" data-lang="typescript" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">connection</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">onDidChangeConfiguration</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">change</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> =&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">  if</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> (</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">hasConfigurationCapability</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">    // Reset all cached document settings</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    documentSettings</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">clear</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">();</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  } </span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">else</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">    globalSettings</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = &lt;</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">ExampleSettings</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">&gt;(</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      (</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">change</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">settings</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">languageServerExample</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> || </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">defaultSettings</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">)</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    );</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  }</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">  // Revalidate all open text documents</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  documents</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">all</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">().</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">forEach</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">validateTextDocument</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">});</span></span>
<span class="line"></span></code></pre>
<p>Starting the client again and changing the setting to maximum report 1 problem results in the following validation:</p>
<p><img src="/assets/api/language-extensions/language-server-extension-guide/validationOneProblem.png" alt="Maximum One Problem" loading="lazy"></p>
<h3 id="adding-additional-language-features" data-needslink="adding-additional-language-features">Adding additional Language Features</h3>
<p>The first interesting feature a language server usually implements is validation of documents. In that sense, even a linter counts as a language server and in VS Code linters are usually implemented as language servers (see <a href="https://github.com/microsoft/vscode-eslint" class="external-link" target="_blank">eslint</a> and <a href="https://github.com/microsoft/vscode-jshint" class="external-link" target="_blank">jshint</a> for examples). But there is more to language servers. They can provide code completion, Find All References, or Go To Definition. The example code below adds code completion to the server. It proposes the two words 'TypeScript' and 'JavaScript'.</p>
<pre class="shiki" data-lang="typescript" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">// This handler provides the initial list of the completion items.</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">connection</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">onCompletion</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  (</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">_textDocumentPosition</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">TextDocumentPositionParams</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">): </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">CompletionItem</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">[] </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">=&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">    // The pass parameter contains the position of the text document in</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">    // which code complete got requested. For the example we ignore this</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">    // info and always provide the same completion items.</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">    return</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> [</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">        label:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'TypeScript'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">        kind:</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> CompletionItemKind</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">Text</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">        data:</span><span style="--shiki-dark:#B5CEA8;--shiki-light:#098658"> 1</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      },</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">        label:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'JavaScript'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">        kind:</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> CompletionItemKind</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">Text</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">        data:</span><span style="--shiki-dark:#B5CEA8;--shiki-light:#098658"> 2</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    ];</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">// This handler resolves additional information for the item selected in</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">// the completion list.</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">connection</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">onCompletionResolve</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  (</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">item</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">CompletionItem</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">): </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">CompletionItem</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> =&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">    if</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> (</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">item</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">data</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> === </span><span style="--shiki-dark:#B5CEA8;--shiki-light:#098658">1</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">      item</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">detail</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'TypeScript details'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">      item</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">documentation</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'TypeScript documentation'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    } </span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">else</span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB"> if</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> (</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">item</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">data</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> === </span><span style="--shiki-dark:#B5CEA8;--shiki-light:#098658">2</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">      item</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">detail</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'JavaScript details'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">      item</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">documentation</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'JavaScript documentation'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    }</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">    return</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> item</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"></span></code></pre>
<p>The <code>data</code> fields are used to uniquely identify a completion item in the resolve handler. The data property is transparent for the protocol. Since the underlying message passing protocol is JSON-based, the data field should only hold data that is serializable to and from JSON.</p>
<p>All that is missing is to tell VS Code that the server supports code completion requests. To do so, flag the corresponding capability in the initialize handler:</p>
<pre class="shiki" data-lang="typescript" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">connection</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">onInitialize</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">((</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">params</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">): </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">InitializeResult</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> =&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    ...</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">    return</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">        capabilities:</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">            ...</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">            // Tell the client that the server supports code completion</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">            completionProvider</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">                resolveProvider:</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> true</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">            }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">        }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    };</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">});</span></span>
<span class="line"></span></code></pre>
<p>The screenshot below shows the completed code running on a plain text file:</p>
<p><img src="/assets/api/language-extensions/language-server-extension-guide/codeComplete.png" alt="Code Complete" loading="lazy"></p>
<h3 id="testing-the-language-server" data-needslink="testing-the-language-server">Testing The Language Server</h3>
<p>To create a high-quality Language Server, we need to build a good test suite covering its functionalities. There are two common ways of testing Language Servers:</p>
<ul><li>Unit Test: This is useful if you want to test specific functionalities in Language Servers by mocking up all the information being sent to it. VS Code's <a href="https://github.com/microsoft/vscode-html-languageservice" class="external-link" target="_blank">HTML</a> / <a href="https://github.com/microsoft/vscode-css-languageservice" class="external-link" target="_blank">CSS</a> / <a href="https://github.com/microsoft/vscode-json-languageservice" class="external-link" target="_blank">JSON</a> Language Servers take this approach to testing. The LSP npm modules also use this approach. See <a href="https://github.com/microsoft/vscode-languageserver-node/blob/main/protocol/src/node/test/connection.test.ts" class="external-link" target="_blank">here</a> for some unit test written using the npm protocol module.</li>
<li>End-to-End Test: This is similar to <a href="/api/working-with-extensions/testing-extension">VS Code extension test</a>. The benefit of this approach is that it runs the test by instantiating a VS Code instance with a workspace, opening the file, activating the Language Client / Server, and running <a href="/api/references/commands">VS Code commands</a>. This approach is superior if you have files, settings, or dependencies (such as <code>node_modules</code>) which are hard or impossible to mock. The popular <a href="https://github.com/microsoft/vscode-python" class="external-link" target="_blank">Python</a> extension takes this approach to testing.</li>
</ul><p>It is possible to do Unit Test in any testing framework of your choice. Here we describe how to do End-to-End testing for Language Server Extension.</p>
<p>Open <code>.vscode/launch.json</code>, and you can find a <code>E2E</code> test target:</p>
<pre class="shiki" data-lang="json" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">{</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "name"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"Language Server E2E Test"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "type"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"extensionHost"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "request"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"launch"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "runtimeExecutable"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"${execPath}"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "args"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">    "--extensionDevelopmentPath=${workspaceRoot}"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">    "--extensionTestsPath=${workspaceRoot}/client/out/test/index"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">    "${workspaceRoot}/client/testFixture"</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  ],</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "outFiles"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"${workspaceRoot}/client/out/test/**/*.js"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">]</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<p>If you run this debug target, it will launch a VS Code instance with <code>client/testFixture</code> as the active workspace. VS Code will then proceed to execute all tests in <code>client/src/test</code>. As a debugging tip, you can set breakpoints in TypeScript files in <code>client/src/test</code> and they will be hit.</p>
<p>Let's take a look at the <code>completion.test.ts</code> file:</p>
<pre class="shiki" data-lang="ts" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">import</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> *</span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB"> as</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> vscode</span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB"> from</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'vscode'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">import</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> *</span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB"> as</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> assert</span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB"> from</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'assert'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">import</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> { </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">getDocUri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">activate</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> } </span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">from</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> './helper'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">suite</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'Should do completion'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, () </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">=&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">  const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> docUri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">getDocUri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'completion.txt'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">  test</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'Completes JS/TS in txt file'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">async</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> () </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">=&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">    await</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> testCompletion</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">docUri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">new</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">Position</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#B5CEA8;--shiki-light:#098658">0</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#B5CEA8;--shiki-light:#098658">0</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">), {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">      items:</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> [</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">        { </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">label:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'JavaScript'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">kind:</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">CompletionItemKind</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">Text</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> },</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">        { </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">label:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'TypeScript'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">kind:</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">CompletionItemKind</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">Text</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      ]</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    });</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  });</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">});</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">async</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> function</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> testCompletion</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  docUri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">Uri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  position</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">Position</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  expectedCompletionList</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">CompletionList</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">  await</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> activate</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">docUri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">  // Executing the command `vscode.executeCompletionItemProvider` to simulate triggering completion</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">  const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> actualCompletionList</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = (</span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">await</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">commands</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">executeCommand</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">    'vscode.executeCompletionItemProvider'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    docUri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    position</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  )) </span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">as</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99"> vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">CompletionList</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  assert</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">ok</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">actualCompletionList</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">items</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">length</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> &gt;= </span><span style="--shiki-dark:#B5CEA8;--shiki-light:#098658">2</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  expectedCompletionList</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">items</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">forEach</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">((</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">expectedItem</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">i</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">=&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">    const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> actualItem</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">actualCompletionList</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">items</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">[</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">i</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">];</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    assert</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">equal</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">actualItem</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">label</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">expectedItem</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">label</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    assert</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">equal</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">actualItem</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">kind</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">expectedItem</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">kind</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  });</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<p>In this test, we:</p>
<ul><li>Activate the extension.</li>
<li>Run the command <code>vscode.executeCompletionItemProvider</code> with a URI and a position to simulate completion trigger.</li>
<li>Assert the returned completion items against our expected completion items.</li>
</ul><p>Let's dive a bit deeper into the <code>activate(docURI)</code> function. It is defined in <code>client/src/test/helper.ts</code>:</p>
<pre class="shiki" data-lang="ts" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">import</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> *</span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB"> as</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> vscode</span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB"> from</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'vscode'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">import</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> *</span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB"> as</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> path</span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB"> from</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'path'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">export</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> let</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> doc</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">TextDocument</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">export</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> let</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> editor</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">TextEditor</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">export</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> let</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> documentEol</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">string</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">export</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> let</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> platformEol</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">string</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">/**</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000"> * Activates the vscode.lsp-sample extension</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000"> */</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">export</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> async</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> function</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> activate</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">docUri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">Uri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">  // The extensionId is `publisher.name` from package.json</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">  const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> ext</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">extensions</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">getExtension</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'vscode-samples.lsp-sample'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">)!;</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">  await</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> ext</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">activate</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">();</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">  try</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    doc</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">await</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">workspace</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">openTextDocument</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">docUri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    editor</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">await</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">window</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">showTextDocument</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">doc</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">    await</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> sleep</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#B5CEA8;--shiki-light:#098658">2000</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">); </span><span style="--shiki-dark:#6A9955;--shiki-light:#008000">// Wait for server activation</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  } </span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">catch</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> (</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">e</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    console</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">error</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">e</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">async</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> function</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> sleep</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">ms</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">number</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">  return</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> new</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99"> Promise</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">resolve</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> =&gt;</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> setTimeout</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">resolve</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">ms</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">));</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<p>In the activation part, we:</p>
<ul><li>Get the extension using the <code>{publisher.name}.{extensionId}</code>, as defined in <code>package.json</code>.</li>
<li>Open the specified document, and show it in the active text editor.</li>
<li>Sleep for 2 seconds, so we are sure the Language Server is instantiated.</li>
</ul><p>After the preparation, we can run the <a href="/api/references/commands">VS Code Commands</a> corresponding to each language feature, and assert against the returned result.</p>
<p>There is one more test that covers the diagnostics feature that we just implemented. Check it out at <code>client/src/test/diagnostics.test.ts</code>.</p>
<h2 id="advanced-topics" data-needslink="advanced-topics">Advanced Topics</h2>
<p>So far, this guide covered:</p>
<ul><li>A brief overview of Language Server and Language Server Protocol.</li>
<li>Architecture of a Language Server extension in VS Code</li>
<li>The <strong>lsp-sample</strong> extension, and how to develop/debug/inspect/test it.</li>
</ul><p>There are some more advanced topics we could not fit in to this guide. We will include links to these resources for further studying of Language Server development.</p>
<h3 id="additional-language-server-features" data-needslink="additional-language-server-features">Additional Language Server features</h3>
<p>The following language features are currently supported in a language server along with code completions:</p>
<ul><li><em>Document Highlights</em>: highlights all 'equal' symbols in a text document.</li>
<li><em>Hover</em>: provides hover information for a symbol selected in a text document.</li>
<li><em>Signature Help</em>: provides signature help for a symbol selected in a text document.</li>
<li><em>Goto Definition</em>: provides go to definition support for a symbol selected in a text document.</li>
<li><em>Goto Type Definition</em>: provides go to type/interface definition support for a symbol selected in a text document.</li>
<li><em>Goto Implementation</em>: provides go to implementation definition support for a symbol selected in a text document.</li>
<li><em>Find References</em>: finds all project-wide references for a symbol selected in a text document.</li>
<li><em>List Document Symbols</em>: lists all symbols defined in a text document.</li>
<li><em>List Workspace Symbols</em>: lists all project-wide symbols.</li>
<li><em>Code Actions</em>: compute commands to run (typically beautify/refactor) for a given text document and range.</li>
<li><em>CodeLens</em>: compute CodeLens statistics for a given text document.</li>
<li><em>Document Formatting</em>: this includes formatting of whole documents, document ranges and formatting on type.</li>
<li><em>Rename</em>: project-wide rename of a symbol.</li>
<li><em>Document Links</em>: compute and resolve links inside a document.</li>
<li><em>Document Colors</em>: compute and resolve colors inside a document to provide color picker in editor.</li>
</ul><p>The <a href="/api/language-extensions/programmatic-language-features">Programmatic Language Features</a> topic describes each of the language features above and provides guidance on how to implement them either through the language server protocol or by using the extensibility API directly from your extension.</p>
<h3 id="incremental-text-document-synchronization" data-needslink="incremental-text-document-synchronization">Incremental Text Document Synchronization</h3>
<p>The example uses the simple text document manager provided by the <code>vscode-languageserver</code> module to synchronize documents between VS Code and the language server.</p>
<p>This has two drawbacks:</p>
<ul><li>Lots of data is transferred since the whole content of a text document is sent to the server repeatedly.</li>
<li>If an existing language library is used, such libraries usually support incremental document updates to avoid unnecessary parsing and abstract syntax tree creation.</li>
</ul><p>The protocol therefore supports incremental document synchronization as well.</p>
<p>To make use of incremental document synchronization, a server needs to install three notification handlers:</p>
<ul><li><em>onDidOpenTextDocument</em>: is called when a text document is opened in VS Code.</li>
<li><em>onDidChangeTextDocument</em>: is called when the content of a text document changes in VS Code.</li>
<li><em>onDidCloseTextDocument</em>: is called when a text document is closed in VS Code.</li>
</ul><p>Below is a code snippet that illustrates how to hook these notification handlers on a connection and how to return the right capability on initialize:</p>
<pre class="shiki" data-lang="typescript" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">connection</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">onInitialize</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">((</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">params</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">): </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">InitializeResult</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> =&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    ...</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">    return</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">        capabilities:</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">            // Enable incremental document sync</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">            textDocumentSync:</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> TextDocumentSyncKind</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">Incremental</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">            ...</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">        }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    };</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">});</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">connection</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">onDidOpenTextDocument</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">((</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">params</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">=&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">    // A text document was opened in VS Code.</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">    // params.uri uniquely identifies the document. For documents stored on disk, this is a file URI.</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">    // params.text the initial full content of the document.</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">});</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">connection</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">onDidChangeTextDocument</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">((</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">params</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">=&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">    // The content of a text document has change in VS Code.</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">    // params.uri uniquely identifies the document.</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">    // params.contentChanges describe the content changes to the document.</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">});</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">connection</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">onDidCloseTextDocument</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">((</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">params</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">=&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">    // A text document was closed in VS Code.</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">    // params.uri uniquely identifies the document.</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">});</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">/*</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">Make the text document manager listen on the connection</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">for open, change and close text document events.</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">Comment out this line to allow `connection.onDidOpenTextDocument`,</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">`connection.onDidChangeTextDocument`, and `connection.onDidCloseTextDocument` to handle the events</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">*/</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">// documents.listen(connection);</span></span>
<span class="line"></span></code></pre>
<h3 id="using-vs-code-api-directly-to-implement-language-features" data-needslink="using-vs-code-api-directly-to-implement-language-features">Using VS Code API directly to implement Language Features</h3>
<p>While Language Servers have many benefits, they are not the only option for extending the editing capabilities of VS Code. In the cases when you want to add some simple language features for a type of document, consider using <code>vscode.languages.register[LANGUAGE_FEATURE]Provider</code> as an option.</p>
<p>Here is a <a href="https://github.com/microsoft/vscode-extension-samples/tree/main/completions-sample" class="external-link" target="_blank"><code>completions-sample</code></a> using <code>vscode.languages.registerCompletionItemProvider</code> to add a few snippets as completions for plain text files.</p>
<p>More samples illustrating the usage of VS Code API can be found at <a href="https://github.com/microsoft/vscode-extension-samples" class="external-link" target="_blank">https://github.com/microsoft/vscode-extension-samples</a>.</p>
<h3 id="error-tolerant-parser-for-language-server" data-needslink="error-tolerant-parser-for-language-server">Error Tolerant Parser for Language Server</h3>
<p>Most of the time, the code in the editor is incomplete and syntactically incorrect, but developers would still expect autocomplete and other language features to work. Therefore, an error tolerant parser is necessary for a Language Server: The parser generates meaningful AST from partially complete code, and the Language Server provides language features based on the AST.</p>
<p>When we were improving PHP support in VS Code, we realized the official PHP parser is not error tolerant and cannot be reused directly in the Language Server. Therefore, we worked on <a href="https://github.com/microsoft/tolerant-php-parser" class="external-link" target="_blank">Microsoft/tolerant-php-parser</a> and left detailed <a href="https://github.com/microsoft/tolerant-php-parser/blob/master/docs/HowItWorks.md" class="external-link" target="_blank">notes</a> that might help Language Server authors who need to implement an error tolerant parser.</p>
<h2 id="common-questions" data-needslink="common-questions">Common questions</h2>
<h3 id="when-i-try-to-attach-to-the-server-i-get-cannot-connect-to-runtime-process-timeout-after-5000-ms" data-needslink="when-i-try-to-attach-to-the-server-i-get-cannot-connect-to-runtime-process-timeout-after-5000-ms">When I try to attach to the server, I get "cannot connect to runtime process (timeout after 5000 ms)"?</h3>
<p>You will see this timeout error if the server isn't running when you try to attach the debugger. The client starts the language server so make sure you have started the client in order to have a running server. You may also need to disable your client breakpoints if they are interfering with starting the server.</p>
<h3 id="i-have-read-through-this-guide-and-the-lsp-specificationhttpsmicrosoft.github.iolanguageserverprotocol-but-i-still-have-unresolved-questions.-where-can-i-get-help" data-needslink="i-have-read-through-this-guide-and-the-lsp-specificationhttpsmicrosoft.github.iolanguageserverprotocol-but-i-still-have-unresolved-questions.-where-can-i-get-help">I have read through this guide and the <a href="https://microsoft.github.io/language-server-protocol/" class="external-link" target="_blank">LSP Specification</a>, but I still have unresolved questions. Where can I get help?</h3>
<p>Please open an issue at <a href="https://github.com/microsoft/language-server-protocol" class="external-link" target="_blank">https://github.com/microsoft/language-server-protocol</a>.</p>

				<div class="feedback" data-edit-url="https://vscode.dev/github/microsoft/vscode-docs/blob/main/api/language-extensions/language-server-extension-guide.md"></div>
				
				<div class="body-footer">6/3/2026</div>
				
            </main><aside class="docs-right-sidebar hidden-xs"><div class="docs-markdown-actions">
                    <div class="docs-markdown-dropdown" data-raw-url="/raw/api/language-extensions/language-server-extension-guide.md">
                        <button type="button" class="docs-markdown-btn-main" data-action="copy-markdown" aria-label="Copy as Markdown">
                            <span class="codicon codicon-copy" aria-hidden="true"></span>
                            <span>Copy as Markdown</span>
                        </button>
                        <button type="button" class="docs-markdown-btn-trigger" aria-haspopup="true" aria-expanded="false" aria-label="More Markdown options">
                            <span class="codicon codicon-chevron-down docs-markdown-chevron" aria-hidden="true"></span>
                        </button>
                        <ul class="docs-markdown-menu" role="menu" aria-label="Markdown options"><li role="menuitem" tabindex="0" data-action="copy-markdown">
                                <span class="codicon codicon-copy" aria-hidden="true"></span>
                                <span>Copy as Markdown</span>
                            </li>
                            <li role="menuitem" tabindex="0" data-action="view-markdown">
                                <span class="codicon codicon-file" aria-hidden="true"></span>
                                <span>View as Markdown</span>
                                <span class="codicon codicon-link-external" aria-hidden="true"></span>
                            </li>
                        </ul></div>
                </div>
                <nav id="docs-subnavbar" aria-label="On Page"><h4><span class="sr-only">On this page there are 4 sections</span><span aria-hidden="true">On this page</span></h4>
                    <ul class="nav"><li><a href="#why-language-server">Why Language Server?</a></li>
                        
                        <li><a href="#implementing-a-language-server">Implementing a Language Server</a></li>
                        
                        <li><a href="#advanced-topics">Advanced Topics</a></li>
                        
                        <li><a href="#common-questions">Common questions</a></li>
                        
                    </ul></nav></aside></div>
		<div class="docs-mobile-widgets visible-xs">
			<div class="connect-widget"></div>
		</div>
	</div>
</div>
		</main>