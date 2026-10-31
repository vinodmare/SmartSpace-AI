import Link from "next/link";
import { Building2 } from "lucide-react";

import { ThemeToggle } from "@/components/theme-toggle";

export default function AuthLayout({ children }: { children: React.ReactNode }) {
  return (
    <main className="grid min-h-screen place-items-center px-4 py-10">
      <div className="absolute left-6 top-6 flex items-center gap-3">
        <Link href="/" className="flex items-center gap-2 font-semibold">
          <span className="flex size-9 items-center justify-center rounded-md bg-primary text-primary-foreground">
            <Building2 className="size-5" />
          </span>
          SmartSpace AI
        </Link>
      </div>
      <div className="absolute right-6 top-6">
        <ThemeToggle />
      </div>
      {children}
    </main>
  );
}
