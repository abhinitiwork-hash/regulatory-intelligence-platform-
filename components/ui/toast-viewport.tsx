"use client";

import { AnimatePresence, motion } from "framer-motion";
import { CheckCircle2, Info, TriangleAlert, XCircle } from "lucide-react";
import { useNirnay } from "@/components/providers/nirnay-provider";
import { Button } from "@/components/ui/button";

const iconMap = {
  info: Info,
  success: CheckCircle2,
  warning: TriangleAlert,
  danger: XCircle
};

export function ToastViewport() {
  const { toasts, dismissToast } = useNirnay();

  return (
    <div className="pointer-events-none fixed bottom-4 right-4 z-[60] flex w-full max-w-sm flex-col gap-3">
      <AnimatePresence>
        {toasts.map((toast) => {
          const Icon = iconMap[toast.tone];

          return (
            <motion.div
              animate={{ opacity: 1, x: 0 }}
              className="pointer-events-auto surface-subtle p-4"
              exit={{ opacity: 0, x: 24 }}
              initial={{ opacity: 0, x: 24 }}
              key={toast.id}
            >
              <div className="flex items-start gap-3">
                <span className="mt-0.5 rounded-full bg-[rgba(24,166,184,0.08)] p-2 text-nirnay-blue">
                  <Icon className="h-4 w-4" />
                </span>
                <div className="flex-1 space-y-1">
                  <p className="text-sm font-semibold text-nirnay-navy">{toast.title}</p>
                  <p className="text-sm leading-6 text-nirnay-slate">{toast.description}</p>
                </div>
                <Button
                  className="h-8 min-h-0 px-2"
                  onClick={() => dismissToast(toast.id)}
                  variant="ghost"
                >
                  Dismiss
                </Button>
              </div>
            </motion.div>
          );
        })}
      </AnimatePresence>
    </div>
  );
}

