import type { Metadata } from "next";
import type { ReactNode } from "react";
import { NirnayProvider } from "@/components/providers/nirnay-provider";
import { ToastViewport } from "@/components/ui/toast-viewport";
import "./globals.css";

export const metadata: Metadata = {
  title: "Nirnay Portal",
  description:
    "AI-assisted regulatory review workbench for structured evidence, protected data, and audit-ready decisions."
};

export default function RootLayout({
  children
}: Readonly<{
  children: ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        <NirnayProvider>
          {children}
          <ToastViewport />
        </NirnayProvider>
      </body>
    </html>
  );
}

