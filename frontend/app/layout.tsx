import type { Metadata } from "next";
import { Inter } from "next/font/google";

import { AppProviders } from "@/providers/app-providers";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "SmartSpace AI",
  description: "AI-powered marketplace for renting and managing spaces.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>
        <AppProviders>{children}</AppProviders>
      </body>
    </html>
  );
}
