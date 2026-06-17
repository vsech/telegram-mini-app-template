import { useNavigate } from "react-router-dom";

import type { ApiUser } from "../api/client";
import { Button } from "../components/Button";
import { Card } from "../components/Card";
import { ErrorState } from "../components/ErrorState";
import { Loader } from "../components/Loader";
import { Page } from "../components/Page";

type HomePageProps = {
  status: "loading" | "unauthorized" | "authorized" | "error";
  user: ApiUser | null;
  onRetry: () => void;
};

export function HomePage({ status, user, onRetry }: HomePageProps) {
  const navigate = useNavigate();

  if (status === "loading") {
    return (
      <Page title="Telegram Mini App" subtitle="Starter kit">
        <Loader />
      </Page>
    );
  }

  if (status === "unauthorized") {
    return (
      <Page title="Telegram Mini App" subtitle="Starter kit">
        <ErrorState
          title="Open inside Telegram"
          message="Telegram initData is empty. Launch this app as a Mini App to authorize."
          onRetry={onRetry}
        />
      </Page>
    );
  }

  if (status === "error") {
    return (
      <Page title="Telegram Mini App" subtitle="Starter kit">
        <ErrorState
          title="Authorization failed"
          message="The backend rejected the Telegram session or is temporarily unavailable."
          onRetry={onRetry}
        />
      </Page>
    );
  }

  return (
    <Page
      title={`Hi${user?.first_name ? `, ${user.first_name}` : ""}`}
      subtitle="You are authorized with Telegram WebApp initData."
    >
      <Card>
        <div className="status-row">
          <span className="status-dot" />
          <div>
            <strong>Authorized</strong>
            <p>Profile synced with the backend.</p>
          </div>
        </div>
        <Button className="button-link" onClick={() => navigate("/profile")}>
          Open profile
        </Button>
      </Card>
    </Page>
  );
}
