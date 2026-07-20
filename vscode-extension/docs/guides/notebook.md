# Notebook API

> 源文档: [https://code.visualstudio.com/api/extension-guides/notebook](https://code.visualstudio.com/api/extension-guides/notebook)

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
			          
			        <li class="active">
			          <a href="/api/extension-guides/notebook" aria-label="Current Page: Notebook">Notebook</a>
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
				<select id="small-nav-dropdown" aria-label="topics"><option value="/api">Overview</option><optgroup label="Get Started"><option value="/api/get-started/your-first-extension">Your First Extension</option><option value="/api/get-started/extension-anatomy">Extension Anatomy</option><option value="/api/get-started/wrapping-up">Wrapping Up</option></optgroup><optgroup label="Extension Capabilities"><option value="/api/extension-capabilities/overview">Overview</option><option value="/api/extension-capabilities/common-capabilities">Common Capabilities</option><option value="/api/extension-capabilities/theming">Theming</option><option value="/api/extension-capabilities/extending-workbench">Extending Workbench</option></optgroup><optgroup label="Extension Guides"><option value="/api/extension-guides/overview">Overview</option><optgroup label="Extension Guides - AI"><option value="/api/extension-guides/ai/ai-extensibility-overview">AI Extensibility</option><option value="/api/extension-guides/ai/tools">Language Model Tool</option><option value="/api/extension-guides/ai/mcp">MCP Dev Guide</option><option value="/api/extension-guides/ai/chat">Chat Participant</option><option value="/api/extension-guides/ai/chat-tutorial">Chat Tutorial</option><option value="/api/extension-guides/ai/language-model">Language Model</option><option value="/api/extension-guides/ai/language-model-tutorial">Language Model Tutorial</option><option value="/api/extension-guides/ai/language-model-chat-provider">Language Model Chat Provider</option><option value="/api/extension-guides/ai/prompt-tsx">Prompt TSX</option></optgroup><option value="/api/extension-guides/command">Command</option><option value="/api/extension-guides/color-theme">Color Theme</option><option value="/api/extension-guides/file-icon-theme">File Icon Theme</option><option value="/api/extension-guides/product-icon-theme">Product Icon Theme</option><option value="/api/extension-guides/tree-view">Tree View</option><option value="/api/extension-guides/webview">Webview</option><option value="/api/extension-guides/notebook" selected>Notebook</option><option value="/api/extension-guides/custom-editors">Custom Editors</option><option value="/api/extension-guides/virtual-documents">Virtual Documents</option><option value="/api/extension-guides/virtual-workspaces">Virtual Workspaces</option><option value="/api/extension-guides/web-extensions">Web Extensions</option><option value="/api/extension-guides/workspace-trust">Workspace Trust</option><option value="/api/extension-guides/task-provider">Task Provider</option><option value="/api/extension-guides/scm-provider">Source Control</option><option value="/api/extension-guides/debugger-extension">Debugger Extension</option><option value="/api/extension-guides/markdown-extension">Markdown Extension</option><option value="/api/extension-guides/testing">Test Extension</option><option value="/api/extension-guides/custom-data-extension">Custom Data Extension</option><option value="/api/extension-guides/telemetry">Telemetry</option></optgroup><optgroup label="UX Guidelines"><option value="/api/ux-guidelines/overview">Overview</option><option value="/api/ux-guidelines/activity-bar">Activity Bar</option><option value="/api/ux-guidelines/sidebars">Sidebars</option><option value="/api/ux-guidelines/panel">Panel</option><option value="/api/ux-guidelines/status-bar">Status Bar</option><option value="/api/ux-guidelines/views">Views</option><option value="/api/ux-guidelines/editor-actions">Editor Actions</option><option value="/api/ux-guidelines/quick-picks">Quick Picks</option><option value="/api/ux-guidelines/command-palette">Command Palette</option><option value="/api/ux-guidelines/notifications">Notifications</option><option value="/api/ux-guidelines/webviews">Webviews</option><option value="/api/ux-guidelines/context-menus">Context Menus</option><option value="/api/ux-guidelines/walkthroughs">Walkthroughs</option><option value="/api/ux-guidelines/settings">Settings</option></optgroup><optgroup label="Language Extensions"><option value="/api/language-extensions/overview">Overview</option><option value="/api/language-extensions/syntax-highlight-guide">Syntax Highlight Guide</option><option value="/api/language-extensions/semantic-highlight-guide">Semantic Highlight Guide</option><option value="/api/language-extensions/snippet-guide">Snippet Guide</option><option value="/api/language-extensions/language-configuration-guide">Language Configuration Guide</option><option value="/api/language-extensions/programmatic-language-features">Programmatic Language Features</option><option value="/api/language-extensions/language-server-extension-guide">Language Server Extension Guide</option><option value="/api/language-extensions/embedded-languages">Embedded Languages</option></optgroup><optgroup label="Testing and Publishing"><option value="/api/working-with-extensions/testing-extension">Testing Extensions</option><option value="/api/working-with-extensions/publishing-extension">Publishing Extensions</option><option value="/api/working-with-extensions/bundling-extension">Bundling Extensions</option><option value="/api/working-with-extensions/continuous-integration">Continuous Integration</option></optgroup><optgroup label="Advanced Topics"><option value="/api/advanced-topics/extension-host">Extension Host</option><option value="/api/advanced-topics/remote-extensions">Remote Development and Codespaces</option><option value="/api/advanced-topics/using-proposed-api">Using Proposed API</option><option value="/api/advanced-topics/tslint-eslint-migration">Migrate from TSLint to ESLint</option><option value="/api/advanced-topics/python-extension-template">Python Extension Template</option></optgroup><optgroup label="References"><option value="/api/references/vscode-api">VS Code API</option><option value="/api/references/contribution-points">Contribution Points</option><option value="/api/references/activation-events">Activation Events</option><option value="/api/references/extension-manifest">Extension Manifest</option><option value="/api/references/commands">Built-In Commands</option><option value="/api/references/when-clause-contexts">When Clause Contexts</option><option value="/api/references/theme-color">Theme Color</option><option value="/api/references/icons-in-labels">Product Icon Reference</option><option value="/api/references/document-selector">Document Selector</option></optgroup></select></nav></aside><div class="docs-content-wrapper">
			
			<main class="docs-main-content body"><h1>Notebook API</h1>
<p>The Notebook API allows Visual Studio Code extensions to open files as notebooks, execute notebook code cells, and render notebook outputs in a variety of rich and interactive formats. You may know of popular notebook interfaces like Jupyter Notebook or Google Colab – the Notebook API allows for similar experiences inside Visual Studio Code.</p>
<h2 id="parts-of-a-notebook" data-needslink="parts-of-a-notebook">Parts of a Notebook</h2>
<p>A notebook consists of a sequence of cells and their outputs. The cells of a notebook can be either <strong>Markdown cells</strong> or <strong>code cells</strong>, and are rendered within the core of VS Code. The outputs can be of various formats. Some output formats, such as plain text, JSON, images, and HTML are rendered by VS Code core. Others, such as application-specific data or interactive applets, are rendered by extensions.</p>
<p>Cells in a notebook are read and written to the file system by a <code>NotebookSerializer</code>, which handles reading data from the file system and converting it into a description of cells, as well as persisting modifications to the notebook back to the file system. The <strong>code cells</strong> of a notebook can be executed by a <code>NotebookController</code>, which takes the contents of a cell and from it produces zero or more outputs in a variety of formats ranging from plain text to formatted documents or interactive applets. Application-specific output formats and interactive applet outputs are rendered by a <code>NotebookRenderer</code>.</p>
<p>Visually:</p>
<p><img src="/assets/api/extension-guides/notebook/architecture-overview.png" alt="Overview of 3 components of notebooks: NotebookSerializer, NotebookController, and NotebookRenderer, and how they interact. Described textually above and in following sections." loading="lazy"></p>
<h2 id="serializer" data-needslink="serializer">Serializer</h2>
<p><a href="https://github.com/microsoft/vscode/blob/e1a8566a298dcced016d8e16db95c33c270274b4/src/vs/vscode.d.ts#L11865-L11884" class="external-link" target="_blank">NotebookSerializer API Reference</a></p>
<p>A <code>NotebookSerializer</code> is responsible for taking the serialized bytes of a notebook and deserializing those bytes into <code>NotebookData</code>, which contains list of Markdown and code cells. It is responsible for the opposite conversion as well: taking <code>NotebookData</code> and converting the data into serialized bytes to be saved.</p>
<p>Samples:</p>
<ul><li><a href="https://github.com/microsoft/notebook-extension-samples/tree/main/notebook-serializer" class="external-link" target="_blank">JSON Notebook Serializer</a>: Simple example notebook that takes JSON input and outputs prettified JSON in a custom <code>NotebookRenderer</code>.</li>
<li><a href="https://github.com/microsoft/vscode-markdown-notebook" class="external-link" target="_blank">Markdown Serializer</a>: Open and edit Markdown files as a notebook.</li>
</ul><h3 id="example" data-needslink="example">Example</h3>
<p>In this example, we build a simplified notebook provider extension for viewing files in the <a href="https://nbformat.readthedocs.io/en/latest/format_description.html" class="external-link" target="_blank">Jupyter Notebook format</a> with a <code>.notebook</code> extension (instead of its traditional file extension <code>.ipynb</code>).</p>
<p>A notebook serializer is declared in <code>package.json</code> under the <code>contributes.notebooks</code> section as follows:</p>
<pre class="shiki" data-lang="json" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">{</span></span>
<span class="line"><span style="--shiki-dark:#F44747;--shiki-light:#CD3131">    ...</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "contributes"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#F44747;--shiki-light:#CD3131">        ...</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">        "notebooks"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">            {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">                "type"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"my-notebook"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">                "displayName"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"My Notebook"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">                "selector"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">                    {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">                        "filenamePattern"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"*.notebook"</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">                    }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">                ]</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">            }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">        ]</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<p>The notebook serializer is then registered in the extension's activation event:</p>
<pre class="shiki" data-lang="ts" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">import</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> { </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">TextDecoder</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">TextEncoder</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> } </span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">from</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'util'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">import</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> *</span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB"> as</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> vscode</span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB"> from</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'vscode'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">export</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> function</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> activate</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">context</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">ExtensionContext</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  context</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">subscriptions</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">push</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">workspace</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">registerNotebookSerializer</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'my-notebook'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">new</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> SampleSerializer</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">())</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  );</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">interface</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99"> RawNotebook</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  cells</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">RawNotebookCell</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">[];</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">interface</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99"> RawNotebookCell</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  source</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">string</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">[];</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  cell_type</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'code'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> | </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'markdown'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">class</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99"> SampleSerializer</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> implements</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99"> vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">NotebookSerializer</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">  async</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> deserializeNotebook</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    content</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">Uint8Array</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    _token</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">CancellationToken</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  ): </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">Promise</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">&lt;</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">NotebookData</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">&gt; {</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">    var</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> contents</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">new</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> TextDecoder</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">().</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">decode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">content</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">    let</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> raw</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">RawNotebookCell</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">[];</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">    try</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">      raw</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = (&lt;</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">RawNotebook</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">&gt;</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1">JSON</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">parse</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">contents</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">)).</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">cells</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    } </span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">catch</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">      raw</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = [];</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    }</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">    const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> cells</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">raw</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">map</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">      item</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> =&gt;</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">        new</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">NotebookCellData</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">          item</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">cell_type</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> === </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'code'</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">            ? </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">NotebookCellKind</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">Code</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">            : </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">NotebookCellKind</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">Markup</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">          item</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">source</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">join</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\n</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">),</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">          item</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">cell_type</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> === </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'code'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> ? </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'python'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> : </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'markdown'</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">        )</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    );</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">    return</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> new</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">NotebookData</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">cells</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  }</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">  async</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> serializeNotebook</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    data</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">NotebookData</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    _token</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">CancellationToken</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  ): </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">Promise</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">&lt;</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">Uint8Array</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">&gt; {</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">    let</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> contents</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">RawNotebookCell</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">[] = [];</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">    for</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> (</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> cell</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> of</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> data</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">cells</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">      contents</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">push</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">({</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">        cell_type:</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> cell</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">kind</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> === </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">NotebookCellKind</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">Code</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> ? </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'code'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> : </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'markdown'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">        source:</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> cell</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">value</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">split</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#D16969;--shiki-light:#811F3F">/\r</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#000000">?</span><span style="--shiki-dark:#D16969;--shiki-light:#811F3F">\n/</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">g</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">)</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      });</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    }</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">    return</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> new</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> TextEncoder</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">().</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">encode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1">JSON</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">stringify</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">contents</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">));</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<p>Now try running your extension and opening a Jupyter Notebook formatted file saved with the <code>.notebook</code> extension:</p>
<p><img src="/assets/api/extension-guides/notebook/ipynb-simple-provider.png" alt="Notebook showing contents of a Jupyter Notebook formatted file" loading="lazy"></p>
<p>You should be able to open Jupyter-formatted notebooks and view their cells as both plain text and rendered Markdown, as well as edit the cells. However, outputs will not be persisted to disk; to save outputs you would need to also serialize and deserialize the outputs of cells from <code>NotebookData</code>.</p>
<p>To run a cell, you will need to implement a <code>NotebookController</code>.</p>
<h2 id="controller" data-needslink="controller">Controller</h2>
<p><a href="https://github.com/microsoft/vscode/blob/e1a8566a298dcced016d8e16db95c33c270274b4/src/vs/vscode.d.ts#L11941" class="external-link" target="_blank">NotebookController API Reference</a></p>
<p>A <code>NotebookController</code> is responsible for taking a <strong>code cell</strong> and executing the code to produce some or no outputs.</p>
<p>A controller is directly associated with a notebook serializer and a type of notebook by setting the <code>NotebookController#notebookType</code> property on creation of the controller. Then the controller is registered globally by pushing the controller onto the extension subscriptions on activate of the extension.</p>
<pre class="shiki" data-lang="ts" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">export</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> function</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> activate</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">context</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">ExtensionContext</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  context</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">subscriptions</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">push</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">new</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> Controller</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">());</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">class</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99"> Controller</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">  readonly</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> controllerId</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'my-notebook-controller-id'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">  readonly</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> notebookType</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'my-notebook'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">  readonly</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> label</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'My Notebook'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">  readonly</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> supportedLanguages</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = [</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'python'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">];</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">  private</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> readonly</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> _controller</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">NotebookController</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">  private</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> _executionOrder</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#B5CEA8;--shiki-light:#098658">0</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">  constructor</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">() {</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">    this</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">_controller</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">notebooks</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">createNotebookController</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">      this</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">controllerId</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">      this</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">notebookType</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">      this</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">label</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    );</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">    this</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">_controller</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">supportedLanguages</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">this</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">supportedLanguages</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">    this</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">_controller</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">supportsExecutionOrder</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">true</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">    this</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">_controller</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">executeHandler</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">this</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">_execute</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">bind</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">this</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  }</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">  private</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> _execute</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    cells</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">NotebookCell</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">[],</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    _notebook</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">NotebookDocument</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    _controller</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">NotebookController</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  ): </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">void</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">    for</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> (</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">let</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> cell</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> of</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> cells</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">      this</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">_doExecution</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">cell</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  }</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">  private</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> async</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> _doExecution</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">cell</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">NotebookCell</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">): </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">Promise</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">&lt;</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">void</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">&gt; {</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">    const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> execution</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">this</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">_controller</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">createNotebookCellExecution</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">cell</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    execution</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">executionOrder</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = ++</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">this</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">_executionOrder</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    execution</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">start</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">Date</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">now</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">()); </span><span style="--shiki-dark:#6A9955;--shiki-light:#008000">// Keep track of elapsed time to execute cell.</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">    /* Do some execution here; not implemented */</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    execution</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">replaceOutput</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">([</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">      new</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">NotebookCellOutput</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">([</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">        vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">NotebookCellOutputItem</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">text</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'Dummy output text!'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">)</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      ])</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    ]);</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    execution</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">end</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">true</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">Date</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">now</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">());</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<p>If you're publishing a <code>NotebookController</code>-providing extension separately from its serializer, then add an entry like <code>notebookKernel&lt;ViewTypeUpperCamelCased&gt;</code> to the <code>keywords</code> in its <code>package.json</code>. For example, if you published an alternative kernel for the <code>github-issues</code> notebook type, you should add a keyword <code>notebookKernelGithubIssues</code> keyword to your extension.
This improves the discoverability of the extension when opening notebooks of the type <code>&lt;ViewTypeUpperCamelCased&gt;</code> from within Visual Studio Code.</p>
<p>Samples:</p>
<ul><li><a href="https://github.com/microsoft/vscode-github-issue-notebooks/blob/93359d842cd01dfaef0a78b620c5a3b4cf5c2e38/src/extension/notebookProvider.ts#L29" class="external-link" target="_blank">GitHub Issues Notebook</a>: Controller to execute queries for GitHub Issues</li>
<li><a href="https://github.com/tanhakabir/rest-book/blob/main/src/extension/notebookKernel.ts" class="external-link" target="_blank">REST Book</a>: Controller to run REST queries.</li>
<li><a href="https://github.com/jrieken/vscode-regex-notebook/blob/master/src/extension/extension.ts#L56" class="external-link" target="_blank">Regexper notebooks</a>: Controller to visualize regular expressions.</li>
</ul><h2 id="output-types" data-needslink="output-types">Output types</h2>
<p>Outputs must be in one of three formats: Text Output, Error Output, or Rich Output. A kernel may provide multiple outputs for a single execution of a cell, in which case they will be displayed as a list.</p>
<p>Simple formats like Text Output, Error Output, or "simple" variants of Rich Output (HTML, Markdown, JSON, etc.) are rendered by VS Code core, whereas application specific Rich Output types are rendered by a <a href="#_notebook-renderer">NotebookRenderer</a>. An extension may optionally choose to render "simple" Rich Outputs itself, for instance to add LaTeX support to Markdown outputs.</p>
<p><img src="/assets/api/extension-guides/notebook/kernel.png" alt="Diagram of the different output types described above" loading="lazy"></p>
<h3 id="text-output" data-needslink="text-output">Text Output</h3>
<p>Text outputs are the most simple output format, and work much like many REPLs you may be familiar with. They consist only of a <code>text</code> field, which is rendered as plain text in the cell's output element:</p>
<pre class="shiki" data-lang="ts" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">NotebookCellOutputItem</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">text</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'This is the output...'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"></span></code></pre>
<p><img src="/assets/api/extension-guides/notebook/text-output.png" alt="Cell with simple text output" loading="lazy"></p>
<h3 id="error-output" data-needslink="error-output">Error Output</h3>
<p>Error outputs are helpful for displaying runtime errors in a consistent and understandable manner. They support standard <code>Error</code> objects.</p>
<pre class="shiki" data-lang="ts" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">try</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">  /* Some code */</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">} </span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">catch</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> (</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">error</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">NotebookCellOutputItem</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">error</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">error</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<p><img src="/assets/api/extension-guides/notebook/error-output.png" alt="Cell with error output showing error name and message, as well as a stack trace with magenta text" loading="lazy"></p>
<h3 id="rich-output" data-needslink="rich-output">Rich Output</h3>
<p>Rich outputs are the most advanced form of displaying cell outputs. They allow for providing many different representations of the output data, keyed by mimetype. For example, if a cell output was to represent a GitHub Issue, the kernel might produce a rich output with several properties on its <code>data</code> field:</p>
<ul><li>A <code>text/html</code> field containing a formatted view of the issue.</li>
<li>A <code>text/x-json</code> field containing a machine readable view.</li>
<li>An <code>application/github-issue</code> field that a <code>NotebookRenderer</code> could use to create a fully interactive view of the issue.</li>
</ul><p>In this case, the <code>text/html</code> and <code>text/x-json</code> views will be rendered by VS Code natively, but the <code>application/github-issue</code> view will display an error if no <code>NotebookRenderer</code> was registered to that mimetype.</p>
<pre class="shiki" data-lang="ts" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">execution</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">replaceOutput</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">([</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">new</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">NotebookCellOutput</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">([</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">                            vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">NotebookCellOutputItem</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">text</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'&lt;b&gt;Hello&lt;/b&gt; World'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'text/html'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">),</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">                            vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">NotebookCellOutputItem</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">json</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">({ </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">hello:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'world'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> }),</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">                            vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">NotebookCellOutputItem</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">json</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">({ custom-data-for-custom-</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">renderer:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'data'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> }, </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'application/custom'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">),</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">                        ])]);</span></span>
<span class="line"></span></code></pre>
<p><img src="/assets/api/extension-guides/notebook/rich-output.gif" alt="Cell with rich output showing switching between formatted HTML, a JSON editor, and an error message showing no renderer is available (application/hello-world)" loading="lazy"></p>
<p>By default, VS Code can render the following mimetypes:</p>
<ul><li>application/javascript</li>
<li>text/html</li>
<li>image/svg+xml</li>
<li>text/markdown</li>
<li>image/png</li>
<li>image/jpeg</li>
<li>text/plain</li>
</ul><p>VS Code will render these mimetypes as code in a built-in editor:</p>
<ul><li>text/x-json</li>
<li>text/x-javascript</li>
<li>text/x-html</li>
<li>text/x-rust</li>
<li>... text/x-LANGUAGE_ID for any other built-in or installed languages.</li>
</ul><p>This notebook is using the built-in editor to display some Rust code:
<img src="/assets/api/extension-guides/notebook/rust-output.png" alt="Notebook displaying Rust code in a built in Monaco editor" loading="lazy"></p>
<p>To render an alternative mimetype, a <code>NotebookRenderer</code> must be registered for that mimetype.</p>
<h2 id="notebook-renderer" data-needslink="notebook-renderer">Notebook Renderer</h2>
<p>A notebook renderer is responsible for taking output data of a specific mimetype and providing a rendered view of that data. A renderer shared by output cells can maintain global state between these cells. The complexity of the rendered view can range from simple static HTML to dynamic fully interactive applets. In this section, we'll explore various techniques for rendering an output representing a GitHub Issue.</p>
<p>You can get started quickly using boilerplate from our Yeoman generators. To do so, first install Yeoman and the VS Code Generators using:</p>
<pre class="shiki" data-lang="bash" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">npm</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> install</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> -g</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> yo</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> generator-code</span></span>
<span class="line"></span></code></pre>
<p>Then, run <code>yo code</code> and choose <code>New Notebook Renderer (TypeScript)</code>.</p>
<p>If you don't use this template, you'll just want to make sure that you add <code>notebookRenderer</code> to the <code>keywords</code> in your extension's <code>package.json</code>, and mention its mimetype somewhere in the extension name or description, so that users can find your renderer.</p>
<h3 id="a-simple-noninteractive-renderer" data-needslink="a-simple-noninteractive-renderer">A Simple, Non-Interactive Renderer</h3>
<p>Renderers are declared for a set of mimetypes by contributing to the <code>contributes.notebookRenderer</code> property of an extension's <code>package.json</code>. This renderer will work with input in the <code>ms-vscode.github-issue-notebook/github-issue</code> format, which we will assume some installed controller is able to provide:</p>
<pre class="shiki" data-lang="json" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">{</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "activationEvents"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"...."</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">],</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "contributes"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#F44747;--shiki-light:#CD3131">    ...</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "notebookRenderer"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">        "id"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"github-issue-renderer"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">        "displayName"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"GitHub Issue Renderer"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">        "entrypoint"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"./out/renderer.js"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">        "mimeTypes"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">          "ms-vscode.github-issue-notebook/github-issue"</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">        ]</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    ]</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<p>Output renderers are always rendered in a single <code>iframe</code>, separate from the rest of VS Code's UI, to ensure they don't accidentally interfere or cause slowdowns in VS Code. The contribution refers to an "entrypoint" script, which is loaded into the notebook's <code>iframe</code> right before any output needs to be rendered. Your entrypoint needs to be a single file, which you can write yourself, or use a bundler like Webpack, Rollup, or Parcel to create.</p>
<p>When it's loaded, your entrypoint script should export <code>ActivationFunction</code> from <code>vscode-notebook-renderer</code> to render your UI once VS Code is ready to render your renderer. For example, this will put all your GitHub issue data as JSON into the cell output:</p>
<pre class="shiki" data-lang="js" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">import</span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB"> type</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> { </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">ActivationFunction</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> } </span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">from</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'vscode-notebook-renderer'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">export</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> const</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> activate</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">ActivationFunction</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">context</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> =&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> ({</span></span>
<span class="line"><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">  renderOutputItem</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">data</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">element</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    element</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">innerText</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1">JSON</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">stringify</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">data</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">json</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">());</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">});</span></span>
<span class="line"></span></code></pre>
<p>You can <a href="https://github.com/DefinitelyTyped/DefinitelyTyped/blob/master/types/vscode-notebook-renderer/index.d.ts" class="external-link" target="_blank">refer to the complete API definition here</a>. If you're using TypeScript, you can install <code>@types/vscode-notebook-renderer</code> and then add <code>vscode-notebook-renderer</code> to the <code>types</code> array in your <code>tsconfig.json</code> to make these types available in your code.</p>
<p>To create richer content, you could manually create DOM elements, or use a framework like Preact and render it into the output element, for example:</p>
<pre class="shiki" data-lang="jsx" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">import</span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB"> type</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> { </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">ActivationFunction</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> } </span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">from</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'vscode-notebook-renderer'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">import</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> { </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">h</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">render</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> } </span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">from</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'preact'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">const</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> Issue</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">FunctionComponent</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">&lt;{ </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">issue</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">GithubIssue</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> }&gt; = ({ </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">issue</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> }) </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">=&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> (</span></span>
<span class="line"><span style="--shiki-dark:#808080;--shiki-light:#800000">  &lt;</span><span style="--shiki-dark:#569CD6;--shiki-light:#800000">div</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#E50000"> key</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">=</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">{</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">issue</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">number</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&gt;</span></span>
<span class="line"><span style="--shiki-dark:#808080;--shiki-light:#800000">    &lt;</span><span style="--shiki-dark:#569CD6;--shiki-light:#800000">h2</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&gt;</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">      {</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">issue</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">title</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      (</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&lt;</span><span style="--shiki-dark:#569CD6;--shiki-light:#800000">a</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#E50000"> href</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">=</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">{</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">`https://github.com/</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">${</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">issue</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">repo</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">/issues/</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">${</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">issue</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">number</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">`</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">#</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">{</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">issue</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">number</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&lt;/</span><span style="--shiki-dark:#569CD6;--shiki-light:#800000">a</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">)</span></span>
<span class="line"><span style="--shiki-dark:#808080;--shiki-light:#800000">    &lt;/</span><span style="--shiki-dark:#569CD6;--shiki-light:#800000">h2</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&gt;</span></span>
<span class="line"><span style="--shiki-dark:#808080;--shiki-light:#800000">    &lt;</span><span style="--shiki-dark:#569CD6;--shiki-light:#800000">img</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#E50000"> src</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">=</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">{</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">issue</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">user</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">avatar_url</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#E50000"> style</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">=</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">{</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">{ </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">float:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'left'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">width:</span><span style="--shiki-dark:#B5CEA8;--shiki-light:#098658"> 32</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">borderRadius:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> '50%'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">marginRight:</span><span style="--shiki-dark:#B5CEA8;--shiki-light:#098658"> 20</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF"> }</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#808080;--shiki-light:#800000"> /&gt;</span></span>
<span class="line"><span style="--shiki-dark:#808080;--shiki-light:#800000">    &lt;</span><span style="--shiki-dark:#569CD6;--shiki-light:#800000">i</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">@</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">{</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">issue</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">user</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">login</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&lt;/</span><span style="--shiki-dark:#569CD6;--shiki-light:#800000">i</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> Opened: </span><span style="--shiki-dark:#808080;--shiki-light:#800000">&lt;</span><span style="--shiki-dark:#569CD6;--shiki-light:#800000">div</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#E50000"> style</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">=</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"margin-top: 10px"</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&gt;</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">{</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">issue</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">body</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&lt;/</span><span style="--shiki-dark:#569CD6;--shiki-light:#800000">div</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&gt;</span></span>
<span class="line"><span style="--shiki-dark:#808080;--shiki-light:#800000">  &lt;/</span><span style="--shiki-dark:#569CD6;--shiki-light:#800000">div</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&gt;</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">const</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> GithubIssues</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">FunctionComponent</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">&lt;{ </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">issues</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">GithubIssue</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">[]; }&gt; = ({ </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">issues</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> }) </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">=&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> (</span></span>
<span class="line"><span style="--shiki-dark:#808080;--shiki-light:#800000">  &lt;</span><span style="--shiki-dark:#569CD6;--shiki-light:#800000">div</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&gt;</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">{</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">issues</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">map</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">issue</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> =&gt;</span><span style="--shiki-dark:#808080;--shiki-light:#800000"> &lt;</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">Issue</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#E50000"> key</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">=</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">{</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">issue</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">number</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#E50000"> issue</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">=</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">{</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">issue</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#808080;--shiki-light:#800000"> /&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">)</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&lt;/</span><span style="--shiki-dark:#569CD6;--shiki-light:#800000">div</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&gt;</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">export</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> const</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> activate</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">ActivationFunction</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = (</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">context</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">=&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> ({</span></span>
<span class="line"><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">    renderOutputItem</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">data</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">element</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">        render</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&lt;</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">GithubIssues</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#E50000"> issues</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">=</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">{</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">data</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">json</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">()</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#808080;--shiki-light:#800000"> /&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">element</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">});</span></span>
<span class="line"></span></code></pre>
<p>Running this renderer on an output cell with a <code>ms-vscode.github-issue-notebook/github-issue</code> data field gives us the following static HTML view:</p>
<p><img src="/assets/api/extension-guides/notebook/static-renderer-sample.png" alt="Cell output showing rendered HTML view of issue" loading="lazy"></p>
<p>If you have elements outside of the container or other asynchronous processes, you can use <code>disposeOutputItem</code> to tear them down. This event will fire when output is cleared, a cell is deleted, and before new output is rendered for an existing cell. For example:</p>
<pre class="shiki" data-lang="js" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> intervals</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">new</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> Map</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">();</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">export</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> const</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> activate</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">ActivationFunction</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = (</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">context</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">=&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> ({</span></span>
<span class="line"><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">    renderOutputItem</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">data</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">element</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">        render</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&lt;</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">GithubIssues</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#E50000"> issues</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">=</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">{</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">data</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">json</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">()</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#808080;--shiki-light:#800000"> /&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">element</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">        intervals</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">set</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">data</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">mime</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">setInterval</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(() </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">=&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">            if</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">element</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">querySelector</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'h2'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">)) {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">                element</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">querySelector</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'h2'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">)!.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">style</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">color</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">`hsl(</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">${</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">Math</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">random</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">() </span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">*</span><span style="--shiki-dark:#B5CEA8;--shiki-light:#098658"> 360</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">, 100%, 50%)`</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">            }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">        }, </span><span style="--shiki-dark:#B5CEA8;--shiki-light:#098658">1000</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">));</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    },</span></span>
<span class="line"><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">    disposeOutputItem</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">id</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">        clearInterval</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">intervals</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">get</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">id</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">));</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">        intervals</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">delete</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">id</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">});</span></span>
<span class="line"></span></code></pre>
<p>It's important to bear in mind that all outputs for a notebook are rendered in different elements in the same iframe. If you use functions like <code>document.querySelector</code>, make sure to scope it to the specific output you're interested in to avoid conflicting with other outputs. In this example, we use <code>element.querySelector</code> to avoid that issue.</p>
<h3 id="interactive-notebooks-communicating-with-the-controller" data-needslink="interactive-notebooks-communicating-with-the-controller">Interactive Notebooks (communicating with the controller)</h3>
<p>Imagine we want to add the ability to view an issue's comments after clicking a button in the rendered output. Assuming a controller can provide issue data with comments under the <code>ms-vscode.github-issue-notebook/github-issue-with-comments</code> mimetype, we might try to retrieve all the comments up front and implement it as follows:</p>
<pre class="shiki" data-lang="jsx" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">const</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> Issue</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">FunctionComponent</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">&lt;{ </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">issue</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">GithubIssueWithComments</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> }&gt; = ({ </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">issue</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> }) </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">=&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">  const</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> [</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1">showComments</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1">setShowComments</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">] = </span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">useState</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">false</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">  return</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> (</span></span>
<span class="line"><span style="--shiki-dark:#808080;--shiki-light:#800000">    &lt;</span><span style="--shiki-dark:#569CD6;--shiki-light:#800000">div</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#E50000"> key</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">=</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">{</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">issue</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">number</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&gt;</span></span>
<span class="line"><span style="--shiki-dark:#808080;--shiki-light:#800000">      &lt;</span><span style="--shiki-dark:#569CD6;--shiki-light:#800000">h2</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&gt;</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">        {</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">issue</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">title</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">        (</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&lt;</span><span style="--shiki-dark:#569CD6;--shiki-light:#800000">a</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#E50000"> href</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">=</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">{</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">`https://github.com/</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">${</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">issue</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">repo</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">/issues/</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">${</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">issue</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">number</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">`</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">#</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">{</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">issue</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">number</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&lt;/</span><span style="--shiki-dark:#569CD6;--shiki-light:#800000">a</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">)</span></span>
<span class="line"><span style="--shiki-dark:#808080;--shiki-light:#800000">      &lt;/</span><span style="--shiki-dark:#569CD6;--shiki-light:#800000">h2</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&gt;</span></span>
<span class="line"><span style="--shiki-dark:#808080;--shiki-light:#800000">      &lt;</span><span style="--shiki-dark:#569CD6;--shiki-light:#800000">img</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#E50000"> src</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">=</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">{</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">issue</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">user</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">avatar_url</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#E50000"> style</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">=</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">{</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">{ </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">float:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'left'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">width:</span><span style="--shiki-dark:#B5CEA8;--shiki-light:#098658"> 32</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">borderRadius:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> '50%'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">marginRight:</span><span style="--shiki-dark:#B5CEA8;--shiki-light:#098658"> 20</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF"> }</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#808080;--shiki-light:#800000"> /&gt;</span></span>
<span class="line"><span style="--shiki-dark:#808080;--shiki-light:#800000">      &lt;</span><span style="--shiki-dark:#569CD6;--shiki-light:#800000">i</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">@</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">{</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">issue</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">user</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">login</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&lt;/</span><span style="--shiki-dark:#569CD6;--shiki-light:#800000">i</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> Opened: </span><span style="--shiki-dark:#808080;--shiki-light:#800000">&lt;</span><span style="--shiki-dark:#569CD6;--shiki-light:#800000">div</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#E50000"> style</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">=</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"margin-top: 10px"</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&gt;</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">{</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">issue</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">body</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&lt;/</span><span style="--shiki-dark:#569CD6;--shiki-light:#800000">div</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&gt;</span></span>
<span class="line"><span style="--shiki-dark:#808080;--shiki-light:#800000">      &lt;</span><span style="--shiki-dark:#569CD6;--shiki-light:#800000">button</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#E50000"> onClick</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">=</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">{</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">() </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">=&gt;</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> setShowComments</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">(</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">true</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">)</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">Show Comments</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&lt;/</span><span style="--shiki-dark:#569CD6;--shiki-light:#800000">button</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&gt;</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">      {</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">showComments</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> &amp;&amp;</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> issue</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">comments</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">map</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">comment</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> =&gt;</span><span style="--shiki-dark:#808080;--shiki-light:#800000"> &lt;</span><span style="--shiki-dark:#569CD6;--shiki-light:#800000">div</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&gt;</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">{</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">comment</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">text</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&lt;/</span><span style="--shiki-dark:#569CD6;--shiki-light:#800000">div</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">)</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span></span>
<span class="line"><span style="--shiki-dark:#808080;--shiki-light:#800000">    &lt;/</span><span style="--shiki-dark:#569CD6;--shiki-light:#800000">div</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&gt;</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  );</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">};</span></span>
<span class="line"></span></code></pre>
<p>This immediately raises some flags. For one, we're loading full comment data for all issues, even before we've clicked the button. Additionally, we require controller support for a whole different mimetype even though we just want to show a bit more data.</p>
<p>Instead, the controller can provide additional functionality to the renderer by including a preload script which VS Code will load in the iframe as well. This script has access global functions <code>postKernelMessage</code> and <code>onDidReceiveKernelMessage</code> that can be used to communicate with the controller.</p>
<p><img src="/assets/api/extension-guides/notebook/kernel-communication.png" alt="Diagram showing how controllers interact with renderers through the NotebookRendererScript" loading="lazy"></p>
<p>For example, you might modify your controller <code>rendererScripts</code> to reference a new file where you create a connection back to the Extension Host, and expose a global communication script for the renderer to use.</p>
<p>In your controller:</p>
<pre class="shiki" data-lang="ts" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">class</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99"> Controller</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">  // ...</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">  readonly</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> rendererScriptId</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'my-renderer-script'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">  constructor</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">() {</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">    // ...</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">    this</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">_controller</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">rendererScripts</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">push</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">      new</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">NotebookRendererScript</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">        vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">Uri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">file</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#6A9955;--shiki-light:#008000">/* path to script */</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">),</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">        rendererScriptId</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      )</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    );</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<p>In your <code>package.json</code> specify your script as a dependency of your renderer:</p>
<pre class="shiki" data-lang="json" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">{</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "activationEvents"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"...."</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">],</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "contributes"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#F44747;--shiki-light:#CD3131">    ...</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "notebookRenderer"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">        "id"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"github-issue-renderer"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">        "displayName"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"GitHub Issue Renderer"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">        "entrypoint"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"./out/renderer.js"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">        "mimeTypes"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span><span style="--shiki-dark:#F44747;--shiki-light:#CD3131">...</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">],</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">        "dependencies"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">            "my-renderer-script"</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">        ]</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    ]</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<p>In your script file you can declare communication functions to communicate with the controller:</p>
<pre class="shiki" data-lang="js" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">import</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'vscode-notebook-renderer/preload'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">globalThis</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">githubIssueCommentProvider</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = {</span></span>
<span class="line"><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">  loadComments</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">issueId</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">string</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">callback</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: (</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">comments</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">GithubComment</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">[]) </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">=&gt;</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99"> void</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">    postKernelMessage</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">({ </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">command:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'comments'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">issueId</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> });</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">    onDidReceiveKernelMessage</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">event</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> =&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">      if</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> (</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">event</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">data</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">type</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> === </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'comments'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> &amp;&amp; </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">event</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">data</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">issueId</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> === </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">issueId</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">        callback</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">event</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">data</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">comments</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    });</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">};</span></span>
<span class="line"></span></code></pre>
<p>And then you can consume that in the renderer. You want to make sure that you check whether the global exposed by the controller's render scripts is available, since other developers might create github issue output in other notebooks and controllers that don't implement the <code>githubIssueCommentProvider</code>. In this case, we'll only show the <strong>Load Comments</strong> button if the global is available:</p>
<pre class="shiki" data-lang="jsx" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> canLoadComments</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">globalThis</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">githubIssueCommentProvider</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> !== </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">undefined</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">const</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> Issue</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">FunctionComponent</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">&lt;{ </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">issue</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">GithubIssue</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> }&gt; = ({ </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">issue</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> }) </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">=&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">  const</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> [</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1">comments</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1">setComments</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">] = </span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">useState</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">([]);</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">  const</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> loadComments</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = () </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">=&gt;</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    globalThis</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">githubIssueCommentProvider</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">loadComments</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">issue</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">id</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">setComments</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">  return</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> (</span></span>
<span class="line"><span style="--shiki-dark:#808080;--shiki-light:#800000">    &lt;</span><span style="--shiki-dark:#569CD6;--shiki-light:#800000">div</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#E50000"> key</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">=</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">{</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">issue</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">number</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&gt;</span></span>
<span class="line"><span style="--shiki-dark:#808080;--shiki-light:#800000">      &lt;</span><span style="--shiki-dark:#569CD6;--shiki-light:#800000">h2</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&gt;</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">        {</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">issue</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">title</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">        (</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&lt;</span><span style="--shiki-dark:#569CD6;--shiki-light:#800000">a</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#E50000"> href</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">=</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">{</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">`https://github.com/</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">${</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">issue</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">repo</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">/issues/</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">${</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">issue</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">number</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">`</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">#</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">{</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">issue</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">number</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&lt;/</span><span style="--shiki-dark:#569CD6;--shiki-light:#800000">a</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">)</span></span>
<span class="line"><span style="--shiki-dark:#808080;--shiki-light:#800000">      &lt;/</span><span style="--shiki-dark:#569CD6;--shiki-light:#800000">h2</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&gt;</span></span>
<span class="line"><span style="--shiki-dark:#808080;--shiki-light:#800000">      &lt;</span><span style="--shiki-dark:#569CD6;--shiki-light:#800000">img</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#E50000"> src</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">=</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">{</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">issue</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">user</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">avatar_url</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#E50000"> style</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">=</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">{</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">{ </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">float:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'left'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">width:</span><span style="--shiki-dark:#B5CEA8;--shiki-light:#098658"> 32</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">borderRadius:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> '50%'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">marginRight:</span><span style="--shiki-dark:#B5CEA8;--shiki-light:#098658"> 20</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF"> }</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#808080;--shiki-light:#800000"> /&gt;</span></span>
<span class="line"><span style="--shiki-dark:#808080;--shiki-light:#800000">      &lt;</span><span style="--shiki-dark:#569CD6;--shiki-light:#800000">i</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">@</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">{</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">issue</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">user</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">login</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&lt;/</span><span style="--shiki-dark:#569CD6;--shiki-light:#800000">i</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> Opened: </span><span style="--shiki-dark:#808080;--shiki-light:#800000">&lt;</span><span style="--shiki-dark:#569CD6;--shiki-light:#800000">div</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#E50000"> style</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">=</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"margin-top: 10px"</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&gt;</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">{</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">issue</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">body</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&lt;/</span><span style="--shiki-dark:#569CD6;--shiki-light:#800000">div</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&gt;</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">      {</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">canLoadComments</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> &amp;&amp;</span><span style="--shiki-dark:#808080;--shiki-light:#800000"> &lt;</span><span style="--shiki-dark:#569CD6;--shiki-light:#800000">button</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#E50000"> onClick</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">=</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">{</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">loadComments</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">Load Comments</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&lt;/</span><span style="--shiki-dark:#569CD6;--shiki-light:#800000">button</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&gt;</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">      {</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">comments</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">map</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">comment</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> =&gt;</span><span style="--shiki-dark:#808080;--shiki-light:#800000"> &lt;</span><span style="--shiki-dark:#569CD6;--shiki-light:#800000">div</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&gt;</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">{</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">comment</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">text</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&lt;/</span><span style="--shiki-dark:#569CD6;--shiki-light:#800000">div</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">)</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span></span>
<span class="line"><span style="--shiki-dark:#808080;--shiki-light:#800000">    &lt;/</span><span style="--shiki-dark:#569CD6;--shiki-light:#800000">div</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&gt;</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  );</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">};</span></span>
<span class="line"></span></code></pre>
<p>Finally, we want to set up communication to the controller. <code>NotebookController.onDidReceiveMessage</code> method is called when a renderer posts a message using the global <code>postKernelMessage</code> function. To implement this method, attach to <code>onDidReceiveMessage</code> to listen for messages:</p>
<pre class="shiki" data-lang="ts" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">class</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99"> Controller</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">  // ...</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">  constructor</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">() {</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">    // ...</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">    this</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">_controller</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">onDidReceiveMessage</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">event</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> =&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">      if</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> (</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">event</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">message</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">command</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> === </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'comments'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">        _getCommentsForIssue</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">event</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">message</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">issueId</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">).</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">then</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">          comments</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> =&gt;</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">            this</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">_controller</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">postMessage</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">({</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">              type:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'comments'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">              issueId:</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> event</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">message</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">issueId</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">              comments</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">            }),</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">          event</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">editor</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">        );</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    });</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<h3 id="interactive-notebooks-communicating-with-the-extension-host" data-needslink="interactive-notebooks-communicating-with-the-extension-host">Interactive Notebooks (communicating with the extension host)</h3>
<p>Imagine we want to add the ability to open the output item within a separate editor. To make this possible, the renderer needs to be able to send a message to the extension host, which will then launch the editor.</p>
<p>This would be useful in scenarios where the renderer and controller are two separate extensions.</p>
<p>In the <code>package.json</code> of the renderer extension specify the value for <code>requiresMessaging</code> as <code>optional</code> which allows your renderer to work in both situations when it has and doesn't have access to the extension host.</p>
<pre class="shiki" data-lang="json" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">{</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "activationEvents"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"...."</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">],</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "contributes"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#F44747;--shiki-light:#CD3131">    ...</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "notebookRenderer"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">        "id"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"output-editor-renderer"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">        "displayName"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"Output Editor Renderer"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">        "entrypoint"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"./out/renderer.js"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">        "mimeTypes"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span><span style="--shiki-dark:#F44747;--shiki-light:#CD3131">...</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">],</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">        "requiresMessaging"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"optional"</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    ]</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<p>The possible values for <code>requiresMessaging</code> include:</p>
<ul><li><code>always</code>  : Messaging is required. The renderer will only be used when it's part of an extension that can be run in an extension host.</li>
<li><code>optional</code>: The renderer is better with messaging when the extension host is available, but it's not required to install and run the renderer.</li>
<li><code>never</code>   : The renderer does not require messaging.</li>
</ul><p>The last two options are preferred, as this ensures the portability of renderer extensions to other contexts where the extension host might not necessarily be available.</p>
<p>The renderer script file can setup communications as follows:</p>
<pre class="shiki" data-lang="js" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">import</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> { </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">ActivationFunction</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> } </span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">from</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'vscode-notebook-renderer'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">export</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> const</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> activate</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">ActivationFunction</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = (</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">context</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">=&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> ({</span></span>
<span class="line"><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">  renderOutputItem</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">data</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">element</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">    // Render the output using the output `data`</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    ....</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">    // The availability of messaging depends on the value in `requiresMessaging`</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">    if</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> (!</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">context</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">postMessage</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">){</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">      return</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    }</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">    // Upon some user action in the output (such as clicking a button),</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">    // send a message to the extension host requesting the launch of the editor.</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    document</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">querySelector</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'#openEditor'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">).</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">addEventListener</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'click'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, () </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">=&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">      context</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">postMessage</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">({</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">        request:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'showEditor'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">        data:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> '&lt;custom data&gt;'</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      })</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    });</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">});</span></span>
<span class="line"></span></code></pre>
<p>And then you can consume that message in the extension host as follows:</p>
<pre class="shiki" data-lang="ts" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> messageChannel</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">notebooks</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">createRendererMessaging</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'output-editor-renderer'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">messageChannel</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">onDidReceiveMessage</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">e</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> =&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">  if</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> (</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">e</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">message</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">request</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> === </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'showEditor'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">    // Launch the editor for the output identified by `e.message.data`</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">});</span></span>
<span class="line"></span></code></pre>
<p>Note:</p>
<ul><li>To ensure your extension is running in the extension host before messages are delivered, add <code>onRenderer:&lt;your renderer id&gt;</code> to your <code>activationEvents</code> and set up communication in your extension's <code>activate</code> function.</li>
<li>Not all messages sent by the renderer extension to the extension host are guaranteed to be delivered. A user could close the notebook before messages from the renderer are delivered.</li>
</ul><h2 id="supporting-debugging" data-needslink="supporting-debugging">Supporting debugging</h2>
<p>For some controllers, such as those that implement a programming language, it can be desirable to allow debugging a cell's execution. To add debugging support, a notebook kernel can implement a <a href="/api/extension-guides/debugger-extension">debug adapter</a>, either by directly implementing the <a href="https://microsoft.github.io/debug-adapter-protocol/" class="external-link" target="_blank">debug adapter protocol</a> (DAP), or by delegating and transforming the protocol to an existing notebook debugger (as done in the 'vscode-simple-jupyter-notebook' sample). A much simpler approach is to use an existing unmodified debug extension and transform the DAP for notebook needs on the fly (as done in 'vscode-nodebook').</p>
<p>Samples:</p>
<ul><li><a href="https://github.com/microsoft/vscode-nodebook" class="external-link" target="_blank">vscode-nodebook</a>: Node.js notebook with debugging support provided by VS Code's built-in JavaScript debugger and some simple protocol transformations</li>
<li><a href="https://github.com/microsoft/vscode-simple-jupyter-notebook" class="external-link" target="_blank">vscode-simple-jupyter-notebook</a>: Jupyter notebook with debugging support provided by the existing Xeus debugger</li>
</ul><div class="feedback" data-edit-url="https://vscode.dev/github/microsoft/vscode-docs/blob/main/api/extension-guides/notebook.md"></div>
				
				<div class="body-footer">6/3/2026</div>
				
            </main><aside class="docs-right-sidebar hidden-xs"><div class="docs-markdown-actions">
                    <div class="docs-markdown-dropdown" data-raw-url="/raw/api/extension-guides/notebook.md">
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
                <nav id="docs-subnavbar" aria-label="On Page"><h4><span class="sr-only">On this page there are 6 sections</span><span aria-hidden="true">On this page</span></h4>
                    <ul class="nav"><li><a href="#parts-of-a-notebook">Parts of a Notebook</a></li>
                        
                        <li><a href="#serializer">Serializer</a></li>
                        
                        <li><a href="#controller">Controller</a></li>
                        
                        <li><a href="#output-types">Output types</a></li>
                        
                        <li><a href="#notebook-renderer">Notebook Renderer</a></li>
                        
                        <li><a href="#supporting-debugging">Supporting debugging</a></li>
                        
                    </ul></nav></aside></div>
		<div class="docs-mobile-widgets visible-xs">
			<div class="connect-widget"></div>
		</div>
	</div>
</div>
		</main>