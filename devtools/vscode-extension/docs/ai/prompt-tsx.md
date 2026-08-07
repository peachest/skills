# Craft language model prompts

> 源文档: [https://code.visualstudio.com/api/extension-guides/ai/prompt-tsx](https://code.visualstudio.com/api/extension-guides/ai/prompt-tsx)

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
			          
			        <li>
			          <a href="/api/extension-guides/ai/language-model-chat-provider">Language Model Chat Provider</a>
			        </li>
			          
			        <li class="active">
			          <a href="/api/extension-guides/ai/prompt-tsx" aria-label="Current Page: Prompt TSX">Prompt TSX</a>
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
				<select id="small-nav-dropdown" aria-label="topics"><option value="/api">Overview</option><optgroup label="Get Started"><option value="/api/get-started/your-first-extension">Your First Extension</option><option value="/api/get-started/extension-anatomy">Extension Anatomy</option><option value="/api/get-started/wrapping-up">Wrapping Up</option></optgroup><optgroup label="Extension Capabilities"><option value="/api/extension-capabilities/overview">Overview</option><option value="/api/extension-capabilities/common-capabilities">Common Capabilities</option><option value="/api/extension-capabilities/theming">Theming</option><option value="/api/extension-capabilities/extending-workbench">Extending Workbench</option></optgroup><optgroup label="Extension Guides"><option value="/api/extension-guides/overview">Overview</option><optgroup label="Extension Guides - AI"><option value="/api/extension-guides/ai/ai-extensibility-overview">AI Extensibility</option><option value="/api/extension-guides/ai/tools">Language Model Tool</option><option value="/api/extension-guides/ai/mcp">MCP Dev Guide</option><option value="/api/extension-guides/ai/chat">Chat Participant</option><option value="/api/extension-guides/ai/chat-tutorial">Chat Tutorial</option><option value="/api/extension-guides/ai/language-model">Language Model</option><option value="/api/extension-guides/ai/language-model-tutorial">Language Model Tutorial</option><option value="/api/extension-guides/ai/language-model-chat-provider">Language Model Chat Provider</option><option value="/api/extension-guides/ai/prompt-tsx" selected>Prompt TSX</option></optgroup><option value="/api/extension-guides/command">Command</option><option value="/api/extension-guides/color-theme">Color Theme</option><option value="/api/extension-guides/file-icon-theme">File Icon Theme</option><option value="/api/extension-guides/product-icon-theme">Product Icon Theme</option><option value="/api/extension-guides/tree-view">Tree View</option><option value="/api/extension-guides/webview">Webview</option><option value="/api/extension-guides/notebook">Notebook</option><option value="/api/extension-guides/custom-editors">Custom Editors</option><option value="/api/extension-guides/virtual-documents">Virtual Documents</option><option value="/api/extension-guides/virtual-workspaces">Virtual Workspaces</option><option value="/api/extension-guides/web-extensions">Web Extensions</option><option value="/api/extension-guides/workspace-trust">Workspace Trust</option><option value="/api/extension-guides/task-provider">Task Provider</option><option value="/api/extension-guides/scm-provider">Source Control</option><option value="/api/extension-guides/debugger-extension">Debugger Extension</option><option value="/api/extension-guides/markdown-extension">Markdown Extension</option><option value="/api/extension-guides/testing">Test Extension</option><option value="/api/extension-guides/custom-data-extension">Custom Data Extension</option><option value="/api/extension-guides/telemetry">Telemetry</option></optgroup><optgroup label="UX Guidelines"><option value="/api/ux-guidelines/overview">Overview</option><option value="/api/ux-guidelines/activity-bar">Activity Bar</option><option value="/api/ux-guidelines/sidebars">Sidebars</option><option value="/api/ux-guidelines/panel">Panel</option><option value="/api/ux-guidelines/status-bar">Status Bar</option><option value="/api/ux-guidelines/views">Views</option><option value="/api/ux-guidelines/editor-actions">Editor Actions</option><option value="/api/ux-guidelines/quick-picks">Quick Picks</option><option value="/api/ux-guidelines/command-palette">Command Palette</option><option value="/api/ux-guidelines/notifications">Notifications</option><option value="/api/ux-guidelines/webviews">Webviews</option><option value="/api/ux-guidelines/context-menus">Context Menus</option><option value="/api/ux-guidelines/walkthroughs">Walkthroughs</option><option value="/api/ux-guidelines/settings">Settings</option></optgroup><optgroup label="Language Extensions"><option value="/api/language-extensions/overview">Overview</option><option value="/api/language-extensions/syntax-highlight-guide">Syntax Highlight Guide</option><option value="/api/language-extensions/semantic-highlight-guide">Semantic Highlight Guide</option><option value="/api/language-extensions/snippet-guide">Snippet Guide</option><option value="/api/language-extensions/language-configuration-guide">Language Configuration Guide</option><option value="/api/language-extensions/programmatic-language-features">Programmatic Language Features</option><option value="/api/language-extensions/language-server-extension-guide">Language Server Extension Guide</option><option value="/api/language-extensions/embedded-languages">Embedded Languages</option></optgroup><optgroup label="Testing and Publishing"><option value="/api/working-with-extensions/testing-extension">Testing Extensions</option><option value="/api/working-with-extensions/publishing-extension">Publishing Extensions</option><option value="/api/working-with-extensions/bundling-extension">Bundling Extensions</option><option value="/api/working-with-extensions/continuous-integration">Continuous Integration</option></optgroup><optgroup label="Advanced Topics"><option value="/api/advanced-topics/extension-host">Extension Host</option><option value="/api/advanced-topics/remote-extensions">Remote Development and Codespaces</option><option value="/api/advanced-topics/using-proposed-api">Using Proposed API</option><option value="/api/advanced-topics/tslint-eslint-migration">Migrate from TSLint to ESLint</option><option value="/api/advanced-topics/python-extension-template">Python Extension Template</option></optgroup><optgroup label="References"><option value="/api/references/vscode-api">VS Code API</option><option value="/api/references/contribution-points">Contribution Points</option><option value="/api/references/activation-events">Activation Events</option><option value="/api/references/extension-manifest">Extension Manifest</option><option value="/api/references/commands">Built-In Commands</option><option value="/api/references/when-clause-contexts">When Clause Contexts</option><option value="/api/references/theme-color">Theme Color</option><option value="/api/references/icons-in-labels">Product Icon Reference</option><option value="/api/references/document-selector">Document Selector</option></optgroup></select></nav></aside><div class="docs-content-wrapper">
			
			<main class="docs-main-content body"><h1>Craft language model prompts</h1>
<p>You can build language model prompts by using string concatenation, but it's hard to compose features and make sure your prompts stay within the context window of language models. To overcome these limitations, you can use the <a href="https://github.com/microsoft/vscode-prompt-tsx" class="external-link" target="_blank"><code>@vscode/prompt-tsx</code></a> library.</p>
<p>The <code>@vscode/prompt-tsx</code> library provides the following features:</p>
<ul><li><strong>TSX-based prompt rendering</strong>: Compose prompts using TSX components, making them more readable and maintainable</li>
<li><strong>Priority-based pruning</strong>: Automatically prune less important parts of prompts to fit within the model's context window</li>
<li><strong>Flexible token management</strong>: Use properties like <code>flexGrow</code>, <code>flexReserve</code>, and <code>flexBasis</code> to cooperatively use token budgets</li>
<li><strong>Tool integration</strong>: Integrate with VS Code's language model tools API</li>
</ul><p>For a complete overview of all features and detailed usage instructions, refer to the <a href="https://github.com/microsoft/vscode-prompt-tsx/blob/main/README.md" class="external-link" target="_blank">full README</a>.</p>
<p>This article describes practical examples of prompt design with the library. The complete code for these examples can be found in the <a href="https://github.com/microsoft/vscode-prompt-tsx/tree/main/examples" class="external-link" target="_blank">prompt-tsx repository</a>.</p>
<h2 id="manage-priorities-in-the-conversation-history" data-needslink="manage-priorities-in-the-conversation-history">Manage priorities in the conversation history</h2>
<p>Including conversation history in your prompt is important as it enables the user to ask follow-up questions to previous messages. However, you want to make sure its priority is treated appropriately because history can grow large over time. We've found that the pattern which makes the most sense is usually to prioritize, in order:</p>
<ol><li>The base prompt instructions</li>
<li>The current user query</li>
<li>The last couple of turns of chat history</li>
<li>Any supporting data</li>
<li>As much of the remaining history as you can fit</li>
</ol><p>For this reason, split the history into two parts in the prompt, where recent prompt turns are prioritized over general contextual information.</p>
<p>In this library, each TSX node in the tree has a priority that is conceptually similar to a zIndex where a higher number means a higher priority.</p>
<h3 id="step-1-define-the-historymessages-component" data-needslink="step-1-define-the-historymessages-component">Step 1: Define the HistoryMessages component</h3>
<p>To list history messages, define a <code>HistoryMessages</code> component. This example provides a good starting point, but you might have to expand it if you deal with more complex data types.</p>
<p>This example uses the <code>PrioritizedList</code> helper component, which automatically assigns ascending or descending priorities to each of its children.</p>
<pre class="shiki" data-lang="tsx" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">import</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">	UserMessage</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">	AssistantMessage</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">	PromptElement</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">	BasePromptElementProps</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">	PrioritizedList</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">} </span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">from</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> '@vscode/prompt-tsx'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">import</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> { </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">ChatContext</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">ChatRequestTurn</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">ChatResponseTurn</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">ChatResponseMarkdownPart</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> } </span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">from</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'vscode'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">interface</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99"> IHistoryMessagesProps</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> extends</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99"> BasePromptElementProps</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">	history</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">ChatContext</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">[</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'history'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">];</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">export</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> class</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99"> HistoryMessages</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> extends</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99"> PromptElement</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">&lt;</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">IHistoryMessagesProps</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">&gt; {</span></span>
<span class="line"><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">	render</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(): </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">PromptPiece</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">		const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> history</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: (</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">UserMessage</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> | </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">AssistantMessage</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">)[] = [];</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">		for</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> (</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> turn</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> of</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> this</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">props</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">history</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">			if</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> (</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">turn</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> instanceof</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99"> ChatRequestTurn</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">				history</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">push</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&lt;</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">UserMessage</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&gt;</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">{</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">turn</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">prompt</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&lt;/</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">UserMessage</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">			} </span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">else</span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB"> if</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> (</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">turn</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> instanceof</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99"> ChatResponseTurn</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">				history</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">push</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span></span>
<span class="line"><span style="--shiki-dark:#808080;--shiki-light:#800000">					&lt;</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">AssistantMessage</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#E50000"> name</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">=</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">{</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">turn</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">participant</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&gt;</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">						{</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">chatResponseToMarkdown</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">turn</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">)</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span></span>
<span class="line"><span style="--shiki-dark:#808080;--shiki-light:#800000">					&lt;/</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">AssistantMessage</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&gt;</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">				);</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">			}</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">		}</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">		return</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> (</span></span>
<span class="line"><span style="--shiki-dark:#808080;--shiki-light:#800000">			&lt;</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">PrioritizedList</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#E50000"> priority</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">=</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">{</span><span style="--shiki-dark:#B5CEA8;--shiki-light:#098658">0</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#E50000"> descending</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">=</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">{false}</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&gt;</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">				{</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">history</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span></span>
<span class="line"><span style="--shiki-dark:#808080;--shiki-light:#800000">			&lt;/</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">PrioritizedList</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&gt;</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">		);</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">	}</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<h3 id="step-2-define-the-prompt-component" data-needslink="step-2-define-the-prompt-component">Step 2: Define the Prompt component</h3>
<p>Next, define a <code>MyPrompt</code> component that includes the base instructions, user query, and history messages with their appropriate priorities. Priority values are local among siblings. Remember that you might want to trim older messages in the history before touching anything else in the prompt, so you need to split up two <code>&lt;HistoryMessages&gt;</code> elements:</p>
<pre class="shiki" data-lang="tsx" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">import</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">	UserMessage</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">	PromptElement</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">	BasePromptElementProps</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">} </span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">from</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> '@vscode/prompt-tsx'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">interface</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99"> IMyPromptProps</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> extends</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99"> BasePromptElementProps</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">	history</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">ChatContext</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">[</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'history'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">];</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">	userQuery</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">string</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">export</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> class</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99"> MyPrompt</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> extends</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99"> PromptElement</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">&lt;</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">IMyPromptProps</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">&gt; {</span></span>
<span class="line"><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">	render</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">() {</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">		return</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> (</span></span>
<span class="line"><span style="--shiki-dark:#808080;--shiki-light:#800000">			&lt;&gt;</span></span>
<span class="line"><span style="--shiki-dark:#808080;--shiki-light:#800000">				&lt;</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">UserMessage</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#E50000"> priority</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">=</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">{</span><span style="--shiki-dark:#B5CEA8;--shiki-light:#098658">100</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&gt;</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">					Here are your base instructions. They have the highest priority because you want to make</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">					sure they're always included!</span></span>
<span class="line"><span style="--shiki-dark:#808080;--shiki-light:#800000">				&lt;/</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">UserMessage</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&gt;</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">				{</span><span style="--shiki-dark:#6A9955;--shiki-light:#008000">/* Older messages in the history have the lowest priority since they're less relevant */</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span></span>
<span class="line"><span style="--shiki-dark:#808080;--shiki-light:#800000">				&lt;</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">HistoryMessages</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#E50000"> history</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">=</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">{this</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">props</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">history</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">slice</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">(</span><span style="--shiki-dark:#B5CEA8;--shiki-light:#098658">0</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">, </span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">-</span><span style="--shiki-dark:#B5CEA8;--shiki-light:#098658">2</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">)</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#E50000"> priority</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">=</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">{</span><span style="--shiki-dark:#B5CEA8;--shiki-light:#098658">0</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#808080;--shiki-light:#800000"> /&gt;</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">				{</span><span style="--shiki-dark:#6A9955;--shiki-light:#008000">/* The last 2 history messages are preferred over any workspace context you have below */</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span></span>
<span class="line"><span style="--shiki-dark:#808080;--shiki-light:#800000">				&lt;</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">HistoryMessages</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#E50000"> history</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">=</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">{this</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">props</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">history</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">slice</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">(</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">-</span><span style="--shiki-dark:#B5CEA8;--shiki-light:#098658">2</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">)</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#E50000"> priority</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">=</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">{</span><span style="--shiki-dark:#B5CEA8;--shiki-light:#098658">80</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#808080;--shiki-light:#800000"> /&gt;</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">				{</span><span style="--shiki-dark:#6A9955;--shiki-light:#008000">/* The user query is right behind the based instructions in priority */</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span></span>
<span class="line"><span style="--shiki-dark:#808080;--shiki-light:#800000">				&lt;</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">UserMessage</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#E50000"> priority</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">=</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">{</span><span style="--shiki-dark:#B5CEA8;--shiki-light:#098658">90</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&gt;</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">{this</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">props</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">userQuery</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&lt;/</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">UserMessage</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&gt;</span></span>
<span class="line"><span style="--shiki-dark:#808080;--shiki-light:#800000">				&lt;</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">UserMessage</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#E50000"> priority</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">=</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">{</span><span style="--shiki-dark:#B5CEA8;--shiki-light:#098658">70</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&gt;</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">					With a slightly lower priority, you can include some contextual data about the workspace</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">					or files here...</span></span>
<span class="line"><span style="--shiki-dark:#808080;--shiki-light:#800000">				&lt;/</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">UserMessage</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&gt;</span></span>
<span class="line"><span style="--shiki-dark:#808080;--shiki-light:#800000">			&lt;/&gt;</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">		);</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">	}</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<p>Now, all older history messages are pruned before the library tries to prune other elements of the prompt.</p>
<h3 id="step-3-define-the-history-component" data-needslink="step-3-define-the-history-component">Step 3: Define the History component</h3>
<p>To make consumption a little easier, define a <code>History</code> component that wraps the history messages and uses the <code>passPriority</code> attribute to act as a pass-through container. With <code>passPriority</code>, its children are treated as if they are direct children of the containing element for prioritization purposes.</p>
<pre class="shiki" data-lang="tsx" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">import</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> { </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">PromptElement</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">BasePromptElementProps</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> } </span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">from</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> '@vscode/prompt-tsx'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">interface</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99"> IHistoryProps</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> extends</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99"> BasePromptElementProps</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">	history</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">ChatContext</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">[</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'history'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">];</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">	newer</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">number</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">; </span><span style="--shiki-dark:#6A9955;--shiki-light:#008000">// last 2 message priority values</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">	older</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">number</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">; </span><span style="--shiki-dark:#6A9955;--shiki-light:#008000">// previous message priority values</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">	passPriority</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">true</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">; </span><span style="--shiki-dark:#6A9955;--shiki-light:#008000">// require this prop be set!</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">export</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> class</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99"> History</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> extends</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99"> PromptElement</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">&lt;</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">IHistoryProps</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">&gt; {</span></span>
<span class="line"><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">	render</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(): </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">PromptPiece</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">		return</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> (</span></span>
<span class="line"><span style="--shiki-dark:#808080;--shiki-light:#800000">			&lt;&gt;</span></span>
<span class="line"><span style="--shiki-dark:#808080;--shiki-light:#800000">				&lt;</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">HistoryMessages</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#E50000"> history</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">=</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">{this</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">props</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">history</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">slice</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">(</span><span style="--shiki-dark:#B5CEA8;--shiki-light:#098658">0</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">, </span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">-</span><span style="--shiki-dark:#B5CEA8;--shiki-light:#098658">2</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">)</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#E50000"> priority</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">=</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">{this</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">props</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">older</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#808080;--shiki-light:#800000"> /&gt;</span></span>
<span class="line"><span style="--shiki-dark:#808080;--shiki-light:#800000">				&lt;</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">HistoryMessages</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#E50000"> history</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">=</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">{this</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">props</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">history</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">slice</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">(</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">-</span><span style="--shiki-dark:#B5CEA8;--shiki-light:#098658">2</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">)</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#E50000"> priority</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">=</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">{this</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">props</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">newer</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#808080;--shiki-light:#800000"> /&gt;</span></span>
<span class="line"><span style="--shiki-dark:#808080;--shiki-light:#800000">			&lt;/&gt;</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">		);</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">	}</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<p>Now, you can use and reuse this single element to include chat history:</p>
<pre class="shiki" data-lang="tsx" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#808080;--shiki-light:#800000">&lt;</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">History</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#E50000"> history</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">=</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">{this</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">props</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">history</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#E50000"> passPriority</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#E50000"> older</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">=</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">{</span><span style="--shiki-dark:#B5CEA8;--shiki-light:#098658">0</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#E50000"> newer</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">=</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">{</span><span style="--shiki-dark:#B5CEA8;--shiki-light:#098658">80</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#808080;--shiki-light:#800000">/&gt;</span></span>
<span class="line"></span></code></pre>
<h2 id="grow-file-contents-to-fit" data-needslink="grow-file-contents-to-fit">Grow file contents to fit</h2>
<p>In this example, you want to include the contents of all files the user is currently looking at in their prompt. These files could be large, to the point where including all of them would lead to their text being pruned! This example shows how to use the <code>flexGrow</code> property to cooperatively size the file contents to fit within the token budget.</p>
<h3 id="step-1-define-base-instructions-and-user-query" data-needslink="step-1-define-base-instructions-and-user-query">Step 1: Define base instructions and user query</h3>
<p>First, you define a <code>UserMessage</code> component that includes the base instructions.</p>
<pre class="shiki" data-lang="tsx" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#808080;--shiki-light:#800000">&lt;</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">UserMessage</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#E50000"> priority</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">=</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">{</span><span style="--shiki-dark:#B5CEA8;--shiki-light:#098658">100</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">Here are your base instructions.</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&lt;/</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">UserMessage</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&gt;</span></span>
<span class="line"></span></code></pre>
<p>You then include the user query by using the <code>UserMessage</code> component. This component has a high priority to ensure it is included right after the base instructions.</p>
<pre class="shiki" data-lang="tsx" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#808080;--shiki-light:#800000">&lt;</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">UserMessage</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#E50000"> priority</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">=</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">{</span><span style="--shiki-dark:#B5CEA8;--shiki-light:#098658">90</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&gt;</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">{this</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">props</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">userQuery</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&lt;/</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">UserMessage</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&gt;</span></span>
<span class="line"></span></code></pre>
<h3 id="step-2-include-the-file-contents" data-needslink="step-2-include-the-file-contents">Step 2: Include the File Contents</h3>
<p>You can now include the file contents by using the <code>FileContext</code> component. You assign it a <a href="https://github.com/microsoft/vscode-prompt-tsx?tab=readme-ov-file#flex-behavior" class="external-link" target="_blank"><code>flexGrow</code></a> value of <code>1</code> to ensure it is rendered after the base instructions, user query, and history.</p>
<pre class="shiki" data-lang="tsx" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#808080;--shiki-light:#800000">&lt;</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">FileContext</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#E50000"> priority</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">=</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">{</span><span style="--shiki-dark:#B5CEA8;--shiki-light:#098658">70</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#E50000"> flexGrow</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">=</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">{</span><span style="--shiki-dark:#B5CEA8;--shiki-light:#098658">1</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#E50000"> files</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">=</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">{this</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">props</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">files</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#808080;--shiki-light:#800000"> /&gt;</span></span>
<span class="line"></span></code></pre>
<p>With a <code>flexGrow</code> value, the element gets any <em>unused</em> token budget in its <code>PromptSizing</code> object that's passed into its <code>render()</code> and <code>prepare()</code> calls. You can read more about the behavior of flex elements in the <a href="https://github.com/microsoft/vscode-prompt-tsx?tab=readme-ov-file#flex-behavior" class="external-link" target="_blank">prompt-tsx documentation</a>.</p>
<h3 id="step-3-include-the-history" data-needslink="step-3-include-the-history">Step 3: Include the history</h3>
<p>Next, include the history messages using the <code>History</code> component that you created previously. This is a little trickier, since you do want some history to be shown, but also want the file contents to take up most the prompt.</p>
<p>Therefore, assign the <code>History</code> component a <code>flexGrow</code> value of <code>2</code> to ensure it is rendered after all other elements, including <code>&lt;FileContext /&gt;</code>. But, also set a <code>flexReserve</code> value of <code>"/5"</code> to reserve 1/5th of the total budget for history.</p>
<pre class="shiki" data-lang="tsx" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#808080;--shiki-light:#800000">&lt;</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">History</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#E50000">	history</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">=</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">{this</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">props</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">history</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#E50000">	passPriority</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#E50000">	older</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">=</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">{</span><span style="--shiki-dark:#B5CEA8;--shiki-light:#098658">0</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#E50000">	newer</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">=</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">{</span><span style="--shiki-dark:#B5CEA8;--shiki-light:#098658">80</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#E50000">	flexGrow</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">=</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">{</span><span style="--shiki-dark:#B5CEA8;--shiki-light:#098658">2</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#E50000">	flexReserve</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">=</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"/5"</span></span>
<span class="line"><span style="--shiki-dark:#808080;--shiki-light:#800000">/&gt;</span></span>
<span class="line"></span></code></pre>
<h3 id="step-3-combine-all-elements-of-the-prompt" data-needslink="step-3-combine-all-elements-of-the-prompt">Step 3: Combine all elements of the prompt</h3>
<p>Now, combine all the elements into the <code>MyPrompt</code> component.</p>
<pre class="shiki" data-lang="tsx" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">import</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">	UserMessage</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">	PromptElement</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">	BasePromptElementProps</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">} </span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">from</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> '@vscode/prompt-tsx'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">import</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> { </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">History</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> } </span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">from</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> './history'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">interface</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99"> IFilesToInclude</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">	document</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">TextDocument</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">	line</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">number</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">interface</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99"> IMyPromptProps</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> extends</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99"> BasePromptElementProps</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">	history</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">ChatContext</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">[</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'history'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">];</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">	userQuery</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">string</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">	files</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">IFilesToInclude</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">[];</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">export</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> class</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99"> MyPrompt</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> extends</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99"> PromptElement</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">&lt;</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">IMyPromptProps</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">&gt; {</span></span>
<span class="line"><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">	render</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">() {</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">		return</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> (</span></span>
<span class="line"><span style="--shiki-dark:#808080;--shiki-light:#800000">			&lt;&gt;</span></span>
<span class="line"><span style="--shiki-dark:#808080;--shiki-light:#800000">				&lt;</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">UserMessage</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#E50000"> priority</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">=</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">{</span><span style="--shiki-dark:#B5CEA8;--shiki-light:#098658">100</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">Here are your base instructions.</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&lt;/</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">UserMessage</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&gt;</span></span>
<span class="line"><span style="--shiki-dark:#808080;--shiki-light:#800000">				&lt;</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">History</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#E50000">					history</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">=</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">{this</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">props</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">history</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#E50000">					passPriority</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#E50000">					older</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">=</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">{</span><span style="--shiki-dark:#B5CEA8;--shiki-light:#098658">0</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#E50000">					newer</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">=</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">{</span><span style="--shiki-dark:#B5CEA8;--shiki-light:#098658">80</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#E50000">					flexGrow</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">=</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">{</span><span style="--shiki-dark:#B5CEA8;--shiki-light:#098658">2</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#E50000">					flexReserve</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">=</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"/5"</span></span>
<span class="line"><span style="--shiki-dark:#808080;--shiki-light:#800000">				/&gt;</span></span>
<span class="line"><span style="--shiki-dark:#808080;--shiki-light:#800000">				&lt;</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">UserMessage</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#E50000"> priority</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">=</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">{</span><span style="--shiki-dark:#B5CEA8;--shiki-light:#098658">90</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&gt;</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">{this</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">props</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">userQuery</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&lt;/</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">UserMessage</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&gt;</span></span>
<span class="line"><span style="--shiki-dark:#808080;--shiki-light:#800000">				&lt;</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">FileContext</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#E50000"> priority</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">=</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">{</span><span style="--shiki-dark:#B5CEA8;--shiki-light:#098658">70</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#E50000"> flexGrow</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">=</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">{</span><span style="--shiki-dark:#B5CEA8;--shiki-light:#098658">1</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#E50000"> files</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">=</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">{this</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">props</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">files</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#808080;--shiki-light:#800000"> /&gt;</span></span>
<span class="line"><span style="--shiki-dark:#808080;--shiki-light:#800000">			&lt;/&gt;</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">		);</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">	}</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<h3 id="step-4-define-the-filecontext-component" data-needslink="step-4-define-the-filecontext-component">Step 4: Define the FileContext component</h3>
<p>Finally, define a <code>FileContext</code> component that includes the contents of the files the user is currently looking at. Because you used <code>flexGrow</code>, you can implement logic that gets as many of the lines around the 'interesting' line for each file by using the information in <code>PromptSizing</code>.</p>
<p>For brevity, the implementation logic for <code>getExpandedFiles</code> is omitted. You can check it out in the <a href="https://github.com/microsoft/vscode-prompt-tsx/blob/5501d54a5b9a7608582e8419cd968a82ca317cc9/examples/file-contents.tsx#L103" class="external-link" target="_blank">prompt-tsx repo</a>.</p>
<pre class="shiki" data-lang="tsx" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">import</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> { </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">PromptElement</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">BasePromptElementProps</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">PromptSizing</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">PromptPiece</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> } </span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">from</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> '@vscode/prompt-tsx'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">class</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99"> FileContext</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> extends</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99"> PromptElement</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">&lt;{ </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">files</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">IFilesToInclude</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">[] } &amp; </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">BasePromptElementProps</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">&gt; {</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">	async</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> render</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">_state</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">void</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">sizing</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">PromptSizing</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">): </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">Promise</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">&lt;</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">PromptPiece</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">&gt; {</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">		const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> files</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">await</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> this</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">getExpandedFiles</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">sizing</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">		return</span><span style="--shiki-dark:#808080;--shiki-light:#800000"> &lt;&gt;</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">{</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">files</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">map</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">f</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> =&gt;</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> f</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">toString</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000FF">())</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">}</span><span style="--shiki-dark:#808080;--shiki-light:#800000">&lt;/&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">	}</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">	private</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> async</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> getExpandedFiles</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">sizing</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">PromptSizing</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">		// Implementation details are summarized here.</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">		// Refer to the repo for the complete implementation.</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">	}</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<h2 id="summary" data-needslink="summary">Summary</h2>
<p>In these examples, you created a <code>MyPrompt</code> component that includes base instructions, user query, history messages, and file contents with different priorities. You used <code>flexGrow</code> to cooperatively size the file contents to fit within the token budget.</p>
<p>By following this pattern, you can ensure that the most important parts of your prompt are always included, while less important parts are pruned as needed to fit within the model's context window. For the complete implementation details of the <code>getExpandedFiles</code> method and the <code>FileContextTracker</code> class, refer to the <a href="https://github.com/microsoft/vscode-prompt-tsx/tree/main/examples" class="external-link" target="_blank">prompt-tsx repo</a>.</p>

				<div class="feedback" data-edit-url="https://vscode.dev/github/microsoft/vscode-docs/blob/main/api/extension-guides/ai/prompt-tsx.md"></div>
				
				<div class="body-footer">6/3/2026</div>
				
            </main><aside class="docs-right-sidebar hidden-xs"><div class="docs-markdown-actions">
                    <div class="docs-markdown-dropdown" data-raw-url="/raw/api/extension-guides/ai/prompt-tsx.md">
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
                    <ul class="nav"><li><a href="#manage-priorities-in-the-conversation-history">Manage priorities in the conversation history</a></li>
                        
                        <li><a href="#grow-file-contents-to-fit">Grow file contents to fit</a></li>
                        
                        <li><a href="#summary">Summary</a></li>
                        
                    </ul></nav></aside></div>
		<div class="docs-mobile-widgets visible-xs">
			<div class="connect-widget"></div>
		</div>
	</div>
</div>
		</main>