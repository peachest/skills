# Language Model API

> 源文档: [https://code.visualstudio.com/api/extension-guides/ai/language-model](https://code.visualstudio.com/api/extension-guides/ai/language-model)

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
			          
			        <li class="active">
			          <a href="/api/extension-guides/ai/language-model" aria-label="Current Page: Language Model">Language Model</a>
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
				<select id="small-nav-dropdown" aria-label="topics"><option value="/api">Overview</option><optgroup label="Get Started"><option value="/api/get-started/your-first-extension">Your First Extension</option><option value="/api/get-started/extension-anatomy">Extension Anatomy</option><option value="/api/get-started/wrapping-up">Wrapping Up</option></optgroup><optgroup label="Extension Capabilities"><option value="/api/extension-capabilities/overview">Overview</option><option value="/api/extension-capabilities/common-capabilities">Common Capabilities</option><option value="/api/extension-capabilities/theming">Theming</option><option value="/api/extension-capabilities/extending-workbench">Extending Workbench</option></optgroup><optgroup label="Extension Guides"><option value="/api/extension-guides/overview">Overview</option><optgroup label="Extension Guides - AI"><option value="/api/extension-guides/ai/ai-extensibility-overview">AI Extensibility</option><option value="/api/extension-guides/ai/tools">Language Model Tool</option><option value="/api/extension-guides/ai/mcp">MCP Dev Guide</option><option value="/api/extension-guides/ai/chat">Chat Participant</option><option value="/api/extension-guides/ai/chat-tutorial">Chat Tutorial</option><option value="/api/extension-guides/ai/language-model" selected>Language Model</option><option value="/api/extension-guides/ai/language-model-tutorial">Language Model Tutorial</option><option value="/api/extension-guides/ai/language-model-chat-provider">Language Model Chat Provider</option><option value="/api/extension-guides/ai/prompt-tsx">Prompt TSX</option></optgroup><option value="/api/extension-guides/command">Command</option><option value="/api/extension-guides/color-theme">Color Theme</option><option value="/api/extension-guides/file-icon-theme">File Icon Theme</option><option value="/api/extension-guides/product-icon-theme">Product Icon Theme</option><option value="/api/extension-guides/tree-view">Tree View</option><option value="/api/extension-guides/webview">Webview</option><option value="/api/extension-guides/notebook">Notebook</option><option value="/api/extension-guides/custom-editors">Custom Editors</option><option value="/api/extension-guides/virtual-documents">Virtual Documents</option><option value="/api/extension-guides/virtual-workspaces">Virtual Workspaces</option><option value="/api/extension-guides/web-extensions">Web Extensions</option><option value="/api/extension-guides/workspace-trust">Workspace Trust</option><option value="/api/extension-guides/task-provider">Task Provider</option><option value="/api/extension-guides/scm-provider">Source Control</option><option value="/api/extension-guides/debugger-extension">Debugger Extension</option><option value="/api/extension-guides/markdown-extension">Markdown Extension</option><option value="/api/extension-guides/testing">Test Extension</option><option value="/api/extension-guides/custom-data-extension">Custom Data Extension</option><option value="/api/extension-guides/telemetry">Telemetry</option></optgroup><optgroup label="UX Guidelines"><option value="/api/ux-guidelines/overview">Overview</option><option value="/api/ux-guidelines/activity-bar">Activity Bar</option><option value="/api/ux-guidelines/sidebars">Sidebars</option><option value="/api/ux-guidelines/panel">Panel</option><option value="/api/ux-guidelines/status-bar">Status Bar</option><option value="/api/ux-guidelines/views">Views</option><option value="/api/ux-guidelines/editor-actions">Editor Actions</option><option value="/api/ux-guidelines/quick-picks">Quick Picks</option><option value="/api/ux-guidelines/command-palette">Command Palette</option><option value="/api/ux-guidelines/notifications">Notifications</option><option value="/api/ux-guidelines/webviews">Webviews</option><option value="/api/ux-guidelines/context-menus">Context Menus</option><option value="/api/ux-guidelines/walkthroughs">Walkthroughs</option><option value="/api/ux-guidelines/settings">Settings</option></optgroup><optgroup label="Language Extensions"><option value="/api/language-extensions/overview">Overview</option><option value="/api/language-extensions/syntax-highlight-guide">Syntax Highlight Guide</option><option value="/api/language-extensions/semantic-highlight-guide">Semantic Highlight Guide</option><option value="/api/language-extensions/snippet-guide">Snippet Guide</option><option value="/api/language-extensions/language-configuration-guide">Language Configuration Guide</option><option value="/api/language-extensions/programmatic-language-features">Programmatic Language Features</option><option value="/api/language-extensions/language-server-extension-guide">Language Server Extension Guide</option><option value="/api/language-extensions/embedded-languages">Embedded Languages</option></optgroup><optgroup label="Testing and Publishing"><option value="/api/working-with-extensions/testing-extension">Testing Extensions</option><option value="/api/working-with-extensions/publishing-extension">Publishing Extensions</option><option value="/api/working-with-extensions/bundling-extension">Bundling Extensions</option><option value="/api/working-with-extensions/continuous-integration">Continuous Integration</option></optgroup><optgroup label="Advanced Topics"><option value="/api/advanced-topics/extension-host">Extension Host</option><option value="/api/advanced-topics/remote-extensions">Remote Development and Codespaces</option><option value="/api/advanced-topics/using-proposed-api">Using Proposed API</option><option value="/api/advanced-topics/tslint-eslint-migration">Migrate from TSLint to ESLint</option><option value="/api/advanced-topics/python-extension-template">Python Extension Template</option></optgroup><optgroup label="References"><option value="/api/references/vscode-api">VS Code API</option><option value="/api/references/contribution-points">Contribution Points</option><option value="/api/references/activation-events">Activation Events</option><option value="/api/references/extension-manifest">Extension Manifest</option><option value="/api/references/commands">Built-In Commands</option><option value="/api/references/when-clause-contexts">When Clause Contexts</option><option value="/api/references/theme-color">Theme Color</option><option value="/api/references/icons-in-labels">Product Icon Reference</option><option value="/api/references/document-selector">Document Selector</option></optgroup></select></nav></aside><div class="docs-content-wrapper">
			
			<main class="docs-main-content body"><h1>Language Model API</h1>
<p>The Language Model API enables you to <a href="/api/references/vscode-api#lm">use the Language Model</a> and integrate AI-powered features and natural language processing in your Visual Studio Code extension.</p>
<p>You can use the Language Model API in different types of extensions. A typical use for this API is in <a href="/api/extension-guides/ai/chat">chat extensions</a>, where you use a language model to interpret the user's request and help provide an answer. However, the use of the Language Model API is not limited to this scenario. You might use a language model in a <a href="/api/language-extensions/overview">language</a> or <a href="/api/extension-guides/debugger-extension">debugger</a> extension, or as part of a <a href="/api/extension-guides/command">command</a> or <a href="/api/extension-guides/task-provider">task</a> in a custom extension. For example, the Rust extension might use the Language Model to offer default names to improve its rename experience.</p>
<p>The process for using the Language Model API consists of the following steps:</p>
<ol><li>Build the language model prompt</li>
<li>Send the language model request</li>
<li>Interpret the response</li>
</ol><p>The following sections provide more details on how to implement these steps in your extension.</p>
<p>To get started, you can explore the <a href="https://github.com/microsoft/vscode-extension-samples/tree/main/chat-sample" class="external-link" target="_blank">chat extension sample</a>.</p>
<h2 id="build-the-language-model-prompt" data-needslink="build-the-language-model-prompt">Build the language model prompt</h2>
<p>To interact with a language model, extensions should first craft their prompt, and then send a request to the language model. You can use prompts to provide instructions to the language model on the broad task that you're using the model for. Prompts can also define the context in which user messages are interpreted.</p>
<p>The Language Model API supports two types of messages when building the language model prompt:</p>
<ul><li><strong>User</strong> - used for providing instructions and the user's request</li>
<li><strong>Assistant</strong> - used for adding the history of previous language model responses as context to the prompt</li>
</ul><blockquote><p><strong>Note</strong>: Currently, the Language Model API doesn't support the use of system messages.</p>
</blockquote><p>You can use two approaches for building the language model prompt:</p>
<ul><li><code>LanguageModelChatMessage</code> - create the prompt by providing one or more messages as strings. You might use this approach if you're just getting started with the Language Model API.</li>
<li><a href="https://www.npmjs.com/package/@vscode/prompt-tsx" class="external-link" target="_blank"><code>@vscode/prompt-tsx</code></a> - declare the prompt by using the TSX syntax.</li>
</ul><p>You can use the <code>prompt-tsx</code> library if you want more control over how the language model prompt is composed. For example, the library can help with dynamically adapting the length of the prompt to each language model's context window size. Learn more about <a href="https://www.npmjs.com/package/@vscode/prompt-tsx" class="external-link" target="_blank"><code>@vscode/prompt-tsx</code></a> or explore the <a href="https://github.com/microsoft/vscode-extension-samples/tree/main/chat-sample" class="external-link" target="_blank">chat extension sample</a> to get started.</p>
<p>To learn more about the concepts of prompt engineering, we suggest reading OpenAI's excellent <a href="https://platform.openai.com/docs/guides/prompt-engineering" class="external-link" target="_blank">Prompt engineering guidelines</a>.</p>
<blockquote><p><strong>Tip:</strong> take advantage of the rich VS Code extension API to get the most relevant context and include it in your prompt. For example, to include the contents of the active file in the editor.</p>
</blockquote><h3 id="use-the-languagemodelchatmessage-class" data-needslink="use-the-languagemodelchatmessage-class">Use the <code>LanguageModelChatMessage</code> class</h3>
<p>The Language Model API provides the <code>LanguageModelChatMessage</code> class to represent and create chat messages. You can use the <code>LanguageModelChatMessage.User</code> or <code>LanguageModelChatMessage.Assistant</code> methods to create user or assistant messages respectively.</p>
<p>In the following example, the first message provides context for the prompt:</p>
<ul><li>The persona used by the model in its replies (in this case, a cat)</li>
<li>The rules the model should follow when generating responses (in this case, explaining computer science concepts in a funny manner by using cat metaphors)</li>
</ul><p>The second message then provides the specific request or instruction coming from the user. It determines the specific task to be accomplished, given the context provided by the first message.</p>
<pre class="shiki" data-lang="typescript" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> craftedPrompt</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = [</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">LanguageModelChatMessage</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">User</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">    'You are a cat! Think carefully and step by step like a cat would. Your job is to explain computer science concepts in the funny manner of a cat, using cat metaphors. Always start your response by stating what concept you are explaining. Always include code samples.'</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  ),</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">LanguageModelChatMessage</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">User</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'I want to understand recursion'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">)</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">];</span></span>
<span class="line"></span></code></pre>
<h2 id="send-the-language-model-request" data-needslink="send-the-language-model-request">Send the language model request</h2>
<p>Once you've built the prompt for the language model, you first select the language model you want to use with the <a href="/api/references/vscode-api#lm.selectChatModels"><code>selectChatModels</code></a> method. This method returns an array of language models that match the specified criteria. If you are implementing a chat participant, we recommend that you instead use the model that is passed as part of the <code>request</code> object in your chat request handler. This ensures that your extension respects the model that the user chose in the chat model dropdown. Then, you send the request to the language model by using the <a href="/api/references/vscode-api#LanguageModelChat"><code>sendRequest</code></a> method.</p>
<p>To select the language model, you can specify the following properties: <code>vendor</code>, <code>id</code>, <code>family</code>, or <code>version</code>. Use these properties to either broadly match all models of a given vendor or family, or select one specific model by its ID. Learn more about these properties in the <a href="/api/references/vscode-api#LanguageModelChat">API reference</a>.</p>
<blockquote><p><strong>Note</strong>: Currently, <code>gpt-4o</code>, <code>gpt-4o-mini</code>, <code>o1</code>, <code>o1-mini</code>, <code>claude-3.5-sonnet</code> are supported for the language model family. If you are unsure what model to use, we recommend <code>gpt-4o</code> for it's performance and quality. For interactions directly in the editor, we recommend <code>gpt-4o-mini</code> for it's performance.</p>
</blockquote><p>If there are no models that match the specified criteria, the <code>selectChatModels</code> method returns an empty array. Your extension must appropriately handle this case.</p>
<p>The following example shows how to select all <code>Copilot</code> models, regardless of the family or version:</p>
<pre class="shiki" data-lang="typescript" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> models</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">await</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">lm</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">selectChatModels</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">({</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  vendor:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'copilot'</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">});</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">// No models available</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">if</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> (</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">models</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">length</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> === </span><span style="--shiki-dark:#B5CEA8;--shiki-light:#098658">0</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">  // TODO: handle the case when no models are available</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<blockquote><p><strong>Important</strong>: Copilot's language models require consent from the user before an extension can use them. Consent is implemented as an authentication dialog. Because of that, <code>selectChatModels</code> should be called as part of a user-initiated action, such as a command.</p>
</blockquote><p>After you select a model, you can send a request to the language model by invoking the <a href="/api/references/vscode-api#LanguageModelChat"><code>sendRequest</code></a> method on the model instance. You pass the <a href="#_build-the-language-model-prompt">prompt</a> you crafted earlier, along with any additional options, and a cancellation token.</p>
<p>When you make a request to the Language Model API, the request might fail. For example, because the model doesn't exist, or the user didn't give consent to use the Language Model API, or because quota limits are exceeded. Use <code>LanguageModelError</code> to distinguish between different types of errors.</p>
<p>The following code snippet shows how to make a language model request:</p>
<pre class="shiki" data-lang="typescript" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">try</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">  const</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> [</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1">model</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">] = </span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">await</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">lm</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">selectChatModels</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">({ </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">vendor:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'copilot'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">family:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'gpt-4o'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> });</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">  const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> request</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">model</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">sendRequest</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">craftedPrompt</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, {}, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">token</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">} </span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">catch</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> (</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">err</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">  // Making the chat request might fail because</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">  // - model does not exist</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">  // - user consent not given</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">  // - quota limits were exceeded</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">  if</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> (</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">err</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> instanceof</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99"> vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">LanguageModelError</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">    console</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">log</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">err</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">message</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">err</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">code</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">err</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">cause</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">    if</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> (</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">err</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">cause</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> instanceof</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99"> Error</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> &amp;&amp; </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">err</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">cause</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">message</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">includes</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'off_topic'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">)) {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">      stream</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">markdown</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">        vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">l10n</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">t</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"I'm sorry, I can only explain computer science concepts."</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">)</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      );</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  } </span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">else</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">    // add other error handling logic</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">    throw</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> err</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<h2 id="interpret-the-response" data-needslink="interpret-the-response">Interpret the response</h2>
<p>After you've sent the request, you have to process the response from the language model API. Depending on your usage scenario, you can pass the response directly on to the user, or you can interpret the response and perform extra logic.</p>
<p>The response (<a href="/api/references/vscode-api#LanguageModelChatResponse"><code>LanguageModelChatResponse</code></a>) from the Language Model API is streaming-based, which enables you to provide a smooth user experience. For example, by reporting results and progress continuously when you use the API in combination with the <a href="/api/extension-guides/ai/chat">Chat API</a>.</p>
<p>Errors might occur while processing the streaming response, such as network connection issues. Make sure to add appropriate error handling in your code to handle these errors.</p>
<p>The following code snippet shows how an extension can register a command, which uses the language model to change all variable names in the active editor with funny cat names. Notice that the extension streams the code back to the editor for a smooth user experience.</p>
<pre class="shiki" data-lang="typescript" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">commands</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">registerTextEditorCommand</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">  'cat.namesInEditor'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">  async</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> (</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">textEditor</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">TextEditor</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">=&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">    // Replace all variables in active editor with cat names and words</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">    const</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> [</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1">model</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">] = </span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">await</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">lm</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">selectChatModels</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">({</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">      vendor:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'copilot'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">      family:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'gpt-4o'</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    });</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">    let</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> chatResponse</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">LanguageModelChatResponse</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> | </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">undefined</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">    const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> text</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">textEditor</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">document</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">getText</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">();</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">    const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> messages</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = [</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">      vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">LanguageModelChatMessage</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">        .</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">User</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">`You are a cat! Think carefully and step by step like a cat would.</span></span>
<span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">        Your job is to replace all variable names in the following code with funny cat variable names. Be creative. IMPORTANT respond just with code. Do not use markdown!`</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">),</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">      vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">LanguageModelChatMessage</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">User</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">text</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">)</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    ];</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">    try</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">      chatResponse</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">await</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> model</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">sendRequest</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">        messages</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">        {},</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">        new</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">CancellationTokenSource</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">().</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">token</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      );</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    } </span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">catch</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> (</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">err</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">      if</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> (</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">err</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> instanceof</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99"> vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">LanguageModelError</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">        console</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">log</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">err</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">message</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">err</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">code</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">err</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">cause</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      } </span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">else</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">        throw</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> err</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      }</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">      return</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    }</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">    // Clear the editor content before inserting new content</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">    await</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> textEditor</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">edit</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">edit</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> =&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">      const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> start</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">new</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">Position</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#B5CEA8;--shiki-light:#098658">0</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#B5CEA8;--shiki-light:#098658">0</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">      const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> end</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">new</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">Position</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">        textEditor</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">document</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">lineCount</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> - </span><span style="--shiki-dark:#B5CEA8;--shiki-light:#098658">1</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">        textEditor</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">document</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">lineAt</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">textEditor</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">document</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">lineCount</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> - </span><span style="--shiki-dark:#B5CEA8;--shiki-light:#098658">1</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">).</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">text</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">length</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      );</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">      edit</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">delete</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">new</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">Range</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">start</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">end</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">));</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    });</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">    try</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">      // Stream the code into the editor as it is coming in from the Language Model</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">      for</span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB"> await</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> (</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> fragment</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> of</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> chatResponse</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">text</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">        await</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> textEditor</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">edit</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">edit</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> =&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">          const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> lastLine</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">textEditor</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">document</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">lineAt</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">textEditor</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">document</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">lineCount</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> - </span><span style="--shiki-dark:#B5CEA8;--shiki-light:#098658">1</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">          const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> position</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">new</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">Position</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">lastLine</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">lineNumber</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">lastLine</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">text</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">length</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">          edit</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">insert</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">position</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">fragment</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">        });</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    } </span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">catch</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> (</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">err</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) {</span></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000">      // async response stream may fail, e.g network interruption or server side error</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">      await</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> textEditor</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">edit</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">edit</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> =&gt;</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">        const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> lastLine</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">textEditor</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">document</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">lineAt</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">textEditor</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">document</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">lineCount</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> - </span><span style="--shiki-dark:#B5CEA8;--shiki-light:#098658">1</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">        const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> position</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">new</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">Position</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">lastLine</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">lineNumber</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">lastLine</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">text</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">length</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">        edit</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">insert</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">position</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, (&lt;</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">Error</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">&gt;</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">err</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">).</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">message</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      });</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"></span></code></pre>
<h2 id="considerations" data-needslink="considerations">Considerations</h2>
<h3 id="model-availability" data-needslink="model-availability">Model availability</h3>
<p>We don't expect specific models to stay supported forever. When you reference a language model in your extension, make sure to take a "defensive" approach when sending requests to that language model. This means that you should gracefully handle cases where you don't have access to a particular model.</p>
<h3 id="choosing-the-appropriate-model" data-needslink="choosing-the-appropriate-model">Choosing the appropriate model</h3>
<p>Extension authors can choose which model is the most appropriate for their extension. We recommend using <code>gpt-4o</code> for its performance and quality. To get a full list of available models, you can use this code snippet:</p>
<pre class="shiki" data-lang="typescript" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> allModels</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">await</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">lm</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">selectChatModels</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1">MODEL_SELECTOR</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"></span></code></pre>
<div class="markdown-alert note" dir="auto">
      <span>
        <svg class="markdown-alert-icon" viewbox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8Zm8-6.5a6.5 6.5 0 1 0 0 13 6.5 6.5 0 0 0 0-13ZM6.5 7.75A.75.75 0 0 1 7.25 7h1a.75.75 0 0 1 .75.75v2.75h.25a.75.75 0 0 1 0 1.5h-2a.75.75 0 0 1 0-1.5h.25v-2h-.25a.75.75 0 0 1-.75-.75ZM8 6a1 1 0 1 1 0-2 1 1 0 0 1 0 2Z"></path></svg>
        Note
      </span><p>The recommended GPT-4o model has a limit of <code>64K</code> tokens. The returned model object from the <code>selectChatModels</code> call has a <code>maxInputTokens</code> attribute that shows the token limit. These limits will be expanded as we learn more about how extensions are using the language models.</p>
</div><h3 id="rate-limiting" data-needslink="rate-limiting">Rate limiting</h3>
<p>Extensions should responsibly use the language model and be aware of rate limiting. VS Code is transparent to the user regarding how extensions are using language models and how many requests each extension is sending and how that influences their respective quotas.</p>
<p>Extensions should not use the Language Model API for integration tests due to rate-limitations. Internally, VS Code uses a dedicated non-production language model for simulation testing, and we are currently thinking how to provide a scalable language model testing solution for extensions.</p>
<h2 id="testing-your-extension" data-needslink="testing-your-extension">Testing your extension</h2>
<p>The responses that the Language Model API provides are nondeterministic, which means that you might get a different response for an identical request. This behavior can be challenging for testing your extension.</p>
<p>The part of the extension for building prompts and interpreting language model responses is deterministic, and can thus be unit tested without using an actual language model. However, interacting and getting responses from the language model itself, is nondeterministic and can’t be easily tested. Consider designing your extension code in a modular way to enable you to unit test the specific parts that can be tested.</p>
<h2 id="publishing-your-extension" data-needslink="publishing-your-extension">Publishing your extension</h2>
<p>Once you have created your AI extension, you can publish your extension to the Visual Studio Marketplace:</p>
<ul><li>Before publishing to the VS Marketplace we recommend that you read the <a href="https://www.microsoft.com/en-us/ai/tools-practices" class="external-link" target="_blank">Microsoft AI tools and practices guidelines</a>. These guidelines provide best practices for the responsible development and use of AI technologies.</li>
<li>By publishing to the VS Marketplace, your extension is adhering to the <a href="https://docs.github.com/en/early-access/copilot/github-copilot-extensibility-platform-partnership-plugin-acceptable-development-and-use-policy" class="external-link" target="_blank">GitHub Copilot extensibility acceptable development and use policy</a>.</li>
<li>If your extension already contributes functionality other than using the Language Model API, we recommend that you do not introduce an extension dependency on GitHub Copilot in the <a href="/api/references/extension-manifest">extension manifest</a>. This ensures that extension users that do not use GitHub Copilot can use the non language model functionality without having to install GitHub Copilot. Make sure to have appropriate error handling when accessing language models for this case.</li>
<li>Upload to the Marketplace as described in <a href="https://code.visualstudio.com/api/working-with-extensions/publishing-extension">Publishing Extension</a>.</li>
</ul><h2 id="related-content" data-needslink="related-content">Related content</h2>
<ul><li><a href="/api/references/vscode-api#lm">Language Models API Reference</a></li>
<li><a href="https://www.npmjs.com/package/@vscode/prompt-tsx" class="external-link" target="_blank">Learn more about @vscode/prompt-tsx</a></li>
<li><a href="/api/extension-guides/ai/chat">Build a VS Code chat extension</a></li>
</ul><div class="feedback" data-edit-url="https://vscode.dev/github/microsoft/vscode-docs/blob/main/api/extension-guides/ai/language-model.md"></div>
				
				<div class="body-footer">6/3/2026</div>
				
            </main><aside class="docs-right-sidebar hidden-xs"><div class="docs-markdown-actions">
                    <div class="docs-markdown-dropdown" data-raw-url="/raw/api/extension-guides/ai/language-model.md">
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
                    <ul class="nav"><li><a href="#build-the-language-model-prompt">Build the language model prompt</a></li>
                        
                        <li><a href="#send-the-language-model-request">Send the language model request</a></li>
                        
                        <li><a href="#interpret-the-response">Interpret the response</a></li>
                        
                        <li><a href="#considerations">Considerations</a></li>
                        
                        <li><a href="#testing-your-extension">Testing your extension</a></li>
                        
                        <li><a href="#publishing-your-extension">Publishing your extension</a></li>
                        
                        <li><a href="#related-content">Related content</a></li>
                        
                    </ul></nav></aside></div>
		<div class="docs-mobile-widgets visible-xs">
			<div class="connect-widget"></div>
		</div>
	</div>
</div>
		</main>