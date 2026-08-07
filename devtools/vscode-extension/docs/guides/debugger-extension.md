# Debugger Extension

> 源文档: [https://code.visualstudio.com/api/extension-guides/debugger-extension](https://code.visualstudio.com/api/extension-guides/debugger-extension)

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
			          
			        <li class="active">
			          <a href="/api/extension-guides/debugger-extension" aria-label="Current Page: Debugger Extension">Debugger Extension</a>
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
				<select id="small-nav-dropdown" aria-label="topics"><option value="/api">Overview</option><optgroup label="Get Started"><option value="/api/get-started/your-first-extension">Your First Extension</option><option value="/api/get-started/extension-anatomy">Extension Anatomy</option><option value="/api/get-started/wrapping-up">Wrapping Up</option></optgroup><optgroup label="Extension Capabilities"><option value="/api/extension-capabilities/overview">Overview</option><option value="/api/extension-capabilities/common-capabilities">Common Capabilities</option><option value="/api/extension-capabilities/theming">Theming</option><option value="/api/extension-capabilities/extending-workbench">Extending Workbench</option></optgroup><optgroup label="Extension Guides"><option value="/api/extension-guides/overview">Overview</option><optgroup label="Extension Guides - AI"><option value="/api/extension-guides/ai/ai-extensibility-overview">AI Extensibility</option><option value="/api/extension-guides/ai/tools">Language Model Tool</option><option value="/api/extension-guides/ai/mcp">MCP Dev Guide</option><option value="/api/extension-guides/ai/chat">Chat Participant</option><option value="/api/extension-guides/ai/chat-tutorial">Chat Tutorial</option><option value="/api/extension-guides/ai/language-model">Language Model</option><option value="/api/extension-guides/ai/language-model-tutorial">Language Model Tutorial</option><option value="/api/extension-guides/ai/language-model-chat-provider">Language Model Chat Provider</option><option value="/api/extension-guides/ai/prompt-tsx">Prompt TSX</option></optgroup><option value="/api/extension-guides/command">Command</option><option value="/api/extension-guides/color-theme">Color Theme</option><option value="/api/extension-guides/file-icon-theme">File Icon Theme</option><option value="/api/extension-guides/product-icon-theme">Product Icon Theme</option><option value="/api/extension-guides/tree-view">Tree View</option><option value="/api/extension-guides/webview">Webview</option><option value="/api/extension-guides/notebook">Notebook</option><option value="/api/extension-guides/custom-editors">Custom Editors</option><option value="/api/extension-guides/virtual-documents">Virtual Documents</option><option value="/api/extension-guides/virtual-workspaces">Virtual Workspaces</option><option value="/api/extension-guides/web-extensions">Web Extensions</option><option value="/api/extension-guides/workspace-trust">Workspace Trust</option><option value="/api/extension-guides/task-provider">Task Provider</option><option value="/api/extension-guides/scm-provider">Source Control</option><option value="/api/extension-guides/debugger-extension" selected>Debugger Extension</option><option value="/api/extension-guides/markdown-extension">Markdown Extension</option><option value="/api/extension-guides/testing">Test Extension</option><option value="/api/extension-guides/custom-data-extension">Custom Data Extension</option><option value="/api/extension-guides/telemetry">Telemetry</option></optgroup><optgroup label="UX Guidelines"><option value="/api/ux-guidelines/overview">Overview</option><option value="/api/ux-guidelines/activity-bar">Activity Bar</option><option value="/api/ux-guidelines/sidebars">Sidebars</option><option value="/api/ux-guidelines/panel">Panel</option><option value="/api/ux-guidelines/status-bar">Status Bar</option><option value="/api/ux-guidelines/views">Views</option><option value="/api/ux-guidelines/editor-actions">Editor Actions</option><option value="/api/ux-guidelines/quick-picks">Quick Picks</option><option value="/api/ux-guidelines/command-palette">Command Palette</option><option value="/api/ux-guidelines/notifications">Notifications</option><option value="/api/ux-guidelines/webviews">Webviews</option><option value="/api/ux-guidelines/context-menus">Context Menus</option><option value="/api/ux-guidelines/walkthroughs">Walkthroughs</option><option value="/api/ux-guidelines/settings">Settings</option></optgroup><optgroup label="Language Extensions"><option value="/api/language-extensions/overview">Overview</option><option value="/api/language-extensions/syntax-highlight-guide">Syntax Highlight Guide</option><option value="/api/language-extensions/semantic-highlight-guide">Semantic Highlight Guide</option><option value="/api/language-extensions/snippet-guide">Snippet Guide</option><option value="/api/language-extensions/language-configuration-guide">Language Configuration Guide</option><option value="/api/language-extensions/programmatic-language-features">Programmatic Language Features</option><option value="/api/language-extensions/language-server-extension-guide">Language Server Extension Guide</option><option value="/api/language-extensions/embedded-languages">Embedded Languages</option></optgroup><optgroup label="Testing and Publishing"><option value="/api/working-with-extensions/testing-extension">Testing Extensions</option><option value="/api/working-with-extensions/publishing-extension">Publishing Extensions</option><option value="/api/working-with-extensions/bundling-extension">Bundling Extensions</option><option value="/api/working-with-extensions/continuous-integration">Continuous Integration</option></optgroup><optgroup label="Advanced Topics"><option value="/api/advanced-topics/extension-host">Extension Host</option><option value="/api/advanced-topics/remote-extensions">Remote Development and Codespaces</option><option value="/api/advanced-topics/using-proposed-api">Using Proposed API</option><option value="/api/advanced-topics/tslint-eslint-migration">Migrate from TSLint to ESLint</option><option value="/api/advanced-topics/python-extension-template">Python Extension Template</option></optgroup><optgroup label="References"><option value="/api/references/vscode-api">VS Code API</option><option value="/api/references/contribution-points">Contribution Points</option><option value="/api/references/activation-events">Activation Events</option><option value="/api/references/extension-manifest">Extension Manifest</option><option value="/api/references/commands">Built-In Commands</option><option value="/api/references/when-clause-contexts">When Clause Contexts</option><option value="/api/references/theme-color">Theme Color</option><option value="/api/references/icons-in-labels">Product Icon Reference</option><option value="/api/references/document-selector">Document Selector</option></optgroup></select></nav></aside><div class="docs-content-wrapper">
			
			<main class="docs-main-content body"><h1>Debugger Extension</h1>
<p>Visual Studio Code's debugging architecture allows extension authors to easily integrate existing debuggers into VS Code, while having a common user interface with all of them.</p>
<p>VS Code ships with one built-in debugger extension, the <a href="https://nodejs.org" class="external-link" target="_blank">Node.js</a> debugger extension, which is an excellent showcase for the many debugger features supported by VS Code:</p>
<p><img src="/assets/api/extension-guides/debugger-extension/debug-features.png" alt="VS Code Debug Features" loading="lazy"></p>
<p>This screenshot shows the following debugging features:</p>
<ol><li>Debug configuration management.</li>
<li>Debug actions for starting/stopping and stepping.</li>
<li>Source-, function-, conditional-, inline breakpoints, and log points.</li>
<li>Stack traces, including multi-thread and multi-process support.</li>
<li>Navigating through complex data structures in views and hovers.</li>
<li>Variable values shown in hovers or inlined in the source.</li>
<li>Managing watch expressions.</li>
<li>Debug console for interactive evaluation with autocomplete.</li>
</ol><p>This documentation will help you create a debugger extension which can make any debugger work with VS Code.</p>
<h2 id="debugging-architecture-of-vs-code" data-needslink="debugging-architecture-of-vs-code">Debugging Architecture of VS Code</h2>
<p>VS Code implements a generic (language-agnostic) debugger UI based on an abstract protocol that we've introduced to communicate with debugger backends.
Because debuggers typically do not implement this protocol, some intermediary is needed to "adapt" the debugger to the protocol.
This intermediary is typically a standalone process that communicates with the debugger.</p>
<p><img src="/assets/api/extension-guides/debugger-extension/debug-arch1.png" alt="VS Code Debug Architecture" loading="lazy"></p>
<p>We call this intermediary the <strong>Debug Adapter</strong> (or <strong>DA</strong> for short) and the abstract protocol that is used between the DA and VS Code is the <strong>Debug Adapter Protocol</strong> (<strong>DAP</strong> for short).
Since the Debug Adapter Protocol is independent from VS Code, it has its own <a href="https://microsoft.github.io/debug-adapter-protocol/" class="external-link" target="_blank">web site</a> where you can find an <a href="https://microsoft.github.io/debug-adapter-protocol/overview" class="external-link" target="_blank">introduction and overview</a>, the detailed <a href="https://microsoft.github.io/debug-adapter-protocol/specification" class="external-link" target="_blank">specification</a>, and some lists with <a href="https://microsoft.github.io/debug-adapter-protocol/implementors/adapters/" class="external-link" target="_blank">known implementations and supporting tools</a>.
The history of and motivation behind DAP is explained in this <a href="https://code.visualstudio.com/blogs/2018/08/07/debug-adapter-protocol-website#_why-the-need-for-decoupling-with-protocols">blog post</a>.</p>
<p>Since debug adapters are independent from VS Code and can be used in <a href="https://microsoft.github.io/debug-adapter-protocol/implementors/tools/" class="external-link" target="_blank">other developments tools</a>, they do not match VS Code's extensibility architecture which is based on extensions and contribution points.</p>
<p>For this reason VS Code provides a contribution point, <code>debuggers</code>, where a debug adapter can be contributed under a specific debug type (e.g. <code>node</code> for the Node.js debugger). VS Code launches the registered DA whenever the user starts a debug session of that type.</p>
<p>So in its most minimal form, a debugger extension is just a declarative contribution of a debug adapter implementation and the extension is basically a packaging container for the debug adapter without any additional code.</p>
<p><img src="/assets/api/extension-guides/debugger-extension/debug-arch2.png" alt="VS Code Debug Architecture 2" loading="lazy"></p>
<p>A more realistic debugger extension contributes many or all of the following declarative items to VS Code:</p>
<ul><li>List of languages supported by the debugger. VS Code enables the UI to set breakpoints for those languages.</li>
<li>JSON schema for the debug configuration attributes introduced by the debugger. VS Code uses this schema to verify the configuration in the launch.json editor and provides IntelliSense. Please note that the JSON schema constructs <code>$ref</code> and <code>definition</code> are not supported.</li>
<li>Default debug configurations for the initial launch.json created by VS Code.</li>
<li>Debug configuration snippets that a user can add to a launch.json file.</li>
<li>Declaration of variables that can be used in debug configurations.</li>
</ul><p>You can find more information in <a href="/api/references/contribution-points#contributes.breakpoints"><code>contributes.breakpoints</code></a> and <a href="/api/references/contribution-points#contributes.debuggers"><code>contributes.debuggers</code></a> references.</p>
<p>In addition to the purely declarative contributions from above, the Debug Extension API enables this code-based functionality:</p>
<ul><li>Dynamically generated default debug configurations for the initial launch.json created by VS Code.</li>
<li>Determine the debug adapter to use dynamically.</li>
<li>Verify or modify debug configurations before they are passed to the debug adapter.</li>
<li>Communicate with the debug adapter.</li>
<li>Send messages to the debug console.</li>
</ul><p>In the rest of this document we show how to develop a debugger extension.</p>
<h2 id="the-mock-debug-extension" data-needslink="the-mock-debug-extension">The Mock Debug Extension</h2>
<p>Since creating a debug adapter from scratch is a bit heavy for this tutorial, we will start with a simple DA which we have created as an educational "debug adapter starter kit". It is called <em>Mock Debug</em> because it does not talk to a real debugger, but mocks one. Mock Debug simulates a debugger and supports step, continue, breakpoints, exceptions, and variable access, but it is not connected to any real debugger.</p>
<p>Before delving into the development setup for mock-debug, let's first install a <a href="https://marketplace.visualstudio.com/items/andreweinand.mock-debug" class="external-link" target="_blank">pre-built version</a>
from the VS Code Marketplace and play with it:</p>
<ul><li>Switch to the Extensions viewlet and type "mock" to search for the Mock Debug extension,</li>
<li>"Install" and "Reload" the extension.</li>
</ul><p>To try Mock Debug:</p>
<ul><li>Create a new empty folder <code>mock test</code> and open it in VS Code.</li>
<li>Create a file <code>readme.md</code> and enter several lines of arbitrary text.</li>
<li>Switch to the Run and Debug view (<span class="dynamic-keybinding" data-commandid="workbench.view.debug" data-osx="⇧⌘D" data-win="Ctrl+Shift+D" data-linux="Ctrl+Shift+D"><span class="keybinding">⇧⌘D</span> (Windows, Linux <span class="keybinding">Ctrl+Shift+D</span>)</span>) and select the <strong>create a launch.json file</strong> link.</li>
<li>VS Code will let you select an "debugger" in order to create a default launch configuration. Pick "Mock Debug".</li>
<li>Press the green <strong>Start</strong> button and then <span class="keybinding">Enter</span> to confirm the suggested file <code>readme.md</code>.</li>
</ul><p>A debug session starts and you can "step" through the readme file, set and hit breakpoints, and run into exceptions (if the word <code>exception</code> appears in a line).</p>
<p><img src="/assets/api/extension-guides/debugger-extension/mock-debug.gif" alt="Mock Debugger running" loading="lazy"></p>
<p>Before using Mock Debug as a starting point for your own development, we recommend to uninstall the pre-built version first:</p>
<ul><li>Switch to the Extensions viewlet and click on the gear icon of the Mock Debug extension.</li>
<li>Run the "Uninstall" action and then "Reload" the window.</li>
</ul><h2 id="development-setup-for-mock-debug" data-needslink="development-setup-for-mock-debug">Development Setup for Mock Debug</h2>
<p>Now let's get the source for Mock Debug and start development on it within VS Code:</p>
<pre class="shiki" data-lang="bash" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">git</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> clone</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> https://github.com/microsoft/vscode-mock-debug.git</span></span>
<span class="line"><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">cd</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> vscode-mock-debug</span></span>
<span class="line"><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">yarn</span></span>
<span class="line"></span></code></pre>
<p>Open the project folder <code>vscode-mock-debug</code> in VS Code.</p>
<p>What's in the package?</p>
<ul><li><code>package.json</code> is the manifest for the mock-debug extension:
<ul><li>It lists the contributions of the mock-debug extension.</li>
<li>The <code>compile</code> and <code>watch</code> scripts are used to transpile the TypeScript source into the <code>out</code> folder and watch for subsequent source modifications.</li>
<li>The dependencies <code>vscode-debugprotocol</code>, <code>vscode-debugadapter</code>, and <code>vscode-debugadapter-testsupport</code> are NPM modules that simplify the development of node-based debug adapters.</li>
</ul></li>
<li><code>src/mockRuntime.ts</code> is a <em>mock</em> runtime with a simple debug API.</li>
<li>The code that <em>adapts</em> the runtime to the Debug Adapter Protocol lives in <code>src/mockDebug.ts</code>. Here you find the handlers for the various requests of the DAP.</li>
<li>Since the implementation of debugger extension lives in the debug adapter, there is no need to have extension code at all (i.e. code that runs in the extension host process). However, Mock Debug has a small <code>src/extension.ts</code> because it illustrates what can be done in the extension code of a debugger extension.</li>
</ul><p>Now build and launch the Mock Debug extension by selecting the <strong>Extension</strong> launch configuration and hitting <code>F5</code>.
Initially, this will do a full transpile of the TypeScript sources into the <code>out</code> folder.
After the full build, a <em>watcher task</em> is started that transpiles any changes you make.</p>
<p>After transpiling the source, a new VS Code window labelled "[Extension Development Host]" appears with the Mock Debug extension now running in debug mode. From that window open your <code>mock test</code> project with the <code>readme.md</code> file, start a debug session with 'F5', and then step through it:</p>
<p><img src="/assets/api/extension-guides/debugger-extension/debug-mock-session.png" alt="Debugging Extension and Server" loading="lazy"></p>
<p>Since you are running the extension in debug mode, you could now set and hit breakpoints in <code>src/extension.ts</code> but as I've mentioned above, there is not much interesting code executing in the extension. The interesting code runs in the debug adapter which is a separate process.</p>
<p>In order to debug the debug adapter itself, we have to run it in debug mode. This is most easily achieved by running the debug adapter in <em>server mode</em> and configure VS Code to connect to it. In your VS Code vscode-mock-debug project select the launch configuration <strong>Server</strong> from the dropdown menu and press the green start button.</p>
<p>Since we already had an active debug session for the extension the VS Code debugger UI now enters <em>multi session</em> mode which is indicated by seeing the names of the two debug sessions <strong>Extension</strong> and <strong>Server</strong> showing up in the CALL STACK view:</p>
<p><img src="/assets/api/extension-guides/debugger-extension/debugger-extension-server.png" alt="Debugging Extension and Server" loading="lazy"></p>
<p>Now we are able to debug both the extension and the DA simultaneously.
A faster way to arrive here is by using the <strong>Extension + Server</strong> launch configuration which launches both sessions automatically.</p>
<p>An alternative, even simpler approach for debugging the extension and the DA can be found <a href="#_alternative-approach-to-develop-a-debugger-extension">below</a>.</p>
<p>Set a breakpoint at the beginning of method <code>launchRequest(...)</code> in file <code>src/mockDebug.ts</code> and as a last step configure the mock debugger to connect to the DA server by adding a <code>debugServer</code> attribute for port <code>4711</code> to your mock test launch config:</p>
<pre class="shiki" data-lang="json" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">{</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "version"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"0.2.0"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "configurations"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">      "type"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"mock"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">      "request"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"launch"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">      "name"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"mock test"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">      "program"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"${workspaceFolder}/readme.md"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">      "stopOnEntry"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">true</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">      "debugServer"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#B5CEA8;--shiki-light:#098658">4711</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  ]</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<p>If you now launch this debug configuration, VS Code does not start the mock debug adapter as a separate process, but directly connects to local port 4711 of the already running server, and you should hit the breakpoint in <code>launchRequest</code>.</p>
<p>With this setup, you can now easily edit, transpile, and debug Mock Debug.</p>
<p>But now the real work begins: you will have to replace the mock implementation of the debug adapter in <code>src/mockDebug.ts</code> and <code>src/mockRuntime.ts</code> by some code that talks to a "real" debugger or runtime. This involves understanding and implementing the Debug Adapter Protocol. More details
about this can be found <a href="https://microsoft.github.io/debug-adapter-protocol/overview#How_it_works" class="external-link" target="_blank">here</a>.</p>
<h2 id="anatomy-of-the-package.json-of-a-debugger-extension" data-needslink="anatomy-of-the-package.json-of-a-debugger-extension">Anatomy of the package.json of a Debugger Extension</h2>
<p>Besides providing a debugger-specific implementation of the debug adapter a debugger extension needs a <code>package.json</code> that contributes to the various debug-related contribution points.</p>
<p>So let's have a closer look at the <code>package.json</code> of Mock Debug.</p>
<p>Like every VS Code extension, the <code>package.json</code> declares the fundamental properties <strong>name</strong>, <strong>publisher</strong>, and <strong>version</strong> of the extension. Use the <strong>categories</strong> field to make the extension easier to find in the VS Code Extension Marketplace.</p>
<pre class="shiki" data-lang="json" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">{</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "name"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"mock-debug"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "displayName"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"Mock Debug"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "version"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"0.24.0"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "publisher"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"..."</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "description"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"Starter extension for developing debug adapters for VS Code."</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "author"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "name"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"..."</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "email"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"..."</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  },</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "engines"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "vscode"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"^1.17.0"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "node"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"^7.9.0"</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  },</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "icon"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"images/mock-debug-icon.png"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "categories"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"Debuggers"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">],</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "contributes"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "breakpoints"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [{ </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">"language"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"markdown"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> }],</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "debuggers"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">        "type"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"mock"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">        "label"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"Mock Debug"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">        "program"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"./out/mockDebug.js"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">        "runtime"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"node"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">        "configurationAttributes"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">          "launch"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">            "required"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"program"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">],</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">            "properties"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">              "program"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">                "type"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"string"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">                "description"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"Absolute path to a text file."</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">                "default"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"${workspaceFolder}/${command:AskForProgramName}"</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">              },</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">              "stopOnEntry"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">                "type"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"boolean"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">                "description"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"Automatically stop after launch."</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">                "default"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">true</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">              }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">            }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">          }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">        },</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">        "initialConfigurations"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">          {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">            "type"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"mock"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">            "request"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"launch"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">            "name"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"Ask for file name"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">            "program"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"${workspaceFolder}/${command:AskForProgramName}"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">            "stopOnEntry"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">true</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">          }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">        ],</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">        "configurationSnippets"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">          {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">            "label"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"Mock Debug: Launch"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">            "description"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"A new configuration for launching a mock debug program"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">            "body"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">              "type"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"mock"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">              "request"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"launch"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">              "name"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"${2:Launch Program}"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">              "program"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"^</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\"\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">${workspaceFolder}/${1:Program}</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\"</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">            }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">          }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">        ],</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">        "variables"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">          "AskForProgramName"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"extension.mock-debug.getProgramName"</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">        }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    ]</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  },</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "activationEvents"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"onDebug"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"onCommand:extension.mock-debug.getProgramName"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">]</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<p>Now take a look at the <strong>contributes</strong> section which contains the contributions specific to debug extensions.</p>
<p>First, we use the <strong>breakpoints</strong> contribution point to list the languages for which setting breakpoints will be enabled. Without this, it would not be possible to set breakpoints in Markdown files.</p>
<p>Next is the <strong>debuggers</strong> section. Here, one debugger is introduced under a debug <strong>type</strong> <code>mock</code>. The user can reference this type in launch configurations. The optional attribute <strong>label</strong> can be used to give the debug type a nice name when showing it in the UI.</p>
<p>Since the debug extension uses a debug adapter, a relative path to its code is given as the <strong>program</strong> attribute.
In order to make the extension self-contained the application must live inside the extension folder. By convention, we keep this application inside a folder named <code>out</code> or <code>bin</code>, but you are free to use a different name.</p>
<p>Since VS Code runs on different platforms, we have to make sure that the DA program supports the different platforms as well. For this we have the following options:</p>
<ol><li>
<p>If the program is implemented in a platform independent way, e.g. as program that runs on a runtime that is available on all supported platforms, you can specify this runtime via the <strong>runtime</strong> attribute. As of today, VS Code supports <code>node</code> and <code>mono</code> runtimes. Our Mock debug adapter from above uses this approach.</p>
</li>
<li>
<p>If your DA implementation needs different executables on different platforms, the <strong>program</strong> attribute can be qualified for specific platforms like this:</p>
<pre class="shiki" data-lang="json" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"debuggers"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [{</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "type"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"gdb"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "windows"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">        "program"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"./bin/gdbDebug.exe"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    },</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "osx"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">        "program"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"./bin/gdbDebug.sh"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    },</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "linux"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">        "program"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"./bin/gdbDebug.sh"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}]</span></span>
<span class="line"></span></code></pre>
</li>
<li>
<p>A combination of both approaches is possible too. The following example is from the Mono DA which is implemented as a mono application that needs a runtime on macOS and Linux but not on Windows:</p>
<pre class="shiki" data-lang="json" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"debuggers"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [{</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "type"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"mono"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "program"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"./bin/monoDebug.exe"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "osx"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">        "runtime"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"mono"</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    },</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "linux"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">        "runtime"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"mono"</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}]</span></span>
<span class="line"></span></code></pre>
</li>
</ol><p><strong>configurationAttributes</strong> declares the schema for the <code>launch.json</code> attributes that are available for this debugger. This schema is used for validating the <code>launch.json</code> and supporting IntelliSense and hover help when editing the launch configuration.</p>
<p>The <strong>initialConfigurations</strong> define the initial content of the default <code>launch.json</code> for this debugger. This information is used when a project does not have a <code>launch.json</code> and a user starts a debug session or selects the <strong>create a launch.json file</strong> link in the Run and Debug view. In this case VS Code lets the user pick a debug environment and then creates the corresponding <code>launch.json</code>:</p>
<p><img src="/assets/api/extension-guides/debugger-extension/debug-init-config.png" alt="Debugger Quickpick" loading="lazy"></p>
<p>Instead of defining the initial content of the <code>launch.json</code> statically in the <code>package.json</code>, it is possible to compute the initial configurations dynamically by implementing a <code>DebugConfigurationProvider</code> (for details see the section <a href="#_using-a-debugconfigurationprovider">Using a DebugConfigurationProvider below</a>).</p>
<p><strong>configurationSnippets</strong> define launch configuration snippets that get surfaced in IntelliSense when editing the <code>launch.json</code>. As a convention, prefix the <code>label</code> attribute of a snippet by the debug environment name so that it can be clearly identified when presented in a list of many snippet proposals.</p>
<p>The <strong>variables</strong> contribution binds "variables" to "commands". These variables can be used in the launch configuration using the <strong>${command:xyz}</strong> syntax and the variables are substituted by the value returned from the bound command when a debug session is started.</p>
<p>The implementation of a command lives in the extension and it can range from a simple expression with no UI, to sophisticated functionality based on the UI features available in the extension API.
Mock Debug binds a variable <code>AskForProgramName</code> to the command <code>extension.mock-debug.getProgramName</code>. The <a href="https://github.com/microsoft/vscode-mock-debug/blob/606454ff3bd669867a38d9b2dc7b348d324a3f6b/src/extension.ts#L21-L26" class="external-link" target="_blank">implementation</a> of this command in <code>src/extension.ts</code> uses the <code>showInputBox</code> to let the user enter a program name:</p>
<pre class="shiki" data-lang="ts" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">commands</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">registerCommand</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'extension.mock-debug.getProgramName'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">config</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> =&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">  return</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">window</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">showInputBox</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">({</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    placeHolder:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'Please enter the name of a markdown file in the workspace folder'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    value:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'readme.md'</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  });</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">});</span></span>
<span class="line"></span></code></pre>
<p>The variable can now be used in any string typed value of a launch configuration as <strong>${command:AskForProgramName}</strong>.</p>
<h2 id="using-a-debugconfigurationprovider" data-needslink="using-a-debugconfigurationprovider">Using a DebugConfigurationProvider</h2>
<p>If the static nature of debug contributions in the <code>package.json</code> is not sufficient, a <code>DebugConfigurationProvider</code> can be used to dynamically control the following aspects of a debug extension:</p>
<ul><li>The initial debug configurations for a newly created launch.json can be generated dynamically, e.g. based on some contextual information available in the workspace.</li>
<li>A launch configuration can be <em>resolved</em> (or modified) before it is used to start a new debug session. This allows for filling in default values based on information available in the workspace. Two <em>resolve</em> methods exist: <code>resolveDebugConfiguration</code> is called before variables are substituted in the launch configuration, <code>resolveDebugConfigurationWithSubstitutedVariables</code> is called after all variables have been substituted. The former must be used if the validation logic inserts additional variables into the debug configuration. The latter must be used if the validation logic needs access to the final values of all debug configuration attributes.</li>
</ul><p>The <code>MockConfigurationProvider</code> in <code>src/extension.ts</code> implements <code>resolveDebugConfiguration</code> to detect the case where a debug session is started when no launch.json exists, but a Markdown file is open in the active editor. This is a typical scenario where the user has a file open in the editor and just wants to debug it without creating a launch.json.</p>
<p>A debug configuration provider is registered for a specific debug type via <code>vscode.debug.registerDebugConfigurationProvider</code>, typically in the extension's <code>activate</code> function.
To ensure that the <code>DebugConfigurationProvider</code> is registered early enough, the extension must be activated as soon as the debug functionality is used. This can be easily achieved by configuring extension activation for the <code>onDebug</code> event in the <code>package.json</code>:</p>
<pre class="shiki" data-lang="json" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"activationEvents"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">    "onDebug"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">    // ...</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">],</span></span>
<span class="line"></span></code></pre>
<p>This catch-all <code>onDebug</code> is triggered as soon as any debug functionality is used. This works fine as long as the extension has cheap startup costs (i.e. does not spend a lot of time in its startup sequence). If a debug extension has an expensive startup (for instance because of starting a language server), the <code>onDebug</code> activation event could negatively affect other debug extensions, because it is triggered rather early and does not take a specific debug type into account.</p>
<p>A better approach for expensive debug extensions is to use more fine-grained activation events:</p>
<ul><li><code>onDebugInitialConfigurations</code> is fired just before the <code>provideDebugConfigurations</code> method of the <code>DebugConfigurationProvider</code> is called.</li>
<li><code>onDebugResolve:type</code> is fired just before the <code>resolveDebugConfiguration</code> or <code>resolveDebugConfigurationWithSubstitutedVariables</code> methods of the <code>DebugConfigurationProvider</code> for the specified type is called.</li>
</ul><p><strong>Rule of thumb:</strong> If activation of a debug extensions is cheap, use <code>onDebug</code>. If it is expensive, use <code>onDebugInitialConfigurations</code> and/or <code>onDebugResolve</code> depending on whether the <code>DebugConfigurationProvider</code> implements the corresponding methods <code>provideDebugConfigurations</code> and/or <code>resolveDebugConfiguration</code>.</p>
<h2 id="publishing-your-debugger-extension" data-needslink="publishing-your-debugger-extension">Publishing your debugger extension</h2>
<p>Once you have created your debugger extension you can publish it to the Marketplace:</p>
<ul><li>Update the attributes in the <code>package.json</code> to reflect the naming and purpose of your debugger extension.</li>
<li>Upload to the Marketplace as described in <a href="/api/working-with-extensions/publishing-extension">Publishing Extension</a>.</li>
</ul><h2 id="alternative-approach-to-develop-a-debugger-extension" data-needslink="alternative-approach-to-develop-a-debugger-extension">Alternative approach to develop a debugger extension</h2>
<p>As we have seen, developing a debugger extension typically involves debugging both the extension and the debug adapter in two parallel sessions. As explained above VS Code supports this nicely but development could be easier if both the extension and the debug adapter would be one program that could be debugged in one debug session.</p>
<p>This approach is in fact easily doable as long as your debug adapter is implemented in TypeScript/JavaScript. The basic idea is to run the debug adapter directly inside the extension and to make VS Code to connect to it instead of launching a new external debug adapter per session.</p>
<p>For this VS Code provides extension API to control how a debug adapter is created and run. A <code>DebugAdapterDescriptorFactory</code> has a method <code>createDebugAdapterDescriptor</code> that is called by VS Code when a debug session starts and a debug adapter is needed. This method must return a descriptor object (<code>DebugAdapterDescriptor</code>) that describes how the debug adapter is run.</p>
<p>Today VS Code supports three different ways for running a debug adapter and consequently offers three different descriptor types:</p>
<ul><li><code>DebugAdapterExecutable</code>: this object describes a debug adapter as an external executable with a path and optional arguments and runtime. The executable must implement the Debug Adapter Protocol and communicate via stdin/stdout. This is VS Code's default mode of operation and VS Code uses this descriptor automatically with the corresponding values from the package.json if no <code>DebugAdapterDescriptorFactory</code> is explicitly registered.</li>
<li><code>DebugAdapterServer</code>: this object describes a debug adapter running as a server that communicates via a specific local or remote port. A debug adapter implementation based on the <a href="https://www.npmjs.com/package/vscode-debugadapter" class="external-link" target="_blank"><code>vscode-debugadapter</code></a> npm module supports this server mode automatically.</li>
<li><code>DebugAdapterInlineImplementation</code>: this object describes a debug adapter as a JavaScript or Typescript object that implements the <code>vscode.DebugAdapter</code> interface. A debug adapter implementation based on version 1.38-pre.4 or later of the <a href="https://www.npmjs.com/package/vscode-debugadapter" class="external-link" target="_blank"><code>vscode-debugadapter</code></a> npm module implements the interface automatically.</li>
</ul><p>Mock Debug shows examples for the <a href="https://github.com/microsoft/vscode-mock-debug/blob/668fa6f5db95dbb76825d4eb670ab0d305050c3b/src/extension.ts#L91-L150" class="external-link" target="_blank">three types of DebugAdapterDescriptorFactories</a>  and how they are <a href="https://github.com/microsoft/vscode-mock-debug/blob/668fa6f5db95dbb76825d4eb670ab0d305050c3b/src/extension.ts#L50" class="external-link" target="_blank">registered for the 'mock' debug type</a>. The run mode to use can be selected by <a href="https://github.com/microsoft/vscode-mock-debug/blob/668fa6f5db95dbb76825d4eb670ab0d305050c3b/src/extension.ts#L16" class="external-link" target="_blank">setting the global variable <code>runMode</code></a> to one of the possible values <code>external</code>, <code>server</code>, or <code>inline</code>.</p>
<p>For development, the <code>inline</code> and <code>server</code> modes are particularly useful because they allow for debugging extension and debug adapter within a single process.</p>

				<div class="feedback" data-edit-url="https://vscode.dev/github/microsoft/vscode-docs/blob/main/api/extension-guides/debugger-extension.md"></div>
				
				<div class="body-footer">6/3/2026</div>
				
            </main><aside class="docs-right-sidebar hidden-xs"><div class="docs-markdown-actions">
                    <div class="docs-markdown-dropdown" data-raw-url="/raw/api/extension-guides/debugger-extension.md">
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
                <nav id="docs-subnavbar" aria-label="On Page"><h4><span class="sr-only">On this page there are 7 sections</span><span aria-hidden="true">On this page</span></h4>
                    <ul class="nav"><li><a href="#debugging-architecture-of-vs-code">Debugging Architecture of VS Code</a></li>
                        
                        <li><a href="#the-mock-debug-extension">The Mock Debug Extension</a></li>
                        
                        <li><a href="#development-setup-for-mock-debug">Development Setup for Mock Debug</a></li>
                        
                        <li><a href="#anatomy-of-the-package.json-of-a-debugger-extension">Anatomy of the package.json of a Debugger Extension</a></li>
                        
                        <li><a href="#using-a-debugconfigurationprovider">Using a DebugConfigurationProvider</a></li>
                        
                        <li><a href="#publishing-your-debugger-extension">Publishing your debugger extension</a></li>
                        
                        <li><a href="#alternative-approach-to-develop-a-debugger-extension">Alternative approach to develop a debugger extension</a></li>
                        
                    </ul></nav></aside></div>
		<div class="docs-mobile-widgets visible-xs">
			<div class="connect-widget"></div>
		</div>
	</div>
</div>
		</main>