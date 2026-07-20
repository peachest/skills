# Workspace Trust Extension Guide

> 源文档: [https://code.visualstudio.com/api/extension-guides/workspace-trust](https://code.visualstudio.com/api/extension-guides/workspace-trust)

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
			          
			        <li class="active">
			          <a href="/api/extension-guides/workspace-trust" aria-label="Current Page: Workspace Trust">Workspace Trust</a>
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
				<select id="small-nav-dropdown" aria-label="topics"><option value="/api">Overview</option><optgroup label="Get Started"><option value="/api/get-started/your-first-extension">Your First Extension</option><option value="/api/get-started/extension-anatomy">Extension Anatomy</option><option value="/api/get-started/wrapping-up">Wrapping Up</option></optgroup><optgroup label="Extension Capabilities"><option value="/api/extension-capabilities/overview">Overview</option><option value="/api/extension-capabilities/common-capabilities">Common Capabilities</option><option value="/api/extension-capabilities/theming">Theming</option><option value="/api/extension-capabilities/extending-workbench">Extending Workbench</option></optgroup><optgroup label="Extension Guides"><option value="/api/extension-guides/overview">Overview</option><optgroup label="Extension Guides - AI"><option value="/api/extension-guides/ai/ai-extensibility-overview">AI Extensibility</option><option value="/api/extension-guides/ai/tools">Language Model Tool</option><option value="/api/extension-guides/ai/mcp">MCP Dev Guide</option><option value="/api/extension-guides/ai/chat">Chat Participant</option><option value="/api/extension-guides/ai/chat-tutorial">Chat Tutorial</option><option value="/api/extension-guides/ai/language-model">Language Model</option><option value="/api/extension-guides/ai/language-model-tutorial">Language Model Tutorial</option><option value="/api/extension-guides/ai/language-model-chat-provider">Language Model Chat Provider</option><option value="/api/extension-guides/ai/prompt-tsx">Prompt TSX</option></optgroup><option value="/api/extension-guides/command">Command</option><option value="/api/extension-guides/color-theme">Color Theme</option><option value="/api/extension-guides/file-icon-theme">File Icon Theme</option><option value="/api/extension-guides/product-icon-theme">Product Icon Theme</option><option value="/api/extension-guides/tree-view">Tree View</option><option value="/api/extension-guides/webview">Webview</option><option value="/api/extension-guides/notebook">Notebook</option><option value="/api/extension-guides/custom-editors">Custom Editors</option><option value="/api/extension-guides/virtual-documents">Virtual Documents</option><option value="/api/extension-guides/virtual-workspaces">Virtual Workspaces</option><option value="/api/extension-guides/web-extensions">Web Extensions</option><option value="/api/extension-guides/workspace-trust" selected>Workspace Trust</option><option value="/api/extension-guides/task-provider">Task Provider</option><option value="/api/extension-guides/scm-provider">Source Control</option><option value="/api/extension-guides/debugger-extension">Debugger Extension</option><option value="/api/extension-guides/markdown-extension">Markdown Extension</option><option value="/api/extension-guides/testing">Test Extension</option><option value="/api/extension-guides/custom-data-extension">Custom Data Extension</option><option value="/api/extension-guides/telemetry">Telemetry</option></optgroup><optgroup label="UX Guidelines"><option value="/api/ux-guidelines/overview">Overview</option><option value="/api/ux-guidelines/activity-bar">Activity Bar</option><option value="/api/ux-guidelines/sidebars">Sidebars</option><option value="/api/ux-guidelines/panel">Panel</option><option value="/api/ux-guidelines/status-bar">Status Bar</option><option value="/api/ux-guidelines/views">Views</option><option value="/api/ux-guidelines/editor-actions">Editor Actions</option><option value="/api/ux-guidelines/quick-picks">Quick Picks</option><option value="/api/ux-guidelines/command-palette">Command Palette</option><option value="/api/ux-guidelines/notifications">Notifications</option><option value="/api/ux-guidelines/webviews">Webviews</option><option value="/api/ux-guidelines/context-menus">Context Menus</option><option value="/api/ux-guidelines/walkthroughs">Walkthroughs</option><option value="/api/ux-guidelines/settings">Settings</option></optgroup><optgroup label="Language Extensions"><option value="/api/language-extensions/overview">Overview</option><option value="/api/language-extensions/syntax-highlight-guide">Syntax Highlight Guide</option><option value="/api/language-extensions/semantic-highlight-guide">Semantic Highlight Guide</option><option value="/api/language-extensions/snippet-guide">Snippet Guide</option><option value="/api/language-extensions/language-configuration-guide">Language Configuration Guide</option><option value="/api/language-extensions/programmatic-language-features">Programmatic Language Features</option><option value="/api/language-extensions/language-server-extension-guide">Language Server Extension Guide</option><option value="/api/language-extensions/embedded-languages">Embedded Languages</option></optgroup><optgroup label="Testing and Publishing"><option value="/api/working-with-extensions/testing-extension">Testing Extensions</option><option value="/api/working-with-extensions/publishing-extension">Publishing Extensions</option><option value="/api/working-with-extensions/bundling-extension">Bundling Extensions</option><option value="/api/working-with-extensions/continuous-integration">Continuous Integration</option></optgroup><optgroup label="Advanced Topics"><option value="/api/advanced-topics/extension-host">Extension Host</option><option value="/api/advanced-topics/remote-extensions">Remote Development and Codespaces</option><option value="/api/advanced-topics/using-proposed-api">Using Proposed API</option><option value="/api/advanced-topics/tslint-eslint-migration">Migrate from TSLint to ESLint</option><option value="/api/advanced-topics/python-extension-template">Python Extension Template</option></optgroup><optgroup label="References"><option value="/api/references/vscode-api">VS Code API</option><option value="/api/references/contribution-points">Contribution Points</option><option value="/api/references/activation-events">Activation Events</option><option value="/api/references/extension-manifest">Extension Manifest</option><option value="/api/references/commands">Built-In Commands</option><option value="/api/references/when-clause-contexts">When Clause Contexts</option><option value="/api/references/theme-color">Theme Color</option><option value="/api/references/icons-in-labels">Product Icon Reference</option><option value="/api/references/document-selector">Document Selector</option></optgroup></select></nav></aside><div class="docs-content-wrapper">
			
			<main class="docs-main-content body"><h1>Workspace Trust Extension Guide</h1>
<h2 id="what-is-workspace-trust" data-needslink="what-is-workspace-trust">What is Workspace Trust?</h2>
<p><a href="/docs/editor/workspace-trust">Workspace Trust</a> is a feature driven by the security risks associated with unintended code execution when a user opens a workspace in VS Code. For example, consider that a language extension, in order to provide functionality, may execute code from the currently loaded workspace. In this scenario, the user should trust that the contents of the workspace are not malicious. Workspace Trust centralizes this decision within VS Code and supports a <a href="/docs/editor/workspace-trust#_restricted-mode">Restricted Mode</a> to protect against automatic code execution so that extension authors do not have to handle this infrastructure themselves. VS Code offers static declaration and API support to onboard extensions quickly without the need to duplicate code across extensions.</p>
<h2 id="onboarding" data-needslink="onboarding">Onboarding</h2>
<h3 id="static-declarations" data-needslink="static-declarations">Static declarations</h3>
<p>In your extension's <code>package.json</code>, VS Code supports the following new <code>capabilities</code> property <code>untrustedWorkspaces</code>:</p>
<pre class="shiki" data-lang="typescript" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#C8C8C8;--shiki-light:#000000">capabilities</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">:</span></span>
<span class="line"><span style="--shiki-dark:#C8C8C8;--shiki-light:#000000">  untrustedWorkspaces</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">:</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    { </span><span style="--shiki-dark:#C8C8C8;--shiki-light:#000000">supported</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">true</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> } |</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    { </span><span style="--shiki-dark:#C8C8C8;--shiki-light:#000000">supported</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">false</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#C8C8C8;--shiki-light:#000000">description</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">string</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> } |</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    { </span><span style="--shiki-dark:#C8C8C8;--shiki-light:#000000">supported</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'limited'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#C8C8C8;--shiki-light:#000000">description</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">string</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">restrictedConfigurations</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">?: </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">string</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">[] }</span></span>
<span class="line"></span></code></pre>
<p>For the <code>supported</code> property, the following values are accepted:</p>
<ul><li><code>true</code> - The extension is fully supported in Restricted Mode as it does not need Workspace Trust to perform any functionality. It will be enabled exactly as before.</li>
<li><code>false</code> - The extension is not supported in Restricted Mode as it cannot function without Workspace Trust. It will remain disabled until Workspace Trust is granted.</li>
<li><code>'limited'</code> - Some features of the extension are supported in Restricted Mode. Trust-sensitive features should be disabled until Workspace Trust is granted. The extension can use the VS Code API to hide or disable these features. Workspace settings can be gated by trust automatically using the <code>restrictedConfigurations</code> property.</li>
</ul><p>For the <code>description</code> property, a description of why trust is needed must be provided to help the user understand what features will be disabled or what they should review before granting or denying Workspace Trust. If <code>supported</code> is set to <code>true</code>, this property is ignored.</p>
<p>The value for the <code>description</code> property should be added to <code>package.nls.json</code> and then referenced in the <code>package.json</code> file for localization support.</p>
<p>The <code>restrictedConfigurations</code> property takes an array of configuration setting IDs. For the settings listed, the extension will not be given workspace-defined values when in Restricted Mode for an untrusted workspace.</p>
<h2 id="how-to-support-restricted-mode" data-needslink="how-to-support-restricted-mode">How to support Restricted Mode?</h2>
<p>To help extension authors understand what is in scope for Workspace Trust and what types of features are safe in Restricted Mode, here are a list of questions to consider.</p>
<h3 id="does-my-extension-have-a-main-entry-point" data-needslink="does-my-extension-have-a-main-entry-point">Does my extension have a main entry point?</h3>
<p>If an extension does not have a <code>main</code> entry point (for example themes and language grammars), the extension does not require Workspace Trust. Extension authors do not need to take any action for such extensions as they will continue to function independent whether the workspace is trusted or not.</p>
<h3 id="does-my-extension-rely-on-files-in-the-opened-workspace-to-provide-features" data-needslink="does-my-extension-rely-on-files-in-the-opened-workspace-to-provide-features">Does my extension rely on files in the opened workspace to provide features?</h3>
<p>This can mean things like settings that can be set by the workspace or actual code in the workspace. If the extension never uses any of the contents of the workspace, it probably doesn't require trust. Otherwise, take a look at the other questions.</p>
<h3 id="does-my-extension-treat-any-contents-of-the-workspace-as-code" data-needslink="does-my-extension-treat-any-contents-of-the-workspace-as-code">Does my extension treat any contents of the workspace as code?</h3>
<p>The most common example of this is using a project's workspace dependencies, such as the Node.js modules stored in the local workspace. A malicious workspace might check in a compromised version of the module. Thus, this is a security risk for the user and extension. In addition, an extension may rely on JavaScript or other configuration files that control the extension or other modules' behavior. There are many other examples, such as executing an opened code file to determine its output for error reporting.</p>
<h3 id="does-my-extension-use-settings-that-determine-code-execution-that-can-be-defined-in-the-workspace" data-needslink="does-my-extension-use-settings-that-determine-code-execution-that-can-be-defined-in-the-workspace">Does my extension use settings that determine code execution that can be defined in the workspace?</h3>
<p>Your extension might use settings values as flags to a CLI that your extension executes. If these settings are overridden by a malicious workspace, they could be used as an attack vector against your extension. On the other hand, if the settings' values are only used to detect certain conditions, then it may not be a security risk and does not require Workspace Trust. For example, an extension might check whether the value of a preferred shell setting is <code>bash</code> or <code>pwsh</code> to determine what documentation to show. The <a href="#_configurations-settings">Configurations (settings)</a> section below has guidance on settings to help you find the optimal configuration for your extension.</p>
<p>This is not an exhaustive list of cases that might require Workspace Trust. As we review more extensions, we will update this list. Use this list to think of similar behavior your extension might be doing when considering Workspace Trust.</p>
<h3 id="what-if-i-dont-make-changes-to-my-extension" data-needslink="what-if-i-dont-make-changes-to-my-extension">What if I don't make changes to my extension?</h3>
<p>As mentioned above, an extension that does not contribute anything to their <code>package.json</code> will be treated as not supporting Workspace Trust. It will be disabled when a workspace is in Restricted Mode and the user will be notified that some extensions are not working due to Workspace Trust. This measure is the most security-conscious approach for the user. Even though this is the default, it is a best practice to set the appropriate value indicating that as an extension author, you have made the effort to protect the user and your extension from malicious workspace content.</p>
<h2 id="workspace-trust-api" data-needslink="workspace-trust-api">Workspace Trust API</h2>
<p>As described above, the first step to using the API is adding the static declarations to your <code>package.json</code>. The easiest method of onboarding would be to use a <code>false</code> value for the <code>supported</code> property. Once again, this is the default behavior even if you do nothing, but it's a good signal to the user that you have made a deliberate choice. In this case, your extension does not need to do anything else. It will not be activated until trust is given and then your extension will know that it is executing with the consent of the user. However, if your extension only requires trust for part of its functionality, this is likely not the best option.</p>
<p>For extensions that wish to gate their features on Workspace Trust, they should use the <code>'limited'</code> value for the <code>supported</code> property, and VS Code provides the following API:</p>
<pre class="shiki" data-lang="typescript" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">export</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> namespace</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99"> workspace</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">  /**</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">   * When true, the user has explicitly trusted the contents of the workspace.</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">   */</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">  export</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> isTrusted</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">boolean</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">  /**</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">   * Event that fires when the current workspace has been trusted.</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">   */</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">  export</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> onDidGrantWorkspaceTrust</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">Event</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">&lt;</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">void</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">&gt;;</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<p>Use the <code>isTrusted</code> property to determine if the current workspace is trusted and the <code>onDidGrantWorkspaceTrust</code> event to listen for when trust has been granted to the workspace. You can use this API to block specific code paths and perform any necessary registrations once the workspace has been trusted.</p>
<p>VS Code also exposes a context key <code>isWorkspaceTrusted</code> for use in <code>when</code> clauses as described below.</p>
<h2 id="contribution-points" data-needslink="contribution-points">Contribution points</h2>
<h3 id="commands-views-or-other-ui" data-needslink="commands-views-or-other-ui">Commands, views, or other UI</h3>
<p>When the user has not trusted the workspace, they will be operating in Restricted Mode with limited functionality geared towards browsing code. Any features that you disable in Restricted Mode should be hidden from the user. This can be done via <a href="/api/references/when-clause-contexts">when clause contexts</a> and the context key <code>isWorkspaceTrusted</code>. A command can still be called even if it is not presented in the UI, so you should block execution or not register a command based on the API above in your extension code.</p>
<h3 id="configurations-settings" data-needslink="configurations-settings">Configurations (settings)</h3>
<p>First, you should review your settings to determine if they need to take trust into account. As described above, a workspace may define a value for a setting that your extension consumes that is malicious to the use. If you identify settings that are vulnerable, you should use <code>'limited'</code> for the <code>supported</code> property and list the setting ID in the <code>restrictedConfigurations</code> array.</p>
<p>When you add a setting ID to the <code>restrictedConfigurations</code> array, VS Code will only return the user-defined value of the setting in Restricted Mode. Your extension then doesn't need to make any additional code changes to handle the setting. When trust is granted, a configuration change event will fire in addition to the Workspace Trust event.</p>
<h3 id="debug-extensions" data-needslink="debug-extensions">Debug extensions</h3>
<p>VS Code will prevent debugging in Restricted Mode. For this reason, debugging extensions generally do not need to require trust and should select <code>true</code> for the <code>supported</code> property. However, if your extension provides additional functionality, commands, or settings that are not part of the built-in debugging flow, you should use <code>'limited'</code> and follow the above guidance.</p>
<h3 id="task-providers" data-needslink="task-providers">Task providers</h3>
<p>Similar to debugging, VS Code prevents running tasks in Restricted Mode. If your extension provides additional functionality, commands, or settings that are not part of the built-in tasks flow, you should use <code>'limited'</code> and follow the above guidance. Otherwise, you can specify <code>supported: true</code>.</p>
<h2 id="testing-workspace-trust" data-needslink="testing-workspace-trust">Testing Workspace Trust</h2>
<p>See the <a href="/docs/editor/workspace-trust">Workspace Trust user guide</a> for details on enabling and configuring Workspace Trust.</p>

				<div class="feedback" data-edit-url="https://vscode.dev/github/microsoft/vscode-docs/blob/main/api/extension-guides/workspace-trust.md"></div>
				
				<div class="body-footer">6/3/2026</div>
				
            </main><aside class="docs-right-sidebar hidden-xs"><div class="docs-markdown-actions">
                    <div class="docs-markdown-dropdown" data-raw-url="/raw/api/extension-guides/workspace-trust.md">
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
                    <ul class="nav"><li><a href="#what-is-workspace-trust">What is Workspace Trust?</a></li>
                        
                        <li><a href="#onboarding">Onboarding</a></li>
                        
                        <li><a href="#how-to-support-restricted-mode">How to support Restricted Mode?</a></li>
                        
                        <li><a href="#workspace-trust-api">Workspace Trust API</a></li>
                        
                        <li><a href="#contribution-points">Contribution points</a></li>
                        
                        <li><a href="#testing-workspace-trust">Testing Workspace Trust</a></li>
                        
                    </ul></nav></aside></div>
		<div class="docs-mobile-widgets visible-xs">
			<div class="connect-widget"></div>
		</div>
	</div>
</div>
		</main>