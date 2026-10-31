import * as React from "react";

import { cn } from "@/lib/utils";

export const Input = React.forwardRef<HTMLInputElement, React.InputHTMLAttributes<HTMLInputElement>>(
  ({ className, type, ...props }, ref) => (
    <input
      type={type}
      className={cn(
        "focus-ring flex h-11 w-full rounded-md border bg-background/80 px-3 py-2 text-sm shadow-sm transition placeholder:text-muted-foreground",
        className,
      )}
      ref={ref}
      {...props}
    />
  ),
);
Input.displayName = "Input";
