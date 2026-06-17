from typing import Sequence

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.note import Note
from app.schemas.note import NoteCreate


async def get_user_notes(db: AsyncSession, user_id: int) -> Sequence[Note]:
    result = await db.execute(
        select(Note).where(Note.user_id == user_id).order_by(Note.created_at.desc())
    )
    return result.scalars().all()


async def create_note(db: AsyncSession, user_id: int, note_in: NoteCreate) -> Note:
    note = Note(
        user_id=user_id,
        content=note_in.content,
    )
    db.add(note)
    await db.commit()
    await db.refresh(note)
    return note


async def delete_note(db: AsyncSession, user_id: int, note_id: int) -> bool:
    result = await db.execute(
        delete(Note).where(Note.id == note_id, Note.user_id == user_id)
    )
    await db.commit()
    return result.rowcount > 0
