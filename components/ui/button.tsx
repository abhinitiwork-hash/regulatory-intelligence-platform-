"use client";

import { ButtonHTMLAttributes, forwardRef } from "react";
import { cn } from "@/lib/utils";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "ghost";
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(function Button(
  { className, variant = "primary", ...props },
  ref
) {
  return (
    <button
      className={cn(
        variant === "primary" && "action-button",
        variant === "secondary" && "ghost-button",
        variant === "ghost" &&
          "inline-flex min-h-10 items-center justify-center gap-2 rounded-xl px-3 text-sm font-medium text-nirnay-slate transition hover:bg-[rgba(11,63,117,0.06)] hover:text-nirnay-blue",
        className
      )}
      ref={ref}
      {...props}
    />
  );
});

