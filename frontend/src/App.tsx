import { useCallback, useEffect, useState } from "react";
import { Route, Routes } from "react-router-dom";

import { authTelegram, type ApiUser } from "./api/client";
import { Layout } from "./components/Layout";
import { initTelegramWebApp } from "./lib/telegram";
import { HomePage } from "./pages/HomePage";
import { ProfilePage } from "./pages/ProfilePage";
import { NotesPage } from "./pages/NotesPage";

type AuthStatus = "loading" | "unauthorized" | "authorized" | "error";

function App() {
  const [status, setStatus] = useState<AuthStatus>("loading");
  const [user, setUser] = useState<ApiUser | null>(null);

  const authorize = useCallback(async () => {
    setStatus("loading");
    const webApp = initTelegramWebApp();
    const initData = webApp?.initData ?? "";

    if (!initData) {
      setStatus("unauthorized");
      setUser(null);
      return;
    }

    try {
      const profile = await authTelegram(initData);
      setUser(profile);
      setStatus("authorized");
    } catch {
      setUser(null);
      setStatus("error");
    }
  }, []);

  useEffect(() => {
    void authorize();
  }, [authorize]);

  return (
    <Layout>
      <Routes>
        <Route
          path="/"
          element={<HomePage status={status} user={user} onRetry={authorize} />}
        />
        <Route
          path="/profile"
          element={
            <ProfilePage status={status} user={user} onRetry={authorize} />
          }
        />
        <Route path="/notes" element={<NotesPage />} />
      </Routes>
    </Layout>
  );
}

export default App;
