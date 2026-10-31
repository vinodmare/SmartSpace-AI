import { ReactNode } from "react";

import { AiAssistantCard, AiPricePredictionCard, DemandForecastWidget, FraudRiskIndicator, SentimentWidget } from "@/components/ai-widgets";
import { BookingTable } from "@/components/data-table";
import { SearchFilters } from "@/components/search-filters";
import { SpaceCard } from "@/components/space-card";
import { StatCard } from "@/components/stat-card";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { spaces, stats } from "@/lib/mock-data";

export function PageHeader({ title, description, action }: { title: string; description: string; action?: ReactNode }) {
  return (
    <div className="mb-6 flex flex-col justify-between gap-4 md:flex-row md:items-end">
      <div>
        <h1 className="text-3xl font-semibold md:text-4xl">{title}</h1>
        <p className="mt-2 max-w-2xl text-muted-foreground">{description}</p>
      </div>
      {action}
    </div>
  );
}

export function OverviewPage({ title, description }: { title: string; description: string }) {
  return (
    <>
      <PageHeader title={title} description={description} />
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {stats.map((stat) => (
          <StatCard key={stat.label} {...stat} />
        ))}
      </div>
      <div className="mt-6 grid gap-6 xl:grid-cols-[1.3fr_0.7fr]">
        <DemandForecastWidget />
        <AiAssistantCard />
      </div>
      <div className="mt-6 grid gap-6 xl:grid-cols-[1fr_1fr]">
        <AiPricePredictionCard />
        <FraudRiskIndicator />
      </div>
      <div className="mt-6">
        <BookingTable />
      </div>
    </>
  );
}

export function SearchPageTemplate({ ai = false }: { ai?: boolean }) {
  return (
    <>
      <PageHeader
        title={ai ? "AI Search" : "Search Spaces"}
        description={
          ai
            ? "Describe your event, budget, audience, and vibe. The interface is ready for ML-powered intent matching."
            : "Explore bookable spaces with filters designed for marketplace discovery."
        }
      />
      <SearchFilters />
      {ai && (
        <div className="mt-6">
          <AiAssistantCard />
        </div>
      )}
      <div className="mt-6 grid gap-5 md:grid-cols-2 xl:grid-cols-4">
        {spaces.map((space) => (
          <SpaceCard key={space.id} space={space} />
        ))}
      </div>
    </>
  );
}

export function OperationsPage({ title, description }: { title: string; description: string }) {
  return (
    <>
      <PageHeader title={title} description={description} />
      <div className="grid gap-6 xl:grid-cols-[1.2fr_0.8fr]">
        <BookingTable />
        <SentimentWidget />
      </div>
    </>
  );
}

export function AnalyticsPage({ title, description, fraud = false }: { title: string; description: string; fraud?: boolean }) {
  return (
    <>
      <PageHeader title={title} description={description} />
      <div className="grid gap-6 xl:grid-cols-[1.2fr_0.8fr]">
        <DemandForecastWidget />
        {fraud ? <FraudRiskIndicator /> : <AiPricePredictionCard />}
      </div>
      <div className="mt-6 grid gap-4 md:grid-cols-3">
        {[1, 2, 3].map((item) => (
          <Card key={item}>
            <CardHeader>
              <CardTitle>Insight {item}</CardTitle>
              <CardDescription>AI-generated operating recommendation.</CardDescription>
            </CardHeader>
            <CardContent>
              <Skeleton className="h-3 w-full" />
              <Skeleton className="mt-3 h-3 w-3/4" />
            </CardContent>
          </Card>
        ))}
      </div>
    </>
  );
}
