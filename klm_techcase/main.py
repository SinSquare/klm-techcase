"""KLM main app"""

from typing import Annotated

from fastapi import FastAPI, HTTPException, Query
from sqlmodel import select
from pathlib import Path
import json
from klm_techcase import models, utils

app = FastAPI(title="KLM techcase")


@app.post(
    "/notes",
    response_model=models.NoteOutput,
    response_model_exclude_unset=True,
    status_code=201,
)
def create_note(note_input: models.NoteInput, session: utils.SessionDep):
    """Create a note"""
    note = models.Note.model_validate(note_input)
    session.add(note)
    session.commit()
    session.refresh(note)
    return note


@app.get(
    "/notes",
    response_model=list[models.NoteOutput],
    response_model_exclude_unset=True,
    status_code=200,
)
def read_notes(
    session: utils.SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    """Retrieve notes"""
    notes = session.exec(
        select(models.Note).order_by(models.Note.id).offset(offset).limit(limit)
    ).all()
    return notes


@app.get(
    "/notes/{note_id}",
    response_model=models.NoteOutput,
    response_model_exclude_unset=True,
    status_code=200,
)
def read_note(note_id: int, session: utils.SessionDep):
    """Retrieve a single note"""
    note = session.get(models.Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@app.put(
    "/notes/{note_id}",
    response_model=models.NoteOutput,
    response_model_exclude_unset=True,
    status_code=200,
)
def modify_note(note_input: models.NoteInput, note_id: int, session: utils.SessionDep):
    """Modify a note"""
    note = session.get(models.Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    note_data = note_input.model_dump(exclude_unset=True)
    note.sqlmodel_update(note_data)
    session.add(note)
    session.commit()
    session.refresh(note)
    note = session.get(models.Note, note_id)
    return note


@app.delete("/notes/{note_id}")
def delete_note(note_id: int, session: utils.SessionDep):
    """Delete a note"""
    note = session.get(models.Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    session.delete(note)
    session.commit()
    return {"ok": True}



def generate_docs() -> None:  # pragma: no cover
    """Generate OpenAPI docs in public/index.html."""
    openapi_spec = app.openapi()
    openapi_spec["servers"] = [{"url": "http://127.0.0.1/", "description": "Sandbox"}]
    html_template = Path("public/index.html.tpl").read_text(encoding="utf8")
    html = html_template % json.dumps(openapi_spec, separators=(",", ":"))
    Path("public/index.html").write_text(html, encoding="utf8")
