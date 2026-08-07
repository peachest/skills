# Language Model Tool API

> 源文档: [https://code.visualstudio.com/api/extension-guides/ai/tools](https://code.visualstudio.com/api/extension-guides/ai/tools)

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
			          
			        <li class="active">
			          <a href="/api/extension-guides/ai/tools" aria-label="Current Page: Language Model Tool">Language Model Tool</a>
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
				<select id="small-nav-dropdown" aria-label="topics"><option value="/api">Overview</option><optgroup label="Get Started"><option value="/api/get-started/your-first-extension">Your First Extension</option><option value="/api/get-started/extension-anatomy">Extension Anatomy</option><option value="/api/get-started/wrapping-up">Wrapping Up</option></optgroup><optgroup label="Extension Capabilities"><option value="/api/extension-capabilities/overview">Overview</option><option value="/api/extension-capabilities/common-capabilities">Common Capabilities</option><option value="/api/extension-capabilities/theming">Theming</option><option value="/api/extension-capabilities/extending-workbench">Extending Workbench</option></optgroup><optgroup label="Extension Guides"><option value="/api/extension-guides/overview">Overview</option><optgroup label="Extension Guides - AI"><option value="/api/extension-guides/ai/ai-extensibility-overview">AI Extensibility</option><option value="/api/extension-guides/ai/tools" selected>Language Model Tool</option><option value="/api/extension-guides/ai/mcp">MCP Dev Guide</option><option value="/api/extension-guides/ai/chat">Chat Participant</option><option value="/api/extension-guides/ai/chat-tutorial">Chat Tutorial</option><option value="/api/extension-guides/ai/language-model">Language Model</option><option value="/api/extension-guides/ai/language-model-tutorial">Language Model Tutorial</option><option value="/api/extension-guides/ai/language-model-chat-provider">Language Model Chat Provider</option><option value="/api/extension-guides/ai/prompt-tsx">Prompt TSX</option></optgroup><option value="/api/extension-guides/command">Command</option><option value="/api/extension-guides/color-theme">Color Theme</option><option value="/api/extension-guides/file-icon-theme">File Icon Theme</option><option value="/api/extension-guides/product-icon-theme">Product Icon Theme</option><option value="/api/extension-guides/tree-view">Tree View</option><option value="/api/extension-guides/webview">Webview</option><option value="/api/extension-guides/notebook">Notebook</option><option value="/api/extension-guides/custom-editors">Custom Editors</option><option value="/api/extension-guides/virtual-documents">Virtual Documents</option><option value="/api/extension-guides/virtual-workspaces">Virtual Workspaces</option><option value="/api/extension-guides/web-extensions">Web Extensions</option><option value="/api/extension-guides/workspace-trust">Workspace Trust</option><option value="/api/extension-guides/task-provider">Task Provider</option><option value="/api/extension-guides/scm-provider">Source Control</option><option value="/api/extension-guides/debugger-extension">Debugger Extension</option><option value="/api/extension-guides/markdown-extension">Markdown Extension</option><option value="/api/extension-guides/testing">Test Extension</option><option value="/api/extension-guides/custom-data-extension">Custom Data Extension</option><option value="/api/extension-guides/telemetry">Telemetry</option></optgroup><optgroup label="UX Guidelines"><option value="/api/ux-guidelines/overview">Overview</option><option value="/api/ux-guidelines/activity-bar">Activity Bar</option><option value="/api/ux-guidelines/sidebars">Sidebars</option><option value="/api/ux-guidelines/panel">Panel</option><option value="/api/ux-guidelines/status-bar">Status Bar</option><option value="/api/ux-guidelines/views">Views</option><option value="/api/ux-guidelines/editor-actions">Editor Actions</option><option value="/api/ux-guidelines/quick-picks">Quick Picks</option><option value="/api/ux-guidelines/command-palette">Command Palette</option><option value="/api/ux-guidelines/notifications">Notifications</option><option value="/api/ux-guidelines/webviews">Webviews</option><option value="/api/ux-guidelines/context-menus">Context Menus</option><option value="/api/ux-guidelines/walkthroughs">Walkthroughs</option><option value="/api/ux-guidelines/settings">Settings</option></optgroup><optgroup label="Language Extensions"><option value="/api/language-extensions/overview">Overview</option><option value="/api/language-extensions/syntax-highlight-guide">Syntax Highlight Guide</option><option value="/api/language-extensions/semantic-highlight-guide">Semantic Highlight Guide</option><option value="/api/language-extensions/snippet-guide">Snippet Guide</option><option value="/api/language-extensions/language-configuration-guide">Language Configuration Guide</option><option value="/api/language-extensions/programmatic-language-features">Programmatic Language Features</option><option value="/api/language-extensions/language-server-extension-guide">Language Server Extension Guide</option><option value="/api/language-extensions/embedded-languages">Embedded Languages</option></optgroup><optgroup label="Testing and Publishing"><option value="/api/working-with-extensions/testing-extension">Testing Extensions</option><option value="/api/working-with-extensions/publishing-extension">Publishing Extensions</option><option value="/api/working-with-extensions/bundling-extension">Bundling Extensions</option><option value="/api/working-with-extensions/continuous-integration">Continuous Integration</option></optgroup><optgroup label="Advanced Topics"><option value="/api/advanced-topics/extension-host">Extension Host</option><option value="/api/advanced-topics/remote-extensions">Remote Development and Codespaces</option><option value="/api/advanced-topics/using-proposed-api">Using Proposed API</option><option value="/api/advanced-topics/tslint-eslint-migration">Migrate from TSLint to ESLint</option><option value="/api/advanced-topics/python-extension-template">Python Extension Template</option></optgroup><optgroup label="References"><option value="/api/references/vscode-api">VS Code API</option><option value="/api/references/contribution-points">Contribution Points</option><option value="/api/references/activation-events">Activation Events</option><option value="/api/references/extension-manifest">Extension Manifest</option><option value="/api/references/commands">Built-In Commands</option><option value="/api/references/when-clause-contexts">When Clause Contexts</option><option value="/api/references/theme-color">Theme Color</option><option value="/api/references/icons-in-labels">Product Icon Reference</option><option value="/api/references/document-selector">Document Selector</option></optgroup></select></nav></aside><div class="docs-content-wrapper">
			
			<main class="docs-main-content body"><h1>Language Model Tool API</h1>
<p>Language model tools enable you to extend the functionality of a large language model (LLM) in chat with domain-specific capabilities. To process a user's chat prompt, <a href="/docs/chat/chat-overview">agents</a> in VS Code can automatically invoke these tools to perform specialized tasks as part of the conversation.</p>
<p>By contributing a language model tool in your VS Code extension, you can extend the agentic coding workflow while also providing deep integration with the editor. Extension tools are one of three types of tools available in VS Code, alongside <a href="/docs/agents/concepts/tools#_types-of-tools">built-in tools and MCP tools</a>.</p>
<p>In this extension guide, you learn how to create a language model tool by using the Language Model Tools API and how to implement tool calling in a chat extension.</p>
<p>You can also extend the chat experience with specialized tools by contributing an <a href="/api/extension-guides/ai/mcp">MCP server</a>. See the <a href="/api/extension-guides/ai/ai-extensibility-overview">AI Extensibility Overview</a> for details on the different options and how to decide which approach to use.</p>
<div class="markdown-alert tip" dir="auto">
      <span>
        <svg class="markdown-alert-icon" viewbox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path d="M8 1.5c-2.363 0-4 1.69-4 3.75 0 .984.424 1.625.984 2.304l.214.253c.223.264.47.556.673.848.284.411.537.896.621 1.49a.75.75 0 0 1-1.484.211c-.04-.282-.163-.547-.37-.847a8.456 8.456 0 0 0-.542-.68c-.084-.1-.173-.205-.268-.32C3.201 7.75 2.5 6.766 2.5 5.25 2.5 2.31 4.863 0 8 0s5.5 2.31 5.5 5.25c0 1.516-.701 2.5-1.328 3.259-.095.115-.184.22-.268.319-.207.245-.383.453-.541.681-.208.3-.33.565-.37.847a.751.751 0 0 1-1.485-.212c.084-.593.337-1.078.621-1.489.203-.292.45-.584.673-.848.075-.088.147-.173.213-.253.561-.679.985-1.32.985-2.304 0-2.06-1.637-3.75-4-3.75ZM5.75 12h4.5a.75.75 0 0 1 0 1.5h-4.5a.75.75 0 0 1 0-1.5ZM6 15.25a.75.75 0 0 1 .75-.75h2.5a.75.75 0 0 1 0 1.5h-2.5a.75.75 0 0 1-.75-.75Z"></path></svg>
        Tip
      </span><p>For information about using tools as an end user, see <a href="/docs/chat/chat-tools">Use tools in chat</a>.</p>
</div><h2 id="what-is-tool-calling-in-an-llm" data-needslink="what-is-tool-calling-in-an-llm">What is tool calling in an LLM?</h2>
<p>A language model tool is a function that can be invoked as part of a language model request. For example, you might have a function that retrieves information from a database, performs some calculation, or calls an online API. When you contribute a tool in a VS Code extension, agent mode can then invoke the tool based on the context of the conversation.</p>
<p>The LLM never actually executes the tool itself, instead the LLM generates the parameters that are used to call your tool. It's important to clearly describe the tool's purpose, functionality, and input parameters so that the tool can be invoked in the right context.</p>
<p>The following diagram shows the tool-calling flow in agent mode in VS Code. See <a href="#_tool-calling-flow">Tool-calling flow</a> for details about the specific steps involved.</p>
<p><img src="/assets/api/extension-guides/ai/tools/copilot-tool-calling-flow.png" alt="Diagram that shows the Copilot tool-calling flow" loading="lazy"></p>
<p>Read more about <a href="https://platform.openai.com/docs/guides/function-calling" class="external-link" target="_blank">function calling</a> in the OpenAI documentation.</p>
<h2 id="why-implement-a-language-model-tool-in-your-extension" data-needslink="why-implement-a-language-model-tool-in-your-extension">Why implement a language model tool in your extension?</h2>
<p>Implementing a language model tool in your extension has several benefits:</p>
<ul><li><strong>Extend agent mode</strong> with specialized, domain-specific tools that are automatically invoked as part of responding to a user prompt. For example, enable database scaffolding and querying to dynamically provide the LLM with relevant context.</li>
<li><strong>Deeply integrate with VS Code</strong> by using the broad set of extension APIs. For example, use the <a href="/api/extension-guides/debugger-extension">debug APIs</a> to get the current debugging context and use it as part of the tool's functionality.</li>
<li><strong>Distribute and deploy</strong> tools via the Visual Studio Marketplace, providing a reliable and seamless experience for users. Users don't need a separate installation and update process for your tool.</li>
</ul><p>You might consider implementing a language model tool with an <a href="/api/extension-guides/ai/mcp">MCP server</a> in the following scenarios:</p>
<ul><li>You already have an MCP server implementation and also want to use it in VS Code.</li>
<li>You want to reuse the same tool across different development environments and platforms.</li>
<li>Your tool is hosted remotely as a service.</li>
<li>You don't need access to VS Code APIs.</li>
</ul><p>Learn more about the <a href="/docs/agents/concepts/tools#_types-of-tools">differences between tool types</a>.</p>
<h2 id="create-a-language-model-tool" data-needslink="create-a-language-model-tool">Create a language model tool</h2>
<p>Implementing a language model tool consists of two main parts:</p>
<ol><li>Define the tool's configuration in the <code>package.json</code> file of your extension.</li>
<li>Implement the tool in your extension code by using the <a href="/api/references/vscode-api#lm">Language Model API reference</a></li>
</ol><p>You can get started with a <a href="https://github.com/microsoft/vscode-extension-samples/tree/main/chat-sample" class="external-link" target="_blank">basic example project</a>.</p>
<h3 id="1.-static-configuration-in-package.json" data-needslink="1.-static-configuration-in-package.json">1. Static configuration in <code>package.json</code></h3>
<p>The first step to define a language model tool in your extension is to define it in the <code>package.json</code> file of your extension. This configuration includes the tool name, description, input schema, and other metadata:</p>
<ol><li>
<p>Add an entry for your tool in the <code>contributes.languageModelTools</code> section of your extension's <code>package.json</code> file.</p>
</li>
<li>
<p>Give the tool a unique name:</p>
<table class="table table-striped"><thead><tr><th>Property</th>
<th>Description</th>
</tr></thead><tbody><tr><td><code>name</code></td>
<td>The unique name of the tool, used to reference the tool in the extension implementation code. Format the name in the format <code>{verb}_{noun}</code>. See <a href="#_guidelines-and-conventions">naming guidelines</a>.</td>
</tr><tr><td><code>displayName</code></td>
<td>The user-friendly name of the tool, used for displaying in the UI.</td>
</tr></tbody></table></li>
<li>
<p>If the tool can be used with <a href="/docs/agents/overview#_built-in-agents">agents</a> or referenced in a chat prompt with <code>#</code>, add the following properties:</p>
<p>Users can enable or disable the tool in the Chat view, similar to how this is done for <a href="/docs/agent-customization/mcp-servers">Model Context Protocol (MCP) tools</a>.</p>
<table class="table table-striped"><thead><tr><th>Property</th>
<th>Description</th>
</tr></thead><tbody><tr><td><code>canBeReferencedInPrompt</code></td>
<td>Set to <code>true</code> if the tool can be used with <a href="/docs/agents/overview#_built-in-agents">agents</a> or referenced in chat.</td>
</tr><tr><td><code>toolReferenceName</code></td>
<td>The name for users to reference the tool in a chat prompt via <code>#</code>.</td>
</tr><tr><td><code>icon</code></td>
<td>The icon to display for the tool in the UI.</td>
</tr><tr><td><code>userDescription</code></td>
<td>User-friendly description of the tool, used for displaying in the UI.</td>
</tr></tbody></table></li>
<li>
<p>Add a detailed description in <code>modelDescription</code>. This information is used by the LLM to determine in which context your tool should be used.</p>
<ul><li>What exactly does the tool do?</li>
<li>What kind of information does it return?</li>
<li>When should and shouldn't it be used?</li>
<li>Describe important limitations or constraints of the tool.</li>
</ul></li>
<li>
<p>If the tool takes input parameters, add an <code>inputSchema</code> property that describes the tool's input parameters.</p>
<p>This JSON schema describes an object with the properties that the tool takes as input, and whether they are required. File paths should be absolute paths.</p>
<p>Describe what each parameter does and how it relates to the tool's functionality.</p>
</li>
<li>
<p>Add a <code>when</code> clause to control when the tool is available.</p>
<p>The <code>languageModelTools</code> contribution point lets you restrict when a tool is available for agent mode or can be referenced in a prompt by using a <a href="/api/references/when-clause-contexts">when clause</a>. For example, a tool that gets the debug call stack information, should only be available when the user is debugging.</p>
<pre class="shiki" data-lang="json" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"contributes"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "languageModelTools"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">        {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">            "name"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"chat-tools-sample_tabCount"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#F44747;--shiki-light:#CD3131">            ...</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">            "when"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"debugState == 'running'"</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">        }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    ]</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
</li>
</ol><details><summary>Example tool definition</summary><p>The following example shows how to define a tool that counts the number of active tabs in a tab group.</p>
<pre class="shiki" data-lang="json" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"contributes"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "languageModelTools"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">        {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">            "name"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"chat-tools-sample_tabCount"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">            "tags"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">                "editors"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">                "chat-tools-sample"</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">            ],</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">            "toolReferenceName"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"tabCount"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">            "displayName"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"Tab Count"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">            "modelDescription"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"The number of active tabs in a tab group in VS Code."</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">            "userDescription"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"Count the number of active tabs in a tab group."</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">            "canBeReferencedInPrompt"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">true</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">            "icon"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"$(files)"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">            "inputSchema"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">                "type"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"object"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">                "properties"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">                    "tabGroup"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">                        "type"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"number"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">                        "description"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"The index of the tab group to check. This is optional- if not specified, the active tab group will be checked."</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">                        "default"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#B5CEA8;--shiki-light:#098658">0</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">                    }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">                }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">            }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">        }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    ]</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
</details><h3 id="2.-tool-implementation" data-needslink="2.-tool-implementation">2. Tool implementation</h3>
<p>Implement the language model tool by using the <a href="/api/references/vscode-api#lm">Language Model API</a>. This consists of the following steps:</p>
<ol><li>
<p>On activation of the extension, register the tool with <a href="/api/references/vscode-api#lm.registerTool"><code>vscode.lm.registerTool</code></a>.</p>
<p>Provide the name of the tool as you specified it in the <code>name</code> property in <code>package.json</code>.</p>
<p>If you want the tool to be private to your extension, skip the tool registration step.</p>
<pre class="shiki" data-lang="ts" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">export</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> function</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> registerChatTools</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">context</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">ExtensionContext</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  context</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">subscriptions</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">push</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">lm</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">registerTool</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'chat-tools-sample_tabCount'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">new</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> TabCountTool</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">())</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  );</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
</li>
<li>
<p>Create a class that implements the <a href="/api/references/vscode-api#LanguageModelTool%3CT%3E"><code>vscode.LanguageModelTool&lt;&gt;</code></a> interface.</p>
</li>
<li>
<p>Add tool confirmation messages in the <code>prepareInvocation</code> method.</p>
<p>A generic confirmation dialog will always be shown for tools from extensions, but the tool can customize the confirmation message. Give enough context to the user to understand what the tool is doing. The message can be a <code>MarkdownString</code> containing a code block.</p>
<p>The following example shows how to provide a confirmation message for the tab count tool.</p>
<pre class="shiki" data-lang="ts" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">async</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> prepareInvocation</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    options</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">LanguageModelToolInvocationPrepareOptions</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">&lt;</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">ITabCountParameters</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">&gt;,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    _token</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">CancellationToken</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">    const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> confirmationMessages</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">        title:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'Count the number of open tabs'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">        message:</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> new</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">MarkdownString</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">            `Count the number of open tabs?`</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> +</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">            (</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">options</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">input</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">tabGroup</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> !== </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">undefined</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">                ? </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">` in tab group </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">${</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">options</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">input</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">tabGroup</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">`</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">                : </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">''</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">)</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">        ),</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    };</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">    return</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">        invocationMessage:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'Counting the number of tabs'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">        confirmationMessages</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    };</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<p>If <code>prepareInvocation</code> returned <code>undefined</code>, the generic confirmation message will be shown. Note that the user can also select to "Always Allow" a certain tool.</p>
</li>
<li>
<p>Define an interface that describes the tool input parameters.</p>
<p>The interface is used in the <code>invoke</code> method of the <code>vscode.LanguageModelTool</code> class. The input parameters are validated against the JSON schema you defined in the <code>inputSchema</code> in <code>package.json</code>.</p>
<p>The following example shows the interface for the tab count tool.</p>
<pre class="shiki" data-lang="ts" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">export</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> interface</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99"> ITabCountParameters</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  tabGroup</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">?: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">number</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
</li>
<li>
<p>Implement the <code>invoke</code> method. This method is called when the language model tool is invoked while processing a chat prompt.</p>
<p>The <code>invoke</code> method receives the tool input parameters in the <code>options</code> parameter. The parameters are validated against the JSON schema defined in <code>inputSchema</code> in <code>package.json</code>.</p>
<p>When an error occurs, throw an error with a message that makes sense to the LLM. Optionally, provide instructions on what the LLM should do next, such as retrying with different parameters, or performing a different action.</p>
<p>The following example shows the implementation of the tab count tool. The result of the tool is an instance of type <code>vscode.LanguageModelToolResult</code>.</p>
<pre class="shiki" data-lang="ts" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">async</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> invoke</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    options</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">LanguageModelToolInvocationOptions</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">&lt;</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">ITabCountParameters</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">&gt;,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    _token</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">CancellationToken</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">    const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> params</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">options</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">input</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">    if</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> (</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">typeof</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> params</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">tabGroup</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> === </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'number'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">        const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> group</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">window</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">tabGroups</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">all</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">[</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">Math</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">max</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">params</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">tabGroup</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> - </span><span style="--shiki-dark:#B5CEA8;--shiki-light:#098658">1</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#B5CEA8;--shiki-light:#098658">0</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">)];</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">        const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> nth</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> =</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">            params</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">tabGroup</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> === </span><span style="--shiki-dark:#B5CEA8;--shiki-light:#098658">1</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">                ? </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'1st'</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">                : </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">params</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">tabGroup</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> === </span><span style="--shiki-dark:#B5CEA8;--shiki-light:#098658">2</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">                    ? </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'2nd'</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">                    : </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">params</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">tabGroup</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> === </span><span style="--shiki-dark:#B5CEA8;--shiki-light:#098658">3</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">                        ? </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'3rd'</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">                        : </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">`</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">${</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">params</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">tabGroup</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">th`</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">        return</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> new</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">LanguageModelToolResult</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">([</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">new</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">LanguageModelTextPart</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">`There are </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">${</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">group</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">tabs</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">length</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> tabs open in the </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">${</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">nth</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> tab group.`</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">)]);</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    } </span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">else</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">        const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> group</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">window</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">tabGroups</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">activeTabGroup</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">        return</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> new</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">LanguageModelToolResult</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">([</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">new</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">LanguageModelTextPart</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">`There are </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">${</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">group</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">tabs</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">length</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> tabs open.`</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">)]);</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
</li>
</ol><p>View the full source code for implementing a <a href="https://github.com/microsoft/vscode-extension-samples/blob/main/chat-sample/src/tools.ts" class="external-link" target="_blank">language model tool</a> in the VS Code Extension Samples repository.</p>
<h2 id="toolcalling-flow" data-needslink="toolcalling-flow">Tool-calling flow</h2>
<p>When a user sends a chat prompt, the following steps occur:</p>
<ol><li>
<p>Copilot determines the list of available tools based on the user's configuration.</p>
<p>The list of tools consists of built-in tools, tools registered by extensions, and tools from <a href="/docs/agent-customization/mcp-servers">MCP servers</a>. You can contribute to agent mode via extensions or MCP servers (shown in green in the diagram).</p>
</li>
<li>
<p>Copilot sends the request to the LLM and provides it with the prompt, chat context, and the list of tool definitions to consider.</p>
<p>The LLM generates a response, which might include one or more requests to invoke a tool.</p>
</li>
<li>
<p>If needed, Copilot invokes the suggested tool(s) with the parameter values provided by the LLM.</p>
<p>A tool response might result in more requests for tool invocations.</p>
</li>
<li>
<p>If there are errors or follow-up tool requests, Copilot iterates over the tool-calling flow until all tool requests are resolved.</p>
</li>
<li>
<p>Copilot returns the final response to the user, which might include responses from multiple tools.</p>
</li>
</ol><h2 id="guidelines-and-conventions" data-needslink="guidelines-and-conventions">Guidelines and conventions</h2>
<ul><li>
<p><strong>Naming</strong>: write clear and descriptive names for tools and parameters.</p>
<ul><li>
<p><strong>Tool name</strong>: should be unique, and clearly describe their intent. Structure the tool name in the format <code>{verb}_{noun}</code>. For example, <code>get_weather</code>, <code>get_azure_deployment</code>, or <code>get_terminal_output</code>.</p>
</li>
<li>
<p><strong>Parameter name</strong>: should describe the parameter's purpose. Structure the parameter name in the format <code>{noun}</code>. For example, <code>destination_location</code>, <code>ticker</code>, or <code>file_name</code>.</p>
</li>
</ul></li>
<li>
<p><strong>Descriptions</strong>: write detailed descriptions for tools and parameters.</p>
<ul><li>Describe what the tool does and when it should and shouldn't be used. For example, "This tool retrieves the weather for a given location."</li>
<li>Describe what each parameter does and how it relates to the tool's functionality. For example, "The <code>destination_location</code> parameter specifies the location for which to retrieve the weather. It should be a valid location name or coordinates."</li>
<li>Describe important limitations or constraints of the tool. For example, "This tool only retrieves weather data for locations in the United States. It might not work for other regions."</li>
</ul></li>
<li>
<p><strong>User confirmation</strong>: provide a confirmation message for the tool invocation. A generic confirmation dialog will always be shown for tools from extensions, but the tool can customize the confirmation message. Give enough context to the user to understand what the tool is doing.</p>
</li>
<li>
<p><strong>Error handling</strong>: when an error occurs, throw an error with a message that makes sense to the LLM. Optionally, provide instructions on what the LLM should do next, such as retrying with different parameters, or performing a different action.</p>
</li>
</ul><p>Get more best practices for creating tools in the <a href="https://platform.openai.com/docs/guides/function-calling?api-mode=chat#best-practices-for-defining-functions" class="external-link" target="_blank">OpenAI documentation</a> and <a href="https://docs.anthropic.com/en/docs/build-with-claude/tool-use/overview" class="external-link" target="_blank">Anthropic documentation</a>.</p>
<h2 id="related-content" data-needslink="related-content">Related content</h2>
<ul><li><a href="/api/references/vscode-api#lm">Language Model API reference</a></li>
<li><a href="/api/extension-guides/ai/mcp">Register an MCP server in a VS Code extension</a></li>
<li><a href="/docs/agent-customization/mcp-servers">Use MCP tools in agent mode</a></li>
</ul><div class="feedback" data-edit-url="https://vscode.dev/github/microsoft/vscode-docs/blob/main/api/extension-guides/ai/tools.md"></div>
				
				<div class="body-footer">6/3/2026</div>
				
            </main><aside class="docs-right-sidebar hidden-xs"><div class="docs-markdown-actions">
                    <div class="docs-markdown-dropdown" data-raw-url="/raw/api/extension-guides/ai/tools.md">
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
                    <ul class="nav"><li><a href="#what-is-tool-calling-in-an-llm">What is tool calling in an LLM?</a></li>
                        
                        <li><a href="#why-implement-a-language-model-tool-in-your-extension">Why implement a language model tool in your extension?</a></li>
                        
                        <li><a href="#create-a-language-model-tool">Create a language model tool</a></li>
                        
                        <li><a href="#toolcalling-flow">Tool-calling flow</a></li>
                        
                        <li><a href="#guidelines-and-conventions">Guidelines and conventions</a></li>
                        
                        <li><a href="#related-content">Related content</a></li>
                        
                    </ul></nav></aside></div>
		<div class="docs-mobile-widgets visible-xs">
			<div class="connect-widget"></div>
		</div>
	</div>
</div>
		</main>