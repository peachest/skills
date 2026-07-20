# Supporting Remote Development and GitHub Codespaces

> 源文档: [https://code.visualstudio.com/api/advanced-topics/remote-extensions](https://code.visualstudio.com/api/advanced-topics/remote-extensions)

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
			          
			        <li class="active">
			          <a href="/api/advanced-topics/remote-extensions" aria-label="Current Page: Remote Development and Codespaces">Remote Development and Codespaces</a>
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
				<select id="small-nav-dropdown" aria-label="topics"><option value="/api">Overview</option><optgroup label="Get Started"><option value="/api/get-started/your-first-extension">Your First Extension</option><option value="/api/get-started/extension-anatomy">Extension Anatomy</option><option value="/api/get-started/wrapping-up">Wrapping Up</option></optgroup><optgroup label="Extension Capabilities"><option value="/api/extension-capabilities/overview">Overview</option><option value="/api/extension-capabilities/common-capabilities">Common Capabilities</option><option value="/api/extension-capabilities/theming">Theming</option><option value="/api/extension-capabilities/extending-workbench">Extending Workbench</option></optgroup><optgroup label="Extension Guides"><option value="/api/extension-guides/overview">Overview</option><optgroup label="Extension Guides - AI"><option value="/api/extension-guides/ai/ai-extensibility-overview">AI Extensibility</option><option value="/api/extension-guides/ai/tools">Language Model Tool</option><option value="/api/extension-guides/ai/mcp">MCP Dev Guide</option><option value="/api/extension-guides/ai/chat">Chat Participant</option><option value="/api/extension-guides/ai/chat-tutorial">Chat Tutorial</option><option value="/api/extension-guides/ai/language-model">Language Model</option><option value="/api/extension-guides/ai/language-model-tutorial">Language Model Tutorial</option><option value="/api/extension-guides/ai/language-model-chat-provider">Language Model Chat Provider</option><option value="/api/extension-guides/ai/prompt-tsx">Prompt TSX</option></optgroup><option value="/api/extension-guides/command">Command</option><option value="/api/extension-guides/color-theme">Color Theme</option><option value="/api/extension-guides/file-icon-theme">File Icon Theme</option><option value="/api/extension-guides/product-icon-theme">Product Icon Theme</option><option value="/api/extension-guides/tree-view">Tree View</option><option value="/api/extension-guides/webview">Webview</option><option value="/api/extension-guides/notebook">Notebook</option><option value="/api/extension-guides/custom-editors">Custom Editors</option><option value="/api/extension-guides/virtual-documents">Virtual Documents</option><option value="/api/extension-guides/virtual-workspaces">Virtual Workspaces</option><option value="/api/extension-guides/web-extensions">Web Extensions</option><option value="/api/extension-guides/workspace-trust">Workspace Trust</option><option value="/api/extension-guides/task-provider">Task Provider</option><option value="/api/extension-guides/scm-provider">Source Control</option><option value="/api/extension-guides/debugger-extension">Debugger Extension</option><option value="/api/extension-guides/markdown-extension">Markdown Extension</option><option value="/api/extension-guides/testing">Test Extension</option><option value="/api/extension-guides/custom-data-extension">Custom Data Extension</option><option value="/api/extension-guides/telemetry">Telemetry</option></optgroup><optgroup label="UX Guidelines"><option value="/api/ux-guidelines/overview">Overview</option><option value="/api/ux-guidelines/activity-bar">Activity Bar</option><option value="/api/ux-guidelines/sidebars">Sidebars</option><option value="/api/ux-guidelines/panel">Panel</option><option value="/api/ux-guidelines/status-bar">Status Bar</option><option value="/api/ux-guidelines/views">Views</option><option value="/api/ux-guidelines/editor-actions">Editor Actions</option><option value="/api/ux-guidelines/quick-picks">Quick Picks</option><option value="/api/ux-guidelines/command-palette">Command Palette</option><option value="/api/ux-guidelines/notifications">Notifications</option><option value="/api/ux-guidelines/webviews">Webviews</option><option value="/api/ux-guidelines/context-menus">Context Menus</option><option value="/api/ux-guidelines/walkthroughs">Walkthroughs</option><option value="/api/ux-guidelines/settings">Settings</option></optgroup><optgroup label="Language Extensions"><option value="/api/language-extensions/overview">Overview</option><option value="/api/language-extensions/syntax-highlight-guide">Syntax Highlight Guide</option><option value="/api/language-extensions/semantic-highlight-guide">Semantic Highlight Guide</option><option value="/api/language-extensions/snippet-guide">Snippet Guide</option><option value="/api/language-extensions/language-configuration-guide">Language Configuration Guide</option><option value="/api/language-extensions/programmatic-language-features">Programmatic Language Features</option><option value="/api/language-extensions/language-server-extension-guide">Language Server Extension Guide</option><option value="/api/language-extensions/embedded-languages">Embedded Languages</option></optgroup><optgroup label="Testing and Publishing"><option value="/api/working-with-extensions/testing-extension">Testing Extensions</option><option value="/api/working-with-extensions/publishing-extension">Publishing Extensions</option><option value="/api/working-with-extensions/bundling-extension">Bundling Extensions</option><option value="/api/working-with-extensions/continuous-integration">Continuous Integration</option></optgroup><optgroup label="Advanced Topics"><option value="/api/advanced-topics/extension-host">Extension Host</option><option value="/api/advanced-topics/remote-extensions" selected>Remote Development and Codespaces</option><option value="/api/advanced-topics/using-proposed-api">Using Proposed API</option><option value="/api/advanced-topics/tslint-eslint-migration">Migrate from TSLint to ESLint</option><option value="/api/advanced-topics/python-extension-template">Python Extension Template</option></optgroup><optgroup label="References"><option value="/api/references/vscode-api">VS Code API</option><option value="/api/references/contribution-points">Contribution Points</option><option value="/api/references/activation-events">Activation Events</option><option value="/api/references/extension-manifest">Extension Manifest</option><option value="/api/references/commands">Built-In Commands</option><option value="/api/references/when-clause-contexts">When Clause Contexts</option><option value="/api/references/theme-color">Theme Color</option><option value="/api/references/icons-in-labels">Product Icon Reference</option><option value="/api/references/document-selector">Document Selector</option></optgroup></select></nav></aside><div class="docs-content-wrapper">
			
			<main class="docs-main-content body"><h1>Supporting Remote Development and GitHub Codespaces</h1>
<p><strong><a href="/docs/remote/remote-overview">Visual Studio Code Remote Development</a></strong> allows you to transparently interact with source code and runtime environments sitting on other machines (whether virtual or physical). <strong><a href="https://github.com/features/codespaces" class="external-link" target="_blank">GitHub Codespaces</a></strong> is a service that expands these capabilities with managed cloud-hosted environments that are accessible from both VS Code and a browser-based editor.</p>
<p>To ensure performance, Remote Development and GitHub Codespaces both transparently run certain VS Code extensions remotely. However, this can have subtle impacts on how extensions need to work.  While many extensions will work without any modifications, you may need to make changes so that your extension works properly in all environments, although these changes are often fairly minor.</p>
<p>This article summarizes what extension authors need to know about Remote Development and Codespaces including the extension <a href="#_architecture-and-extension-kinds">architecture</a>, how to <a href="#_debugging-extensions">debug your extension</a> in remote workspaces or Codespaces, and recommendations on <a href="#_common-problems">what to do if your extension does not work properly</a>.</p>
<h2 id="architecture-and-extension-kinds" data-needslink="architecture-and-extension-kinds">Architecture and extension kinds</h2>
<p>In order to make working with Remote Development or Codespaces as transparent as possible to users, VS Code distinguishes two kinds of extensions:</p>
<ul><li>
<p><strong>UI Extensions</strong>: These extensions contribute to the VS Code user interface and are always run on the user's local machine. UI Extensions cannot directly access files in the remote workspace, or run scripts/tools installed in that workspace or on the machine. Example UI Extensions include: themes, snippets, language grammars, and keymaps.</p>
</li>
<li>
<p><strong>Workspace Extensions</strong>: These extensions are run on the same machine as where the workspace is located. When in a local workspace, Workspace Extensions run on the local machine. When in a remote workspace or when using Codespaces, Workspace Extensions run on the remote machine / environment. Workspace Extensions can access files in the workspace to provide rich, multi-file language services, debugger support, or perform complex operations on multiple files in the workspace (either directly or by invoking scripts/tools). While Workspace Extensions do not focus on modifying the UI, they can contribute explorers, views, and other UI elements as well.</p>
</li>
</ul><p>When a user installs an extension, VS Code automatically installs it to the correct location based on its kind. If an extension can run as either kind, VS Code will attempt to choose the optimal one for the situation; UI Extensions will run in VS Code's <a href="/api/advanced-topics/extension-host">local Extension Host</a>, while Workspace Extensions will run in a <strong>Remote Extension Host</strong> that sits in a small <a href="/docs/remote/vscode-server"><strong>VS Code Server</strong></a>, if it exists in a remote workspace, otherwise will run in VS Code's local extension host if it exists locally. To ensure the latest VS Code client features are available, the server needs to match the VS Code client version exactly. Therefore, the server is automatically installed (or updated) by the Remote Development or GitHub Codespaces extensions when you open a folder in a container, on a remote SSH host, using Codespaces, or in the Windows Subsystem for Linux (WSL). (VS Code also automatically manages starting and stopping the server, so users aren't aware of its presence.)</p>
<p><img src="/assets/api/advanced-topics/remote-extensions/architecture.png" alt="Architecture diagram" loading="lazy"></p>
<p>The VS Code APIs are designed to automatically run on the correct machine (either local or remote) when called from both UI or Workspace Extensions. However, if your extension uses APIs not provided by VS Code — such using Node APIs or running shell scripts — it may not work properly when run remotely. We recommend that you test that all features of your extension work properly in both local and remote workspaces.</p>
<h2 id="debugging-extensions" data-needslink="debugging-extensions">Debugging Extensions</h2>
<p>While you <a href="#_installing-a-development-version-of-your-extension">can install a development version of your extension</a> in a remote environment for testing, if you encounter issues, you will likely want to debug your extension directly in a remote environment. In this section, we will cover how to edit, launch, and debug your extension in <a href="#_debugging-with-github-codespaces">GitHub Codespaces</a>, a <a href="#_debugging-in-a-custom-development-container">local container</a>, an <a href="#_debugging-using-ssh">SSH host</a>, or in <a href="#_debugging-using-wsl">WSL</a>.</p>
<p>Typically, your best starting point for testing is to use a remote environment that restricts port access (for example Codespaces, a container, or remote SSH hosts with a restrictive firewall) since extensions that work in these environments tend to work in less restrictive ones like WSL.</p>
<h3 id="debugging-with-github-codespaces" data-needslink="debugging-with-github-codespaces">Debugging with GitHub Codespaces</h3>
<p>Debugging your extension in <a href="https://docs.github.com/github/developing-online-with-codespaces" class="external-link" target="_blank">GitHub Codespaces</a> preview can be a great starting point since you can use both VS Code and the Codespaces browser-based editor for testing and troubleshooting. You can also use a <a href="#_debugging-in-a-custom-development-container">custom development container</a> if preferred.</p>
<p>Follow these steps:</p>
<ol><li>
<p>Navigate to the repository that contains your extension on GitHub and <a href="https://docs.github.com/github/developing-online-with-codespaces/creating-a-codespace" class="external-link" target="_blank">open it in a codespace</a> to work with it in a browser-based editor. You can also <a href="https://docs.github.com/github/developing-online-with-codespaces/using-codespaces-in-visual-studio-code" class="external-link" target="_blank">open the codespace in VS Code</a> if you prefer.</p>
</li>
<li>
<p>While the default image for GitHub Codespaces should have all the needed prerequisites for most extensions, you can install any other required dependencies (for example, using <code>yarn install</code> or <code>sudo apt-get</code>) in a new VS Code terminal window (<span class="dynamic-keybinding" data-commandid="workbench.action.terminal.new" data-osx="⌃⇧`" data-win="Ctrl+Shift+`" data-linux="Ctrl+Shift+`"><span class="keybinding">⌃⇧`</span> (Windows, Linux <span class="keybinding">Ctrl+Shift+`</span>)</span>).</p>
</li>
<li>
<p>Finally, press <span class="dynamic-keybinding" data-commandid="workbench.action.debug.start" data-osx="F5" data-win="F5" data-linux="F5"><span class="keybinding">F5</span></span> or use the <strong>Run and Debug</strong> view to launch the extension inside in the codespace.</p>
<blockquote><p><strong>Note:</strong> You will not be able to open the extension source code folder in the window that appears, but you can open a sub-folder or somewhere else in the codespace.</p>
</blockquote></li>
</ol><p>The extension development host window that appears will include your extension running in a codespace with the debugger attached to it.</p>
<h3 id="debugging-in-a-custom-development-container" data-needslink="debugging-in-a-custom-development-container">Debugging in a custom development container</h3>
<p>Follow these steps:</p>
<ol><li>
<p>To use a development container locally, <a href="/docs/devcontainers/containers#getting-started">install and configure the Dev Containers extension</a>, and use <strong>File &gt; Open... / Open Folder...</strong> to open your source code locally in VS Code. To use Codespaces instead, navigate to the repository that contains your extension on GitHub and <a href="https://docs.github.com/github/developing-online-with-codespaces/creating-a-codespace" class="external-link" target="_blank">open it in a codespace</a> to work with it in a browser-based editor. You can also <a href="https://docs.github.com/github/developing-online-with-codespaces/using-codespaces-in-visual-studio-code" class="external-link" target="_blank">open the codespace in VS Code</a> if you prefer.</p>
</li>
<li>
<p>Select <strong>Dev Containers: Add Dev Container Configuration Files...</strong> or <strong>Codespaces: Add Dev Container Configuration Files...</strong> from the Command Palette (<span class="keybinding">F1</span>), and pick <strong>Node.js &amp; TypeScript</strong> (or Node.js if you are not using TypeScript) to add the needed container configuration files.</p>
</li>
<li>
<p><strong>Optional:</strong> After this command runs, you can modify the contents of the <code>.devcontainer</code> folder to include additional build or runtime requirements. See the in-depth <a href="/docs/devcontainers/create-dev-container">Create a Dev Container</a> documentation for details.</p>
</li>
<li>
<p>Run <strong>Dev Containers: Reopen in Container</strong> or <strong>Codespaces: Add Dev Container Configuration Files...</strong> and in a moment, VS Code will set up the container and connect. You will now be able to develop your source code from inside the container just as you would in the local case.</p>
</li>
<li>
<p>Run <code>yarn install</code> or <code>npm install</code> in a new VS Code terminal window (<span class="dynamic-keybinding" data-commandid="workbench.action.terminal.new" data-osx="⌃⇧`" data-win="Ctrl+Shift+`" data-linux="Ctrl+Shift+`"><span class="keybinding">⌃⇧`</span> (Windows, Linux <span class="keybinding">Ctrl+Shift+`</span>)</span>) to ensure the Linux versions Node.js native dependencies are installed. You can also install other OS or runtime dependencies, but you may want to add these to <code>.devcontainer/Dockerfile</code> as well so they are available if you rebuild the container.</p>
</li>
<li>
<p>Finally, press <span class="dynamic-keybinding" data-commandid="workbench.action.debug.start" data-osx="F5" data-win="F5" data-linux="F5"><span class="keybinding">F5</span></span> or use the <strong>Run and Debug</strong> view to launch the extension inside this same container and attach the debugger.</p>
<blockquote><p><strong>Note:</strong> You will not be able to open the extension source code folder in the window that appears, but you can open a sub-folder or somewhere else in the container.</p>
</blockquote></li>
</ol><p>The extension development host window that appears will include your extension running in the container you defined in step 2 with the debugger attached to it.</p>
<h3 id="debugging-using-ssh" data-needslink="debugging-using-ssh">Debugging using SSH</h3>
<p>Follow steps:</p>
<ol><li>
<p>After <a href="/docs/remote/ssh#getting-started">installing and configuring the Remote - SSH extension</a>, select <strong>Remote-SSH: Connect to Host...</strong> from the Command Palette (<span class="keybinding">F1</span>) in VS Code to connect to a host.</p>
</li>
<li>
<p>Once connected, either use <strong>File &gt; Open... / Open Folder...</strong> to select the remote folder with your extension source code in it or select <strong>Git: Clone</strong> from the Command Palette (<span class="keybinding">F1</span>) to clone it and open it on the remote host.</p>
</li>
<li>
<p>Install any required dependencies that might be missing (for example using <code>yarn install</code> or <code>apt-get</code>) in a new VS Code terminal window (<span class="dynamic-keybinding" data-commandid="workbench.action.terminal.new" data-osx="⌃⇧`" data-win="Ctrl+Shift+`" data-linux="Ctrl+Shift+`"><span class="keybinding">⌃⇧`</span> (Windows, Linux <span class="keybinding">Ctrl+Shift+`</span>)</span>).</p>
</li>
<li>
<p>Finally, press <span class="dynamic-keybinding" data-commandid="workbench.action.debug.start" data-osx="F5" data-win="F5" data-linux="F5"><span class="keybinding">F5</span></span> or use the <strong>Run and Debug</strong> view to launch the extension inside on the remote host and attach the debugger.</p>
<blockquote><p><strong>Note:</strong> You will not be able to open the extension source code folder in the window that appears, but you can open a sub-folder or somewhere else on the SSH host.</p>
</blockquote></li>
</ol><p>The extension development host window that appears will include your extension running on the SSH host with the debugger attached to it.</p>
<h3 id="debugging-using-wsl" data-needslink="debugging-using-wsl">Debugging using WSL</h3>
<p>Follow these steps:</p>
<ol><li>
<p>After <a href="/docs/remote/wsl">installing and configuring the WSL extension</a>, select <strong>WSL: New Window</strong> from the Command Palette (<span class="keybinding">F1</span>) in VS Code.</p>
</li>
<li>
<p>In the new window that appears, either use <strong>File &gt; Open... / Open Folder...</strong> to select the remote folder with your extension source code in it or select <strong>Git: Clone</strong> from the Command Palette (<span class="keybinding">F1</span>) to clone it and open it in WSL.</p>
<blockquote><p><strong>Tip:</strong> You can select the <code>/mnt/c</code> folder to access any cloned source code you have on the Windows side.</p>
</blockquote></li>
<li>
<p>Install any required dependencies that might be missing (for example using <code>apt-get</code>) in a new VS Code terminal window (<span class="dynamic-keybinding" data-commandid="workbench.action.terminal.new" data-osx="⌃⇧`" data-win="Ctrl+Shift+`" data-linux="Ctrl+Shift+`"><span class="keybinding">⌃⇧`</span> (Windows, Linux <span class="keybinding">Ctrl+Shift+`</span>)</span>). You will at least want to run <code>yarn install</code> or <code>npm install</code> to ensure Linux versions of native Node.js dependencies are available.</p>
</li>
<li>
<p>Finally, press <span class="dynamic-keybinding" data-commandid="workbench.action.debug.start" data-osx="F5" data-win="F5" data-linux="F5"><span class="keybinding">F5</span></span> or use the <strong>Run and Debug</strong> view to launch the extension and attach the debugger as you would locally.</p>
<blockquote><p><strong>Note:</strong> You will not be able to open the extension source code folder in the window that appears, but you can open a sub-folder or somewhere else in WSL.</p>
</blockquote></li>
</ol><p>The extension development host window that appears will include your extension running in WSL with the debugger attached to it.</p>
<h2 id="installing-a-development-version-of-your-extension" data-needslink="installing-a-development-version-of-your-extension">Installing a development version of your extension</h2>
<p>Anytime VS Code automatically installs an extension on an SSH host, inside a container or WSL, or through GitHub Codespaces, the Marketplace version is used (and not the version already installed on your local machine).</p>
<p>While this makes sense in most situations, you may want to use (or share) an unpublished version of your extension for testing without having to set up a debugging environment. To install an unpublished version of your extension, you can package the extension as a <code>VSIX</code> and manually install it into a VS Code window that is already connected to a running remote environment.</p>
<p>Follow these steps:</p>
<ol><li>If this is a published extension, you may want to add <code>"extensions.autoUpdate": false</code> to <code>settings.json</code> to prevent it from auto-updating to the latest Marketplace version.</li>
<li>Next, use <code>vsce package</code> to package your extension as a VSIX.</li>
<li>Connect to a <a href="https://docs.github.com/github/developing-online-with-codespaces" class="external-link" target="_blank">codespace</a>, <a href="/docs/devcontainers/containers">Dev Containers</a>, <a href="/docs/remote/ssh">SSH host</a>, or <a href="/docs/remote/wsl">WSL environment</a>.</li>
<li>Use the <strong>Install from VSIX...</strong> command available in the Extensions view <strong>More Actions</strong> (<code>...</code>) menu to install the extension in this specific window (not a local one).</li>
<li>Reload when prompted.</li>
</ol><blockquote><p><strong>Tip:</strong> Once installed, you can use the <strong>Developer: Show Running Extensions</strong> command to see whether VS Code is running the extension locally or remotely.</p>
</blockquote><h2 id="handling-dependencies-with-remote-extensions" data-needslink="handling-dependencies-with-remote-extensions">Handling dependencies with remote extensions</h2>
<p>Extensions can take dependencies on other extensions for APIs. For example:</p>
<ul><li>An extension can export an API from their <code>activate</code> function.</li>
<li>This API will become available to all extensions running in the same extension host.</li>
<li>Consumer extensions declare in their <code>package.json</code> that they depend on the providing extension using the <code>extensionDependencies</code> property.</li>
</ul><p>Extension dependencies work fine when all the extensions are running locally and share the same extension host.</p>
<p>When dealing with remote scenarios, it is possible that an extension running remotely has an extension dependency on an extension running locally. For example, the local extension exposes a command that is critical to the functioning of the remote extension. In this case, we recommend that the remote extension declares the local extension as an <code>extensionDependency</code>, but the problem is that the extensions run on two different extension hosts, which means that the API from the provider is not available to the consumer. It is therefore required that the providing extension give up entirely the ability to export any APIs by using <code>"api": "none"</code> in their extension's <code>package.json</code>. The extensions can still communicate using VS Code commands (which are asynchronous).</p>
<p>This may seem an unnecessarily strict constraint on the providing extension, but an extension that uses <code>"api": "none"</code> only gives up the ability to return APIs from its <code>activate</code> method. Consumer extensions that execute on other extension hosts can still take a dependency on them and will be activated.</p>
<h2 id="common-problems" data-needslink="common-problems">Common problems</h2>
<p>VS Code's APIs are designed to automatically run in the right location regardless of where your extension happens to be located. With this in mind, there are a few APIs that will help you avoid unexpected behaviors.</p>
<h3 id="incorrect-execution-location" data-needslink="incorrect-execution-location">Incorrect execution location</h3>
<p>If your extension is not functioning as expected, it may be running in the wrong location. Most commonly, this shows up as an extension running remotely when you expect it to only be run locally. You can use the <strong>Developer: Show Running Extensions</strong> command from the Command Palette (<span class="keybinding">F1</span>) to see where an extension is running.</p>
<p>If the <strong>Developer: Show Running Extensions</strong> command shows that a UI extension is incorrectly being treated as a workspace extension or vice versa, try setting the <code>extensionKind</code> property in your extension's <a href="/api/get-started/extension-anatomy#extension-manifest">package.json</a> as described in the <a href="/api/advanced-topics/extension-host#preferred-extension-location">Extension Kinds section</a>.</p>
<p>You can quickly <strong>test</strong> the effect of changing an extension's kind with the <code>remote.extensionKind</code> <a href="/docs/configure/settings">setting</a>. This setting is a map of extension IDs to extension kinds. For example, if you want to force the <a href="https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-cosmosdb" class="external-link" target="_blank">Azure Databases</a> extension to be a UI extension (instead of its Workspace default) and the <a href="https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-ssh-edit" class="external-link" target="_blank">Remote - SSH: Editing Configuration Files</a> extension to be a workspace extension (instead of its UI default), you would set:</p>
<pre class="shiki" data-lang="json" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">{</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "remote.extensionKind"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "ms-azuretools.vscode-cosmosdb"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"ui"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">],</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "ms-vscode-remote.remote-ssh-edit"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"workspace"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">]</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<p>Using <code>remote.extensionKind</code> allows you to quickly test published versions of extensions without having to modify their <code>package.json</code> and rebuild them.</p>
<h3 id="persisting-extension-data-or-state" data-needslink="persisting-extension-data-or-state">Persisting extension data or state</h3>
<p>In some cases, your extension may need to persist state information that does not belong in <code>settings.json</code> or a separate workspace configuration file (for example <code>.eslintrc</code>). To solve this problem, VS Code provides a set of helpful storage properties on the <code>vscode.ExtensionContext</code> object passed to your extension during activation. If your extension already takes advantage of these properties, it should continue to function regardless of where it runs.</p>
<p>However, if your extension relies on current VS Code pathing conventions (for example <code>~/.vscode</code>) or the presence of certain OS folders (for example <code>~/.config/Code</code> on Linux) to persist data, you may run into problems. Fortunately, it should be simple to update your extension and avoid these challenges.</p>
<p>If you are persisting simple key-value pairs, you can store workspace specific or global state information using <code>vscode.ExtensionContext.workspaceState</code> or <code>vscode.ExtensionContext.globalState</code> respectively. If your data is more complicated than key-value pairs, the  <code>globalStorageUri</code> and <code>storageUri</code> properties provide "safe" URIs that you can use to read/write global workspace-specific information in a file.</p>
<p>To use the APIs:</p>
<pre class="shiki" data-lang="typescript" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">import</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> *</span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB"> as</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> vscode</span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB"> from</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'vscode'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">export</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> function</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> activate</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">context</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">ExtensionContext</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    context</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">subscriptions</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">push</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">        vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">commands</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">registerCommand</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'myAmazingExtension.persistWorkspaceData'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">async</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> () </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">=&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">            if</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> (!</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">context</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">storageUri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">                return</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">            }</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">            // Create the extension's workspace storage folder if it doesn't already exist</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">            try</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">                // When folder doesn't exist, and error gets thrown</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">                await</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">workspace</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">fs</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">stat</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">context</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">storageUri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">            } </span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">catch</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">                // Create the extension's workspace storage folder</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">                await</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">workspace</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">fs</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">createDirectory</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">context</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">storageUri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">)</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">            }</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">            const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> workspaceData</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">Uri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">joinPath</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">context</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">storageUri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'workspace-data.json'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">            const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> writeData</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">new</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> TextEncoder</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">().</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">encode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1">JSON</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">stringify</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">({ </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">now:</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> Date</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">now</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">() }));</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">            vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">workspace</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">fs</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">writeFile</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">workspaceData</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">writeData</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">        }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    ));</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    context</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">subscriptions</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">push</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">        vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">commands</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">registerCommand</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'myAmazingExtension.persistGlobalData'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">async</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> () </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">=&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">        if</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> (!</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">context</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">globalStorageUri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">            return</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">        }</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">        // Create the extension's global (cross-workspace) folder if it doesn't already exist</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">        try</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">            // When folder doesn't exist, and error gets thrown</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">            await</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">workspace</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">fs</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">stat</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">context</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">globalStorageUri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">        } </span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">catch</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">            await</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">workspace</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">fs</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">createDirectory</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">context</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">globalStorageUri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">)</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">        }</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">        const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> workspaceData</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">Uri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">joinPath</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">context</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">globalStorageUri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'global-data.json'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">        const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> writeData</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">new</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> TextEncoder</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">().</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">encode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1">JSON</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">stringify</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">({ </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">now:</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> Date</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">now</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">() }));</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">        vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">workspace</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">fs</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">writeFile</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">workspaceData</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">writeData</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    ));</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<h3 id="sync-user-global-state-between-machines" data-needslink="sync-user-global-state-between-machines">Sync user global state between machines</h3>
<p>If your extension needs to preserve some user state across different machines then provide the state to <a href="/docs/configure/settings-sync">Settings Sync</a> using <code>vscode.ExtensionContext.globalState.setKeysForSync</code>. This can help prevent displaying the same welcome or updates page to users on multiple machines.</p>
<p>There is an example of using <code>setKeysforSync</code> in the <a href="/api/extension-capabilities/common-capabilities#data-storage">Extension Capabilities</a> topic.</p>
<h3 id="persisting-secrets" data-needslink="persisting-secrets">Persisting secrets</h3>
<p>If your extension needs to persist passwords or other secrets, you may want to use Visual Studio Code's <a href="https://code.visualstudio.com/api/references/vscode-api#SecretStorage">SecretStorage API</a> which provides a way to securely store text on the filesystem backed by encryption. For example, on desktop, we use Electron's <a href="https://www.electronjs.org/docs/latest/api/safe-storage" class="external-link" target="_blank">safeStorage API</a> to encrypt secrets before storing them on the filesystem. The API will always store the secrets on the client side but you can use this API regardless of where your extension is running and retrieve the same secret values.</p>
<blockquote><p><strong>Note</strong>: This API is the recommended way to persist passwords &amp; secrets. You should <strong>not</strong> store your secrets using <code>vscode.ExtensionContext.workspaceState</code> or <code>vscode.ExtensionContext.globalState</code> because these APIs store data in plaintext.</p>
</blockquote><p>Here's an example:</p>
<pre class="shiki" data-lang="typescript" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">import</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> *</span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB"> as</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> vscode</span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB"> from</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'vscode'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">export</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> function</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> activate</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">context</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">ExtensionContext</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">  // ...</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">  const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> myApiKey</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">context</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">secrets</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">get</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'apiKey'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">  // ...</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  context</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">secrets</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">delete</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'apiKey'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">  // ...</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  context</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">secrets</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">store</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'apiKey'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">myApiKey</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<h3 id="using-the-clipboard" data-needslink="using-the-clipboard">Using the clipboard</h3>
<p>Historically, extension authors have used Node.js modules such as <code>clipboardy</code> to interact with the clipboard. Unfortunately, if you use these modules in a Workspace Extension, they will use the remote clipboard instead of the user's local one. The VS Code clipboard API solves this problem. It is always run locally, regardless of the type of extension that calls it.</p>
<p>To use the VS Code clipboard API in an extension:</p>
<pre class="shiki" data-lang="typescript" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">import</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> *</span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB"> as</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> vscode</span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB"> from</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'vscode'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">export</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> function</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> activate</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">context</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">ExtensionContext</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  context</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">subscriptions</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">push</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">commands</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">registerCommand</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'myAmazingExtension.clipboardIt'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">async</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> () </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">=&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">      // Read from clipboard</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">      const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> text</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">await</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">env</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">clipboard</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">readText</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">();</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">      // Write to clipboard</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">      await</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">env</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">clipboard</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">writeText</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">        `It looks like you're copying "</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">${</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">text</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">". Would you like help?`</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      );</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    })</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  );</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<h3 id="opening-something-in-a-local-browser-or-application" data-needslink="opening-something-in-a-local-browser-or-application">Opening something in a local browser or application</h3>
<p>Spawning a process or using a module like <code>opn</code> to launch a browser or other application for particular URI can work well for local scenarios, but Workspace Extensions run remotely, which can cause the application to launch on the wrong side. VS Code Remote Development <strong>partially</strong> shims the <code>opn</code> node module to allow existing extensions to function. You can call the module with a URI and VS Code will cause the default application for the URI to appear on the client side. However, this is not a complete implementation, as options are not supported and a <code>child_process</code> object is not returned.</p>
<p>Instead of relying on a third-party node module, we recommend that extensions take advantage of the <code>vscode.env.openExternal</code> method to launch the default registered application on your local operating system for given URI. Even better, <code>vscode.env.openExternal</code> <strong>does automatic localhost port forwarding!</strong> You can use it to point to a local web server on a remote machine or codespace and serve up content even if that port is blocked externally.</p>
<blockquote><p><strong>Note:</strong> Currently the forwarding mechanism in the Codespaces browser-based editor only supports <strong>http and https requests</strong>. However, you can interact with any TCP connection when connecting to a codespace from VS Code.</p>
</blockquote><p>To use the <code>vscode.env.openExternal</code> API:</p>
<pre class="shiki" data-lang="typescript" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">import</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> *</span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB"> as</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> vscode</span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB"> from</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'vscode'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">export</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> async</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> function</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> activate</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">context</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">ExtensionContext</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  context</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">subscriptions</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">push</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">commands</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">registerCommand</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'myAmazingExtension.openExternal'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, () </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">=&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">      // Example 1 - Open the VS Code homepage in the default browser.</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">      vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">env</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">openExternal</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">Uri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">parse</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'https://code.visualstudio.com'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">));</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">      // Example 2 - Open an auto-forwarded localhost HTTP server.</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">      vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">env</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">openExternal</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">Uri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">parse</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'http://localhost:3000'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">));</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">      // Example 3 - Open the default email application.</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">      vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">env</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">openExternal</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">Uri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">parse</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'mailto:&lt;fill in your email here&gt;'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">));</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    })</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  );</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<h3 id="forwarding-localhost" data-needslink="forwarding-localhost">Forwarding localhost</h3>
<p>While the <a href="#_opening-something-in-a-local-browser-or-application">localhost forwarding mechanism in <code>vscode.env.openExternal</code> is useful</a>, there may also be situations where you want to forward something without actually launching a new browser window or application. This is where the <code>vscode.env.asExternalUri</code> API comes in.</p>
<blockquote><p><strong>Note:</strong> Currently the forwarding mechanism in the Codespaces browser-based editor only supports <strong>http and https requests</strong>. However, you can interact with any TCP connection when connecting to a codespace from VS Code.</p>
</blockquote><p>To use the <code>vscode.env.asExternalUri</code> API:</p>
<pre class="shiki" data-lang="typescript" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">import</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> *</span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB"> as</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> vscode</span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB"> from</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'vscode'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">import</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> { </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">getExpressServerPort</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> } </span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">from</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> './server'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">export</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> async</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> function</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> activate</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">context</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">ExtensionContext</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">    const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> dynamicServerPort</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">await</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> getWebServerPort</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">();</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    context</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">subscriptions</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">push</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">commands</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">registerCommand</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'myAmazingExtension.forwardLocalhost'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">async</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> () </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">=&gt;</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">        // Make the port available locally and get the full URI</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">        const</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> fullUri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">await</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">env</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">asExternalUri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">            vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">Uri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">parse</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">`http://localhost:</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">${</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">dynamicServerPort</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">`</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">));</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">        // ... do something with the fullUri ...</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    }));</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<p>It is important to note that the URI that is passed back by the API <strong>may not reference localhost at all</strong>, so you should use it in its entirety. This is particularly important for the Codespaces browser-based editor, where localhost cannot be used.</p>
<h3 id="callbacks-and-uri-handlers" data-needslink="callbacks-and-uri-handlers">Callbacks and URI handlers</h3>
<p>The <code>vscode.window.registerUriHandler</code> API allows your extension to register a custom URI that, if opened in a browser, will fire a callback function in your extension. A common use case for registering a URI handler is when implementing a service sign in with an <a href="https://oauth.net/2/" class="external-link" target="_blank">OAuth 2.0</a> authentication provider (for example, Azure AD). However, it can be used for any scenario where you want an external application or the browser to send information to your extension.</p>
<p>The Remote Development and Codespaces extensions in VS Code will transparently handle passing the URI to your extension regardless of where it is actually running (local or remote). However, <code>vscode://</code> URIs will not work with the Codespaces browser-based editor since opening these URIs in something like a browser would attempt to pass them to the local VS Code client rather than the browser-based editor. Fortunately, this can be easily remedied by using the <code>vscode.env.asExternalUri</code> API.</p>
<p>Let's use a combination of <code>vscode.window.registerUriHandler</code> and <code>vscode.env.asExternalUri</code> to wire up an example OAuth authentication callback:</p>
<pre class="shiki" data-lang="typescript" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">import</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> *</span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB"> as</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> vscode</span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB"> from</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'vscode'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">// This is ${publisher}.${name} from package.json</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> extensionId</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'my.amazing-extension'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">export</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> async</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> function</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> activate</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">context</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">ExtensionContext</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">  // Register a URI handler for the authentication callback</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">window</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">registerUriHandler</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">({</span></span>
<span class="line"><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">    handleUri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">uri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">Uri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">): </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">ProviderResult</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">&lt;</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">void</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">&gt; {</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">      // Add your code for what to do when the authentication completes here.</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">      if</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> (</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">uri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">path</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> === </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'/auth-complete'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">        vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">window</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">showInformationMessage</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'Sign in successful!'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  });</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">  // Register a sign in command</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  context</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">subscriptions</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">push</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">commands</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">registerCommand</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">`</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">${</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">extensionId</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">.signin`</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">async</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> () </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">=&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">      // Get an externally addressable callback URI for the handler that the authentication provider can use</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">      const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> callbackUri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">await</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">env</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">asExternalUri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">        vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">Uri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">parse</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">`</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">${</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">env</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">uriScheme</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">://</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">${</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">extensionId</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">/auth-complete`</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">)</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      );</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">      // Add your code to integrate with an authentication provider here - we'll fake it.</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">      vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">env</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">clipboard</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">writeText</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">callbackUri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">toString</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">());</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">      await</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">window</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">showInformationMessage</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">        'Open the URI copied to the clipboard in a browser window to authorize.'</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      );</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    })</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  );</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<p>When running this sample in VS Code, it wires up a <code>vscode://</code> or <code>vscode-insiders://</code> URI that can be used as a callback for an authentication provider. When running in the Codespaces browser-based editor, it wires up a <code>https://*.github.dev</code> URI without any code changes or special conditions.</p>
<p>While OAuth is outside the scope of this document, note that if you adapted this sample to a real authentication provider, you may need to build a proxy service in front of the provider. This is because not all providers allow <code>vscode://</code> callback URIs and others do not allow wildcard host names for callbacks over HTTPS. We also recommend using an <a href="https://oauth.net/2/pkce/" class="external-link" target="_blank">OAuth 2.0 Authorization Code with PKCE flow</a> wherever possible (for example, Azure AD supports PKCE) to improve the security of the callback.</p>
<h3 id="varying-behaviors-when-running-remotely-or-in-the-codespaces-browser-editor" data-needslink="varying-behaviors-when-running-remotely-or-in-the-codespaces-browser-editor">Varying behaviors when running remotely or in the Codespaces browser editor</h3>
<p>In some cases, your Workspace Extension may need to vary the behavior when running remotely. In others, you might want to vary its behavior when running in the Codespaces browser-based editor. VS Code provides three APIs to detect these situations: <code>vscode.env.uiKind</code>, <code>extension.extensionKind</code>, and <code>vscode.env.remoteName</code>.</p>
<p>Next, you can use the three APIs as follows:</p>
<pre class="shiki" data-lang="typescript" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">import</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> *</span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB"> as</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> vscode</span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB"> from</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'vscode'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">export</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> async</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> function</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> activate</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">context</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">ExtensionContext</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">  // extensionKind returns ExtensionKind.UI when running locally, so use this to detect remote</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">  const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> extension</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">extensions</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">getExtension</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'your.extensionId'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">  if</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> (</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">extension</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">extensionKind</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> === </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">ExtensionKind</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">Workspace</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">window</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">showInformationMessage</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'I am running remotely!'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  }</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">  // Codespaces browser-based editor will return UIKind.Web for uiKind</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">  if</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> (</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">env</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">uiKind</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> === </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">UIKind</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">Web</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">window</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">showInformationMessage</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'I am running in the Codespaces browser editor!'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  }</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">  // VS Code will return undefined for remoteName if working with a local workspace</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">  if</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> (</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">typeof</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">env</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">remoteName</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> === </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'undefined'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">window</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">showInformationMessage</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'Not currently connected to a remote workspace.'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<h3 id="communicating-between-extensions-using-commands" data-needslink="communicating-between-extensions-using-commands">Communicating between extensions using commands</h3>
<p>Some extensions return APIs as a part of their activation that are intended for use by other extensions (via <code>vscode.extension.getExtension(extensionName).exports</code>). While these will work if all extensions involved are on the same side (either all UI Extensions or all Workspace Extensions), these will not work between UI and Workspace Extensions.</p>
<p>Fortunately, VS Code automatically routes any executed commands to the correct extension regardless of its location. You can freely invoke any command (including those provided by other extensions) without worrying about impacts.</p>
<p>If you have a set of extensions that need to interact with one another, exposing functionality using a private command can help you avoid unexpected impacts. However, any objects you pass in as parameters will be "stringified" (<code>JSON.stringify</code>) before being transmitted, so the object cannot have cyclic references and will end up as a "plain old JavaScript object" on the other side.</p>
<p>For example:</p>
<pre class="shiki" data-lang="typescript" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">import</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> *</span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB"> as</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> vscode</span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB"> from</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'vscode'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">export</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> async</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> function</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> activate</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">context</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">ExtensionContext</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">  // Register the private echo command</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">  const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> echoCommand</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">commands</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">registerCommand</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">    '_private.command.called.echo'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    (</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">value</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">string</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">=&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">      return</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> value</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  );</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  context</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">subscriptions</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">push</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">echoCommand</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<p>See the <a href="/api/extension-guides/command">command API guide</a> for details on working with commands.</p>
<h2 id="using-the-webview-api" data-needslink="using-the-webview-api">Using the Webview API</h2>
<p>Like the clipboard API, the <a href="/api/extension-guides/webview">Webview API</a> is always run on the user's local machine or in the browser, even when used from a Workspace Extension. This means that many webview-based extensions should just work, even when used in remote workspaces or Codespaces. However, there are some considerations to be aware of so that your webview extension works properly when run remotely.</p>
<h3 id="always-use-aswebviewuri" data-needslink="always-use-aswebviewuri">Always use asWebviewUri</h3>
<p>You should use the <code>asWebviewUri</code> API to manage extension resources. Using this API instead of hard coding <code>vscode-resource://</code> URIs is required to ensure the Codespaces browser-based editor works with your extension. See the <a href="/api/extension-guides/webview">Webview API</a> guide for details, but here is a quick example.</p>
<p>You can use the API in your content as follows:</p>
<pre class="shiki" data-lang="typescript" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">// Create the webview</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> panel</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">window</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">createWebviewPanel</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">  'catWebview'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">  'Cat Webview'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">ViewColumn</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">One</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">// Get the content Uri</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> catGifUri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">panel</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">webview</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">asWebviewUri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">Uri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">joinPath</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">context</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">extensionUri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'media'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'cat.gif'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">)</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">// Reference it in your content</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">panel</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">webview</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">html</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">`&lt;!DOCTYPE html&gt;</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">&lt;html&gt;</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">&lt;body&gt;</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">    &lt;img src="</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">${</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">catGifUri</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">" width="300" /&gt;</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">&lt;/body&gt;</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">&lt;/html&gt;`</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"></span></code></pre>
<h3 id="use-the-message-passing-api-for-dynamic-webview-content" data-needslink="use-the-message-passing-api-for-dynamic-webview-content">Use the message passing API for dynamic webview content</h3>
<p>The VS Code webview includes a <a href="/api/extension-guides/webview#scripts-and-message-passing">message passing</a> API that allows you to dynamically update your webview content without the use of a local web server. Even if your extension is running some local web services that you want to interact with to update webview content, you can do this from the extension itself rather than directly from your HTML content.</p>
<p>This is an important pattern for Remote Development and GitHub Codespaces to ensure your webview code works in both VS Code and the Codespaces browser-based editor.</p>
<p><strong>Why message passing instead of a localhost web server?</strong></p>
<p>The alternate pattern is to serve up web content in an <code>iframe</code> or have webview content directly interact with a localhost server. Unfortunately, by default, <code>localhost</code> inside a webview will resolve to a developer's local machine. This means that for a remotely running workspace extension, the webviews it creates would not be able to access local servers spawned by the extension. Even if you use the IP of the machine, the ports you are connecting to will typically be blocked by default in a cloud VM or a container. Even if this worked in VS Code, it would not work in the Codespaces browser-based editor.</p>
<p>Here's an illustration of the problem when using the Remote - SSH extension, but the problem also exists for Dev Containers and GitHub Codespaces:</p>
<p><img src="/assets/api/advanced-topics/remote-extensions/webview-problem.png" alt="Webview problem" loading="lazy"></p>
<p>If possible, <strong>you should avoid doing this</strong> since it complicates your extension significantly. <a href="/api/extension-guides/webview#scripts-and-message-passing">Message passing</a> API can enable the same type of user experience without these types of headaches. The extension itself will be running in VS Code Server on the remote side, so it can transparently interact with any web servers your extension starts up as a result of any messages passed to it from the webview.</p>
<h3 id="workarounds-for-using-localhost-from-a-webview" data-needslink="workarounds-for-using-localhost-from-a-webview">Workarounds for using localhost from a webview</h3>
<p>If you can't use the <a href="/api/extension-guides/webview#scripts-and-message-passing">message passing</a> API for some reason, there are two options that will work with the Remote Development and GitHub Codespaces extensions in VS Code.</p>
<p>Each option allows webview content to route through the same channel VS Code uses to talk to VS Code Server. For example, if we update the illustration in the previous section for Remote - SSH, you would have this:</p>
<p><img src="/assets/api/advanced-topics/remote-extensions/webview-solution.png" alt="Webview Solution" loading="lazy"></p>
<h3 id="option-1-use-asexternaluri" data-needslink="option-1-use-asexternaluri">Option 1 - Use asExternalUri</h3>
<p>VS Code 1.40 introduced the <code>vscode.env.asExternalUri</code> API to allow extensions to forward local <code>http</code> and <code>https</code> requests remotely in a programmatic way. You can use this same API to forward requests to <code>localhost</code> web servers from the webview when your extension is running in VS Code.</p>
<p>Use the API to get a full URI for the iframe and add it to your HTML. You will also need to enable scripts in your webview and add a CSP to your HTML content.</p>
<pre class="shiki" data-lang="typescript" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">// Use asExternalUri to get the URI for the web server</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> dynamicWebServerPort</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">await</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> getWebServerPort</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">();</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> fullWebServerUri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">await</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">env</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">asExternalUri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">Uri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">parse</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">`http://localhost:</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">${</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">dynamicWebServerPort</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">`</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">)</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">// Create the webview</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> panel</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">window</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">createWebviewPanel</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">  'asExternalUriWebview'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">  'asExternalUri Example'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">ViewColumn</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">One</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    enableScripts:</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> true</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> cspSource</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">panel</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">webview</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">cspSource</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">panel</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">webview</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">html</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">`&lt;!DOCTYPE html&gt;</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">        &lt;head&gt;</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">            &lt;meta</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">                http-equiv="Content-Security-Policy"</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">                content="default-src 'none'; frame-src </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">${</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">fullWebServerUri</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> ${</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">cspSource</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> https:; img-src </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">${</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">cspSource</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> https:; script-src </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">${</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">cspSource</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">; style-src </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">${</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">cspSource</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">;"</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">            /&gt;</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">        &lt;/head&gt;</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">        &lt;body&gt;</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">        &lt;!-- All content from the web server must be in an iframe --&gt;</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">        &lt;iframe src="</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">${</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">fullWebServerUri</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"&gt;</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">    &lt;/body&gt;</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">    &lt;/html&gt;`</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"></span></code></pre>
<p>Note that any HTML content served up in the <code>iframe</code> in the example above <strong>needs to use relative pathing</strong> rather than hard coding <code>localhost</code>.</p>
<h3 id="option-2-use-a-port-mapping" data-needslink="option-2-use-a-port-mapping">Option 2 - Use a port mapping</h3>
<p>If you do <strong>not intend to support the Codespaces browser-based editor</strong>, you can use the <code>portMapping</code> option available in the webview API. (This approach will also work with Codespaces from the VS Code client, but not in the browser).</p>
<p>To use a port mapping, pass in a <code>portMapping</code> object when you create your webview:</p>
<pre class="shiki" data-lang="typescript" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> LOCAL_STATIC_PORT</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#B5CEA8;--shiki-light:#098658">3000</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> dynamicServerPort</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">await</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> getWebServerPort</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">();</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">// Create webview and pass portMapping in</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> panel</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">window</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">createWebviewPanel</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">  'remoteMappingExample'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">  'Remote Mapping Example'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">ViewColumn</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">One</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    portMapping:</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> [</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">      // This maps localhost:3000 in the webview to the web server port on the remote host.</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      { </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">webviewPort:</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> LOCAL_STATIC_PORT</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">extensionHostPort:</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> dynamicServerPort</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    ]</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">// Reference the port in any full URIs you reference in your HTML.</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">panel</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">webview</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">html</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">`&lt;!DOCTYPE html&gt;</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">    &lt;body&gt;</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">        &lt;!-- This will resolve to the dynamic server port on the remote machine --&gt;</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">        &lt;img src="http://localhost:</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">${</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1">LOCAL_STATIC_PORT</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">/canvas.png"&gt;</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">    &lt;/body&gt;</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">    &lt;/html&gt;`</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"></span></code></pre>
<p>In this example, in both the remote and local cases, any requests made to <code>http://localhost:3000</code> will automatically be mapped to the dynamic port an Express.js web server is running on.</p>
<h2 id="using-native-node.js-modules" data-needslink="using-native-node.js-modules">Using native Node.js modules</h2>
<p>Native modules bundled with (or dynamically acquired for) a VS Code extension must be recompiled <a href="https://electronjs.org/docs/tutorial/using-native-node-modules" class="external-link" target="_blank">using Electron's <code>electron-rebuild</code></a>. However, VS Code Server runs a standard (non-Electron) version of Node.js, which can cause binaries to fail when used remotely.</p>
<p>To solve this problem:</p>
<ol><li>Include (or dynamically acquire) both sets of binaries (Electron and standard Node.js) for the "modules" version in Node.js that VS Code ships.</li>
<li>Check to see if <code>vscode.extensions.getExtension('your.extensionId').extensionKind === vscode.ExtensionKind.Workspace</code> to set up the correct binaries based on whether the extension is running remotely or locally.</li>
<li>You may also want to add support for non-x86_64 targets and Alpine Linux at the same time by <a href="#_supporting-nonx8664-hosts-or-alpine-linux-containers">following similar logic</a>.</li>
</ol><p>You can find the "modules" version VS Code uses by going to <strong>Help &gt; Developer Tools</strong> and typing <code>process.versions.modules</code> in the console. However, to make sure native modules work seamlessly in different Node.js environments, you may want to compile the native modules against all possible Node.js "modules" versions and platforms you want support (Electron Node.js, official Node.js Windows/Darwin/Linux, all versions). The <a href="https://github.com/tree-sitter/node-tree-sitter/releases/tag/v0.14.0" class="external-link" target="_blank">node-tree-sitter</a> module is a good example of a module that does this well.</p>
<h2 id="supporting-nonx8664-hosts-or-alpine-linux-containers" data-needslink="supporting-nonx8664-hosts-or-alpine-linux-containers">Supporting non-x86_64 hosts or Alpine Linux containers</h2>
<p>If your extension is purely written in JavaScript/TypeScript, you may not need to do anything to add support for other processor architectures or the <code>musl</code> based Alpine Linux to your extension.</p>
<p>However, if your extension works on Debian 9+, Ubuntu 16.04+, or RHEL / CentOS 7+ remote SSH hosts, containers, or WSL, but fails on supported non-x86_64 hosts (for example ARMv7l) or Alpine Linux containers, the extension may include x86_64 <code>glibc</code> specific native code or runtimes that will fail on these architectures/operating systems.</p>
<p>For example, your extension may only include x86_64 compiled versions of native modules or runtimes. For Alpine Linux, the included native code or runtimes may not work due to <a href="https://wiki.musl-libc.org/functional-differences-from-glibc.html" class="external-link" target="_blank">fundamental differences</a> between how <code>libc</code> is implemented in Alpine Linux (<code>musl</code>) and other distributions (<code>glibc</code>).</p>
<p>To resolve this problem:</p>
<ol><li>
<p>If you are dynamically acquiring compiled code, you can add support by detecting non-x86_64 targets using <code>process.arch</code> and downloading versions compiled for the right architecture. If you are including binaries for all supported architectures inside your extension instead, you can use this logic to use the correct one.</p>
</li>
<li>
<p>For Alpine Linux, you can detect the operating system using  <code>await fs.exists('/etc/alpine-release')</code> and once again download or use the correct binaries for a <code>musl</code> based operating system.</p>
</li>
<li>
<p>If you'd prefer not to support these platforms, you can use the same logic to provide a good error message instead.</p>
</li>
</ol><p>It is important to note that some third-party npm modules include native code that can cause this problem. So, in some cases you may need to work with the npm module author to add additional compilation targets.</p>
<h2 id="avoid-using-electron-modules" data-needslink="avoid-using-electron-modules">Avoid using Electron modules</h2>
<p>While it can be convenient to rely on built-in Electron or VS Code modules not exposed by the extension API, it's important to note that VS Code Server runs a standard (non-Electron) version of Node.js. These modules will be missing when running remotely. There are a few exceptions, where there is specific code in place to make them work.</p>
<p>Use base Node.js modules or modules in your extension VSIX to avoid these problems. If you absolutely have to use an Electron module, be sure to have a fallback if the module is missing.</p>
<p>The example below will use the Electron <code>original-fs</code> node module if found, and fall back to the base Node.js <code>fs</code> module if not.</p>
<pre class="shiki" data-lang="typescript" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">function</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> requireWithFallback</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">electronModule</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">string</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">nodeModule</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">string</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">  try</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">    return</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> require</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">electronModule</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  } </span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">catch</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> (</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">err</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {}</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">  return</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> require</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">nodeModule</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> fs</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">requireWithFallback</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'original-fs'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'fs'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"></span></code></pre>
<p>Try to avoid these situations whenever possible.</p>
<h2 id="known-issues" data-needslink="known-issues">Known issues</h2>
<p>There are a few extension problems that could be resolved with some added functionality for Workspace Extensions. The following table is a list of known issues under consideration:</p>
<table class="table table-striped"><thead><tr><th>Problem</th>
<th>Description</th>
</tr></thead><tbody><tr><td><strong>Cannot access attached devices from Workspace extension</strong></td>
<td>Extensions that access locally attached devices will be unable to connect to them when running remotely. One approach to overcome this is to create a companion UI extension whose job is to access the attached device and offers commands that the remote extension can invoke too. <br> Another approach is reverse tunneling, which is being tracked in a <a href="https://github.com/microsoft/vscode/issues/100222" class="external-link" target="_blank">VS Code repo issue</a>.</td>
</tr></tbody></table><h2 id="questions-and-feedback" data-needslink="questions-and-feedback">Questions and feedback</h2>
<ul><li>See <a href="/docs/remote/troubleshooting">Tips and Tricks</a> or the <a href="/docs/remote/faq">FAQ</a>.</li>
<li>Search for answers on <a href="https://stackoverflow.com/questions/tagged/vscode-remote" class="external-link" target="_blank">Stack Overflow</a>.</li>
<li><a href="https://aka.ms/vscode-remote/feature-requests" class="external-link" target="_blank">Upvote a feature or request a new one</a>, search <a href="https://aka.ms/vscode-remote/issues" class="external-link" target="_blank">existing issues</a>, or <a href="https://aka.ms/vscode-remote/issues/new" class="external-link" target="_blank">report a problem</a>.</li>
<li>Create a <a href="https://containers.dev/templates" class="external-link" target="_blank">development container Template</a> or <a href="https://containers.dev/features" class="external-link" target="_blank">Feature</a> for others to use.</li>
<li>Contribute to <a href="https://github.com/microsoft/vscode-docs" class="external-link" target="_blank">our documentation</a> or <a href="https://github.com/microsoft/vscode" class="external-link" target="_blank">VS Code</a>.</li>
<li>See our <a href="https://aka.ms/vscode-remote/contributing" class="external-link" target="_blank">CONTRIBUTING</a> guide for details.</li>
</ul><div class="feedback" data-edit-url="https://vscode.dev/github/microsoft/vscode-docs/blob/main/api/advanced-topics/remote-extensions.md"></div>
				
				<div class="body-footer">6/3/2026</div>
				
            </main><aside class="docs-right-sidebar hidden-xs"><div class="docs-markdown-actions">
                    <div class="docs-markdown-dropdown" data-raw-url="/raw/api/advanced-topics/remote-extensions.md">
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
                <nav id="docs-subnavbar" aria-label="On Page"><h4><span class="sr-only">On this page there are 11 sections</span><span aria-hidden="true">On this page</span></h4>
                    <ul class="nav"><li><a href="#architecture-and-extension-kinds">Architecture and extension kinds</a></li>
                        
                        <li><a href="#debugging-extensions">Debugging Extensions</a></li>
                        
                        <li><a href="#installing-a-development-version-of-your-extension">Installing a development version of your extension</a></li>
                        
                        <li><a href="#handling-dependencies-with-remote-extensions">Handling dependencies with remote extensions</a></li>
                        
                        <li><a href="#common-problems">Common problems</a></li>
                        
                        <li><a href="#using-the-webview-api">Using the Webview API</a></li>
                        
                        <li><a href="#using-native-node.js-modules">Using native Node.js modules</a></li>
                        
                        <li><a href="#supporting-nonx8664-hosts-or-alpine-linux-containers">Supporting non-x86_64 hosts or Alpine Linux containers</a></li>
                        
                        <li><a href="#avoid-using-electron-modules">Avoid using Electron modules</a></li>
                        
                        <li><a href="#known-issues">Known issues</a></li>
                        
                        <li><a href="#questions-and-feedback">Questions and feedback</a></li>
                        
                    </ul></nav></aside></div>
		<div class="docs-mobile-widgets visible-xs">
			<div class="connect-widget"></div>
		</div>
	</div>
</div>
		</main>