# Chat Participant API

> 源文档: [https://code.visualstudio.com/api/extension-guides/ai/chat](https://code.visualstudio.com/api/extension-guides/ai/chat)

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
			          
			        <li class="active">
			          <a href="/api/extension-guides/ai/chat" aria-label="Current Page: Chat Participant">Chat Participant</a>
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
				<select id="small-nav-dropdown" aria-label="topics"><option value="/api">Overview</option><optgroup label="Get Started"><option value="/api/get-started/your-first-extension">Your First Extension</option><option value="/api/get-started/extension-anatomy">Extension Anatomy</option><option value="/api/get-started/wrapping-up">Wrapping Up</option></optgroup><optgroup label="Extension Capabilities"><option value="/api/extension-capabilities/overview">Overview</option><option value="/api/extension-capabilities/common-capabilities">Common Capabilities</option><option value="/api/extension-capabilities/theming">Theming</option><option value="/api/extension-capabilities/extending-workbench">Extending Workbench</option></optgroup><optgroup label="Extension Guides"><option value="/api/extension-guides/overview">Overview</option><optgroup label="Extension Guides - AI"><option value="/api/extension-guides/ai/ai-extensibility-overview">AI Extensibility</option><option value="/api/extension-guides/ai/tools">Language Model Tool</option><option value="/api/extension-guides/ai/mcp">MCP Dev Guide</option><option value="/api/extension-guides/ai/chat" selected>Chat Participant</option><option value="/api/extension-guides/ai/chat-tutorial">Chat Tutorial</option><option value="/api/extension-guides/ai/language-model">Language Model</option><option value="/api/extension-guides/ai/language-model-tutorial">Language Model Tutorial</option><option value="/api/extension-guides/ai/language-model-chat-provider">Language Model Chat Provider</option><option value="/api/extension-guides/ai/prompt-tsx">Prompt TSX</option></optgroup><option value="/api/extension-guides/command">Command</option><option value="/api/extension-guides/color-theme">Color Theme</option><option value="/api/extension-guides/file-icon-theme">File Icon Theme</option><option value="/api/extension-guides/product-icon-theme">Product Icon Theme</option><option value="/api/extension-guides/tree-view">Tree View</option><option value="/api/extension-guides/webview">Webview</option><option value="/api/extension-guides/notebook">Notebook</option><option value="/api/extension-guides/custom-editors">Custom Editors</option><option value="/api/extension-guides/virtual-documents">Virtual Documents</option><option value="/api/extension-guides/virtual-workspaces">Virtual Workspaces</option><option value="/api/extension-guides/web-extensions">Web Extensions</option><option value="/api/extension-guides/workspace-trust">Workspace Trust</option><option value="/api/extension-guides/task-provider">Task Provider</option><option value="/api/extension-guides/scm-provider">Source Control</option><option value="/api/extension-guides/debugger-extension">Debugger Extension</option><option value="/api/extension-guides/markdown-extension">Markdown Extension</option><option value="/api/extension-guides/testing">Test Extension</option><option value="/api/extension-guides/custom-data-extension">Custom Data Extension</option><option value="/api/extension-guides/telemetry">Telemetry</option></optgroup><optgroup label="UX Guidelines"><option value="/api/ux-guidelines/overview">Overview</option><option value="/api/ux-guidelines/activity-bar">Activity Bar</option><option value="/api/ux-guidelines/sidebars">Sidebars</option><option value="/api/ux-guidelines/panel">Panel</option><option value="/api/ux-guidelines/status-bar">Status Bar</option><option value="/api/ux-guidelines/views">Views</option><option value="/api/ux-guidelines/editor-actions">Editor Actions</option><option value="/api/ux-guidelines/quick-picks">Quick Picks</option><option value="/api/ux-guidelines/command-palette">Command Palette</option><option value="/api/ux-guidelines/notifications">Notifications</option><option value="/api/ux-guidelines/webviews">Webviews</option><option value="/api/ux-guidelines/context-menus">Context Menus</option><option value="/api/ux-guidelines/walkthroughs">Walkthroughs</option><option value="/api/ux-guidelines/settings">Settings</option></optgroup><optgroup label="Language Extensions"><option value="/api/language-extensions/overview">Overview</option><option value="/api/language-extensions/syntax-highlight-guide">Syntax Highlight Guide</option><option value="/api/language-extensions/semantic-highlight-guide">Semantic Highlight Guide</option><option value="/api/language-extensions/snippet-guide">Snippet Guide</option><option value="/api/language-extensions/language-configuration-guide">Language Configuration Guide</option><option value="/api/language-extensions/programmatic-language-features">Programmatic Language Features</option><option value="/api/language-extensions/language-server-extension-guide">Language Server Extension Guide</option><option value="/api/language-extensions/embedded-languages">Embedded Languages</option></optgroup><optgroup label="Testing and Publishing"><option value="/api/working-with-extensions/testing-extension">Testing Extensions</option><option value="/api/working-with-extensions/publishing-extension">Publishing Extensions</option><option value="/api/working-with-extensions/bundling-extension">Bundling Extensions</option><option value="/api/working-with-extensions/continuous-integration">Continuous Integration</option></optgroup><optgroup label="Advanced Topics"><option value="/api/advanced-topics/extension-host">Extension Host</option><option value="/api/advanced-topics/remote-extensions">Remote Development and Codespaces</option><option value="/api/advanced-topics/using-proposed-api">Using Proposed API</option><option value="/api/advanced-topics/tslint-eslint-migration">Migrate from TSLint to ESLint</option><option value="/api/advanced-topics/python-extension-template">Python Extension Template</option></optgroup><optgroup label="References"><option value="/api/references/vscode-api">VS Code API</option><option value="/api/references/contribution-points">Contribution Points</option><option value="/api/references/activation-events">Activation Events</option><option value="/api/references/extension-manifest">Extension Manifest</option><option value="/api/references/commands">Built-In Commands</option><option value="/api/references/when-clause-contexts">When Clause Contexts</option><option value="/api/references/theme-color">Theme Color</option><option value="/api/references/icons-in-labels">Product Icon Reference</option><option value="/api/references/document-selector">Document Selector</option></optgroup></select></nav></aside><div class="docs-content-wrapper">
			
			<main class="docs-main-content body"><h1>Chat Participant API</h1>
<p>Chat participants are specialized assistants that enable users to extend <a href="/docs/chat/chat-overview">chat in VS Code</a> with domain-specific experts. Users invoke a chat participant by @-mentioning it, and the participant is then responsible for handling the user's natural language prompt.</p>
<p>In this extension guide, you learn how to create a chat participant by using the Chat Participant API.</p>
<p>VS Code has several built-in chat participants like <code>@vscode</code>, <code>@terminal</code>, or <code>@workspace</code>. They are optimized to answer questions about their respective domains.</p>
<p>Chat participants are different from <a href="/api/extension-guides/ai/tools">language model tools</a> that are invoked as part of the LLM orchestrating the steps needed to resolve the user's chat prompt. Chat participants receive the user's prompt and orchestrate the tasks that are needed themselves.</p>
<h2 id="why-implement-a-chat-participant-in-your-extension" data-needslink="why-implement-a-chat-participant-in-your-extension">Why implement a chat participant in your extension?</h2>
<p>Implementing a chat participant in your extension has several benefits:</p>
<ul><li><strong>Extend chat</strong> with specialized, domain-specific knowledge and expertise. For example, the built-in <code>@vscode</code> participant has knowledge about VS Code and its extension APIs.</li>
<li><strong>Own conversation</strong> by managing the end-to-end user chat prompt and response.</li>
<li><strong>Deeply integrate with VS Code</strong> by using the broad set of extension APIs. For example, use the <a href="/api/extension-guides/debugger-extension">debug APIs</a> to get the current debugging context and use it as part of the tool's functionality.</li>
<li><strong>Distribute and deploy</strong> chat participants via the Visual Studio Marketplace, providing a reliable and seamless experience for users. Users don't need a separate installation and update process.</li>
</ul><p>You might consider implementing a <a href="/api/extension-guides/ai/tools">language model tool</a> or <a href="/api/extension-guides/ai/mcp">MCP server</a> if you want to provide domain-specific capabilities that can be invoked automatically as part of an autonomous, agentic coding session. See the <a href="/api/extension-guides/ai/ai-extensibility-overview">AI Extensibility Overview</a> for details on the different options and how to decide which approach to use.</p>
<h2 id="parts-of-the-chat-user-experience" data-needslink="parts-of-the-chat-user-experience">Parts of the chat user experience</h2>
<p>The following screenshot shows the different chat concepts in the Visual Studio Code chat experience for the sample extension.</p>
<p><img src="/assets/api/extension-guides/ai/chat/chat.png" alt="Chat concepts explanation" loading="lazy"></p>
<ol><li>Use the <code>@</code> syntax to invoke the <code>@cat</code> chat participant</li>
<li>Use the <code>/</code> syntax to call the <code>/teach</code> command</li>
<li>User-provided query, also known as the user prompt</li>
<li>Icon and participant <code>fullName</code> that indicate that Copilot is using the <code>@cat</code> chat participant</li>
<li>Markdown response, provided by <code>@cat</code></li>
<li>Code fragment included in the markdown response</li>
<li>Button included in the <code>@cat</code> response, the button invokes a VS Code command</li>
<li>Suggested <a href="#_4-register-follow-up-requests">follow-up questions</a> provided by the chat participant</li>
<li>Chat input field with the placeholder text provided by the chat participant's <code>description</code> property</li>
</ol><h2 id="create-a-chat-participant" data-needslink="create-a-chat-participant">Create a chat participant</h2>
<p>Implementing a chat participant consists of the following parts:</p>
<ol><li>Define the chat participant in the <code>package.json</code> file of your extension.</li>
<li>Implement a request handler to process the user's chat prompt and return a response.</li>
<li>(Optional) Implement chat slash commands to provide users with a shorthand notation for common tasks.</li>
<li>(Optional) Define suggested follow-up questions.</li>
<li>(Optional) Implement participant detection where VS Code automatically routes a chat request to the appropriate chat participant without explicit mention from the user.</li>
</ol><p>You can get started with a <a href="https://github.com/microsoft/vscode-extension-samples/tree/main/chat-sample" class="external-link" target="_blank">basic example project</a>.</p>
<p><img src="/assets/api/extension-guides/ai/chat/diagram.png" alt="Diagram showing how extension can contribute to chat" loading="lazy"></p>
<h3 id="1.-register-the-chat-participant" data-needslink="1.-register-the-chat-participant">1. Register the chat participant</h3>
<p>The first step to create a chat extension is to register it in your <code>package.json</code>, with the following properties:</p>
<ul><li><code>id</code>: A unique identifier for the chat participant, as defined in the <code>package.json</code> file.</li>
<li><code>name</code>: A short name for the chat participant, used for @-mentions in the chat.</li>
<li><code>fullName</code>: The full name of the chat participant, displayed in the title area of the response.</li>
<li><code>description</code>: A brief description of the chat participant's purpose, used as placeholder text in the chat input field.</li>
<li><code>isSticky</code>: A boolean value indicating whether the chat participant is persistent in the chat input field after responding.</li>
</ul><pre class="shiki" data-lang="json" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"contributes"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">        "chatParticipants"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">            {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">                "id"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"chat-sample.my-participant"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">                "name"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"my-participant"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">                "fullName"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"My Participant"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">                "description"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"What can I teach you?"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">                "isSticky"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">true</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">            }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">        ]</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<p>We suggest using a lowercase <code>name</code> and using title case for the <code>fullName</code> to align with existing chat participants. Get more info about the <a href="#_chat-participant-naming-conventions">naming conventions for chat participants</a>.</p>
<div class="markdown-alert note" dir="auto">
      <span>
        <svg class="markdown-alert-icon" viewbox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8Zm8-6.5a6.5 6.5 0 1 0 0 13 6.5 6.5 0 0 0 0-13ZM6.5 7.75A.75.75 0 0 1 7.25 7h1a.75.75 0 0 1 .75.75v2.75h.25a.75.75 0 0 1 0 1.5h-2a.75.75 0 0 1 0-1.5h.25v-2h-.25a.75.75 0 0 1-.75-.75ZM8 6a1 1 0 1 1 0-2 1 1 0 0 1 0 2Z"></path></svg>
        Note
      </span><p>Some participant names are reserved. If you use such a reserved name, VS Code displays the fully qualified name of your chat participant (including the extension ID).</p>
</div><h3 id="2.-implement-a-request-handler" data-needslink="2.-implement-a-request-handler">2. Implement a request handler</h3>
<p>Implement the chat participant by using the <a href="/api/references/vscode-api#chat">Chat Participant API</a>. This consists of the following steps:</p>
<ol><li>
<p>On activation of the extension, create the participant with <code>vscode.chat.createChatParticipant</code>.</p>
<p>Provide the ID, which you defined in <code>package.json</code>, and a reference to the request handler that you implement in the next step.</p>
<pre class="shiki" data-lang="typescript" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">export</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> function</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> activate</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">context</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">ExtensionContext</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">  // Register the chat participant and its request handler</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">  const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> cat</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">chat</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">createChatParticipant</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'chat-sample.my-participant'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">handler</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">  // Optionally, set some properties for @cat</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  cat</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">iconPath</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">Uri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">joinPath</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">context</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">extensionUri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'cat.jpeg'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">  // Add the chat request handler here</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
</li>
<li>
<p>In the <code>activate</code> function, define the <code>vscode.ChatRequestHandler</code> request handler.</p>
<p>The request handler is responsible for processing the user's chat requests in the VS Code Chat view. Each time a user enters a prompt in the chat input field, the chat request handler is invoked.</p>
<pre class="shiki" data-lang="typescript" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">const</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> handler</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">ChatRequestHandler</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">async</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> (</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  request</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">ChatRequest</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  context</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">ChatContext</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  stream</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">ChatResponseStream</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  token</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">CancellationToken</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">): </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">Promise</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">&lt;</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">ICatChatResult</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">&gt; </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">=&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">  // Chat request handler implementation goes here</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">};</span></span>
<span class="line"></span></code></pre>
</li>
<li>
<p>Determine the user's intent from <code>vscode.ChatRequest</code>.</p>
<p>To determine the intent of the user's request, you can reference the <code>vscode.ChatRequest</code> parameter to access the user's prompt text, commands, and chat location.</p>
<p>Optionally, you can take advantage of the language model to determine the user's intent, rather than using traditional logic. As part of the <code>request</code> object you get a language model instance that the user picked in the chat model dropdown. Learn how you can use the <a href="/api/extension-guides/ai/language-model">Language Model API</a> in your extension.</p>
<p>The following code snippet shows the basic structure of first using the command, and then the user prompt to determine the user intent:</p>
<pre class="shiki" data-lang="typescript" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">const</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> handler</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">ChatRequestHandler</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">async</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> (</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  request</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">ChatRequest</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  context</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">ChatContext</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  stream</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">ChatResponseStream</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  token</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">CancellationToken</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">): </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">Promise</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">&lt;</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">ICatChatResult</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">&gt; </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">=&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">  // Test for the `teach` command</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">  if</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> (</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">request</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">command</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> == </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'teach'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">    // Add logic here to handle the teaching scenario</span></span>
<span class="line"><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">    doTeaching</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">request</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">prompt</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">request</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">variables</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  } </span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">else</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">    // Determine the user's intent</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">    const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> intent</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">determineUserIntent</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">request</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">prompt</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">request</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">variables</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">request</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">model</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">    // Add logic here to handle other scenarios</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">};</span></span>
<span class="line"></span></code></pre>
</li>
<li>
<p>Add logic to process the user request.</p>
<p>Often, chat extensions use the <code>request.model</code> language model instance to process the request. In this case, you might adjust the language model prompt to match the user's intent.</p>
<p>Alternately, you can implement the extension logic by invoking a backend service, by using traditional programming logic, or by using a combination of all these options. For example, you could invoke a web search to gather additional information, which you then provide as context to the language model.</p>
<p>While processing the current request, you might want to refer to previous chat messages. For example, if a previous response returned a C# code snippet, the user's current request might be "give the code in Python". <a href="#_use-the-chat-message-history">Learn how you can use the chat message history</a>.</p>
<p>If you want to process a request differently based on the location of the chat input (Chat view, Quick Chat, inline chat), you can use the <code>location</code> property of the <code>vscode.ChatRequest</code>. For example, if the user sends a request from the terminal inline chat, you might look up a shell command. Whereas, if the user uses the Chat view, you could return a more elaborate response.</p>
</li>
<li>
<p>Return the chat response to the user.</p>
<p>Once you've processed the request, you have to return a response to the user in the Chat view. You can use streaming to respond to user queries.</p>
<p>Responses can contain different content types: Markdown, images, references, progress, buttons, and file trees.</p>
<p><img src="/assets/api/extension-guides/ai/chat/stream.png" alt="Response from the cat extension that includes code, markdown and a button" loading="lazy"></p>
<p>An extension can use the response stream in the following way:</p>
<pre class="shiki" data-lang="typescript" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">stream</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">progress</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'Picking the right topic to teach...'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">stream</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">markdown</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">`</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\`\`\`</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">typescript</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">const myStack = new Stack();</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">myStack.push(1); // pushing a number on the stack (or let's say, adding a fish to the stack)</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">myStack.push(2); // adding another fish (number 2)</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">console.log(myStack.pop()); // eating the top fish, will output: 2</span></span>
<span class="line"><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\`\`\`</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">So remember, Code Kitten, in a stack, the last fish in is the first fish out - which we tech cats call LIFO (Last In, First Out).`</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">stream</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">button</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">({</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  command:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'cat.meow'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  title:</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">l10n</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">t</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'Meow!'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">),</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  arguments:</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> []</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">});</span></span>
<span class="line"></span></code></pre>
<p>Get more info about the <a href="#_supported-chat-response-output-types">supported chat response output types</a>.</p>
<p>In practice, extensions typically send a request to the language model. Once they get a response from the language model, they might further process it, and decide if they should stream anything back to the user. The VS Code Chat API is streaming-based, and is compatible with the streaming <a href="/api/extension-guides/ai/language-model">Language Model API</a>. This allows extensions to report progress and results continuously with the goal of having a smooth user experience. Learn how you can use the <a href="/api/extension-guides/ai/language-model">Language Model API</a>.</p>
</li>
</ol><h3 id="3.-register-slash-commands" data-needslink="3.-register-slash-commands">3. Register slash commands</h3>
<p>A chat participant can contribute slash commands, which are shortcuts to specific functionality provided by the extension. Users can reference slash commands in chat by using the <code>/</code> syntax, for example <code>/explain</code>.</p>
<p>One of the tasks when answering questions is to determine the user intent. For example, VS Code could infer that <code>Create a new workspace with Node.js Express Pug TypeScript</code> means that you want a new project, but <code>@workspace /new Node.js Express Pug TypeScript</code> is more explicit, concise, and saves typing time. If you type <code>/</code> in the chat input field, VS Code offers a list of registered commands with their description.</p>
<p><img src="/assets/api/extension-guides/ai/chat/commands.png" alt="List of commands in chat for @workspace" loading="lazy"></p>
<p>Chat participants can contribute slash commands with their description by adding them in <code>package.json</code>:</p>
<pre class="shiki" data-lang="typescript" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"contributes"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">    "chatParticipants"</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">:</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> [</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">        {</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">            "id"</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> "chat-sample.cat"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">            "name"</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> "cat"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">            "fullName"</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> "Cat"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">            "description"</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> "Meow! What can I teach you?"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">            "isSticky"</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">:</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> true</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">            "commands"</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">:</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> [</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">                {</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">                    "name"</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> "teach"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">                    "description"</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> "Pick at random a computer science concept then explain it in purfect way of a cat"</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">                },</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">                {</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">                    "name"</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> "play"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">                    "description"</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> "Do whatever you want, you are a cat after all"</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">                }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">            ]</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">        }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    ]</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<p>Get more info about the <a href="#_slash-command-naming-conventions">naming conventions for slash commands</a>.</p>
<h3 id="4.-register-followup-requests" data-needslink="4.-register-followup-requests">4. Register follow-up requests</h3>
<p>After each chat request, VS Code invokes follow-up providers to get suggested follow-up questions to show to the user. The user can then select the follow-up question, and immediately send it to the chat extension. Use the <a href="/api/references/vscode-api#ChatFollowupProvider"><code>ChatFollowupProvider</code></a> API to register follow-up prompts of type <a href="/api/references/vscode-api#ChatFollowup"><code>ChatFollowup</code></a>.</p>
<p>The following code snippet shows how to register follow-up requests in a chat extension:</p>
<pre class="shiki" data-lang="typescript" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">cat</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">followupProvider</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = {</span></span>
<span class="line"><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">    provideFollowups</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">result</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">ICatChatResult</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">context</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">ChatContext</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">token</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">CancellationToken</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">        if</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> (</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">result</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">metadata</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">command</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> === </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'teach'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">            return</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> [{</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">                prompt:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'let us play'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">                label:</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">l10n</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">t</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'Play with the cat'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">)</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">            } </span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">satisfies</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99"> vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">ChatFollowup</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">];</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">        }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">};</span></span>
<span class="line"></span></code></pre>
<div class="markdown-alert tip" dir="auto">
      <span>
        <svg class="markdown-alert-icon" viewbox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path d="M8 1.5c-2.363 0-4 1.69-4 3.75 0 .984.424 1.625.984 2.304l.214.253c.223.264.47.556.673.848.284.411.537.896.621 1.49a.75.75 0 0 1-1.484.211c-.04-.282-.163-.547-.37-.847a8.456 8.456 0 0 0-.542-.68c-.084-.1-.173-.205-.268-.32C3.201 7.75 2.5 6.766 2.5 5.25 2.5 2.31 4.863 0 8 0s5.5 2.31 5.5 5.25c0 1.516-.701 2.5-1.328 3.259-.095.115-.184.22-.268.319-.207.245-.383.453-.541.681-.208.3-.33.565-.37.847a.751.751 0 0 1-1.485-.212c.084-.593.337-1.078.621-1.489.203-.292.45-.584.673-.848.075-.088.147-.173.213-.253.561-.679.985-1.32.985-2.304 0-2.06-1.637-3.75-4-3.75ZM5.75 12h4.5a.75.75 0 0 1 0 1.5h-4.5a.75.75 0 0 1 0-1.5ZM6 15.25a.75.75 0 0 1 .75-.75h2.5a.75.75 0 0 1 0 1.5h-2.5a.75.75 0 0 1-.75-.75Z"></path></svg>
        Tip
      </span><p>Follow-ups should be written as questions or directions, not just concise commands.</p>
</div><h3 id="5.-implement-participant-detection" data-needslink="5.-implement-participant-detection">5. Implement participant detection</h3>
<p>To make it easier to use chat participants with natural language, you can implement participant detection. Participant detection is a way to automatically route the user's question to a suitable participant, without having to explicitly mention the participant in the prompt. For example, if the user asks "How do I add a login page to my project?", the question would be automatically routed to the <code>@workspace</code> participant because it can answer questions about the user's project.</p>
<p>VS Code uses the chat participant description and examples to determine which participant to route a chat prompt to. You can specify this information in the <code>disambiguation</code> property in the extension <code>package.json</code> file. The <code>disambiguation</code> property contains a list of detection categories, each with a description and examples.</p>
<table class="table table-striped"><thead><tr><th>Property</th>
<th>Description</th>
<th>Examples</th>
</tr></thead><tbody><tr><td><code>category</code></td>
<td>The detection category. If the participant serves different purposes, you can have a category for each.</td>
<td><ul><li><code>cat</code></li><li><code>workspace_questions</code></li><li><code>web_questions</code></li></ul></td>
</tr><tr><td><code>description</code></td>
<td>A detailed description of the kinds of questions that are suitable for this participant.</td>
<td><ul><li><code>The user wants to learn a specific computer science topic in an informal way.</code></li><li><code>The user just wants to relax and see the cat play.</code></li></ul></td>
</tr><tr><td><code>examples</code></td>
<td>A list of representative example questions.</td>
<td><ul><li><code>Teach me C++ pointers using metaphors</code></li><li><code>Explain to me what is a linked list in a simple way</code></li><li><code>Can you show me a cat playing with a laser pointer?</code></li></ul></td>
</tr></tbody></table><p>You can define participant detection for the overall chat participant, for specific commands, or a combination of both.</p>
<p>The following code snippet shows how to implement participant detection at the participant level.</p>
<pre class="shiki" data-lang="json" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"contributes"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "chatParticipants"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">        {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">            "id"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"chat-sample.cat"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">            "fullName"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"Cat"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">            "name"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"cat"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">            "description"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"Meow! What can I teach you?"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">            "disambiguation"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">                {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">                    "category"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"cat"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">                    "description"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"The user wants to learn a specific computer science topic in an informal way."</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">                    "examples"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">                        "Teach me C++ pointers using metaphors"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">                        "Explain to me what is a linked list in a simple way"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">                        "Can you explain to me what is a function in programming?"</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">                    ]</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">                }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">            ]</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">        }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    ]</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<p>Similarly, you can also configure participant detection at the command level by adding a <code>disambiguation</code> property for one or more items in the <code>commands</code> property.</p>
<p>Apply the following guidelines to improve the accuracy of participant detection for your extension:</p>
<ul><li><strong>Be specific</strong>: The description and examples should be as specific as possible to avoid conflicts with other participants. Avoid using generic terminology in the participant and command information.</li>
<li><strong>Use examples</strong>: The examples should be representative of the kinds of questions that are suitable for the participant. Use synonyms and variations to cover a wide range of user queries.</li>
<li><strong>Use natural language</strong>: The description and examples should be written in natural language, as if you were explaining the participant to a user.</li>
<li><strong>Test the detection</strong>: Test the participant detection with a variation of example questions and verify there's no conflict with built-in chat participants.</li>
</ul><div class="markdown-alert note" dir="auto">
      <span>
        <svg class="markdown-alert-icon" viewbox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8Zm8-6.5a6.5 6.5 0 1 0 0 13 6.5 6.5 0 0 0 0-13ZM6.5 7.75A.75.75 0 0 1 7.25 7h1a.75.75 0 0 1 .75.75v2.75h.25a.75.75 0 0 1 0 1.5h-2a.75.75 0 0 1 0-1.5h.25v-2h-.25a.75.75 0 0 1-.75-.75ZM8 6a1 1 0 1 1 0-2 1 1 0 0 1 0 2Z"></path></svg>
        Note
      </span><p>Built-in chat participants take precedence for participant detection. For example, a chat participant that operates on workspace files might conflict with the built-in <code>@workspace</code> participant.</p>
</div><h2 id="use-the-chat-message-history" data-needslink="use-the-chat-message-history">Use the chat message history</h2>
<p>Participants have access to the message history of the current chat session. A participant can only access messages where it was mentioned. A <code>history</code> item is either a <code>ChatRequestTurn</code> or a <code>ChatResponseTurn</code>. For example, use the following code snippet to retrieve all the previous requests that the user sent to your participant in the current chat session:</p>
<pre class="shiki" data-lang="typescript" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> previousMessages</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">context</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">history</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">filter</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">h</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> =&gt;</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> h</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> instanceof</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99"> vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">ChatRequestTurn</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"></span></code></pre>
<p>History will not be automatically included in the prompt, it is up to the participant to decide if it wants to add history as additional context when passing messages to the language model.</p>
<h2 id="supported-chat-response-output-types" data-needslink="supported-chat-response-output-types">Supported chat response output types</h2>
<p>To return a response to a chat request, you use the <a href="/api/references/vscode-api#ChatResponseStream"><code>ChatResponseStream</code></a> parameter on the <a href="/api/references/vscode-api#ChatRequestHandler"><code>ChatRequestHandler</code></a>.</p>
<p>The following list provides the output types for a chat response in the Chat view. A chat response can combine multiple different output types.</p>
<ul><li>
<p><strong>Markdown</strong></p>
<p>Render a fragment of Markdown text simple text or images. You can use any Markdown syntax that is part of the <a href="https://commonmark.org/" class="external-link" target="_blank">CommonMark</a> specification. Use the <a href="/api/references/vscode-api#ChatResponseStream.markdown"><code>ChatResponseStream.markdown</code></a> method and provide the Markdown text.</p>
<p>Example code snippet:</p>
<pre class="shiki" data-lang="typescript" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">// Render Markdown text</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">stream</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">markdown</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'# This is a title </span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\n</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">stream</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">markdown</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'This is stylized text that uses _italics_ and **bold**. '</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">stream</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">markdown</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'This is a [link](https://code.visualstudio.com).</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\n\n</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">stream</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">markdown</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'![VS Code](https://code.visualstudio.com/assets/favicon.ico)'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"></span></code></pre>
</li>
<li>
<p><strong>Code block</strong></p>
<p>Render a code block that supports IntelliSense, code formatting, and interactive controls to apply the code to the active editor. To show a code block, use the <a href="/api/references/vscode-api#ChatResponseStream.markdown"><code>ChatResponseStream.markdown</code></a> method and apply the Markdown syntax for code blocks (using backticks).</p>
<p>Example code snippet:</p>
<pre class="shiki" data-lang="typescript" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">// Render a code block that enables users to interact with</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">stream</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">markdown</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'```bash</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\n</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">stream</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">markdown</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'```ls -l</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\n</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">stream</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">markdown</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'```'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"></span></code></pre>
</li>
<li>
<p><strong>Command link</strong></p>
<p>Render a link inline in the chat response that users can select to invoke a VS Code command. To show a command link, use the <a href="/api/references/vscode-api#ChatResponseStream.markdown"><code>ChatResponseStream.markdown</code></a> method and use the Markdown syntax for links <code>[link text](command:commandId)</code>, where you provide the command ID in the URL. For example, the following link opens the Command Palette: <code>[Command Palette](command:workbench.action.showCommands)</code>.</p>
<p>To protect against command injection when you load the Markdown text from a service, you have to use a <a href="/api/references/vscode-api#MarkdownString"><code>vscode.MarkdownString</code></a> object with the <code>isTrusted</code> property set to the list of trusted VS Code command IDs. This property is required to enable the command link to work. If the <code>isTrusted</code> property is not set or a command is not listed, the command link will not work.</p>
<p>Example code snippet:</p>
<pre class="shiki" data-lang="typescript" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">// Use command URIs to link to commands from Markdown</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">let</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> markdownCommandString</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">MarkdownString</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">new</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">MarkdownString</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">  `[Use cat names](command:</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">${</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1">CAT_NAMES_COMMAND_ID</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">)`</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">markdownCommandString</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">isTrusted</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = { </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">enabledCommands:</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> [</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1">CAT_NAMES_COMMAND_ID</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">] };</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">stream</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">markdown</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">markdownCommandString</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"></span></code></pre>
<p>If the command takes arguments, you need to first JSON encode the arguments and then encode the JSON string as a URI component. You then append the encoded arguments as a query string to the command link.</p>
<pre class="shiki" data-lang="typescript" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">// Encode the command arguments</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> encodedArgs</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">encodeURIComponent</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1">JSON</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">stringify</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">args</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">));</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">// Use command URIs with arguments to link to commands from Markdown</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">let</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> markdownCommandString</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">MarkdownString</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">new</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">MarkdownString</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">  `[Use cat names](command:</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">${</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1">CAT_NAMES_COMMAND_ID</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">?</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">${</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">encodedArgs</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">)`</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">markdownCommandString</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">isTrusted</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = { </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">enabledCommands:</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> [</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1">CAT_NAMES_COMMAND_ID</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">] };</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">stream</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">markdown</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">markdownCommandString</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"></span></code></pre>
</li>
<li>
<p><strong>Command button</strong></p>
<p>Render a button that invokes a VS Code command. The command can be a built-in command or one that you define in your extension. Use the <a href="/api/references/vscode-api#ChatResponseStream.button"><code>ChatResponseStream.button</code></a> method and provide the button text and command ID.</p>
<p>Example code snippet:</p>
<pre class="shiki" data-lang="typescript" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">// Render a button to trigger a VS Code command</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">stream</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">button</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">({</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  command:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'my.command'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  title:</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">l10n</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">t</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'Run my command'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">)</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">});</span></span>
<span class="line"></span></code></pre>
</li>
<li>
<p><strong>File tree</strong></p>
<p>Render a file tree control that lets users preview individual files. For example, to show a workspace preview when proposing to create a new workspace. Use the <a href="/api/references/vscode-api#ChatResponseStream.filetree"><code>ChatResponseStream.filetree</code></a> method and provide an array of file tree elements and the base location (folder) of the files.</p>
<p>Example code snippet:</p>
<pre class="shiki" data-lang="typescript" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">// Create a file tree instance</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">var</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> tree</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">ChatResponseFileTree</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">[] = [</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    name:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'myworkspace'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    children:</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> [{ </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">name:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'README'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> }, { </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">name:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'app.js'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> }, { </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">name:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'package.json'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> }]</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">];</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">// Render the file tree control at a base location</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">stream</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">filetree</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">tree</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">baseLocation</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"></span></code></pre>
</li>
<li>
<p><strong>Progress message</strong></p>
<p>Render a progress message during a long-running operation to provide the user with intermediate feedback. For example, to report the completion of each step in a multi-step operation. Use the <a href="/api/references/vscode-api#ChatResponseStream.progress"><code>ChatResponseStream.progress</code></a> method and provide the message.</p>
<p>Example code snippet:</p>
<pre class="shiki" data-lang="typescript" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">// Render a progress message</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">stream</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">progress</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'Connecting to the database.'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"></span></code></pre>
</li>
<li>
<p><strong>Reference</strong></p>
<p>Add a reference for an external URL or editor location in the list references to indicate which information you use as context. Use the <a href="/api/references/vscode-api#ChatResponseStream.reference"><code>ChatResponseStream.reference</code></a> method and provide the reference location.</p>
<p>Example code snippet:</p>
<pre class="shiki" data-lang="typescript" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> fileUri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">Uri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">Uri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">file</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'/path/to/workspace/app.js'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">); </span><span style="--shiki-dark:#6A9955;--shiki-light:#008000">// On Windows, the path should be in the format of 'c:\\path\\to\\workspace\\app.js'</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> fileRange</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">Range</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">new</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">Range</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#B5CEA8;--shiki-light:#098658">0</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#B5CEA8;--shiki-light:#098658">0</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#B5CEA8;--shiki-light:#098658">3</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#B5CEA8;--shiki-light:#098658">0</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> externalUri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">Uri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">Uri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">parse</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'https://code.visualstudio.com'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">// Add a reference to an entire file</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">stream</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">reference</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">fileUri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">// Add a reference to a specific selection within a file</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">stream</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">reference</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">new</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">Location</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">fileUri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">fileRange</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">));</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">// Add a reference to an external URL</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">stream</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">reference</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">externalUri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"></span></code></pre>
</li>
<li>
<p><strong>Inline reference</strong></p>
<p>Add an inline reference to a URI or editor location. Use the <a href="/api/references/vscode-api#ChatResponseStream.anchor"><code>ChatResponseStream.anchor</code></a> method and provide the anchor location and optional title. To reference a symbol (for example, a class or variable), you would use a location in an editor.</p>
<p>Example code snippet:</p>
<pre class="shiki" data-lang="typescript" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> symbolLocation</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">Uri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">Uri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">parse</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'location-to-a-symbol'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">// Render an inline anchor to a symbol in the workspace</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">stream</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">anchor</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">symbolLocation</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'MySymbol'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"></span></code></pre>
</li>
</ul><blockquote><p><strong>Important</strong>: Images and links are only available when they originate from a domain that is in the trusted domain list. Get more info about <a href="/docs/editing/editingevolved#outgoing-link-protection">link protection in VS Code</a>.</p>
</blockquote><h2 id="implement-tool-calling" data-needslink="implement-tool-calling">Implement tool calling</h2>
<p>To respond to a user request, a chat extension can invoke language model tools. Learn more about <a href="/api/extension-guides/ai/tools">language model tools</a> and the <a href="/api/extension-guides/ai/tools#toolcalling-flow">tool-calling flow</a>.</p>
<p>You can implement tool calling in two ways:</p>
<ul><li>By using the <a href="https://www.npmjs.com/package/@vscode/chat-extension-utils" class="external-link" target="_blank"><code>@vscode/chat-extension-utils</code> library</a> to simplify the process of calling tools in a chat extension.</li>
<li>By implementing tool calling yourself, which gives you more control over the tool-calling process. For example, to perform additional validation or to handle tool responses in a specific way before sending them to the LLM.</li>
</ul><h3 id="implement-tool-calling-with-the-chat-extension-library" data-needslink="implement-tool-calling-with-the-chat-extension-library">Implement tool calling with the chat extension library</h3>
<p>You can use the <a href="https://www.npmjs.com/package/@vscode/chat-extension-utils" class="external-link" target="_blank"><code>@vscode/chat-extension-utils</code> library</a> to simplify the process of calling tools in a chat extension.</p>
<p>Implement tool calling in the <code>vscode.ChatRequestHandler</code> function of your <a href="/api/extension-guides/ai/chat">chat participant</a>.</p>
<ol><li>
<p>Determine the relevant tools for the current chat context. You can access all available tools by using <code>vscode.lm.tools</code>.</p>
<p>The following code snippet shows how to filter the tools to only those that have a specific tag.</p>
<pre class="shiki" data-lang="ts" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> tools</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> =</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  request</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">command</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> === </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'all'</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    ? </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">lm</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">tools</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    : </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">lm</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">tools</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">filter</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">tool</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> =&gt;</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> tool</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">tags</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">includes</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'chat-tools-sample'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">));</span></span>
<span class="line"></span></code></pre>
</li>
<li>
<p>Send the request and tool definitions to the LLM by using <code>sendChatParticipantRequest</code>.</p>
<pre class="shiki" data-lang="ts" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> libResult</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">chatUtils</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">sendChatParticipantRequest</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  request</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  chatContext</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    prompt:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'You are a cat! Answer as a cat.'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    responseStreamOptions:</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">      stream</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">      references:</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> true</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">      responseText:</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> true</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    },</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    tools</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  },</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  token</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"></span></code></pre>
<p>The <code>ChatHandlerOptions</code> object has the following properties:</p>
<ul><li><code>prompt</code>: (optional) Instructions for the chat participant prompt.</li>
<li><code>model</code>: (optional) The model to use for the request. If not specified, the model from the chat context is used.</li>
<li><code>tools</code>: (optional) The list of tools to consider for the request.</li>
<li><code>requestJustification</code>: (optional) A string that describes why the request is being made.</li>
<li><code>responseStreamOptions</code>: (optional) Enable <code>sendChatParticipantRequest</code> to stream the response back to VS Code. Optionally, you can also enable references and/or response text.</li>
</ul></li>
<li>
<p>Return the result from the LLM. This might contain error details or tool-calling metadata.</p>
<pre class="shiki" data-lang="ts" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">return</span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB"> await</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> libResult</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">result</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"></span></code></pre>
</li>
</ol><p>The full source code of this <a href="https://github.com/microsoft/vscode-extension-samples/blob/main/chat-sample/src/chatUtilsSample.ts" class="external-link" target="_blank">tool-calling sample</a> is available in the VS Code Extension Samples repository.</p>
<h3 id="implement-tool-calling-yourself" data-needslink="implement-tool-calling-yourself">Implement tool calling yourself</h3>
<p>For more advanced scenarios, you can also implement tool calling yourself. Optionally, you can use the <code>@vscode/prompt-tsx</code> library for crafting the LLM prompts. By implementing tool calling yourself, you have more control over the tool-calling process. For example, to perform additional validation or to handle tool responses in a specific way before sending them to the LLM.</p>
<p>View the full source code for implementing <a href="https://github.com/microsoft/vscode-extension-samples/blob/main/chat-sample/src/toolParticipant.ts" class="external-link" target="_blank">tool calling by using prompt-tsx</a> in the VS Code Extension Samples repository.</p>
<h2 id="measuring-success" data-needslink="measuring-success">Measuring success</h2>
<p>We recommend that you measure the success of your participant by adding telemetry logging for <code>Unhelpful</code> user feedback events, and for the total number of requests that your participant handled. An initial participant success metric can then be defined as: <code>unhelpful_feedback_count / total_requests</code>.</p>
<pre class="shiki" data-lang="typescript" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> logger</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">env</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">createTelemetryLogger</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">({</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">  // telemetry logging implementation goes here</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">});</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">cat</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">onDidReceiveFeedback</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">((</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">feedback</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">ChatResultFeedback</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">=&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">  // Log chat result feedback to be able to compute the success metric of the participant</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  logger</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">logUsage</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'chatResultFeedback'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    kind:</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> feedback</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">kind</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  });</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">});</span></span>
<span class="line"></span></code></pre>
<p>Any other user interaction with your chat response should be measured as a positive metric (for example, the user selecting a button that was generated in a chat response). Measuring success with telemetry is crucial when working with AI, since it is a nondeterministic technology. Run experiments, measure and iteratively improve your participant to ensure a good user experience.</p>
<h2 id="guidelines-and-conventions" data-needslink="guidelines-and-conventions">Guidelines and conventions</h2>
<h3 id="guidelines" data-needslink="guidelines">Guidelines</h3>
<p>Chat participants should not be purely question-answering bots. When building a chat participant, be creative and use the existing VS Code API to create rich integrations in VS Code. Users also love rich and convenient interactions, such as buttons in your responses, menu items that bring users to your participant in chat. Think about real life scenarios where AI can help your users.</p>
<p>It doesn't make sense for every extension to contribute a chat participant. Having too many participants in chat might lead to a bad user experience. Chat participants are best when you want to control the full prompt, including instructions to the language model. You can reuse the carefully crafted Copilot system message and you can contribute context to other participants.</p>
<p>For example, language extensions (such as the C++ extension) can contribute in various other ways:</p>
<ul><li>Contribute tools that bring language service smarts to the user query. For example, the C++ extension could resolve the <code>#cpp</code> tool to the C++ state of the workspace. This gives the Copilot language model the right C++ context to improve the quality of Copilot answers for C++.</li>
<li>Contribute smart actions that use the language model, optionally in combination with traditional language service knowledge, to deliver a great user experience. For example, C++ might already offer an "extract to method" smart action that uses the language model to generate a fitting default name for the new method.</li>
</ul><p>Chat extensions should explicitly ask for user consent if they are about to do a costly operation or are about to edit or delete something that can't be undone. To have a great user experience, we discourage extensions from contributing multiple chat participants. Up to one chat participant per extension is a simple model that scales well in the UI.</p>
<h3 id="chat-participant-naming-conventions" data-needslink="chat-participant-naming-conventions">Chat participant naming conventions</h3>
<table class="table table-striped"><thead><tr><th>Property</th>
<th>Description</th>
<th>Naming guidelines</th>
</tr></thead><tbody><tr><td><code>id</code></td>
<td>Globally unique identifier for the chat participant</td>
<td><ul><li>String value</li><li>Use the extension name as a prefix, followed by a unique ID for your extension</li><li>Example: <code>chat-sample.cat</code>, <code>code-visualizer.code-visualizer-participant</code></li></ul></td>
</tr><tr><td><code>name</code></td>
<td>Name of the chat participant, referenced by users through the <code>@</code> symbol</td>
<td><ul><li>String value consisting of alphanumeric characters, underscores, and hyphens</li><li>It's recommended to only use lowercase to ensure consistency with existing chat participants</li><li>Ensure the purpose of the participant is obvious from its name by referencing your company name or its functionality</li><li>Some participant names are reserved. If you use a reserved name, the fully qualified name is shown, including the extension ID</li><li>Examples: <code>vscode</code>, <code>terminal</code>, <code>code-visualizer</code></li></ul></td>
</tr><tr><td><code>fullName</code></td>
<td>(Optional) The full name of the participant, which is shown as the label for responses coming from the participant</td>
<td><ul><li>String value</li><li>It's recommended to use <a href="https://en.wikipedia.org/wiki/Title_case" class="external-link" target="_blank">title case</a></li><li>Use your company name, brand name, or user-friendly name for your participant</li><li>Examples: <code>GitHub Copilot</code>, <code>VS Code</code>, <code>Math Tutor</code></li></ul></td>
</tr><tr><td><code>description</code></td>
<td>(Optional) Short description of what the chat participant does, shown as placeholder text in the chat input field or in the list of participants</td>
<td><ul><li>String value</li><li>It's recommended to use sentence case, without punctuation at the end</li><li>Keep the description short to avoid horizontal scrolling</li><li>Examples: <code>Ask questions about VS Code</code>, <code>Generate UML diagrams for your code</code></li></ul></td>
</tr></tbody></table><p>When referring to your chat participant in any of the user-facing elements, such as properties, chat responses, or chat user interface, it's recommended to not use the term <em>participant</em>, as it's the name of the API. For example, the <code>@cat</code> extension could be called "Cat extension for GitHub Copilot".</p>
<h3 id="slash-command-naming-conventions" data-needslink="slash-command-naming-conventions">Slash command naming conventions</h3>
<table class="table table-striped"><thead><tr><th>Property</th>
<th>Description</th>
<th>Naming guidelines</th>
</tr></thead><tbody><tr><td><code>name</code></td>
<td>Name of the slash command, referenced by users through the <code>/</code> symbol</td>
<td><ul><li>String value</li><li>It's recommended to use <a href="https://en.wikipedia.org/wiki/Camel_case" class="external-link" target="_blank">lower camel case</a> to align with existing slash commands</li><li>Ensure the purpose of the command is obvious from its name</li><li>Examples: <code>fix</code>, <code>explain</code>, <code>runCommand</code></li></ul></td>
</tr><tr><td><code>description</code></td>
<td>(Optional) Short description of what the slash command does, shown as placeholder text in the chat input field or in the list of participants and commands</td>
<td><ul><li>String value</li><li>It's recommended to use sentence case, without punctuation at the end</li><li>Keep the description short to avoid horizontal scrolling</li><li>Examples: <code>Search for and execute a command in VS Code</code>, <code>Generate unit tests for the selected code</code></li></ul></td>
</tr></tbody></table><h2 id="publishing-your-extension" data-needslink="publishing-your-extension">Publishing your extension</h2>
<p>Once you have created your AI extension, you can publish your extension to the Visual Studio Marketplace:</p>
<ul><li>Before publishing to the VS Marketplace we recommend that you read the <a href="https://www.microsoft.com/en-us/ai/tools-practices" class="external-link" target="_blank">Microsoft AI tools and practices guidelines</a>. These guidelines provide best practices for the responsible development and use of AI technologies.</li>
<li>By publishing to the VS Marketplace, your extension is adhering to the <a href="https://docs.github.com/en/early-access/copilot/github-copilot-extensibility-platform-partnership-plugin-acceptable-development-and-use-policy" class="external-link" target="_blank">GitHub Copilot extensibility acceptable development and use policy</a>.</li>
<li>Upload to the Marketplace as described in <a href="https://code.visualstudio.com/api/working-with-extensions/publishing-extension">Publishing Extension</a>.</li>
<li>If your extension already contributes functionality other than chat, we recommend that you do not introduce an extension dependency on GitHub Copilot in the <a href="/api/references/extension-manifest">extension manifest</a>. This ensures that extension users that do not use GitHub Copilot can use the non-chat functionality without having to install GitHub Copilot.</li>
</ul><h2 id="extending-github-copilot-via-github-apps" data-needslink="extending-github-copilot-via-github-apps">Extending GitHub Copilot via GitHub Apps</h2>
<p>Alternatively, it is possible to extend GitHub Copilot by creating a GitHub App that contributes a chat participant in the Chat view. A GitHub App is backed by a service and works across all GitHub Copilot surfaces, such as github.com, Visual Studio, or VS Code. On the other hand, GitHub Apps do not have full access to the VS Code API. To learn more about extending GitHub Copilot through a GitHub App see the <a href="https://docs.github.com/en/copilot/building-copilot-extensions/about-building-copilot-extensions" class="external-link" target="_blank">GitHub documentation</a>.</p>
<h2 id="using-the-language-model" data-needslink="using-the-language-model">Using the language model</h2>
<p>Chat participants can use the language model in a wide range of ways. Some participants only make use of the language model to get answers to custom prompts, for example the <a href="https://github.com/microsoft/vscode-extension-samples/tree/main/chat-sample" class="external-link" target="_blank">sample chat participant</a>. Other participants are more advanced and act like autonomous agents that invoke multiple tools with the help of the language model. An example of such an advanced participant is the built-in <code>@workspace</code> that knows about your workspace and can answer questions about it. Internally, <code>@workspace</code> is powered by multiple tools: GitHub's knowledge graph, combined with semantic search, local code indexes, and VS Code's language services.</p>
<h2 id="related-content" data-needslink="related-content">Related content</h2>
<ul><li><a href="/api/references/vscode-api#chat">Chat Participant API Reference</a></li>
<li><a href="/api/extension-guides/ai/language-model">Use the Language Model API in your extension</a></li>
<li><a href="/api/extension-guides/ai/tools">Contribute a language model tool</a></li>
</ul><div class="feedback" data-edit-url="https://vscode.dev/github/microsoft/vscode-docs/blob/main/api/extension-guides/ai/chat.md"></div>
				
				<div class="body-footer">6/3/2026</div>
				
            </main><aside class="docs-right-sidebar hidden-xs"><div class="docs-markdown-actions">
                    <div class="docs-markdown-dropdown" data-raw-url="/raw/api/extension-guides/ai/chat.md">
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
                <nav id="docs-subnavbar" aria-label="On Page"><h4><span class="sr-only">On this page there are 12 sections</span><span aria-hidden="true">On this page</span></h4>
                    <ul class="nav"><li><a href="#why-implement-a-chat-participant-in-your-extension">Why implement a chat participant in your extension?</a></li>
                        
                        <li><a href="#parts-of-the-chat-user-experience">Parts of the chat user experience</a></li>
                        
                        <li><a href="#create-a-chat-participant">Create a chat participant</a></li>
                        
                        <li><a href="#use-the-chat-message-history">Use the chat message history</a></li>
                        
                        <li><a href="#supported-chat-response-output-types">Supported chat response output types</a></li>
                        
                        <li><a href="#implement-tool-calling">Implement tool calling</a></li>
                        
                        <li><a href="#measuring-success">Measuring success</a></li>
                        
                        <li><a href="#guidelines-and-conventions">Guidelines and conventions</a></li>
                        
                        <li><a href="#publishing-your-extension">Publishing your extension</a></li>
                        
                        <li><a href="#extending-github-copilot-via-github-apps">Extending GitHub Copilot via GitHub Apps</a></li>
                        
                        <li><a href="#using-the-language-model">Using the language model</a></li>
                        
                        <li><a href="#related-content">Related content</a></li>
                        
                    </ul></nav></aside></div>
		<div class="docs-mobile-widgets visible-xs">
			<div class="connect-widget"></div>
		</div>
	</div>
</div>
		</main>