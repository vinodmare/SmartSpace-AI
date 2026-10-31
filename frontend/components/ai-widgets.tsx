import { AlertTriangle, BrainCircuit, ShieldCheck, Sparkles, TrendingUp } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { DemandChart } from "@/components/chart";
import { currency } from "@/lib/utils";

export function AiAssistantCard() {
  return (
    <Card className="glass">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Sparkles className="size-5 text-primary" />
          AI Assistant Chat
        </CardTitle>
        <CardDescription>Natural language booking, pricing, and trust operations.</CardDescription>
      </CardHeader>
      <CardContent className="grid gap-3">
        {["Find a 120-person launch venue under ₹3.5L", "Compare owner revenue risk", "Explain this fraud alert"].map((item) => (
          <div className="rounded-lg border bg-background/70 p-3 text-sm" key={item}>
            {item}
          </div>
        ))}
      </CardContent>
    </Card>
  );
}

export function AiPricePredictionCard() {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <BrainCircuit className="size-5 text-primary" />
          AI Price Prediction
        </CardTitle>
        <CardDescription>Suggested rate based on demand, seasonality, reviews, and nearby spaces.</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="flex items-end justify-between gap-4">
          <div>
            <p className="text-4xl font-semibold">{currency(25500)}</p>
            <p className="text-sm text-muted-foreground">per hour optimal midpoint</p>
          </div>
          <Badge className="border-teal-400 text-teal-600">+18% lift</Badge>
        </div>
        <div className="mt-5 h-2 rounded-full bg-muted">
          <div className="h-2 w-[76%] rounded-full bg-gradient-to-r from-sky-600 to-teal-400" />
        </div>
      </CardContent>
    </Card>
  );
}

export function DemandForecastWidget() {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <TrendingUp className="size-5 text-primary" />
          Demand Forecast
        </CardTitle>
        <CardDescription>Projected marketplace demand over the next 12 weeks.</CardDescription>
      </CardHeader>
      <CardContent>
        <DemandChart />
      </CardContent>
    </Card>
  );
}

export function SentimentWidget() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Review Sentiment</CardTitle>
        <CardDescription>Aggregated guest feedback signal.</CardDescription>
      </CardHeader>
      <CardContent className="grid gap-3">
        {[
          ["Positive", "82%", "bg-teal-500"],
          ["Neutral", "13%", "bg-amber-400"],
          ["Needs attention", "5%", "bg-rose-500"],
        ].map(([label, value, color]) => (
          <div key={label}>
            <div className="mb-1 flex justify-between text-sm">
              <span>{label}</span>
              <span className="font-medium">{value}</span>
            </div>
            <div className="h-2 rounded-full bg-muted">
              <div className={`h-2 rounded-full ${color}`} style={{ width: value }} />
            </div>
          </div>
        ))}
      </CardContent>
    </Card>
  );
}

export function FraudRiskIndicator() {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <ShieldCheck className="size-5 text-teal-500" />
          Fraud Risk Indicator
        </CardTitle>
        <CardDescription>Identity, payment, device, and booking behavior model.</CardDescription>
      </CardHeader>
      <CardContent className="flex items-center justify-between gap-4">
        <div>
          <p className="text-3xl font-semibold">Low</p>
          <p className="text-sm text-muted-foreground">Risk score 18/100</p>
        </div>
        <div className="flex size-20 items-center justify-center rounded-full border-8 border-teal-400 text-teal-600">
          <AlertTriangle className="size-7" />
        </div>
      </CardContent>
    </Card>
  );
}
