"use client";

import { SlidersHorizontal } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

export function SearchFilters() {
  return (
    <div className="grid gap-3 rounded-lg border bg-card p-4 md:grid-cols-[1.2fr_1fr_1fr_auto]">
      <Input placeholder="Search city, space, or amenity" aria-label="Search query" />
      <Input placeholder="Capacity" aria-label="Capacity" />
      <Input placeholder="Budget per hour" aria-label="Budget" />
      <Button>
        <SlidersHorizontal />
        Filters
      </Button>
    </div>
  );
}
