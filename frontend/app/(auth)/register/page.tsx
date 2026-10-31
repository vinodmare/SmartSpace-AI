import Link from "next/link";

import { AuthForm } from "@/components/forms";

export default function RegisterPage() {
  return (
    <div className="w-full">
      <AuthForm mode="register" />
      <p className="mt-4 text-center text-sm text-muted-foreground">
        Already have an account? <Link className="font-medium text-primary" href="/login">Login</Link>
      </p>
    </div>
  );
}
