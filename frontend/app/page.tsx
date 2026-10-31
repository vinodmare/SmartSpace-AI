import { ArrowRight, BadgeCheck, Building2, ShieldCheck, Sparkles } from "lucide-react";
import Link from "next/link";

import { AiPricePredictionCard, DemandForecastWidget, FraudRiskIndicator, SentimentWidget } from "@/components/ai-widgets";
import { Footer } from "@/components/footer";
import { HeroSection } from "@/components/hero-section";
import { Navbar } from "@/components/navbar";
import { SpaceCard } from "@/components/space-card";
import { StatCard } from "@/components/stat-card";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { spaces, stats } from "@/lib/mock-data";

export default function LandingPage() {
  return (
    <>
      <Navbar />
      <main>
        <HeroSection />
        <section className="border-y bg-card/45 py-14">
          <div className="container grid gap-4 md:grid-cols-2 xl:grid-cols-4">
            {stats.map((stat) => (
              <StatCard key={stat.label} {...stat} />
            ))}
          </div>
        </section>
        <section className="container py-16">
          <div className="mb-8 flex flex-col justify-between gap-4 md:flex-row md:items-end">
            <div>
              <h2 className="text-3xl font-semibold md:text-4xl">Recommended spaces</h2>
              <p className="mt-2 max-w-2xl text-muted-foreground">
                A polished discovery experience for event halls, coworking, studios, parking, warehouses, classrooms, sports venues, and offices.
              </p>
            </div>
            <Button variant="outline" asChild>
              <Link href="/search">
                View marketplace
                <ArrowRight />
              </Link>
            </Button>
          </div>
          <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-4">
            {spaces.map((space) => (
              <SpaceCard key={space.id} space={space} />
            ))}
          </div>
        </section>
        <section className="bg-muted/40 py-16">
          <div className="container grid gap-6 xl:grid-cols-2">
            <DemandForecastWidget />
            <AiPricePredictionCard />
            <SentimentWidget />
            <FraudRiskIndicator />
          </div>
        </section>
        <section className="container py-16">
          <div className="grid gap-6 md:grid-cols-3">
            {[
              ["Customer intelligence", Sparkles, "Natural language discovery, smart recommendations, favorites, history, notifications, and profile settings."],
              ["Owner operations", Building2, "Space management, calendars, booking workflow, revenue analytics, AI price suggestions, and reviews."],
              ["Admin trust", ShieldCheck, "Owner verification, approvals, booking oversight, reports, fraud monitoring, and marketplace analytics."],
            ].map(([title, Icon, copy]) => (
              <Card key={title as string}>
                <CardContent className="p-6">
                  <span className="flex size-11 items-center justify-center rounded-md bg-primary/10 text-primary">
                    {typeof Icon !== "string" && <Icon className="size-5" />}
                  </span>
                  <h3 className="mt-5 text-xl font-semibold">{title as string}</h3>
                  <p className="mt-2 text-sm leading-6 text-muted-foreground">{copy as string}</p>
                </CardContent>
              </Card>
            ))}
          </div>
          <div className="mt-10 rounded-lg border bg-gradient-to-r from-sky-700 via-teal-600 to-amber-500 p-8 text-white shadow-glow">
            <BadgeCheck className="size-8" />
            <h2 className="mt-4 text-3xl font-semibold">Built as a SaaS-grade frontend foundation.</h2>
            <p className="mt-3 max-w-2xl text-white/82">
              Componentized, responsive, theme-aware, accessible, and ready for backend APIs, payments, auth, and ML services.
            </p>
          </div>
        </section>
      </main>
      <Footer />
    </>
  );
}
