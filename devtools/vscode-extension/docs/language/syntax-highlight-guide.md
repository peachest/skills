# Syntax Highlight Guide

> 源文档: [https://code.visualstudio.com/api/language-extensions/syntax-highlight-guide](https://code.visualstudio.com/api/language-extensions/syntax-highlight-guide)

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
			    
			<li class="panel active expanded">
			  <a class="area" role="button" href="#language-extensions-articles" data-parent="#main-nav" data-toggle="collapse">Language Extensions</a>
			  <ul id="language-extensions-articles" class="collapse in"><li>
			          <a href="/api/language-extensions/overview">Overview</a>
			        </li>
			          
			        <li class="active">
			          <a href="/api/language-extensions/syntax-highlight-guide" aria-label="Current Page: Syntax Highlight Guide">Syntax Highlight Guide</a>
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
				<select id="small-nav-dropdown" aria-label="topics"><option value="/api">Overview</option><optgroup label="Get Started"><option value="/api/get-started/your-first-extension">Your First Extension</option><option value="/api/get-started/extension-anatomy">Extension Anatomy</option><option value="/api/get-started/wrapping-up">Wrapping Up</option></optgroup><optgroup label="Extension Capabilities"><option value="/api/extension-capabilities/overview">Overview</option><option value="/api/extension-capabilities/common-capabilities">Common Capabilities</option><option value="/api/extension-capabilities/theming">Theming</option><option value="/api/extension-capabilities/extending-workbench">Extending Workbench</option></optgroup><optgroup label="Extension Guides"><option value="/api/extension-guides/overview">Overview</option><optgroup label="Extension Guides - AI"><option value="/api/extension-guides/ai/ai-extensibility-overview">AI Extensibility</option><option value="/api/extension-guides/ai/tools">Language Model Tool</option><option value="/api/extension-guides/ai/mcp">MCP Dev Guide</option><option value="/api/extension-guides/ai/chat">Chat Participant</option><option value="/api/extension-guides/ai/chat-tutorial">Chat Tutorial</option><option value="/api/extension-guides/ai/language-model">Language Model</option><option value="/api/extension-guides/ai/language-model-tutorial">Language Model Tutorial</option><option value="/api/extension-guides/ai/language-model-chat-provider">Language Model Chat Provider</option><option value="/api/extension-guides/ai/prompt-tsx">Prompt TSX</option></optgroup><option value="/api/extension-guides/command">Command</option><option value="/api/extension-guides/color-theme">Color Theme</option><option value="/api/extension-guides/file-icon-theme">File Icon Theme</option><option value="/api/extension-guides/product-icon-theme">Product Icon Theme</option><option value="/api/extension-guides/tree-view">Tree View</option><option value="/api/extension-guides/webview">Webview</option><option value="/api/extension-guides/notebook">Notebook</option><option value="/api/extension-guides/custom-editors">Custom Editors</option><option value="/api/extension-guides/virtual-documents">Virtual Documents</option><option value="/api/extension-guides/virtual-workspaces">Virtual Workspaces</option><option value="/api/extension-guides/web-extensions">Web Extensions</option><option value="/api/extension-guides/workspace-trust">Workspace Trust</option><option value="/api/extension-guides/task-provider">Task Provider</option><option value="/api/extension-guides/scm-provider">Source Control</option><option value="/api/extension-guides/debugger-extension">Debugger Extension</option><option value="/api/extension-guides/markdown-extension">Markdown Extension</option><option value="/api/extension-guides/testing">Test Extension</option><option value="/api/extension-guides/custom-data-extension">Custom Data Extension</option><option value="/api/extension-guides/telemetry">Telemetry</option></optgroup><optgroup label="UX Guidelines"><option value="/api/ux-guidelines/overview">Overview</option><option value="/api/ux-guidelines/activity-bar">Activity Bar</option><option value="/api/ux-guidelines/sidebars">Sidebars</option><option value="/api/ux-guidelines/panel">Panel</option><option value="/api/ux-guidelines/status-bar">Status Bar</option><option value="/api/ux-guidelines/views">Views</option><option value="/api/ux-guidelines/editor-actions">Editor Actions</option><option value="/api/ux-guidelines/quick-picks">Quick Picks</option><option value="/api/ux-guidelines/command-palette">Command Palette</option><option value="/api/ux-guidelines/notifications">Notifications</option><option value="/api/ux-guidelines/webviews">Webviews</option><option value="/api/ux-guidelines/context-menus">Context Menus</option><option value="/api/ux-guidelines/walkthroughs">Walkthroughs</option><option value="/api/ux-guidelines/settings">Settings</option></optgroup><optgroup label="Language Extensions"><option value="/api/language-extensions/overview">Overview</option><option value="/api/language-extensions/syntax-highlight-guide" selected>Syntax Highlight Guide</option><option value="/api/language-extensions/semantic-highlight-guide">Semantic Highlight Guide</option><option value="/api/language-extensions/snippet-guide">Snippet Guide</option><option value="/api/language-extensions/language-configuration-guide">Language Configuration Guide</option><option value="/api/language-extensions/programmatic-language-features">Programmatic Language Features</option><option value="/api/language-extensions/language-server-extension-guide">Language Server Extension Guide</option><option value="/api/language-extensions/embedded-languages">Embedded Languages</option></optgroup><optgroup label="Testing and Publishing"><option value="/api/working-with-extensions/testing-extension">Testing Extensions</option><option value="/api/working-with-extensions/publishing-extension">Publishing Extensions</option><option value="/api/working-with-extensions/bundling-extension">Bundling Extensions</option><option value="/api/working-with-extensions/continuous-integration">Continuous Integration</option></optgroup><optgroup label="Advanced Topics"><option value="/api/advanced-topics/extension-host">Extension Host</option><option value="/api/advanced-topics/remote-extensions">Remote Development and Codespaces</option><option value="/api/advanced-topics/using-proposed-api">Using Proposed API</option><option value="/api/advanced-topics/tslint-eslint-migration">Migrate from TSLint to ESLint</option><option value="/api/advanced-topics/python-extension-template">Python Extension Template</option></optgroup><optgroup label="References"><option value="/api/references/vscode-api">VS Code API</option><option value="/api/references/contribution-points">Contribution Points</option><option value="/api/references/activation-events">Activation Events</option><option value="/api/references/extension-manifest">Extension Manifest</option><option value="/api/references/commands">Built-In Commands</option><option value="/api/references/when-clause-contexts">When Clause Contexts</option><option value="/api/references/theme-color">Theme Color</option><option value="/api/references/icons-in-labels">Product Icon Reference</option><option value="/api/references/document-selector">Document Selector</option></optgroup></select></nav></aside><div class="docs-content-wrapper">
			
			<main class="docs-main-content body"><h1>Syntax Highlight Guide</h1>
<p>Syntax highlighting determines the color and style of source code displayed in the Visual Studio Code editor. It is responsible for colorizing keywords like <code>if</code> or <code>for</code> in JavaScript differently than strings and comments and variable names.</p>
<p>There are two components to syntax highlighting:</p>
<ul><li><a href="#_tokenization">Tokenization</a>: Breaking text into a list of tokens</li>
<li><a href="#_theming">Theming</a>: Using themes or user settings to map the tokens to specific colors and styles</li>
</ul><p>Before diving into the details, a good start is to play with the <a href="#_scope-inspector">scope inspector</a> tool and explore what tokens are present in a source file and what theme rules they match to. To see both semantic and syntax token, use a built-in theme (for example, Dark+) on a TypeScript file.</p>
<h2 id="tokenization" data-needslink="tokenization">Tokenization</h2>
<p>The tokenization of text is about breaking the text into segments and to classify each segment with a token type.</p>
<p>VS Code's tokenization engine is powered by <a href="https://macromates.com/manual/en/language_grammars" class="external-link" target="_blank">TextMate grammars</a>. TextMate grammars are a structured collection of regular expressions and are written as a plist (XML) or JSON files. VS Code extensions can contribute grammars through the <code>grammars</code> contribution point.</p>
<p>The TextMate tokenization engine runs in the same process as the renderer and tokens are updated as the user types. Tokens are used for syntax highlighting, but also to classify the source code into areas of comments, strings, regex.</p>
<p>Starting with release 1.43, VS Code also allows extensions to provide tokenization through a <a href="/api/references/vscode-api#DocumentSemanticTokensProvider">Semantic Token Provider</a>. Semantic providers are typically implemented by language servers that have a deeper understanding of the source file and can resolve symbols in the context of the project. For example, a constant variable name can be rendered using constant highlighting throughout the project, not just at the place of its declaration.</p>
<p>Highlighting based on semantic tokens is considered an addition to the TextMate-based syntax highlighting. Semantic highlighting goes on top of the syntax highlighting. And as language servers can take a while to load and analyze a project, semantic token highlighting may appear after a short delay.</p>
<p>This article focuses on the TextMate-based tokenization. Semantic tokenization and theming are explained in the <a href="semantic-highlight-guide">Semantic Highlighting guide</a>.</p>
<h3 id="textmate-grammars" data-needslink="textmate-grammars">TextMate grammars</h3>
<p>VS Code uses <a href="https://macromates.com/manual/en/language_grammars" class="external-link" target="_blank">TextMate grammars</a> as the syntax tokenization engine. Invented for the TextMate editor, they have been adopted by many other editors and IDEs due to large number of language bundles created and maintained by the Open Source community.</p>
<p>TextMate grammars rely on <a href="https://macromates.com/manual/en/regular_expressions" class="external-link" target="_blank">Oniguruma regular expressions</a> and are typically written as a plist or JSON. You can find a good introduction to TextMate grammars <a href="https://www.apeth.com/nonblog/stories/textmatebundle.html" class="external-link" target="_blank">here</a>, and you can take a look at existing TextMate grammars to learn more about how they work.</p>
<h3 id="textmate-tokens-and-scopes" data-needslink="textmate-tokens-and-scopes">TextMate tokens and scopes</h3>
<p>Tokens are one or more characters that are part of the same program element. Example tokens include operators such as <code>+</code> and <code>*</code>, variable names such as <code>myVar</code>, or strings such as <code>"my string"</code>.</p>
<p>Each token is associated with a scope that defines the context of the token. A scope is a dot separated list of identifiers that specify the context of the current token. The <code>+</code> operation in JavaScript, for example, has the scope <code>keyword.operator.arithmetic.js</code>.</p>
<p>Themes map scopes to colors and styles to provide syntax highlighting. TextMate provides <a href="https://macromates.com/manual/en/language_grammars" class="external-link" target="_blank">list of common scopes</a> that many themes target. In order to have your grammar as broadly supported as possible, try to build on existing scopes rather than defining new ones.</p>
<p>Scopes nest so that each token is also associated with a list of parent scopes. The example below uses the <a href="#_scope-inspector">scope inspector</a> to show the scope hierarchy for the <code>+</code> operator in a simple JavaScript function. The most specific scope is listed at the top, with more general parent scopes listed below:</p>
<p><img src="/assets/api/language-extensions/syntax-highlighting/scopes.png" alt="syntax highlighting scopes" loading="lazy"></p>
<p>Parent scope information is also used for theming. When a theme targets a scope, all tokens with that parent scope will be colorized unless the theme also provides a more specific colorization for their individual scopes.</p>
<h3 id="configure-bracket-matching-scopes" data-needslink="configure-bracket-matching-scopes">Configure bracket matching scopes</h3>
<p>Some languages include tokens that should not participate in bracket matching, even though they visually resemble brackets.</p>
<p>There are two properties for configuring bracket matching behavior:</p>
<ul><li><code>balancedBracketScopes</code>: defines which scopes participate in bracket matching. By default, all scopes are included.</li>
<li><code>unbalancedBracketScopes</code>: defines scopes that should be excluded from bracket matching.</li>
</ul><pre class="shiki" data-lang="json" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">{</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "unbalancedBracketScopes"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"meta.scope.case-pattern.shell"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">]</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<h3 id="contributing-a-basic-grammar" data-needslink="contributing-a-basic-grammar">Contributing a basic grammar</h3>
<p>VS Code supports json TextMate grammars. These are contributed through the <code>grammars</code> <a href="/api/references/contribution-points">contribution point</a>.</p>
<p>Each grammar contribution specifies: the identifier of the language the grammar applies to, the top-level scope name for the tokens of the grammar, and the relative path to a grammar file. The example below shows a grammar contribution for a fictional <code>abc</code> language:</p>
<pre class="shiki" data-lang="json" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">{</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "contributes"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "languages"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">        "id"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"abc"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">        "extensions"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">".abc"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">]</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    ],</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "grammars"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">        "language"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"abc"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">        "scopeName"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"source.abc"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">        "path"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"./syntaxes/abc.tmGrammar.json"</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    ]</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<p>The grammar file itself consists of a top-level rule. This is typically split into a <code>patterns</code> section that lists the top-level elements of the program and a <code>repository</code> that defines each of the elements. Other rules in the grammar can reference elements from the <code>repository</code> using <code>{ "include": "#id" }</code>.</p>
<p>The example <code>abc</code> grammar marks the letters <code>a</code>, <code>b</code>, and <code>c</code> as keywords, and nestings of parens as expressions.</p>
<pre class="shiki" data-lang="json" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">{</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "scopeName"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"source.abc"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "patterns"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [{ </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">"include"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"#expression"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> }],</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "repository"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "expression"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">      "patterns"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [{ </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">"include"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"#letter"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> }, { </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">"include"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"#paren-expression"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> }]</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    },</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "letter"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">      "match"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"a|b|c"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">      "name"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"keyword.letter"</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    },</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "paren-expression"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">      "begin"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">("</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">      "end"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"</span><span style="--shiki-dark:#D7BA7D;--shiki-light:#EE0000">\\</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">)"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">      "beginCaptures"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">        "0"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: { </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">"name"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"punctuation.paren.open"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      },</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">      "endCaptures"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">        "0"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: { </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">"name"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"punctuation.paren.close"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      },</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">      "name"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"expression.group"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">      "patterns"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [{ </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">"include"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"#expression"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> }]</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<p>The grammar engine will try to successively apply the <code>expression</code> rule to all text in the document. For a simple program such as:</p>
<pre class="shiki" data-lang="text" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span>a</span></span>
<span class="line"><span>(</span></span>
<span class="line"><span>    b</span></span>
<span class="line"><span>)</span></span>
<span class="line"><span>x</span></span>
<span class="line"><span>(</span></span>
<span class="line"><span>    (</span></span>
<span class="line"><span>        c</span></span>
<span class="line"><span>        xyz</span></span>
<span class="line"><span>    )</span></span>
<span class="line"><span>)</span></span>
<span class="line"><span>(</span></span>
<span class="line"><span>a</span></span>
<span class="line"><span></span></span></code></pre>
<p>The example grammar produces the following scopes (listed left-to-right from most specific to least specific scope):</p>
<pre class="shiki" data-lang="text" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span>a               keyword.letter, source.abc</span></span>
<span class="line"><span>(               punctuation.paren.open, expression.group, source.abc</span></span>
<span class="line"><span>    b           keyword.letter, expression.group, source.abc</span></span>
<span class="line"><span>)               punctuation.paren.close, expression.group, source.abc</span></span>
<span class="line"><span>x               source.abc</span></span>
<span class="line"><span>(               punctuation.paren.open, expression.group, source.abc</span></span>
<span class="line"><span>    (           punctuation.paren.open, expression.group, expression.group, source.abc</span></span>
<span class="line"><span>        c       keyword.letter, expression.group, expression.group, source.abc</span></span>
<span class="line"><span>        xyz     expression.group, expression.group, source.abc</span></span>
<span class="line"><span>    )           punctuation.paren.close, expression.group, expression.group, source.abc</span></span>
<span class="line"><span>)               punctuation.paren.close, expression.group, source.abc</span></span>
<span class="line"><span>(               punctuation.paren.open, expression.group, source.abc</span></span>
<span class="line"><span>a               keyword.letter, expression.group, source.abc</span></span>
<span class="line"><span></span></span></code></pre>
<p>Note that text that is not matched by one of the rules, such as the string <code>xyz</code>, is included in the current scope. The last parenthesis at the end of the file is part of the <code>expression.group</code> even if the <code>end</code> rule is not matched, as <code>end-of-document</code> was found before the <code>end</code> rule was.</p>
<h3 id="embedded-languages" data-needslink="embedded-languages">Embedded languages</h3>
<p>If your grammar includes embedded languages within the parent language, such as CSS style blocks in HTML, you can use the <code>embeddedLanguages</code> contribution point to tell VS Code to treat the embedded language as distinct from the parent language. This ensures that bracket matching, commenting, and other basic language features work as expected in the embedded language.</p>
<p>The <code>embeddedLanguages</code> contribution point maps a scope in the embedded language to a top-level language scope. In the example below, any tokens in the <code>meta.embedded.block.javascript</code> scope will be treated as JavaScript content:</p>
<pre class="shiki" data-lang="json" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">{</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "contributes"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "grammars"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">        "path"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"./syntaxes/abc.tmLanguage.json"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">        "scopeName"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"source.abc"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">        "embeddedLanguages"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">          "meta.embedded.block.javascript"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"javascript"</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">        }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    ]</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<p>Now if you try to comment code or trigger snippets inside a set of tokens marked <code>meta.embedded.block.javascript</code>, they will get the correct <code>//</code> JavaScript style comment and the correct JavaScript snippets.</p>
<h3 id="developing-a-new-grammar-extension" data-needslink="developing-a-new-grammar-extension">Developing a new grammar extension</h3>
<p>To quickly create a new grammar extension, use <a href="/api/get-started/your-first-extension">VS Code's Yeoman templates</a> to run <code>yo code</code> and select the <code>New Language</code> option:</p>
<p><img src="/assets/api/language-extensions/syntax-highlighting/yo-new-language.png" alt="Selecting the 'new language' template in 'yo code'" loading="lazy"></p>
<p>Yeoman will walk you through some basic questions to scaffold the new extension. The important questions for creating a new grammar are:</p>
<ul><li><code>Language id</code> - A unique identifier for your language.</li>
<li><code>Language name</code> - A human readable name for your language.</li>
<li><code>Scope names</code> - Root TextMate scope name for your grammar.</li>
</ul><p><img src="/assets/api/language-extensions/syntax-highlighting/yo-new-language-questions.png" alt="Filling in the 'new language' questions" loading="lazy"></p>
<p>The generator assumes that you want to define both a new language and a new grammar for that language. If you are creating a grammar for an existing language, just fill these in with your target language's information and be sure to delete the <code>languages</code> contribution point in the generated <code>package.json</code>.</p>
<p>After answering all the questions, Yeoman will create a new extension with the structure:</p>
<p><img src="/assets/api/language-extensions/syntax-highlighting/generated-new-language-extension.png" alt="A new language extension" loading="lazy"></p>
<p>Remember, if you are contributing a grammar to a language that VS Code already knows about, be sure to delete the <code>languages</code> contribution point in the generated <code>package.json</code>.</p>
<h4>Converting an existing TextMate grammar</h4>
<p><code>yo code</code> can also help convert an existing TextMate grammar to a VS Code extension. Again, start by running <code>yo code</code> and selecting <code>Language extension</code>. When asked for an existing grammar file, give it the full path to either a <code>.tmLanguage</code> or <code>.json</code> TextMate grammar file:</p>
<p><img src="/assets/api/language-extensions/syntax-highlighting/yo-convert.png" alt="Converting an existing TextMate grammar" loading="lazy"></p>
<h4>Using YAML to write a grammar</h4>
<p>As a grammar grows more complex, it can become difficult to understand and maintain it as json. If you find yourself writing complex regular expressions or needing to add comments to explain aspects of the grammar, consider using yaml to define your grammar instead.</p>
<p>Yaml grammars have the exact same structure as a json based grammar but allow you to use yaml's more concise syntax, along with features such as multi-line strings and comments.</p>
<p><img src="/assets/api/language-extensions/syntax-highlighting/yaml-grammar.png" alt="A yaml grammar using multiline strings and comments" loading="lazy"></p>
<p>VS Code can only load json grammars, so yaml based grammars must be converted to json. The <a href="https://www.npmjs.com/package/js-yaml" class="external-link" target="_blank"><code>js-yaml</code> package</a> and command-line tool makes this easy.</p>
<pre class="shiki" data-lang="bash" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000"># Install js-yaml as a development only dependency in your extension</span></span>
<span class="line"><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">$</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> npm</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> install</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> js-yaml</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> --save-dev</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#6A9955;--shiki-light:#008000"># Use the command-line tool to convert the yaml grammar to json</span></span>
<span class="line"><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">$</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> npx</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> js-yaml</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> syntaxes/abc.tmLanguage.yaml</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> &gt; </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">syntaxes/abc.tmLanguage.json</span></span>
<span class="line"></span></code></pre>
<h3 id="injection-grammars" data-needslink="injection-grammars">Injection grammars</h3>
<p>Injection grammars let you extend an existing grammar. An injection grammar is a regular TextMate grammar that is injected into a specific scope within an existing grammar. Example applications of injection grammars:</p>
<ul><li>Highlighting keywords such as <code>TODO</code> in comments.</li>
<li>Add more specific scope information to an existing grammar.</li>
<li>Adding highlighting for a new language to Markdown fenced code blocks.</li>
</ul><h4>Creating a basic injection grammar</h4>
<p>Injection grammars are contributed though the <code>package.json</code> just like regular grammars. However, instead of specifying a <code>language</code>, an injection grammar uses <code>injectTo</code> to specify a list of target language scopes to inject the grammar into.</p>
<p>For this example, we'll create a simple injection grammar that highlights <code>TODO</code> as a keyword in JavaScript comments. To apply our injection grammar in JavaScript files, we use the <code>source.js</code> target language scope in <code>injectTo</code>:</p>
<pre class="shiki" data-lang="json" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">{</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "contributes"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "grammars"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">        "path"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"./syntaxes/injection.json"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">        "scopeName"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"todo-comment.injection"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">        "injectTo"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"source.js"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">]</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    ]</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<p>The grammar itself is a standard TextMate grammar except for the top level <code>injectionSelector</code> entry. The <code>injectionSelector</code> is a scope selector that specifies which scopes the injected grammar should be applied in. For our example, we want to highlight the word <code>TODO</code> in all <code>//</code> comments. Using the <a href="#_scope-inspector">scope inspector</a>, we find that JavaScript's double slash comments have the scope <code>comment.line.double-slash</code>, so our injection selector is <code>L:comment.line.double-slash</code>:</p>
<pre class="shiki" data-lang="json" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">{</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "scopeName"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"todo-comment.injection"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "injectionSelector"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"L:comment.line.double-slash"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "patterns"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">      "include"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"#todo-keyword"</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  ],</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "repository"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "todo-keyword"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">      "match"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"TODO"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">      "name"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"keyword.todo"</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<p>The <code>L:</code> in the injection selector means that the injection is added to the left of existing grammar rules. This basically means that our injected grammar's rules will be applied before any existing grammar rules.</p>
<h4>Embedded languages</h4>
<p>Injection grammars can also contribute embedded languages to their parent grammar. Just like with a normal grammar, an injection grammar can use <code>embeddedLanguages</code> to map scopes from the embedded language to a top-level language scope.</p>
<p>An extension that highlights SQL queries in JavaScript strings, for example, may use <code>embeddedLanguages</code> to make sure all token inside the string marked <code>meta.embedded.inline.sql</code> are treated as SQL for basic language features such as bracket matching and snippet selection.</p>
<pre class="shiki" data-lang="json" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">{</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "contributes"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "grammars"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">        "path"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"./syntaxes/injection.json"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">        "scopeName"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"sql-string.injection"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">        "injectTo"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"source.js"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">],</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">        "embeddedLanguages"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">          "meta.embedded.inline.sql"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"sql"</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">        }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    ]</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<h4>Token types and embedded languages</h4>
<p>There is one additional complication for injection languages embedded languages: by default, VS Code treats all tokens within a string as string contents and all tokens with a comment as token content. Since features such as bracket matching and auto closing pairs are disabled inside of strings and comments, if the embedded language appears inside a string or comment, these features will also be disabled in the embedded language.</p>
<p>To override this behavior, you can use a <code>meta.embedded.*</code> scope to reset VS Code's marking of tokens as string or comment content. It is a good idea to always wrap embedded language in a <code>meta.embedded.*</code> scope to make sure VS Code treats the embedded language properly.</p>
<p>If you can't add a <code>meta.embedded.*</code> scope to your grammar, you can alternatively use <code>tokenTypes</code> in the grammar's contribution point to map specific scopes to content mode. The <code>tokenTypes</code> section below ensures that any content in the <code>my.sql.template.string</code> scope is treated as source code:</p>
<pre class="shiki" data-lang="json" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">{</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "contributes"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">    "grammars"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">        "path"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"./syntaxes/injection.json"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">        "scopeName"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"sql-string.injection"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">        "injectTo"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"source.js"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">],</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">        "embeddedLanguages"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">          "my.sql.template.string"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"sql"</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">        },</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">        "tokenTypes"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">          "my.sql.template.string"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"other"</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">        }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    ]</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<h2 id="theming" data-needslink="theming">Theming</h2>
<p>Theming is about assigning colors and styles to tokens. Theming rules are specified in color themes, but users can customize the theming rules in the user settings.</p>
<p>TextMate theme rules are defined in <code>tokenColors</code> and have the same syntax as regular TextMate themes. Each rule defines a TextMate scope selector and a resulting color and style.</p>
<p>When evaluating the color and style of a token, the current token's scope is matched against the rule's selector to find the most specific rule for each style property (foreground, bold, italic, underline)</p>
<p>The <a href="/api/extension-guides/color-theme#syntax-colors">Color Theme guide</a> describes how to create a color theme. Theming for semantic tokens is explained in the <a href="semantic-highlight-guide#theming">Semantic Highlighting guide</a>.</p>
<h2 id="scope-inspector" data-needslink="scope-inspector">Scope inspector</h2>
<p>VS Code's built-in scope inspector tool helps debug grammars and semantic tokens. It displays the scopes for the token and the semantic tokens at the current position in a file, along with metadata about which theme rules apply to that token.</p>
<p>Trigger the scope inspector from the Command Palette with the <code>Developer: Inspect Editor Tokens and Scopes</code> command or <a href="/docs/getstarted/keybindings">create a keybinding</a> for it:</p>
<pre class="shiki" data-lang="json" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">{</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "key"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"cmd+alt+shift+i"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "command"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"editor.action.inspectTMScopes"</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<p><img src="/assets/api/language-extensions/syntax-highlighting/scope-inspector.png" alt="scope inspector" loading="lazy"></p>
<p>The scope inspector displays the following information:</p>
<ol><li>The current token.</li>
<li>Metadata about the token and information about its computed appearance. If you are working with embedded languages, the important entries here <code>language</code> and <code>token type</code>.</li>
<li>The semantic token section is shown when a semantic token provider is available for the current language and when the current theme supports semantic highlighting. It shows the current semantic token type and modifiers along with the theme rules that match the semantic token type and modifiers.</li>
<li>The TextMate section shows the scope list for the current TextMate token, with the most specific scope at the top. It also shows the most specific theme rules that match the scopes. This only shows the theme rules that are responsible for the token's current style, it does not show overridden rules. If semantic tokens are present, the theme rules are only shown when they differ from the rule matching the semantic token.</li>
</ol><div class="feedback" data-edit-url="https://vscode.dev/github/microsoft/vscode-docs/blob/main/api/language-extensions/syntax-highlight-guide.md"></div>
				
				<div class="body-footer">6/3/2026</div>
				
            </main><aside class="docs-right-sidebar hidden-xs"><div class="docs-markdown-actions">
                    <div class="docs-markdown-dropdown" data-raw-url="/raw/api/language-extensions/syntax-highlight-guide.md">
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
                    <ul class="nav"><li><a href="#tokenization">Tokenization</a></li>
                        
                        <li><a href="#theming">Theming</a></li>
                        
                        <li><a href="#scope-inspector">Scope inspector</a></li>
                        
                    </ul></nav></aside></div>
		<div class="docs-mobile-widgets visible-xs">
			<div class="connect-widget"></div>
		</div>
	</div>
</div>
		</main>