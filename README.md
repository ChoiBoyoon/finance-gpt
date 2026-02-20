# FinanceGPT : Chatbot connected to Yahoo Finance MCP server

Chatbot specializes in giving financial advices.
Web application built with OpenAI Agents SDK, Streamlit, and [Yahoo Finance MCP Server](https://github.com/leoncuhk/mcp-yahoo-finance) (<code>MCPServerStdio</code> - runs on your local environ;ent). Also includes [Context7](https://github.com/upstash/context7)(<code>OpenAI's Hosted MCP Tool</code> - runs on OpenAI server).
Also connected to OpenAI-hosted tools : <code>WebSearchTool, FileSearchTool, ImageGenerationTool, CodeInterpreterTool</code>
Cache all the chat history, including generated images and code, and available on the sidebar in real time. Can be removed manually using <b>"Reset memory"</b> button. (Careful w/ token usage)

<img src="finance_gpt_screenshot.png">


