from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.db.models.user import User
from app.schemas.note import NoteCreate, NoteRead
from app.services import notes as notes_service

router = APIRouter(prefix="/notes", tags=["notes"])

CurrentUser = Annotated[User, Depends(get_current_user)]
Session = Annotated[AsyncSession, Depends(get_db)]


@router.get("/", response_model=List[NoteRead])
async def list_notes(
    current_user: CurrentUser,
    db: Session,
) -> List[NoteRead]:
    return await notes_service.get_user_notes(db, current_user.id)


@router.post("/", response_model=NoteRead, status_code=status.HTTP_201_CREATED)
async def create_note(
    current_user: CurrentUser,
    db: Session,
    note_in: NoteCreate,
) -> NoteRead:
    return await notes_service.create_note(db, current_user.id, note_in)


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(
    current_user: CurrentUser,
    db: Session,
    note_id: int,
):
    success = await notes_service.delete_note(db, current_user.id, note_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found",
        )
