import type { GanttBlock } from "@/lib/scheduler-types";

const PALETTE = [
  "var(--color-chart-1)",
  "var(--color-chart-2)",
  "var(--color-chart-3)",
  "var(--color-chart-4)",
  "var(--color-chart-5)",
];

function colorFor(pid: string, index: number) {
  if (pid.toLowerCase() === "idle" || pid === "-") return "var(--color-muted)";
  return PALETTE[index % PALETTE.length];
}

export function GanttChart({ gantt }: { gantt: GanttBlock[] }) {
  if (!gantt || gantt.length === 0) {
    return <p className="text-sm text-muted-foreground">Sin datos de Gantt.</p>;
  }

  const totalDuration = gantt.reduce((sum, b) => sum + (b.end - b.start), 0);
  const pidIndex = new Map<string, number>();
  gantt.forEach((b) => {
    if (!pidIndex.has(b.pid)) pidIndex.set(b.pid, pidIndex.size);
  });

  return (
    <div className="space-y-2">
      <div className="flex w-full rounded-md overflow-hidden border border-border h-14">
        {gantt.map((b, i) => {
          const width = ((b.end - b.start) / totalDuration) * 100;
          const bg = colorFor(b.pid, pidIndex.get(b.pid) ?? 0);
          return (
            <div
              key={i}
              className="flex items-center justify-center text-xs font-bold text-primary-foreground border-r border-background/40 last:border-r-0 transition-all hover:brightness-110"
              style={{ width: `${width}%`, background: bg, minWidth: "24px" }}
              title={`${b.pid}: ${b.start} → ${b.end}`}
            >
              {b.pid}
            </div>
          );
        })}
      </div>
      <div className="relative flex w-full text-[10px] text-muted-foreground font-mono">
        {gantt.map((b, i) => {
          const width = ((b.end - b.start) / totalDuration) * 100;
          return (
            <div key={i} className="relative" style={{ width: `${width}%`, minWidth: "24px" }}>
              <span className="absolute -left-1 top-0">{b.start}</span>
              {i === gantt.length - 1 && (
                <span className="absolute right-0 top-0">{b.end}</span>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
