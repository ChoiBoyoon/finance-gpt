# FinanceGPT : Chatbot connected to Yahoo Finance MCP server

Chatbot specializes in giving financial advices.
Web application built with <b>OpenAI Agents SDK</b>, Streamlit, and [Yahoo Finance MCP Server](https://github.com/leoncuhk/mcp-yahoo-finance) (<code>MCPServerStdio</code> - runs on your local environment) and [Context7](https://github.com/upstash/context7)(<code>OpenAI's Hosted MCP Tool</code> - runs on OpenAI server).</br>
Also connected to OpenAI-hosted tools : <code>WebSearchTool, FileSearchTool, ImageGenerationTool, CodeInterpreterTool</code>.<br/>
Cache all the chat history, including generated images and code, and available on the sidebar in real time. <br/>
Can be removed manually using <b>"Reset memory"</b> button. (Be careful w/ token usage)<br/>
<br/>
<img src="finance_gpt_screenshot.png">


