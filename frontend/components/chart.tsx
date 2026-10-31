import { chartData } from "@/lib/mock-data";

export function DemandChart() {
  const max = Math.max(...chartData);

  return (
    <div className="flex h-56 items-end gap-2 rounded-lg border bg-background/60 p-4" aria-label="Demand forecast chart">
      {chartData.map((value, index) => (
        <div className="flex flex-1 flex-col items-center gap-2" key={`${value}-${index}`}>
          <div
            className="w-full rounded-t-md bg-gradient-to-t from-sky-600 to-teal-300"
            style={{ height: `${Math.max(14, (value / max) * 100)}%` }}
          />
          <span className="text-[10px] text-muted-foreground">{index + 1}</span>
        </div>
      ))}
    </div>
  );
}
