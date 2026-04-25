"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

import { mockBenchmarkComparison, mockSession } from "@/lib/demo/mock-data";

const primaryNav = [
  { href: "/demo", label: "Dashboard", token: "DB" },
  { href: "/demo/benchmark", label: "Benchmarks", token: "BM" },
  { href: "/demo/interview", label: "Interview Room", token: "IR" },
  { href: "/demo/report", label: "Reports", token: "RP" },
];

const secondaryNav = [
  { href: "/demo/report#prep-plan", label: "Prep Plan", token: "PP" },
  { href: "/demo#resources", label: "Resources", token: "RS" },
];

export function DemoProductShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();

  return (
    <div
      className="min-h-screen bg-[#f6f8fc] text-[#09142f]"
      style={
        {
          "--bg": "#f6f8fc",
          "--fg": "#09142f",
          "--muted": "#64748b",
          "--accent": "#2563eb",
          "--border": "#dbe3ef",
        } as React.CSSProperties
      }
    >
      <div className="lg:grid lg:min-h-screen lg:grid-cols-[240px_1fr]">
        <aside className="hidden border-r border-[#dbe3ef] bg-[#061a38] text-white lg:flex lg:flex-col">
          <div className="border-b border-white/10 px-7 py-6">
            <Link href="/demo" className="flex items-center gap-3 text-white">
              <BrandMark />
              <span className="text-2xl font-semibold tracking-tight">CueSpark</span>
            </Link>
            <div className="mt-2 text-xs text-blue-100/70">Hackathon demo preview</div>
          </div>

          <nav className="flex-1 space-y-1 px-4 py-5">
            {[...primaryNav, ...secondaryNav].map((item) => (
              <ShellNavLink
                key={item.href}
                href={item.href}
                label={item.label}
                token={item.token}
                active={isActive(pathname, item.href)}
              />
            ))}
          </nav>

          <div className="m-4 rounded-lg border border-white/10 bg-indigo-500/25 p-4">
            <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-white/10 text-sm font-semibold">
              AI
            </div>
            <div className="mt-4 text-sm font-semibold">Demo insights mode</div>
            <p className="mt-2 text-xs leading-5 text-blue-100/75">
              Static mock-data preview. No real APIs, recording, export, or account features.
            </p>
            <Link
              href="/setup"
              className="mt-4 inline-flex rounded border border-white/20 px-3 py-2 text-xs font-semibold text-white"
            >
              Real setup flow
            </Link>
          </div>
        </aside>

        <div className="min-w-0">
          <header className="sticky top-0 z-20 border-b border-[#dbe3ef] bg-white/95 backdrop-blur">
            <div className="flex min-h-16 flex-wrap items-center justify-between gap-3 px-4 py-3 lg:px-8">
              <div className="flex items-center gap-3 lg:hidden">
                <Link href="/demo" className="flex items-center gap-2 text-[#09142f]">
                  <BrandMark />
                  <span className="text-lg font-semibold">CueSpark</span>
                </Link>
              </div>

              <nav className="order-3 flex w-full gap-2 overflow-x-auto text-sm lg:order-1 lg:w-auto">
                {primaryNav.map((item) => (
                  <Link
                    key={item.href}
                    href={item.href}
                    className={`whitespace-nowrap rounded-md px-3 py-2 font-medium ${
                      isActive(pathname, item.href)
                        ? "bg-blue-50 text-blue-700"
                        : "text-slate-600 hover:bg-slate-100"
                    }`}
                  >
                    {item.label}
                  </Link>
                ))}
              </nav>

              <div className="order-2 flex flex-wrap items-center justify-end gap-2 text-sm lg:order-2">
                <StaticPill label="Role" value={mockSession.roleTitle} />
                <StaticPill label="Benchmark Set" value="Backend Engineer Set" />
                <div className="hidden h-9 w-9 items-center justify-center rounded-full border border-[#dbe3ef] bg-white text-xs font-semibold text-slate-600 sm:flex">
                  N
                </div>
                <div className="flex h-9 w-9 items-center justify-center rounded-full bg-[#061a38] text-xs font-semibold text-white">
                  AR
                </div>
              </div>
            </div>
          </header>

          <div className="border-b border-[#dbe3ef] bg-white px-4 py-2 text-xs text-slate-500 lg:px-8">
            <div className="flex flex-wrap items-center justify-between gap-2">
              <span>{mockSession.demoModeLabel}</span>
              <span>
                Hiring bar gap:{" "}
                <strong className="font-semibold text-red-600">
                  {mockBenchmarkComparison.hiringBarGap.toUpperCase()}
                </strong>
              </span>
            </div>
          </div>

          <div className="min-h-[calc(100vh-105px)]">{children}</div>
        </div>
      </div>
    </div>
  );
}

function ShellNavLink({
  href,
  label,
  token,
  active,
}: {
  href: string;
  label: string;
  token: string;
  active: boolean;
}) {
  return (
    <Link
      href={href}
      className={`flex items-center gap-3 rounded-lg px-4 py-3 text-sm font-medium transition-colors ${
        active ? "bg-indigo-500/35 text-white" : "text-blue-100/85 hover:bg-white/10 hover:text-white"
      }`}
    >
      <span className="flex h-7 w-7 items-center justify-center rounded-md border border-white/15 text-[10px] font-semibold">
        {token}
      </span>
      {label}
    </Link>
  );
}

function StaticPill({ label, value }: { label: string; value: string }) {
  return (
    <div className="hidden items-center gap-2 rounded-md border border-[#dbe3ef] bg-white px-3 py-2 text-xs text-slate-600 md:flex">
      <span className="font-medium text-slate-500">{label}:</span>
      <span className="font-semibold text-slate-800">{value}</span>
    </div>
  );
}

function BrandMark() {
  return (
    <span className="relative flex h-8 w-8 items-center justify-center rounded-lg bg-blue-600 text-white shadow-sm">
      <span className="absolute h-6 w-1 rounded-full bg-white/90" />
      <span className="absolute h-1 w-6 rounded-full bg-white/90" />
      <span className="h-2 w-2 rounded-full bg-white" />
    </span>
  );
}

function isActive(pathname: string, href: string) {
  const [path] = href.split("#");

  if (path === "/demo") {
    return pathname === "/demo";
  }

  return pathname === path || pathname.startsWith(`${path}/`);
}
