# Language Model Chat Provider API

> 源文档: [https://code.visualstudio.com/api/extension-guides/ai/language-model-chat-provider](https://code.visualstudio.com/api/extension-guides/ai/language-model-chat-provider)

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
			          
			<li class="panel expanded">
			  <a class="area" role="button" href="#extension-guides-ai-articles" data-parent="#extension-guides-articles" data-toggle="collapse">AI</a>
			  <ul id="extension-guides-ai-articles" class="collapse in"><li>
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
			          
			        <li class="active">
			          <a href="/api/extension-guides/ai/language-model-chat-provider" aria-label="Current Page: Language Model Chat Provider">Language Model Chat Provider</a>
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
				<select id="small-nav-dropdown" aria-label="topics"><option value="/api">Overview</option><optgroup label="Get Started"><option value="/api/get-started/your-first-extension">Your First Extension</option><option value="/api/get-started/extension-anatomy">Extension Anatomy</option><option value="/api/get-started/wrapping-up">Wrapping Up</option></optgroup><optgroup label="Extension Capabilities"><option value="/api/extension-capabilities/overview">Overview</option><option value="/api/extension-capabilities/common-capabilities">Common Capabilities</option><option value="/api/extension-capabilities/theming">Theming</option><option value="/api/extension-capabilities/extending-workbench">Extending Workbench</option></optgroup><optgroup label="Extension Guides"><option value="/api/extension-guides/overview">Overview</option><optgroup label="Extension Guides - AI"><option value="/api/extension-guides/ai/ai-extensibility-overview">AI Extensibility</option><option value="/api/extension-guides/ai/tools">Language Model Tool</option><option value="/api/extension-guides/ai/mcp">MCP Dev Guide</option><option value="/api/extension-guides/ai/chat">Chat Participant</option><option value="/api/extension-guides/ai/chat-tutorial">Chat Tutorial</option><option value="/api/extension-guides/ai/language-model">Language Model</option><option value="/api/extension-guides/ai/language-model-tutorial">Language Model Tutorial</option><option value="/api/extension-guides/ai/language-model-chat-provider" selected>Language Model Chat Provider</option><option value="/api/extension-guides/ai/prompt-tsx">Prompt TSX</option></optgroup><option value="/api/extension-guides/command">Command</option><option value="/api/extension-guides/color-theme">Color Theme</option><option value="/api/extension-guides/file-icon-theme">File Icon Theme</option><option value="/api/extension-guides/product-icon-theme">Product Icon Theme</option><option value="/api/extension-guides/tree-view">Tree View</option><option value="/api/extension-guides/webview">Webview</option><option value="/api/extension-guides/notebook">Notebook</option><option value="/api/extension-guides/custom-editors">Custom Editors</option><option value="/api/extension-guides/virtual-documents">Virtual Documents</option><option value="/api/extension-guides/virtual-workspaces">Virtual Workspaces</option><option value="/api/extension-guides/web-extensions">Web Extensions</option><option value="/api/extension-guides/workspace-trust">Workspace Trust</option><option value="/api/extension-guides/task-provider">Task Provider</option><option value="/api/extension-guides/scm-provider">Source Control</option><option value="/api/extension-guides/debugger-extension">Debugger Extension</option><option value="/api/extension-guides/markdown-extension">Markdown Extension</option><option value="/api/extension-guides/testing">Test Extension</option><option value="/api/extension-guides/custom-data-extension">Custom Data Extension</option><option value="/api/extension-guides/telemetry">Telemetry</option></optgroup><optgroup label="UX Guidelines"><option value="/api/ux-guidelines/overview">Overview</option><option value="/api/ux-guidelines/activity-bar">Activity Bar</option><option value="/api/ux-guidelines/sidebars">Sidebars</option><option value="/api/ux-guidelines/panel">Panel</option><option value="/api/ux-guidelines/status-bar">Status Bar</option><option value="/api/ux-guidelines/views">Views</option><option value="/api/ux-guidelines/editor-actions">Editor Actions</option><option value="/api/ux-guidelines/quick-picks">Quick Picks</option><option value="/api/ux-guidelines/command-palette">Command Palette</option><option value="/api/ux-guidelines/notifications">Notifications</option><option value="/api/ux-guidelines/webviews">Webviews</option><option value="/api/ux-guidelines/context-menus">Context Menus</option><option value="/api/ux-guidelines/walkthroughs">Walkthroughs</option><option value="/api/ux-guidelines/settings">Settings</option></optgroup><optgroup label="Language Extensions"><option value="/api/language-extensions/overview">Overview</option><option value="/api/language-extensions/syntax-highlight-guide">Syntax Highlight Guide</option><option value="/api/language-extensions/semantic-highlight-guide">Semantic Highlight Guide</option><option value="/api/language-extensions/snippet-guide">Snippet Guide</option><option value="/api/language-extensions/language-configuration-guide">Language Configuration Guide</option><option value="/api/language-extensions/programmatic-language-features">Programmatic Language Features</option><option value="/api/language-extensions/language-server-extension-guide">Language Server Extension Guide</option><option value="/api/language-extensions/embedded-languages">Embedded Languages</option></optgroup><optgroup label="Testing and Publishing"><option value="/api/working-with-extensions/testing-extension">Testing Extensions</option><option value="/api/working-with-extensions/publishing-extension">Publishing Extensions</option><option value="/api/working-with-extensions/bundling-extension">Bundling Extensions</option><option value="/api/working-with-extensions/continuous-integration">Continuous Integration</option></optgroup><optgroup label="Advanced Topics"><option value="/api/advanced-topics/extension-host">Extension Host</option><option value="/api/advanced-topics/remote-extensions">Remote Development and Codespaces</option><option value="/api/advanced-topics/using-proposed-api">Using Proposed API</option><option value="/api/advanced-topics/tslint-eslint-migration">Migrate from TSLint to ESLint</option><option value="/api/advanced-topics/python-extension-template">Python Extension Template</option></optgroup><optgroup label="References"><option value="/api/references/vscode-api">VS Code API</option><option value="/api/references/contribution-points">Contribution Points</option><option value="/api/references/activation-events">Activation Events</option><option value="/api/references/extension-manifest">Extension Manifest</option><option value="/api/references/commands">Built-In Commands</option><option value="/api/references/when-clause-contexts">When Clause Contexts</option><option value="/api/references/theme-color">Theme Color</option><option value="/api/references/icons-in-labels">Product Icon Reference</option><option value="/api/references/document-selector">Document Selector</option></optgroup></select></nav></aside><div class="docs-content-wrapper">
			
			<main class="docs-main-content body"><h1>Language Model Chat Provider API</h1>
<p>The Language Model Chat Provider API enables you to contribute your own language models to chat in Visual Studio Code.</p>
<div class="markdown-alert note" dir="auto">
      <span>
        <svg class="markdown-alert-icon" viewbox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8Zm8-6.5a6.5 6.5 0 1 0 0 13 6.5 6.5 0 0 0 0-13ZM6.5 7.75A.75.75 0 0 1 7.25 7h1a.75.75 0 0 1 .75.75v2.75h.25a.75.75 0 0 1 0 1.5h-2a.75.75 0 0 1 0-1.5h.25v-2h-.25a.75.75 0 0 1-.75-.75ZM8 6a1 1 0 1 1 0-2 1 1 0 0 1 0 2Z"></path></svg>
        Note
      </span><p>If you are a Copilot Business or Enterprise user, your administrator can disable the <strong>Bring Your Own Language Model Key</strong> policy in the <a href="https://github.com/settings/copilot/features" class="external-link" target="_blank">Copilot policy settings</a> on GitHub.com for models provided through this API.</p>
</div><h2 id="overview" data-needslink="overview">Overview</h2>
<p>The <code>LanguageModelChatProvider</code> interface follows a one-provider-to-many-models relationship, enabling providers to offer multiple models. Each provider is responsible for:</p>
<ul><li>Discovering and preparing available language models</li>
<li>Handling chat requests for its models</li>
<li>Providing token counting functionality</li>
</ul><h2 id="language-model-information" data-needslink="language-model-information">Language model information</h2>
<p>Each language model must provide metadata through the <code>LanguageModelChatInformation</code> interface. The <code>provideLanguageModelChatInformation</code> method returns an array of these objects to inform VS Code about the available models.</p>
<pre class="shiki" data-lang="typescript" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">interface</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99"> LanguageModelChatInformation</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">  readonly</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> id</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">string</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">; </span><span style="--shiki-dark:#6A9955;--shiki-light:#008000">// Unique identifier for the model - unique within the provider</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">  readonly</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> name</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">string</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">; </span><span style="--shiki-dark:#6A9955;--shiki-light:#008000">// Human-readable name of the language model - shown in the model picker</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">  readonly</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> family</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">string</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">; </span><span style="--shiki-dark:#6A9955;--shiki-light:#008000">// Model family name</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">  readonly</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> version</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">string</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">; </span><span style="--shiki-dark:#6A9955;--shiki-light:#008000">// Version string</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">  readonly</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> maxInputTokens</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">number</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">; </span><span style="--shiki-dark:#6A9955;--shiki-light:#008000">// Maximum number of tokens the model can accept as input</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">  readonly</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> maxOutputTokens</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">number</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">; </span><span style="--shiki-dark:#6A9955;--shiki-light:#008000">// Maximum number of tokens the model is capable of producing</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">  readonly</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> tooltip</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">?: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">string</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">; </span><span style="--shiki-dark:#6A9955;--shiki-light:#008000">// Optional tooltip text when hovering the model in the UI</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">  readonly</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> detail</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">?: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">string</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">; </span><span style="--shiki-dark:#6A9955;--shiki-light:#008000">// Human-readable text that is rendered alongside the model</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">  readonly</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> capabilities</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">    readonly</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> imageInput</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">?: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">boolean</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">; </span><span style="--shiki-dark:#6A9955;--shiki-light:#008000">// Supports image inputs</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">    readonly</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> toolCalling</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">?: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">boolean</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> | </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">number</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">; </span><span style="--shiki-dark:#6A9955;--shiki-light:#008000">// Supports tool calling</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  };</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<h2 id="register-the-provider" data-needslink="register-the-provider">Register the provider</h2>
<ol><li>
<p>The first step is to register the provider in your <code>package.json</code>, in the <code>contributes.languageModelChatProviders</code> section. Provide a unique <code>vendor</code> ID and a <code>displayName</code>.</p>
<pre class="shiki" data-lang="json" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">{</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "contributes"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "languageModelChatProviders"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">        "vendor"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"my-provider"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">        "displayName"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"My Provider"</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    ]</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
</li>
<li>
<p>Next, in your extension activation function, register your language model provider using the <code>lm.registerLanguageModelChatProvider</code> method.</p>
<p>Provide the provider ID that you used in the <code>package.json</code> and an instance of your provider class:</p>
<pre class="shiki" data-lang="typescript" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">import</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> *</span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB"> as</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> vscode</span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB"> from</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'vscode'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">import</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> { </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">SampleChatModelProvider</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> } </span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">from</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> './provider'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">export</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> function</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> activate</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">_</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">ExtensionContext</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">lm</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">registerLanguageModelChatProvider</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'my-provider'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">new</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> SampleChatModelProvider</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">());</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
</li>
<li>
<p>Optionally, provide a <code>contributes.languageModelChatProviders.managementCommand</code> in your <code>package.json</code> to allow users to manage the language model provider.</p>
<p>The value of the <code>managementCommand</code> property must be a command defined in the <code>contributes.commands</code> section of your <code>package.json</code>. In your extension, register the command (<code>vscode.commands.registerCommand</code>) and implement the logic for managing the provider such as configuring API keys or other settings.</p>
<pre class="shiki" data-lang="json" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">{</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "contributes"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "languageModelChatProviders"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">        "vendor"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"my-provider"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">        "displayName"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"My Provider"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">        "managementCommand"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"my-provider.manage"</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    ],</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "commands"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">        "command"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"my-provider.manage"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">        "title"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"Manage My Provider"</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    ]</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
</li>
</ol><h2 id="implement-the-provider" data-needslink="implement-the-provider">Implement the provider</h2>
<p>A language provider must implement the <code>LanguageModelChatProvider</code> interface, which has three main methods:</p>
<ul><li><code>provideLanguageModelChatInformation</code>: returns the list of available models</li>
<li><code>provideLanguageModelChatResponse</code>: handles chat requests and streams responses</li>
<li><code>provideTokenCount</code>: implements token counting functionality</li>
</ul><h3 id="prepare-language-model-information" data-needslink="prepare-language-model-information">Prepare language model information</h3>
<p>The <code>provideLanguageModelChatInformation</code> method is called by VS Code to discover the available models and returns a list of <code>LanguageModelChatInformation</code> objects.</p>
<p>Use the <code>options.silent</code> parameter to control whether to prompt the user for credentials or extra configuration:</p>
<pre class="shiki" data-lang="typescript" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">async</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> provideLanguageModelChatInformation</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    options</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: { </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">silent:</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> boolean</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> },</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    token</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">CancellationToken</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">): </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">Promise</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">&lt;</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">LanguageModelChatInformation</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">[]&gt; {</span></span>
<span class="line"><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">    if</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> (options.silent) {</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">        return</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> []; </span><span style="--shiki-dark:#6A9955;--shiki-light:#008000">// Don't prompt user in silent mode</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    } else {</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">        await</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> this</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">promptForApiKey</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(); </span><span style="--shiki-dark:#6A9955;--shiki-light:#008000">// Prompt user for credentials</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    }</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">    // Fetch available models from your service</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    const </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">models</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">await</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> this</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">fetchAvailableModels</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">();</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">    // Map your models to LanguageModelChatInformation format</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    return models.map(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">model</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> =&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> ({</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">        id:</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> model</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">id</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">        name:</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> model</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">displayName</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">        family:</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> model</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">family</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">        version:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> '1.0.0'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">        maxInputTokens:</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> model</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">contextWindow</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> - </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">model</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">maxOutput</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">        maxOutputTokens:</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> model</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">maxOutput</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">        capabilities:</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">            imageInput:</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> model</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">supportsImages</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">            toolCalling:</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> model</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">supportsTools</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">        }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    }));</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<h3 id="handle-chat-requests" data-needslink="handle-chat-requests">Handle chat requests</h3>
<p>The <code>provideLanguageModelChatResponse</code> method handles actual chat requests. The provider receives an array of messages in the <code>LanguageModelChatRequestMessage</code> format and you can optionally convert them to the format required by your language model API (see <a href="#_message-format-and-conversion">Message format and conversion</a>).</p>
<p>Use the <code>progress</code> parameter to stream response chunks. The response can include text parts, tool calls, and tool results (see <a href="#_response-parts">Response parts</a>).</p>
<pre class="shiki" data-lang="typescript" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">async</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> provideLanguageModelChatResponse</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    model</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">LanguageModelChatInformation</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    messages</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">readonly</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> LanguageModelChatRequestMessage</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">[],</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    options</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">ProvideLanguageModelChatResponseOptions</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    progress</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">Progress</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">&lt;</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">LanguageModelResponsePart</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">&gt;,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    token</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">CancellationToken</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">): </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">Promise</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">&lt;</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">void</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">&gt; {</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">    // TODO: Implement message conversion, processing, and response streaming</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">    // Optionally, differentiate behavior based on model ID</span></span>
<span class="line"><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">    if</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> (model.id === </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"my-model-a"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">        progress</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">report</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">new</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> LanguageModelTextPart</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"This is my A response."</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">));</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    } else {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">        progress</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">report</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">new</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> LanguageModelTextPart</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"Unknown model."</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">));</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<h3 id="provide-token-count" data-needslink="provide-token-count">Provide token count</h3>
<p>The <code>provideTokenCount</code> method is responsible for estimating the number of tokens in a given text input:</p>
<pre class="shiki" data-lang="typescript" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">async</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> provideTokenCount</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    model</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">LanguageModelChatInformation</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    text</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">string</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> | </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">LanguageModelChatRequestMessage</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    token</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">CancellationToken</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">): </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">Promise</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">&lt;</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">number</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">&gt; {</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">    // TODO: Implement token counting for your models</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">    // Example estimation for strings</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    return Math.ceil(text.toString().length / </span><span style="--shiki-dark:#B5CEA8;--shiki-light:#098658">4</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">);</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<h2 id="message-format-and-conversion" data-needslink="message-format-and-conversion">Message format and conversion</h2>
<p>Your provider receives messages in the <code>LanguageModelChatRequestMessage</code> format, which you'll typically need to convert to your service's API format. The message content can be a mix of text parts, tool calls, and tool results.</p>
<pre class="shiki" data-lang="typescript" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">interface</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99"> LanguageModelChatRequestMessage</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">  readonly</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> role</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">LanguageModelChatMessageRole</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">  readonly</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> content</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">ReadonlyArray</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">&lt;</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">LanguageModelInputPart</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> | </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">unknown</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">&gt;;</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">  readonly</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> name</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">string</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> | </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">undefined</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<p>Optionally, convert these messages appropriately for your language model API:</p>
<pre class="shiki" data-lang="typescript" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">private</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> convertMessages</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">messages</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">readonly</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> LanguageModelChatRequestMessage</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">[]) {</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">    return</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> messages</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">map</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">msg</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> =&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> ({</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">        role:</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> msg</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">role</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> === </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">LanguageModelChatMessageRole</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">User</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> ? </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'user'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> : </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'assistant'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">        content:</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> msg</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">content</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">            .</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">filter</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">part</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> =&gt;</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> part</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> instanceof</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99"> vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">LanguageModelTextPart</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">)</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">            .</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">map</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">part</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> =&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> (</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">part</span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB"> as</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99"> vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">LanguageModelTextPart</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">).</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">value</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">)</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">            .</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">join</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">''</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">)</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    }));</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<h2 id="response-parts" data-needslink="response-parts">Response parts</h2>
<p>Your provider can report different types of response parts through the progress callback via the <code>LanguageModelResponsePart</code> type, which can be one of:</p>
<ul><li><code>LanguageModelTextPart</code> - Text content</li>
<li><code>LanguageModelToolCallPart</code> - Tool/function calls</li>
<li><code>LanguageModelToolResultPart</code> - Tool result content</li>
</ul><h2 id="getting-started" data-needslink="getting-started">Getting started</h2>
<p>You can get started with a <a href="https://github.com/microsoft/vscode-extension-samples/blob/main/chat-model-provider-sample" class="external-link" target="_blank">basic example project</a>.</p>
<h2 id="related-content" data-needslink="related-content">Related content</h2>
<ul><li><a href="/api/references/vscode-api">VS Code API Reference</a></li>
<li><a href="/api/extension-guides/ai/language-model">Language Model API Guide</a></li>
<li><a href="/api/extension-guides/ai/chat">Chat API Extension</a></li>
</ul><div class="feedback" data-edit-url="https://vscode.dev/github/microsoft/vscode-docs/blob/main/api/extension-guides/ai/language-model-chat-provider.md"></div>
				
				<div class="body-footer">6/3/2026</div>
				
            </main><aside class="docs-right-sidebar hidden-xs"><div class="docs-markdown-actions">
                    <div class="docs-markdown-dropdown" data-raw-url="/raw/api/extension-guides/ai/language-model-chat-provider.md">
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
                    <ul class="nav"><li><a href="#overview">Overview</a></li>
                        
                        <li><a href="#language-model-information">Language model information</a></li>
                        
                        <li><a href="#register-the-provider">Register the provider</a></li>
                        
                        <li><a href="#implement-the-provider">Implement the provider</a></li>
                        
                        <li><a href="#message-format-and-conversion">Message format and conversion</a></li>
                        
                        <li><a href="#response-parts">Response parts</a></li>
                        
                        <li><a href="#getting-started">Getting started</a></li>
                        
                        <li><a href="#related-content">Related content</a></li>
                        
                    </ul></nav></aside></div>
		<div class="docs-mobile-widgets visible-xs">
			<div class="connect-widget"></div>
		</div>
	</div>
</div>
		</main>