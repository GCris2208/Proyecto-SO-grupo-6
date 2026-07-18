import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { GanttChart } from "./GanttChart";
import type { SimulacionNormal } from "@/lib/scheduler-types";
import { Clock, Timer, Hourglass, Zap, Cpu } from "lucide-react";

const fmt = (n: number) => Number(n).toFixed(2);

function MetricCard({
  icon: Icon,
  label,
  value,
  suffix,
}: {
  icon: React.ComponentType<{ className?: string }>;
  label: string;
  value: string;
  suffix?: string;
}) {
  return (
    <Card className="bg-card/60 border-border/60">
      <CardContent className="p-4">
        <div className="flex items-center gap-2 text-muted-foreground text-xs uppercase tracking-wider mb-2">
          <Icon className="h-3.5 w-3.5" />
          {label}
        </div>
        <div className="text-2xl font-bold text-foreground">
          {value}
          {suffix && <span className="text-sm text-muted-foreground ml-1">{suffix}</span>}
        </div>
      </CardContent>
    </Card>
  );
}

export function ResultadosNormal({ data }: { data: SimulacionNormal }) {
  const { procesos, metricas, gantt } = data;

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
        <MetricCard icon={Clock} label="Tiempo Total" value={fmt(metricas.tiempo_total)} />
        <MetricCard icon={Timer} label="Prom. Retorno" value={fmt(metricas.promedio_retorno)} />
        <MetricCard icon={Hourglass} label="Prom. Espera" value={fmt(metricas.promedio_espera)} />
        <MetricCard icon={Zap} label="Prom. Respuesta" value={fmt(metricas.promedio_respuesta)} />
        <MetricCard icon={Cpu} label="Utilización CPU" value={fmt(metricas.utilizacion_cpu)} suffix="%" />
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">Diagrama de Gantt</CardTitle>
        </CardHeader>
        <CardContent>
          <GanttChart gantt={gantt} />
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">Detalle por Proceso</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="rounded-md border border-border overflow-hidden">
            <Table>
              <TableHeader>
                <TableRow className="bg-muted/40 hover:bg-muted/40">
                  <TableHead>PID</TableHead>
                  <TableHead>Finalización</TableHead>
                  <TableHead>Retorno</TableHead>
                  <TableHead>Espera</TableHead>
                  <TableHead>Respuesta</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {procesos.map((p) => (
                  <TableRow key={p.pid}>
                    <TableCell className="font-semibold text-primary">{p.pid}</TableCell>
                    <TableCell>{fmt(p.completion_time)}</TableCell>
                    <TableCell>{fmt(p.turnaround_time)}</TableCell>
                    <TableCell>{fmt(p.waiting_time)}</TableCell>
                    <TableCell>{fmt(p.response_time)}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        </CardContent>
      </Card>

      {(metricas.procesos_convoy?.length > 0 || metricas.interrupciones > 0) && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {metricas.procesos_convoy?.length > 0 && (
            <Card className="border-warning/50 bg-warning/5">
              <CardContent className="p-4">
                <div className="text-xs uppercase tracking-wider text-warning mb-1">
                  Procesos en Convoy
                </div>
                <div className="text-sm font-medium">{metricas.procesos_convoy.join(", ")}</div>
              </CardContent>
            </Card>
          )}
          <Card>
            <CardContent className="p-4">
              <div className="text-xs uppercase tracking-wider text-muted-foreground mb-1">
                Cambios de Contexto · Tiempo Ocioso
              </div>
              <div className="text-sm font-medium">
                {metricas.interrupciones} Cambios de Contexto · {fmt(metricas.tiempo_ocioso)} ocioso
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
}
