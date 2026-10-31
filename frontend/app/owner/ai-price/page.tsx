import { AiPricePredictionCard, DemandForecastWidget } from "@/components/ai-widgets";
import { PageHeader } from "@/components/page-templates";

export default function AiPriceSuggestionPage() {
  return (
    <>
      <PageHeader title="AI Price Suggestion" description="Explainable rate recommendations for each listing, ready for ML model integration." />
      <div className="grid gap-6 xl:grid-cols-2">
        <AiPricePredictionCard />
        <DemandForecastWidget />
      </div>
    </>
  );
}
