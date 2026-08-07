# Source Control API

> 源文档: [https://code.visualstudio.com/api/extension-guides/scm-provider](https://code.visualstudio.com/api/extension-guides/scm-provider)

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
			          
			        <li>
			          <a href="/api/extension-guides/workspace-trust">Workspace Trust</a>
			        </li>
			          
			        <li>
			          <a href="/api/extension-guides/task-provider">Task Provider</a>
			        </li>
			          
			        <li class="active">
			          <a href="/api/extension-guides/scm-provider" aria-label="Current Page: Source Control">Source Control</a>
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
				<select id="small-nav-dropdown" aria-label="topics"><option value="/api">Overview</option><optgroup label="Get Started"><option value="/api/get-started/your-first-extension">Your First Extension</option><option value="/api/get-started/extension-anatomy">Extension Anatomy</option><option value="/api/get-started/wrapping-up">Wrapping Up</option></optgroup><optgroup label="Extension Capabilities"><option value="/api/extension-capabilities/overview">Overview</option><option value="/api/extension-capabilities/common-capabilities">Common Capabilities</option><option value="/api/extension-capabilities/theming">Theming</option><option value="/api/extension-capabilities/extending-workbench">Extending Workbench</option></optgroup><optgroup label="Extension Guides"><option value="/api/extension-guides/overview">Overview</option><optgroup label="Extension Guides - AI"><option value="/api/extension-guides/ai/ai-extensibility-overview">AI Extensibility</option><option value="/api/extension-guides/ai/tools">Language Model Tool</option><option value="/api/extension-guides/ai/mcp">MCP Dev Guide</option><option value="/api/extension-guides/ai/chat">Chat Participant</option><option value="/api/extension-guides/ai/chat-tutorial">Chat Tutorial</option><option value="/api/extension-guides/ai/language-model">Language Model</option><option value="/api/extension-guides/ai/language-model-tutorial">Language Model Tutorial</option><option value="/api/extension-guides/ai/language-model-chat-provider">Language Model Chat Provider</option><option value="/api/extension-guides/ai/prompt-tsx">Prompt TSX</option></optgroup><option value="/api/extension-guides/command">Command</option><option value="/api/extension-guides/color-theme">Color Theme</option><option value="/api/extension-guides/file-icon-theme">File Icon Theme</option><option value="/api/extension-guides/product-icon-theme">Product Icon Theme</option><option value="/api/extension-guides/tree-view">Tree View</option><option value="/api/extension-guides/webview">Webview</option><option value="/api/extension-guides/notebook">Notebook</option><option value="/api/extension-guides/custom-editors">Custom Editors</option><option value="/api/extension-guides/virtual-documents">Virtual Documents</option><option value="/api/extension-guides/virtual-workspaces">Virtual Workspaces</option><option value="/api/extension-guides/web-extensions">Web Extensions</option><option value="/api/extension-guides/workspace-trust">Workspace Trust</option><option value="/api/extension-guides/task-provider">Task Provider</option><option value="/api/extension-guides/scm-provider" selected>Source Control</option><option value="/api/extension-guides/debugger-extension">Debugger Extension</option><option value="/api/extension-guides/markdown-extension">Markdown Extension</option><option value="/api/extension-guides/testing">Test Extension</option><option value="/api/extension-guides/custom-data-extension">Custom Data Extension</option><option value="/api/extension-guides/telemetry">Telemetry</option></optgroup><optgroup label="UX Guidelines"><option value="/api/ux-guidelines/overview">Overview</option><option value="/api/ux-guidelines/activity-bar">Activity Bar</option><option value="/api/ux-guidelines/sidebars">Sidebars</option><option value="/api/ux-guidelines/panel">Panel</option><option value="/api/ux-guidelines/status-bar">Status Bar</option><option value="/api/ux-guidelines/views">Views</option><option value="/api/ux-guidelines/editor-actions">Editor Actions</option><option value="/api/ux-guidelines/quick-picks">Quick Picks</option><option value="/api/ux-guidelines/command-palette">Command Palette</option><option value="/api/ux-guidelines/notifications">Notifications</option><option value="/api/ux-guidelines/webviews">Webviews</option><option value="/api/ux-guidelines/context-menus">Context Menus</option><option value="/api/ux-guidelines/walkthroughs">Walkthroughs</option><option value="/api/ux-guidelines/settings">Settings</option></optgroup><optgroup label="Language Extensions"><option value="/api/language-extensions/overview">Overview</option><option value="/api/language-extensions/syntax-highlight-guide">Syntax Highlight Guide</option><option value="/api/language-extensions/semantic-highlight-guide">Semantic Highlight Guide</option><option value="/api/language-extensions/snippet-guide">Snippet Guide</option><option value="/api/language-extensions/language-configuration-guide">Language Configuration Guide</option><option value="/api/language-extensions/programmatic-language-features">Programmatic Language Features</option><option value="/api/language-extensions/language-server-extension-guide">Language Server Extension Guide</option><option value="/api/language-extensions/embedded-languages">Embedded Languages</option></optgroup><optgroup label="Testing and Publishing"><option value="/api/working-with-extensions/testing-extension">Testing Extensions</option><option value="/api/working-with-extensions/publishing-extension">Publishing Extensions</option><option value="/api/working-with-extensions/bundling-extension">Bundling Extensions</option><option value="/api/working-with-extensions/continuous-integration">Continuous Integration</option></optgroup><optgroup label="Advanced Topics"><option value="/api/advanced-topics/extension-host">Extension Host</option><option value="/api/advanced-topics/remote-extensions">Remote Development and Codespaces</option><option value="/api/advanced-topics/using-proposed-api">Using Proposed API</option><option value="/api/advanced-topics/tslint-eslint-migration">Migrate from TSLint to ESLint</option><option value="/api/advanced-topics/python-extension-template">Python Extension Template</option></optgroup><optgroup label="References"><option value="/api/references/vscode-api">VS Code API</option><option value="/api/references/contribution-points">Contribution Points</option><option value="/api/references/activation-events">Activation Events</option><option value="/api/references/extension-manifest">Extension Manifest</option><option value="/api/references/commands">Built-In Commands</option><option value="/api/references/when-clause-contexts">When Clause Contexts</option><option value="/api/references/theme-color">Theme Color</option><option value="/api/references/icons-in-labels">Product Icon Reference</option><option value="/api/references/document-selector">Document Selector</option></optgroup></select></nav></aside><div class="docs-content-wrapper">
			
			<main class="docs-main-content body"><h1>Source Control API</h1>
<p>The Source Control API allows extension authors to define Source Control Management (SCM) features. There is a slim, yet powerful API surface which allows many different SCM systems to be integrated in Visual Studio Code, while having a common user interface with all of them.</p>
<p><img src="/assets/api/extension-guides/scm-provider/main.png" alt="VS Code SCM" loading="lazy"></p>
<p>VS Code itself ships with one Source Control provider, the Git extension, which is the best reference for this API and is <a href="https://github.com/microsoft/vscode/blob/main/extensions/git/src/repository.ts" class="external-link" target="_blank">a great starting point</a> if you'd like to contribute your very own SCM provider. There are other great examples in the Marketplace such as the <a href="https://marketplace.visualstudio.com/items?itemName=johnstoncode.svn-scm" class="external-link" target="_blank">SVN extension</a>.</p>
<p>This documentation will help you build an extension which can make any SCM system work with VS Code.</p>
<blockquote><p><strong>Note:</strong> that you can always refer to the <a href="/api/references/vscode-api#scm"><code>vscode</code> namespace API reference</a> in our documentation.</p>
</blockquote><h2 id="source-control-model" data-needslink="source-control-model">Source Control Model</h2>
<p>A <code>SourceControl</code> is the entity responsible for populating the Source Control model with <strong>resource states</strong>, instances of <code>SourceControlResourceState</code>. Resource states are themselves organized in <strong>groups</strong>, instances of <code>SourceControlResourceGroup</code>.</p>
<p>You can create a new SourceControl with <code>vscode.scm.createSourceControl</code>.</p>
<p>In order to better understand how these three entities correlate with each other, let's take <a href="https://github.com/microsoft/vscode/tree/main/extensions/git" class="external-link" target="_blank">Git</a> as an example. Consider the following output of <code>git status</code>:</p>
<pre class="shiki" data-lang="bash" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">vsce</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> main</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">*</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> →</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> git</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> status</span></span>
<span class="line"><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">On</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> branch</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> main</span></span>
<span class="line"><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">Your</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> branch</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> is</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> up-to-date</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> with</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> 'origin/main'.</span></span>
<span class="line"><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">Changes</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> to</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> be</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> committed:</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  (</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">use</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> "git reset HEAD &lt;file&gt;..."</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> to</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> unstage</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">)</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">        modified:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">   README.md</span></span>
<span class="line"><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">        renamed:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">    src/api.ts</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> -&gt; </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">src/test/api.ts</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">Changes</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> not</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> staged</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> for</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> commit:</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  (</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">use</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> "git add/rm &lt;file&gt;..."</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> to</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> update</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> what</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> will</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> be</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> committed</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">)</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  (</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">use</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> "git checkout -- &lt;file&gt;..."</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> to</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> discard</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> changes</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> in</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> working</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515"> directory</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">)</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">        deleted:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">    .travis.yml</span></span>
<span class="line"><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">        modified:</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">   README.md</span></span>
<span class="line"></span></code></pre>
<p>There are many things going on in this workspace. First, the <code>README.md</code> file has been modified, staged and then modified once again. Second, the <code>src/api.ts</code> file has been moved to <code>src/test/api.ts</code> and that move was staged. Finally, the <code>.travis.yml</code> file has been deleted.</p>
<p>For this workspace, Git defines two resource groups: the <strong>working tree</strong> and the <strong>index</strong>. Each <strong>file change</strong> within that group is <strong>resource state</strong>:</p>
<ul><li><strong>Index</strong> - resource group
<ul><li><code>README.md</code>, modified - resource state</li>
<li><code>src/test/api.ts</code>, renamed from <code>src/api.ts</code> - resource state</li>
</ul></li>
<li><strong>Working Tree</strong> - resource group
<ul><li><code>.travis.yml</code>, deleted - resource state</li>
<li><code>README.md</code>, modified - resource state</li>
</ul></li>
</ul><p>Note how the same file, <code>README.md</code>, is part of two distinct resource states.</p>
<p>Here's how Git creates this model:</p>
<pre class="shiki" data-lang="ts" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">function</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> createResourceUri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">relativePath</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">string</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">): </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">Uri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">  const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> absolutePath</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">path</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">join</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">workspace</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">rootPath</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">relativePath</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">  return</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">Uri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">file</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">absolutePath</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> gitSCM</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">scm</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">createSourceControl</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'git'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'Git'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> index</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">gitSCM</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">createResourceGroup</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'index'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'Index'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">index</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">resourceStates</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = [</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  { </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">resourceUri:</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> createResourceUri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'README.md'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) },</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  { </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">resourceUri:</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> createResourceUri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'src/test/api.ts'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">];</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> workingTree</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">gitSCM</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">createResourceGroup</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'workingTree'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'Changes'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">workingTree</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">resourceStates</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = [</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  { </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">resourceUri:</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> createResourceUri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'.travis.yml'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) },</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  { </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">resourceUri:</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> createResourceUri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'README.md'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">) }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">];</span></span>
<span class="line"></span></code></pre>
<p>Changes made to the source control and resource groups will be propagated to the Source Control view.</p>
<h2 id="source-control-view" data-needslink="source-control-view">Source Control View</h2>
<p>VS Code is able to populate the Source Control view, as the Source Control model changes. Resource states are customizable using <code>SourceControlResourceDecorations</code>:</p>
<pre class="shiki" data-lang="ts" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">export</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> interface</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99"> SourceControlResourceState</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">  readonly</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> decorations</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">?: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">SourceControlResourceDecorations</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<p>The previous example would be sufficient to populate a simple list in the Source Control view, but there are many user interactions that the user might want to perform with each resource. For instance, what happens when the user clicks a resource state? The resource state can optionally provide a command to handle this action:</p>
<pre class="shiki" data-lang="ts" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">export</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> interface</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99"> SourceControlResourceState</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">  readonly</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> command</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">?: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">Command</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<h3 id="menus" data-needslink="menus">Menus</h3>
<p>There are six Source Control menu ids where you can place menu items, in order to provide the user with a much richer user interface.</p>
<p>The <code>scm/title</code> menu is located to the right of the SCM view title. The menu items in the <code>navigation</code> group will be inline, while all the others will be within the <code>…</code> dropdown menu.</p>
<p>These three are similar:</p>
<ul><li><code>scm/resourceGroup/context</code> adds commands to <a href="/api/references/contribution-points#contributes.menus"><code>SourceControlResourceGroup</code></a> items.</li>
<li><code>scm/resourceState/context</code> adds commands to <a href="/api/references/contribution-points#contributes.menus"><code>SourceControlResourceState</code></a> items.</li>
<li><code>scm/resourceFolder/context</code> add commands to the intermediate folders that appear when a <a href="/api/references/contribution-points#contributes.menus"><code>SourceControlResourceState</code></a>'s resourceUri path includes folders and the user has opted for tree-view rather than list-view mode.</li>
</ul><p>Place menu items in the <code>inline</code> group to have them inline. All other menu item groups will be represented in a context menu usually accessible using the mouse right-click.</p>
<p>Note that the SCM view supports multiple selection, so a command receives as its argument an array of one or more resources.</p>
<p>For example, Git supports staging multiple files by adding the <code>git.stage</code> command to the <code>scm/resourceState/context</code> menu and using such a method declaration:</p>
<pre class="shiki" data-lang="ts" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">stage</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(...</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">resourceStates</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">SourceControlResourceState</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">[]): </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">Promise</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">&lt;</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">void</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">&gt;;</span></span>
<span class="line"></span></code></pre>
<p>When creating them, <code>SourceControl</code> and <code>SourceControlResourceGroup</code> instances require you to provide an <code>id</code> string. These values will be populated in the <code>scmProvider</code> and <code>scmResourceGroup</code> context keys, respectively. You can rely on these <a href="/api/references/when-clause-contexts">context keys</a> in the <code>when</code> clauses of your menu items. Here's how Git is able to show an inline menu item for its <code>git.stage</code> command:</p>
<pre class="shiki" data-lang="json" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">{</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "command"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"git.stage"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "when"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"scmProvider == git &amp;&amp; scmResourceGroup == merge"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "group"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"inline"</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<p>The <code>scm/repository</code> menu is the menu on each <code>SourceControl</code> instance in the <strong>Source Control Repositories</strong> view. Place menu items in the <code>inline</code> group to have them appear inline. All other menu item groups will be shown in the <code>...</code> menu. The <code>inline</code> group is rendered given the available space and menu items that do not fit are automatically moved into the <code>...</code> menu.</p>
<p>The <code>scm/sourceControl</code> menu is the context menu on each <code>SourceControl</code> instance in the <strong>Source Control Repositories</strong> view:</p>
<p><img src="/assets/api/extension-guides/scm-provider/sourcecontrol-menu.png" alt="source control menu" loading="lazy"></p>
<p>The <code>scm/change/title</code> allows you to contribute commands to the title bar of the <a href="/api/references/vscode-api#QuickDiffProvider">Quick Diff</a> inline diff editor, described <a href="#_quick-diff">further ahead</a>. The command will be passed as arguments the URI of the document, the array of changes within it, and the index of the change which the inline change diff editor is currently focused on. For example, here's the declaration of the <code>stageChange</code> Git command which is contributed to this menu with a <code>when</code> clause testing that the <code>originalResourceScheme</code> <a href="/api/references/when-clause-contexts">context key</a> equals <code>git</code>:</p>
<pre class="shiki" data-lang="ts" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">async</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26"> stageChange</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">uri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">Uri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">changes</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">LineChange</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">[], </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">index</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">number</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">): </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">Promise</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">&lt;</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">void</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">&gt;;</span></span>
<span class="line"></span></code></pre>
<h3 id="scm-input-box" data-needslink="scm-input-box">SCM Input Box</h3>
<p>The Source Control Input Box, located atop of each Source Control view, allows the user to input a message. You can get (and set) this message in order to perform operations. In Git, for example, this is used as the commit box, in which users type in commit messages and <code>git commit</code> commands pick them up.</p>
<pre class="shiki" data-lang="ts" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">export</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> interface</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99"> SourceControlInputBox</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  value</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">string</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span>
<span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">export</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> interface</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99"> SourceControl</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">  readonly</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> inputBox</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">SourceControlInputBox</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<p>The user can type <kbd>Ctrl+Enter</kbd> (or <kbd>Cmd+Enter</kbd> on macOS) to accept any message. You can handle this event by providing a <code>acceptInputCommand</code> to your <code>SourceControl</code> instance.</p>
<pre class="shiki" data-lang="ts" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">export</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> interface</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99"> SourceControl</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">  readonly</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080"> acceptInputCommand</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">?: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">Command</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<h2 id="quick-diff" data-needslink="quick-diff">Quick Diff</h2>
<p>VS Code also supports displaying <strong>quick diff</strong> editor gutter decorations. Clicking those decorations will reveal an inline diff experience, to which you can contribute contextual commands:</p>
<p><img src="/assets/api/extension-guides/scm-provider/quickdiff.png" alt="SCM quick diff" loading="lazy"></p>
<p>These decorations are computed by VS Code itself. All you need to do is provide VS Code with the original contents of any given file.</p>
<pre class="shiki" data-lang="ts" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#C586C0;--shiki-light:#AF00DB">export</span><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF"> interface</span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99"> SourceControl</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">  quickDiffProvider</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">?: </span><span style="--shiki-dark:#4EC9B0;--shiki-light:#267F99">QuickDiffProvider</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">;</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<p>Using a <code>QuickDiffProvider</code>'s <code>provideOriginalResource</code> method, your implementation is able to tell VS Code the <code>Uri</code> of the original resource that matches the resource whose <code>Uri</code> is provided as an argument to the method.</p>
<p>Combine this API with the <a href="/api/references/vscode-api#workspace"><code>registerTextDocumentContentProvider</code> method in the <code>workspace</code> namespace</a>, which lets you provide contents for arbitrary resources, given a <a href="/api/references/vscode-api#Uri"><code>Uri</code></a> matching the custom <code>scheme</code> that it registered for.</p>
<h2 id="next-steps" data-needslink="next-steps">Next steps</h2>
<p>To learn more about VS Code extensibility model, try these topics:</p>
<ul><li><a href="/api/references/vscode-api#scm">SCM API Reference</a> - Read the full SCM API documentation</li>
<li><a href="https://github.com/microsoft/vscode/tree/main/extensions/git" class="external-link" target="_blank">Git Extension</a> - Learn by reading the Git extension implementation</li>
<li><a href="/api">Extension API Overview</a> - Learn about the full VS Code extensibility model.</li>
<li><a href="/api/references/extension-manifest">Extension Manifest File</a> - VS Code package.json extension manifest file reference</li>
<li><a href="/api/references/contribution-points">Contribution Points</a> - VS Code contribution points reference</li>
</ul><div class="feedback" data-edit-url="https://vscode.dev/github/microsoft/vscode-docs/blob/main/api/extension-guides/scm-provider.md"></div>
				
				<div class="body-footer">6/3/2026</div>
				
            </main><aside class="docs-right-sidebar hidden-xs"><div class="docs-markdown-actions">
                    <div class="docs-markdown-dropdown" data-raw-url="/raw/api/extension-guides/scm-provider.md">
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
                <nav id="docs-subnavbar" aria-label="On Page"><h4><span class="sr-only">On this page there are 4 sections</span><span aria-hidden="true">On this page</span></h4>
                    <ul class="nav"><li><a href="#source-control-model">Source Control Model</a></li>
                        
                        <li><a href="#source-control-view">Source Control View</a></li>
                        
                        <li><a href="#quick-diff">Quick Diff</a></li>
                        
                        <li><a href="#next-steps">Next steps</a></li>
                        
                    </ul></nav></aside></div>
		<div class="docs-mobile-widgets visible-xs">
			<div class="connect-widget"></div>
		</div>
	</div>
</div>
		</main>