import Link from "next/link";
import { Building2, Menu, Sparkles } from "lucide-react";

import { ThemeToggle } from "@/components/theme-toggle";
import { Button } from "@/components/ui/button";
import { publicNav } from "@/lib/mock-data";

export function Navbar() {
  return (
    <header className="sticky top-0 z-40 border-b bg-background/78 backdrop-blur-xl">
      <div className="container flex h-16 items-center justify-between gap-4">
        <Link href="/" className="flex items-center gap-2 font-semibold">
          <span className="flex size-9 items-center justify-center rounded-md bg-primary text-primary-foreground">
            <Building2 className="size-5" />
          </span>
          <span>SmartSpace AI</span>
        </Link>
        <nav className="hidden items-center gap-6 md:flex" aria-label="Primary navigation">
          {publicNav.map((item) => (
            <Link key={item.href} className="text-sm font-medium text-muted-foreground transition hover:text-foreground" href={item.href}>
              {item.label}
            </Link>
          ))}
        </nav>
        <div className="flex items-center gap-2">
          <ThemeToggle />
          <Button variant="ghost" className="hidden sm:inline-flex" asChild>
            <Link href="/login">Login</Link>
          </Button>
          <Button variant="premium" className="hidden sm:inline-flex" asChild>
            <Link href="/register">
              <Sparkles />
              Start free
            </Link>
          </Button>
          <Button variant="ghost" size="icon" className="md:hidden" aria-label="Open menu">
            <Menu />
          </Button>
        </div>
      </div>
    </header>
  );
}
