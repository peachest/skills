# Commands

> 源文档: [https://code.visualstudio.com/api/extension-guides/command](https://code.visualstudio.com/api/extension-guides/command)

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
			        
			        <li class="active">
			          <a href="/api/extension-guides/command" aria-label="Current Page: Command">Command</a>
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
				<select id="small-nav-dropdown" aria-label="topics"><option value="/api">Overview</option><optgroup label="Get Started"><option value="/api/get-started/your-first-extension">Your First Extension</option><option value="/api/get-started/extension-anatomy">Extension Anatomy</option><option value="/api/get-started/wrapping-up">Wrapping Up</option></optgroup><optgroup label="Extension Capabilities"><option value="/api/extension-capabilities/overview">Overview</option><option value="/api/extension-capabilities/common-capabilities">Common Capabilities</option><option value="/api/extension-capabilities/theming">Theming</option><option value="/api/extension-capabilities/extending-workbench">Extending Workbench</option></optgroup><optgroup label="Extension Guides"><option value="/api/extension-guides/overview">Overview</option><optgroup label="Extension Guides - AI"><option value="/api/extension-guides/ai/ai-extensibility-overview">AI Extensibility</option><option value="/api/extension-guides/ai/tools">Language Model Tool</option><option value="/api/extension-guides/ai/mcp">MCP Dev Guide</option><option value="/api/extension-guides/ai/chat">Chat Participant</option><option value="/api/extension-guides/ai/chat-tutorial">Chat Tutorial</option><option value="/api/extension-guides/ai/language-model">Language Model</option><option value="/api/extension-guides/ai/language-model-tutorial">Language Model Tutorial</option><option value="/api/extension-guides/ai/language-model-chat-provider">Language Model Chat Provider</option><option value="/api/extension-guides/ai/prompt-tsx">Prompt TSX</option></optgroup><option value="/api/extension-guides/command" selected>Command</option><option value="/api/extension-guides/color-theme">Color Theme</option><option value="/api/extension-guides/file-icon-theme">File Icon Theme</option><option value="/api/extension-guides/product-icon-theme">Product Icon Theme</option><option value="/api/extension-guides/tree-view">Tree View</option><option value="/api/extension-guides/webview">Webview</option><option value="/api/extension-guides/notebook">Notebook</option><option value="/api/extension-guides/custom-editors">Custom Editors</option><option value="/api/extension-guides/virtual-documents">Virtual Documents</option><option value="/api/extension-guides/virtual-workspaces">Virtual Workspaces</option><option value="/api/extension-guides/web-extensions">Web Extensions</option><option value="/api/extension-guides/workspace-trust">Workspace Trust</option><option value="/api/extension-guides/task-provider">Task Provider</option><option value="/api/extension-guides/scm-provider">Source Control</option><option value="/api/extension-guides/debugger-extension">Debugger Extension</option><option value="/api/extension-guides/markdown-extension">Markdown Extension</option><option value="/api/extension-guides/testing">Test Extension</option><option value="/api/extension-guides/custom-data-extension">Custom Data Extension</option><option value="/api/extension-guides/telemetry">Telemetry</option></optgroup><optgroup label="UX Guidelines"><option value="/api/ux-guidelines/overview">Overview</option><option value="/api/ux-guidelines/activity-bar">Activity Bar</option><option value="/api/ux-guidelines/sidebars">Sidebars</option><option value="/api/ux-guidelines/panel">Panel</option><option value="/api/ux-guidelines/status-bar">Status Bar</option><option value="/api/ux-guidelines/views">Views</option><option value="/api/ux-guidelines/editor-actions">Editor Actions</option><option value="/api/ux-guidelines/quick-picks">Quick Picks</option><option value="/api/ux-guidelines/command-palette">Command Palette</option><option value="/api/ux-guidelines/notifications">Notifications</option><option value="/api/ux-guidelines/webviews">Webviews</option><option value="/api/ux-guidelines/context-menus">Context Menus</option><option value="/api/ux-guidelines/walkthroughs">Walkthroughs</option><option value="/api/ux-guidelines/settings">Settings</option></optgroup><optgroup label="Language Extensions"><option value="/api/language-extensions/overview">Overview</option><option value="/api/language-extensions/syntax-highlight-guide">Syntax Highlight Guide</option><option value="/api/language-extensions/semantic-highlight-guide">Semantic Highlight Guide</option><option value="/api/language-extensions/snippet-guide">Snippet Guide</option><option value="/api/language-extensions/language-configuration-guide">Language Configuration Guide</option><option value="/api/language-extensions/programmatic-language-features">Programmatic Language Features</option><option value="/api/language-extensions/language-server-extension-guide">Language Server Extension Guide</option><option value="/api/language-extensions/embedded-languages">Embedded Languages</option></optgroup><optgroup label="Testing and Publishing"><option value="/api/working-with-extensions/testing-extension">Testing Extensions</option><option value="/api/working-with-extensions/publishing-extension">Publishing Extensions</option><option value="/api/working-with-extensions/bundling-extension">Bundling Extensions</option><option value="/api/working-with-extensions/continuous-integration">Continuous Integration</option></optgroup><optgroup label="Advanced Topics"><option value="/api/advanced-topics/extension-host">Extension Host</option><option value="/api/advanced-topics/remote-extensions">Remote Development and Codespaces</option><option value="/api/advanced-topics/using-proposed-api">Using Proposed API</option><option value="/api/advanced-topics/tslint-eslint-migration">Migrate from TSLint to ESLint</option><option value="/api/advanced-topics/python-extension-template">Python Extension Template</option></optgroup><optgroup label="References"><option value="/api/references/vscode-api">VS Code API</option><option value="/api/references/contribution-points">Contribution Points</option><option value="/api/references/activation-events">Activation Events</option><option value="/api/references/extension-manifest">Extension Manifest</option><option value="/api/references/commands">Built-In Commands</option><option value="/api/references/when-clause-contexts">When Clause Contexts</option><option value="/api/references/theme-color">Theme Color</option><option value="/api/references/icons-in-labels">Product Icon Reference</option><option value="/api/references/document-selector">Document Selector</option></optgroup></select></nav></aside><div class="docs-content-wrapper">
			
			<main class="docs-main-content body"><h1>Commands</h1>
<p>Commands trigger actions in Visual Studio Code. If you have ever <a href="/docs/getstarted/keybindings">configured a keybinding</a>, then you've worked with commands. Commands are also used by extensions to expose functionality to users, bind to actions in VS Code's UI, and implement internal logic.</p>
<h2 id="using-commands" data-needslink="using-commands">Using Commands</h2>
<p>VS Code includes a large set of <a href="/api/references/commands">built-in commands</a> that you can use to interact with the editor, control the user interface, or perform background operations. Many extensions also expose their core functionality as commands that users and other extensions can leverage.</p>
<h3 id="programmatically-executing-a-command" data-needslink="programmatically-executing-a-command">Programmatically executing a command</h3>
<p>The <a href="/api/references/vscode-api#commands.executeCommand"><code>vscode.commands.executeCommand</code></a> API programmatically executes a command. This lets you use VS Code's built-in functionality, and build on extensions such as VS Code's built-in Git and Markdown extensions.</p>
<p>The <code>editor.action.addCommentLine</code> command, for example, comments the currently selected lines in the active text editor:</p>
<pre class="shiki" data-lang="ts" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">import</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> *</span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB"> as</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> vscode</span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB"> from</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'vscode'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">function</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> commentLine</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">() {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">commands</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">executeCommand</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'editor.action.addCommentLine'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<p>Some commands take arguments that control their behavior. Commands may also return a result. The API-like <code>vscode.executeDefinitionProvider</code> command, for example, queries a document for definitions at a given position. It takes a document URI and a position as arguments, and returns a promise with a list of definitions:</p>
<pre class="shiki" data-lang="ts" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">import</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> *</span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB"> as</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> vscode</span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB"> from</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'vscode'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">async</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> function</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> printDefinitionsForActiveEditor</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">() {</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">  const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> activeEditor</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">window</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">activeTextEditor</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">  if</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> (!</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">activeEditor</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">    return</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  }</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">  const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> definitions</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">await</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">commands</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">executeCommand</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">&lt;</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">Location</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">[]&gt;(</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">    'vscode.executeDefinitionProvider'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    activeEditor</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">document</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">uri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    activeEditor</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">selection</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">active</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  );</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">  for</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> (</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> definition</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> of</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> definitions</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    console</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">log</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">definition</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<p>To find available commands:</p>
<ul><li><a href="/docs/getstarted/keybindings">Browse the keyboard shortcuts</a></li>
<li><a href="/api/references/commands">Look through VS Code's built-in advanced commands api</a></li>
</ul><h3 id="command-uris" data-needslink="command-uris">Command URIs</h3>
<p>Commands URIs are links that execute a given command. They can be used as clickable links in hover text, completion item details, or inside of webviews.</p>
<p>A command URI uses the <code>command</code> scheme followed by the command name. The command URI for the <code>editor.action.addCommentLine</code> command, for example, is <code>command:editor.action.addCommentLine</code>. Here's a hover provider that shows a link in the comments of the current line in the active text editor:</p>
<pre class="shiki" data-lang="ts" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">import</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> *</span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB"> as</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> vscode</span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB"> from</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'vscode'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">export</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> function</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> activate</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">context</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">ExtensionContext</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">languages</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">registerHoverProvider</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">    'javascript'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">    new</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> (</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">class</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> implements</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99"> vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">HoverProvider</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">      provideHover</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">        _document</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">TextDocument</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">        _position</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">Position</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">        _token</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">CancellationToken</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      ): </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">ProviderResult</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">&lt;</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">Hover</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">&gt; {</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">        const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> commentCommandUri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">Uri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">parse</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">`command:editor.action.addCommentLine`</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">        const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> contents</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">new</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">MarkdownString</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">`[Add comment](</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">${</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">commentCommandUri</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">)`</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">        // To enable command URIs in Markdown content, you must set the `isTrusted` flag.</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">        // When creating trusted Markdown string, make sure to properly sanitize all the</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">        // input content so that only expected command URIs can be executed</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">        contents</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">isTrusted</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">true</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">        return</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> new</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">Hover</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">contents</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    })()</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  );</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<p>The list of arguments to the command is passed as a JSON array that has been properly URI encoded: The example below uses the <code>git.stage</code> command to create a hover link that stages the current file:</p>
<pre class="shiki" data-lang="ts" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">import</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> *</span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB"> as</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> vscode</span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB"> from</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'vscode'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">export</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> function</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> activate</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">context</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">ExtensionContext</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">languages</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">registerHoverProvider</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">    'javascript'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">    new</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> (</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">class</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> implements</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99"> vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">HoverProvider</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">      provideHover</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">        document</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">TextDocument</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">        _position</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">Position</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">        _token</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">CancellationToken</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      ): </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">ProviderResult</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">&lt;</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">Hover</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">&gt; {</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">        const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> args</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = [{ </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">resourceUri:</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> document</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">uri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> }];</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">        const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> stageCommandUri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">Uri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">parse</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">          `command:git.stage?</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">${</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">encodeURIComponent</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">(</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1">JSON</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">stringify</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">args</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">))</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">`</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">        );</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">        const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> contents</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">new</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">MarkdownString</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">`[Stage file](</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">${</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">stageCommandUri</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">)`</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">        contents</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">isTrusted</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">true</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">        return</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> new</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">Hover</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">contents</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    })()</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  );</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<p>You can enable command URIs in <a href="/api/extension-guides/webview">webviews</a> by setting <code>enableCommandUris</code> in the <code>WebviewOptions</code> when the webview is created.</p>
<h2 id="creating-new-commands" data-needslink="creating-new-commands">Creating new commands</h2>
<h3 id="registering-a-command" data-needslink="registering-a-command">Registering a command</h3>
<p><a href="/api/references/vscode-api#commands.registerCommand"><code>vscode.commands.registerCommand</code></a> binds a command ID to a handler function in your extension:</p>
<pre class="shiki" data-lang="ts" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">import</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> *</span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB"> as</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> vscode</span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB"> from</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'vscode'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">export</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> function</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> activate</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">context</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">ExtensionContext</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">  const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> command</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'myExtension.sayHello'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">  const</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> commandHandler</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = (</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">name</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">string</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'world'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">=&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    console</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">log</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">`Hello </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">${</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">name</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">!!!`</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  };</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  context</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">subscriptions</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">push</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">commands</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">registerCommand</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">command</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">commandHandler</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">));</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<p>The handler function will be invoked whenever the <code>myExtension.sayHello</code> command is executed, be it programmatically with <code>executeCommand</code>, from the VS Code UI, or through a keybinding.</p>
<h3 id="creating-a-user-facing-command" data-needslink="creating-a-user-facing-command">Creating a user facing command</h3>
<p><code>vscode.commands.registerCommand</code> only binds a command ID to a handler function. To expose this command in the Command Palette so it is discoverable by users, you also need a corresponding command <code>contribution</code> in your extension's <code>package.json</code>:</p>
<pre class="shiki" data-lang="json" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">{</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "contributes"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "commands"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">        "command"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"myExtension.sayHello"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">        "title"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"Say Hello"</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    ]</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<p>The <code>commands</code> contribution tells VS Code that your extension provides a given command and should be activated when that command is invoked, and also lets you control how the command is displayed in the UI. Make sure to follow the <a href="#_naming-conventions">command naming conventions</a> when creating commands.</p>
<p><img src="/assets/api/extension-guides/commands/palette.png" alt="The contributed command in the Command Palette" loading="lazy"></p>
<p>Now when a user first invokes the <code>myExtension.sayHello</code> command from the Command Palette or through a keybinding, the extension will be activated and <code>registerCommand</code> will bind <code>myExtension.sayHello</code> to the proper handler.</p>
<blockquote><p><strong>Note</strong>: Extensions targeting VS Code versions prior to 1.74.0 must explicitly register an <code>onCommand</code> <code>activationEvent</code> for all user facing commands so that the extension activates and <code>registerCommand</code> executes:</p>
<pre class="shiki" data-lang="json" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">{</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "activationEvents"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"onCommand:myExtension.sayHello"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">]</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
</blockquote><p>You do not need an <code>onCommand</code> activation event for internal commands but you must define them for any commands that:</p>
<ul><li>Can be invoked using the Command Palette.</li>
<li>Can be invoked using a keybinding.</li>
<li>Can be invoked through the VS Code UI, such as through the editor title bar.</li>
<li>Is intended as an API for other extensions to consume.</li>
</ul><h3 id="controlling-when-a-command-shows-up-in-the-command-palette" data-needslink="controlling-when-a-command-shows-up-in-the-command-palette">Controlling when a command shows up in the Command Palette</h3>
<p>By default, all user facing commands contributed through the <code>commands</code> section of the <code>package.json</code> show up in the Command Palette. However, many commands are only relevant in certain circumstances, such as when there is an active text editor of a given language or when the user has a certain configuration option set.</p>
<p>The <a href="/api/references/contribution-points#contributes.menus"><code>menus.commandPalette</code></a> contribution point lets you restrict when a command should show in the Command Palette. It takes the ID of the target command and a <a href="/api/references/when-clause-contexts">when clause</a> that controls when the command is shown:</p>
<pre class="shiki" data-lang="json" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">{</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "contributes"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "menus"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">      "commandPalette"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">        {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">          "command"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"myExtension.sayHello"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">          "when"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"editorLangId == markdown"</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">        }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      ]</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<p>Now the <code>myExtension.sayHello</code> command will only show up in the Command Palette when the user is in a Markdown file.</p>
<h3 id="enablement-of-commands" data-needslink="enablement-of-commands">Enablement of commands</h3>
<p>Commands support enablement via an <code>enablement</code> property - its value is a <a href="/api/references/when-clause-contexts">when-clause</a>. Enablement applies to all menus and to registered keybindings.</p>
<blockquote><p><strong>Note</strong>: There is semantic overlap between <code>enablement</code> and the <code>when</code> condition of menu items. The latter is used to prevent menus full of disabled items. For example, a command that analyzes a JavaScript regular expression should show <strong>when</strong> the file is JavaScript and be <strong>enabled</strong> only when the cursor is over a regular expression. The <code>when</code> clause prevents clutter, by not showing the command for all other language files. Preventing cluttered menus is highly recommended.</p>
</blockquote><p>Last, menus showing commands, like the Command Palette or context menus, implement different ways of dealing with enablement. Editor and explorer context menus render enablement/disablement items while the Command Palette filters them.</p>
<h3 id="using-a-custom-when-clause-context" data-needslink="using-a-custom-when-clause-context">Using a custom when clause context</h3>
<p>If you are authoring your own VS Code extension and need to enable/disable commands, menus, or views by using a <code>when</code> clause context and none of the existing keys suit your needs, then you can add your own context.</p>
<p>The first example below sets the key <code>myExtension.showMyCommand</code> to true, which you can use in enablement of commands or with the <code>when</code> property. The second example stores a value that you could use with a <code>when</code> clause to check if the number of cool open things is greater than 2.</p>
<pre class="shiki" data-lang="js" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">commands</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">executeCommand</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'setContext'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'myExtension.showMyCommand'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">true</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">commands</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">executeCommand</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'setContext'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'myExtension.numberOfCoolOpenThings'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#B5CEA8;--shiki-light:#098658">2</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"></span></code></pre>
<h2 id="naming-conventions" data-needslink="naming-conventions">Naming conventions</h2>
<p>When creating commands, you should follow these naming conventions:</p>
<ul><li>Command title
<ul><li>Use title-style capitalization. Don't capitalize prepositions of four or fewer letters (such as on, to, in, of, with, and for) unless the preposition is the first or last word.</li>
<li>Start with a verb to describe the action that will be performed.</li>
<li>Use a noun to describe the target of the action.</li>
<li>Avoid using "command" in the title.</li>
</ul></li>
</ul><div class="feedback" data-edit-url="https://vscode.dev/github/microsoft/vscode-docs/blob/main/api/extension-guides/command.md"></div>
				
				<div class="body-footer">6/3/2026</div>
				
            </main><aside class="docs-right-sidebar hidden-xs"><div class="docs-markdown-actions">
                    <div class="docs-markdown-dropdown" data-raw-url="/raw/api/extension-guides/command.md">
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
                <nav id="docs-subnavbar" aria-label="On Page"><h4><span class="sr-only">On this page there are 3 sections</span><span aria-hidden="true">On this page</span></h4>
                    <ul class="nav"><li><a href="#using-commands">Using Commands</a></li>
                        
                        <li><a href="#creating-new-commands">Creating new commands</a></li>
                        
                        <li><a href="#naming-conventions">Naming conventions</a></li>
                        
                    </ul></nav></aside></div>
		<div class="docs-mobile-widgets visible-xs">
			<div class="connect-widget"></div>
		</div>
	</div>
</div>
		</main>