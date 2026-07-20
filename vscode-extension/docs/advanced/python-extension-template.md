# Authoring Python Extensions

> 源文档: [https://code.visualstudio.com/api/advanced-topics/python-extension-template](https://code.visualstudio.com/api/advanced-topics/python-extension-template)

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
			    
			<li class="panel collapsed">
			  <a class="area" role="button" href="#language-extensions-articles" data-parent="#main-nav" data-toggle="collapse">Language Extensions</a>
			  <ul id="language-extensions-articles" class="collapse "><li>
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
			          
			        <li>
			          <a href="/api/language-extensions/language-server-extension-guide">Language Server Extension Guide</a>
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
			    
			<li class="panel active expanded">
			  <a class="area" role="button" href="#advanced-topics-articles" data-parent="#main-nav" data-toggle="collapse">Advanced Topics</a>
			  <ul id="advanced-topics-articles" class="collapse in"><li>
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
			          
			        <li class="active">
			          <a href="/api/advanced-topics/python-extension-template" aria-label="Current Page: Python Extension Template">Python Extension Template</a>
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
				<select id="small-nav-dropdown" aria-label="topics"><option value="/api">Overview</option><optgroup label="Get Started"><option value="/api/get-started/your-first-extension">Your First Extension</option><option value="/api/get-started/extension-anatomy">Extension Anatomy</option><option value="/api/get-started/wrapping-up">Wrapping Up</option></optgroup><optgroup label="Extension Capabilities"><option value="/api/extension-capabilities/overview">Overview</option><option value="/api/extension-capabilities/common-capabilities">Common Capabilities</option><option value="/api/extension-capabilities/theming">Theming</option><option value="/api/extension-capabilities/extending-workbench">Extending Workbench</option></optgroup><optgroup label="Extension Guides"><option value="/api/extension-guides/overview">Overview</option><optgroup label="Extension Guides - AI"><option value="/api/extension-guides/ai/ai-extensibility-overview">AI Extensibility</option><option value="/api/extension-guides/ai/tools">Language Model Tool</option><option value="/api/extension-guides/ai/mcp">MCP Dev Guide</option><option value="/api/extension-guides/ai/chat">Chat Participant</option><option value="/api/extension-guides/ai/chat-tutorial">Chat Tutorial</option><option value="/api/extension-guides/ai/language-model">Language Model</option><option value="/api/extension-guides/ai/language-model-tutorial">Language Model Tutorial</option><option value="/api/extension-guides/ai/language-model-chat-provider">Language Model Chat Provider</option><option value="/api/extension-guides/ai/prompt-tsx">Prompt TSX</option></optgroup><option value="/api/extension-guides/command">Command</option><option value="/api/extension-guides/color-theme">Color Theme</option><option value="/api/extension-guides/file-icon-theme">File Icon Theme</option><option value="/api/extension-guides/product-icon-theme">Product Icon Theme</option><option value="/api/extension-guides/tree-view">Tree View</option><option value="/api/extension-guides/webview">Webview</option><option value="/api/extension-guides/notebook">Notebook</option><option value="/api/extension-guides/custom-editors">Custom Editors</option><option value="/api/extension-guides/virtual-documents">Virtual Documents</option><option value="/api/extension-guides/virtual-workspaces">Virtual Workspaces</option><option value="/api/extension-guides/web-extensions">Web Extensions</option><option value="/api/extension-guides/workspace-trust">Workspace Trust</option><option value="/api/extension-guides/task-provider">Task Provider</option><option value="/api/extension-guides/scm-provider">Source Control</option><option value="/api/extension-guides/debugger-extension">Debugger Extension</option><option value="/api/extension-guides/markdown-extension">Markdown Extension</option><option value="/api/extension-guides/testing">Test Extension</option><option value="/api/extension-guides/custom-data-extension">Custom Data Extension</option><option value="/api/extension-guides/telemetry">Telemetry</option></optgroup><optgroup label="UX Guidelines"><option value="/api/ux-guidelines/overview">Overview</option><option value="/api/ux-guidelines/activity-bar">Activity Bar</option><option value="/api/ux-guidelines/sidebars">Sidebars</option><option value="/api/ux-guidelines/panel">Panel</option><option value="/api/ux-guidelines/status-bar">Status Bar</option><option value="/api/ux-guidelines/views">Views</option><option value="/api/ux-guidelines/editor-actions">Editor Actions</option><option value="/api/ux-guidelines/quick-picks">Quick Picks</option><option value="/api/ux-guidelines/command-palette">Command Palette</option><option value="/api/ux-guidelines/notifications">Notifications</option><option value="/api/ux-guidelines/webviews">Webviews</option><option value="/api/ux-guidelines/context-menus">Context Menus</option><option value="/api/ux-guidelines/walkthroughs">Walkthroughs</option><option value="/api/ux-guidelines/settings">Settings</option></optgroup><optgroup label="Language Extensions"><option value="/api/language-extensions/overview">Overview</option><option value="/api/language-extensions/syntax-highlight-guide">Syntax Highlight Guide</option><option value="/api/language-extensions/semantic-highlight-guide">Semantic Highlight Guide</option><option value="/api/language-extensions/snippet-guide">Snippet Guide</option><option value="/api/language-extensions/language-configuration-guide">Language Configuration Guide</option><option value="/api/language-extensions/programmatic-language-features">Programmatic Language Features</option><option value="/api/language-extensions/language-server-extension-guide">Language Server Extension Guide</option><option value="/api/language-extensions/embedded-languages">Embedded Languages</option></optgroup><optgroup label="Testing and Publishing"><option value="/api/working-with-extensions/testing-extension">Testing Extensions</option><option value="/api/working-with-extensions/publishing-extension">Publishing Extensions</option><option value="/api/working-with-extensions/bundling-extension">Bundling Extensions</option><option value="/api/working-with-extensions/continuous-integration">Continuous Integration</option></optgroup><optgroup label="Advanced Topics"><option value="/api/advanced-topics/extension-host">Extension Host</option><option value="/api/advanced-topics/remote-extensions">Remote Development and Codespaces</option><option value="/api/advanced-topics/using-proposed-api">Using Proposed API</option><option value="/api/advanced-topics/tslint-eslint-migration">Migrate from TSLint to ESLint</option><option value="/api/advanced-topics/python-extension-template" selected>Python Extension Template</option></optgroup><optgroup label="References"><option value="/api/references/vscode-api">VS Code API</option><option value="/api/references/contribution-points">Contribution Points</option><option value="/api/references/activation-events">Activation Events</option><option value="/api/references/extension-manifest">Extension Manifest</option><option value="/api/references/commands">Built-In Commands</option><option value="/api/references/when-clause-contexts">When Clause Contexts</option><option value="/api/references/theme-color">Theme Color</option><option value="/api/references/icons-in-labels">Product Icon Reference</option><option value="/api/references/document-selector">Document Selector</option></optgroup></select></nav></aside><div class="docs-content-wrapper">
			
			<main class="docs-main-content body"><h1>Authoring Python Extensions</h1>
<blockquote><p><strong>Note</strong>: If you are new to VS Code extension authoring, you may want to read the <a href="/api/get-started/your-first-extension">Your First Extension</a> tutorial first and try creating a simple Hello World extension.</p>
</blockquote><p>The <a href="https://marketplace.visualstudio.com/items?itemName=ms-python.python" class="external-link" target="_blank">Python</a> extension provides APIs for other extensions to work with Python environments available on the user's machine. Check out <a href="https://www.npmjs.com/package/@vscode/python-extension" class="external-link" target="_blank">@vscode/python-extension</a> npm module that includes types and helper utilities to access these APIs from your extension.</p>
<h2 id="python-extension-template" data-needslink="python-extension-template">Python extension template</h2>
<p>The <a href="https://github.com/microsoft/vscode-python-tools-extension-template" class="external-link" target="_blank">Python extension template</a> helps get you started building a Visual Studio Code extension for your favorite Python tool. It could be a linter, formatter, or code analysis, or all of those together. The template will give you the basic building blocks you need to build an extension that integrates your tool into VS Code, and it already has access to the Python APIs mentioned above.</p>
<h2 id="programming-languages-and-frameworks" data-needslink="programming-languages-and-frameworks">Programming languages and frameworks</h2>
<p>The extension template has two parts, the extension part and language server part. The extension part is written in TypeScript, and language server part is written in Python over the <code>pygls</code> (Python language server) library.</p>
<p>You will mostly be working on the Python part of the code when using this template. You will be integrating your tool with the extension part using the <a href="https://microsoft.github.io/language-server-protocol" class="external-link" target="_blank">Language Server Protocol</a>. <code>pygls</code> currently works on the <a href="https://microsoft.github.io/language-server-protocol/specifications/specification-3-16" class="external-link" target="_blank">version 3.16 of LSP</a>.</p>
<p>The TypeScript part handles working with VS Code and its UI. The extension template comes with a few settings built-in that can be used by your tool. If you need to add new settings to support your tool, you will have to work with a bit of TypeScript. The extension template has examples for a few settings and you can also look at <a href="#_examples">extensions developed</a> by our team for some of the popular tools.</p>
<h2 id="requirements" data-needslink="requirements">Requirements</h2>
<ol><li>VS Code 1.64.0 or greater</li>
<li>Python 3.7 or greater</li>
<li>node &gt;= 14.19.0</li>
<li>npm &gt;= 8.3.0 (<code>npm</code> is installed with node, check npm version, use <code>npm install -g npm@8.3.0</code> to update)</li>
<li><a href="https://marketplace.visualstudio.com/items?itemName=ms-python.python" class="external-link" target="_blank">Python</a> extension for VS Code</li>
</ol><p>You should know how to create and work with Python virtual environments.</p>
<h2 id="getting-started" data-needslink="getting-started">Getting started</h2>
<p>To get started, follow the instructions in the template <a href="https://github.com/microsoft/vscode-python-tools-extension-template#readme" class="external-link" target="_blank">README</a>. There you will learn how to use the <a href="https://docs.github.com/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template" class="external-link" target="_blank">template to create your repository</a> and how to install the necessary tools (for example, the <a href="https://nox.thea.codes" class="external-link" target="_blank">nox</a> task runner) and optional dependencies (testing support).</p>
<p>The <a href="https://github.com/microsoft/vscode-python-tools-extension-template#readme" class="external-link" target="_blank">README</a> has the most up-to-date instructions and also goes into details on how to customize the extension's <code>package.json</code> placeholders (<code>&lt;pythontool-module&gt;</code>, <code>&lt;pythontool-display-name&gt;</code>, etc.).</p>
<h2 id="features-of-the-template" data-needslink="features-of-the-template">Features of the template</h2>
<p>After creating your extension via the template, it will include the following extension contributions. Assume <code>&lt;pytool-module&gt;</code> was replaced with <code>mytool</code>, and <code>&lt;pytool-display-name&gt;</code> with<code>My Tool</code>:</p>
<ol><li>A command <strong>My Tool: Restart Server</strong> (command ID: <code>mytool.restart</code>).</li>
<li>Following settings:
<ul><li><code>mytool.logLevel</code></li>
<li><code>mytool.args</code></li>
<li><code>mytool.path</code></li>
<li><code>mytool.importStrategy</code></li>
<li><code>mytool.interpreter</code></li>
<li><code>mytool.showNotification</code></li>
</ul></li>
<li>Following triggers for extension activation:
<ul><li>On Language <code>python</code>.</li>
<li>On File with <code>.py</code> extension found in the opened workspace.</li>
<li>On Command <code>mytool.restart</code>.</li>
</ul></li>
<li>Output channel for logging <strong>Output</strong> &gt; <strong>My Tool</strong>.</li>
</ol><h2 id="integrating-your-tool" data-needslink="integrating-your-tool">Integrating your tool</h2>
<p>The generated <code>bundled/tool/server.py</code> file is where you will make most of your changes. <code>TODO</code> comments in the file point out the various customization points. Also search for <code>TODO</code> comments in other locations in the template, such as other Python and Markdown files. You will want to review the LICENSE file, even if you want to keep it MIT License.</p>
<h2 id="examples" data-needslink="examples">Examples</h2>
<p>There are several example implementations created from the template:</p>
<ul><li><a href="https://github.com/microsoft/vscode-pylint/tree/main/bundled/tool" class="external-link" target="_blank">Pylint</a> - implements linting and Code Actions on file <code>open</code>, <code>save</code>, and <code>close</code>.</li>
<li><a href="https://github.com/microsoft/vscode-flake8/tree/main/bundled/tool" class="external-link" target="_blank">Flake8</a> - implements linting and Code Actions.</li>
<li><a href="https://github.com/microsoft/vscode-black-formatter/tree/main/bundled/tool" class="external-link" target="_blank">Black Formatter</a> - integrates the <a href="https://github.com/python/black" class="external-link" target="_blank"><em>Black</em></a> formatter.</li>
<li><a href="https://github.com/microsoft/vscode-autopep8/tree/main/bundled/tool" class="external-link" target="_blank">autopep8</a> - integrates the <a href="https://pypi.org/project/autopep8" class="external-link" target="_blank">autopep8</a> formatter.</li>
<li><a href="https://github.com/microsoft/vscode-isort/blob/main/bundled/tool" class="external-link" target="_blank">isort</a> - adds Code Actions to sort imports.</li>
</ul><p>You can also review the <a href="https://microsoft.github.io/language-server-protocol/specifications/specification-3-16" class="external-link" target="_blank">Language Server Protocol specification</a> to better understand the <code>pygls</code> language server integration.</p>
<h2 id="extension-development" data-needslink="extension-development">Extension development</h2>
<p>The template README goes into detail on the <a href="https://github.com/microsoft/vscode-python-tools-extension-template#debugging" class="external-link" target="_blank">development cycle support</a> included with the template. The template has commands and configurations so you can build, run, debug, and test your extension.</p>
<p>If you run into problems during development, there is a <a href="https://github.com/microsoft/vscode-python-tools-extension-template#troubleshooting" class="external-link" target="_blank">Troubleshooting</a> section to help with common issues.</p>
<h2 id="packaging-and-publishing" data-needslink="packaging-and-publishing">Packaging and publishing</h2>
<p>Before publishing your extension, you'll need to update the extension <code>package.json</code> fields (such as <code>publisher</code> and <code>license</code>) for your specific extension. You also want to update the auxiliary Markdown files (<code>CODE_OF_CONDUCT.md</code>, <code>CHANGELOG.md</code>, etc.).</p>
<p>Once your extension is ready to publish, there is a <code>nox</code> <code>build-package</code> task to create a <code>.vsix</code> file, which you can then upload to your extension <a href="https://marketplace.visualstudio.com/manage" class="external-link" target="_blank">management page</a>.</p>
<p>If you are new to creating and publishing VS Code extensions, we recommend you follow best practices outlined in the main VS Code <a href="/api/working-with-extensions/publishing-extension#advanced-usage">extension authoring</a> topics. Here you'll find guidance to help make your extension look great on the Marketplace and how to become a verified publisher so that the users feel confident installing your extension.</p>

				<div class="feedback" data-edit-url="https://vscode.dev/github/microsoft/vscode-docs/blob/main/api/advanced-topics/python-extension-template.md"></div>
				
				<div class="body-footer">6/3/2026</div>
				
            </main><aside class="docs-right-sidebar hidden-xs"><div class="docs-markdown-actions">
                    <div class="docs-markdown-dropdown" data-raw-url="/raw/api/advanced-topics/python-extension-template.md">
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
                <nav id="docs-subnavbar" aria-label="On Page"><h4><span class="sr-only">On this page there are 9 sections</span><span aria-hidden="true">On this page</span></h4>
                    <ul class="nav"><li><a href="#python-extension-template">Python extension template</a></li>
                        
                        <li><a href="#programming-languages-and-frameworks">Programming languages and frameworks</a></li>
                        
                        <li><a href="#requirements">Requirements</a></li>
                        
                        <li><a href="#getting-started">Getting started</a></li>
                        
                        <li><a href="#features-of-the-template">Features of the template</a></li>
                        
                        <li><a href="#integrating-your-tool">Integrating your tool</a></li>
                        
                        <li><a href="#examples">Examples</a></li>
                        
                        <li><a href="#extension-development">Extension development</a></li>
                        
                        <li><a href="#packaging-and-publishing">Packaging and publishing</a></li>
                        
                    </ul></nav></aside></div>
		<div class="docs-mobile-widgets visible-xs">
			<div class="connect-widget"></div>
		</div>
	</div>
</div>
		</main>