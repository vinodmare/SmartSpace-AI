import { Badge } from "@/components/ui/badge";
import { bookings } from "@/lib/mock-data";

export function BookingTable() {
  return (
    <div className="overflow-hidden rounded-lg border bg-card">
      <table className="w-full text-sm">
        <thead className="bg-muted/60 text-left">
          <tr>
            <th className="px-4 py-3 font-semibold">Guest</th>
            <th className="px-4 py-3 font-semibold">Space</th>
            <th className="px-4 py-3 font-semibold">Date</th>
            <th className="px-4 py-3 font-semibold">Amount</th>
            <th className="px-4 py-3 font-semibold">Status</th>
          </tr>
        </thead>
        <tbody>
          {bookings.map((booking) => (
            <tr className="border-t" key={`${booking.guest}-${booking.space}`}>
              <td className="px-4 py-3">{booking.guest}</td>
              <td className="px-4 py-3 text-muted-foreground">{booking.space}</td>
              <td className="px-4 py-3">{booking.date}</td>
              <td className="px-4 py-3 font-medium">{booking.amount}</td>
              <td className="px-4 py-3">
                <Badge className={booking.status === "Confirmed" ? "border-teal-400 text-teal-600" : ""}>{booking.status}</Badge>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
