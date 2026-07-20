# MCP developer guide

> 源文档: [https://code.visualstudio.com/api/extension-guides/ai/mcp](https://code.visualstudio.com/api/extension-guides/ai/mcp)

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
			          
			        <li class="active">
			          <a href="/api/extension-guides/ai/mcp" aria-label="Current Page: MCP Dev Guide">MCP Dev Guide</a>
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
				<select id="small-nav-dropdown" aria-label="topics"><option value="/api">Overview</option><optgroup label="Get Started"><option value="/api/get-started/your-first-extension">Your First Extension</option><option value="/api/get-started/extension-anatomy">Extension Anatomy</option><option value="/api/get-started/wrapping-up">Wrapping Up</option></optgroup><optgroup label="Extension Capabilities"><option value="/api/extension-capabilities/overview">Overview</option><option value="/api/extension-capabilities/common-capabilities">Common Capabilities</option><option value="/api/extension-capabilities/theming">Theming</option><option value="/api/extension-capabilities/extending-workbench">Extending Workbench</option></optgroup><optgroup label="Extension Guides"><option value="/api/extension-guides/overview">Overview</option><optgroup label="Extension Guides - AI"><option value="/api/extension-guides/ai/ai-extensibility-overview">AI Extensibility</option><option value="/api/extension-guides/ai/tools">Language Model Tool</option><option value="/api/extension-guides/ai/mcp" selected>MCP Dev Guide</option><option value="/api/extension-guides/ai/chat">Chat Participant</option><option value="/api/extension-guides/ai/chat-tutorial">Chat Tutorial</option><option value="/api/extension-guides/ai/language-model">Language Model</option><option value="/api/extension-guides/ai/language-model-tutorial">Language Model Tutorial</option><option value="/api/extension-guides/ai/language-model-chat-provider">Language Model Chat Provider</option><option value="/api/extension-guides/ai/prompt-tsx">Prompt TSX</option></optgroup><option value="/api/extension-guides/command">Command</option><option value="/api/extension-guides/color-theme">Color Theme</option><option value="/api/extension-guides/file-icon-theme">File Icon Theme</option><option value="/api/extension-guides/product-icon-theme">Product Icon Theme</option><option value="/api/extension-guides/tree-view">Tree View</option><option value="/api/extension-guides/webview">Webview</option><option value="/api/extension-guides/notebook">Notebook</option><option value="/api/extension-guides/custom-editors">Custom Editors</option><option value="/api/extension-guides/virtual-documents">Virtual Documents</option><option value="/api/extension-guides/virtual-workspaces">Virtual Workspaces</option><option value="/api/extension-guides/web-extensions">Web Extensions</option><option value="/api/extension-guides/workspace-trust">Workspace Trust</option><option value="/api/extension-guides/task-provider">Task Provider</option><option value="/api/extension-guides/scm-provider">Source Control</option><option value="/api/extension-guides/debugger-extension">Debugger Extension</option><option value="/api/extension-guides/markdown-extension">Markdown Extension</option><option value="/api/extension-guides/testing">Test Extension</option><option value="/api/extension-guides/custom-data-extension">Custom Data Extension</option><option value="/api/extension-guides/telemetry">Telemetry</option></optgroup><optgroup label="UX Guidelines"><option value="/api/ux-guidelines/overview">Overview</option><option value="/api/ux-guidelines/activity-bar">Activity Bar</option><option value="/api/ux-guidelines/sidebars">Sidebars</option><option value="/api/ux-guidelines/panel">Panel</option><option value="/api/ux-guidelines/status-bar">Status Bar</option><option value="/api/ux-guidelines/views">Views</option><option value="/api/ux-guidelines/editor-actions">Editor Actions</option><option value="/api/ux-guidelines/quick-picks">Quick Picks</option><option value="/api/ux-guidelines/command-palette">Command Palette</option><option value="/api/ux-guidelines/notifications">Notifications</option><option value="/api/ux-guidelines/webviews">Webviews</option><option value="/api/ux-guidelines/context-menus">Context Menus</option><option value="/api/ux-guidelines/walkthroughs">Walkthroughs</option><option value="/api/ux-guidelines/settings">Settings</option></optgroup><optgroup label="Language Extensions"><option value="/api/language-extensions/overview">Overview</option><option value="/api/language-extensions/syntax-highlight-guide">Syntax Highlight Guide</option><option value="/api/language-extensions/semantic-highlight-guide">Semantic Highlight Guide</option><option value="/api/language-extensions/snippet-guide">Snippet Guide</option><option value="/api/language-extensions/language-configuration-guide">Language Configuration Guide</option><option value="/api/language-extensions/programmatic-language-features">Programmatic Language Features</option><option value="/api/language-extensions/language-server-extension-guide">Language Server Extension Guide</option><option value="/api/language-extensions/embedded-languages">Embedded Languages</option></optgroup><optgroup label="Testing and Publishing"><option value="/api/working-with-extensions/testing-extension">Testing Extensions</option><option value="/api/working-with-extensions/publishing-extension">Publishing Extensions</option><option value="/api/working-with-extensions/bundling-extension">Bundling Extensions</option><option value="/api/working-with-extensions/continuous-integration">Continuous Integration</option></optgroup><optgroup label="Advanced Topics"><option value="/api/advanced-topics/extension-host">Extension Host</option><option value="/api/advanced-topics/remote-extensions">Remote Development and Codespaces</option><option value="/api/advanced-topics/using-proposed-api">Using Proposed API</option><option value="/api/advanced-topics/tslint-eslint-migration">Migrate from TSLint to ESLint</option><option value="/api/advanced-topics/python-extension-template">Python Extension Template</option></optgroup><optgroup label="References"><option value="/api/references/vscode-api">VS Code API</option><option value="/api/references/contribution-points">Contribution Points</option><option value="/api/references/activation-events">Activation Events</option><option value="/api/references/extension-manifest">Extension Manifest</option><option value="/api/references/commands">Built-In Commands</option><option value="/api/references/when-clause-contexts">When Clause Contexts</option><option value="/api/references/theme-color">Theme Color</option><option value="/api/references/icons-in-labels">Product Icon Reference</option><option value="/api/references/document-selector">Document Selector</option></optgroup></select></nav></aside><div class="docs-content-wrapper">
			
			<main class="docs-main-content body"><h1>MCP developer guide</h1>
<p>Model Context Protocol (MCP) is an open standard that enables AI models to interact with external tools and services through a unified interface. Visual Studio Code implements the full MCP specification, enabling you to create MCP servers that provide tools, prompts, and resources for extending the capabilities of AI agents in VS Code.</p>
<p>MCP servers provide one of three types of tools available in VS Code, alongside built-in tools and extension-contributed tools. Learn more about <a href="/docs/agents/concepts/tools#_types-of-tools">tool types</a>.</p>
<p>This guide covers everything you need to know to build MCP servers that work seamlessly with VS Code and other MCP clients.</p>
<div class="markdown-alert tip" dir="auto">
      <span>
        <svg class="markdown-alert-icon" viewbox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path d="M8 1.5c-2.363 0-4 1.69-4 3.75 0 .984.424 1.625.984 2.304l.214.253c.223.264.47.556.673.848.284.411.537.896.621 1.49a.75.75 0 0 1-1.484.211c-.04-.282-.163-.547-.37-.847a8.456 8.456 0 0 0-.542-.68c-.084-.1-.173-.205-.268-.32C3.201 7.75 2.5 6.766 2.5 5.25 2.5 2.31 4.863 0 8 0s5.5 2.31 5.5 5.25c0 1.516-.701 2.5-1.328 3.259-.095.115-.184.22-.268.319-.207.245-.383.453-.541.681-.208.3-.33.565-.37.847a.751.751 0 0 1-1.485-.212c.084-.593.337-1.078.621-1.489.203-.292.45-.584.673-.848.075-.088.147-.173.213-.253.561-.679.985-1.32.985-2.304 0-2.06-1.637-3.75-4-3.75ZM5.75 12h4.5a.75.75 0 0 1 0 1.5h-4.5a.75.75 0 0 1 0-1.5ZM6 15.25a.75.75 0 0 1 .75-.75h2.5a.75.75 0 0 1 0 1.5h-2.5a.75.75 0 0 1-.75-.75Z"></path></svg>
        Tip
      </span><p>For information about using MCP servers as an end user, see <a href="/docs/agent-customization/mcp-servers">Use MCP servers in VS Code</a>.</p>
</div><h2 id="why-use-mcp-servers" data-needslink="why-use-mcp-servers">Why use MCP servers?</h2>
<p>Implementing an MCP server to extend chat in VS Code with language model tools has the following benefits:</p>
<ul><li><strong>Extend agent mode</strong> with specialized, domain-specific, tools that are automatically invoked as part of responding to a user prompt. For example, enable database scaffolding and querying to dynamically provide the LLM with relevant context.</li>
<li><strong>Flexible deployment options</strong> for local and remote scenarios.</li>
<li><strong>Reuse</strong> your MCP server across different tools and platforms.</li>
</ul><p>You might consider implementing a language model tool with the <a href="/api/extension-guides/ai/tools">Language Model API</a> in the following scenarios:</p>
<ul><li>You want to deeply integrate with VS Code by using extension APIs.</li>
<li>You want to distribute your tool and updates by using the Visual Studio Marketplace.</li>
</ul><h2 id="mcp-features-supported-by-vs-code" data-needslink="mcp-features-supported-by-vs-code">MCP features supported by VS Code</h2>
<p>VS Code supports the following MCP capabilities:</p>
<ul><li>
<p><a href="https://modelcontextprotocol.io/specification/2025-06-18/basic/transports" class="external-link" target="_blank">Transports</a>:</p>
<ul><li>Local standard input/output (<code>stdio</code>)</li>
<li>Streamable HTTP (<code>http</code>)</li>
<li>Server-sent events (<code>sse</code>) - legacy support.</li>
</ul></li>
<li>
<p><a href="https://modelcontextprotocol.io/specification/2025-06-18#features" class="external-link" target="_blank">Features</a>:</p>
<ul><li>Tools: extend <a href="/docs/chat/chat-overview">agent mode</a> with extra tools</li>
<li>Prompts: add reusable prompts as slash commands in chat</li>
<li>Resources: provide data and content that users can add as chat context or interact with directly in VS Code</li>
<li>Elicitation: request input from the user</li>
<li>Sampling: make language model requests using the user's configured models and subscription</li>
<li>Authentication: authorize access to an MCP server using OAuth</li>
<li>Server instructions</li>
<li>Roots: provide information about the user's workspace root folder(s)</li>
<li><a href="https://modelcontextprotocol.github.io/ext-apps/api/" class="external-link" target="_blank">MCP Apps</a>: return interactive UI components from tools</li>
</ul></li>
</ul><h3 id="tools" data-needslink="tools">Tools</h3>
<h4>Tool definition</h4>
<p>VS Code supports MCP tools in agent mode, where they are invoked as needed based on the task. Users can enable and configure them with the tools picker. The tool description is shown in the tools picker, alongside the tool name, and in the dialog when asking for confirmation before running a tool.</p>
<p><img src="/assets/api/extension-guides/ai/mcp/mcp-tools-picker.png" alt="Screenshot that shows the tools picker in agent mode, highlighting tools from an MCP server." loading="lazy"></p>
<p>Users can edit model-generated input parameters in the tool confirmation dialog. The confirmation dialog will be shown for all tools that are not marked with the <code>readOnlyHint</code> annotation.</p>
<p><img src="/assets/api/extension-guides/ai/mcp/mcp-tool-input-parameters.png" alt="Screenshot that shows the tool confirmation dialog with input parameters for an MCP tool." loading="lazy"></p>
<h4>Dynamic tool discovery</h4>
<p>VS Code also supports <a href="https://modelcontextprotocol.io/docs/concepts/tools#tool-discovery-and-updates" class="external-link" target="_blank">dynamic tool discovery</a>, allowing servers to register tools at runtime. For example, a server can provide different tools based on the framework or language detected in the workspace, or in response to the user's chat prompt.</p>
<h4>Tool annotations</h4>
<p>To provide extra metadata about a tool's behavior, you can use <a href="https://modelcontextprotocol.io/docs/concepts/tools#tool-annotations" class="external-link" target="_blank">tool annotations</a>:</p>
<ul><li><code>title</code>: Human-readable title for the tool, shown in the Chat view when a tool is invoked</li>
<li><code>readOnlyHint</code>: Optional hint to indicate that the tool is read-only. VS Code doesn't ask for confirmation to run read-only tools.</li>
</ul><h3 id="resources" data-needslink="resources">Resources</h3>
<p>Resources enable you to provide data and content to users in a structured way. Users can directly access resources in VS Code, or use them as context in chat prompts. For example, an MCP server could generate screenshots and make them available as resources, or provide access to log files, which are then updated in real-time.</p>
<p>When you define an MCP resource, the resource name is shown in the MCP Resources Quick Picks. Resources can be opened via the <strong>MCP: Browse Resources</strong> command or attached to a chat request with <strong>Add Context</strong> and then selecting <strong>MCP Resource</strong>. Resources can contain text or binary content.</p>
<p><img src="/assets/api/extension-guides/ai/mcp/mcp-resources-picker.png" alt="Screenshot that shows the MCP Resources Quick Pick." loading="lazy"></p>
<p>VS Code supports resource updates, enabling users to see changes to the contents of a resource in real-time in the editor.</p>
<h4>Resource templates</h4>
<p>VS Code also supports <a href="https://modelcontextprotocol.io/docs/concepts/resources#resource-templates" class="external-link" target="_blank">resource templates</a>, enabling users to provide input parameters when referencing a resource. For example, a database query tool could ask for the database table name.</p>
<p>When accessing a resource with a template, users are prompted for the required parameters in a Quick Pick. You can provide completions to suggest values for the parameter.</p>
<h3 id="prompts" data-needslink="prompts">Prompts</h3>
<p>Prompts are reusable chat prompt templates that users can invoke in chat by using a slash command (<code>mcp.servername.promptname</code>). Prompts can be useful for onboarding users to your servers by highlighting various tools or providing built-in complex workflows that adapt to the user's local context and service.</p>
<p>If you define <a href="https://modelcontextprotocol.io/specification/2025-06-18/server/utilities/completion" class="external-link" target="_blank">completions</a> to suggest values for prompt input arguments, then VS Code shows a dialog to collect input from the user.</p>
<pre class="shiki" data-lang="typescript" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">server</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">prompt</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">  'teamGreeting'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">  'Generate a greeting for team members'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    name:</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> completable</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">z</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">string</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(), </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">value</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> =&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">      return</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> [</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'Alice'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'Bob'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'Charlie'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">].</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">filter</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">n</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> =&gt;</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> n</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">startsWith</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">value</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">));</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    })</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  },</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">  async</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> ({ </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">name</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> }) </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">=&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> ({</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    messages:</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> [</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">        role:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'assistant'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">        content:</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> { </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">type:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'text'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">text:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> `Hello </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">${</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">name</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">, welcome to the team!`</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    ]</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  })</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"></span></code></pre>
<p><img src="/assets/api/extension-guides/ai/mcp/mcp-prompt-argument.png" alt="Screenshot that shows the prompt dialog for an MCP prompt with input parameters." loading="lazy"></p>
<div class="markdown-alert note" dir="auto">
      <span>
        <svg class="markdown-alert-icon" viewbox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8Zm8-6.5a6.5 6.5 0 1 0 0 13 6.5 6.5 0 0 0 0-13ZM6.5 7.75A.75.75 0 0 1 7.25 7h1a.75.75 0 0 1 .75.75v2.75h.25a.75.75 0 0 1 0 1.5h-2a.75.75 0 0 1 0-1.5h.25v-2h-.25a.75.75 0 0 1-.75-.75ZM8 6a1 1 0 1 1 0-2 1 1 0 0 1 0 2Z"></path></svg>
        Note
      </span><p>Users can enter a terminal command in the prompt dialog and use the command output as input for the prompt.</p>
</div><p>When you include a resource type in the prompt response, VS Code attaches that resource as context to the chat prompt.</p>
<h3 id="authorization" data-needslink="authorization">Authorization</h3>
<p>VS Code supports MCP servers that require authentication, allowing users to interact with an MCP server that operates on behalf of their user account for that service.</p>
<p>The <a href="https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization" class="external-link" target="_blank">authorization specification</a> cleanly separates MCP servers as Resource Servers from Authorization Servers, allowing developers to delegate authentication to existing identity providers (IdPs) rather than building their own OAuth implementations from scratch.</p>
<p>VS Code has built-in authentication support for GitHub and Microsoft Entra. If your MCP server implements the latest specification and uses GitHub or Microsoft Entra as the authorization server, users can manage which MCP servers have access to their account through the <strong>Accounts menu</strong> &gt; <strong>Manage Trusted MCP Servers</strong> action for that account.</p>
<p><img src="/assets/api/extension-guides/ai/mcp/manage-trusted-mcp.png" alt="Screenshot that shows the Accounts menu with the Manage Trusted MCP Servers action." loading="lazy"></p>
<p>VS Code supports authorization using OAuth 2.1 standards and 2.0 standards to other IdPs than GitHub and Microsoft Entra. VS Code first starts with a <a href="https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization#dynamic-client-registration" class="external-link" target="_blank">Dynamic Client Registration (DCR)</a> handshake and then falls back to a client-credentials workflow if the IdP does not support DCR. This gives more flexibility to the various IdPs to create static client IDs or specific client ID-secret pairs for each MCP server accordingly.</p>
<p>Users can then view their authentication status also through the <strong>Accounts menu</strong>. To remove dynamic client registrations, users can use the <strong>Authentication: Remove Dynamic Authentication Providers</strong> command in the Command Palette.</p>
<p>Below is a checklist to ensure your MCP server and VS Code's OAuth workflows will work:</p>
<ol><li>The MCP server defines the <a href="https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization" class="external-link" target="_blank">MCP authorization specification</a>.</li>
<li>The IdP must support either DCR or client credentials</li>
<li>The redirect URL list must include these URLs: <code>http://127.0.0.1:33418</code> and <code>https://vscode.dev/redirect</code></li>
</ol><p>When DCR is not supported by the MCP server, users will go through the fallback client-credential flow:</p>
<p><img src="/assets/api/extension-guides/ai/mcp/mcp-auth-dynamic-client-required.png" alt="Screenshot that shows the authorization when DCR is not supported for a MCP server." loading="lazy"></p>
<p><img src="/assets/api/extension-guides/ai/mcp/mcp-auth-client-id.png" alt="Screenshot that shows the authorization when Client ID for a MCP server is requested." loading="lazy"></p>
<p><img src="/assets/api/extension-guides/ai/mcp/mcp-auth-client-secret.png" alt="Screenshot that shows the authorization when Client Secret for a MCP server is requested." loading="lazy"></p>
<div class="markdown-alert note" dir="auto">
      <span>
        <svg class="markdown-alert-icon" viewbox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8Zm8-6.5a6.5 6.5 0 1 0 0 13 6.5 6.5 0 0 0 0-13ZM6.5 7.75A.75.75 0 0 1 7.25 7h1a.75.75 0 0 1 .75.75v2.75h.25a.75.75 0 0 1 0 1.5h-2a.75.75 0 0 1 0-1.5h.25v-2h-.25a.75.75 0 0 1-.75-.75ZM8 6a1 1 0 1 1 0-2 1 1 0 0 1 0 2Z"></path></svg>
        Note
      </span><p>VS Code still supports MCP servers that behave as an authorization server, but it is recommended to use the latest specification for new servers.</p>
</div><h3 id="sampling" data-needslink="sampling">Sampling</h3>
<p>VS Code provides access to <a href="https://modelcontextprotocol.io/docs/concepts/sampling" class="external-link" target="_blank">sampling</a> for MCP servers. This allows your MCP server to make language model requests using the user's configured models and subscriptions. For example, use sampling to summarize large data sets, to extract information before sending it to the client, or to implement agentic decision logic in a tool.</p>
<p>The first time an MCP server performs a sampling request, the user is prompted to authorize the server to access their models.</p>
<p><img src="/assets/api/extension-guides/ai/mcp/mcp-allow-sampling.png" alt="Screenshot that shows the authorization prompt for an MCP server to access models." loading="lazy"></p>
<p>When making sampling requests with specific models, consider that users can restrict which models an MCP server can use with the <strong>MCP: List Servers</strong> &gt; <strong>Configure Model Access</strong> command in the Command Palette. When you specify <code>modelPreferences</code> in your MCP server to provide hints about which models to use for sampling, VS Code will pick from the allowed models.</p>
<p><img src="/assets/api/extension-guides/ai/mcp/mcp-configure-model-access.png" alt="Screenshot that shows the Configure Model Access dialog for an MCP server." loading="lazy"></p>
<p>Users can view the sampling requests made by an MCP server with the <strong>MCP: List Servers</strong> &gt; <strong>Show Sampling Requests</strong> command in the Command Palette.</p>
<h3 id="workspace-roots" data-needslink="workspace-roots">Workspace roots</h3>
<p>VS Code provides the MCP server with the user's workspace root folder information.</p>
<h3 id="mcp-apps" data-needslink="mcp-apps">MCP Apps</h3>
<p>MCP Apps enable tools to return interactive UI components that render inline in chat instead of text-only output. This is useful for scenarios like drag-and-drop list reordering, visualizations, forms, and multi-step workflows.</p>
<h4>Architecture</h4>
<p>MCP Apps use a Tool + UI Resource pattern:</p>
<ol><li>Define a tool that returns a <code>_meta.ui.resourceUri</code> pointing to a UI resource</li>
<li>Create a UI resource with the <code>ui://</code> URI scheme and MIME type <code>text/html;profile=mcp-app</code></li>
<li>The HTML resource runs in a sandboxed iframe and uses the MCP Apps SDK to communicate with VS Code</li>
</ol><h4>SDK</h4>
<p>Use the <a href="https://github.com/modelcontextprotocol/ext-apps" class="external-link" target="_blank"><code>@modelcontextprotocol/ext-apps</code></a> package to build MCP Apps. The SDK provides:</p>
<ul><li>
<p><strong><code>App</code> class</strong>: Main interface for communicating with the host</p>
<ul><li><code>connect()</code>: Establish connection with VS Code</li>
<li><code>callServerTool(name, args)</code>: Call tools on the originating MCP server</li>
<li><code>sendMessage(content)</code>: Send a message to the chat input</li>
<li><code>updateModelContext(context)</code>: Provide context for future conversation turns</li>
<li><code>openLink(url)</code>: Request to open a URL in the browser</li>
<li><code>sendLog(level, message)</code>: Send debug logs (not added to conversation)</li>
</ul></li>
<li>
<p><strong>Notification handlers</strong>: Set these to receive events from VS Code</p>
<ul><li><code>ontoolinput</code>: Receive complete tool arguments</li>
<li><code>ontoolinputpartial</code>: Receive streaming partial arguments</li>
<li><code>ontoolresult</code>: Receive tool execution results</li>
<li><code>ontoolcancelled</code>: Handle tool cancellation</li>
<li><code>onhostcontextchanged</code>: Respond to theme or locale changes</li>
<li><code>onteardown</code>: Clean up before unmounting</li>
</ul></li>
</ul><h4>VS Code behavior and limitations</h4>
<table class="table table-striped"><thead><tr><th>Feature</th>
<th>VS Code Support</th>
</tr></thead><tbody><tr><td>Display modes</td>
<td><code>inline</code> only (not <code>fullscreen</code> or <code>pip</code>)</td>
</tr><tr><td>Send message</td>
<td>Fills chat input box; does not auto-send</td>
</tr><tr><td>Context updates</td>
<td>Appear as attachments</td>
</tr><tr><td>Clipboard write</td>
<td>Supported</td>
</tr><tr><td>Camera, microphone, geolocation</td>
<td>Not supported</td>
</tr></tbody></table><h4>Security</h4>
<p>MCP Apps run in sandboxed iframes with Content Security Policy (CSP) enforcement. When defining a UI resource, declare the domains your app needs to access:</p>
<ul><li><code>connectDomains</code>: Domains for fetch/XHR requests</li>
<li><code>resourceDomains</code>: Domains for images, fonts, and other resources</li>
<li><code>frameDomains</code>: Domains that can be embedded in iframes</li>
</ul><h4>Learn more</h4>
<ul><li><a href="https://modelcontextprotocol.github.io/ext-apps/api/" class="external-link" target="_blank">MCP Apps specification</a></li>
<li><a href="https://github.com/modelcontextprotocol/ext-apps" class="external-link" target="_blank">MCP Apps SDK and examples</a></li>
<li><a href="https://code.visualstudio.com/blogs/2026/01/26/mcp-apps-support">MCP Apps announcement blog post</a></li>
</ul><h3 id="icons" data-needslink="icons">Icons</h3>
<p>VS Code supports <code>icons</code> provided on MCP servers, resources, and tools. MCP Icons have a <code>src</code> property which is a URI to the image:</p>
<ul><li>MCP servers using the HTTP or SSE transports may serve images from the same authority the MCP server is hosted on. For example, a server configured at <code>https://example.com/mcp</code> can serve images from <code>example.com</code>.</li>
<li>MCP servers using the stdio transport may serve images from the file system using <code>file:///</code> URIs.</li>
<li>Any MCP server can embed images as data URIs beginning with <code>data:</code>.</li>
</ul><h2 id="add-mcp-servers-to-vs-code" data-needslink="add-mcp-servers-to-vs-code">Add MCP servers to VS Code</h2>
<p>Users can add MCP servers within VS Code in several ways:</p>
<ul><li>Install directly from the web: use a special MCP installation URL (<code>vscode:mcp/install</code>) on your website.</li>
<li>Workspace configuration: Specify the server configuration in a <code>.vscode/mcp.json</code> file in the workspace.</li>
<li>Global configuration: Define servers globally in the user <a href="/docs/configure/profiles">profile</a>.</li>
<li>Autodiscovery: VS Code can discover servers from other tools like Claude Desktop.</li>
<li>Extension: VS Code extensions can register MCP servers programmatically.</li>
<li>Command line: Install MCP servers from the command line with the <code>--add-mcp</code> VS Code command-line option.</li>
</ul><p>Learn more about the different ways to <a href="/docs/agent-customization/mcp-servers#add-an-mcp-server">add MCP servers to VS Code</a>.</p>
<h2 id="manage-mcp-servers" data-needslink="manage-mcp-servers">Manage MCP servers</h2>
<p>You can manage the list of installed MCP servers from the Extension view (<span class="dynamic-keybinding" data-commandid="workbench.view.extensions" data-osx="⇧⌘X" data-win="Ctrl+Shift+X" data-linux="Ctrl+Shift+X"><span class="keybinding">⇧⌘X</span> (Windows, Linux <span class="keybinding">Ctrl+Shift+X</span>)</span>) in VS Code.</p>
<p><img src="/assets/api/extension-guides/ai/mcp/extensions-view-mcp-servers.png" alt="Screenshot showing the MCP servers in the Extensions view." loading="lazy"></p>
<p>Right-click on an MCP server or select the gear icon to perform different management actions on the server. Alternatively, run the <strong>MCP: List Servers</strong> command from the Command Palette to view the list of configured MCP servers. You can then select a server and perform actions on it.</p>
<div class="markdown-alert tip" dir="auto">
      <span>
        <svg class="markdown-alert-icon" viewbox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path d="M8 1.5c-2.363 0-4 1.69-4 3.75 0 .984.424 1.625.984 2.304l.214.253c.223.264.47.556.673.848.284.411.537.896.621 1.49a.75.75 0 0 1-1.484.211c-.04-.282-.163-.547-.37-.847a8.456 8.456 0 0 0-.542-.68c-.084-.1-.173-.205-.268-.32C3.201 7.75 2.5 6.766 2.5 5.25 2.5 2.31 4.863 0 8 0s5.5 2.31 5.5 5.25c0 1.516-.701 2.5-1.328 3.259-.095.115-.184.22-.268.319-.207.245-.383.453-.541.681-.208.3-.33.565-.37.847a.751.751 0 0 1-1.485-.212c.084-.593.337-1.078.621-1.489.203-.292.45-.584.673-.848.075-.088.147-.173.213-.253.561-.679.985-1.32.985-2.304 0-2.06-1.637-3.75-4-3.75ZM5.75 12h4.5a.75.75 0 0 1 0 1.5h-4.5a.75.75 0 0 1 0-1.5ZM6 15.25a.75.75 0 0 1 .75-.75h2.5a.75.75 0 0 1 0 1.5h-2.5a.75.75 0 0 1-.75-.75Z"></path></svg>
        Tip
      </span><p>When you open the <code>.vscode/mcp.json</code> file, VS Code shows commands in the editor to start, stop, or restart a server directly from the editor.</p>
<p><img src="/assets/api/extension-guides/ai/mcp/mcp-server-config-lenses.png" alt="MCP server configuration with lenses to manage server." loading="lazy"></p>
</div><h2 id="create-an-mcp-installation-url" data-needslink="create-an-mcp-installation-url">Create an MCP installation URL</h2>
<p>VS Code provides a URL handler for installing an MCP server from a link: <code>vscode:mcp/install?{json-configuration}</code> (Insiders: <code>vscode-insiders:mcp/install?{json-configuration}</code>).</p>
<p>Provide the JSON server configuration in the form <code>{\"name\":\"server-name\",\"command\":...}</code> and then perform a JSON-stringify and URL encode on it. For example, use the following logic to create the installation URL:</p>
<pre class="shiki" data-lang="typescript" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">// For Insiders, use `vscode-insiders` instead of `code`</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> link</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">`vscode:mcp/install?</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">${</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">encodeURIComponent</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">(</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1">JSON</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">stringify</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">obj</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">))</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">`</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"></span></code></pre>
<p>This link can be used in a browser, or opened on the command line, for example via <code>xdg-open $LINK</code> on Linux.</p>
<h2 id="register-an-mcp-server-in-your-extension" data-needslink="register-an-mcp-server-in-your-extension">Register an MCP server in your extension</h2>
<p>To register an MCP server in your extension, you need to perform the following steps:</p>
<ol><li>Define the MCP server definition provider in the <code>package.json</code> file of your extension.</li>
<li>Implement the MCP server definition provider in your extension code by using the <a href="/api/references/vscode-api#lm.registerMcpServerDefinitionProvider"><code>vscode.lm.registerMcpServerDefinitionProvider</code></a> API.</li>
</ol><p>You can get started with a basic <a href="https://github.com/microsoft/vscode-extension-samples/blob/main/mcp-extension-sample" class="external-link" target="_blank">example of how to register an MCP server in a VS Code extension</a>.</p>
<h3 id="1.-static-configuration-in-package.json" data-needslink="1.-static-configuration-in-package.json">1. Static configuration in <code>package.json</code></h3>
<p>Extensions that want to register MCP servers must contribute the <code>contributes.mcpServerDefinitionProviders</code> extension point in the <code>package.json</code> with the <code>id</code> of the provider. This <code>id</code> should match the one used in the implementation.</p>
<pre class="shiki" data-lang="json" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">{</span></span>
<span class="line"><span style="--shiki-dark:#F44747;--shiki-light:#CD3131">    ...</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "contributes"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">        "mcpServerDefinitionProviders"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">            {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">                "id"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"exampleProvider"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">                "label"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"Example MCP Server Provider"</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">            }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">        ]</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    }</span></span>
<span class="line"><span style="--shiki-dark:#F44747;--shiki-light:#CD3131">    ...</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<h3 id="2.-implement-the-provider" data-needslink="2.-implement-the-provider">2. Implement the provider</h3>
<p>To register an MCP server in your extension, use the <a href="/api/references/vscode-api#lm.registerMcpServerDefinitionProvider"><code>vscode.lm.registerMcpServerDefinitionProvider</code></a> API to provide the <a href="/docs/agents/reference/mcp-configuration">MCP configuration</a> for the server. The API takes a <code>providerId</code> string and a <code>McpServerDefinitionProvider</code> object.</p>
<p>The <code>McpServerDefinitionProvider</code> object has three properties:</p>
<ul><li><code>onDidChangeMcpServerDefinitions</code>: event that is triggered when the MCP server configurations change.</li>
<li><code>provideMcpServerDefinitions</code>: function that returns an array of MCP server configurations (<code>vscode.McpServerDefinition[]</code>).</li>
<li><code>resolveMcpServerDefinition</code>: function that the editor calls when the MCP server needs to be started. Use this function to perform additional actions that may require user interaction, such as authentication.</li>
</ul><p>An <code>McpServerDefinition</code> object can be one of the following types:</p>
<ul><li><code>vscode.McpStdioServerDefinition</code>: represents an MCP server available by running a local process and operating on its stdin and stdout streams.</li>
<li><code>vscode.McpHttpServerDefinition</code>: represents an MCP server available using the Streamable HTTP transport.</li>
</ul><details><summary>Example MCP server definition provider</summary><p>The following example demonstrates how to register MCP servers in an extension and prompt the user for an API key when starting the server.</p>
<pre class="shiki" data-lang="ts" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">import</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> *</span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB"> as</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> vscode</span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB"> from</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'vscode'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">export</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> function</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> activate</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">context</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">ExtensionContext</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">    const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> didChangeEmitter</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">new</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">EventEmitter</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">&lt;</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">void</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">&gt;();</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    context</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">subscriptions</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">push</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">lm</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">registerMcpServerDefinitionProvider</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'exampleProvider'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">        onDidChangeMcpServerDefinitions:</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> didChangeEmitter</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">event</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">        provideMcpServerDefinitions</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">:</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> async</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> () </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">=&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">            let</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> servers</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">McpServerDefinition</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">[] = [];</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">            // Example of a simple stdio server definition</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">            servers</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">push</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">new</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">McpStdioServerDefinition</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">            {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">                label:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'myServer'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">                command:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'node'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">                args:</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> [</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'server.js'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">],</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">                cwd:</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">Uri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">file</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'/path/to/server'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">),</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">                env:</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">                    API_KEY:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> ''</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">                },</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">                version:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> '1.0.0'</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">            });</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">            // Example of an HTTP server definition</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">            servers</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">push</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">new</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">McpHttpServerDefinition</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">            {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">                label:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'myRemoteServer'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">                uri:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'http://localhost:3000'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">                headers:</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">                    'API_VERSION'</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> '1.0.0'</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">                },</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">                version:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> '1.0.0'</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">            }));</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">            return</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> servers</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">        },</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">        resolveMcpServerDefinition</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">async</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> (</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">server</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">McpServerDefinition</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">=&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">            if</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> (</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">server</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">label</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> === </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'myServer'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">                // Get the API key from the user, e.g. using vscode.window.showInputBox</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">                // Update the server definition with the API key</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">            }</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">            // Return undefined to indicate that the server should not be started or throw an error</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">            // If there is a pending tool call, the editor will cancel it and return an error message</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">            // to the language model.</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">            return</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> server</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">        }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    }));</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
</details><h2 id="troubleshoot-and-debug-mcp-servers" data-needslink="troubleshoot-and-debug-mcp-servers">Troubleshoot and debug MCP servers</h2>
<h3 id="mcp-development-mode-in-vs-code" data-needslink="mcp-development-mode-in-vs-code">MCP development mode in VS Code</h3>
<p>When developing MCP servers, you can enable <em>development mode</em> for MCP servers by adding a <code>dev</code> key to the MCP server configuration. This is an object with two properties:</p>
<ul><li>
<p><code>watch</code>: A glob pattern, or an array of glob patterns, to watch for file changes that restart the MCP server.</p>
</li>
<li>
<p><code>debug</code>: Enables you to set up a debugger with the MCP server. Currently, VS Code supports debugging Node.js and Python MCP servers.</p>
  <details><summary>Node.js MCP server</summary><p>To debug a Node.js MCP server, set the <code>debug.type</code> property to <code>node</code>.</p>
<pre class="shiki" data-lang="json" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">{</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "servers"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "my-mcp-server"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">      "type"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"stdio"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">      "command"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"node"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">      "cwd"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"${workspaceFolder}"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">      "args"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"./build/index.js"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">],</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">      "dev"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">        "watch"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"src/**/*.ts"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">        "debug"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: { </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">"type"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"node"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
  </details><details><summary>Python MCP server</summary><p>To debug a Python MCP server, set the <code>debug.type</code> property to <code>debugpy</code>, and optionally set the <code>debug.debugpyPath</code> property to the path of the <code>debugpy</code> module if it is not installed in the default Python environment.</p>
<pre class="shiki" data-lang="json" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">{</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "servers"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "my-python-mcp-server"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">      "type"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"stdio"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">      "command"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"python"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">      "cwd"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"${workspaceFolder}"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">      "args"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"./server.py"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">],</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">      "dev"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">        "watch"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"**/*.py"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">        "debug"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">          "type"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"debugpy"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">          "debugpyPath"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"/path/to/debugpy"</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">        }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
  </details></li>
</ul><h3 id="mcp-output-log" data-needslink="mcp-output-log">MCP output log</h3>
<p>When VS Code encounters an issue with an MCP server, it shows an error indicator in the Chat view.</p>
<p><img src="/assets/api/extension-guides/ai/mcp/mcp-error-loading-tool.png" alt="MCP Server Error" loading="lazy"></p>
<p>Select the error notification in the Chat view, and then select the <strong>Show Output</strong> option to view the server logs. Alternatively, run <strong>MCP: List Servers</strong> from the Command Palette, select the server, and then choose <strong>Show Output</strong>.</p>
<p><img src="/assets/api/extension-guides/ai/mcp/mcp-server-error-output.png" alt="MCP Server Error Output" loading="lazy"></p>
<h2 id="best-practices" data-needslink="best-practices">Best practices</h2>
<ul><li><strong>Naming conventions</strong> to ensure unique and descriptive names</li>
<li><strong>Implement proper error handling and validation</strong> with descriptive error messages</li>
<li><strong>Use progress reporting</strong> to inform users about long-running operations</li>
<li><strong>Keep tool operations focused and atomic</strong> to avoid complex interactions</li>
<li><strong>Document your tools clearly</strong> with descriptions that help users understand when to use them</li>
<li><strong>Handle missing input parameters gracefully</strong> by providing default values or clear error messages</li>
<li><strong>Set MIME types for resources</strong> to ensure proper handling of different content types in VS Code</li>
<li><strong>Use resource templates</strong> to allow users to provide input parameters when accessing resources</li>
<li><strong>Cache resource content</strong> to improve performance and reduce unnecessary network requests</li>
<li><strong>Set reasonable token limits</strong> for sampling requests to avoid excessive resource usage</li>
<li><strong>Validate sampling responses</strong> before using them</li>
</ul><h3 id="naming-conventions" data-needslink="naming-conventions">Naming conventions</h3>
<p>The following naming conventions are recommended for MCP servers and their components:</p>
<table class="table table-striped"><thead><tr><th>Component</th>
<th>Naming Convention Guidelines</th>
</tr></thead><tbody><tr><td>Tool name</td>
<td><ul><li>Unique within the MCP server</li><li>Describes the action and the target of the action</li><li>Use snake case, structured as <code>{verb}_{noun}</code></li><li>Examples: <code>generate_report</code>, <code>fetch_data</code>, <code>analyze_code</code></li></ul></td>
</tr><tr><td>Tool input parameter</td>
<td><ul><li>Describes the purpose of the parameter</li><li>Use camelCase for multi-word parameters</li><li>Examples: <code>path</code>, <code>queryString</code>, <code>userId</code></li></ul></td>
</tr><tr><td>Resource name</td>
<td><ul><li>Unique within the MCP server</li><li>Describes the content of the resource</li><li>Use title case</li><li>Examples: <code>Application Logs</code>, <code>Database Table</code>, <code>GitHub Repository</code></li></ul></td>
</tr><tr><td>Resource template parameter</td>
<td><ul><li>Describes the purpose of the parameter</li><li>Use camelCase for multi-word parameters</li><li>Examples: <code>name</code>, <code>repo</code>, <code>fileType</code></li></ul></td>
</tr><tr><td>Prompt name</td>
<td><ul><li>Unique within the MCP server</li><li>Describes the intended use of the prompt</li><li>Use camelCase for multi-word parameters</li><li>Examples: <code>generateApiRoute</code>, <code>performSecurityReview</code>, <code>analyzeCodeQuality</code></li></ul></td>
</tr><tr><td>Prompt input parameter</td>
<td><ul><li>Describes the purpose of the parameter</li><li>Use camelCase for multi-word parameters</li><li>Examples: <code>filePath</code>, <code>queryString</code>, <code>userId</code></li></ul></td>
</tr></tbody></table><h2 id="get-started-to-create-an-mcp-server" data-needslink="get-started-to-create-an-mcp-server">Get started to create an MCP server</h2>
<p>VS Code has all the tools you need to develop your own MCP server. While MCP servers can be written in any language that can handle <code>stdout</code>, the MCP's official SDKs are a good place to start:</p>
<ul><li><a href="https://github.com/modelcontextprotocol/typescript-sdk" class="external-link" target="_blank">TypeScript SDK</a></li>
<li><a href="https://github.com/modelcontextprotocol/python-sdk" class="external-link" target="_blank">Python SDK</a></li>
<li><a href="https://github.com/modelcontextprotocol/java-sdk" class="external-link" target="_blank">Java SDK</a></li>
<li><a href="https://github.com/modelcontextprotocol/kotlin-sdk" class="external-link" target="_blank">Kotlin SDK</a></li>
<li><a href="https://github.com/modelcontextprotocol/csharp-sdk" class="external-link" target="_blank">C# SDK</a></li>
</ul><p>You might also find the <a href="https://github.com/microsoft/mcp-for-beginners" class="external-link" target="_blank">MCP for Beginners curriculum</a> helpful to get started with building your first MCP server.</p>
<h2 id="related-content" data-needslink="related-content">Related content</h2>
<ul><li><a href="/api/extension-guides/ai/tools">Contribute a language model tool</a></li>
<li><a href="/docs/agent-customization/mcp-servers">Use MCP tools in agent mode</a></li>
<li><a href="https://code.visualstudio.com/mcp">VS Code curated list of MCP servers</a></li>
<li><a href="https://modelcontextprotocol.io/" class="external-link" target="_blank">Model Context Protocol Documentation</a></li>
</ul><div class="feedback" data-edit-url="https://vscode.dev/github/microsoft/vscode-docs/blob/main/api/extension-guides/ai/mcp.md"></div>
				
				<div class="body-footer">6/3/2026</div>
				
            </main><aside class="docs-right-sidebar hidden-xs"><div class="docs-markdown-actions">
                    <div class="docs-markdown-dropdown" data-raw-url="/raw/api/extension-guides/ai/mcp.md">
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
                <nav id="docs-subnavbar" aria-label="On Page"><h4><span class="sr-only">On this page there are 10 sections</span><span aria-hidden="true">On this page</span></h4>
                    <ul class="nav"><li><a href="#why-use-mcp-servers">Why use MCP servers?</a></li>
                        
                        <li><a href="#mcp-features-supported-by-vs-code">MCP features supported by VS Code</a></li>
                        
                        <li><a href="#add-mcp-servers-to-vs-code">Add MCP servers to VS Code</a></li>
                        
                        <li><a href="#manage-mcp-servers">Manage MCP servers</a></li>
                        
                        <li><a href="#create-an-mcp-installation-url">Create an MCP installation URL</a></li>
                        
                        <li><a href="#register-an-mcp-server-in-your-extension">Register an MCP server in your extension</a></li>
                        
                        <li><a href="#troubleshoot-and-debug-mcp-servers">Troubleshoot and debug MCP servers</a></li>
                        
                        <li><a href="#best-practices">Best practices</a></li>
                        
                        <li><a href="#get-started-to-create-an-mcp-server">Get started to create an MCP server</a></li>
                        
                        <li><a href="#related-content">Related content</a></li>
                        
                    </ul></nav></aside></div>
		<div class="docs-mobile-widgets visible-xs">
			<div class="connect-widget"></div>
		</div>
	</div>
</div>
		</main>