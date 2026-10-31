import { faqs } from "@/lib/mock-data";

export default function FaqPage() {
  return (
    <section className="container py-16">
      <h1 className="text-4xl font-semibold">FAQ</h1>
      <div className="mt-8 grid gap-4">
        {faqs.map((faq) => (
          <article className="rounded-lg border bg-card p-5" key={faq.q}>
            <h2 className="font-semibold">{faq.q}</h2>
            <p className="mt-2 text-muted-foreground">{faq.a}</p>
          </article>
        ))}
      </div>
    </section>
  );
}
