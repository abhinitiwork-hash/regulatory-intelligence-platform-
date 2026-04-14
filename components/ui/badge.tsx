import { HTMLAttributes } from "react";
import { cn } from "@/lib/utils";

export function Badge({
  className,
  tone,
  ...props
}: HTMLAttributes<HTMLSpanElement> & {
  tone?: "blue" | "slate" | "green" | "amber" | "red" | "cyan";
}) {
  return (
    <span
      className={cn(
        "inline-flex items-center gap-2 rounded-full border border-[rgba(11,63,117,0.12)] bg-white/90 px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.12em] text-nirnay-slate",
        tone === "blue" && "border-[rgba(24,166,184,0.18)] bg-[rgba(24,166,184,0.08)] text-nirnay-blue",
        tone === "cyan" && "border-[rgba(24,166,184,0.18)] bg-[rgba(24,166,184,0.08)] text-nirnay-cyan",
        tone === "amber" && "border-[rgba(245,166,35,0.2)] bg-[rgba(245,166,35,0.1)] text-[var(--nirnay-amber)]",
        tone === "green" && "border-[rgba(46,125,50,0.2)] bg-[rgba(46,125,50,0.08)] text-[var(--nirnay-green)]",
        tone === "red" && "border-[rgba(198,40,40,0.18)] bg-[rgba(198,40,40,0.08)] text-[var(--nirnay-red)]",
        tone === "slate" && "border-[rgba(11,63,117,0.12)] bg-[rgba(11,63,117,0.04)] text-nirnay-slate",
        className
      )}
      {...props}
    />
  );
}
