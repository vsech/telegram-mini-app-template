import type { PropsWithChildren } from "react";

type PageProps = PropsWithChildren<{
  title: string;
  subtitle?: string;
}>;

export function Page({ title, subtitle, children }: PageProps) {
  return (
    <main className="page">
      <header className="page__header">
        <h1>{title}</h1>
        {subtitle ? <p>{subtitle}</p> : null}
      </header>
      {children}
    </main>
  );
}
