import { Mail, MapPin, Phone } from "lucide-react";

import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

export default function ContactPage() {
  return (
    <section className="container grid gap-8 py-16 lg:grid-cols-[0.8fr_1.2fr]">
      <div>
        <h1 className="text-4xl font-semibold">Contact</h1>
        <p className="mt-3 text-muted-foreground">Talk to the team about marketplace launches, owner onboarding, and AI integrations.</p>
        <div className="mt-8 grid gap-3 text-sm">
          {[Mail, Phone, MapPin].map((Icon, index) => (
            <div className="flex items-center gap-3" key={index}>
              <Icon className="size-5 text-primary" />
              <span>{["hello@smartspace.ai", "+1 415 555 0198", "San Francisco, CA"][index]}</span>
            </div>
          ))}
        </div>
      </div>
      <Card>
        <CardContent className="grid gap-4 p-6">
          <Input placeholder="Name" />
          <Input placeholder="Email" />
          <Input placeholder="Company" />
          <Input placeholder="How can we help?" />
          <Button variant="premium">Send message</Button>
        </CardContent>
      </Card>
    </section>
  );
}
