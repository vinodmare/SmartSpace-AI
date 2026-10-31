import { Star, Users } from "lucide-react";

import { AiPricePredictionCard, SentimentWidget } from "@/components/ai-widgets";
import { BookingCard } from "@/components/forms";
import { Badge } from "@/components/ui/badge";
import { spaces } from "@/lib/mock-data";
import { currency } from "@/lib/utils";

export default async function SpaceDetailsPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const space = spaces.find((item) => item.id === id) ?? spaces[0];

  return (
    <div className="grid gap-6 xl:grid-cols-[1.4fr_0.6fr]">
      <div>
        <div className="overflow-hidden rounded-lg border">
          <img src={space.image} alt={space.name} className="h-[420px] w-full object-cover" />
        </div>
        <div className="mt-6">
          <div className="flex flex-wrap items-start justify-between gap-4">
            <div>
              <h1 className="text-4xl font-semibold">{space.name}</h1>
              <p className="mt-2 text-muted-foreground">{space.city} · {space.type}</p>
            </div>
            <div className="flex items-center gap-2">
              <Star className="size-5 fill-amber-400 text-amber-400" />
              <span className="font-semibold">{space.rating}</span>
            </div>
          </div>
          <div className="mt-4 flex flex-wrap gap-2">
            {space.tags.map((tag) => (
              <Badge key={tag}>{tag}</Badge>
            ))}
          </div>
          <p className="mt-6 max-w-3xl leading-7 text-muted-foreground">
            A premium, AI-scored listing page ready for availability, payments, owner rules, cancellation policies, floor plans, and ML-generated recommendations.
          </p>
          <div className="mt-6 flex items-center gap-6 text-sm">
            <span className="font-semibold">{currency(space.price)}/hr</span>
            <span className="flex items-center gap-1 text-muted-foreground">
              <Users className="size-4" />
              Up to {space.capacity} guests
            </span>
          </div>
        </div>
        <div className="mt-6 grid gap-6 lg:grid-cols-2">
          <AiPricePredictionCard />
          <SentimentWidget />
        </div>
      </div>
      <BookingCard />
    </div>
  );
}
