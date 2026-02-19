import dotenv
dotenv.load_dotenv()

from openai import OpenAI
import asyncio
import streamlit as st
from agents import Agent, Runner, SQLiteSession, WebSearchTool, FileSearchTool

client = OpenAI()

VECTOR_STORE_ID = "vs_69978ed85b0881918be6fb5ed22bb56c"

if "agent" not in st.session_state:
    st.session_state["agent"]=Agent(
        name="ChatGPT Clone",
        instructions="""
        You are a helpful assistant.
        You have access to the following tools:
            -Web Search Tool: Use this when the user asks a question that isn't in your training data. Use this to learn about current events.
        """,
        tools=[
            WebSearchTool(),
            FileSearchTool(
                vector_store_ids=[VECTOR_STORE_ID],
                max_num_results=3 #파일이 많을 경우 top3 파일만 선택
            )
        ]
    )
agent = st.session_state["agent"] #이걸 if 안에 넣으면 처음에만 실행되고 다음부턴 undefine이 됨

if "session" not in st.session_state: #딱 한 번만 실행됨!
    st.session_state["session"] = SQLiteSession(
        "chat-history", 
        "chat-gpt-clone-memory.db"
    )
session = st.session_state["session"]

async def paint_history():
    messages = await session.get_items()
    for message in messages:
        if "role" in message:
            with st.chat_message(message["role"]):
                if message["role"]=="user":
                    st.write(message["content"])
                else:
                    if message["type"]=="message":
                        st.write(message["content"][0]["text"])
        if "type" in message and message["type"]=="web_search_call":
            with st.chat_message("ai"):
                st.write("🔍 Searched the web...") 

def update_status(status_container, event):
    status_messages={
        "response.web_search_call.completed" : ("✅ Web search completed.", "complete"),
        "response.web_search_call.in_progress" : ("🔍 Starting web search...", "running"),
        "response.web_search_call.searching" : ("🔍 Web search in progress...", "running"),
        "response.completed":("✅", "complete")
    }
    if event in status_messages:
        label, state = status_messages[event]
        status_container.update(label=label, state=state)


asyncio.run(paint_history())

async def run_agent(message):
    with st.chat_message("ai"):
        status_container=st.status("⏳", expanded=False)
        text_placeholder=st.empty()
        response=""

        stream = Runner.run_streamed(
            agent,
            message,
            session=session)
        async for event in stream.stream_events():
            if event.type=="raw_response_event":

                update_status(status_container, event.data.type)

                if event.data.type=="response.output_text.delta":
                    response+=event.data.delta
                    text_placeholder.write(response)

prompt = st.chat_input(
    "Write a message for your assistant", 
    accept_file=True,
    file_type=["txt"])

if prompt:

    for file in prompt.files:
        if file.type.startswith("text/"):
            with st.chat_message("ai"):
                with st.status("⏳Uplodading file...") as status:
                    uploaded_file = client.files.create( #OpenAI에 저장됨
                        file=(file.name, file.getvalue()), #streamlit specific thing
                        purpose="user_data"
                    )
                    status.update(label="⏳ Attaching file...")
                    client.vector_stores.files.create(
                        vector_store_id=VECTOR_STORE_ID,
                        file_id=uploaded_file.id
                    )
                    status.update(label="✅ File uploaded", status="complete")

    if prompt.text:
        with st.chat_message("human"):
            st.write(prompt)
        asyncio.run(run_agent(prompt))




with st.sidebar:
    reset = st.button("Reset memory") #becomes True when user clicks on it
    if reset:
        asyncio.run(session.clear_session())
    st.write(asyncio.run(session.get_items()))
