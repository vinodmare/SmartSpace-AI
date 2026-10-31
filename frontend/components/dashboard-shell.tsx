import Link from "next/link";
import { Building2, Menu, Sparkles } from "lucide-react";
import { ReactNode } from "react";

import { ThemeToggle } from "@/components/theme-toggle";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

type NavItem = {
  label: string;
  href: string;
  icon: React.ComponentType<{ className?: string }>;
};

export function DashboardShell({
  children,
  nav,
  role,
}: {
  children: ReactNode;
  nav: NavItem[];
  role: "Customer" | "Owner" | "Admin";
}) {
  return (
    <div className="min-h-screen bg-background">
      <aside className="fixed inset-y-0 left-0 z-40 hidden w-72 border-r bg-card/80 backdrop-blur-xl lg:block">
        <div className="flex h-16 items-center gap-2 border-b px-5">
          <span className="flex size-9 items-center justify-center rounded-md bg-primary text-primary-foreground">
            <Building2 className="size-5" />
          </span>
          <div>
            <p className="font-semibold">SmartSpace AI</p>
            <p className="text-xs text-muted-foreground">{role} console</p>
          </div>
        </div>
        <nav className="grid gap-1 p-3" aria-label={`${role} navigation`}>
          {nav.map((item, index) => {
            const Icon = item.icon;
            return (
              <Link
                href={item.href}
                key={item.href}
                className={cn(
                  "flex items-center gap-3 rounded-md px-3 py-2.5 text-sm font-medium text-muted-foreground transition hover:bg-muted hover:text-foreground",
                  index === 0 && "bg-primary/10 text-primary",
                )}
              >
                <Icon className="size-4" />
                {item.label}
              </Link>
            );
          })}
        </nav>
      </aside>
      <div className="lg:pl-72">
        <header className="sticky top-0 z-30 flex h-16 items-center justify-between border-b bg-background/78 px-4 backdrop-blur-xl md:px-6">
          <div className="flex items-center gap-3">
            <Button variant="ghost" size="icon" className="lg:hidden" aria-label="Open navigation">
              <Menu />
            </Button>
            <div>
              <p className="text-sm font-semibold">{role} workspace</p>
              <p className="hidden text-xs text-muted-foreground sm:block">Mock data connected to production-ready UI states</p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <Button variant="outline" className="hidden sm:inline-flex">
              <Sparkles />
              Ask AI
            </Button>
            <ThemeToggle />
          </div>
        </header>
        <main className="container py-6">{children}</main>
      </div>
    </div>
  );
}
