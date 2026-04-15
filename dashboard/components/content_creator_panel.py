"""
Content Creator Panel — v3

Added in this version:
- _format_export()   : formats hook/caption/cta/hashtags into one clean block
- _format_canva()    : formats carousel slides for direct Canva paste
- _render_actions()  : action bar — Export Full Post, Download .txt,
                       Turn into Reel Script, Canva Mode toggle
- st.download_button for zina_post_{brand}_{type}.txt
- "Turn into Reel Script" re-sends content through the orchestrator
- Canva Mode: shows carousel as plain "Slide N:" paste format
- Session-state: cc_export_open, cc_canva_mode, cc_reel_result
"""

import html
import json as _json
from typing import Optional
import streamlit as st

# ─── constants ────────────────────────────────────────────────────────────────

_CONTENT_TYPES = ["Auto-detect", "Post", "Carousel", "Reel", "Story"]
_TONES         = ["Auto-detect", "Casual", "Professional", "Inspirational", "Educational", "Humorous"]

_VARIANT_ANGLES = [
    "Creative angle: emotional storytelling — connect with the audience's real pain points and aspirations. Make them feel seen.",
    "Creative angle: bold and benefit-driven — lead with the strongest transformation or product claim. Be specific and concrete.",
    "Creative angle: unexpected or provocative — challenge a common assumption in this niche. Make people stop and think.",
]

_EXAMPLES = [
    "New spa experience at a luxury hotel — focus on escapism and self-care",
    "Fitness coach: 5 morning habits that double energy levels",
    "Sustainable fashion brand targeting Gen Z — new summer collection drop",
    "Coffee shop's new seasonal autumn menu launch",
    "Tech startup product launch — AI-powered productivity tool for remote teams",
]

# ─── helpers ──────────────────────────────────────────────────────────────────

def _e(text: str) -> str:
    return html.escape(str(text or ""))

def _badge(label: str, color: str = "neutral") -> str:
    palettes = {
        "green":   ("dbe7d7", "9eb495", "345139"),
        "blue":    ("d7e3f0", "8aaacf", "2a4a6b"),
        "purple":  ("e8ddf0", "b89ecf", "4a2a6b"),
        "orange":  ("f0e6d6", "c9a87a", "7a5230"),
        "neutral": ("e8e4df", "c4bdb6", "6e665f"),
    }
    bg, bd, fg = palettes.get(color, palettes["neutral"])
    return (
        f'<span style="font-size:0.75rem;padding:0.2rem 0.65rem;border-radius:999px;'
        f'background:#{bg};border:1px solid #{bd};color:#{fg};white-space:nowrap;">'
        f'{_e(label)}</span>'
    )

def _section_label(text: str) -> None:
    st.markdown(
        f'<div style="font-size:0.7rem;font-weight:700;letter-spacing:0.09em;'
        f'text-transform:uppercase;color:#8a7e76;margin-bottom:0.35rem;">{_e(text)}</div>',
        unsafe_allow_html=True,
    )

def _divider() -> None:
    st.markdown(
        '<div style="height:1px;background:#d7cbbf;margin:1.4rem 0;"></div>',
        unsafe_allow_html=True,
    )

def _copy_block(text: str) -> None:
    st.code(text, language=None)


# ─── formatters ───────────────────────────────────────────────────────────────

def _format_export(hook: str, caption: str, cta: str, hashtags: list) -> str:
    """One clean text block ready to paste anywhere."""
    tag_line = " ".join(hashtags) if hashtags else ""
    return (
        "---\n"
        f"HOOK:\n{hook}\n\n"
        f"CAPTION:\n{caption}\n\n"
        f"CTA:\n{cta}\n\n"
        f"HASHTAGS:\n{tag_line}\n"
        "---"
    )

def _format_canva(slides: list) -> str:
    """Carousel slides formatted for direct Canva paste."""
    lines = []
    for s in slides:
        num   = s.get("slide", "")
        title = s.get("title", "")
        text  = s.get("text", "")
        lines.append(f"Slide {num}:\n{title}\n{text}")
    return "\n\n".join(lines)

def _safe_filename(brand: str, ct: str) -> str:
    safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in brand.lower().strip())
    safe = safe[:30] or "brand"
    return f"zina_post_{safe}_{ct}.txt"


# ─── prompt builder ───────────────────────────────────────────────────────────

