import html
import streamlit as st


# ── helpers ──────────────────────────────────────────────────────────────────

def _e(text: str) -> str:
    """Escape text for safe HTML interpolation."""
    return html.escape(str(text or ""))


def _badge(label: str, color: str = "neutral") -> str:
    colors = {
        "green":  ("dbe7d7", "9eb495", "345139"),
        "blue":   ("d7e3f0", "8aaacf", "2a4a6b"),
        "purple": ("e8ddf0", "b89ecf", "4a2a6b"),
        "orange": ("f0e6d6", "c9a87a", "7a5230"),
        "neutral":("e8e4df", "c4bdb6", "6e665f"),
    }
    bg, border, fg = colors.get(color, colors["neutral"])
    return (
        f'<span style="font-size:0.75rem;padding:0.2rem 0.6rem;border-radius:999px;'
        f'background:#{bg};border:1px solid #{border};color:#{fg};'
        f'white-space:nowrap;">{_e(label)}</span>'
    )


def _card(title: str, body_html: str, accent: str = "#cdbfb0") -> None:
    st.markdown(
        f"""
        <div style="background:#f8f4ef;border:1.5px solid {accent};border-radius:14px;
                    padding:1.1rem 1.2rem;margin-bottom:0.9rem;">
            <div style="font-size:0.72rem;font-weight:700;letter-spacing:0.08em;
                        text-transform:uppercase;color:#8a7e76;margin-bottom:0.55rem;">
                {_e(title)}
            </div>
            {body_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


# ── result renderer ───────────────────────────────────────────────────────────

def _render_result(result: dict) -> None:
    content = result.get("content", {})

    # ── meta strip ──────────────────────────────────────────────────────────
    col_a, col_b, col_c, col_d = st.columns(4)
    with col_a:
        st.markdown(_badge(f"Agent: {result.get('agent', '—')}", "blue"), unsafe_allow_html=True)
    with col_b:
        ct = content.get("content_type", "post")
        color_map = {"post": "green", "carousel": "purple", "reel": "orange", "story": "neutral"}
        st.markdown(_badge(f"Type: {ct}", color_map.get(ct, "neutral")), unsafe_allow_html=True)
    with col_c:
        st.markdown(_badge(f"Tone: {content.get('tone', '—')}", "neutral"), unsafe_allow_html=True)
    with col_d:
        tin  = result.get("input_tokens", 0)
        tout = result.get("output_tokens", 0)
        st.markdown(_badge(f"{tin + tout} tokens", "neutral"), unsafe_allow_html=True)

    st.markdown("<div style='margin-top:1rem;'></div>", unsafe_allow_html=True)

    # ── hook (full width) ────────────────────────────────────────────────────
    hook = content.get("hook", "")
    if hook:
        st.markdown(
            f"""
            <div style="background:#2f2a26;border-radius:14px;padding:1.2rem 1.4rem;
                        margin-bottom:1rem;">
                <div style="font-size:0.7rem;letter-spacing:0.1em;text-transform:uppercase;
                            color:#a0958a;margin-bottom:0.4rem;">Hook</div>
                <div style="font-size:1.2rem;font-weight:700;color:#f5f1eb;
                            line-height:1.45;">{_e(hook)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ── caption | cta + hashtags ─────────────────────────────────────────────
    left, right = st.columns([3, 2])

    with left:
        caption = content.get("caption", "")
        caption_lines = _e(caption).replace("\n", "<br>")
        _card(
            "Caption",
            f'<div style="font-size:0.9rem;color:#2f2a26;line-height:1.65;">{caption_lines}</div>',
            accent="#9eb495",
        )

    with right:
        cta = content.get("call_to_action", "")
        _card(
            "Call to Action",
            f'<div style="font-size:0.92rem;font-weight:600;color:#2f2a26;">{_e(cta)}</div>',
            accent="#c9a87a",
        )

        hashtags = content.get("hashtags", [])
        if hashtags:
            pills = " ".join(
                f'<span style="display:inline-block;margin:0.2rem 0.15rem;padding:0.25rem 0.6rem;'
                f'border-radius:999px;background:#e0d8f0;border:1px solid #b8a8d8;'
                f'color:#4a3a6b;font-size:0.78rem;">{_e(tag)}</span>'
                for tag in hashtags
            )
            _card("Hashtags", f'<div style="line-height:2;">{pills}</div>', accent="#b89ecf")

    # ── post ideas ───────────────────────────────────────────────────────────
    ideas = content.get("post_ideas", [])
    if ideas:
        st.markdown(
            '<div style="font-size:0.72rem;font-weight:700;letter-spacing:0.08em;'
            'text-transform:uppercase;color:#8a7e76;margin:0.5rem 0 0.6rem 0;">Alternative Post Ideas</div>',
            unsafe_allow_html=True,
        )
        cols = st.columns(len(ideas))
        for col, idea in zip(cols, ideas):
            with col:
                st.markdown(
                    f"""
                    <div style="background:#f8f4ef;border:1px solid #cdbfb0;border-radius:12px;
                                padding:0.85rem 0.95rem;min-height:80px;">
                        <span style="font-size:0.82rem;color:#2f2a26;line-height:1.5;">{_e(idea)}</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    # ── carousel slides ──────────────────────────────────────────────────────
    carousel = content.get("carousel")
    if carousel and isinstance(carousel, dict):
        slides = carousel.get("slides", [])
        if slides:
            st.markdown(
                '<div style="font-size:0.72rem;font-weight:700;letter-spacing:0.08em;'
                'text-transform:uppercase;color:#8a7e76;margin:1rem 0 0.6rem 0;">'
                f'Carousel — {len(slides)} Slides</div>',
                unsafe_allow_html=True,
            )
            for slide in slides:
                num   = slide.get("slide", "")
                title = slide.get("title", "")
                text  = slide.get("text", "")
                is_first = num == 1
                is_last  = num == len(slides)
                accent = "#9eb495" if is_first else ("#c9a87a" if is_last else "#cdbfb0")
                st.markdown(
                    f"""
                    <div style="background:#f8f4ef;border:1.5px solid {accent};
                                border-radius:12px;padding:0.85rem 1rem;
                                margin-bottom:0.5rem;display:flex;gap:1rem;align-items:flex-start;">
                        <div style="min-width:28px;height:28px;border-radius:999px;
                                    background:#2f2a26;color:#f5f1eb;font-size:0.78rem;
                                    font-weight:700;display:flex;align-items:center;
                                    justify-content:center;">{_e(str(num))}</div>
                        <div>
                            <div style="font-weight:700;font-size:0.88rem;
                                        color:#2f2a26;margin-bottom:0.2rem;">{_e(title)}</div>
                            <div style="font-size:0.82rem;color:#6e655d;">{_e(text)}</div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    # ── reel section ─────────────────────────────────────────────────────────
    reel = content.get("reel")
    if reel and isinstance(reel, dict):
        st.markdown(
            '<div style="font-size:0.72rem;font-weight:700;letter-spacing:0.08em;'
            'text-transform:uppercase;color:#8a7e76;margin:1rem 0 0.6rem 0;">Reel Blueprint</div>',
            unsafe_allow_html=True,
        )
        r_left, r_right = st.columns(2)
        with r_left:
            _card("Opening Scene (0–3 sec)", f'<div style="font-size:0.88rem;color:#2f2a26;">{_e(reel.get("opening_scene",""))}</div>')
            beats_html = "".join(
                f'<div style="padding:0.3rem 0;border-bottom:1px solid #e8e4df;font-size:0.85rem;color:#2f2a26;">→ {_e(b)}</div>'
                for b in reel.get("script_beats", [])
            )
            _card("Script Beats", beats_html)
        with r_right:
            overlays_html = "".join(
                f'<div style="background:#e8ddf0;border:1px solid #b89ecf;border-radius:8px;'
                f'padding:0.35rem 0.65rem;margin-bottom:0.35rem;font-size:0.83rem;color:#4a2a6b;">{_e(o)}</div>'
                for o in reel.get("text_overlays", [])
            )
            _card("Text Overlays", overlays_html, accent="#b89ecf")
            _card("Audio Vibe", f'<div style="font-size:0.88rem;color:#2f2a26;">{_e(reel.get("audio_suggestion",""))}</div>')

    # ── strategy notes ───────────────────────────────────────────────────────
    notes = content.get("notes", "")
    if notes:
        st.markdown(
            f"""
            <div style="background:#f0e8d8;border:1px solid #c9a87a;border-radius:12px;
                        padding:0.85rem 1.1rem;margin-top:0.75rem;">
                <span style="font-size:0.72rem;font-weight:700;letter-spacing:0.08em;
                             text-transform:uppercase;color:#7a5230;">Strategy Note</span>
                <div style="font-size:0.85rem;color:#4d3820;margin-top:0.35rem;
                            line-height:1.55;">{_e(notes)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ── page entry point ──────────────────────────────────────────────────────────

def render_content_creator_page(orchestrator) -> None:
    st.markdown('<div class="page-title">Content Creator</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-subtitle">Instagram Content — Posts · Captions · Hooks · Carousels · Reels</div>',
        unsafe_allow_html=True,
    )

    # ── input form ───────────────────────────────────────────────────────────
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Brief</div>', unsafe_allow_html=True)

    example_tasks = [
        "Create an Instagram post for a luxury hotel launching a new spa experience",
        "Write a carousel for a fitness coach: 5 morning habits that double your energy",
        "Create a reel script for a sustainable fashion brand, Gen Z audience",
        "Write a caption for a coffee shop's new seasonal menu",
        "Generate hashtags and a hook for a tech startup's product launch post",
    ]

    task_input = st.text_area(
        "Describe the content you need",
        placeholder="e.g. Create an Instagram carousel for a skincare brand about their new vitamin C serum — professional but approachable tone",
        height=120,
        key="cc_task_input",
        label_visibility="collapsed",
    )

    with st.expander("Quick examples — click to copy"):
        for ex in example_tasks:
            if st.button(ex, key=f"cc_ex_{ex[:30]}"):
                st.session_state["cc_task_input"] = ex
                st.rerun()

    run_clicked = st.button("Generate Content", key="cc_run")
    st.markdown("</div>", unsafe_allow_html=True)

    # ── run ──────────────────────────────────────────────────────────────────
    if run_clicked:
        if not task_input.strip():
            st.warning("Please enter a brief first.")
            return

        with st.spinner("Generating content..."):
            result = orchestrator.handle_task(task_input.strip())

        if result.get("status") == "error":
            st.error(f"Error: {result.get('message')}")
            return

        agent_used = result.get("selected_agent", "—")
        if agent_used != "zina_content_creator_agent":
            st.info(
                f"Task was routed to **{agent_used}** — try adding keywords like "
                f'"instagram", "post", "caption", "carousel" or "reel" to your brief.',
                icon="ℹ️",
            )

        st.markdown(
            '<div style="height:1px;background:#cdbfb0;margin:1.2rem 0;"></div>',
            unsafe_allow_html=True,
        )

        _render_result(result["result"])

        with st.expander("Raw JSON output"):
            st.json(result)
