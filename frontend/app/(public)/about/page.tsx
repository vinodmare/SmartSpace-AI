import { PageHeader } from "@/components/page-templates";

export default function AboutPage() {
  return (
    <section className="container py-16">
      <PageHeader title="About SmartSpace AI" description="A marketplace operating system for discovery, dynamic pricing, booking trust, and owner revenue growth." />
      <div className="grid gap-6 text-lg leading-8 text-muted-foreground md:grid-cols-2">
        <p>SmartSpace AI helps customers find the right physical space faster and helps owners run every square foot like a modern software business.</p>
        <p>The product experience is designed for premium marketplace quality: fast scanning, rich comparison, AI assistance, and clear operational workflows.</p>
      </div>
    </section>
  );
}
