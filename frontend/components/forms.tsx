"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { CalendarDays, Mail, Send } from "lucide-react";
import { useForm } from "react-hook-form";
import { z } from "zod";

import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

const authSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8).optional(),
});

export function AuthForm({ mode }: { mode: "login" | "register" | "forgot" }) {
  const { register, formState } = useForm<z.infer<typeof authSchema>>({
    resolver: zodResolver(authSchema),
  });
  return (
    <Card className="mx-auto w-full max-w-md">
      <CardContent className="grid gap-4 p-6">
        <div>
          <h1 className="text-2xl font-semibold capitalize">{mode === "forgot" ? "Reset password" : mode}</h1>
          <p className="mt-1 text-sm text-muted-foreground">Secure access for customers, owners, and admins.</p>
        </div>
        <div className="grid gap-2">
          <Label htmlFor="email">Email</Label>
          <Input id="email" type="email" placeholder="you@company.com" {...register("email")} />
          {formState.errors.email && <p className="text-sm text-destructive">Enter a valid email.</p>}
        </div>
        {mode !== "forgot" && (
          <div className="grid gap-2">
            <Label htmlFor="password">Password</Label>
            <Input id="password" type="password" placeholder="Minimum 8 characters" {...register("password")} />
          </div>
        )}
        <Button variant="premium">
          <Mail />
          {mode === "forgot" ? "Send reset link" : "Continue"}
        </Button>
      </CardContent>
    </Card>
  );
}

export function SpaceForm({ title }: { title: string }) {
  return (
    <Card>
      <CardContent className="grid gap-4 p-6">
        <h1 className="text-2xl font-semibold">{title}</h1>
        <div className="grid gap-4 md:grid-cols-2">
          {["Space name", "Space type", "City", "Hourly price", "Capacity", "Amenities"].map((field) => (
            <div className="grid gap-2" key={field}>
              <Label htmlFor={field}>{field}</Label>
              <Input id={field} placeholder={field} />
            </div>
          ))}
        </div>
        <Button className="w-fit">
          <Send />
          Save space
        </Button>
      </CardContent>
    </Card>
  );
}

export function BookingCard() {
  return (
    <Card>
      <CardContent className="grid gap-4 p-6">
        <h2 className="text-xl font-semibold">Complete booking</h2>
        {["Date", "Start time", "Duration", "Guests"].map((field) => (
          <div className="grid gap-2" key={field}>
            <Label htmlFor={field}>{field}</Label>
            <Input id={field} placeholder={field} />
          </div>
        ))}
        <Button variant="premium">
          <CalendarDays />
          Reserve space
        </Button>
      </CardContent>
    </Card>
  );
}
