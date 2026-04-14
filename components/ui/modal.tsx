"use client";

import { AnimatePresence, motion } from "framer-motion";
import { ReactNode } from "react";
import { X } from "lucide-react";
import { Button } from "@/components/ui/button";

export function Modal({
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
          className="fixed inset-0 z-50 flex items-center justify-center bg-[rgba(7,30,61,0.5)] px-4 py-10 backdrop-blur-sm"
          exit={{ opacity: 0 }}
          initial={{ opacity: 0 }}
          onClick={onClose}
        >
          <motion.div
            animate={{ opacity: 1, scale: 1, y: 0 }}
            className="surface max-h-[85vh] w-full max-w-4xl overflow-hidden"
            exit={{ opacity: 0, scale: 0.98, y: 12 }}
            initial={{ opacity: 0, scale: 0.98, y: 12 }}
            onClick={(event) => event.stopPropagation()}
          >
            <div className="flex items-start justify-between gap-4 border-b border-[rgba(11,63,117,0.1)] px-6 py-5">
              <div className="space-y-2">
                <p className="eyebrow">Interactive Detail</p>
                <h3 className="text-2xl font-semibold tracking-tight text-nirnay-navy">{title}</h3>
                {description ? <p className="max-w-2xl text-sm text-nirnay-slate">{description}</p> : null}
              </div>
              <Button onClick={onClose} variant="ghost">
                <X className="h-4 w-4" />
              </Button>
            </div>
            <div className="max-h-[calc(85vh-110px)] overflow-y-auto px-6 py-5">{children}</div>
          </motion.div>
        </motion.div>
      ) : null}
    </AnimatePresence>
  );
}

