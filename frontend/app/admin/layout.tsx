import { DashboardShell } from "@/components/dashboard-shell";
import { adminNav } from "@/lib/mock-data";

export default function AdminLayout({ children }: { children: React.ReactNode }) {
  return (
    <DashboardShell nav={adminNav} role="Admin">
      {children}
    </DashboardShell>
  );
}
