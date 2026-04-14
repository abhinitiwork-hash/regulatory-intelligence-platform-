"use client";

import { animate, useInView } from "framer-motion";
import { useEffect, useRef, useState } from "react";

export function AnimatedCounter({
  value,
  suffix
}: {
  value: number;
  suffix?: string;
}) {
  const ref = useRef<HTMLSpanElement | null>(null);
  const inView = useInView(ref, { once: true, margin: "-40px" });
  const [display, setDisplay] = useState(0);

  useEffect(() => {
    if (!inView) {
      return;
    }

    const controls = animate(0, value, {
      duration: 1.2,
      ease: "easeOut",
      onUpdate: (latest) => {
        setDisplay(Math.round(latest));
      }
    });

    return () => controls.stop();
  }, [inView, value]);

  return <span ref={ref}>{`${display}${suffix ?? ""}`}</span>;
}
