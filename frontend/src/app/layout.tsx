import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "CueSpark Interview Coach",
  description: "Benchmark-driven AI interview readiness for role-specific preparation",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
