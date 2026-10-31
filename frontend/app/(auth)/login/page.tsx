import Link from "next/link";

import { AuthForm } from "@/components/forms";

export default function LoginPage() {
  return (
    <div className="w-full">
      <AuthForm mode="login" />
      <p className="mt-4 text-center text-sm text-muted-foreground">
        New to SmartSpace AI? <Link className="font-medium text-primary" href="/register">Create account</Link>
      </p>
    </div>
  );
}
