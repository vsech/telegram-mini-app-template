export type TelegramUser = {
  id: number;
  username?: string;
  first_name?: string;
  last_name?: string;
  language_code?: string;
  photo_url?: string;
};

export type TelegramWebApp = {
  initData: string;
  initDataUnsafe: {
    user?: TelegramUser;
    auth_date?: number;
    query_id?: string;
  };
  colorScheme: "light" | "dark";
  ready: () => void;
  expand: () => void;
};

declare global {
  interface Window {
    Telegram?: {
      WebApp: TelegramWebApp;
    };
  }
}

export function getTelegramWebApp(): TelegramWebApp | null {
  return window.Telegram?.WebApp ?? null;
}

export function initTelegramWebApp(): TelegramWebApp | null {
  const webApp = getTelegramWebApp();
  if (!webApp) {
    return null;
  }

  webApp.ready();
  webApp.expand();
  document.documentElement.dataset.theme = webApp.colorScheme;
  return webApp;
}

export function getInitData(): string {
  return getTelegramWebApp()?.initData ?? "";
}
