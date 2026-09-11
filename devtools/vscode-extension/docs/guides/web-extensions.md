# Web Extensions

> 源文档: [https://code.visualstudio.com/api/extension-guides/web-extensions](https://code.visualstudio.com/api/extension-guides/web-extensions)

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
			    
			<li class="panel active expanded">
			  <a class="area" role="button" href="#extension-guides-articles" data-parent="#main-nav" data-toggle="collapse">Extension Guides</a>
			  <ul id="extension-guides-articles" class="collapse in"><li>
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
			          
			        <li class="active">
			          <a href="/api/extension-guides/web-extensions" aria-label="Current Page: Web Extensions">Web Extensions</a>
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
				<select id="small-nav-dropdown" aria-label="topics"><option value="/api">Overview</option><optgroup label="Get Started"><option value="/api/get-started/your-first-extension">Your First Extension</option><option value="/api/get-started/extension-anatomy">Extension Anatomy</option><option value="/api/get-started/wrapping-up">Wrapping Up</option></optgroup><optgroup label="Extension Capabilities"><option value="/api/extension-capabilities/overview">Overview</option><option value="/api/extension-capabilities/common-capabilities">Common Capabilities</option><option value="/api/extension-capabilities/theming">Theming</option><option value="/api/extension-capabilities/extending-workbench">Extending Workbench</option></optgroup><optgroup label="Extension Guides"><option value="/api/extension-guides/overview">Overview</option><optgroup label="Extension Guides - AI"><option value="/api/extension-guides/ai/ai-extensibility-overview">AI Extensibility</option><option value="/api/extension-guides/ai/tools">Language Model Tool</option><option value="/api/extension-guides/ai/mcp">MCP Dev Guide</option><option value="/api/extension-guides/ai/chat">Chat Participant</option><option value="/api/extension-guides/ai/chat-tutorial">Chat Tutorial</option><option value="/api/extension-guides/ai/language-model">Language Model</option><option value="/api/extension-guides/ai/language-model-tutorial">Language Model Tutorial</option><option value="/api/extension-guides/ai/language-model-chat-provider">Language Model Chat Provider</option><option value="/api/extension-guides/ai/prompt-tsx">Prompt TSX</option></optgroup><option value="/api/extension-guides/command">Command</option><option value="/api/extension-guides/color-theme">Color Theme</option><option value="/api/extension-guides/file-icon-theme">File Icon Theme</option><option value="/api/extension-guides/product-icon-theme">Product Icon Theme</option><option value="/api/extension-guides/tree-view">Tree View</option><option value="/api/extension-guides/webview">Webview</option><option value="/api/extension-guides/notebook">Notebook</option><option value="/api/extension-guides/custom-editors">Custom Editors</option><option value="/api/extension-guides/virtual-documents">Virtual Documents</option><option value="/api/extension-guides/virtual-workspaces">Virtual Workspaces</option><option value="/api/extension-guides/web-extensions" selected>Web Extensions</option><option value="/api/extension-guides/workspace-trust">Workspace Trust</option><option value="/api/extension-guides/task-provider">Task Provider</option><option value="/api/extension-guides/scm-provider">Source Control</option><option value="/api/extension-guides/debugger-extension">Debugger Extension</option><option value="/api/extension-guides/markdown-extension">Markdown Extension</option><option value="/api/extension-guides/testing">Test Extension</option><option value="/api/extension-guides/custom-data-extension">Custom Data Extension</option><option value="/api/extension-guides/telemetry">Telemetry</option></optgroup><optgroup label="UX Guidelines"><option value="/api/ux-guidelines/overview">Overview</option><option value="/api/ux-guidelines/activity-bar">Activity Bar</option><option value="/api/ux-guidelines/sidebars">Sidebars</option><option value="/api/ux-guidelines/panel">Panel</option><option value="/api/ux-guidelines/status-bar">Status Bar</option><option value="/api/ux-guidelines/views">Views</option><option value="/api/ux-guidelines/editor-actions">Editor Actions</option><option value="/api/ux-guidelines/quick-picks">Quick Picks</option><option value="/api/ux-guidelines/command-palette">Command Palette</option><option value="/api/ux-guidelines/notifications">Notifications</option><option value="/api/ux-guidelines/webviews">Webviews</option><option value="/api/ux-guidelines/context-menus">Context Menus</option><option value="/api/ux-guidelines/walkthroughs">Walkthroughs</option><option value="/api/ux-guidelines/settings">Settings</option></optgroup><optgroup label="Language Extensions"><option value="/api/language-extensions/overview">Overview</option><option value="/api/language-extensions/syntax-highlight-guide">Syntax Highlight Guide</option><option value="/api/language-extensions/semantic-highlight-guide">Semantic Highlight Guide</option><option value="/api/language-extensions/snippet-guide">Snippet Guide</option><option value="/api/language-extensions/language-configuration-guide">Language Configuration Guide</option><option value="/api/language-extensions/programmatic-language-features">Programmatic Language Features</option><option value="/api/language-extensions/language-server-extension-guide">Language Server Extension Guide</option><option value="/api/language-extensions/embedded-languages">Embedded Languages</option></optgroup><optgroup label="Testing and Publishing"><option value="/api/working-with-extensions/testing-extension">Testing Extensions</option><option value="/api/working-with-extensions/publishing-extension">Publishing Extensions</option><option value="/api/working-with-extensions/bundling-extension">Bundling Extensions</option><option value="/api/working-with-extensions/continuous-integration">Continuous Integration</option></optgroup><optgroup label="Advanced Topics"><option value="/api/advanced-topics/extension-host">Extension Host</option><option value="/api/advanced-topics/remote-extensions">Remote Development and Codespaces</option><option value="/api/advanced-topics/using-proposed-api">Using Proposed API</option><option value="/api/advanced-topics/tslint-eslint-migration">Migrate from TSLint to ESLint</option><option value="/api/advanced-topics/python-extension-template">Python Extension Template</option></optgroup><optgroup label="References"><option value="/api/references/vscode-api">VS Code API</option><option value="/api/references/contribution-points">Contribution Points</option><option value="/api/references/activation-events">Activation Events</option><option value="/api/references/extension-manifest">Extension Manifest</option><option value="/api/references/commands">Built-In Commands</option><option value="/api/references/when-clause-contexts">When Clause Contexts</option><option value="/api/references/theme-color">Theme Color</option><option value="/api/references/icons-in-labels">Product Icon Reference</option><option value="/api/references/document-selector">Document Selector</option></optgroup></select></nav></aside><div class="docs-content-wrapper">
			
			<main class="docs-main-content body"><h1>Web Extensions</h1>
<p>Visual Studio Code can run as an editor in the browser. One example is the <code>github.dev</code> user interface reached by pressing <code>.</code> (the period key) when browsing a repository or Pull Request in GitHub. When VS Code is used in the Web, installed extensions are run in an extension host in the browser, called the 'web extension host'. An extension that can run in a web extension host is called a 'web extension'.</p>
<p>Web extensions share the same structure as regular extensions, but given the different runtime, don't run with the same code as extensions written for a Node.js runtime. Web extensions still have access to the full VS Code API, but no longer to the Node.js APIs and module loading. Instead, web extensions are restricted by the browser sandbox and therefore have <a href="#_web-extension-main-file">limitations</a> compared to normal extensions.</p>
<p>The web extension runtime is supported on VS Code desktop too. If you decide to create your extension as a web extension, it will be supported on <a href="/docs/remote/vscode-web">VS Code for the Web</a> (including <code>vscode.dev</code> and <code>github.dev</code>) as well as on the desktop and in services like <a href="/docs/remote/codespaces">GitHub Codespaces</a>.</p>
<h2 id="web-extension-anatomy" data-needslink="web-extension-anatomy">Web extension anatomy</h2>
<p>A web extension is <a href="/api/get-started/extension-anatomy">structured like a regular extension</a>. The extension manifest (<code>package.json</code>) defines the entry file for the extension's source code and declares extension contributions.</p>
<p>For web extensions, the <a href="#_web-extension-main-file">main entry file</a> is defined by the <code>browser</code> property, and not by the <code>main</code> property as with regular extensions.</p>
<p>The <code>contributes</code> property works the same way for both web and regular extensions.</p>
<p>The example below shows the <code>package.json</code> for a simple hello world extension, that runs in the web extension host only (it only has a <code>browser</code> entry point):</p>
<pre class="shiki" data-lang="json" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">{</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "name"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"helloworld-web-sample"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "displayName"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"helloworld-web-sample"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "description"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"HelloWorld example for VS Code in the browser"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "version"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"0.0.1"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "publisher"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"vscode-samples"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "repository"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"https://github.com/microsoft/vscode-extension-samples/helloworld-web-sample"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "engines"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "vscode"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"^1.74.0"</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  },</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "categories"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"Other"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">],</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "activationEvents"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [],</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "browser"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"./dist/web/extension.js"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "contributes"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "commands"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">        "command"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"helloworld-web-sample.helloWorld"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">        "title"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"Hello World"</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    ]</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  },</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "scripts"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "vscode:prepublish"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"npm run package-web"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "compile-web"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"webpack"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "watch-web"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"webpack --watch"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "package-web"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"webpack --mode production --devtool hidden-source-map"</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  },</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "devDependencies"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "@types/vscode"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"^1.59.0"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "ts-loader"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"^9.2.2"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "webpack"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"^5.38.1"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "webpack-cli"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"^4.7.0"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "@types/webpack-env"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"^1.16.0"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "process"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"^0.11.10"</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<blockquote><p><strong>Note</strong>: If your extension targets a VS Code version prior to 1.74, you must explicitly list <code>onCommand:helloworld-web-sample.helloWorld</code> in <code>activationEvents</code>.</p>
</blockquote><p>Extensions that have only a <code>main</code> entry point, but no <code>browser</code> are not web extensions. They are ignored by the web extension host and not available for download in the Extensions view.</p>
<p><img src="/assets/api/extension-guides/web-extensions/extensions-view-item-disabled.png" alt="Extensions view" loading="lazy"></p>
<p>Extensions with only declarative contributions (only <code>contributes</code>, no <code>main</code> or <code>browser</code>) can be web extensions. They can be installed and run in <a href="/docs/remote/vscode-web">VS Code for the Web</a> without any modifications by the extension author. Examples of extensions with declarative contributions include themes, grammars, and snippets.</p>
<p>Extensions can have both <code>browser</code> and <code>main</code> entry points in order to run in browser and in Node.js runtimes. The <a href="#_update-existing-extensions-to-web-extensions">Update existing extensions to Web extensions</a> section shows how to migrate an extension to work in both runtimes.</p>
<p>The <a href="#_web-extension-enablement">web extension enablement</a> section lists the rules used to decide whether an extension can be loaded in a web extension host.</p>
<h3 id="web-extension-main-file" data-needslink="web-extension-main-file">Web extension main file</h3>
<p>The web extension's main file is defined by the <code>browser</code> property. The script runs in the web extension host in a <a href="https://developer.mozilla.org/docs/Web/API/Web_Workers_API" class="external-link" target="_blank">Browser WebWorker</a> environment. It is restricted by the browser worker sandbox and has limitations compared to normal extensions running in a Node.js runtime.</p>
<ul><li>Importing or requiring other modules is not supported. <code>importScripts</code> is not available as well. As a consequence, the code must be packaged to a single file.</li>
<li>The <a href="/api/references/vscode-api">VS Code API</a> can be loaded via the pattern <code>require('vscode')</code>. This will work because there is a shim for <code>require</code>, but this shim cannot be used to load additional extension files or additional node modules. It only works with <code>require('vscode')</code>.</li>
<li>Node.js globals and libraries such as <code>process</code>, <code>os</code>, <code>setImmediate</code>, <code>path</code>, <code>util</code>, <code>url</code> are not available at runtime. They can, however, be added with tools like webpack. The <a href="#_webpack-configuration">webpack configuration</a> section explains how this is done.</li>
<li>The opened workspace or folder is on a virtual file system. Access to workspace files needs to go through the VS Code <a href="/api/references/vscode-api#FileSystem">file system</a> API accessible at <code>vscode.workspace.fs</code>.</li>
<li><a href="/api/references/vscode-api#ExtensionContext">Extension context</a> locations (<code>ExtensionContext.extensionUri</code>) and  storage locations (<code>ExtensionContext.storageUri</code>, <code>globalStorageUri</code>) are also on a virtual file system and need to go through <code>vscode.workspace.fs</code>.</li>
<li>For accessing web resources, the <a href="https://developer.mozilla.org/docs/Web/API/Fetch_API" class="external-link" target="_blank">Fetch</a> API must be used. Accessed resources need to support <a href="https://developer.mozilla.org/docs/Web/HTTP/CORS" class="external-link" target="_blank">Cross-Origin Resource Sharing</a> (CORS)</li>
<li>Creating child processes or running executables is not possible. However, web workers can be created through the <a href="https://developer.mozilla.org/en-US/docs/Web/API/Worker" class="external-link" target="_blank">Worker</a> API. This is used for running language servers as described in the <a href="#_language-server-protocol-in-web-extensions">Language Server Protocol in web extensions</a> section.</li>
<li>As with regular extensions, the extension's <code>activate/deactivate</code> functions need to be exported via the pattern <code>exports.activate = ...</code>.</li>
</ul><h2 id="develop-a-web-extension" data-needslink="develop-a-web-extension">Develop a web extension</h2>
<p>Thankfully, tools like TypeScript and webpack can hide many of the browser runtime constraints and allow you to write web extensions the same way as regular extensions. Both a web extension and a regular extension can often be generated from the same source code.</p>
<p>For example, the <code>Hello Web Extension</code> created by the <code>yo code</code> <a href="https://www.npmjs.com/package/generator-code" class="external-link" target="_blank">generator</a> only differs in the build scripts. You can run and debug the generated extension just like traditional Node.js extensions by using the provided launch configurations accessible using the <strong>Debug: Select and Start Debugging</strong> command.</p>
<h2 id="create-a-web-extension" data-needslink="create-a-web-extension">Create a web extension</h2>
<p>To scaffold a new web extension, use <code>yo code</code> and pick <strong>New Web Extension</strong>. Make sure to have the latest version of <a href="https://www.npmjs.com/package/generator-code" class="external-link" target="_blank">generator-code</a> (&gt;= generator-code@1.6) installed. To update the generator and yo, run <code>npm i -g yo generator-code</code>.</p>
<p>The extension that is created consists of the extension's source code (a command showing a hello world notification), the <code>package.json</code> manifest file, and a webpack or esbuild configuration file.</p>
<p>To keep things simpler, we assume you use <code>webpack</code> as the bundler. At the end of the article we also explain what is different when choosing <code>esbuild</code>.</p>
<ul><li><code>src/web/extension.ts</code> is the extension's entry source code file. It's identical to the regular hello extension.</li>
<li><code>package.json</code> is the extension manifest.
<ul><li>It points to the entry file using the <code>browser</code> property.</li>
<li>It provides scripts: <code>compile-web</code>, <code>watch-web</code> and <code>package-web</code> to compile, watch, and package.</li>
</ul></li>
<li><code>webpack.config.js</code> is the webpack config file that compiles and bundles the extension sources into a single file.</li>
<li><code>.vscode/launch.json</code> contains the launch configurations that run the web extension and the tests in the VS Code desktop with a web extension host (setting <code>extensions.webWorker</code> is no longer needed).</li>
<li><code>.vscode/task.json</code> contains the build task used by the launch configuration. It uses <code>npm run watch-web</code> and depends on the webpack specific <code>ts-webpack-watch</code> problem matcher.</li>
<li><code>.vscode/extensions.json</code> contains the extensions that provide the problem matchers. These extensions need to be installed for the launch configurations to work.</li>
<li><code>tsconfig.json</code> defines the compile options matching the <code>webworker</code> runtime.</li>
</ul><p>The source code in the <a href="https://github.com/microsoft/vscode-extension-samples/tree/main/helloworld-web-sample" class="external-link" target="_blank">helloworld-web-sample</a> is similar to what's created by the generator.</p>
<h3 id="webpack-configuration" data-needslink="webpack-configuration">Webpack configuration</h3>
<p>The webpack configuration file is automatically generated by <code>yo code</code>. It bundles the source code from your extension into a single JavaScript file to be loaded in the web extension host.</p>
<p>Later we explain how to use esbuild as bundler, but for now we start with webpack.</p>
<p><a href="https://github.com/microsoft/vscode-extension-samples/blob/main/helloworld-web-sample/webpack.config.js" class="external-link" target="_blank">webpack.config.js</a></p>
<pre class="shiki" data-lang="js" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> path</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">require</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'path'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> webpack</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">require</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'webpack'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">/** </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">@typedef</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99"> {import('webpack').Configuration}</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99"> WebpackConfig</span><span style="--shiki-dark:#6A9955;--shiki-light:#008000"> **/</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">/** </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">@type</span><span style="--shiki-dark:#6A9955;--shiki-light:#008000"> WebpackConfig */</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> webExtensionConfig</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  mode:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'none'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#6A9955;--shiki-light:#008000">// this leaves the source code as close as possible to the original (when packaging we set this to 'production')</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  target:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'webworker'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#6A9955;--shiki-light:#008000">// extensions run in a webworker context</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  entry:</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    extension:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> './src/web/extension.ts'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#6A9955;--shiki-light:#008000">// source of the web extension main file</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">    'test/suite/index'</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> './src/web/test/suite/index.ts'</span><span style="--shiki-dark:#6A9955;--shiki-light:#008000"> // source of the web extension test runner</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  },</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  output:</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    filename:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> '[name].js'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    path:</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> path</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">join</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">__dirname</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'./dist/web'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">),</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    libraryTarget:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'commonjs'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    devtoolModuleFilenameTemplate:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> '../../[resource-path]'</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  },</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  resolve:</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    mainFields:</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> [</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'browser'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'module'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'main'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">], </span><span style="--shiki-dark:#6A9955;--shiki-light:#008000">// look for `browser` entry point in imported node modules</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    extensions:</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> [</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'.ts'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'.js'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">], </span><span style="--shiki-dark:#6A9955;--shiki-light:#008000">// support ts-files and js-files</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    alias:</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">      // provides alternate implementation for node module and source files</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    },</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    fallback:</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">      // Webpack 5 no longer polyfills Node.js core modules automatically.</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">      // see https://webpack.js.org/configuration/resolve/#resolvefallback</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">      // for the list of Node.js core module polyfills.</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">      assert:</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> require</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">resolve</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'assert'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">)</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  },</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  module:</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    rules:</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> [</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">        test:</span><span style="--shiki-dark:#D16969;--shiki-light:#811F3F"> /</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\.</span><span style="--shiki-dark:#D16969;--shiki-light:#811F3F">ts</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#EE0000">$</span><span style="--shiki-dark:#D16969;--shiki-light:#811F3F">/</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">        exclude:</span><span style="--shiki-dark:#D16969;--shiki-light:#811F3F"> /node_modules/</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">        use:</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> [</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">          {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">            loader:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'ts-loader'</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">          }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">        ]</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    ]</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  },</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  plugins:</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> [</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">    new</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> webpack</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">ProvidePlugin</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">({</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">      process:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'process/browser'</span><span style="--shiki-dark:#6A9955;--shiki-light:#008000"> // provide a shim for the global `process` variable</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    })</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  ],</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  externals:</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    vscode:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'commonjs vscode'</span><span style="--shiki-dark:#6A9955;--shiki-light:#008000"> // ignored because it doesn't exist</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  },</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  performance:</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    hints:</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> false</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  },</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  devtool:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'nosources-source-map'</span><span style="--shiki-dark:#6A9955;--shiki-light:#008000"> // create a source map that points to the original source file</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">};</span></span>
<span class="line"><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">module</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">exports</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = [</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">webExtensionConfig</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">];</span></span>
<span class="line"></span></code></pre>
<p>Some important fields of <code>webpack.config.js</code> are:</p>
<ul><li>The <code>entry</code> field contains the main entry point into your extension and test suite.
<ul><li>You may need to adjust this path to appropriately point to the entry point of your extension.</li>
<li>For an existing extension, you can start by pointing this path to the file you're using currently for <code>main</code> of your <code>package.json</code>.</li>
<li>If you do not want to package your tests, you can omit the test suite field.</li>
</ul></li>
<li>The <code>output</code> field indicates where the compiled file will be located.
<ul><li><code>[name]</code> will be replaced by the key used in <code>entry</code>. So in the generated config file, it will produce <code>dist/web/extension.js</code> and <code>dist/web/test/suite/index.js</code>.</li>
</ul></li>
<li>The <code>target</code> field indicates which type of environment the compiled JavaScript file will run. For web extensions, you want this to be <code>webworker</code>.</li>
<li>The <code>resolve</code> field contains the ability to add aliases and fallbacks for node libraries that don't work in the browser.
<ul><li>If you're using a library like <code>path</code>, you can specify how to resolve <code>path</code> in a web compiled context. For instance, you can point to a file in the project that defines <code>path</code> with <code>path: path.resolve(__dirname, 'src/my-path-implementation-for-web.js')</code>. Or you can use the Browserify node packaged version of the library called <code>path-browserify</code> and specify <code>path: require.resolve('path-browserify')</code>.</li>
<li>See <a href="https://webpack.js.org/configuration/resolve/#resolvefallback" class="external-link" target="_blank">webpack resolve.fallback</a> for the list of Node.js core module polyfills.</li>
</ul></li>
<li>The <code>plugins</code> section uses the <a href="https://webpack.js.org/plugins/define-plugin/" class="external-link" target="_blank">DefinePlugin plugin</a> to polyfill globals such as the <code>process</code> Node.js global.</li>
</ul><h2 id="test-your-web-extension" data-needslink="test-your-web-extension">Test your web extension</h2>
<p>There are currently three ways to test a web extension before publishing it to the Marketplace.</p>
<ul><li>Use VS Code running on the desktop with the <code>--extensionDevelopmentKind=web</code> option to run your web extension in a web extension host running in VS Code.</li>
<li>Use the <a href="https://github.com/microsoft/vscode-test-web" class="external-link" target="_blank">@vscode/test-web</a> node module to open a browser containing VS Code for the Web including your extension, served from a local server.</li>
<li><a href="#_test-your-web-extension-in-vscode.dev">Sideload</a> your extension onto <a href="https://vscode.dev" class="external-link" target="_blank">vscode.dev</a> to see your extension in the actual environment.</li>
</ul><h3 id="test-your-web-extension-in-vs-code-running-on-desktop" data-needslink="test-your-web-extension-in-vs-code-running-on-desktop">Test your web extension in VS Code running on desktop</h3>
<p>To use the existing VS Code extension development experience, VS Code running on the desktop supports running a web extension host along with the regular Node.js extension host.</p>
<p>Use the <code>pwa-extensionhost</code> launch configuration provided by the <strong>New Web Extension</strong> generator:</p>
<pre class="shiki" data-lang="json" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">{</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "version"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"0.2.0"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "configurations"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">      "name"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"Run Web Extension in VS Code"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">      "type"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"pwa-extensionHost"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">      "debugWebWorkerHost"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">true</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">      "request"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"launch"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">      "args"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">        "--extensionDevelopmentPath=${workspaceFolder}"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">        "--extensionDevelopmentKind=web"</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      ],</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">      "outFiles"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"${workspaceFolder}/dist/web/**/*.js"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">],</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">      "preLaunchTask"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"npm: watch-web"</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  ]</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<p>It uses the task <code>npm: watch-web</code> to compile the extension by calling <code>npm run watch-web</code>. That task is expected in <code>tasks.json</code>:</p>
<pre class="shiki" data-lang="json" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">{</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "version"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"2.0.0"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "tasks"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">      "type"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"npm"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">      "script"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"watch-web"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">      "group"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"build"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">      "isBackground"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">true</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">      "problemMatcher"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"$ts-webpack-watch"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">]</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  ]</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<p><code>$ts-webpack-watch</code> is a problem matcher that can parse the output from the webpack tool. It is provided by the <a href="https://marketplace.visualstudio.com/items?itemName=eamodio.tsl-problem-matcher" class="external-link" target="_blank">TypeScript + Webpack Problem Matchers</a> extension.</p>
<p>In the <strong>Extension Development Host</strong> instance that launches, the web extension will be available and running in a web extension host. Run the <code>Hello World</code> command to activate the extension.</p>
<p>Open the <strong>Running Extensions</strong> view (command: <strong>Developer: Show Running Extensions</strong>) to see which extensions are running in the web extension host.</p>
<h3 id="test-your-web-extension-in-a-browser-using-atvscodetestweb" data-needslink="test-your-web-extension-in-a-browser-using-atvscodetestweb">Test your web extension in a browser using @vscode/test-web</h3>
<p>The <a href="https://github.com/microsoft/vscode-test-web" class="external-link" target="_blank">@vscode/test-web</a> node module offers a CLI and API to test a web extension in a browser.</p>
<p>The node module contributes an npm binary <code>vscode-test-web</code> that can open VS Code for the Web from the command line:</p>
<ul><li>It downloads the web bits of VS Code into <code>.vscode-test-web</code>.</li>
<li>Starts a local server on <code>localhost:3000</code>.</li>
<li>Opens a browser (Chromium, Firefox, or Webkit).</li>
</ul><p>You can run it from command line:</p>
<pre class="shiki" data-lang="bash" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">npx</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> @vscode/test-web</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> --extensionDevelopmentPath=</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">$extensionFolderPath</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> $testDataPath</span></span>
<span class="line"></span></code></pre>
<p>Or better, add <code>@vscode/test-web</code> as a development dependency to your extension and invoke it in a script:</p>
<pre class="shiki" data-lang="json" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">  "devDependencies"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "@vscode/test-web"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"*"</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  },</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">  "scripts"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "open-in-browser"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"vscode-test-web --extensionDevelopmentPath=. ."</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  }</span></span>
<span class="line"></span></code></pre>
<p>Check the <a href="https://www.npmjs.com/package/@vscode/test-web" class="external-link" target="_blank">@vscode/test-web README</a> for more CLI options:</p>
<table class="table table-striped"><thead><tr><th>Option</th>
<th>Argument Description</th>
</tr></thead><tbody><tr><td>--browserType</td>
<td>The browser to launch: <code>chromium</code> (default), <code>firefox</code> or <code>webkit</code></td>
</tr><tr><td>--extensionDevelopmentPath</td>
<td>A path pointing to an extension under development to include.</td>
</tr><tr><td>--extensionTestsPath</td>
<td>A path to a test module to run.</td>
</tr><tr><td>--permission</td>
<td>Permission granted to the opened browser: e.g. <code>clipboard-read</code>, <code>clipboard-write</code>.<br>See <a href="https://playwright.dev/docs/api/class-browsercontext#browser-context-grant-permissions" class="external-link" target="_blank">full list of options</a>. Argument can be provided multiple times.</td>
</tr><tr><td>--folder-uri</td>
<td>URI of the workspace to open VS Code on. Ignored when <code>folderPath</code> is provided</td>
</tr><tr><td>--extensionPath</td>
<td>A path pointing to a folder containing additional extensions to include.<br>Argument can be provided multiple times.</td>
</tr><tr><td>folderPath</td>
<td>A local folder to open VS Code on.<br>The folder content will be available as a virtual file system and opened as workspace.</td>
</tr></tbody></table><p>The web bits of VS Code are downloaded to a folder <code>.vscode-test-web</code>. You want to add this to your <code>.gitignore</code> file.</p>
<h3 id="test-your-web-extension-in-vscode.dev" data-needslink="test-your-web-extension-in-vscode.dev">Test your web extension in vscode.dev</h3>
<p>Before you publish your extension for everyone to use on VS Code for the Web, you can verify how your extension behaves in the actual <a href="https://vscode.dev" class="external-link" target="_blank">vscode.dev</a> environment.</p>
<p>To see your extension on vscode.dev, you first need to host it from your machine for vscode.dev to download and run.</p>
<p>First, you'll need to <a href="https://github.com/FiloSottile/mkcert#installation" class="external-link" target="_blank">install <code>mkcert</code></a>.</p>
<p>Then, generate the <code>localhost.pem</code> and <code>localhost-key.pem</code> files into a location you won't lose them (for example <code>$HOME/certs</code>):</p>
<pre class="shiki" data-lang="text" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span>$ mkdir -p $HOME/certs</span></span>
<span class="line"><span>$ cd $HOME/certs</span></span>
<span class="line"><span>$ mkcert -install</span></span>
<span class="line"><span>$ mkcert localhost</span></span>
<span class="line"><span></span></span></code></pre>
<p>Then, from your extension's path, start an HTTP server by running <code>npx serve</code>:</p>
<pre class="shiki" data-lang="text" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span>$ npx serve --cors -l 5000 --ssl-cert $HOME/certs/localhost.pem --ssl-key $HOME/certs/localhost-key.pem</span></span>
<span class="line"><span>npx: installed 78 in 2.196s</span></span>
<span class="line"><span></span></span>
<span class="line"><span>   ┌────────────────────────────────────────────────────┐</span></span>
<span class="line"><span>   │                                                    │</span></span>
<span class="line"><span>   │   Serving!                                         │</span></span>
<span class="line"><span>   │                                                    │</span></span>
<span class="line"><span>   │   - Local:            https://localhost:5000       │</span></span>
<span class="line"><span>   │   - On Your Network:  https://203.0.113.42:5000   │</span></span>
<span class="line"><span>   │                                                    │</span></span>
<span class="line"><span>   │   Copied local address to clipboard!               │</span></span>
<span class="line"><span>   │                                                    │</span></span>
<span class="line"><span>   └────────────────────────────────────────────────────┘</span></span>
<span class="line"><span></span></span></code></pre>
<p>Finally, open <a href="https://vscode.dev" class="external-link" target="_blank">vscode.dev</a>, run <strong>Developer: Install Extension From Location...</strong> from the Command Palette (<span class="dynamic-keybinding" data-commandid="workbench.action.showCommands" data-osx="⇧⌘P" data-win="Ctrl+Shift+P" data-linux="Ctrl+Shift+P"><span class="keybinding">⇧⌘P</span> (Windows, Linux <span class="keybinding">Ctrl+Shift+P</span>)</span>), paste the URL from above, <code>https://localhost:5000</code> in the example, and select <strong>Install</strong>.</p>
<p><strong>Check the logs</strong></p>
<p>You can check the logs in the console of the Developer Tools of your browser to see any errors, status, and logs from your extension.</p>
<p>You may see other logs from vscode.dev itself. In addition, you can't easily set breakpoints nor see the source code of your extension. These limitations make debugging in vscode.dev not the most pleasant experience so we recommend using the first two options for testing before sideloading onto vscode.dev. Sideloading is a good final sanity check before publishing your extension.</p>
<h2 id="web-extension-tests" data-needslink="web-extension-tests">Web extension tests</h2>
<p>Web extension tests are supported and can be implemented similar to regular extension tests. See the <a href="/api/working-with-extensions/testing-extension">Testing Extensions</a> article to learn the basic structure of extension tests.</p>
<p>The <a href="https://github.com/microsoft/vscode-test-web" class="external-link" target="_blank">@vscode/test-web</a> node module is the equivalent to <a href="https://github.com/microsoft/vscode-test" class="external-link" target="_blank">@vscode/test-electron</a> (previously named <code>vscode-test</code>). It allows you to run extension tests from the command line on Chromium, Firefox, and Safari.</p>
<p>The utility does the following steps:</p>
<ol><li>Starts a VS Code for the Web editor from a local web server.</li>
<li>Opens the specified browser.</li>
<li>Runs the provided test runner script.</li>
</ol><p>You can run the tests in continuous builds to ensure that the extension works on all browsers.</p>
<p>The test runner script is running on the web extension host with the same restrictions as the <a href="#_web-extension-main-file">web extension main file</a>:</p>
<ul><li>All files are bundled into a single file. It should contain the test runner (for example, Mocha) and all tests (typically <code>*.test.ts</code>).</li>
<li>Only <code>require('vscode')</code> is supported.</li>
</ul><p>The <a href="https://github.com/microsoft/vscode-extension-samples/blob/main/helloworld-web-sample/webpack.config.js" class="external-link" target="_blank">webpack config</a> that is created by the <code>yo code</code> web extension generator has a section for tests. It expects the test runner script at <code>./src/web/test/suite/index.ts</code>. The provided <a href="https://github.com/microsoft/vscode-extension-samples/blob/main/helloworld-web-sample/src/web/test/suite/index.ts" class="external-link" target="_blank">test runner script</a> uses the web version of Mocha and contains webpack-specific syntax to import all test files.</p>
<pre class="shiki" data-lang="ts" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">require</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'mocha/mocha'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">); </span><span style="--shiki-dark:#6A9955;--shiki-light:#008000">// import the mocha web build</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">export</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> function</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> run</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(): </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">Promise</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">&lt;</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">void</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">&gt; {</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">  return</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> new</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99"> Promise</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">((</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">c</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">e</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">=&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    mocha</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">setup</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">({</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">      ui:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'tdd'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">      reporter:</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> undefined</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    });</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">    // bundles all files in the current directory matching `*.test`</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">    const</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> importAll</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = (</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">r</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">__WebpackModuleApi</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">RequireContext</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">=&gt;</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> r</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">keys</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">().</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">forEach</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">r</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">    importAll</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">require</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">context</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'.'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">true</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span><span style="--shiki-dark:#D16969;--shiki-light:#811F3F"> /</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\.</span><span style="--shiki-dark:#D16969;--shiki-light:#811F3F">test</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#EE0000">$</span><span style="--shiki-dark:#D16969;--shiki-light:#811F3F">/</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">));</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">    try</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">      // Run the mocha test</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">      mocha</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">run</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">failures</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> =&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">        if</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> (</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">failures</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> &gt; </span><span style="--shiki-dark:#B5CEA8;--shiki-light:#098658">0</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">          e</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">new</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> Error</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">`</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">${</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">failures</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> tests failed.`</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">));</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">        } </span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">else</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">          c</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">();</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">        }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      });</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    } </span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">catch</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> (</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">err</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">      console</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">error</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">err</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">      e</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">err</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  });</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<p>To run the web test from the command line, add the following to your <code>package.json</code> and run it with <code>npm test</code>.</p>
<pre class="shiki" data-lang="json" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">  "devDependencies"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "@vscode/test-web"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"*"</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  },</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">  "scripts"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "test"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"vscode-test-web --extensionDevelopmentPath=. --extensionTestsPath=dist/web/test/suite/index.js"</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  }</span></span>
<span class="line"></span></code></pre>
<p>To open VS Code on a folder with test data, pass a local folder path (<code>folderPath</code>) as the last parameter.</p>
<p>To run (and debug) extension tests in VS Code (Insiders) desktop, use the <code>Extension Tests in VS Code</code> launch configuration:</p>
<pre class="shiki" data-lang="json" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">{</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "version"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"0.2.0"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "configurations"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">      "name"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"Extension Tests in VS Code"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">      "type"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"extensionHost"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">      "debugWebWorkerHost"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">true</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">      "request"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"launch"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">      "args"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">        "--extensionDevelopmentPath=${workspaceFolder}"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">        "--extensionDevelopmentKind=web"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">        "--extensionTestsPath=${workspaceFolder}/dist/web/test/suite/index"</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      ],</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">      "outFiles"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"${workspaceFolder}/dist/web/**/*.js"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">],</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">      "preLaunchTask"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"npm: watch-web"</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  ]</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<h2 id="publish-a-web-extension" data-needslink="publish-a-web-extension">Publish a web extension</h2>
<p>Web extensions are hosted on the <a href="https://marketplace.visualstudio.com/vscode" class="external-link" target="_blank">Marketplace</a> along with other extensions.</p>
<p>Make sure to use the latest version of <code>vsce</code> to publish your extension. <code>vsce</code> tags all extensions that are web extension. For that <code>vsce</code> is using the rules listed in the <a href="#_web-extension-enablement">web extension enablement</a> section.</p>
<h2 id="update-existing-extensions-to-web-extensions" data-needslink="update-existing-extensions-to-web-extensions">Update existing extensions to Web extensions</h2>
<h3 id="extension-without-code" data-needslink="extension-without-code">Extension without code</h3>
<p>Extensions that have no code, but only contribution points (for example, themes, snippets, and basic language extensions) don't need any modification. They can run in a web extension host and can be installed from the Extensions view.</p>
<p>Republishing is not necessary, but when publishing a new version of the extension, make sure to use the most current version of <code>vsce</code>.</p>
<h3 id="migrate-extension-with-code" data-needslink="migrate-extension-with-code">Migrate extension with code</h3>
<p>Extensions with source code (defined by the <code>main</code> property) need to provide a <a href="#_web-extension-main-file">web extension main file</a> and set the <code>browser</code> property in <code>package.json</code>.</p>
<p>Use these steps to recompile your extension code for the browser environment:</p>
<ul><li>Add a webpack config file as shown in the <a href="#_webpack-configuration">webpack configuration</a> section. If you already have a webpack file for your Node.js extension code, you can add a new section for web. Check out the <a href="https://github.com/aeschli/vscode-css-formatter/blob/master/webpack.config.js" class="external-link" target="_blank">vscode-css-formatter</a> as an example.</li>
<li>Add the <code>launch.json</code> and <code>tasks.json</code> files as shown in the <a href="#_test-your-web-extension">Test your web extension</a> section.</li>
<li>In the webpack config file, set the input file to the existing Node.js main file or create a new main file for the web extension.</li>
<li>In <code>package.json</code>, add a <code>browser</code> and the <code>scripts</code> properties as shown in the <a href="#_web-extension-anatomy">Web extension anatomy</a> section.</li>
<li>Run <code>npm run compile-web</code> to invoke webpack and see where work is needed to make your extension run in the web.</li>
</ul><p>To make sure as much source code as possible can be reused, here are a few techniques:</p>
<ul><li>To polyfill a Node.js core module such as <code>path</code>, add an entry to <a href="https://webpack.js.org/configuration/resolve/#resolvefallback" class="external-link" target="_blank">resolve.fallback</a>.</li>
<li>To provide a Node.js global such as <code>process</code> use the <a href="https://webpack.js.org/plugins/define-plugin" class="external-link" target="_blank">DefinePlugin plugin</a>.</li>
<li>Use node modules that work in both browser and node runtime. Node modules can do that by defining both <code>browser</code> and <code>main</code> entry points. Webpack will automatically use the one matching its target. Examples of node modules that do this are <a href="https://github.com/microsoft/node-request-light" class="external-link" target="_blank">request-light</a> and <a href="https://github.com/microsoft/vscode-l10n" class="external-link" target="_blank">@vscode/l10n</a>.</li>
<li>To provide an alternate implementation for a node module or source file, use <a href="https://webpack.js.org/configuration/resolve/#resolvealias" class="external-link" target="_blank">resolve.alias</a>.</li>
<li>Separate your code in a browser part, Node.js part, and common part. In common, only use code that works in both the browser and Node.js runtime. Create abstractions for functionality that has different implementations in Node.js and the browser.</li>
<li>Look out for usages of <code>path</code>, <code>URI.file</code>, <code>context.extensionPath</code>, <code>rootPath</code>. <code>uri.fsPath</code>. These will not work with virtual workspaces (non-file system) as they are used in VS Code for the Web. Instead use URIs with <code>URI.parse</code>, <code>context.extensionUri</code>. The <a href="https://www.npmjs.com/package/vscode-uri" class="external-link" target="_blank">vscode-uri</a> node module provides <code>joinPath</code>, <code>dirName</code>, <code>baseName</code>, <code>extName</code>, <code>resolvePath</code>.</li>
<li>Look out for usages of <code>fs</code>. Replace by using vscode <code>workspace.fs</code>.</li>
</ul><p>It is fine to provide less functionality when your extension is running in the web. Use <a href="/api/references/when-clause-contexts">when clause contexts</a> to control which commands, views, and tasks are available or hidden with running in a virtual workspace on the web.</p>
<ul><li>Use the <code>virtualWorkspace</code> context variable to find out if the current workspace is a non-file system workspace.</li>
<li>Use <code>resourceScheme</code> to check if the current resource is a <code>file</code> resource.</li>
<li>Use <code>shellExecutionSupported</code> if there is a platform shell present.</li>
<li>Implement alternative command handlers that show a dialog to explain why the command is not applicable.</li>
</ul><p>WebWorkers can be used as an alternative to forking processes. We have updated several language servers to run as web extensions, including the built-in <a href="https://github.com/microsoft/vscode/tree/main/extensions/json-language-features" class="external-link" target="_blank">JSON</a>, <a href="https://github.com/microsoft/vscode/tree/main/extensions/css-language-features" class="external-link" target="_blank">CSS</a>, and <a href="https://github.com/microsoft/vscode/tree/main/extensions/html-language-features" class="external-link" target="_blank">HTML</a> language servers. The <a href="#_language-server-protocol-in-web-extensions">Language Server Protocol</a> section below gives more details.</p>
<p>The browser runtime environment only supports the execution of JavaScript and <a href="https://webassembly.org/" class="external-link" target="_blank">WebAssembly</a>. Libraries written in other programming languages need to be cross-compiled, for instance there is tooling to compile <a href="https://developer.mozilla.org/en-US/docs/WebAssembly/C_to_wasm" class="external-link" target="_blank">C/C++</a> and <a href="https://developer.mozilla.org/en-US/docs/WebAssembly/Rust_to_wasm" class="external-link" target="_blank">Rust</a> to WebAssembly. The <a href="https://github.com/microsoft/vscode-anycode" class="external-link" target="_blank">vscode-anycode</a> extension, for example, uses <a href="https://www.npmjs.com/package/tree-sitter" class="external-link" target="_blank">tree-sitter</a>, which is C/C++ code compiled to WebAssembly.</p>
<h3 id="language-server-protocol-in-web-extensions" data-needslink="language-server-protocol-in-web-extensions">Language Server Protocol in web extensions</h3>
<p><a href="https://github.com/Microsoft/vscode-languageserver-node" class="external-link" target="_blank">vscode-languageserver-node</a> is an implementation of the <a href="https://microsoft.github.io/language-server-protocol" class="external-link" target="_blank">Language Server Protocol</a> (LSP) that is used as a foundation to language server implementations such as <a href="https://github.com/microsoft/vscode/tree/main/extensions/json-language-features" class="external-link" target="_blank">JSON</a>, <a href="https://github.com/microsoft/vscode/tree/main/extensions/css-language-features" class="external-link" target="_blank">CSS</a>, and <a href="https://github.com/microsoft/vscode/tree/main/extensions/html-language-features" class="external-link" target="_blank">HTML</a>.</p>
<p>Since 3.16.0, the client and server now also provide a browser implementation. The server can run in a web worker and the connection is based on the webworkers <code>postMessage</code> protocol.</p>
<p>The client for the browser can be found at 'vscode-languageclient/browser':</p>
<pre class="shiki" data-lang="typescript" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">import</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> { </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">LanguageClient</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> } </span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">from</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> `vscode-languageclient/browser`</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"></span></code></pre>
<p>The server at <code>vscode-languageserver/browser</code>.</p>
<p>The <a href="https://github.com/microsoft/vscode-extension-samples/tree/main/lsp-web-extension-sample" class="external-link" target="_blank">lsp-web-extension-sample</a> shows how this works.</p>
<h2 id="web-extension-enablement" data-needslink="web-extension-enablement">Web extension enablement</h2>
<p>VS Code automatically treats an extension as a web extension if:</p>
<ul><li>The extension manifest (<code>package.json</code>) has <code>browser</code> entry point.</li>
<li>The extension manifest has no <code>main</code> entry point and none of the following contribution points: <code>localizations</code>, <code>debuggers</code>, <code>terminal</code>, <code>typescriptServerPlugins</code>.</li>
</ul><p>If an extension wants to provide a debugger or terminal that also work in the web extension host, a <code>browser</code> entry point needs to be defined.</p>
<h2 id="using-esbuild" data-needslink="using-esbuild">Using ESBuild</h2>
<p>If you want to use esbuild instead of webpack, do the following:</p>
<p>Add a <code>esbuild.js</code> build script:</p>
<pre class="shiki" data-lang="js" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> esbuild</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">require</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'esbuild'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> glob</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">require</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'glob'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> path</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">require</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'path'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> polyfill</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">require</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'@esbuild-plugins/node-globals-polyfill'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> production</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">process</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">argv</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">includes</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'--production'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> watch</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">process</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">argv</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">includes</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'--watch'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">async</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> function</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> main</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">() {</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">  const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> ctx</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">await</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> esbuild</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">context</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">({</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    entryPoints:</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> [</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'src/web/extension.ts'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'src/web/test/suite/extensionTests.ts'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">],</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    bundle:</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> true</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    format:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'cjs'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    minify:</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> production</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    sourcemap:</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> !</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">production</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    sourcesContent:</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> false</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    platform:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'browser'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    outdir:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'dist/web'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    external:</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> [</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'vscode'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">],</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    logLevel:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'warning'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">    // Node.js global to browser globalThis</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    define:</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">      global:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'globalThis'</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    },</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    plugins:</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> [</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">      polyfill</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">NodeGlobalsPolyfillPlugin</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">({</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">        process:</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> true</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">        buffer:</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> true</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      }),</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">      testBundlePlugin</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">      esbuildProblemMatcherPlugin</span><span style="--shiki-dark:#6A9955;--shiki-light:#008000"> /* add to the end of plugins array */</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    ]</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  });</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">  if</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> (</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">watch</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">    await</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> ctx</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">watch</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">();</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  } </span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">else</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">    await</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> ctx</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">rebuild</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">();</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">    await</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> ctx</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">dispose</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">();</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">/**</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000"> * For web extension, all tests, including the test runner, need to be bundled into</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000"> * a single module that has a exported `run` function .</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000"> * This plugin bundles implements a virtual file extensionTests.ts that bundles all these together.</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000"> * </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">@type</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99"> {import('esbuild').Plugin}</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000"> */</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> testBundlePlugin</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  name:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'testBundlePlugin'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">  setup</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">build</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    build</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">onResolve</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">({ </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">filter:</span><span style="--shiki-dark:#D16969;--shiki-light:#811F3F"> /</span><span style="--shiki-dark:#CE9178;--shiki-light:#D16969">[</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\/\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#D16969">]</span><span style="--shiki-dark:#D16969;--shiki-light:#811F3F">extensionTests</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\.</span><span style="--shiki-dark:#D16969;--shiki-light:#811F3F">ts</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#EE0000">$</span><span style="--shiki-dark:#D16969;--shiki-light:#811F3F">/</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> }, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">args</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> =&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">      if</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> (</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">args</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">kind</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> === </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'entry-point'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">        return</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> { </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">path:</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> path</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">resolve</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">args</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">path</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) };</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    });</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    build</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">onLoad</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">({ </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">filter:</span><span style="--shiki-dark:#D16969;--shiki-light:#811F3F"> /</span><span style="--shiki-dark:#CE9178;--shiki-light:#D16969">[</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\/\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#D16969">]</span><span style="--shiki-dark:#D16969;--shiki-light:#811F3F">extensionTests</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\.</span><span style="--shiki-dark:#D16969;--shiki-light:#811F3F">ts</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#EE0000">$</span><span style="--shiki-dark:#D16969;--shiki-light:#811F3F">/</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> }, </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">async</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> args</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> =&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">      const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> testsRoot</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">path</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">join</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">__dirname</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'src/web/test/suite'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">      const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> files</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">await</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> glob</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">glob</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'*.test.{ts,tsx}'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, { </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">cwd:</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> testsRoot</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">posix:</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> true</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> });</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">      return</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">        contents:</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">          `export { run } from './mochaTestRunner.ts';`</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> +</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">          files</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">map</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">f</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> =&gt;</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> `import('./</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">${</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">f</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">');`</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">).</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">join</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">''</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">),</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">        watchDirs:</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> files</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">map</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">f</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> =&gt;</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> path</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">dirname</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">path</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">resolve</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">testsRoot</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">f</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">))),</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">        watchFiles:</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> files</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">map</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">f</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> =&gt;</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> path</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">resolve</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">testsRoot</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">f</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">))</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      };</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    });</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">};</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">/**</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000"> * This plugin hooks into the build process to print errors in a format that the problem matcher in</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000"> * Visual Studio Code can understand.</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000"> * </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">@type</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99"> {import('esbuild').Plugin}</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000"> */</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> esbuildProblemMatcherPlugin</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  name:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'esbuild-problem-matcher'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">  setup</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">build</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    build</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">onStart</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(() </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">=&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">      console</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">log</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'[watch] build started'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    });</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    build</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">onEnd</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">result</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> =&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">      result</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">errors</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">forEach</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(({ </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">text</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">location</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> }) </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">=&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">        console</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">error</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">`✘ [ERROR] </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">${</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">text</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">`</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">        if</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> (</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">location</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> == </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">null</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) </span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">return</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">        console</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">error</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">`    </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">${</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">location</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">file</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">:</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">${</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">location</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">line</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">:</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">${</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">location</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">column</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">:`</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      });</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">      console</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">log</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'[watch] build finished'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    });</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">};</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">main</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">().</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">catch</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">e</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> =&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  console</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">error</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">e</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  process</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">exit</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#B5CEA8;--shiki-light:#098658">1</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">});</span></span>
<span class="line"></span></code></pre>
<p>The build script does the following:</p>
<ul><li>It creates a build context with esbuild. The context is configured to:
<ul><li>Bundle the code in <code>src/web/extension.ts</code> into a single file <code>dist/web/extension.js</code>.</li>
<li>Bundle all tests, including the test runner (mocha) into a single file <code>dist/web/test/suite/extensionTests.js</code>.</li>
<li>Minify the code if the <code>--production</code> flag was passed.</li>
<li>Generate source maps unless the <code>--production</code> flag was passed.</li>
<li>Exclude the 'vscode' module from the bundle (since it's provided by the VS Code runtime).</li>
<li>creates polyfills for <code>process</code> and <code>buffer</code></li>
<li>Use the esbuildProblemMatcherPlugin plugin to report errors that prevented the bundler to complete. This plugin emits the errors in a format that is detected by the <code>esbuild</code> problem matcher with also needs to be installed as an extension.</li>
<li>Use the testBundlePlugin to implement a test main file (<code>extensionTests.js</code>) that references all tests files and the mocha test runner <code>mochaTestRunner.js</code></li>
</ul></li>
<li>If the <code>--watch</code> flag was passed, it starts watching the source files for changes and rebuilds the bundle whenever a change is detected.</li>
</ul><p>esbuild can work directly with TypeScript files. However, esbuild simply strips off all type declarations without doing any type checks.
Only syntax error are reported and can cause esbuild to fail.</p>
<p>For that reason, we separately run the TypeScript compiler (<code>tsc</code>) to check the types, but without emitting any code (flag <code>--noEmit</code>).</p>
<p>The <code>scripts</code> section in <code>package.json</code> now looks like that</p>
<pre class="shiki" data-lang="json" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">  "scripts"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "vscode:prepublish"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"npm run package-web"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "compile-web"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"npm run check-types &amp;&amp; node esbuild.js"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "watch-web"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"npm-run-all -p watch-web:*"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "watch-web:esbuild"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"node esbuild.js --watch"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "watch-web:tsc"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"tsc --noEmit --watch --project tsconfig.json"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "package-web"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"npm run check-types &amp;&amp; node esbuild.js --production"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "check-types"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"tsc --noEmit"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "pretest"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"npm run compile-web"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "test"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"vscode-test-web --browserType=chromium --extensionDevelopmentPath=. --extensionTestsPath=dist/web/test/suite/extensionTests.js"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "run-in-browser"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"vscode-test-web --browserType=chromium --extensionDevelopmentPath=. ."</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  }</span></span>
<span class="line"></span></code></pre>
<p><code>npm-run-all</code> is a node module that runs scripts in parallel whose name match a given prefix. For us, it runs the <code>watch-web:esbuild</code> and <code>watch-web:tsc</code> scripts. You need to add <code>npm-run-all</code> to the <code>devDependencies</code> section in <code>package.json</code>.</p>
<p>The following <code>tasks.json</code> files gives you separate terminals for each watch task:</p>
<pre class="shiki" data-lang="json" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">{</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "version"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"2.0.0"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "tasks"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">      "label"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"watch-web"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">      "dependsOn"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"npm: watch-web:tsc"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"npm: watch-web:esbuild"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">],</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">      "presentation"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">        "reveal"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"never"</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      },</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">      "group"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">        "kind"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"build"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">        "isDefault"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">true</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      },</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">      "runOptions"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">        "runOn"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"folderOpen"</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    },</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">      "type"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"npm"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">      "script"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"watch-web:esbuild"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">      "group"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"build"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">      "problemMatcher"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"$esbuild-watch"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">      "isBackground"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">true</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">      "label"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"npm: watch-web:esbuild"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">      "presentation"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">        "group"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"watch"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">        "reveal"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"never"</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    },</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">      "type"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"npm"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">      "script"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"watch-web:tsc"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">      "group"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"build"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">      "problemMatcher"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"$tsc-watch"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">      "isBackground"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">true</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">      "label"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"npm: watch-web:tsc"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">      "presentation"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">        "group"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"watch"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">        "reveal"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"never"</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    },</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">      "label"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"compile"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">      "type"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"npm"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">      "script"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"compile-web"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">      "problemMatcher"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"$tsc"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"$esbuild"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">]</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  ]</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<p>This is the <code>mochaTestRunner.js</code> referenced in the esbuild build script:</p>
<pre class="shiki" data-lang="ts" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">// Imports mocha for the browser, defining the `mocha` global.</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">import</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'mocha/mocha'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">mocha</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">setup</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">({</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  ui:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'tdd'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  reporter:</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> undefined</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">});</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">export</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> function</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> run</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(): </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">Promise</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">&lt;</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">void</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">&gt; {</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">  return</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> new</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99"> Promise</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">((</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">c</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">e</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">=&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">    try</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">      // Run the mocha test</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">      mocha</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">run</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">failures</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> =&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">        if</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> (</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">failures</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> &gt; </span><span style="--shiki-dark:#B5CEA8;--shiki-light:#098658">0</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">          e</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">new</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> Error</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">`</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">${</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">failures</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> tests failed.`</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">));</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">        } </span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">else</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">          c</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">();</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">        }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      });</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    } </span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">catch</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> (</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">err</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">      console</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">error</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">err</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">      e</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">err</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  });</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<h2 id="samples" data-needslink="samples">Samples</h2>
<ul><li><a href="https://github.com/microsoft/vscode-extension-samples/tree/main/helloworld-web-sample" class="external-link" target="_blank">helloworld-web-sample</a></li>
<li><a href="https://github.com/microsoft/vscode-extension-samples/tree/main/lsp-web-extension-sample" class="external-link" target="_blank">lsp-web-extension-sample</a></li>
</ul><div class="feedback" data-edit-url="https://vscode.dev/github/microsoft/vscode-docs/blob/main/api/extension-guides/web-extensions.md"></div>
				
				<div class="body-footer">6/3/2026</div>
				
            </main><aside class="docs-right-sidebar hidden-xs"><div class="docs-markdown-actions">
                    <div class="docs-markdown-dropdown" data-raw-url="/raw/api/extension-guides/web-extensions.md">
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
                <nav id="docs-subnavbar" aria-label="On Page"><h4><span class="sr-only">On this page there are 10 sections</span><span aria-hidden="true">On this page</span></h4>
                    <ul class="nav"><li><a href="#web-extension-anatomy">Web extension anatomy</a></li>
                        
                        <li><a href="#develop-a-web-extension">Develop a web extension</a></li>
                        
                        <li><a href="#create-a-web-extension">Create a web extension</a></li>
                        
                        <li><a href="#test-your-web-extension">Test your web extension</a></li>
                        
                        <li><a href="#web-extension-tests">Web extension tests</a></li>
                        
                        <li><a href="#publish-a-web-extension">Publish a web extension</a></li>
                        
                        <li><a href="#update-existing-extensions-to-web-extensions">Update existing extensions to Web extensions</a></li>
                        
                        <li><a href="#web-extension-enablement">Web extension enablement</a></li>
                        
                        <li><a href="#using-esbuild">Using ESBuild</a></li>
                        
                        <li><a href="#samples">Samples</a></li>
                        
                    </ul></nav></aside></div>
		<div class="docs-mobile-widgets visible-xs">
			<div class="connect-widget"></div>
		</div>
	</div>
</div>
		</main>