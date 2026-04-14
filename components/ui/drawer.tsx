"use client";

import { AnimatePresence, motion } from "framer-motion";
import { ReactNode } from "react";
import { X } from "lucide-react";
import { Button } from "@/components/ui/button";

export function Drawer({
  open,
  onClose,
  title,
  children,
  description
}: {
  open: boolean;
  onClose: () => void;
  title: string;
  description?: string;
  children: ReactNode;
}) {
  return (
    <AnimatePresence>
      {open ? (
        <motion.div
          animate={{ opacity: 1 }}
          className="fixed inset-0 z-50 bg-[rgba(7,30,61,0.42)] backdrop-blur-sm"
          exit={{ opacity: 0 }}
          initial={{ opacity: 0 }}
          onClick={onClose}
        >
          <motion.aside
            animate={{ x: 0 }}
            className="absolute right-0 top-0 h-full w-full max-w-xl overflow-hidden border-l border-white/10 bg-white/96 shadow-[0_24px_50px_rgba(7,30,61,0.18)]"
            exit={{ x: "100%" }}
            initial={{ x: "100%" }}
            onClick={(event) => event.stopPropagation()}
          >
            <div className="flex items-start justify-between gap-4 border-b border-[rgba(11,63,117,0.1)] px-6 py-5">
              <div className="space-y-2">
                <p className="eyebrow">Detail Panel</p>
                <h3 className="text-2xl font-semibold tracking-tight text-nirnay-navy">{title}</h3>
                {description ? <p className="text-sm text-nirnay-slate">{description}</p> : null}
              </div>
              <Button onClick={onClose} variant="ghost">
                <X className="h-4 w-4" />
              </Button>
            </div>
            <div className="h-[calc(100vh-110px)] overflow-y-auto px-6 py-5">{children}</div>
          </motion.aside>
        </motion.div>
      ) : null}
    </AnimatePresence>
  );
}

