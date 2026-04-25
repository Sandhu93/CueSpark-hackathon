export function DashboardCard({
  children,
  className = "",
}: {
  children: React.ReactNode;
  className?: string;
}) {
  return (
    <section className={`rounded-lg border border-[var(--border)] bg-white p-5 shadow-sm ${className}`}>
      {children}
    </section>
  );
}

export function MetricCard({
  title,
  value,
  suffix = "/100",
  detail,
  trend,
  tone = "blue",
}: {
  title: string;
  value: number | string;
  suffix?: string;
  detail: string;
  trend?: number[];
  tone?: "blue" | "purple" | "red" | "amber" | "green";
}) {
  return (
    <DashboardCard>
      <div className="flex items-start justify-between gap-3">
        <div>
          <div className="text-sm font-semibold text-slate-800">{title}</div>
          <div className={`mt-3 text-4xl font-semibold ${toneText(tone)}`}>
            {value}
            {suffix ? <span className="ml-1 text-base font-medium text-slate-500">{suffix}</span> : null}
          </div>
        </div>
        <span className={`rounded-full px-2 py-1 text-xs font-semibold ${toneBadge(tone)}`}>
          demo
        </span>
      </div>
      {trend ? <MiniTrendLine values={trend} tone={tone} /> : null}
      <p className="mt-3 text-sm leading-6 text-[var(--muted)]">{detail}</p>
    </DashboardCard>
  );
}

export function MiniTrendLine({ values, tone = "blue" }: { values: number[]; tone?: "blue" | "purple" | "red" | "amber" | "green" }) {
  const max = Math.max(...values);
  const min = Math.min(...values);
  const range = Math.max(max - min, 1);
  const points = values
    .map((value, index) => {
      const x = (index / Math.max(values.length - 1, 1)) * 100;
      const y = 34 - ((value - min) / range) * 24;
      return `${x},${y}`;
    })
    .join(" ");

  return (
    <svg className="mt-4 h-10 w-full" viewBox="0 0 100 40" preserveAspectRatio="none" aria-hidden="true">
      <polyline fill="none" stroke={toneStroke(tone)} strokeWidth="3" points={points} />
      <line x1="0" y1="36" x2="100" y2="36" stroke="#e2e8f0" strokeWidth="1" />
    </svg>
  );
}

export function ProgressBar({
  value,
  tone = "blue",
}: {
  value: number;
  tone?: "blue" | "purple" | "red" | "amber" | "green";
}) {
  return (
    <div className="h-2 overflow-hidden rounded-full bg-slate-100">
      <div className={`h-full rounded-full ${toneBg(tone)}`} style={{ width: `${value}%` }} />
    </div>
  );
}

export function ScoreGauge({
  value,
  tone = "amber",
}: {
  value: number;
  tone?: "blue" | "purple" | "red" | "amber" | "green";
}) {
  return (
    <div className="relative mx-auto flex h-28 w-44 items-end justify-center overflow-hidden">
      <div className="absolute bottom-0 h-44 w-44 rounded-full border-[18px] border-slate-100" />
      <div
        className={`absolute bottom-0 h-44 w-44 rounded-full border-[18px] border-transparent ${gaugeBorder(tone)}`}
        style={{
          clipPath: "polygon(0 50%, 100% 50%, 100% 100%, 0 100%)",
          transform: `rotate(${Math.round((value / 100) * 180) - 180}deg)`,
        }}
      />
      <div className="relative mb-2 text-center">
        <div className="text-3xl font-semibold text-slate-900">{value}</div>
        <div className="text-xs text-slate-500">readiness</div>
      </div>
    </div>
  );
}

export function EvidenceDistribution({
  items,
}: {
  items: Array<{ label: string; count: number; percent: number; tone: "strong" | "weak" | "missing" }>;
}) {
  return (
    <div className="space-y-4">
      <div className="flex h-4 overflow-hidden rounded-full bg-slate-100">
        {items.map((item) => (
          <div
            key={item.label}
            className={evidenceBg(item.tone)}
            style={{ width: `${item.percent}%` }}
            title={`${item.label}: ${item.percent}%`}
          />
        ))}
      </div>
      <div className="space-y-3">
        {items.map((item) => (
          <div key={item.label} className="flex items-center justify-between gap-3 text-sm">
            <div className="flex items-center gap-2">
              <span className={`h-2.5 w-2.5 rounded-full ${evidenceBg(item.tone)}`} />
              <span className="text-slate-700">{item.label}</span>
            </div>
            <span className="font-semibold text-slate-900">
              {item.count} ({item.percent}%)
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}

function toneText(tone: string) {
  if (tone === "purple") return "text-violet-700";
  if (tone === "red") return "text-red-600";
  if (tone === "amber") return "text-amber-600";
  if (tone === "green") return "text-emerald-600";
  return "text-blue-700";
}

function toneBadge(tone: string) {
  if (tone === "red") return "bg-red-50 text-red-700";
  if (tone === "amber") return "bg-amber-50 text-amber-700";
  if (tone === "green") return "bg-emerald-50 text-emerald-700";
  if (tone === "purple") return "bg-violet-50 text-violet-700";
  return "bg-blue-50 text-blue-700";
}

function toneStroke(tone: string) {
  if (tone === "purple") return "#7c3aed";
  if (tone === "red") return "#dc2626";
  if (tone === "amber") return "#d97706";
  if (tone === "green") return "#059669";
  return "#2563eb";
}

function toneBg(tone: string) {
  if (tone === "purple") return "bg-violet-600";
  if (tone === "red") return "bg-red-500";
  if (tone === "amber") return "bg-amber-500";
  if (tone === "green") return "bg-emerald-500";
  return "bg-blue-600";
}

function gaugeBorder(tone: string) {
  if (tone === "green") return "border-t-emerald-500 border-r-emerald-500";
  if (tone === "red") return "border-t-red-500 border-r-red-500";
  if (tone === "purple") return "border-t-violet-600 border-r-violet-600";
  if (tone === "blue") return "border-t-blue-600 border-r-blue-600";
  return "border-t-amber-500 border-r-amber-500";
}

function evidenceBg(tone: "strong" | "weak" | "missing") {
  if (tone === "strong") return "bg-emerald-500";
  if (tone === "weak") return "bg-amber-400";
  return "bg-red-500";
}
