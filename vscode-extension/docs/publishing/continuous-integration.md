# Continuous Integration

> 源文档: [https://code.visualstudio.com/api/working-with-extensions/continuous-integration](https://code.visualstudio.com/api/working-with-extensions/continuous-integration)

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
			    
			<li class="panel active expanded">
			  <a class="area" role="button" href="#working-with-extensions-articles" data-parent="#main-nav" data-toggle="collapse">Testing and Publishing</a>
			  <ul id="working-with-extensions-articles" class="collapse in"><li>
			          <a href="/api/working-with-extensions/testing-extension">Testing Extensions</a>
			        </li>
			          
			        <li>
			          <a href="/api/working-with-extensions/publishing-extension">Publishing Extensions</a>
			        </li>
			          
			        <li>
			          <a href="/api/working-with-extensions/bundling-extension">Bundling Extensions</a>
			        </li>
			          
			        <li class="active">
			          <a href="/api/working-with-extensions/continuous-integration" aria-label="Current Page: Continuous Integration">Continuous Integration</a>
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
				<select id="small-nav-dropdown" aria-label="topics"><option value="/api">Overview</option><optgroup label="Get Started"><option value="/api/get-started/your-first-extension">Your First Extension</option><option value="/api/get-started/extension-anatomy">Extension Anatomy</option><option value="/api/get-started/wrapping-up">Wrapping Up</option></optgroup><optgroup label="Extension Capabilities"><option value="/api/extension-capabilities/overview">Overview</option><option value="/api/extension-capabilities/common-capabilities">Common Capabilities</option><option value="/api/extension-capabilities/theming">Theming</option><option value="/api/extension-capabilities/extending-workbench">Extending Workbench</option></optgroup><optgroup label="Extension Guides"><option value="/api/extension-guides/overview">Overview</option><optgroup label="Extension Guides - AI"><option value="/api/extension-guides/ai/ai-extensibility-overview">AI Extensibility</option><option value="/api/extension-guides/ai/tools">Language Model Tool</option><option value="/api/extension-guides/ai/mcp">MCP Dev Guide</option><option value="/api/extension-guides/ai/chat">Chat Participant</option><option value="/api/extension-guides/ai/chat-tutorial">Chat Tutorial</option><option value="/api/extension-guides/ai/language-model">Language Model</option><option value="/api/extension-guides/ai/language-model-tutorial">Language Model Tutorial</option><option value="/api/extension-guides/ai/language-model-chat-provider">Language Model Chat Provider</option><option value="/api/extension-guides/ai/prompt-tsx">Prompt TSX</option></optgroup><option value="/api/extension-guides/command">Command</option><option value="/api/extension-guides/color-theme">Color Theme</option><option value="/api/extension-guides/file-icon-theme">File Icon Theme</option><option value="/api/extension-guides/product-icon-theme">Product Icon Theme</option><option value="/api/extension-guides/tree-view">Tree View</option><option value="/api/extension-guides/webview">Webview</option><option value="/api/extension-guides/notebook">Notebook</option><option value="/api/extension-guides/custom-editors">Custom Editors</option><option value="/api/extension-guides/virtual-documents">Virtual Documents</option><option value="/api/extension-guides/virtual-workspaces">Virtual Workspaces</option><option value="/api/extension-guides/web-extensions">Web Extensions</option><option value="/api/extension-guides/workspace-trust">Workspace Trust</option><option value="/api/extension-guides/task-provider">Task Provider</option><option value="/api/extension-guides/scm-provider">Source Control</option><option value="/api/extension-guides/debugger-extension">Debugger Extension</option><option value="/api/extension-guides/markdown-extension">Markdown Extension</option><option value="/api/extension-guides/testing">Test Extension</option><option value="/api/extension-guides/custom-data-extension">Custom Data Extension</option><option value="/api/extension-guides/telemetry">Telemetry</option></optgroup><optgroup label="UX Guidelines"><option value="/api/ux-guidelines/overview">Overview</option><option value="/api/ux-guidelines/activity-bar">Activity Bar</option><option value="/api/ux-guidelines/sidebars">Sidebars</option><option value="/api/ux-guidelines/panel">Panel</option><option value="/api/ux-guidelines/status-bar">Status Bar</option><option value="/api/ux-guidelines/views">Views</option><option value="/api/ux-guidelines/editor-actions">Editor Actions</option><option value="/api/ux-guidelines/quick-picks">Quick Picks</option><option value="/api/ux-guidelines/command-palette">Command Palette</option><option value="/api/ux-guidelines/notifications">Notifications</option><option value="/api/ux-guidelines/webviews">Webviews</option><option value="/api/ux-guidelines/context-menus">Context Menus</option><option value="/api/ux-guidelines/walkthroughs">Walkthroughs</option><option value="/api/ux-guidelines/settings">Settings</option></optgroup><optgroup label="Language Extensions"><option value="/api/language-extensions/overview">Overview</option><option value="/api/language-extensions/syntax-highlight-guide">Syntax Highlight Guide</option><option value="/api/language-extensions/semantic-highlight-guide">Semantic Highlight Guide</option><option value="/api/language-extensions/snippet-guide">Snippet Guide</option><option value="/api/language-extensions/language-configuration-guide">Language Configuration Guide</option><option value="/api/language-extensions/programmatic-language-features">Programmatic Language Features</option><option value="/api/language-extensions/language-server-extension-guide">Language Server Extension Guide</option><option value="/api/language-extensions/embedded-languages">Embedded Languages</option></optgroup><optgroup label="Testing and Publishing"><option value="/api/working-with-extensions/testing-extension">Testing Extensions</option><option value="/api/working-with-extensions/publishing-extension">Publishing Extensions</option><option value="/api/working-with-extensions/bundling-extension">Bundling Extensions</option><option value="/api/working-with-extensions/continuous-integration" selected>Continuous Integration</option></optgroup><optgroup label="Advanced Topics"><option value="/api/advanced-topics/extension-host">Extension Host</option><option value="/api/advanced-topics/remote-extensions">Remote Development and Codespaces</option><option value="/api/advanced-topics/using-proposed-api">Using Proposed API</option><option value="/api/advanced-topics/tslint-eslint-migration">Migrate from TSLint to ESLint</option><option value="/api/advanced-topics/python-extension-template">Python Extension Template</option></optgroup><optgroup label="References"><option value="/api/references/vscode-api">VS Code API</option><option value="/api/references/contribution-points">Contribution Points</option><option value="/api/references/activation-events">Activation Events</option><option value="/api/references/extension-manifest">Extension Manifest</option><option value="/api/references/commands">Built-In Commands</option><option value="/api/references/when-clause-contexts">When Clause Contexts</option><option value="/api/references/theme-color">Theme Color</option><option value="/api/references/icons-in-labels">Product Icon Reference</option><option value="/api/references/document-selector">Document Selector</option></optgroup></select></nav></aside><div class="docs-content-wrapper">
			
			<main class="docs-main-content body"><h1>Continuous Integration</h1>
<p>Extension integration tests can be run on CI services. The <a href="https://github.com/microsoft/vscode-test" class="external-link" target="_blank"><code>@vscode/test-electron</code></a> library helps you set up extension tests on CI providers and contains a <a href="https://github.com/microsoft/vscode-test/tree/main/sample" class="external-link" target="_blank">sample extension</a> setup on Azure Pipelines. You can check out the <a href="https://dev.azure.com/vscode/vscode-test/_build?definitionId=15" class="external-link" target="_blank">build pipeline</a> or jump directly to the <a href="https://github.com/microsoft/vscode-test/blob/main/sample/azure-pipelines.yml" class="external-link" target="_blank"><code>azure-pipelines.yml</code> file</a>.</p>
<h2 id="automated-publishing" data-needslink="automated-publishing">Automated publishing</h2>
<p>You can also configure the CI to publish a new version of the extension automatically.</p>
<p>The publish command is similar to publishing from a local environment using <a href="https://github.com/microsoft/vscode-vsce" class="external-link" target="_blank"><code>vsce</code></a>, but you must somehow provide the Personal Access Token (PAT) in a secure way. By storing the PAT as a <code>VSCE_PAT</code> <strong>secret variable</strong>, <code>vsce</code> will be able to use it. Secret variables are never exposed, so they are safe to use in a CI pipeline.</p>
<h2 id="azure-pipelines" data-needslink="azure-pipelines">Azure Pipelines</h2>
<p><a href="https://azure.microsoft.com/services/devops/"><img alt="Azure Pipelines" src="/assets/api/working-with-extensions/continuous-integration/pipelines-logo.png" width="318"></a></p>
<p><a href="https://azure.microsoft.com/services/devops/pipelines/" class="external-link" target="_blank">Azure Pipelines</a> is great for running VS Code extension tests as it supports running the tests on Windows, macOS, and Linux. For Open Source projects, you get unlimited minutes and 10 free parallel jobs. This section explains how to set up an Azure Pipelines for running your extension tests.</p>
<p>First, create a free account on <a href="https://azure.microsoft.com/services/devops/" class="external-link" target="_blank">Azure DevOps</a> and create an <a href="https://azure.microsoft.com/features/devops-projects/" class="external-link" target="_blank">Azure DevOps project</a> for your extension.</p>
<p>Then, add the following <code>azure-pipelines.yml</code> file to the root of your extension's repository. Other than the <code>xvfb</code> setup script for Linux that is necessary to run VS Code in headless Linux CI machines, the definition is straight-forward:</p>
<pre class="shiki" data-lang="yaml" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#800000">trigger</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">:</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#800000">  branches</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">:</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#800000">    include</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">:</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    - </span><span style="--shiki-dark:#CE9178;--shiki-light:#0000FF">main</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#800000">  tags</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">:</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#800000">    include</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">:</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    - </span><span style="--shiki-dark:#CE9178;--shiki-light:#0000FF">v*</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#800000">strategy</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">:</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#800000">  matrix</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">:</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#800000">    linux</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">:</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#800000">      imageName</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#0000FF">'ubuntu-latest'</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#800000">    mac</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">:</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#800000">      imageName</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#0000FF">'macos-latest'</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#800000">    windows</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">:</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#800000">      imageName</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#0000FF">'windows-latest'</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#800000">pool</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">:</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#800000">  vmImage</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#0000FF">$(imageName)</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#800000">steps</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">:</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">- </span><span style="--shiki-dark:#569CD6;--shiki-light:#800000">task</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#0000FF">NodeTool@0</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#800000">  inputs</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">:</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#800000">    versionSpec</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#0000FF">'10.x'</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#800000">  displayName</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#0000FF">'Install Node.js'</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">- </span><span style="--shiki-dark:#569CD6;--shiki-light:#800000">bash</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">|</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#0000FF">    /usr/bin/Xvfb :99 -screen 0 1024x768x24 &gt; /dev/null 2&gt;&amp;1 &amp;</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#0000FF">    echo "&gt;&gt;&gt; Started xvfb"</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#800000">  displayName</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#0000FF">Start xvfb</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#800000">  condition</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#0000FF">and(succeeded(), eq(variables['Agent.OS'], 'Linux'))</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">- </span><span style="--shiki-dark:#569CD6;--shiki-light:#800000">bash</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">|</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#0000FF">    echo "&gt;&gt;&gt; Compile vscode-test"</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#0000FF">    yarn &amp;&amp; yarn compile</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#0000FF">    echo "&gt;&gt;&gt; Compiled vscode-test"</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#0000FF">    cd sample</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#0000FF">    echo "&gt;&gt;&gt; Run sample integration test"</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#0000FF">    yarn &amp;&amp; yarn compile &amp;&amp; yarn test</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#800000">  displayName</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#0000FF">Run Tests</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#800000">  env</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">:</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#800000">    DISPLAY</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#0000FF">':99.0'</span></span>
<span class="line"></span></code></pre>
<p>Finally, <a href="https://learn.microsoft.com/azure/devops/pipelines/create-first-pipeline" class="external-link" target="_blank">create a new pipeline</a> in your DevOps project and point it to the <code>azure-pipelines.yml</code> file. Trigger a build and voilà:</p>
<p><img src="/assets/api/working-with-extensions/continuous-integration/pipelines.png" alt="pipelines" loading="lazy"></p>
<p>You can enable the build to run continuously when pushing to a branch and even on pull requests. See <a href="https://learn.microsoft.com/azure/devops/pipelines/build/triggers" class="external-link" target="_blank">Build pipeline triggers</a> to learn more.</p>
<h3 id="azure-pipelines-automated-publishing" data-needslink="azure-pipelines-automated-publishing">Azure Pipelines automated publishing</h3>
<ol><li>Set up <code>VSCE_PAT</code> as a secret variable using the <a href="https://learn.microsoft.com/azure/devops/pipelines/process/variables?tabs=classic%2Cbatch#secret-variables" class="external-link" target="_blank">Azure DevOps secrets instructions</a>.</li>
<li>Install <code>vsce</code> as a <code>devDependencies</code> (<code>npm install @vscode/vsce --save-dev</code> or <code>yarn add @vscode/vsce --dev</code>).</li>
<li>Declare a <code>deploy</code> script in <code>package.json</code> without the PAT (by default, <code>vsce</code> will use the <code>VSCE_PAT</code> environment variable as the Personal Access Token).</li>
</ol><pre class="shiki" data-lang="json" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"scripts"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "deploy"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"vsce publish --yarn"</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<ol start="4"><li>Configure the CI so the build will also run when tags are created:</li>
</ol><pre class="shiki" data-lang="yaml" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#800000">trigger</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">:</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#800000">  branches</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">:</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#800000">    include</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">:</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    - </span><span style="--shiki-dark:#CE9178;--shiki-light:#0000FF">main</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#800000">  tags</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">:</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#800000">    include</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">:</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    - </span><span style="--shiki-dark:#CE9178;--shiki-light:#0000FF">refs/tags/v*</span></span>
<span class="line"></span></code></pre>
<ol start="5"><li>Add a <code>publish</code> step in <code>azure-pipelines.yml</code> that calls <code>yarn deploy</code> with the secret variable.</li>
</ol><pre class="shiki" data-lang="yaml" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">- </span><span style="--shiki-dark:#569CD6;--shiki-light:#800000">bash</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">|</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#0000FF">    echo "&gt;&gt;&gt; Publish"</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#0000FF">    yarn deploy</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#800000">  displayName</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#0000FF">Publish</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#800000">  condition</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#0000FF">and(succeeded(), startsWith(variables['Build.SourceBranch'], 'refs/tags/'), eq(variables['Agent.OS'], 'Linux'))</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#800000">  env</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">:</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#800000">    VSCE_PAT</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#0000FF">$(VSCE_PAT)</span></span>
<span class="line"></span></code></pre>
<p>The <a href="https://learn.microsoft.com/azure/devops/pipelines/process/conditions" class="external-link" target="_blank">condition</a> property tells the CI to run the publish step only in certain cases.</p>
<p>In our example, the condition has three checks:</p>
<ul><li><code>succeeded()</code> - Publish only if the tests pass.</li>
<li><code>startsWith(variables['Build.SourceBranch'], 'refs/tags/')</code> - Publish only if a tagged (release) build.</li>
<li><code>eq(variables['Agent.OS'], 'Linux')</code> - Include if your build runs on multiple agents (Windows, Linux, etc.). If not, remove that part of the condition.</li>
</ul><p>Since <code>VSCE_PAT</code> is a secret variable, it is not immediately usable as an environment variable. Thus, we need to explicitly map the environment variable <code>VSCE_PAT</code> to the secret variable.</p>
<h2 id="github-actions" data-needslink="github-actions">GitHub Actions</h2>
<p>You can also configure GitHub Actions to run your extension CI. In headless Linux CI machines <code>xvfb</code> is required to run VS Code, so if Linux is the current OS run the tests in an Xvfb enabled environment:</p>
<pre class="shiki" data-lang="yaml" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">on</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">:</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#800000">  push</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">:</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#800000">    branches</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">:</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      - </span><span style="--shiki-dark:#CE9178;--shiki-light:#0000FF">main</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#800000">jobs</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">:</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#800000">  build</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">:</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#800000">    strategy</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">:</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#800000">      matrix</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">:</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#800000">        os</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span><span style="--shiki-dark:#CE9178;--shiki-light:#0000FF">macos-latest</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#CE9178;--shiki-light:#0000FF">ubuntu-latest</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#CE9178;--shiki-light:#0000FF">windows-latest</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">]</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#800000">    runs-on</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#0000FF">${{ matrix.os }}</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#800000">    steps</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">:</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    - </span><span style="--shiki-dark:#569CD6;--shiki-light:#800000">name</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#0000FF">Checkout</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#800000">      uses</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#0000FF">actions/checkout@v4</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    - </span><span style="--shiki-dark:#569CD6;--shiki-light:#800000">name</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#0000FF">Install Node.js</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#800000">      uses</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#0000FF">actions/setup-node@v4</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#800000">      with</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">:</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#800000">        node-version</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#0000FF">18.x</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    - </span><span style="--shiki-dark:#569CD6;--shiki-light:#800000">run</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#0000FF">npm install</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    - </span><span style="--shiki-dark:#569CD6;--shiki-light:#800000">run</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#0000FF">xvfb-run -a npm test</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#800000">      if</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#0000FF">runner.os == 'Linux'</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    - </span><span style="--shiki-dark:#569CD6;--shiki-light:#800000">run</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#0000FF">npm test</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#800000">      if</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#0000FF">runner.os != 'Linux'</span></span>
<span class="line"></span></code></pre>
<h3 id="github-actions-automated-publishing" data-needslink="github-actions-automated-publishing">GitHub Actions automated publishing</h3>
<ol><li>Set up <code>VSCE_PAT</code> as an encrypted secret using the <a href="https://docs.github.com/actions/security-guides/encrypted-secrets#creating-encrypted-secrets-for-a-repository" class="external-link" target="_blank">GitHub Actions secrets instructions</a>.</li>
<li>Install <code>vsce</code> as a <code>devDependencies</code> (<code>npm install @vscode/vsce --save-dev</code> or <code>yarn add @vscode/vsce --dev</code>).</li>
<li>Declare a <code>deploy</code> script in <code>package.json</code> without the PAT.</li>
</ol><pre class="shiki" data-lang="json" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"scripts"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "deploy"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"vsce publish --yarn"</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<ol start="4"><li>Configure the CI so the build will also run when tags are created:</li>
</ol><pre class="shiki" data-lang="yaml" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">on</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">:</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#800000">  push</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">:</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#800000">    branches</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">:</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    - </span><span style="--shiki-dark:#CE9178;--shiki-light:#0000FF">main</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#800000">  release</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">:</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#800000">    types</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">:</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    - </span><span style="--shiki-dark:#CE9178;--shiki-light:#0000FF">created</span></span>
<span class="line"></span></code></pre>
<ol start="5"><li>Add a <code>publish</code> job to the pipeline that calls <code>npm run deploy</code> with the secret variable.</li>
</ol><pre class="shiki" data-lang="yaml" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">- </span><span style="--shiki-dark:#569CD6;--shiki-light:#800000">name</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#0000FF">Publish</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#800000">  if</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#0000FF">success() &amp;&amp; startsWith(github.ref, 'refs/tags/') &amp;&amp; matrix.os == 'ubuntu-latest'</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#800000">  run</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#0000FF">npm run deploy</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#800000">  env</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">:</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#800000">    VSCE_PAT</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#0000FF">${{ secrets.VSCE_PAT }}</span></span>
<span class="line"></span></code></pre>
<p>The <a href="https://docs.github.com/actions/using-workflows/workflow-syntax-for-github-actions#jobsjob_idif" class="external-link" target="_blank">if</a> property tells the CI to run the publish step only in certain cases.</p>
<p>In our example, the condition has three checks:</p>
<ul><li><code>success()</code> - Publish only if the tests pass.</li>
<li><code>startsWith(github.ref, 'refs/tags/')</code> - Publish only if a tagged (release) build.</li>
<li><code>matrix.os == 'ubuntu-latest'</code> - Include if your build runs on multiple agents (Windows, Linux, etc.). If not, remove that part of the condition.</li>
</ul><h2 id="gitlab-ci" data-needslink="gitlab-ci">GitLab CI</h2>
<p>GitLab CI can be used to test and publish the extension in headless Docker containers. This can be done by pulling a preconfigured Docker image, or installing <code>xvfb</code> and the libraries required to run Visual Studio Code during the pipeline.</p>
<pre class="shiki" data-lang="yaml" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#800000">image</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#0000FF">node:12-buster</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#800000">before_script</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">:</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  - </span><span style="--shiki-dark:#CE9178;--shiki-light:#0000FF">npm install</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#800000">test</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">:</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#800000">  script</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">:</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    - </span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">|</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#0000FF">      apt update</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#0000FF">      apt install -y libasound2 libgbm1 libgtk-3-0 libnss3 xvfb</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#0000FF">      xvfb-run -a npm run test</span></span>
<span class="line"></span></code></pre>
<h3 id="gitlab-ci-automated-publishing" data-needslink="gitlab-ci-automated-publishing">GitLab CI automated publishing</h3>
<ol><li>Set up <code>VSCE_PAT</code> as a masked variable using the <a href="https://docs.gitlab.com/ee/ci/variables/README.html#mask-a-cicd-variable" class="external-link" target="_blank">GitLab CI documentation</a>.</li>
<li>Install <code>vsce</code> as a <code>devDependencies</code> (<code>npm install @vscode/vsce --save-dev</code> or <code>yarn add @vscode/vsce --dev</code>).</li>
<li>Declare a <code>deploy</code> script in <code>package.json</code> without the PAT.</li>
</ol><pre class="shiki" data-lang="json" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"scripts"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "deploy"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"vsce publish --yarn"</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<ol start="4"><li>Add a <code>deploy</code> job that calls <code>npm run deploy</code> with the masked variable which will only trigger on tags.</li>
</ol><pre class="shiki" data-lang="yaml" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#800000">deploy</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">:</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#800000">  only</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">:</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    - </span><span style="--shiki-dark:#CE9178;--shiki-light:#0000FF">tags</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#800000">  script</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">:</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    - </span><span style="--shiki-dark:#CE9178;--shiki-light:#0000FF">npm run deploy</span></span>
<span class="line"></span></code></pre>
<h2 id="common-questions" data-needslink="common-questions">Common questions</h2>
<h3 id="do-i-need-to-use-yarn-for-continuous-integration" data-needslink="do-i-need-to-use-yarn-for-continuous-integration">Do I need to use Yarn for continuous integration?</h3>
<p>All of the above examples refer to a hypothetical project built with <a href="https://yarnpkg.com/" class="external-link" target="_blank">Yarn</a>, but can be adapted to use <a href="https://www.npmjs.com/" class="external-link" target="_blank">npm</a>, <a href="https://gruntjs.com/" class="external-link" target="_blank">Grunt</a>, <a href="https://gulpjs.com/" class="external-link" target="_blank">Gulp</a>, or any other JavaScript build tool.</p>

				<div class="feedback" data-edit-url="https://vscode.dev/github/microsoft/vscode-docs/blob/main/api/working-with-extensions/continuous-integration.md"></div>
				
				<div class="body-footer">6/3/2026</div>
				
            </main><aside class="docs-right-sidebar hidden-xs"><div class="docs-markdown-actions">
                    <div class="docs-markdown-dropdown" data-raw-url="/raw/api/working-with-extensions/continuous-integration.md">
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
                <nav id="docs-subnavbar" aria-label="On Page"><h4><span class="sr-only">On this page there are 5 sections</span><span aria-hidden="true">On this page</span></h4>
                    <ul class="nav"><li><a href="#automated-publishing">Automated publishing</a></li>
                        
                        <li><a href="#azure-pipelines">Azure Pipelines</a></li>
                        
                        <li><a href="#github-actions">GitHub Actions</a></li>
                        
                        <li><a href="#gitlab-ci">GitLab CI</a></li>
                        
                        <li><a href="#common-questions">Common questions</a></li>
                        
                    </ul></nav></aside></div>
		<div class="docs-mobile-widgets visible-xs">
			<div class="connect-widget"></div>
		</div>
	</div>
</div>
		</main>