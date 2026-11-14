from html import escape

import streamlit as st


ACCENT = "#5B8CFF"


def apply_theme(active_thread_id=None):
    active_thread_rule = ""
    hitl_button_rules = ""
    if active_thread_id:
        active_thread_rule = f"""
        [data-testid="stSidebar"] [class~="st-key-thread_{active_thread_id}"] button {{
            background: #E8F0FF !important;
            border-color: #A9C3FF !important;
            color: #173B78 !important;
            font-weight: 650 !important;
        }}
        """
        hitl_button_rules = f"""
        [class~="st-key-approve_{active_thread_id}"] button {{
            border: 1px solid #176B45 !important;
            background: #176B45 !important;
            color: #FFFFFF !important;
            font-weight: 680 !important;
        }}

        [class~="st-key-approve_{active_thread_id}"] button:hover {{
            border-color: #125638 !important;
            background: #125638 !important;
        }}

        [class~="st-key-reject_{active_thread_id}"] button {{
            border: 1px solid #A12727 !important;
            background: #FFFFFF !important;
            color: #8F1D1D !important;
            font-weight: 650 !important;
        }}

        [class~="st-key-reject_{active_thread_id}"] button:hover {{
            background: #FFF4F3 !important;
            border-color: #8F1D1D !important;
        }}
        """

    st.markdown(
        f"""
        <style>
        :root {{
            --agentic-accent: {ACCENT};
            --agentic-ink: #1D2939;
            --agentic-muted: #526174;
            --agentic-border: #D8E0EB;
            --agentic-surface: #FFFFFF;
            --agentic-canvas: #F7F9FC;
        }}

        [data-testid="stAppViewContainer"] {{
            background: var(--agentic-canvas);
            color: var(--agentic-ink);
        }}

        [data-testid="stHeader"],
        [data-testid="stBottom"],
        [data-testid="stBottomBlockContainer"] {{
            background: var(--agentic-canvas) !important;
            color: var(--agentic-ink) !important;
        }}

        [data-testid="stBottomBlockContainer"] {{
            border-top: 1px solid var(--agentic-border);
            box-shadow: 0 -6px 18px rgba(27, 46, 77, 0.06);
        }}

        section.main > div.block-container {{
            max-width: 1440px;
            padding: 1.65rem clamp(1rem, 3vw, 2.75rem) 7rem;
        }}

        [data-testid="stSidebar"] {{
            background: #F1F4F9;
            border-right: 1px solid var(--agentic-border);
        }}

        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
        [data-testid="stSidebar"] button {{
            color: var(--agentic-ink);
        }}

        button[data-testid="stBaseButton-secondary"] {{
            border: 1px solid #D5DEEA !important;
            background: #FFFFFF !important;
            color: var(--agentic-ink) !important;
        }}

        button[data-testid="stBaseButton-secondary"]:hover {{
            border-color: #A9C3FF !important;
            background: #F2F6FF !important;
            color: var(--agentic-ink) !important;
        }}

        button[data-testid="stBaseButton-primary"] {{
            border: 1px solid var(--agentic-accent) !important;
            background: var(--agentic-accent) !important;
            color: #FFFFFF !important;
        }}

        button[data-testid="stBaseButton-primary"]:hover {{
            border-color: #4779E8 !important;
            background: #4779E8 !important;
            color: #FFFFFF !important;
        }}

        .agentic-sidebar-status {{
            position: sticky;
            bottom: 0.5rem;
            z-index: 2;
            margin-top: 1.25rem;
            padding: 0.85rem 0.95rem;
            border: 1px solid #D5DEEA;
            border-radius: 12px;
            background: #FFFFFF;
            box-shadow: 0 4px 14px rgba(27, 46, 77, 0.06);
            color: var(--agentic-ink);
            font-size: 0.82rem;
        }}

        .agentic-sidebar-status__label {{
            display: block;
            margin-bottom: 0.25rem;
            color: var(--agentic-muted);
            font-size: 0.72rem;
            font-weight: 650;
            letter-spacing: 0.06em;
            text-transform: uppercase;
        }}

        .agentic-sidebar-status__state {{
            display: flex;
            align-items: center;
            gap: 0.45rem;
            margin-top: 0.6rem;
            color: #176B45;
            font-weight: 650;
        }}

        .agentic-sidebar-status__dot {{
            width: 0.48rem;
            height: 0.48rem;
            border-radius: 50%;
            background: #25845A;
        }}

        .agentic-hitl-card {{
            margin: 0.75rem 0 1rem;
            padding: 1.1rem 1.2rem;
            border: 1px solid #C9D8F4;
            border-left: 5px solid var(--agentic-accent);
            border-radius: 13px;
            background: #F1F6FF;
            color: #1D2939;
        }}

        .agentic-hitl-card__heading {{
            display: flex;
            align-items: center;
            gap: 0.55rem;
            margin: 0 0 0.45rem;
            color: #203A65;
            font-size: 1rem;
            font-weight: 720;
        }}

        .agentic-hitl-card__prompt {{
            margin: 0;
            color: #34445A;
            line-height: 1.65;
            overflow-wrap: anywhere;
            white-space: pre-wrap;
        }}

        h1, h2, h3 {{
            color: var(--agentic-ink);
            letter-spacing: -0.035em;
        }}

        h1 {{
            margin-bottom: 0.3rem;
            font-size: clamp(1.7rem, 3.2vw, 2.45rem);
            font-weight: 720;
        }}

        .agentic-welcome {{
            margin: 1.1rem auto 1.5rem;
            max-width: 1000px;
        }}

        .agentic-welcome__banner {{
            padding: clamp(1.25rem, 3vw, 2rem);
            border: 1px solid #D8E2F0;
            border-radius: 18px;
            background: #FFFFFF;
        }}

        .agentic-welcome__eyebrow {{
            margin: 0 0 0.35rem;
            color: #355C9B;
            font-size: 0.76rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }}

        .agentic-welcome__title {{
            margin: 0;
            color: var(--agentic-ink);
            font-size: clamp(1.65rem, 4vw, 2.35rem);
            font-weight: 720;
            letter-spacing: -0.045em;
            line-height: 1.15;
        }}

        .agentic-welcome__description {{
            max-width: 68ch;
            margin: 0.7rem 0 0;
            color: #46566C;
            font-size: 1rem;
            line-height: 1.65;
        }}

        .agentic-welcome__grid {{
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 0.85rem;
            margin-top: 0.9rem;
        }}

        .agentic-welcome__card {{
            min-height: 138px;
            padding: 1rem 1.05rem;
            border: 1px solid var(--agentic-border);
            border-radius: 14px;
            background: #FFFFFF;
            transition: border-color 150ms ease, box-shadow 150ms ease;
        }}

        .agentic-welcome__card:hover {{
            border-color: #9EB9F2;
            box-shadow: 0 5px 16px rgba(27, 46, 77, 0.07);
        }}

        .agentic-welcome__card-title {{
            margin: 0 0 0.4rem;
            color: #23344A;
            font-size: 0.97rem;
            font-weight: 680;
        }}

        .agentic-welcome__card-copy {{
            margin: 0;
            color: #526174;
            font-size: 0.88rem;
            line-height: 1.55;
        }}

        .agentic-welcome__example {{
            display: inline-block;
            margin-top: 0.7rem;
            padding: 0.28rem 0.55rem;
            border: 1px solid #D7E1F0;
            border-radius: 999px;
            background: #F5F8FD;
            color: #34445A;
            font-size: 0.78rem;
            line-height: 1.4;
        }}

        [data-testid="stChatMessage"] {{
            max-width: 84ch;
            margin: 0 auto 1.15rem;
            padding: 1rem 1.15rem;
            border: 1px solid transparent;
            border-radius: 16px;
            line-height: 1.65;
        }}

        [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {{
            background: #EAF1FF;
            border-color: #CFDCFA;
        }}

        [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {{
            background: var(--agentic-surface);
            border-color: var(--agentic-border);
        }}

        [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] {{
            max-width: 80ch;
            color: var(--agentic-ink);
            line-height: 1.7;
            overflow-wrap: anywhere;
        }}

        [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] p {{
            margin: 0.45rem 0 0.85rem;
        }}

        [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] h1,
        [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] h2,
        [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] h3 {{
            margin: 1.25rem 0 0.55rem;
        }}

        [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] a {{
            color: #245BC1;
            text-decoration-thickness: 1px;
            text-underline-offset: 3px;
        }}

        [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] blockquote {{
            margin: 0.85rem 0;
            padding: 0.15rem 0 0.15rem 1rem;
            border-left: 3px solid var(--agentic-accent);
            color: #34445A;
        }}

        [data-testid="stCodeBlock"] {{
            margin: 0.8rem 0 1rem;
            border: 1px solid #D5DEEA;
            border-radius: 12px;
            background: #F3F6FA;
            overflow: hidden;
        }}

        [data-testid="stCodeBlock"] pre,
        [data-testid="stCodeBlock"] code,
        [data-testid="stMarkdownContainer"] :not(pre) > code {{
            font-family: "Cascadia Code", "SFMono-Regular", Consolas, monospace;
            font-size: 0.9em;
        }}

        [data-testid="stMarkdownContainer"] :not(pre) > code {{
            padding: 0.12em 0.35em;
            border: 1px solid #DCE3ED;
            border-radius: 5px;
            background: #F1F4F8;
            color: #26364B;
        }}

        [data-testid="stChatMessage"] table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.94rem;
        }}

        [data-testid="stChatMessage"] th,
        [data-testid="stChatMessage"] td {{
            padding: 0.65rem 0.8rem;
            border: 1px solid #D8E0EB;
            text-align: left;
            vertical-align: top;
        }}

        [data-testid="stChatMessage"] th {{
            background: #F0F4FA;
            color: #26364B;
            font-weight: 650;
        }}

        [data-testid="stChatInput"] {{
            max-width: 980px;
            margin: 0 auto;
        }}

        [data-testid="stChatInput"] > div {{
            border: 1px solid #BFCADB;
            border-radius: 16px;
            background: var(--agentic-surface);
            box-shadow: 0 5px 18px rgba(27, 46, 77, 0.08);
            transition: border-color 150ms ease, box-shadow 150ms ease;
        }}

        [data-testid="stChatInput"] > div:focus-within {{
            border-color: #AEB9C8;
            box-shadow: 0 5px 18px rgba(27, 46, 77, 0.08);
        }}

        [data-testid="stChatInput"] textarea:focus-visible {{
            outline: none !important;
        }}

        [data-testid="stChatInput"]:has(textarea:focus-visible) > div {{
            outline: 2px solid #526174;
            outline-offset: 2px;
        }}

        [data-testid="stChatInput"] textarea {{
            background: #FFFFFF !important;
            color: var(--agentic-ink) !important;
        }}

        [data-testid="stChatInput"] textarea::placeholder {{
            color: #667085 !important;
            opacity: 1;
        }}

        [data-testid="stChatInput"] button {{
            background: transparent !important;
            color: #34445A !important;
        }}

        [data-testid="stStatusWidget"] {{
            border: 1px solid var(--agentic-border);
            border-radius: 12px;
            background: #F5F8FC;
        }}

        [data-testid="stStatusWidget"] summary {{
            padding: 0.8rem 1rem;
            color: #26364B;
            font-weight: 650;
        }}

        [data-testid="stStatusWidget"] [data-testid="stMarkdownContainer"] {{
            color: #34445A;
            line-height: 1.55;
        }}

        [data-testid="stExpander"] {{
            border: 1px solid var(--agentic-border);
            border-radius: 12px;
            background: var(--agentic-surface);
        }}

        [data-testid="stAlert"] {{
            border: 1px solid #D8E0EB;
            border-radius: 12px;
            color: var(--agentic-ink);
        }}

        [data-testid="stToast"] {{
            border: 1px solid var(--agentic-border);
            border-radius: 12px;
            background: #FFFFFF;
            color: var(--agentic-ink);
        }}

        [data-testid="stSpinner"] {{
            color: #34445A;
        }}

        [data-testid="stSpinner"] svg {{
            color: var(--agentic-accent);
        }}

        button, a, textarea, input, [tabindex]:not([tabindex="-1"]) {{
            transition: border-color 150ms ease, background-color 150ms ease,
                box-shadow 150ms ease, color 150ms ease;
        }}

        :focus-visible {{
            outline: 3px solid var(--agentic-accent) !important;
            outline-offset: 2px !important;
        }}

        {active_thread_rule}
        {hitl_button_rules}

        @media (max-width: 1024px) {{
            .agentic-welcome__grid {{
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }}
        }}

        @media (max-width: 768px) {{
            section.main > div.block-container {{
                padding: 1.1rem 0.8rem 6.5rem;
            }}

            [data-testid="stChatMessage"] {{
                padding: 0.8rem 0.9rem;
                margin-bottom: 0.85rem;
                border-radius: 13px;
            }}

            .agentic-welcome__grid {{
                grid-template-columns: 1fr;
                gap: 0.65rem;
            }}

            .agentic-welcome__card {{
                min-height: 0;
            }}

            [data-testid="stChatMessage"] table {{
                display: block;
                overflow-x: auto;
            }}
        }}

        @media (prefers-reduced-motion: reduce) {{
            *, *::before, *::after {{
                scroll-behavior: auto !important;
                animation-duration: 0.01ms !important;
                animation-iteration-count: 1 !important;
                transition-duration: 0.01ms !important;
            }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def sidebar_status_html(model_name, status):
    return f"""
    <div class="agentic-sidebar-status" aria-label="Assistant status">
        <span class="agentic-sidebar-status__label">Model</span>
        <div>{escape(model_name)}</div>
        <div class="agentic-sidebar-status__state">
            <span class="agentic-sidebar-status__dot" aria-hidden="true"></span>
            <span>{escape(status)}</span>
        </div>
    </div>
    """


def welcome_panel_html():
    return """
    <section class="agentic-welcome" aria-label="Welcome">
        <div class="agentic-welcome__banner">
            <p class="agentic-welcome__eyebrow">Your AI workspace</p>
            <h2 class="agentic-welcome__title">How can I help you today?</h2>
            <p class="agentic-welcome__description">
                Ask a question, upload a PDF for context, or let the agent
                work through a task with you.
            </p>
        </div>
        <div class="agentic-welcome__grid">
            <article class="agentic-welcome__card">
                <h3 class="agentic-welcome__card-title">Agentic workflows</h3>
                <p class="agentic-welcome__card-copy">
                    Bring multi-step questions to an assistant that can use
                    external tools.
                </p>
                <span class="agentic-welcome__example">
                    Example: Research a topic
                </span>
            </article>
            <article class="agentic-welcome__card">
                <h3 class="agentic-welcome__card-title">Your documents</h3>
                <p class="agentic-welcome__card-copy">
                    Upload a PDF and ask questions grounded in its contents.
                </p>
                <span class="agentic-welcome__example">
                    Example: Summarize this document
                </span>
            </article>
            <article class="agentic-welcome__card">
                <h3 class="agentic-welcome__card-title">You stay in control</h3>
                <p class="agentic-welcome__card-copy">
                    Review and approve actions when the workflow asks for
                    your confirmation.
                </p>
                <span class="agentic-welcome__example">
                    Example: Compare two options
                </span>
            </article>
        </div>
    </section>
    """


def hitl_card_html(prompt):
    return f"""
    <div class="agentic-hitl-card" role="alert" aria-live="assertive">
        <p class="agentic-hitl-card__heading">
            <span aria-hidden="true">🧑‍⚖️</span>
            <span>Human approval required</span>
        </p>
        <p class="agentic-hitl-card__prompt">{escape(prompt)}</p>
    </div>
    """
