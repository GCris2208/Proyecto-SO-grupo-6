import { Trash2, Plus, Eraser } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import type { Proceso } from "@/lib/scheduler-types";

interface Props {
  procesos: Proceso[];
  onChange: (procesos: Proceso[]) => void;
}

export function ProcesosTable({ procesos, onChange }: Props) {
  const update = (index: number, patch: Partial<Proceso>) => {
    const next = procesos.map((p, i) => (i === index ? { ...p, ...patch } : p));
    onChange(next);
  };

  const remove = (index: number) => {
    onChange(procesos.filter((_, i) => i !== index));
  };

  const add = () => {
    const nextId = `P${procesos.length + 1}`;
    onChange([...procesos, { pid: nextId, llegada: 0, rafaga: 1, prioridad: 1 }]);
  };

  const clear = () => onChange([]);

  const inputCls =
    "no-spinner h-8 px-1.5 text-center text-xs w-full min-w-0";

  return (
    <div className="space-y-3">
      <div className="rounded-lg border border-border overflow-hidden">
        <Table className="table-fixed w-full">
          <TableHeader>
            <TableRow className="bg-muted/40 hover:bg-muted/40">
              <TableHead className="text-[10px] font-semibold uppercase tracking-wider px-2 text-center w-[22%]">PID</TableHead>
              <TableHead className="text-[10px] font-semibold uppercase tracking-wider px-1 text-center w-[22%]">Lleg.</TableHead>
              <TableHead className="text-[10px] font-semibold uppercase tracking-wider px-1 text-center w-[22%]">Ráf.</TableHead>
              <TableHead className="text-[10px] font-semibold uppercase tracking-wider px-1 text-center w-[22%]">Prio.</TableHead>
              <TableHead className="w-[12%] px-1"></TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {procesos.length === 0 && (
              <TableRow>
                <TableCell colSpan={5} className="text-center text-muted-foreground py-6 text-sm">
                  Sin procesos. Agrega uno o carga un test.
                </TableCell>
              </TableRow>
            )}
            {procesos.map((p, i) => (
              <TableRow key={i}>
                <TableCell className="py-1 px-1.5">
                  <Input
                    value={p.pid}
                    onChange={(e) => update(i, { pid: e.target.value })}
                    className={inputCls}
                  />
                </TableCell>
                <TableCell className="py-1 px-1">
                  <Input
                    type="number"
                    min={0}
                    value={p.llegada}
                    onChange={(e) => update(i, { llegada: Number(e.target.value) })}
                    className={inputCls}
                  />
                </TableCell>
                <TableCell className="py-1 px-1">
                  <Input
                    type="number"
                    min={1}
                    value={p.rafaga}
                    onChange={(e) => update(i, { rafaga: Number(e.target.value) })}
                    className={inputCls}
                  />
                </TableCell>
                <TableCell className="py-1 px-1">
                  <Input
                    type="number"
                    min={0}
                    value={p.prioridad}
                    onChange={(e) => update(i, { prioridad: Number(e.target.value) })}
                    className={inputCls}
                  />
                </TableCell>
                <TableCell className="py-1 px-1">
                  <Button
                    size="icon"
                    variant="ghost"
                    onClick={() => remove(i)}
                    className="h-7 w-7 text-destructive hover:text-destructive"
                    aria-label="Eliminar"
                  >
                    <Trash2 className="h-3.5 w-3.5" />
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
      <div className="grid grid-cols-2 gap-2">
        <Button variant="outline" size="sm" onClick={add}>
          <Plus className="h-4 w-4 mr-1" /> Agregar
        </Button>
        <Button
          variant="outline"
          size="sm"
          onClick={clear}
          disabled={procesos.length === 0}
          className="text-destructive hover:text-destructive"
        >
          <Eraser className="h-4 w-4 mr-1" /> Limpiar
        </Button>
      </div>
    </div>
  );
}
