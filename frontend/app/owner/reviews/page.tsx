import { SentimentWidget } from "@/components/ai-widgets";
import { OperationsPage } from "@/components/page-templates";

export default function ReviewsPage() {
  return (
    <div className="grid gap-6 xl:grid-cols-[1fr_0.8fr]">
      <OperationsPage title="Reviews" description="Guest ratings, owner replies, sentiment trends, and service recovery workflows." />
      <SentimentWidget />
    </div>
  );
}
