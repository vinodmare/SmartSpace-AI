import Link from "next/link";

import { publicNav } from "@/lib/mock-data";

export function Footer() {
  return (
    <footer className="border-t bg-card/60">
      <div className="container grid gap-8 py-10 md:grid-cols-[1.5fr_1fr_1fr]">
        <div>
          <p className="font-semibold">SmartSpace AI</p>
          <p className="mt-2 max-w-md text-sm text-muted-foreground">
            Intelligent space discovery, booking operations, owner revenue tools, and admin trust systems in one premium marketplace.
          </p>
        </div>
        <div className="grid gap-2 text-sm">
          {publicNav.map((item) => (
            <Link className="text-muted-foreground hover:text-foreground" href={item.href} key={item.href}>
              {item.label}
            </Link>
          ))}
        </div>
        <div className="text-sm text-muted-foreground">
          <p>Enterprise-ready UI prototype.</p>
          <p className="mt-2">Built for backend and ML integration.</p>
        </div>
      </div>
    </footer>
  );
}
