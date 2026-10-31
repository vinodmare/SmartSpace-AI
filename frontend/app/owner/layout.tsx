import { DashboardShell } from "@/components/dashboard-shell";
import { ownerNav } from "@/lib/mock-data";

export default function OwnerLayout({ children }: { children: React.ReactNode }) {
  return (
    <DashboardShell nav={ownerNav} role="Owner">
      {children}
    </DashboardShell>
  );
}
