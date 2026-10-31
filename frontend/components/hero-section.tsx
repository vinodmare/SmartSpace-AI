import Link from "next/link";
import { ArrowRight, CalendarCheck, MapPin, Search, Sparkles } from "lucide-react";

import { MotionShell } from "@/components/motion-shell";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { currency } from "@/lib/utils";

export function HeroSection() {
  return (
    <section className="relative overflow-hidden">
      <div className="container grid min-h-[calc(100vh-4rem)] items-center gap-10 py-16 lg:grid-cols-[1.05fr_0.95fr]">
        <MotionShell>
          <Badge className="mb-5 bg-background/70 text-primary">
            <Sparkles className="mr-2 size-3.5" />
            AI marketplace for every rentable space
          </Badge>
          <h1 className="max-w-4xl text-5xl font-semibold tracking-normal text-foreground md:text-7xl">
            SmartSpace AI
          </h1>
          <p className="mt-5 max-w-2xl text-lg leading-8 text-muted-foreground">
            Find, book, price, and manage event halls, meeting rooms, coworking spaces, parking, studios,
            classrooms, sports venues, warehouses, and offices from one intelligent operating system.
          </p>
          <div className="mt-8 flex flex-col gap-3 sm:flex-row">
            <Button variant="premium" size="lg" asChild>
              <Link href="/ai-search">
                Try AI search
                <ArrowRight />
              </Link>
            </Button>
            <Button variant="outline" size="lg" asChild>
              <Link href="/search">Browse spaces</Link>
            </Button>
          </div>
          <div className="glass mt-10 grid gap-3 rounded-lg p-3 shadow-glow md:grid-cols-[1fr_1fr_auto]">
            <label className="relative">
              <MapPin className="absolute left-3 top-3 size-5 text-muted-foreground" />
              <Input className="pl-10" placeholder="City, neighborhood, venue" aria-label="Location" />
            </label>
            <label className="relative">
              <CalendarCheck className="absolute left-3 top-3 size-5 text-muted-foreground" />
              <Input className="pl-10" placeholder="Date and capacity" aria-label="Date and capacity" />
            </label>
            <Button className="h-11" aria-label="Search spaces">
              <Search />
              Search
            </Button>
          </div>
        </MotionShell>
        <MotionShell className="relative">
          <div className="relative aspect-[4/5] overflow-hidden rounded-lg shadow-glow">
            <img
              src="https://images.unsplash.com/photo-1518005020951-eccb494ad742?auto=format&fit=crop&w=1300&q=80"
              alt="Premium shared workspace with modern architecture"
              className="size-full object-cover"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-slate-950/70 via-slate-950/10 to-transparent" />
            <div className="absolute bottom-4 left-4 right-4 grid gap-3 rounded-lg border border-white/20 bg-white/14 p-4 text-white backdrop-blur-xl">
              <div className="flex items-center justify-between">
                <p className="font-semibold">AI demand score</p>
                <span className="rounded-full bg-teal-400 px-2 py-1 text-xs font-bold text-slate-950">94%</span>
              </div>
              <div className="h-2 rounded-full bg-white/20">
                <div className="h-2 w-[94%] rounded-full bg-gradient-to-r from-sky-300 to-amber-300" />
              </div>
              <p className="text-sm text-white/80">
                Recommended price window: {currency(23000)}-{currency(28000)} per hour
              </p>
            </div>
          </div>
        </MotionShell>
      </div>
    </section>
  );
}
