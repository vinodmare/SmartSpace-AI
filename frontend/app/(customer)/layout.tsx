import { DashboardShell } from "@/components/dashboard-shell";
import { customerNav } from "@/lib/mock-data";

export default function CustomerLayout({ children }: { children: React.ReactNode }) {
  return (
    <DashboardShell nav={customerNav} role="Customer">
      {children}
    </DashboardShell>
  );
}