def _build_prompt(
    brief:        str,
    brand:        str,
    content_type: str,
    tone:         str,
    goal:         str,
    angle:        Optional[str] = None,
) -> str:
    ct   = content_type if content_type != "Auto-detect" else None
    tn   = tone         if tone         != "Auto-detect" else None
    task = ct or "instagram content"

    parts = [f"Create {task.lower()} for {brand.strip() or 'my brand'}."]
    parts.append(f"\nBrief: {brief.strip()}")
    if tn:
        parts.append(f"Tone: {tn}")
    if goal.strip():
        parts.append(f"Goal / CTA focus: {goal.strip()}")
    if angle:
        parts.append(f"\n{angle}")
    return "\n".join(parts)


def _build_pack_prompt(
    brief:     str,
    brand:     str,
    tone:      str,
    goal:      str,
    mode:      str,        # "3 Posts" | "5 Posts" | "Weekly Pack"
) -> str:
    _pt_map   = {"3 Posts": "3_posts", "5 Posts": "5_posts", "Weekly Pack": "weekly"}
    _cnt_map  = {"3 Posts": 3,         "5 Posts": 5,         "Weekly Pack": 7}
    pt    = _pt_map[mode]
    count = _cnt_map[mode]
    tn    = tone if tone != "Auto-detect" else None

    parts = [f"Generate a {pt} content pack for {brand.strip() or 'my brand'}."]
    parts.append(f"\nBrief: {brief.strip()}")
    parts.append(f"Pack type: {pt} — generate exactly {count} posts.")
    if tn:
        parts.append(f"Preferred tone: {tn} (vary tones across posts for variety)")
    if goal.strip():
        parts.append(f"Goal / CTA focus: {goal.strip()}")
    return "\n".join(parts)


def _format_pack_download(posts: list, brand: str, pack_type: str) -> str:
    """Entire pack formatted as a single downloadable .txt file."""
    pt_labels = {
        "3_posts": "3 Posts",
        "5_posts": "5 Posts",
        "weekly":  "Weekly Pack (7 Days)",
    }
    header = (
        f"ZINA CONTENT PACK — {brand or 'General'}\n"
        f"{pt_labels.get(pack_type, pack_type)}  |  {len(posts)} posts\n"
        f"{'=' * 48}\n\n"
    )
    _canva_fields = [
        ("Cover Title",    "cover_title"),
        ("Cover Subtitle", "cover_subtitle"),
        ("Slide 1 Title",  "slide_1_title"),
        ("Slide 1 Body",   "slide_1_text"),
        ("Slide 2 Title",  "slide_2_title"),
        ("Slide 2 Body",   "slide_2_text"),
        ("Slide 3 Title",  "slide_3_title"),
        ("Slide 3 Body",   "slide_3_text"),
        ("CTA Slide",      "cta"),
        ("Image Prompt",   "image_prompt"),
    ]
    blocks = []
    for i, post in enumerate(posts):
        weekly = bool(post.get("day_label"))
        title  = post.get("day_label", f"Post {i + 1}") if weekly else f"Post {i + 1}"
        ct     = post.get("content_type", "post")
        tone   = post.get("tone", "")
        lines  = [
            f"{'─' * 48}",
            f"{title.upper()}",
            f"Type: {ct}  |  Tone: {tone}",
            f"{'─' * 48}",
            f"\nHOOK:\n{post.get('hook', '')}",
            f"\nCAPTION:\n{post.get('caption', '')}",
            f"\nCTA:\n{post.get('call_to_action', '')}",
            f"\nHASHTAGS:\n{' '.join(post.get('hashtags', []))}",
        ]
        canva = post.get("canva")
        if canva and isinstance(canva, dict):
            lines.append("\nCANVA:")
            for label, key in _canva_fields:
                val = canva.get(key, "")
                if val:
                    lines.append(f"  {label}: {val}")
        blocks.append("\n".join(lines))
    return header + "\n\n".join(blocks)


# ─── individual result blocks ──────────────────────────────────────────────────

def _render_meta(result: dict, content: dict) -> None:
    ct        = content.get("content_type", "post")
    ct_colors = {"post": "green", "carousel": "purple", "reel": "orange", "story": "neutral"}
    tin  = result.get("input_tokens", 0)
    tout = result.get("output_tokens", 0)
    cols = st.columns(5)
    for html_str, col in [
        (_badge(f"Agent: {result.get('agent','—')}",  "blue"),             cols[0]),
        (_badge(f"Brand: {content.get('brand','—')}",  "neutral"),         cols[1]),
        (_badge(f"Type: {ct}", ct_colors.get(ct,"neutral")),               cols[2]),
        (_badge(f"Tone: {content.get('tone','—')}",    "neutral"),         cols[3]),
        (_badge(f"{tin + tout} tokens",                "neutral"),         cols[4]),
    ]:
        with col:
            st.markdown(html_str, unsafe_allow_html=True)
    st.markdown("<div style='margin-top:0.8rem;'></div>", unsafe_allow_html=True)


