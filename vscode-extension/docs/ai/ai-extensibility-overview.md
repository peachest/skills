# AI extensibility in VS Code

> 源文档: [https://code.visualstudio.com/api/extension-guides/ai/ai-extensibility-overview](https://code.visualstudio.com/api/extension-guides/ai/ai-extensibility-overview)

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
			  <ul id="extension-guides-ai-articles" class="collapse in"><li class="active">
			          <a href="/api/extension-guides/ai/ai-extensibility-overview" aria-label="Current Page: AI Extensibility">AI Extensibility</a>
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
				<select id="small-nav-dropdown" aria-label="topics"><option value="/api">Overview</option><optgroup label="Get Started"><option value="/api/get-started/your-first-extension">Your First Extension</option><option value="/api/get-started/extension-anatomy">Extension Anatomy</option><option value="/api/get-started/wrapping-up">Wrapping Up</option></optgroup><optgroup label="Extension Capabilities"><option value="/api/extension-capabilities/overview">Overview</option><option value="/api/extension-capabilities/common-capabilities">Common Capabilities</option><option value="/api/extension-capabilities/theming">Theming</option><option value="/api/extension-capabilities/extending-workbench">Extending Workbench</option></optgroup><optgroup label="Extension Guides"><option value="/api/extension-guides/overview">Overview</option><optgroup label="Extension Guides - AI"><option value="/api/extension-guides/ai/ai-extensibility-overview" selected>AI Extensibility</option><option value="/api/extension-guides/ai/tools">Language Model Tool</option><option value="/api/extension-guides/ai/mcp">MCP Dev Guide</option><option value="/api/extension-guides/ai/chat">Chat Participant</option><option value="/api/extension-guides/ai/chat-tutorial">Chat Tutorial</option><option value="/api/extension-guides/ai/language-model">Language Model</option><option value="/api/extension-guides/ai/language-model-tutorial">Language Model Tutorial</option><option value="/api/extension-guides/ai/language-model-chat-provider">Language Model Chat Provider</option><option value="/api/extension-guides/ai/prompt-tsx">Prompt TSX</option></optgroup><option value="/api/extension-guides/command">Command</option><option value="/api/extension-guides/color-theme">Color Theme</option><option value="/api/extension-guides/file-icon-theme">File Icon Theme</option><option value="/api/extension-guides/product-icon-theme">Product Icon Theme</option><option value="/api/extension-guides/tree-view">Tree View</option><option value="/api/extension-guides/webview">Webview</option><option value="/api/extension-guides/notebook">Notebook</option><option value="/api/extension-guides/custom-editors">Custom Editors</option><option value="/api/extension-guides/virtual-documents">Virtual Documents</option><option value="/api/extension-guides/virtual-workspaces">Virtual Workspaces</option><option value="/api/extension-guides/web-extensions">Web Extensions</option><option value="/api/extension-guides/workspace-trust">Workspace Trust</option><option value="/api/extension-guides/task-provider">Task Provider</option><option value="/api/extension-guides/scm-provider">Source Control</option><option value="/api/extension-guides/debugger-extension">Debugger Extension</option><option value="/api/extension-guides/markdown-extension">Markdown Extension</option><option value="/api/extension-guides/testing">Test Extension</option><option value="/api/extension-guides/custom-data-extension">Custom Data Extension</option><option value="/api/extension-guides/telemetry">Telemetry</option></optgroup><optgroup label="UX Guidelines"><option value="/api/ux-guidelines/overview">Overview</option><option value="/api/ux-guidelines/activity-bar">Activity Bar</option><option value="/api/ux-guidelines/sidebars">Sidebars</option><option value="/api/ux-guidelines/panel">Panel</option><option value="/api/ux-guidelines/status-bar">Status Bar</option><option value="/api/ux-guidelines/views">Views</option><option value="/api/ux-guidelines/editor-actions">Editor Actions</option><option value="/api/ux-guidelines/quick-picks">Quick Picks</option><option value="/api/ux-guidelines/command-palette">Command Palette</option><option value="/api/ux-guidelines/notifications">Notifications</option><option value="/api/ux-guidelines/webviews">Webviews</option><option value="/api/ux-guidelines/context-menus">Context Menus</option><option value="/api/ux-guidelines/walkthroughs">Walkthroughs</option><option value="/api/ux-guidelines/settings">Settings</option></optgroup><optgroup label="Language Extensions"><option value="/api/language-extensions/overview">Overview</option><option value="/api/language-extensions/syntax-highlight-guide">Syntax Highlight Guide</option><option value="/api/language-extensions/semantic-highlight-guide">Semantic Highlight Guide</option><option value="/api/language-extensions/snippet-guide">Snippet Guide</option><option value="/api/language-extensions/language-configuration-guide">Language Configuration Guide</option><option value="/api/language-extensions/programmatic-language-features">Programmatic Language Features</option><option value="/api/language-extensions/language-server-extension-guide">Language Server Extension Guide</option><option value="/api/language-extensions/embedded-languages">Embedded Languages</option></optgroup><optgroup label="Testing and Publishing"><option value="/api/working-with-extensions/testing-extension">Testing Extensions</option><option value="/api/working-with-extensions/publishing-extension">Publishing Extensions</option><option value="/api/working-with-extensions/bundling-extension">Bundling Extensions</option><option value="/api/working-with-extensions/continuous-integration">Continuous Integration</option></optgroup><optgroup label="Advanced Topics"><option value="/api/advanced-topics/extension-host">Extension Host</option><option value="/api/advanced-topics/remote-extensions">Remote Development and Codespaces</option><option value="/api/advanced-topics/using-proposed-api">Using Proposed API</option><option value="/api/advanced-topics/tslint-eslint-migration">Migrate from TSLint to ESLint</option><option value="/api/advanced-topics/python-extension-template">Python Extension Template</option></optgroup><optgroup label="References"><option value="/api/references/vscode-api">VS Code API</option><option value="/api/references/contribution-points">Contribution Points</option><option value="/api/references/activation-events">Activation Events</option><option value="/api/references/extension-manifest">Extension Manifest</option><option value="/api/references/commands">Built-In Commands</option><option value="/api/references/when-clause-contexts">When Clause Contexts</option><option value="/api/references/theme-color">Theme Color</option><option value="/api/references/icons-in-labels">Product Icon Reference</option><option value="/api/references/document-selector">Document Selector</option></optgroup></select></nav></aside><div class="docs-content-wrapper">
			
			<main class="docs-main-content body"><h1>AI extensibility in VS Code</h1>
<p>This article provides an overview of AI extensibility options in Visual Studio Code, helping you choose the right approach for your extension.</p>
<p>VS Code includes powerful AI features that enhance the coding experience:</p>
<ul><li><strong>Code completion</strong>: Offers inline code suggestions as you type</li>
<li><strong>Agent mode</strong>: Enables AI to autonomously plan and execute development tasks with specialized tools</li>
<li><strong>Chat</strong>: Lets developers use natural language to ask questions or make edits in codebase through chat interfaces</li>
<li><strong>Smart actions</strong>: Use AI-enhanced actions for common development tasks, integrated throughout the editor</li>
</ul><p>You can extend and customize each of these built-in capabilities to create tailored AI experiences that meet the specific needs of your users.</p>
<h2 id="why-extend-ai-in-vs-code" data-needslink="why-extend-ai-in-vs-code">Why extend AI in VS Code?</h2>
<p>Adding AI capabilities to your extension brings several benefits to your users:</p>
<ul><li><strong>Domain-specific knowledge in agent mode</strong>: Let agent mode access your company's data sources and services</li>
<li><strong>Enhanced user experience</strong>: Provide intelligent assistance tailored to your extension's domain</li>
<li><strong>Domain specialization</strong>: Create AI features specific to a programming language, framework, or domain</li>
<li><strong>Extend chat capabilities</strong>: Add specialized tools or assistants to the chat interface for more powerful interactions</li>
<li><strong>Improved developer productivity</strong>: Enhance common developer tasks, like debugging, code reviewing or testing, with AI capabilities</li>
</ul><h2 id="extend-the-chat-experience" data-needslink="extend-the-chat-experience">Extend the chat experience</h2>
<h3 id="language-model-tool" data-needslink="language-model-tool">Language model tool</h3>
<p>Language model tools enable you to extend agent mode in VS Code with domain-specific capabilities. In agent mode, these tools are automatically invoked based on the user's chat prompt to perform specialized tasks or retrieve information from a data source or service. Users can also reference these tools explicitly in their chat prompt by #-mentioning the tool.</p>
<p>To implement a language model tool, use the <a href="/api/extension-guides/ai/tools">Language Model Tools API</a> within your VS Code extension. A language model tool can access all VS Code extension APIs and provide deep integration with the editor.</p>
<p><strong>Key benefits</strong>:</p>
<ul><li>Domain-specific capabilities as part of an autonomous coding workflow</li>
<li>Your tool implementation can use VS Code APIs since it runs in the extension host process</li>
<li>Easy distribution and deployment via the Visual Studio Marketplace</li>
</ul><p><strong>Key considerations</strong>:</p>
<ul><li>Remote deployment requires the extension to implement the client-server communication</li>
<li>Reuse across different tools requires modular design and implementation</li>
</ul><h3 id="mcp-tool" data-needslink="mcp-tool">MCP tool</h3>
<p>Model Context Protocol (MCP) tools provide a way to integrate external services with language models by using a standardized protocol. In agent mode, these tools are automatically invoked based on the user's chat prompt to perform specialized tasks or retrieve information from external data sources.</p>
<p>MCP tools run outside of VS Code, either locally on the user's machine or as a remote service. Users can add MCP tools through JSON configuration or VS Code extension can configure them programmatically. You can implement MCP tools through various language SDKs and deployment options.</p>
<p>As MCP tools run outside of VS Code, they do not have access to the VS Code extension APIs.</p>
<p><strong>Key benefits</strong>:</p>
<ul><li>Add domain-specific capabilities as part of an autonomous coding workflow</li>
<li>Local and remote deployment options</li>
<li>Reuse MCP servers in other MCP clients</li>
</ul><p><strong>Key considerations</strong>:</p>
<ul><li>No access to VS Code extension APIs</li>
<li>Distribution and deployment require users to set up the MCP server</li>
</ul><h3 id="chat-participant" data-needslink="chat-participant">Chat participant</h3>
<p>Chat participants are specialized assistants that enable users to extend ask mode with domain-specific experts. In chat, users can invoke a chat participant by @-mentioning it and passing in a natural language prompt about a particular topic or domain. The chat participant is responsible for handling the entire chat interaction.</p>
<p>To implement a chat participant, use the <a href="/api/extension-guides/ai/chat">Chat API</a> within your VS Code extension. A chat participant can access all VS Code extension APIs and provide deep integration with the editor.</p>
<p><strong>Key benefits</strong>:</p>
<ul><li>Control the end-to-end interaction flow</li>
<li>Running in the extension host process allows access to VS Code extension APIs</li>
<li>Easy distribution and deployment via the Visual Studio Marketplace</li>
</ul><p><strong>Key considerations</strong>:</p>
<ul><li>Remote deployment requires the extension to implement the client-server communication</li>
<li>Reuse across different tools requires modular design and implementation</li>
</ul><h2 id="build-your-own-aipowered-features" data-needslink="build-your-own-aipowered-features">Build your own AI-powered features</h2>
<p>VS Code gives you direct programmatic access to AI models for creating custom AI-powered features in your extensions. This approach enables you to build editor-specific interactions that use AI capabilities without relying on the chat interface.</p>
<p>To use language models directly, use the <a href="/api/extension-guides/ai/language-model">Language Model API</a> within your VS Code extension. You can incorporate these AI capabilities into any extension feature, such as code actions, hover providers, custom views, and more.</p>
<p><strong>Key benefits</strong>:</p>
<ul><li>Integrate AI capabilities into existing extension features or build new ones</li>
<li>Running in the extension host process allows access to VS Code extension APIs</li>
<li>Easy distribution and deployment via the Visual Studio Marketplace</li>
</ul><p><strong>Key considerations</strong>:</p>
<ul><li>Reuse across different experiences requires modular design and implementation</li>
</ul><h2 id="decide-which-option-to-use" data-needslink="decide-which-option-to-use">Decide which option to use</h2>
<p>When choosing the right approach for extending AI in your VS Code extension, consider the following guidelines:</p>
<ol><li>
<p><strong>Choose Language Model Tool when</strong>:</p>
<ul><li>You want to extend chat in VS Code with specialized capabilities</li>
<li>You want automatic invocation based on user intent in agent mode</li>
<li>You want access to VS Code APIs for deep integration in VS Code</li>
<li>You want to distribute your tool through the VS Code Marketplace</li>
</ul></li>
<li>
<p><strong>Choose MCP Tool when</strong>:</p>
<ul><li>You want to extend chat in VS Code with specialized capabilities</li>
<li>You want automatic invocation based on user intent in agent mode</li>
<li>You don't need to integrate with VS Code APIs</li>
<li>Your tool needs to work across different environments (not just VS Code)</li>
<li>Your tool should run remotely or locally</li>
</ul></li>
<li>
<p><strong>Choose Chat Participant when</strong>:</p>
<ul><li>You want to extend ask mode with a specialized assistant with domain expertise</li>
<li>You need to customize the entire interaction flow and response behavior</li>
<li>You want access to VS Code APIs for deep integration in VS Code</li>
<li>You want to distribute your tool through the VS Code Marketplace</li>
</ul></li>
<li>
<p><strong>Choose Language Model API when</strong>:</p>
<ul><li>You want to integrate AI capabilities into existing extension features</li>
<li>You're building UI experiences outside the chat interface</li>
<li>You need direct programmatic control over AI model requests</li>
</ul></li>
</ol><h2 id="next-steps" data-needslink="next-steps">Next steps</h2>
<p>Choose the approach that best fits your extension's goals:</p>
<ul><li><a href="/api/extension-guides/ai/tools">Implement a language model tool</a></li>
<li><a href="/api/extension-guides/ai/mcp">Register MCP tools in your VS Code extension</a></li>
<li><a href="/api/extension-guides/ai/language-model">Integrate AI in your extension with the Language Model API</a></li>
<li><a href="/api/extension-guides/ai/chat">Implement a chat participant</a></li>
<li><a href="/api/references/vscode-api#InlineCompletionItemProvider">Extend code completions with the Inline Completions API</a></li>
</ul><h3 id="sample-projects" data-needslink="sample-projects">Sample projects</h3>
<ul><li><a href="https://github.com/microsoft/vscode-extension-samples/tree/main/chat-sample" class="external-link" target="_blank">Chat sample</a>: Extension with agent mode tool and chat participant</li>
<li><a href="/api/extension-guides/ai/chat-tutorial">Code tutor chat participant tutorial</a>: Building a specialized chat assistant</li>
<li><a href="/api/extension-guides/ai/language-model-tutorial">AI-powered code annotations tutorial</a>: Step-by-step guide for using the Language Model API</li>
<li><a href="https://github.com/microsoft/vscode-extension-samples/blob/main/mcp-extension-sample" class="external-link" target="_blank">MCP extension sample</a>: Extension that registers an MCP tool</li>
</ul><div class="feedback" data-edit-url="https://vscode.dev/github/microsoft/vscode-docs/blob/main/api/extension-guides/ai/ai-extensibility-overview.md"></div>
				
				<div class="body-footer">6/3/2026</div>
				
            </main><aside class="docs-right-sidebar hidden-xs"><div class="docs-markdown-actions">
                    <div class="docs-markdown-dropdown" data-raw-url="/raw/api/extension-guides/ai/ai-extensibility-overview.md">
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
                    <ul class="nav"><li><a href="#why-extend-ai-in-vs-code">Why extend AI in VS Code?</a></li>
                        
                        <li><a href="#extend-the-chat-experience">Extend the chat experience</a></li>
                        
                        <li><a href="#build-your-own-aipowered-features">Build your own AI-powered features</a></li>
                        
                        <li><a href="#decide-which-option-to-use">Decide which option to use</a></li>
                        
                        <li><a href="#next-steps">Next steps</a></li>
                        
                    </ul></nav></aside></div>
		<div class="docs-mobile-widgets visible-xs">
			<div class="connect-widget"></div>
		</div>
	</div>
</div>
		</main>