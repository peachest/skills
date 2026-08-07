# Language Configuration Guide

> 源文档: [https://code.visualstudio.com/api/language-extensions/language-configuration-guide](https://code.visualstudio.com/api/language-extensions/language-configuration-guide)

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
			          
			        <li class="active">
			          <a href="/api/language-extensions/language-configuration-guide" aria-label="Current Page: Language Configuration Guide">Language Configuration Guide</a>
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
				<select id="small-nav-dropdown" aria-label="topics"><option value="/api">Overview</option><optgroup label="Get Started"><option value="/api/get-started/your-first-extension">Your First Extension</option><option value="/api/get-started/extension-anatomy">Extension Anatomy</option><option value="/api/get-started/wrapping-up">Wrapping Up</option></optgroup><optgroup label="Extension Capabilities"><option value="/api/extension-capabilities/overview">Overview</option><option value="/api/extension-capabilities/common-capabilities">Common Capabilities</option><option value="/api/extension-capabilities/theming">Theming</option><option value="/api/extension-capabilities/extending-workbench">Extending Workbench</option></optgroup><optgroup label="Extension Guides"><option value="/api/extension-guides/overview">Overview</option><optgroup label="Extension Guides - AI"><option value="/api/extension-guides/ai/ai-extensibility-overview">AI Extensibility</option><option value="/api/extension-guides/ai/tools">Language Model Tool</option><option value="/api/extension-guides/ai/mcp">MCP Dev Guide</option><option value="/api/extension-guides/ai/chat">Chat Participant</option><option value="/api/extension-guides/ai/chat-tutorial">Chat Tutorial</option><option value="/api/extension-guides/ai/language-model">Language Model</option><option value="/api/extension-guides/ai/language-model-tutorial">Language Model Tutorial</option><option value="/api/extension-guides/ai/language-model-chat-provider">Language Model Chat Provider</option><option value="/api/extension-guides/ai/prompt-tsx">Prompt TSX</option></optgroup><option value="/api/extension-guides/command">Command</option><option value="/api/extension-guides/color-theme">Color Theme</option><option value="/api/extension-guides/file-icon-theme">File Icon Theme</option><option value="/api/extension-guides/product-icon-theme">Product Icon Theme</option><option value="/api/extension-guides/tree-view">Tree View</option><option value="/api/extension-guides/webview">Webview</option><option value="/api/extension-guides/notebook">Notebook</option><option value="/api/extension-guides/custom-editors">Custom Editors</option><option value="/api/extension-guides/virtual-documents">Virtual Documents</option><option value="/api/extension-guides/virtual-workspaces">Virtual Workspaces</option><option value="/api/extension-guides/web-extensions">Web Extensions</option><option value="/api/extension-guides/workspace-trust">Workspace Trust</option><option value="/api/extension-guides/task-provider">Task Provider</option><option value="/api/extension-guides/scm-provider">Source Control</option><option value="/api/extension-guides/debugger-extension">Debugger Extension</option><option value="/api/extension-guides/markdown-extension">Markdown Extension</option><option value="/api/extension-guides/testing">Test Extension</option><option value="/api/extension-guides/custom-data-extension">Custom Data Extension</option><option value="/api/extension-guides/telemetry">Telemetry</option></optgroup><optgroup label="UX Guidelines"><option value="/api/ux-guidelines/overview">Overview</option><option value="/api/ux-guidelines/activity-bar">Activity Bar</option><option value="/api/ux-guidelines/sidebars">Sidebars</option><option value="/api/ux-guidelines/panel">Panel</option><option value="/api/ux-guidelines/status-bar">Status Bar</option><option value="/api/ux-guidelines/views">Views</option><option value="/api/ux-guidelines/editor-actions">Editor Actions</option><option value="/api/ux-guidelines/quick-picks">Quick Picks</option><option value="/api/ux-guidelines/command-palette">Command Palette</option><option value="/api/ux-guidelines/notifications">Notifications</option><option value="/api/ux-guidelines/webviews">Webviews</option><option value="/api/ux-guidelines/context-menus">Context Menus</option><option value="/api/ux-guidelines/walkthroughs">Walkthroughs</option><option value="/api/ux-guidelines/settings">Settings</option></optgroup><optgroup label="Language Extensions"><option value="/api/language-extensions/overview">Overview</option><option value="/api/language-extensions/syntax-highlight-guide">Syntax Highlight Guide</option><option value="/api/language-extensions/semantic-highlight-guide">Semantic Highlight Guide</option><option value="/api/language-extensions/snippet-guide">Snippet Guide</option><option value="/api/language-extensions/language-configuration-guide" selected>Language Configuration Guide</option><option value="/api/language-extensions/programmatic-language-features">Programmatic Language Features</option><option value="/api/language-extensions/language-server-extension-guide">Language Server Extension Guide</option><option value="/api/language-extensions/embedded-languages">Embedded Languages</option></optgroup><optgroup label="Testing and Publishing"><option value="/api/working-with-extensions/testing-extension">Testing Extensions</option><option value="/api/working-with-extensions/publishing-extension">Publishing Extensions</option><option value="/api/working-with-extensions/bundling-extension">Bundling Extensions</option><option value="/api/working-with-extensions/continuous-integration">Continuous Integration</option></optgroup><optgroup label="Advanced Topics"><option value="/api/advanced-topics/extension-host">Extension Host</option><option value="/api/advanced-topics/remote-extensions">Remote Development and Codespaces</option><option value="/api/advanced-topics/using-proposed-api">Using Proposed API</option><option value="/api/advanced-topics/tslint-eslint-migration">Migrate from TSLint to ESLint</option><option value="/api/advanced-topics/python-extension-template">Python Extension Template</option></optgroup><optgroup label="References"><option value="/api/references/vscode-api">VS Code API</option><option value="/api/references/contribution-points">Contribution Points</option><option value="/api/references/activation-events">Activation Events</option><option value="/api/references/extension-manifest">Extension Manifest</option><option value="/api/references/commands">Built-In Commands</option><option value="/api/references/when-clause-contexts">When Clause Contexts</option><option value="/api/references/theme-color">Theme Color</option><option value="/api/references/icons-in-labels">Product Icon Reference</option><option value="/api/references/document-selector">Document Selector</option></optgroup></select></nav></aside><div class="docs-content-wrapper">
			
			<main class="docs-main-content body"><h1>Language Configuration Guide</h1>
<p>The <a href="/api/references/contribution-points#contributes.languages"><code>contributes.languages</code></a> Contribution Point allows you to define a language configuration that controls the following Declarative Language Features:</p>
<ul><li>Comment toggling</li>
<li>Brackets definition</li>
<li>Autoclosing</li>
<li>Autosurrounding</li>
<li>Folding</li>
<li>Word pattern</li>
<li>Indentation Rules</li>
</ul><p>Here is a <a href="https://github.com/microsoft/vscode-extension-samples/tree/main/language-configuration-sample" class="external-link" target="_blank">Language Configuration sample</a> that configures the editing experience for JavaScript files. This guide explains the content of <code>language-configuration.json</code>:</p>
<p><strong>Note: If your language configuration file name is or ends with <code>language-configuration.json</code>, you will get autocompletion and validation in VS Code.</strong></p>
<pre class="shiki" data-lang="json" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">{</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "comments"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "lineComment"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"//"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "blockComment"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"/*"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"*/"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">]</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  },</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "brackets"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    [</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"{"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"}"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">],</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    [</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"["</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"]"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">],</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    [</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"("</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">")"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">]</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  ],</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "autoClosingPairs"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    { </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">"open"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"{"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">"close"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"}"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> },</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    { </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">"open"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"["</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">"close"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"]"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> },</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    { </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">"open"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"("</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">"close"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">")"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> },</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    { </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">"open"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"'"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">"close"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"'"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">"notIn"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"string"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"comment"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">] },</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    { </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">"open"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\"</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">"close"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\"</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">"notIn"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"string"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">] },</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    { </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">"open"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"`"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">"close"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"`"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">"notIn"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"string"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"comment"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">] },</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    { </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">"open"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"/**"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">"close"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">" */"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">"notIn"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"string"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">] }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  ],</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "autoCloseBefore"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">";:.,=}])&gt;` </span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\n\t</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "surroundingPairs"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    [</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"{"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"}"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">],</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    [</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"["</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"]"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">],</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    [</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"("</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">")"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">],</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    [</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"'"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"'"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">],</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    [</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\"</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\"</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">],</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    [</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"`"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"`"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">]</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  ],</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "folding"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "markers"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">      "start"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"^</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">s*//</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">s*#?region</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">b"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">      "end"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"^</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">s*//</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">s*#?endregion</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">b"</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  },</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "wordPattern"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"(-?</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">d*</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">.</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">d</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">w*)|([^</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">`</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">~</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">!</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">@</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">#</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">%</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">^</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">&amp;</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">*</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">(</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">)</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">-</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">=</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">+</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">[</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">{</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">]</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">}</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\\\\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">|</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">;</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">:</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\\"\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">,</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">.</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">&lt;</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">&gt;</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">/</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">?</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">s]+)"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "indentationRules"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "increaseIndentPattern"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"^((?!</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">/</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">/).)*(</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">{[^}</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\"</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'`]*|</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">([^)</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\"</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'`]*|</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">[[^</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">]</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\"</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'`]*)$"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "decreaseIndentPattern"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"^((?!.*?</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">/</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">*).*</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">*/)?</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">s*[</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">)</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">}</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">]].*$"</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<h2 id="comment-toggling" data-needslink="comment-toggling">Comment toggling</h2>
<p>VS Code offers two commands for comment toggling. <strong>Toggle Line Comment</strong> and <strong>Toggle Block Comment</strong>. You can specify <code>comments.blockComment</code> and <code>comments.lineComment</code> to control how VS Code should comment out lines / blocks.</p>
<pre class="shiki" data-lang="json" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">{</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "comments"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "lineComment"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"//"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "blockComment"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"/*"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"*/"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">]</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<p>The <code>lineComment</code> property supports two formats for backwards compatibility:</p>
<ul><li>A string value for simple line comment definitions.</li>
<li>An object value that enables configuring the indentation behavior of comment lines.</li>
</ul><pre class="shiki" data-lang="json" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">{</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "comments"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "lineComment"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">      "comment"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"//"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">      "noIndent"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">true</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    },</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "blockComment"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"/*"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"*/"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">]</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<h2 id="brackets-definition" data-needslink="brackets-definition">Brackets definition</h2>
<p>When you move the cursor to a bracket defined here, VS Code will highlight that bracket together with its matching pair.</p>
<pre class="shiki" data-lang="json" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">{</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "brackets"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    [</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"{"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"}"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">],</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    [</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"["</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"]"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">],</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    [</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"("</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">")"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">]</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  ]</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<p>Moreover, when you run <strong>Go to Bracket</strong> or <strong>Select to Bracket</strong>, VS Code will use the definition above to find the nearest bracket and its matching pair.</p>
<h2 id="autoclosing" data-needslink="autoclosing">Autoclosing</h2>
<p>When you type <code>'</code>, VS Code creates a pair of single quotes and puts your cursor in the middle: <code>'|'</code>. This section defines such pairs.</p>
<pre class="shiki" data-lang="json" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">{</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "autoClosingPairs"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    { </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">"open"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"{"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">"close"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"}"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> },</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    { </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">"open"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"["</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">"close"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"]"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> },</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    { </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">"open"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"("</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">"close"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">")"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> },</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    { </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">"open"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"'"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">"close"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"'"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">"notIn"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"string"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"comment"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">] },</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    { </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">"open"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\"</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">"close"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\"</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">"notIn"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"string"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">] },</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    { </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">"open"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"`"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">"close"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"`"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">"notIn"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"string"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"comment"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">] },</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    { </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">"open"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"/**"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">"close"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">" */"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">"notIn"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"string"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">] }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  ]</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<p>The <code>notIn</code> key disables this feature in certain code ranges. For example, when you are writing the following code:</p>
<pre class="shiki" data-lang="js" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">// ES6's Template String</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">`ES6's Template String`</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"></span></code></pre>
<p>The single quote will not be autoclosed.</p>
<p>Pairs that do not require a <code>notIn</code> property can also use a simpler syntax:</p>
<pre class="shiki" data-lang="json" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">{</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "autoClosingPairs"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    [</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"{"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"}"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">],</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    [</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"["</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"]"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">]</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  ]</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<p>Users can tweak the autoclosing behavior with the <code>editor.autoClosingQuotes</code> and <code>editor.autoClosingBrackets</code> settings.</p>
<h3 id="autoclosing-before" data-needslink="autoclosing-before">Autoclosing before</h3>
<p>By default, VS Code only autocloses pairs if there is whitespace right after the cursor. So when you type <code>{</code> in the following JSX code, you would not get autoclose:</p>
<pre class="shiki" data-lang="js" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">const</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> Component</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = () </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">=&gt;</span></span>
<span class="line"><span style="--shiki-dark:#808080;--shiki-light:#800000">  &lt;</span><span style="--shiki-dark:#569CD6;--shiki-light:#800000">div</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#E50000"> className</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">=</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">{</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">&gt;</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">                  ^</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> Does</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> not</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> get</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> autoclosed</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> by</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> default</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  &lt;/</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">div</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">&gt;</span></span>
<span class="line"></span></code></pre>
<p>However, this definition overrides that behavior:</p>
<pre class="shiki" data-lang="json" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">{</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "autoCloseBefore"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">";:.,=}])&gt;` </span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\n\t</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<p>Now when you enter <code>{</code> right before <code>&gt;</code>, VS Code autocloses it with <code>}</code>.</p>
<h2 id="autosurrounding" data-needslink="autosurrounding">Autosurrounding</h2>
<p>When you select a range in VS Code and enter an opening bracket, VS Code surrounds the selected content with a pair of brackets. This feature is called Autosurrounding, and here you can define the autosurrounding pairs for a specific language:</p>
<pre class="shiki" data-lang="json" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">{</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "surroundingPairs"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    [</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"{"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"}"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">],</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    [</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"["</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"]"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">],</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    [</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"("</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">")"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">],</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    [</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"'"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"'"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">],</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    [</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\"</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\"</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">],</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    [</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"`"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"`"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">]</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  ]</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<p>Users can tweak the autosurrounding behavior with the <code>editor.autoSurround</code> setting.</p>
<h2 id="folding" data-needslink="folding">Folding</h2>
<p>In VS Code, folding is defined either indentation-based, or defined by contributed folding range providers:</p>
<ul><li>Indentation-based folding with markers: If no folding range provider is available for the given language or if the user has set <code>editor.foldingStrategy</code> to <code>indentation</code>, indentation-based folding is used. A folding region starts when a line has a smaller indent than one or more following lines, and ends when there is a line with the same or smaller indent. Empty lines are ignored.
Additionally, the language configuration can define start and end markers. These are defined as <code>start</code> and <code>end</code> regexes in <code>folding.markers</code>. When matching lines are found, a folding range inside the pair is created. Folding markers must be non-empty and typically look like <code>//#region</code> and <code>//#endregion</code>.</li>
</ul><p>The following JSON creates folding markers for <code>//#region</code> and <code>//#endregion</code>.</p>
<pre class="shiki" data-lang="json" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">{</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "folding"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "markers"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">      "start"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"^</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">s*//</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">s*#?region</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">b"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">      "end"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"^</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">s*//</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">s*#?endregion</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">b"</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<ul><li>Language server folding: The Language Server responds to the <a href="https://microsoft.github.io/language-server-protocol/specification#textDocument_foldingRange" class="external-link" target="_blank"><code>textDocument/foldingRange</code></a> request with a list of folding ranges, and VS Code would render the ranges as folding markers. Learn more about the folding support in Language Server Protocol at the <a href="/api/language-extensions/programmatic-language-features">Programmatic Language Feature</a> topic.</li>
</ul><h2 id="word-pattern" data-needslink="word-pattern">Word Pattern</h2>
<p><code>wordPattern</code> defines what's considered as a word in the programming language. Code suggestion features will use this setting to determine word boundaries if <code>wordPattern</code> is set. Note this setting won't affect word-related editor commands, which are controlled by the editor setting <code>editor.wordSeparators</code>.</p>
<pre class="shiki" data-lang="json" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">{</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "wordPattern"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"(-?</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">d*</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">.</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">d</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">w*)|([^</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">`</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">~</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">!</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">@</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">#</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">%</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">^</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">&amp;</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">*</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">(</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">)</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">-</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">=</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">+</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">[</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">{</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">]</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">}</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\\\\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">|</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">;</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">:</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\\"\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">,</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">.</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">&lt;</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">&gt;</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">/</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">?</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">s]+)"</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<h2 id="indentation-rules" data-needslink="indentation-rules">Indentation Rules</h2>
<p><code>indentationRules</code> defines how the editor should adjust the indentation of current line or next line when you type, paste, and move lines.</p>
<pre class="shiki" data-lang="json" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">{</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "indentationRules"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "increaseIndentPattern"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"^((?!</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">/</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">/).)*(</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">{[^}</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\"</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'`]*|</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">([^)</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\"</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'`]*|</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">[[^</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">]</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\"</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'`]*)$"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "decreaseIndentPattern"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"^((?!.*?</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">/</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">*).*</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">*/)?</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">s*[</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">)</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">}</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">]].*$"</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<p>For example, <code>if (true) {</code> matches <code>increaseIndentPattern</code>, then if you press <span class="keybinding">Enter</span> after the open bracket <code>{</code>, the editor will automatically indent once, and your code will end up as:</p>
<pre class="shiki" data-lang="javascript" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">if</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> (</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">true</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  console</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">log</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">();</span></span>
<span class="line"></span></code></pre>
<p>In addition to <code>increaseIndentPattern</code> and <code>decreaseIndentPattern</code>, there are two other indentation rules:</p>
<ul><li><code>indentNextLinePattern</code> - If a line matches this pattern, then <strong>only the next line</strong> after it should be indented once.</li>
<li><code>unIndentedLinePattern</code> - If a line matches this pattern, then its indentation should not be changed and it should not be evaluated against the other rules.</li>
</ul><p>If there is no indentation rule set for the programming language, the editor will indent when the line ends with an open bracket and outdent when you type a closing bracket. The bracket here is defined by <code>brackets</code>.</p>
<p>Notice that <code>editor.formatOnPaste</code> setting is controlled by the <a href="/api/references/vscode-api#DocumentRangeFormattingEditProvider"><code>DocumentRangeFormattingEditProvider</code></a> and not affected by auto indentation.</p>
<h2 id="on-enter-rules" data-needslink="on-enter-rules">On Enter Rules</h2>
<p><code>onEnterRules</code> defines a list of rules that will be evaluated when <span class="keybinding">Enter</span> is pressed in the editor.</p>
<pre class="shiki" data-lang="json" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">{</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "onEnterRules"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">      "beforeText"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"^</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">s*(?:def|class|for|if|elif|else|while|try|with|finally|except|async).*?:</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">s*$"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">      "action"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: { </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">"indent"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"indent"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  ]</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<p>When pressing <span class="keybinding">Enter</span>, the text before, after, or one line above the cursor is checked against the following properties:</p>
<ul><li><code>beforeText</code> (mandatory). A regular expression that matches the text before the cursor (limited to the current line).</li>
<li><code>afterText</code>. A regular expression that matches the text after the cursor (limited to the current line).</li>
<li><code>previousLineText</code>. A regular expression that matches the text one line above the cursor.</li>
</ul><p>If all the specified properties match, the rule is considered to match and no further <code>onEnterRules</code> will be evaluated. An <code>onEnterRule</code> can specify the following actions:</p>
<ul><li><code>indent</code> (mandatory). One of <code>none, indent, outdent, indentOutdent</code>.
<ul><li><code>none</code> means that the new line will inherit the indentation of the current line.</li>
<li><code>indent</code> means that the new line will be indented relative to the current line.</li>
<li><code>outdent</code> means that the new line will be unindented relative to the current line.</li>
<li><code>indentOutdent</code> means that two new lines will be inserted, one indented and the second one outdented.</li>
</ul></li>
<li><code>appendText</code>. A string that will be appended after the new line and after the indentation.</li>
<li><code>removeText</code>. The number of characters to remove from the new line's indentation.</li>
</ul><div class="feedback" data-edit-url="https://vscode.dev/github/microsoft/vscode-docs/blob/main/api/language-extensions/language-configuration-guide.md"></div>
				
				<div class="body-footer">6/3/2026</div>
				
            </main><aside class="docs-right-sidebar hidden-xs"><div class="docs-markdown-actions">
                    <div class="docs-markdown-dropdown" data-raw-url="/raw/api/language-extensions/language-configuration-guide.md">
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
                <nav id="docs-subnavbar" aria-label="On Page"><h4><span class="sr-only">On this page there are 8 sections</span><span aria-hidden="true">On this page</span></h4>
                    <ul class="nav"><li><a href="#comment-toggling">Comment toggling</a></li>
                        
                        <li><a href="#brackets-definition">Brackets definition</a></li>
                        
                        <li><a href="#autoclosing">Autoclosing</a></li>
                        
                        <li><a href="#autosurrounding">Autosurrounding</a></li>
                        
                        <li><a href="#folding">Folding</a></li>
                        
                        <li><a href="#word-pattern">Word Pattern</a></li>
                        
                        <li><a href="#indentation-rules">Indentation Rules</a></li>
                        
                        <li><a href="#on-enter-rules">On Enter Rules</a></li>
                        
                    </ul></nav></aside></div>
		<div class="docs-mobile-widgets visible-xs">
			<div class="connect-widget"></div>
		</div>
	</div>
</div>
		</main>