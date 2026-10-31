import { BookingCard } from "@/components/forms";
import { PageHeader } from "@/components/page-templates";

export default function BookingPage() {
  return (
    <>
      <PageHeader title="Booking" description="Reserve a selected space with payment, policy, and scheduling controls ready for backend integration." />
      <BookingCard />
    </>
  );
}
