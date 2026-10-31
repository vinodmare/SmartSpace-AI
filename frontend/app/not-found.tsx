import Link from "next/link";

import { Button } from "@/components/ui/button";

export default function NotFound() {
  return (
    <main className="grid min-h-screen place-items-center px-4 text-center">
      <div>
        <p className="text-sm font-semibold text-primary">404</p>
        <h1 className="mt-3 text-4xl font-semibold">Page not found</h1>
        <p className="mt-3 max-w-md text-muted-foreground">This SmartSpace AI route is not available yet.</p>
        <Button className="mt-6" asChild>
          <Link href="/">Return home</Link>
        </Button>
      </div>
    </main>
  );
}