def _render_hook(hook: str) -> None:
    if not hook:
        return
    st.markdown(
        f"""
        <div style="background:#2f2a26;border-radius:14px;padding:1.3rem 1.5rem;margin-bottom:0.4rem;">
            <div style="font-size:0.68rem;letter-spacing:0.1em;text-transform:uppercase;
                        color:#a0958a;margin-bottom:0.4rem;">Hook</div>
            <div style="font-size:1.25rem;font-weight:700;color:#f5f1eb;line-height:1.45;">
                {_e(hook)}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    _section_label("copy hook")
    _copy_block(hook)


def _render_caption(caption: str) -> None:
    if not caption:
        return
    lines = _e(caption).replace("\n", "<br>")
    st.markdown(
        f"""
        <div style="background:#f8f4ef;border:1.5px solid #9eb495;border-radius:14px;
                    padding:1.1rem 1.2rem;margin-bottom:0.4rem;">
            <div style="font-size:0.68rem;font-weight:700;letter-spacing:0.09em;
                        text-transform:uppercase;color:#8a7e76;margin-bottom:0.55rem;">Caption</div>
            <div style="font-size:0.9rem;color:#2f2a26;line-height:1.7;">{lines}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    _section_label("copy caption")
    _copy_block(caption)


def _render_cta(cta: str) -> None:
    if not cta:
        return
    st.markdown(
        f"""
        <div style="background:#f8f4ef;border:1.5px solid #c9a87a;border-radius:14px;
                    padding:1rem 1.2rem;margin-bottom:0.4rem;">
            <div style="font-size:0.68rem;font-weight:700;letter-spacing:0.09em;
                        text-transform:uppercase;color:#8a7e76;margin-bottom:0.45rem;">Call to Action</div>
            <div style="font-size:0.92rem;font-weight:600;color:#2f2a26;">{_e(cta)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    _section_label("copy cta")
    _copy_block(cta)


def _render_hashtags(hashtags: list) -> None:
    if not hashtags:
        return
    pills = " ".join(
        f'<span style="display:inline-block;margin:0.2rem 0.15rem;padding:0.22rem 0.55rem;'
        f'border-radius:999px;background:#e0d8f0;border:1px solid #b8a8d8;'
        f'color:#4a3a6b;font-size:0.77rem;">{_e(tag)}</span>'
        for tag in hashtags
    )
    st.markdown(
        f"""
        <div style="background:#f8f4ef;border:1.5px solid #b89ecf;border-radius:14px;
                    padding:1rem 1.2rem;margin-bottom:0.4rem;">
            <div style="font-size:0.68rem;font-weight:700;letter-spacing:0.09em;
                        text-transform:uppercase;color:#8a7e76;margin-bottom:0.5rem;">
                Hashtags ({len(hashtags)})
            </div>
            <div style="line-height:2.1;">{pills}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    _section_label("copy all hashtags")
    _copy_block(" ".join(hashtags))


def _render_ideas(ideas: list) -> None:
    if not ideas:
        return
    _section_label("Alternative Post Ideas")
    cols = st.columns(len(ideas))
    for col, idea in zip(cols, ideas):
        with col:
            st.markdown(
                f"""
                <div style="background:#f8f4ef;border:1px solid #cdbfb0;border-radius:12px;
                            padding:0.85rem 0.95rem;min-height:90px;">
                    <div style="font-size:0.82rem;color:#2f2a26;line-height:1.55;">{_e(idea)}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def _render_carousel(carousel: Optional[dict], canva_mode: bool = False) -> None:
    if not carousel or not isinstance(carousel, dict):
        return
    slides = carousel.get("slides", [])
    if not slides:
        return

    with st.expander(f"Carousel — {len(slides)} Slides", expanded=True):
        if canva_mode:
            _section_label("Canva Ready — paste directly")
            _copy_block(_format_canva(slides))
        else:
            for slide in slides:
                num    = slide.get("slide", "")
                title  = slide.get("title", "")
                text   = slide.get("text", "")
                n      = int(num) if str(num).isdigit() else 0
                accent = "#9eb495" if n == 1 else ("#c9a87a" if n == len(slides) else "#cdbfb0")
                st.markdown(
                    f"""
                    <div style="background:#f8f4ef;border:1.5px solid {accent};border-radius:12px;
                                padding:0.8rem 1rem;margin-bottom:0.45rem;
                                display:flex;gap:1rem;align-items:flex-start;">
                        <div style="min-width:26px;height:26px;border-radius:999px;background:#2f2a26;
                                    color:#f5f1eb;font-size:0.76rem;font-weight:700;
                                    display:flex;align-items:center;justify-content:center;
                                    flex-shrink:0;">{_e(str(num))}</div>
                        <div>
                            <div style="font-weight:700;font-size:0.87rem;color:#2f2a26;
                                        margin-bottom:0.18rem;">{_e(title)}</div>
                            <div style="font-size:0.81rem;color:#6e655d;">{_e(text)}</div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


def _render_reel(reel: Optional[dict]) -> None:
    if not reel or not isinstance(reel, dict):
        return
    with st.expander("Reel Blueprint", expanded=True):
        c1, c2 = st.columns(2)
        with c1:
            _section_label("Opening Scene (0–3 sec)")
            st.markdown(
                f'<div style="background:#f8f4ef;border:1px solid #cdbfb0;border-radius:10px;'
                f'padding:0.8rem;font-size:0.87rem;color:#2f2a26;margin-bottom:0.8rem;">'
                f'{_e(reel.get("opening_scene",""))}</div>',
                unsafe_allow_html=True,
            )
            _section_label("Script Beats")
            for beat in reel.get("script_beats", []):
                st.markdown(
                    f'<div style="padding:0.32rem 0;border-bottom:1px solid #e8e4df;'
                    f'font-size:0.84rem;color:#2f2a26;">→ {_e(beat)}</div>',
                    unsafe_allow_html=True,
                )
        with c2:
            _section_label("Text Overlays")
            for ov in reel.get("text_overlays", []):
                st.markdown(
                    f'<div style="background:#e8ddf0;border:1px solid #b89ecf;border-radius:8px;'
                    f'padding:0.32rem 0.65rem;margin-bottom:0.3rem;font-size:0.82rem;color:#4a2a6b;">'
                    f'{_e(ov)}</div>',
                    unsafe_allow_html=True,
                )
            st.markdown("<div style='margin-top:0.5rem;'></div>", unsafe_allow_html=True)
            _section_label("Audio Vibe")
            st.markdown(
                f'<div style="background:#f8f4ef;border:1px solid #cdbfb0;border-radius:10px;'
                f'padding:0.7rem;font-size:0.86rem;color:#2f2a26;">'
                f'{_e(reel.get("audio_suggestion",""))}</div>',
                unsafe_allow_html=True,
            )


def _render_canva_export(canva: Optional[dict], show_header: bool = True) -> None:
    """Structured Canva export block — one copy-ready field per slide.

    show_header=False skips the section title and leading divider,
    useful when called inside an already-labelled expander.
    """
    if not canva or not isinstance(canva, dict):
        return

    if show_header:
        _divider()
        st.markdown(
            '<div style="font-size:1rem;font-weight:700;color:#2f2a26;margin-bottom:0.2rem;">'
            'Canva Export</div>'
            '<div style="font-size:0.8rem;color:#8a7e76;margin-bottom:1rem;">'
            'Copy each field directly into your Canva template</div>',
            unsafe_allow_html=True,
        )

    # ── field definitions: (label, key, accent_color) ────────────────────────
    fields = [
        ("Cover Title",    "cover_title",    "#9eb495"),
        ("Cover Subtitle", "cover_subtitle", "#9eb495"),
        ("Slide 1 — Title", "slide_1_title", "#b89ecf"),
        ("Slide 1 — Body",  "slide_1_text",  "#b89ecf"),
        ("Slide 2 — Title", "slide_2_title", "#b89ecf"),
        ("Slide 2 — Body",  "slide_2_text",  "#b89ecf"),
        ("Slide 3 — Title", "slide_3_title", "#b89ecf"),
        ("Slide 3 — Body",  "slide_3_text",  "#b89ecf"),
        ("CTA Slide",       "cta",           "#c9a87a"),
        ("Image Prompt",    "image_prompt",  "#8aaacf"),
    ]

    for label, key, accent in fields:
        value = canva.get(key, "")
        if not value:
            continue
        st.markdown(
            f"""
            <div style="background:#f8f4ef;border-left:3px solid {accent};border-radius:0 10px 10px 0;
                        padding:0.7rem 1rem;margin-bottom:0.3rem;">
                <div style="font-size:0.67rem;font-weight:700;letter-spacing:0.09em;
                            text-transform:uppercase;color:#8a7e76;margin-bottom:0.25rem;">
                    {_e(label)}
                </div>
                <div style="font-size:0.88rem;color:#2f2a26;line-height:1.55;">{_e(value)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        _copy_block(value)

    # ── single "copy all" block ───────────────────────────────────────────────
    _divider()
    _section_label("Copy all Canva data — paste into any doc or template")
    all_lines = []
    for label, key, _ in fields:
        value = canva.get(key, "")
        if value:
            all_lines.append(f"{label.upper()}:\n{value}")
    if all_lines:
        _copy_block("\n\n".join(all_lines))


def _render_notes(notes: str) -> None:
    if not notes:
        return
    st.markdown(
        f"""
        <div style="background:#f0e8d8;border:1px solid #c9a87a;border-radius:12px;
                    padding:0.85rem 1.1rem;margin-top:0.6rem;">
            <div style="font-size:0.68rem;font-weight:700;letter-spacing:0.09em;
                        text-transform:uppercase;color:#7a5230;margin-bottom:0.3rem;">
                Strategy Note
            </div>
            <div style="font-size:0.85rem;color:#4d3820;line-height:1.6;">{_e(notes)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ─── pack renderers ───────────────────────────────────────────────────────────

_CT_COLORS = {"post": "green", "carousel": "purple", "reel": "orange", "story": "neutral"}


def _render_pack_post(post: dict, index: int, weekly: bool = False) -> None:
    """Render a single post from a content pack."""
    ct   = post.get("content_type", "post")
    tone = post.get("tone", "")

    label = post.get("day_label", f"Post {index + 1}") if weekly else f"Post {index + 1}"
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(_badge(label, "blue"), unsafe_allow_html=True)
    with c2:
        st.markdown(_badge(f"Type: {ct}", _CT_COLORS.get(ct, "neutral")), unsafe_allow_html=True)
    with c3:
        st.markdown(_badge(f"Tone: {tone}", "neutral"), unsafe_allow_html=True)
    st.markdown("<div style='margin-top:0.6rem;'></div>", unsafe_allow_html=True)

    _render_hook(post.get("hook", ""))

    left, right = st.columns([3, 2])
    with left:
        _render_caption(post.get("caption", ""))
    with right:
        _render_cta(post.get("call_to_action", ""))
        _render_hashtags(post.get("hashtags", []))

    canva = post.get("canva")
    if canva and isinstance(canva, dict):
        with st.expander("Canva Export", expanded=False):
            _render_canva_export(canva, show_header=False)


def _render_pack(pack_result: dict) -> None:
    """Render a full content pack: summary badges, download, and per-post tabs."""
    posts     = pack_result.get("posts", [])
    pack_type = pack_result.get("pack_type", "")
    brand     = pack_result.get("brand", "")
    weekly    = pack_type == "weekly"
    tin       = pack_result.get("input_tokens", 0)
    tout      = pack_result.get("output_tokens", 0)

    if not posts:
        st.warning("Pack was generated but contains no posts — try again with a more specific brief.")
        return

    # ── summary badges ────────────────────────────────────────────────────────
    pt_label = {"3_posts": "3 Posts", "5_posts": "5 Posts", "weekly": "Weekly Pack"}.get(pack_type, pack_type)
    mc1, mc2, mc3, mc4 = st.columns(4)
    with mc1:
        st.markdown(_badge(f"Brand: {brand or '—'}", "blue"), unsafe_allow_html=True)
    with mc2:
        st.markdown(_badge(pt_label, "green"), unsafe_allow_html=True)
    with mc3:
        st.markdown(_badge(f"{len(posts)} posts", "neutral"), unsafe_allow_html=True)
    with mc4:
        st.markdown(_badge(f"{tin + tout} tokens", "neutral"), unsafe_allow_html=True)
    st.markdown("<div style='margin-top:0.8rem;'></div>", unsafe_allow_html=True)

    # ── download full pack ────────────────────────────────────────────────────
    pack_txt   = _format_pack_download(posts, brand, pack_type)
    safe_brand = "".join(c if c.isalnum() or c in "-_" else "_" for c in brand.lower().strip())[:30] or "brand"
    filename   = f"zina_pack_{safe_brand}_{pack_type}.txt"
    st.download_button(
        label="Download Full Pack .txt",
        data=pack_txt.encode("utf-8"),
        file_name=filename,
        mime="text/plain",
        key="cc_pack_dl",
    )

    # ── per-post tabs ─────────────────────────────────────────────────────────
    if weekly:
        tab_labels = [p.get("day_label", f"Day {i + 1}") for i, p in enumerate(posts)]
    else:
        tab_labels = [f"Post {i + 1}" for i in range(len(posts))]

    tabs = st.tabs(tab_labels)
    for i, (tab, post) in enumerate(zip(tabs, posts)):
        with tab:
            _render_pack_post(post, i, weekly=weekly)


# ─── action bar ───────────────────────────────────────────────────────────────

def _render_actions(content: dict, orchestrator) -> None:
    """
    Action bar rendered below the main result.
    Buttons: Export Full Post · Download .txt · Reel Script · Canva Mode
    """
    _divider()

    hook     = content.get("hook", "")
    caption  = content.get("caption", "")
    cta      = content.get("call_to_action", "")
    hashtags = content.get("hashtags", [])
    carousel = content.get("carousel")
    brand    = content.get("brand", "brand")
    ct       = content.get("content_type", "post")

    export_text = _format_export(hook, caption, cta, hashtags)
    filename    = _safe_filename(brand, ct)

    # ── button row ────────────────────────────────────────────────────────────
    _section_label("Actions")
    b1, b2, b3, b4 = st.columns(4)

    with b1:
        if st.button("Export Full Post", key="cc_act_export", use_container_width=True):
            st.session_state["cc_export_open"] = not st.session_state.get("cc_export_open", False)

    with b2:
        st.download_button(
            label="Download .txt",
            data=export_text.encode("utf-8"),
            file_name=filename,
            mime="text/plain",
            key="cc_act_dl",
            use_container_width=True,
        )

    with b3:
        reel_clicked = st.button("Reel Script", key="cc_act_reel", use_container_width=True)

    with b4:
        canva_mode = st.checkbox(
            "Canva Mode",
            key="cc_canva_mode",
            help="Formats carousel slides for direct Canva paste",
        )

    # ── export block ──────────────────────────────────────────────────────────
    if st.session_state.get("cc_export_open"):
        st.markdown("<div style='margin-top:0.7rem;'></div>", unsafe_allow_html=True)
        _section_label("Full Post — click the copy icon top-right")
        _copy_block(export_text)

    # ── canva mode output ─────────────────────────────────────────────────────
    if canva_mode and carousel and isinstance(carousel, dict):
        slides = carousel.get("slides", [])
        if slides:
            st.markdown("<div style='margin-top:0.7rem;'></div>", unsafe_allow_html=True)
            _section_label("Canva Paste Format — copy and paste into Canva text fields")
            _copy_block(_format_canva(slides))

    # ── reel script generation ────────────────────────────────────────────────
    if reel_clicked:
        reel_prompt = (
            f"Turn this Instagram post into a short reel script (under 30 seconds).\n\n"
            f"Original hook: {hook}\n"
            f"Original caption: {caption}\n\n"
            f"Brand: {brand}. Tone: {content.get('tone', 'casual')}.\n\n"
            f"Return as reel content_type with opening_scene, script_beats, "
            f"text_overlays, and audio_suggestion."
        )
        with st.spinner("Generating reel script…"):
            raw = orchestrator.handle_task(reel_prompt)
        if raw.get("status") == "success":
            st.session_state["cc_reel_result"] = raw["result"]
        else:
            st.error(f"Reel generation failed: {raw.get('message', '—')}")

    reel_result = st.session_state.get("cc_reel_result")
    if reel_result:
        _divider()
        _section_label("Reel Script")
        rc = reel_result.get("content", {})
        _render_hook(rc.get("hook", ""))
        _render_reel(rc.get("reel"))
        # Fallback: if no reel structure was returned, show caption as script text
        if not rc.get("reel") and rc.get("caption"):
            _render_caption(rc.get("caption", ""))
        if st.button("Clear Reel Script", key="cc_clear_reel"):
            st.session_state["cc_reel_result"] = None
            st.rerun()


# ─── result: full view ────────────────────────────────────────────────────────

def _render_result(result: dict, compact: bool = False, canva_mode: bool = False) -> None:
    """
    compact=True  → Hook + Caption + CTA + Hashtags only (variant tabs)
    compact=False → full view incl. ideas, carousel, reel, notes
    canva_mode    → passed to _render_carousel to switch display format
    """
    content = result.get("content", {})

    if not compact:
        _render_meta(result, content)

    _render_hook(content.get("hook", ""))

    left, right = st.columns([3, 2])
    with left:
        _render_caption(content.get("caption", ""))
    with right:
        _render_cta(content.get("call_to_action", ""))
        _render_hashtags(content.get("hashtags", []))

    if not compact:
        _divider()
        _render_ideas(content.get("post_ideas", []))
        _render_carousel(content.get("carousel"), canva_mode=canva_mode)
        _render_reel(content.get("reel"))
        _render_notes(content.get("notes", ""))
        _render_canva_export(content.get("canva"))


# ─── input form ───────────────────────────────────────────────────────────────

def _render_form():
    """Structured input form. Returns (brief, brand, content_type, tone, goal, mode, run_clicked, var_clicked)."""
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Brief</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns([2, 1, 1])
    with c1:
        brand = st.text_input("Brand / Marke", placeholder="e.g. Nike, my coffee shop …", key="cc_brand")
    with c2:
        content_type = st.selectbox("Content Type", _CONTENT_TYPES, key="cc_content_type")
    with c3:
        tone = st.selectbox("Tone", _TONES, key="cc_tone")

    goal = st.text_input(
        "Goal / CTA focus (optional)",
        placeholder="e.g. drive app downloads, grow email list …",
        key="cc_goal",
    )
    brief = st.text_area(
        "Brief — describe the content",
        placeholder=(
            "e.g. Launching a new vitamin C serum. Target: women 28–45. "
            "Key benefit: visible glow in 7 days."
        ),
        height=120,
        key="cc_brief",
    )

    with st.expander("Quick examples"):
        for ex in _EXAMPLES:
            if st.button(ex, key=f"cc_ex_{hash(ex)}"):
                st.session_state["cc_brief"] = ex
                st.rerun()

    st.markdown("<div style='margin:0.8rem 0 0.3rem;'></div>", unsafe_allow_html=True)
    _section_label("Generation Mode")
    mode = st.radio(
        "generation_mode",
        ["Single Post", "3 Posts", "5 Posts", "Weekly Pack"],
        horizontal=True,
        key="cc_mode",
        label_visibility="collapsed",
    )

    if mode == "Single Post":
        b1, b2, _ = st.columns([1, 1, 2])
        with b1:
            run_clicked = st.button("Generate Content", key="cc_generate_btn", use_container_width=True)
        with b2:
            var_clicked = st.button("Generate 3 Versions", key="cc_variants_btn", use_container_width=True)
    else:
        b1, _ = st.columns([1, 3])
        with b1:
            run_clicked = st.button(f"Generate {mode}", key="cc_generate_btn", use_container_width=True)
        var_clicked = False

    st.markdown("</div>", unsafe_allow_html=True)
    return brief, brand, content_type, tone, goal, mode, run_clicked, var_clicked


# ─── page entry point ─────────────────────────────────────────────────────────

def render_content_creator_page(orchestrator) -> None:
    # ── session state ────────────────────────────────────────────────────────
    defaults = {
        "cc_main_result":   None,
        "cc_variants_data": [],
        "cc_export_open":   False,
        "cc_reel_result":   None,
        "cc_pack_result":   None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

    # ── header ───────────────────────────────────────────────────────────────
    st.markdown('<div class="page-title">Content Creator</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-subtitle">'
        'Instagram Content — Posts · Captions · Hooks · Carousels · Reels'
        '</div>',
        unsafe_allow_html=True,
    )

    # ── form ─────────────────────────────────────────────────────────────────
    brief, brand, content_type, tone, goal, mode, run_clicked, var_clicked = _render_form()

    def _validate() -> bool:
        if not brief.strip():
            st.warning("Please fill in the Brief field.")
            return False
        return True

    # ── generate single post ─────────────────────────────────────────────────
    if run_clicked and mode == "Single Post" and _validate():
        prompt = _build_prompt(brief, brand, content_type, tone, goal)
        with st.spinner("Generating content…"):
            raw = orchestrator.handle_task(prompt)
        if raw.get("status") == "error":
            st.error(f"Agent error: {raw.get('message')}")
        else:
            st.session_state["cc_main_result"]   = raw
            st.session_state["cc_variants_data"] = []
            st.session_state["cc_reel_result"]   = None
            st.session_state["cc_pack_result"]   = None

    # ── generate content pack ─────────────────────────────────────────────────
    if run_clicked and mode != "Single Post" and _validate():
        _pt_map  = {"3 Posts": "3_posts", "5 Posts": "5_posts", "Weekly Pack": "weekly"}
        _cnt_map = {"3 Posts": 3, "5 Posts": 5, "Weekly Pack": 7}
        pt    = _pt_map[mode]
        count = _cnt_map[mode]

        prompt = _build_pack_prompt(brief, brand, tone, goal, mode)
        with st.spinner(f"Generating {mode.lower()} ({count} posts)…"):
            agent = orchestrator.registry.get_agent("zina_content_creator_agent")
            if agent is None:
                st.error("Content Creator agent not found in registry.")
            else:
                pack_result = agent.run_pack(prompt, count=count, pack_type=pt)
                if pack_result.get("posts"):
                    st.session_state["cc_pack_result"]   = pack_result
                    st.session_state["cc_main_result"]   = None
                    st.session_state["cc_variants_data"] = []
                    st.session_state["cc_reel_result"]   = None
                else:
                    err = pack_result.get("parse_error", "No posts returned")
                    st.error(f"Pack generation failed: {err}. Try a more specific brief.")

    # ── generate 3 variants ───────────────────────────────────────────────────
    if var_clicked and _validate():
        variants = []
        bar = st.progress(0, text="Generating variant 1 of 3…")
        for i, angle in enumerate(_VARIANT_ANGLES):
            bar.progress((i + 1) / 3, text=f"Generating variant {i+1} of 3…")
            raw = orchestrator.handle_task(_build_prompt(brief, brand, content_type, tone, goal, angle=angle))
            if raw.get("status") == "success":
                variants.append(raw)
        bar.empty()
        st.session_state["cc_variants_data"] = variants
        st.session_state["cc_pack_result"]   = None
        if not st.session_state["cc_main_result"] and variants:
            st.session_state["cc_main_result"] = variants[0]

    # ── display main result ───────────────────────────────────────────────────
    main = st.session_state["cc_main_result"]
    if main:
        _divider()
        agent_used = main.get("selected_agent", "")
        if agent_used and agent_used != "zina_content_creator_agent":
            st.info(
                f"Routed to **{agent_used}** — add keywords like "
                '"instagram", "carousel", "reel" or "caption" to your brief.',
                icon="ℹ️",
            )

        canva_mode = st.session_state.get("cc_canva_mode", False)
        _render_result(main["result"], compact=False, canva_mode=canva_mode)

        # ── action bar ───────────────────────────────────────────────────────
        _render_actions(main["result"]["content"], orchestrator)

    # ── display pack ─────────────────────────────────────────────────────────
    pack = st.session_state.get("cc_pack_result")
    if pack:
        _divider()
        pt_label = {"3_posts": "3 Posts", "5_posts": "5 Posts", "weekly": "Weekly Pack"}.get(
            pack.get("pack_type", ""), "Content Pack"
        )
        st.markdown(
            f'<div class="section-title">{pt_label}</div>',
            unsafe_allow_html=True,
        )
        _render_pack(pack)

    # ── display variants ─────────────────────────────────────────────────────
    variants = st.session_state["cc_variants_data"]
    if variants:
        _divider()
        st.markdown('<div class="section-title">3 Versions</div>', unsafe_allow_html=True)
        tabs = st.tabs([f"Version {i+1}" for i in range(len(variants))])
        labels = ["Emotional Storytelling", "Bold & Benefit-Driven", "Unexpected / Provocative"]
        for tab, variant, label in zip(tabs, variants, labels):
            with tab:
                c = variant["result"].get("content", {})
                ct_val = c.get("content_type", "post")
                ct_col = {"post": "green", "carousel": "purple", "reel": "orange"}.get(ct_val, "neutral")
                mc1, mc2, mc3 = st.columns(3)
                with mc1: st.markdown(_badge(f"Angle: {label}",          "blue"),    unsafe_allow_html=True)
                with mc2: st.markdown(_badge(f"Type: {ct_val}",          ct_col),    unsafe_allow_html=True)
                with mc3: st.markdown(_badge(f"Tone: {c.get('tone','—')}","neutral"), unsafe_allow_html=True)
                st.markdown("<div style='margin-top:0.6rem;'></div>", unsafe_allow_html=True)
                _render_result(variant["result"], compact=True)
