
import os
import uuid
import sqlite3
import tempfile
import streamlit as st

from agentic_chatbot_backend import (
    chatbot,
    get_all_threads,
    ingest_rag_document,
    generate_conversation_title
)

from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    ToolMessage
)

from langgraph.types import Command

from ui_theme import (
    apply_theme,
    sidebar_status_html,
    welcome_panel_html,
    hitl_card_html
)


# ============================================================
# 1. CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Agentic AI Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Agentic AI Assistant")
st.caption(
    "Agentic workflows · Document retrieval · Human approval"
)

DATABASE_PATH = "chatbot.db"


# ============================================================
# 2. SQLITE - CONVERSATION TITLES
# ============================================================

def get_db_connection():
    return sqlite3.connect(
        DATABASE_PATH,
        timeout=30
    )


def init_title_database():
    with get_db_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS conversation_titles (
                thread_id TEXT PRIMARY KEY,
                title TEXT NOT NULL
            )
        """)


def save_conversation_title(thread_id, title):

    with get_db_connection() as conn:
        conn.execute("""
            INSERT OR REPLACE INTO conversation_titles
            (thread_id, title)
            VALUES (?, ?)
        """, (thread_id, title))


def get_conversation_title(thread_id):

    with get_db_connection() as conn:

        result = conn.execute("""
            SELECT title
            FROM conversation_titles
            WHERE thread_id = ?
        """, (thread_id,)).fetchone()

    if result:
        return result[0]

    return "New conversation"


def create_conversation_title(thread_id, user_message):

    current_title = get_conversation_title(thread_id)

    if current_title != "New conversation":
        return current_title

    try:

        title = generate_conversation_title(user_message)

        if isinstance(title, list):

            title = " ".join(
                item.get("text", "")
                for item in title
                if isinstance(item, dict)
            )

        title = str(title).strip().strip('"').strip("'")

        if not title:
            title = user_message.strip()[:40]

    except Exception as error:

        st.warning(
            f"Title generation failed: {error}"
        )

        title = user_message.strip()[:40]

    title = title[:60] or "New conversation"

    save_conversation_title(
        thread_id,
        title
    )

    return title


init_title_database()


# ============================================================
# 3. THREAD MANAGEMENT
# ============================================================

def generate_thread_id():
    return str(uuid.uuid4())


def add_thread(thread_id):

    if thread_id not in st.session_state["chat_threads"]:

        st.session_state["chat_threads"].insert(
            0,
            thread_id
        )


def reset_chat():

    new_thread_id = generate_thread_id()

    st.session_state["thread_id"] = new_thread_id
    st.session_state["message_history"] = []
    st.session_state["pending_hitl"] = None

    add_thread(new_thread_id)


def get_thread_config(thread_id):

    return {
        "configurable": {
            "thread_id": thread_id
        },
        "metadata": {
            "thread_id": thread_id,
            "application": "agentic_ai_chatbot"
        },
        "tags": [
            "agentic-chatbot",
            "langgraph",
            "streamlit"
        ],
        "run_name": "agentic_chatbot_execution"
    }


# ============================================================
# 4. MESSAGE UTILITIES
# ============================================================

def extract_text(content):

    if isinstance(content, str):
        return content

    if isinstance(content, list):

        text_parts = []

        for item in content:

            if isinstance(item, dict):

                if item.get("type") == "text":

                    text_parts.append(
                        item.get("text", "")
                    )

        return "\n".join(text_parts)

    return str(content) if content else ""


def load_conversation(thread_id):

    state = chatbot.get_state(
        get_thread_config(thread_id)
    )

    messages = state.values.get("messages", [])

    history = []

    for message in messages:

        message_type = getattr(
            message,
            "type",
            None
        )

        if message_type == "human":

            role = "user"

        elif message_type == "ai":

            role = "assistant"

            # Ignore empty AI messages used only for tool calls.
            if getattr(message, "tool_calls", None) and not message.content:
                continue

        else:
            # Tool messages are not displayed as ordinary chat messages.
            continue

        content = extract_text(message.content)

        if content.strip():

            history.append({
                "role": role,
                "content": content
            })

    return history


# ============================================================
# 5. HUMAN-IN-THE-LOOP
# ============================================================

def get_pending_interrupt(thread_id):

    try:

        state_snapshot = chatbot.get_state(
            get_thread_config(thread_id)
        )

        direct_interrupts = getattr(
            state_snapshot,
            "interrupts",
            ()
        ) or ()

        if direct_interrupts:
            return direct_interrupts[0]

        tasks = getattr(
            state_snapshot,
            "tasks",
            ()
        ) or ()

        for task in tasks:

            task_interrupts = getattr(
                task,
                "interrupts",
                ()
            ) or ()

            if task_interrupts:
                return task_interrupts[0]

    except Exception as error:

        st.warning(
            f"Could not inspect pending approval: {error}"
        )

    return None


def save_pending_interrupt(thread_id, interrupt_object):

    st.session_state["pending_hitl"] = {
        "thread_id": thread_id,
        "prompt": str(interrupt_object.value)
    }


def sync_pending_interrupt(thread_id):

    pending_interrupt = get_pending_interrupt(
        thread_id
    )

    if pending_interrupt is not None:

        save_pending_interrupt(
            thread_id,
            pending_interrupt
        )

    else:

        current_pending = st.session_state.get(
            "pending_hitl"
        )

        if (
            current_pending is not None
            and current_pending.get("thread_id") == thread_id
        ):

            st.session_state["pending_hitl"] = None


# ============================================================
# 6. STREAMING UTILITIES
# ============================================================

def stream_graph_response(
    input_data,
    config,
    status_box=None
):

    for message_chunk, metadata in chatbot.stream(
        input_data,
        config=config,
        stream_mode="messages"
    ):

        message_type = getattr(
            message_chunk,
            "type",
            None
        )

        if message_type == "tool":

            tool_name = getattr(
                message_chunk,
                "name",
                "tool"
            )

            if status_box is not None:

                status_box.update(
                    label=f"🔧 Using {tool_name}...",
                    state="running"
                )

        elif message_type in ("ai", "AIMessageChunk"):

            text = extract_text(
                message_chunk.content
            )

            if text:
                yield text


# ============================================================
# 7. RESUME HITL EXECUTION
# ============================================================

def resume_hitl_execution(decision):

    pending_hitl = st.session_state.get(
        "pending_hitl"
    )

    if not pending_hitl:

        st.warning(
            "There is no pending action to approve or reject."
        )

        return

    thread_id = pending_hitl["thread_id"]

    resume_config = get_thread_config(thread_id)

    resume_config["run_name"] = "hitl_resume_execution"

    try:

        with st.chat_message("assistant"):

            status_box = st.status(
                "🔄 Resuming the workflow...",
                expanded=True
            )

            response = st.write_stream(
                stream_graph_response(
                    Command(resume=decision),
                    resume_config,
                    status_box
                )
            )

            next_interrupt = get_pending_interrupt(
                thread_id
            )

            if next_interrupt is not None:

                save_pending_interrupt(
                    thread_id,
                    next_interrupt
                )

                status_box.update(
                    label="⚠️ Another approval is required",
                    state="complete",
                    expanded=False
                )

            else:

                st.session_state["pending_hitl"] = None

                status_box.update(
                    label="✅ Workflow completed",
                    state="complete",
                    expanded=False
                )

        # Refresh the complete history from LangGraph.
        # This avoids storing duplicate streamed messages.
        if thread_id == st.session_state["thread_id"]:

            st.session_state["message_history"] = (
                load_conversation(thread_id)
            )

        st.rerun()

    except Exception as error:

        st.error(
            f"Could not resume the workflow: {error}"
        )


# ============================================================
# 8. INITIALIZE SESSION STATE
# ============================================================

if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = generate_thread_id()

if "chat_threads" not in st.session_state:
    st.session_state["chat_threads"] = get_all_threads()

if "pending_hitl" not in st.session_state:
    st.session_state["pending_hitl"] = None


add_thread(
    st.session_state["thread_id"]
)

sync_pending_interrupt(
    st.session_state["thread_id"]
)


# ============================================================
# 9. SIDEBAR - CONVERSATION HISTORY
# ============================================================

apply_theme(st.session_state["thread_id"])

st.sidebar.title("💬 My Conversations")

if st.sidebar.button(
    "➕ New Chat",
    use_container_width=True
):

    reset_chat()
    st.rerun()


st.sidebar.divider()


for thread_id in st.session_state["chat_threads"]:

    title = get_conversation_title(thread_id)

    if thread_id == st.session_state["thread_id"]:

        button_label = f"📌 {title}"

    else:

        button_label = f"💬 {title}"

    if st.sidebar.button(
        button_label,
        key=f"thread_{thread_id}",
        use_container_width=True
    ):

        st.session_state["thread_id"] = thread_id

        st.session_state["message_history"] = (
            load_conversation(thread_id)
        )

        sync_pending_interrupt(thread_id)

        st.rerun()

st.sidebar.markdown(
    sidebar_status_html("Gemini 3.5 Flash · GPT-OSS 20B", "Ready"),
    unsafe_allow_html=True
)


# ============================================================
# 10. MAIN CHAT INTERFACE
# ============================================================

current_thread_id = st.session_state["thread_id"]

current_title = get_conversation_title(
    current_thread_id
)

if st.session_state["message_history"]:
    st.subheader(current_title)
else:
    st.markdown(
        welcome_panel_html(),
        unsafe_allow_html=True
    )


for message in st.session_state["message_history"]:

    avatar = "👤" if message["role"] == "user" else "🤖"

    with st.chat_message(message["role"], avatar=avatar):

        st.markdown(
            message["content"]
        )


# ============================================================
# 11. HITL APPROVAL INTERFACE
# ============================================================

pending_hitl = st.session_state.get(
    "pending_hitl"
)

current_thread_has_pending_hitl = (
    pending_hitl is not None
    and pending_hitl.get("thread_id") == current_thread_id
)


if current_thread_has_pending_hitl:

    st.markdown(
        hitl_card_html(pending_hitl["prompt"]),
        unsafe_allow_html=True
    )

    approve_column, reject_column = st.columns(2)

    with approve_column:

        if st.button(
            "✅ Approve",
            key=f"approve_{current_thread_id}",
            type="primary",
            use_container_width=True
        ):

            resume_hitl_execution("yes")

    with reject_column:

        if st.button(
            "❌ Reject",
            key=f"reject_{current_thread_id}",
            use_container_width=True
        ):

            resume_hitl_execution("no")


# ============================================================
# 12. PDF UPLOAD AND CHAT INPUT
# ============================================================

submission = st.chat_input(
    "Ask me anything...",
    accept_file=True,
    file_type=["pdf"],
    disabled=current_thread_has_pending_hitl
)

user_input = None


if submission:

    user_input = (submission.text or "").strip()

    uploaded_files = submission.files

    if uploaded_files:

        uploaded_pdf = uploaded_files[0]

        temporary_file_path = None

        try:

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".pdf"
            ) as temporary_file:

                temporary_file.write(
                    uploaded_pdf.getvalue()
                )

                temporary_file_path = temporary_file.name

            with st.spinner(
                f"Processing {uploaded_pdf.name}..."
            ):

                ingest_rag_document(
                    temporary_file_path
                )

            st.toast(
                f"{uploaded_pdf.name} processed successfully.",
                icon="✅"
            )

        except Exception as error:

            st.error(
                f"PDF processing failed: {error}"
            )

        finally:

            if (
                temporary_file_path
                and os.path.exists(temporary_file_path)
            ):

                os.remove(temporary_file_path)


# ============================================================
# 13. RUN AGENTIC CHATBOT
# ============================================================

if user_input:

    current_thread_id = st.session_state["thread_id"]

    # Generate a title only for the first user message.
    create_conversation_title(
        current_thread_id,
        user_input
    )

    # Display the user message.
    st.session_state["message_history"].append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)

    config = get_thread_config(
        current_thread_id
    )

    try:

        with st.chat_message("assistant", avatar="🤖"):

            status_box = st.status(
                "🤖 Agent is processing your request...",
                expanded=True
            )

            ai_message = st.write_stream(
                stream_graph_response(
                    {
                        "messages": [
                            HumanMessage(content=user_input)
                        ]
                    },
                    config,
                    status_box
                )
            )

            # Check for an unresolved LangGraph interrupt.
            pending_interrupt = get_pending_interrupt(
                current_thread_id
            )

            if pending_interrupt is not None:

                save_pending_interrupt(
                    current_thread_id,
                    pending_interrupt
                )

                status_box.update(
                    label="⏸️ Waiting for human approval",
                    state="complete",
                    expanded=False
                )

            else:

                status_box.update(
                    label="✅ Workflow completed",
                    state="complete",
                    expanded=False
                )

        # Reload history from the authoritative LangGraph state.
        st.session_state["message_history"] = (
            load_conversation(current_thread_id)
        )

        # The approval prompt is displayed separately by the HITL UI.
        st.rerun()

    except Exception as error:

        st.error(
            f"Chatbot execution failed: {error}"
        )

        st.exception(error)
