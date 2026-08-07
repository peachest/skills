# Custom Editor API

> 源文档: [https://code.visualstudio.com/api/extension-guides/custom-editors](https://code.visualstudio.com/api/extension-guides/custom-editors)

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
			          
			        <li class="active">
			          <a href="/api/extension-guides/custom-editors" aria-label="Current Page: Custom Editors">Custom Editors</a>
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
				<select id="small-nav-dropdown" aria-label="topics"><option value="/api">Overview</option><optgroup label="Get Started"><option value="/api/get-started/your-first-extension">Your First Extension</option><option value="/api/get-started/extension-anatomy">Extension Anatomy</option><option value="/api/get-started/wrapping-up">Wrapping Up</option></optgroup><optgroup label="Extension Capabilities"><option value="/api/extension-capabilities/overview">Overview</option><option value="/api/extension-capabilities/common-capabilities">Common Capabilities</option><option value="/api/extension-capabilities/theming">Theming</option><option value="/api/extension-capabilities/extending-workbench">Extending Workbench</option></optgroup><optgroup label="Extension Guides"><option value="/api/extension-guides/overview">Overview</option><optgroup label="Extension Guides - AI"><option value="/api/extension-guides/ai/ai-extensibility-overview">AI Extensibility</option><option value="/api/extension-guides/ai/tools">Language Model Tool</option><option value="/api/extension-guides/ai/mcp">MCP Dev Guide</option><option value="/api/extension-guides/ai/chat">Chat Participant</option><option value="/api/extension-guides/ai/chat-tutorial">Chat Tutorial</option><option value="/api/extension-guides/ai/language-model">Language Model</option><option value="/api/extension-guides/ai/language-model-tutorial">Language Model Tutorial</option><option value="/api/extension-guides/ai/language-model-chat-provider">Language Model Chat Provider</option><option value="/api/extension-guides/ai/prompt-tsx">Prompt TSX</option></optgroup><option value="/api/extension-guides/command">Command</option><option value="/api/extension-guides/color-theme">Color Theme</option><option value="/api/extension-guides/file-icon-theme">File Icon Theme</option><option value="/api/extension-guides/product-icon-theme">Product Icon Theme</option><option value="/api/extension-guides/tree-view">Tree View</option><option value="/api/extension-guides/webview">Webview</option><option value="/api/extension-guides/notebook">Notebook</option><option value="/api/extension-guides/custom-editors" selected>Custom Editors</option><option value="/api/extension-guides/virtual-documents">Virtual Documents</option><option value="/api/extension-guides/virtual-workspaces">Virtual Workspaces</option><option value="/api/extension-guides/web-extensions">Web Extensions</option><option value="/api/extension-guides/workspace-trust">Workspace Trust</option><option value="/api/extension-guides/task-provider">Task Provider</option><option value="/api/extension-guides/scm-provider">Source Control</option><option value="/api/extension-guides/debugger-extension">Debugger Extension</option><option value="/api/extension-guides/markdown-extension">Markdown Extension</option><option value="/api/extension-guides/testing">Test Extension</option><option value="/api/extension-guides/custom-data-extension">Custom Data Extension</option><option value="/api/extension-guides/telemetry">Telemetry</option></optgroup><optgroup label="UX Guidelines"><option value="/api/ux-guidelines/overview">Overview</option><option value="/api/ux-guidelines/activity-bar">Activity Bar</option><option value="/api/ux-guidelines/sidebars">Sidebars</option><option value="/api/ux-guidelines/panel">Panel</option><option value="/api/ux-guidelines/status-bar">Status Bar</option><option value="/api/ux-guidelines/views">Views</option><option value="/api/ux-guidelines/editor-actions">Editor Actions</option><option value="/api/ux-guidelines/quick-picks">Quick Picks</option><option value="/api/ux-guidelines/command-palette">Command Palette</option><option value="/api/ux-guidelines/notifications">Notifications</option><option value="/api/ux-guidelines/webviews">Webviews</option><option value="/api/ux-guidelines/context-menus">Context Menus</option><option value="/api/ux-guidelines/walkthroughs">Walkthroughs</option><option value="/api/ux-guidelines/settings">Settings</option></optgroup><optgroup label="Language Extensions"><option value="/api/language-extensions/overview">Overview</option><option value="/api/language-extensions/syntax-highlight-guide">Syntax Highlight Guide</option><option value="/api/language-extensions/semantic-highlight-guide">Semantic Highlight Guide</option><option value="/api/language-extensions/snippet-guide">Snippet Guide</option><option value="/api/language-extensions/language-configuration-guide">Language Configuration Guide</option><option value="/api/language-extensions/programmatic-language-features">Programmatic Language Features</option><option value="/api/language-extensions/language-server-extension-guide">Language Server Extension Guide</option><option value="/api/language-extensions/embedded-languages">Embedded Languages</option></optgroup><optgroup label="Testing and Publishing"><option value="/api/working-with-extensions/testing-extension">Testing Extensions</option><option value="/api/working-with-extensions/publishing-extension">Publishing Extensions</option><option value="/api/working-with-extensions/bundling-extension">Bundling Extensions</option><option value="/api/working-with-extensions/continuous-integration">Continuous Integration</option></optgroup><optgroup label="Advanced Topics"><option value="/api/advanced-topics/extension-host">Extension Host</option><option value="/api/advanced-topics/remote-extensions">Remote Development and Codespaces</option><option value="/api/advanced-topics/using-proposed-api">Using Proposed API</option><option value="/api/advanced-topics/tslint-eslint-migration">Migrate from TSLint to ESLint</option><option value="/api/advanced-topics/python-extension-template">Python Extension Template</option></optgroup><optgroup label="References"><option value="/api/references/vscode-api">VS Code API</option><option value="/api/references/contribution-points">Contribution Points</option><option value="/api/references/activation-events">Activation Events</option><option value="/api/references/extension-manifest">Extension Manifest</option><option value="/api/references/commands">Built-In Commands</option><option value="/api/references/when-clause-contexts">When Clause Contexts</option><option value="/api/references/theme-color">Theme Color</option><option value="/api/references/icons-in-labels">Product Icon Reference</option><option value="/api/references/document-selector">Document Selector</option></optgroup></select></nav></aside><div class="docs-content-wrapper">
			
			<main class="docs-main-content body"><h1>Custom Editor API</h1>
<p>Custom editors allow extensions to create fully customizable read/write editors that are used in place of VS Code's standard text editor for specific types of resources. They have a wide variety of use cases, such as:</p>
<ul><li>Previewing assets, such as shaders or 3D models, directly in VS Code.</li>
<li>Creating WYSIWYG editors for languages such as Markdown or XAML.</li>
<li>Offering alternative visual renderings for data files such as CSV or JSON or XML.</li>
<li>Building fully customizable editing experiences for binary or text files.</li>
</ul><p>This document provides an overview of the custom editor API and the basics of implementing a custom editor. We'll take a look at the two types of custom editors and how they differ, as well as which one is right for your use case. Then for each of these custom editor types, we'll cover the basics of building a well behaved custom editor.</p>
<p>Although custom editors are a powerful new extension point, implementing a basic custom editor is not actually that difficult! Still, if you are working on your first VS Code extension, you may want to consider holding off on diving into custom editors until you are more familiar with the basics of the VS Code API. Custom editors build on a lot of VS Code concepts—such as <a href="/api/extension-guides/webview">webviews</a> and text documents—so it may be a bit overwhelming if you are learning all of these new ideas at the same time.</p>
<p>But if you're feeling ready and are thinking about all the cool custom editors you are going to build, then let's get started! Be sure to download the <a href="https://github.com/microsoft/vscode-extension-samples/tree/main/custom-editor-sample" class="external-link" target="_blank">custom editor extension sample</a> so you can follow along with the documentation and see how the custom editor API comes together.</p>
<h2 id="links" data-needslink="links">Links</h2>
<ul><li><a href="https://github.com/microsoft/vscode-extension-samples/tree/main/custom-editor-sample" class="external-link" target="_blank">Custom Editor sample</a></li>
</ul><h3 id="vs-code-api-usage" data-needslink="vs-code-api-usage">VS Code API Usage</h3>
<ul><li><a href="/api/references/vscode-api#window.registerCustomEditorProvider"><code>window.registerCustomEditorProvider</code></a></li>
<li><a href="/api/references/vscode-api#CustomTextEditorProvider"><code>CustomTextEditorProvider</code></a></li>
</ul><h2 id="custom-editor-api-basics" data-needslink="custom-editor-api-basics">Custom Editor API basics</h2>
<p>A custom editor is an alternative view that is shown in place of VS Code's standard text editor for specific resources. There are two parts to a custom editor: the view that users interact with and the document model that your extension uses to interact with the underlying resource.</p>
<p>The view side of a custom editor is implemented using a <a href="/api/extension-guides/webview">webview</a>. This lets you build the user interface of your custom editor using standard HTML, CSS, and JavaScript. Webviews cannot access the VS Code API directly but they can talk with extensions by passing messages back and forth. Check out our <a href="/api/extension-guides/webview">webview documentation</a> for more information on webviews and best practices for working with them.</p>
<p>The other part of a custom editor is the document model. This model is how your extension understands the resource (file) it is working with. A <code>CustomTextEditorProvider</code> uses VS Code's standard <a href="/api/references/vscode-api#TextDocument">TextDocument</a> as its document model and all changes to the file are expressed using VS Code's standard text editing APIs. <code>CustomReadonlyEditorProvider</code> and <code>CustomEditorProvider</code> on the other hand let you provide your own document model, which lets them be used for non-text file formats.</p>
<p>Custom editors have a single document model per resource but there may be multiple editor instances (views) of this document. For example, imagine that you open a file that has a <code>CustomTextEditorProvider</code> and then run the <strong>View: Split editor</strong> command. In this case, there is still just a single <code>TextDocument</code> since there is still just a single copy of the resource in the workspace,  but there are now two webviews for that resource.</p>
<h3 id="customeditor-vs-customtexteditor" data-needslink="customeditor-vs-customtexteditor"><code>CustomEditor</code> vs <code>CustomTextEditor</code></h3>
<p>There are two classes of custom editors: custom text editors and custom editors. The main difference between these is how they define their document model.</p>
<p>A <code>CustomTextEditorProvider</code> uses VS Code's standard <a href="https://code.visualstudio.com/api/references/vscode-api#TextDocument"><code>TextDocument</code></a> as its data model. You can use a <code>CustomTextEditor</code> for any text based file types. <code>CustomTextEditor</code>s are considerably easier to implement because VS Code already knows how to work with text files and can therefore implement operations such as save and backing up files for hot exit.</p>
<p>With a <code>CustomEditorProvider</code> on the other hand, your extension brings its own document model. This means that you can use a <code>CustomEditor</code> for binary formats such as images, but it also means that your extension is responsible for a lot more, including implementing save and backing. You can skip over much of this complexity if your custom editor is readonly, such as custom editors for previews.</p>
<p>When trying to decide which type of custom editor to use, the decision is usually simple: if you are working with a text based file format use <code>CustomTextEditorProvider</code>, for binary file formats use <code>CustomEditorProvider</code>.</p>
<h3 id="contribution-point" data-needslink="contribution-point">Contribution point</h3>
<p>The <code>customEditors</code> <a href="/api/references/contribution-points">contribution point</a> is how your extension tells VS Code about the custom editors that it provides. For example, VS Code needs to know what types of files your custom editor works with as well as how to identify your custom editor in any UI.</p>
<p>Here's a basic <code>customEditor</code> contribution for the <a href="https://github.com/microsoft/vscode-extension-samples/tree/main/custom-editor-sample" class="external-link" target="_blank">custom editor extension sample</a>:</p>
<pre class="shiki" data-lang="json" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"contributes"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">  "customEditors"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">      "viewType"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"catEdit.catScratch"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">      "displayName"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"Cat Scratch"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">,</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">      "selector"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: [</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">        {</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">          "filenamePattern"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"*.cscratch"</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">        }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">      ],</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#0451A5">      "priority"</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">: </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">"default"</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">    }</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">  ]</span></span>
<span class="line"><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">}</span></span>
<span class="line"></span></code></pre>
<p><code>customEditors</code> is an array, so your extension can contribute multiple custom editors. Let's break down the custom editor entry itself:</p>
<ul><li>
<p><code>viewType</code> - Unique identifier for your custom editor.</p>
<p>This is how VS Code ties a custom editor contribution in the <code>package.json</code> to your custom editor implementation in code. This must be unique across all extensions, so instead of a generic <code>viewType</code> such as <code>"preview"</code> make sure to use one that is unique to your extension, for example <code>"viewType": "myAmazingExtension.svgPreview"</code></p>
</li>
<li>
<p><code>displayName</code> - Name that identifies the custom editor in VS Code's UI.</p>
<p>The display name is shown to the user in VS Code UI such as the <strong>View: Reopen with</strong> dropdown.</p>
</li>
<li>
<p><code>selector</code> - Specifies which files a custom editor is active for.</p>
<p>The <code>selector</code> is an array of one or more <a href="/docs/editor/glob-patterns">glob patterns</a>. These glob patterns are matched against file names to determine if the custom editor can be used for them. A <code>filenamePattern</code> such as <code>*.png</code> will enable the custom editor for all PNG files.</p>
<p>You can also create more specific patterns that match on file or directory names, for example <code>**/translations/*.json</code>.</p>
</li>
<li>
<p><code>priority</code> - (optional) Specifies when the custom editor is used.</p>
<p><code>priority</code> controls when a custom editor is used when a resource is open. Possible values are:</p>
<ul><li><code>"default"</code> - Try to use the custom editor for every file that matches the custom editor's <code>selector</code>. If there are multiple custom editors for a given file, the user will have to select which custom editor they want to use.</li>
<li><code>"option"</code> - Do not use the custom editor by default but allow users to switch to it or configure it as their default.</li>
</ul></li>
</ul><h3 id="custom-editor-activation" data-needslink="custom-editor-activation">Custom editor activation</h3>
<p>When a user opens one of your custom editors, VS Code fires an <code>onCustomEditor:VIEW_TYPE</code> activation event. During activation, your extension must call <code>registerCustomEditorProvider</code> to register a custom editor with the expected <code>viewType</code>.</p>
<p>It's important to note that <code>onCustomEditor</code> is only called when VS Code needs to create an instance of your custom editor. If VS Code is merely showing the user some information about an available custom editor—such as with the <strong>View: Reopen with</strong> command—your extension will not be activated.</p>
<h2 id="custom-text-editor" data-needslink="custom-text-editor">Custom Text Editor</h2>
<p>Custom text editors let you create custom editors for text files. This can be anything from plain unstructured text to <a href="https://en.wikipedia.org/wiki/Comma-separated_values" class="external-link" target="_blank">CSV</a> to JSON or XML. Custom text editors use VS Code's standard <a href="/api/references/vscode-api#TextDocument">TextDocument</a> as their document model.</p>
<p>The <a href="https://github.com/microsoft/vscode-extension-samples/tree/main/custom-editor-sample" class="external-link" target="_blank">custom editor extension sample</a> includes a simple example custom text editor for cat scratch files (which are just JSON files that end with a <code>.cscratch</code> file extension). Let's take a look at some of the important bits of implementing a custom text editor.</p>
<h3 id="custom-text-editor-lifecycle" data-needslink="custom-text-editor-lifecycle">Custom Text Editor lifecycle</h3>
<p>VS Code handles the lifecycle of both the view component of custom text editors (the webviews) and the model component (<code>TextDocument</code>). VS Code calls out to your extension when it needs to create a new custom editor instance and cleans up the editor instances and document model when the user closes their tabs.</p>
<p>To understand how this all works in practice, let's work through what happens from an extension's point of view when a user opens a custom text editor and then when a user closes a custom text editor.</p>
<p><strong>Opening a custom text editor</strong></p>
<p>Using the <a href="https://github.com/microsoft/vscode-extension-samples/tree/main/custom-editor-sample" class="external-link" target="_blank">custom editor extension sample</a>, here's what happens when the user first opens a <code>.cscratch</code> file:</p>
<ol><li>
<p>VS Code fires an <code>onCustomEditor:catCustoms.catScratch</code> activation event.</p>
<p>This activates our extension if it has not already been activated. During activation, our extension must ensure the extension registers a <code>CustomTextEditorProvider</code> for <code>catCustoms.catScratch</code> by calling <code>registerCustomEditorProvider</code>.</p>
</li>
<li>
<p>VS Code then invokes <code>resolveCustomTextEditor</code> on the registered <code>CustomTextEditorProvider</code> for <code>catCustoms.catScratch</code>.</p>
<p>This method takes the <code>TextDocument</code> for the resource that is being opened and a <code>WebviewPanel</code>. The extension must fill in the initial HTML contents for this webview panel.</p>
</li>
</ol><p>Once <code>resolveCustomTextEditor</code> returns, our custom editor is displayed to the user. What is drawn inside the webview is entirely up to our extension.</p>
<p>This same flow happens every time a custom editor is opened, even when you split a custom editor. Every instance of a custom editor has its own <code>WebviewPanel</code>, although multiple custom text editors will share the same <code>TextDocument</code> if they are for the same resource. Remember: think of the <code>TextDocument</code> as being the model for the resource while the webview panels are views of that model.</p>
<p><strong>Closing custom text editors</strong></p>
<p>When a user closes a custom text editor, VS Code fires the <code>WebviewPanel.onDidDispose</code> event on the <code>WebviewPanel</code>. At this point, your extension should clean up any resources associated with that editor (event subscriptions, file watchers, etc.)</p>
<p>When the last custom editor for a given resource is closed, the <code>TextDocument</code> for that resource will also be disposed provided there are no other editors using it and no other extensions are holding onto it. You can check the <code>TextDocument.isClosed</code> property to see if the <code>TextDocument</code> has been closed. Once a <code>TextDocument</code> is closed, opening the same resource using a custom editor will cause a new <code>TextDocument</code> to be opened.</p>
<h3 id="synchronizing-changes-with-the-textdocument" data-needslink="synchronizing-changes-with-the-textdocument">Synchronizing changes with the TextDocument</h3>
<p>Since custom text editors use a <code>TextDocument</code> as their document model, they are responsible for updating the <code>TextDocument</code> whenever an edit occurs in a custom editor as well as updating themselves whenever the <code>TextDocument</code> changes.</p>
<p><strong>From webview to <code>TextDocument</code></strong></p>
<p>Edits in custom text editors can take many different forms—clicking a button, changing some text, dragging some items around. Whenever a user edits the file itself inside the custom text editor, the extension must update the <code>TextDocument</code>. Here's how the cat scratch extension implements this:</p>
<ol><li>
<p>User clicks the <strong>Add scratch</strong> button in the webview. This <a href="/api/extension-guides/webview#scripts-and-message-passing">posts a message</a> from the webview back to the extension.</p>
</li>
<li>
<p>The extension receives the message. It then updates its internal model of the document (which in the cat scratch example just consists of adding a new entry to the JSON).</p>
</li>
<li>
<p>The extension creates a <code>WorkspaceEdit</code> that writes the updated JSON to the document. This edit is applied using <code>vscode.workspace.applyEdit</code>.</p>
</li>
</ol><p>Try to keep your workspace edit to the minimal change required to update the document. Also keep in mind that if you are working with a language such as JSON, your extension should try to observe the user's existing formatting conventions (spaces vs tabs, indent size, etc.).</p>
<p><strong>From <code>TextDocument</code> to webviews</strong></p>
<p>When a <code>TextDocument</code> changes, your extension also needs to make sure its webviews reflect the documents new state. TextDocuments can be changed by user actions such as undo, redo, or revert file; by other extensions using a <code>WorkspaceEdit</code>; or by a user who opens the file in VS Code's default text editor. Here's how the cat scratch extension implements this:</p>
<ol><li>
<p>In the extension, we subscribe to the <code>vscode.workspace.onDidChangeTextDocument</code> event. This event is fired for every change to the <code>TextDocument</code> (including changes that our custom editor makes!)</p>
</li>
<li>
<p>When a change comes in for a document that we have an editor for, we post a message to the webview with its new document state. This webview then updates itself to render the updated document.</p>
</li>
</ol><p>It's important to remember that any file edits that a custom editor triggers will cause <code>onDidChangeTextDocument</code> to fire. Make sure your extension does not get into an update loop where the user makes an edit in the webview, which fires <code>onDidChangeTextDocument</code>, which causes the webview to update, which causes the webview to trigger another update on your extension, which fires <code>onDidChangeTextDocument</code>, and so on.</p>
<p>Also remember that if you are working with a structured language such as JSON or XML, the document may not always be in a valid state. Your extension must either be able to gracefully handle errors or display an error message to the user so that they understand what is wrong and how to fix it.</p>
<p>Finally, if updating your webviews is expensive, consider <a href="https://davidwalsh.name/javascript-debounce-function" class="external-link" target="_blank">debouncing</a> the updates to your webview.</p>
<h2 id="custom-editor" data-needslink="custom-editor">Custom Editor</h2>
<p><code>CustomEditorProvider</code> and <code>CustomReadonlyEditorProvider</code> let you create custom editors for binary file formats. This API gives you full control over how the file is displayed to users, how edits are made to it, and lets your extension hook into <code>save</code> and other file operations. Again, if you are building an editor for a text based file format, strongly consider using a <a href="#_custom-text-editor"><code>CustomTextEditor</code></a> instead as they are far simpler to implement.</p>
<p>The <a href="https://github.com/microsoft/vscode-extension-samples/tree/main/custom-editor-sample" class="external-link" target="_blank">custom editor extension sample</a> includes a simple example custom binary editor for paw draw files (which are just jpeg files that end with a <code>.pawdraw</code> file extension). Let's take a look at what goes into building a custom editor for binary files.</p>
<h3 id="customdocument" data-needslink="customdocument">CustomDocument</h3>
<p>With custom editors, your extension is responsible for implementing its own document model with the <code>CustomDocument</code> interface. This leaves your extension free to store whatever data it needs on a <code>CustomDocument</code> in order to interact with your custom editor, but it also means that your extension must implement basic document operations such as saving and backing up file data for hot exit.</p>
<p>There is one <code>CustomDocument</code> per opened file. Users can open multiple editors for a single resource—such as by splitting the current custom editor—but all those editors will be backed by the same <code>CustomDocument</code>.</p>
<h3 id="custom-editor-lifecycle" data-needslink="custom-editor-lifecycle">Custom Editor lifecycle</h3>
<p><strong>supportsMultipleEditorsPerDocument</strong></p>
<p>By default, VS Code only allows there to be one editor for each custom document. This limitation makes it easier to correctly implement a custom editor as you do not have to worry about synchronizing multiple custom editor instances with each other.</p>
<p>If your extension can support it however, we recommend setting <code>supportsMultipleEditorsPerDocument: true</code> when registering your custom editor so that multiple editor instances can be opened for the same document. This will make your custom editors behave more like VS Code's normal text editors.</p>
<p><strong>Opening Custom Editors</strong>
When the user opens a file that matches the <code>customEditor</code> contribution point, VS Code fires an <code>onCustomEditor</code> <a href="/api/references/activation-events">activation event</a> and then invokes the provider registered for the provided view type. A <code>CustomEditorProvider</code> has two roles: providing the document for the custom editor and then providing the editor itself. Here's an ordered list of what happens for the <code>catCustoms.pawDraw</code> editor from the <a href="https://github.com/microsoft/vscode-extension-samples/tree/main/custom-editor-sample" class="external-link" target="_blank">custom editor extension sample</a>:</p>
<ol><li>
<p>VS Code fires an <code>onCustomEditor:catCustoms.pawDraw</code> activation event.</p>
<p>This activates our extension if it has not already been activated. We must also make sure our extension registers a <code>CustomReadonlyEditorProvider</code> or <code>CustomEditorProvider</code> for <code>catCustoms.pawDraw</code> during activation.</p>
</li>
<li>
<p>VS Code calls <code>openCustomDocument</code> on our <code>CustomReadonlyEditorProvider</code> or <code>CustomEditorProvider</code> registered for <code>catCustoms.pawDraw</code> editors.</p>
<p>Here our extension is given a resource uri and must return a new <code>CustomDocument</code> for that resource. This is the point at which our extension should create its document internal model for that resource. This may involve reading and parsing the initial resource state from disk or initializing our new <code>CustomDocument</code>.</p>
<p>Our extension can define this model by creating a new class that implements <code>CustomDocument</code>. Remember that this initialization stage is entirely up to extensions; VS Code does not care about any additional information extensions store on a <code>CustomDocument</code>.</p>
</li>
<li>
<p>VS Code calls <code>resolveCustomEditor</code> with the <code>CustomDocument</code> from step 2 and a new <code>WebviewPanel</code>.</p>
<p>Here our extension must fill in the initial html for the custom editor. If we need, we can also hold onto a reference to the <code>WebviewPanel</code> so that we can reference it later, for example inside commands.</p>
</li>
</ol><p>Once <code>resolveCustomEditor</code> returns, our custom editor is displayed to the user.</p>
<p>If the user opens the same resource in another editor group using our custom editor—for example by splitting the first editor—the extension's job is simplified. In this case, VS Code just calls <code>resolveCustomEditor</code> with the same <code>CustomDocument</code> we created when the first editor was opened.</p>
<p><strong>Closing Custom Editors</strong></p>
<p>Say we have two instance of our custom editors open for the same resource. When the user closes these editors, VS Code signals our extension so that it can clean up any resources associated with the editor.</p>
<p>When the first editor instance is closed, VS Code fires the <code>WebviewPanel.onDidDispose</code> event on the <code>WebviewPanel</code> from the closed editor. At this point, our extension must clean up any resources associated with that specific editor instance.</p>
<p>When the second editor is closed, VS Code again fires <code>WebviewPanel.onDidDispose</code>. However now we've also closed all the editors associated with the <code>CustomDocument</code>. When there are no more editors for a <code>CustomDocument</code>, VS Code calls the <code>CustomDocument.dispose</code> on it. Our extension's implementation of <code>dispose</code> must clean up any resources associated with the document.</p>
<p>If the user then reopens the same resource using our custom editor, we will go back through the whole <code>openCustomDocument</code>, <code>resolveCustomEditor</code> flow with a new <code>CustomDocument</code>.</p>
<h3 id="readonly-custom-editors" data-needslink="readonly-custom-editors">Readonly Custom editors</h3>
<p>Many of the following sections only apply to custom editors that support editing and, while it may sound paradoxical, many custom editors don't require editing capabilities at all. Consider a image preview for example. Or a visual rendering of a memory dump. Both can be implemented using custom editors but neither need to be editable. That's where <code>CustomReadonlyEditorProvider</code> comes in.</p>
<p>A <code>CustomReadonlyEditorProvider</code> lets you create custom editors that do not support editing. They can still be interactive but don't support operations such as undo and save. It is also much simpler to implement a readonly custom editor compared to a fully editable one.</p>
<h3 id="editable-custom-editor-basics" data-needslink="editable-custom-editor-basics">Editable Custom Editor Basics</h3>
<p>Editable custom editors let you hook in to standard VS Code operations such as undo and redo, save, and hot exit. This makes editable custom editors very powerful, but also means that properly implementing one is much more complex than implementing an editable custom text editor or a readonly custom editor.</p>
<p>Editable custom editors are implemented by <code>CustomEditorProvider</code>. This interface extends <code>CustomReadonlyEditorProvider</code>, so you'll have to implement basic operations such as <code>openCustomDocument</code> and <code>resolveCustomEditor</code>, along with a set of editing specific operations. Let's take a look at the editing specific parts of <code>CustomEditorProvider</code>.</p>
<p><strong>Edits</strong></p>
<p>Changes to a editable custom document are expressed through edits. An edit can be anything from a text change, to an image rotation, to reordering a list. VS Code leaves the specifics of what an edit does entirely up to your extension, but VS Code does need to know when an edit takes places. Editing is how VS Code marks documents as dirty, which in turn enables auto save and back ups.</p>
<p>Whenever a user makes an edit in any of the webviews for your custom editor, your extension must fire a <code>onDidChangeCustomDocument</code> event from its <code>CustomEditorProvider</code>. The <code>onDidChangeCustomDocument</code> event can fire two event types depending on your custom editor implementation: <code>CustomDocumentContentChangeEvent</code> and <code>CustomDocumentEditEvent</code>.</p>
<p><strong>CustomDocumentContentChangeEvent</strong></p>
<p>A <code>CustomDocumentContentChangeEvent</code> is a bare-bones edit. Its only function is to tell VS Code that a document has been edited.</p>
<p>When an extension fires a <code>CustomDocumentContentChangeEvent</code> from <code>onDidChangeCustomDocument</code>, VS Code will mark the associated document as being dirty. At this point, the only way for the document to become non-dirty is for the user to either save or revert it. Custom editors that use <code>CustomDocumentContentChangeEvent</code> do not support undo/redo.</p>
<p><strong>CustomDocumentEditEvent</strong></p>
<p>A <code>CustomDocumentEditEvent</code> is a more complex edit that allows for undo/redo. You should always try to implement your custom editor using <code>CustomDocumentEditEvent</code> and only fallback to using <code>CustomDocumentContentChangeEvent</code> if implementing undo/redo is not possible.</p>
<p>A <code>CustomDocumentEditEvent</code> has the following fields:</p>
<ul><li><code>document</code> — The <code>CustomDocument</code> the edit was for.</li>
<li><code>label</code> — Optional text that describes what type of edit was made (for example: "Crop", "Insert", ...)</li>
<li><code>undo</code> — Function invoked by VS Code when the edit needs to be undone.</li>
<li><code>redo</code> — Function invoked by VS Code when the edits needs to be redone.</li>
</ul><p>When an extension fires a <code>CustomDocumentEditEvent</code> from <code>onDidChangeCustomDocument</code>, VS Code marks the associated document as being dirty. To make the document no longer dirty, a user can then either save or revert the document, or undo/redo back to the document's last saved state.</p>
<p>The <code>undo</code> and <code>redo</code> methods on an editor are called by VS Code when that specific edit needs to be undone or reapplied. VS Code maintains an internal stack of edits, so if your extension fires <code>onDidChangeCustomDocument</code> with three edits, let's call them <code>a</code>, <code>b</code>, <code>c</code>:</p>
<pre class="shiki" data-lang="ts" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">onDidChangeCustomDocument</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">a</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">onDidChangeCustomDocument</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">b</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">onDidChangeCustomDocument</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">c</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"></span></code></pre>
<p>The following sequence of user actions results in these calls:</p>
<pre class="shiki" data-lang="text" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span>undo — c.undo()</span></span>
<span class="line"><span>undo — b.undo()</span></span>
<span class="line"><span>redo — b.redo()</span></span>
<span class="line"><span>redo — c.redo()</span></span>
<span class="line"><span>redo — no op, no more edits</span></span>
<span class="line"><span></span></span></code></pre>
<p>To implement undo/redo, your extension must update its associated custom document's internal state, as well as updating all associated webviews for the document so that they reflect the document's new state. Keep in mind that there may be multiple webviews for a single resource. These must always show the same document data. Multiple instances of an image editor for example must always show the same pixel data but may allow each editor instance to have its own zoom level and UI state.</p>
<h3 id="saving" data-needslink="saving">Saving</h3>
<p>When a user saves a custom editor, your extension is responsible for writing the saved resource in its current state to disk. How your custom editor does this depends largely on your extension's <code>CustomDocument</code> type and how your extension tracks edits internally.</p>
<p>The first step to saving is getting the data stream to write to disk. Common approaches to this include:</p>
<ul><li>
<p>Track the resource's state so that it can be quickly serialized.</p>
<p>A basic image editor for example may maintain a buffer of pixel data.</p>
</li>
<li>
<p>Replay edit since the last save to generate the new file.</p>
<p>A more efficient image editor for example might track the edits since the last save, such as <code>crop</code>, <code>rotate</code>, <code>scale</code>. On save, it would then apply these edits to file's last saved state to generate the new file.</p>
</li>
<li>
<p>Ask a <code>WebviewPanel</code> for the custom editor for file data to save.</p>
<p>Keep in mind though that custom editors can be saved even when they are not visible. For this reason, it is recommended that your extension's implementation of <code>save</code> does not depend on a <code>WebviewPanel</code>. If this is not possible, you can use the <code>WebviewPanelOptions.retainContextWhenHidden</code> setting so that the webview stays alive even when it is hidden. <code>retainContextWhenHidden</code> does have significant memory overhead so be conservative about using it.</p>
</li>
</ul><p>After getting the data for the resource, you generally should use the <a href="https://code.visualstudio.com/api/references/vscode-api#FileSystem">workspace FS API</a> to write it to disk. The FS APIs take a <code>UInt8Array</code> of data and can write out both binary and text based files. For binary file data, simply put the binary data into the <code>UInt8Array</code>. For text file data, use <code>Buffer</code> to convert a string into a <code>UInt8Array</code>:</p>
<pre class="shiki" data-lang="ts" shiki-themes dark-plus light-plus" style="--shiki-dark:#D4D4D4;--shiki-light:#000000;--shiki-dark-bg:#1E1E1E;--shiki-light-bg:#FFFFFF" tabindex="0"><code><span class="line"><span style="--shiki-dark:#569CD6;--shiki-light:#0000FF">const</span><span style="--shiki-dark:#4FC1FF;--shiki-light:#0070C1"> writeData</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000"> = </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">Buffer</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">from</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'my text data'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#CE9178;--shiki-light:#A31515">'utf8'</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">vscode</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">workspace</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">fs</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">.</span><span style="--shiki-dark:#DCDCAA;--shiki-light:#795E26">writeFile</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">(</span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">fileUri</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">, </span><span style="--shiki-dark:#9CDCFE;--shiki-light:#001080">writeData</span><span style="--shiki-dark:#D4D4D4;--shiki-light:#000000">);</span></span>
<span class="line"></span></code></pre>
<h2 id="next-steps" data-needslink="next-steps">Next steps</h2>
<p>If you'd like to learn more about VS Code extensibility, try these topics:</p>
<ul><li><a href="/api">Extension API</a> - Learn about the full VS Code Extension API.</li>
<li><a href="/api/extension-capabilities/overview">Extension Capabilities</a> - Take a look at other ways to extend VS Code.</li>
</ul><div class="feedback" data-edit-url="https://vscode.dev/github/microsoft/vscode-docs/blob/main/api/extension-guides/custom-editors.md"></div>
				
				<div class="body-footer">6/3/2026</div>
				
            </main><aside class="docs-right-sidebar hidden-xs"><div class="docs-markdown-actions">
                    <div class="docs-markdown-dropdown" data-raw-url="/raw/api/extension-guides/custom-editors.md">
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
                    <ul class="nav"><li><a href="#links">Links</a></li>
                        
                        <li><a href="#custom-editor-api-basics">Custom Editor API basics</a></li>
                        
                        <li><a href="#custom-text-editor">Custom Text Editor</a></li>
                        
                        <li><a href="#custom-editor">Custom Editor</a></li>
                        
                        <li><a href="#next-steps">Next steps</a></li>
                        
                    </ul></nav></aside></div>
		<div class="docs-mobile-widgets visible-xs">
			<div class="connect-widget"></div>
		</div>
	</div>
</div>
		</main>