import { useState, useEffect } from "react";
import { Page } from "../components/Page";
import { Card } from "../components/Card";
import { Button } from "../components/Button";
import { Loader } from "../components/Loader";
import { ErrorState } from "../components/ErrorState";
import { getNotes, createNote, deleteNote, ApiNote } from "../api/client";

export function NotesPage() {
  const [notes, setNotes] = useState<ApiNote[]>([]);
  const [newNote, setNewNote] = useState("");
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    loadNotes();
  }, []);

  async function loadNotes() {
    try {
      setIsLoading(true);
      const data = await getNotes();
      setNotes(data);
      setError(null);
    } catch (err) {
      setError("Failed to load notes");
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  }

  async function handleCreateNote(e: React.FormEvent) {
    e.preventDefault();
    if (!newNote.trim()) return;

    try {
      setIsSubmitting(true);
      const note = await createNote({ content: newNote });
      setNotes([note, ...notes]);
      setNewNote("");
    } catch (err) {
      console.error(err);
      alert("Failed to create note");
    } finally {
      setIsSubmitting(false);
    }
  }

  async function handleDeleteNote(id: number) {
    if (!confirm("Are you sure you want to delete this note?")) return;

    try {
      await deleteNote(id);
      setNotes(notes.filter((n) => n.id !== id));
    } catch (err) {
      console.error(err);
      alert("Failed to delete note");
    }
  }

  if (isLoading) return <Loader />;
  if (error)
    return <ErrorState title="Error" message={error} onRetry={loadNotes} />;

  return (
    <Page title="My Notes">
      <form onSubmit={handleCreateNote} className="notes-form">
        <textarea
          value={newNote}
          onChange={(e) => setNewNote(e.target.value)}
          placeholder="Type your note here..."
          className="notes-textarea"
          disabled={isSubmitting}
        />
        <Button type="submit" disabled={isSubmitting || !newNote.trim()}>
          {isSubmitting ? "Adding..." : "Add Note"}
        </Button>
      </form>

      <div className="notes-list">
        {notes.length === 0 ? (
          <p className="text-center text-gray-500 py-8">
            No notes yet. Create your first one!
          </p>
        ) : (
          notes.map((note) => (
            <Card key={note.id}>
              <div className="note-card__header">
                <p className="note-card__content">{note.content}</p>
                <button
                  onClick={() => handleDeleteNote(note.id)}
                  className="note-card__delete"
                  aria-label="Delete note"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="20"
                    height="20"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  >
                    <path d="M3 6h18" />
                    <path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6" />
                    <path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2" />
                    <line x1="10" y1="11" x2="10" y2="17" />
                    <line x1="14" y1="11" x2="14" y2="17" />
                  </svg>
                </button>
              </div>
              <p className="note-card__date">
                {new Date(note.created_at).toLocaleString()}
              </p>
            </Card>
          ))
        )}
      </div>
    </Page>
  );
}
