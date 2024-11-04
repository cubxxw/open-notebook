from typing import Optional

import streamlit as st
from humanize import naturaltime
from loguru import logger
from streamlit_monaco import st_monaco  # type: ignore

from open_notebook.domain.notebook import Note
from open_notebook.graphs.multipattern import graph as pattern_graph
from open_notebook.utils import surreal_clean

from .consts import context_icons


@st.dialog("Write a Note", width="large")
def add_note(notebook_id):
    note_title = st.text_input("Title")
    note_content = st.text_area("Content")
    if st.button("Save", key="add_note"):
        logger.debug("Adding note")
        note = Note(title=note_title, content=note_content, note_type="human")
        note.save()
        note.add_to_notebook(notebook_id)
        st.rerun()


@st.dialog("Add a Source", width="large")
def note_panel(notebook_id=None, note: Optional[Note] = None):
    if not note:
        note: Note = Note(note_type="human")

    t_preview, t_edit = st.tabs(["Preview", "Edit"])
    with t_preview:
        st.subheader(note.title)
        st.markdown(note.content)
    with t_edit:
        note.title = st.text_input("Title", value=note.title)
        note.content = st_monaco(
            value=note.content, height="600px", language="markdown"
        )
        if st.button("Save", key=f"pn_edit_note_{note.id or 'new'}"):
            logger.debug("Editing note")
            note.save()
            if not note.id:
                note.add_to_notebook(notebook_id)
            st.rerun()
    if st.button("Delete", type="primary", key=f"delete_note_{note.id or 'new'}"):
        logger.debug("Deleting note")
        note.delete()
        st.rerun()


def make_note_from_chat(content, notebook_id=None):
    # todo: make this more efficient
    patterns = [
        "Based on the Note below, please provide a Title for this content, with max 15 words"
    ]
    output = pattern_graph.invoke(dict(content_stack=[content], patterns=patterns))
    title = surreal_clean(output["output"])

    note = Note(
        title=title,
        content=content,
        note_type="ai",
    )
    note.save()
    if notebook_id:
        note.add_to_notebook(notebook_id)

    st.rerun()


def note_card(note, notebook_id):
    if note.note_type == "human":
        icon = "🤵"
    else:
        icon = "🤖"

    with st.container(border=True):
        st.markdown((f"{icon} **{note.title if note.title else 'No Title'}**"))
        context_state = st.selectbox(
            "Context",
            label_visibility="collapsed",
            options=context_icons,
            index=0,
            key=f"note_{note.id}",
        )
        st.caption(f"Updated: {naturaltime(note.updated)}")

        if st.button("Expand", icon="📝", key=f"edit_note_{note.id}"):
            note_panel(notebook_id=notebook_id, note=note)

    st.session_state[notebook_id]["context_config"][note.id] = context_state


def note_list_item(note_id, score=None):
    note: Note = Note.get(note_id)
    if note.note_type == "human":
        icon = "🤵"
    else:
        icon = "🤖"

    with st.expander(
        f"{icon} [{score:.2f}] **{note.title}** {naturaltime(note.updated)}"
    ):
        st.write(note.content)
        if st.button("Edit Note", icon="📝", key=f"x_edit_note_{note.id}"):
            note_panel(note=note)
