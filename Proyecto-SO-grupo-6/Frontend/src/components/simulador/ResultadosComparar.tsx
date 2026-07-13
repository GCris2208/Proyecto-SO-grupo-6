import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Trophy } from "lucide-react";
import type { SimulacionComparar, Criterio } from "@/lib/scheduler-types";
import { CRITERIO_LABEL } from "@/lib/scheduler-types";

const fmt = (n: number) => Number(n).toFixed(2);

export function ResultadosComparar({
  data,
  criterio1,
  criterio2,
}: {
  data: SimulacionComparar;
  criterio1: Criterio;
  criterio2: Criterio;
}) {
  return (
    <div className="space-y-6">
      <Card className="bg-gradient-primary border-0 shadow-glow">
        <CardContent className="p-6 flex items-center gap-4">
          <Trophy className="h-10 w-10 text-primary-foreground" />
          <div>
            <div className="text-xs uppercase tracking-wider text-primary-foreground/80">
              Ganador por {CRITERIO_LABEL[criterio1]}
            </div>
            <div className="text-2xl font-bold text-primary-foreground">
              🏆 {data.ganadores.join(", ")}
            </div>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">Ranking Comparativo</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="rounded-md border border-border overflow-hidden">
            <Table>
              <TableHeader>
                <TableRow className="bg-muted/40 hover:bg-muted/40">
                  <TableHead>#</TableHead>
                  <TableHead>Algoritmo</TableHead>
                  <TableHead>{CRITERIO_LABEL[criterio1]}</TableHead>
                  <TableHead>{CRITERIO_LABEL[criterio2]}</TableHead>
                  <TableHead>AWT</TableHead>
                  <TableHead>ATT</TableHead>
                  <TableHead>ART</TableHead>
                  <TableHead>Interrup.</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {data.ranking.map((r, i) => {
                  const isWinner = data.ganadores.includes(r.algoritmo);
                  return (
                    <TableRow
                      key={r.algoritmo}
                      className={isWinner ? "bg-primary/10 hover:bg-primary/15" : ""}
                    >
                      <TableCell className="font-mono">{i + 1}</TableCell>
                      <TableCell className="font-semibold">
                        {isWinner && "🏆 "}
                        {r.algoritmo}
                      </TableCell>
                      <TableCell>{fmt(r.criterio_principal)}</TableCell>
                      <TableCell>{fmt(r.criterio_secundario)}</TableCell>
                      <TableCell>{fmt(r.todas_las_metricas.awt)}</TableCell>
                      <TableCell>{fmt(r.todas_las_metricas.att)}</TableCell>
                      <TableCell>{fmt(r.todas_las_metricas.art)}</TableCell>
                      <TableCell>{r.todas_las_metricas.interrupciones}</TableCell>
                    </TableRow>
                  );
                })}
              </TableBody>
            </Table>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
