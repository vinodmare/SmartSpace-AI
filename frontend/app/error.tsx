"use client";

import { Button } from "@/components/ui/button";

export default function ErrorPage({ reset }: { reset: () => void }) {
  return (
    <main className="grid min-h-screen place-items-center px-4 text-center">
      <div>
        <p className="text-sm font-semibold text-destructive">Error</p>
        <h1 className="mt-3 text-4xl font-semibold">Something went wrong</h1>
        <p className="mt-3 max-w-md text-muted-foreground">The interface recovered cleanly and can retry this view.</p>
        <Button className="mt-6" onClick={reset}>Try again</Button>
      </div>
    </main>
  );
}
