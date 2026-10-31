import { CalendarDays } from "lucide-react";

import { PageHeader } from "@/components/page-templates";
import { Card, CardContent } from "@/components/ui/card";

export default function CalendarPage() {
  const days = Array.from({ length: 35 }, (_, index) => index + 1);

  return (
    <>
      <PageHeader title="Calendar" description="A responsive owner calendar surface for availability, holds, bookings, and maintenance blocks." />
      <Card>
        <CardContent className="p-4">
          <div className="mb-4 flex items-center gap-2 font-semibold">
            <CalendarDays className="size-5 text-primary" />
            July 2026
          </div>
          <div className="grid grid-cols-7 gap-2">
            {days.map((day) => (
              <button
                className="focus-ring aspect-square rounded-md border bg-background text-sm transition hover:bg-muted data-[booked=true]:bg-primary data-[booked=true]:text-primary-foreground"
                data-booked={day % 6 === 0}
                key={day}
              >
                {day}
              </button>
            ))}
          </div>
        </CardContent>
      </Card>
    </>
  );
}
