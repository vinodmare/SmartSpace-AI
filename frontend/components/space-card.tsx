import Link from "next/link";
import { MapPin, Star, Users } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { currency } from "@/lib/utils";

export function SpaceCard({ space }: { space: (typeof import("@/lib/mock-data").spaces)[number] }) {
  return (
    <Card className="overflow-hidden transition hover:-translate-y-1 hover:shadow-glow">
      <div className="aspect-[16/10] overflow-hidden">
        <img src={space.image} alt={space.name} className="size-full object-cover transition duration-500 hover:scale-105" />
      </div>
      <CardContent className="p-4">
        <div className="flex items-start justify-between gap-3">
          <div>
            <p className="font-semibold">{space.name}</p>
            <p className="mt-1 flex items-center gap-1 text-sm text-muted-foreground">
              <MapPin className="size-4" />
              {space.city} · {space.type}
            </p>
          </div>
          <span className="flex items-center gap-1 text-sm font-semibold">
            <Star className="size-4 fill-amber-400 text-amber-400" />
            {space.rating}
          </span>
        </div>
        <div className="mt-3 flex flex-wrap gap-2">
          {space.tags.map((tag) => (
            <Badge key={tag}>{tag}</Badge>
          ))}
        </div>
        <div className="mt-4 flex items-center justify-between gap-3">
          <div>
            <p className="text-lg font-semibold">{currency(space.price)}/hr</p>
            <p className="flex items-center gap-1 text-xs text-muted-foreground">
              <Users className="size-3.5" />
              up to {space.capacity}
            </p>
          </div>
          <Button asChild>
            <Link href={`/spaces/${space.id}`}>View</Link>
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}
