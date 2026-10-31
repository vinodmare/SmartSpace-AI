import { Check } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";

const plans = [
  ["Starter", "₹4,099", "For emerging space owners"],
  ["Growth", "₹20,699", "For multi-location operators"],
  ["Enterprise", "Custom", "For marketplace-scale teams"],
];

export default function PricingPage() {
  return (
    <section className="container py-16">
      <h1 className="text-4xl font-semibold">Pricing</h1>
      <p className="mt-3 max-w-2xl text-muted-foreground">Plans for customers, owners, and platform administrators preparing for production integration.</p>
      <div className="mt-8 grid gap-5 md:grid-cols-3">
        {plans.map(([name, price, copy]) => (
          <Card className={name === "Growth" ? "border-primary shadow-glow" : ""} key={name}>
            <CardContent className="p-6">
              <h2 className="text-xl font-semibold">{name}</h2>
              <p className="mt-2 text-sm text-muted-foreground">{copy}</p>
              <p className="mt-6 text-4xl font-semibold">{price}</p>
              <div className="mt-6 grid gap-3 text-sm">
                {["AI recommendations", "Booking workflows", "Analytics dashboards"].map((feature) => (
                  <span className="flex items-center gap-2" key={feature}>
                    <Check className="size-4 text-teal-500" />
                    {feature}
                  </span>
                ))}
              </div>
              <Button className="mt-6 w-full" variant={name === "Growth" ? "premium" : "outline"}>Choose plan</Button>
            </CardContent>
          </Card>
        ))}
      </div>
    </section>
  );
}
