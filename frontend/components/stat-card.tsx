import { Card, CardContent } from "@/components/ui/card";

export function StatCard({
  label,
  value,
  delta,
  icon: Icon,
}: {
  label: string;
  value: string;
  delta: string;
  icon: React.ComponentType<{ className?: string }>;
}) {
  return (
    <Card className="overflow-hidden">
      <CardContent className="p-5">
        <div className="flex items-start justify-between gap-4">
          <div>
            <p className="text-sm text-muted-foreground">{label}</p>
            <p className="mt-2 text-2xl font-semibold">{value}</p>
          </div>
          <span className="flex size-10 items-center justify-center rounded-md bg-primary/10 text-primary">
            <Icon className="size-5" />
          </span>
        </div>
        <p className="mt-4 text-sm font-medium text-teal-600 dark:text-teal-300">{delta} vs last month</p>
      </CardContent>
    </Card>
  );
}
