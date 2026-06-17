import type { ApiUser } from "../api/client";
import { Card } from "../components/Card";
import { ErrorState } from "../components/ErrorState";
import { Loader } from "../components/Loader";
import { Page } from "../components/Page";

type ProfilePageProps = {
  status: "loading" | "unauthorized" | "authorized" | "error";
  user: ApiUser | null;
  onRetry: () => void;
};

export function ProfilePage({ status, user, onRetry }: ProfilePageProps) {
  if (status === "loading") {
    return (
      <Page title="Profile">
        <Loader />
      </Page>
    );
  }

  if (status !== "authorized" || !user) {
    return (
      <Page title="Profile">
        <ErrorState
          title="Profile unavailable"
          message="Authorize through Telegram to view your profile."
          onRetry={onRetry}
        />
      </Page>
    );
  }

  const fullName = [user.first_name, user.last_name].filter(Boolean).join(" ");

  return (
    <Page
      title="Profile"
      subtitle="Telegram account data from verified initData"
    >
      <Card>
        <div className="profile">
          {user.photo_url ? (
            <img src={user.photo_url} alt="" className="profile__avatar" />
          ) : (
            <div className="profile__avatar profile__avatar--empty">
              {user.first_name?.[0] ?? "U"}
            </div>
          )}
          <div>
            <h2>{fullName || user.username || `User ${user.telegram_id}`}</h2>
            {user.username ? <p>@{user.username}</p> : null}
          </div>
        </div>

        <dl className="profile-fields">
          <div>
            <dt>Telegram ID</dt>
            <dd>{user.telegram_id}</dd>
          </div>
          <div>
            <dt>Username</dt>
            <dd>{user.username ? `@${user.username}` : "Not set"}</dd>
          </div>
          <div>
            <dt>Name</dt>
            <dd>{fullName || "Not set"}</dd>
          </div>
          <div>
            <dt>Language</dt>
            <dd>{user.language_code ?? "Unknown"}</dd>
          </div>
        </dl>
      </Card>
    </Page>
  );
}
