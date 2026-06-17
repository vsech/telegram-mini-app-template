import { getInitData } from "../lib/telegram";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "/api";

export type ApiUser = {
  id: number;
  telegram_id: number;
  username: string | null;
  first_name: string | null;
  last_name: string | null;
  language_code: string | null;
  photo_url: string | null;
  is_active: boolean;
  is_admin: boolean;
  created_at: string;
  updated_at: string;
};

export type ApiNote = {
  id: number;
  user_id: number;
  content: string;
  created_at: string;
  updated_at: string;
};

export type NoteCreate = {
  content: string;
};

type RequestOptions = {
  method?: "GET" | "POST" | "DELETE";
  body?: unknown;
  withAuth?: boolean;
};

export async function apiRequest<T>(
  path: string,
  options: RequestOptions = {},
): Promise<T> {
  const headers = new Headers({ "Content-Type": "application/json" });
  if (options.withAuth) {
    const initData = getInitData();
    if (initData) {
      headers.set("X-Telegram-Init-Data", initData);
    }
  }

  const response = await fetch(`${API_BASE_URL}${path}`, {
    method: options.method ?? "GET",
    headers,
    body: options.body ? JSON.stringify(options.body) : undefined,
  });

  if (response.status === 204) {
    return {} as T;
  }

  if (!response.ok) {
    throw new Error(`API request failed with status ${response.status}`);
  }

  return response.json() as Promise<T>;
}

export function authTelegram(initData: string): Promise<ApiUser> {
  return apiRequest<ApiUser>("/auth/telegram", {
    method: "POST",
    body: { init_data: initData },
  });
}

export function getMe(): Promise<ApiUser> {
  return apiRequest<ApiUser>("/users/me", { withAuth: true });
}

export function getNotes(): Promise<ApiNote[]> {
  return apiRequest<ApiNote[]>("/notes/", { withAuth: true });
}

export function createNote(note: NoteCreate): Promise<ApiNote> {
  return apiRequest<ApiNote>("/notes/", {
    method: "POST",
    body: note,
    withAuth: true,
  });
}

export function deleteNote(id: number): Promise<void> {
  return apiRequest<void>(`/notes/${id}`, {
    method: "DELETE",
    withAuth: true,
  });
}
