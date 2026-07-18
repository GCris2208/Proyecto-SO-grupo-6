import { createFileRoute } from "@tanstack/react-router";
import { useMemo, useRef, useState } from "react";
import { Cpu, Play, Upload, FlaskConical, Loader2, BarChart3 } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { toast } from "sonner";
import { Toaster } from "@/components/ui/sonner";

import { ProcesosTable } from "@/components/simulador/ProcesosTable";
import { ResultadosNormal } from "@/components/simulador/ResultadosNormal";
import { ResultadosComparar } from "@/components/simulador/ResultadosComparar";
import type {
  Algoritmo,
  Criterio,
  Proceso,
  SimulacionComparar,
  SimulacionNormal,
} from "@/lib/scheduler-types";

export const Route = createFileRoute("/")({
  component: SimuladorPage,
});

const TEST_1: Proceso[] = [
  { pid: "P1", llegada: 0, rafaga: 8, prioridad: 3 },
  { pid: "P2", llegada: 1, rafaga: 4, prioridad: 1 },
  { pid: "P3", llegada: 2, rafaga: 9, prioridad: 4 },
  { pid: "P4", llegada: 3, rafaga: 5, prioridad: 2 },
];

const TEST_2: Proceso[] = [
  { pid: "P1", llegada: 0, rafaga: 10, prioridad: 2 },
  { pid: "P2", llegada: 2, rafaga: 3,  prioridad: 1 },
  { pid: "P3", llegada: 4, rafaga: 6,  prioridad: 3 },
  { pid: "P4", llegada: 6, rafaga: 1,  prioridad: 1 },
  { pid: "P5", llegada: 8, rafaga: 4,  prioridad: 2 },
];

const TEST_3: Proceso[] = [
  { pid: "P1", llegada: 0, rafaga: 20, prioridad: 3 },
  { pid: "P2", llegada: 1, rafaga: 2, prioridad: 2 },
  { pid: "P3", llegada: 2, rafaga: 2, prioridad: 1 },
  { pid: "P4", llegada: 4, rafaga: 18, prioridad: 1 },
  { pid: "P5", llegada: 5, rafaga: 1, prioridad: 1 },
];

// Edge Case: Llegadas Simultáneas (Prueba los desempates)
const TEST_4: Proceso[] = [
  { pid: "P1", llegada: 0, rafaga: 4, prioridad: 3 },
  { pid: "P2", llegada: 0, rafaga: 2, prioridad: 1 },
  { pid: "P3", llegada: 0, rafaga: 5, prioridad: 4 },
  { pid: "P4", llegada: 0, rafaga: 1, prioridad: 2 },
  { pid: "P5", llegada: 0, rafaga: 3, prioridad: 5 },
];

// Edge Case: Ráfagas Extremas (Desbalance masivo para Round Robin)
const TEST_5: Proceso[] = [
  { pid: "P1", llegada: 0, rafaga: 1, prioridad: 2 },
  { pid: "P2", llegada: 1, rafaga: 15, prioridad: 1 },
  { pid: "P3", llegada: 2, rafaga: 1, prioridad: 3 },
  { pid: "P4", llegada: 3, rafaga: 1, prioridad: 2 },
  { pid: "P5", llegada: 4, rafaga: 1, prioridad: 1 },
];

const API_URL = "http://localhost:8000/simulate";

function parseArchivo(text: string): Proceso[] {
  return text
    .split(/\r?\n/)
    .map((l) => l.trim())
    .filter((l) => l.length > 0 && !l.startsWith("#"))
    .map((line) => {
      const parts = line.split(",").map((p) => p.trim());
      const [pid, llegada, rafaga, prioridad] = parts;
      return {
        pid: pid || "P?",
        llegada: Number(llegada) || 0,
        rafaga: Number(rafaga) || 1,
        prioridad: Number(prioridad) || 1,
      };
    })
    .filter((p) => !Number.isNaN(p.llegada) && !Number.isNaN(p.rafaga));
}

function procesosToText(procesos: Proceso[]): string {
  return procesos
    .map((p) => `${p.pid}, ${p.llegada}, ${p.rafaga}, ${p.prioridad}`)
    .join("\n");
}

function SimuladorPage() {
  const [procesos, setProcesos] = useState<Proceso[]>(TEST_1);
  const [algoritmo, setAlgoritmo] = useState<Algoritmo>("FCFS");
  const [quantum, setQuantum] = useState<number>(3);
  const [criterio1, setCriterio1] = useState<Criterio>("awt");
  const [criterio2, setCriterio2] = useState<Criterio>("art");
  const [loading, setLoading] = useState(false);
  const [resultadoNormal, setResultadoNormal] = useState<SimulacionNormal | null>(null);
  const [resultadoComparar, setResultadoComparar] = useState<SimulacionComparar | null>(null);
  const fileRef = useRef<HTMLInputElement>(null);

  const modo = algoritmo === "comparar" ? "comparar" : "normal";
  const mostrarQuantum = algoritmo === "rr" || algoritmo === "comparar";
  const mostrarCriterios = algoritmo === "comparar";

  const criterio2Options = useMemo(
    () => (["awt", "att", "art"] as Criterio[]).filter((c) => c !== criterio1),
    [criterio1],
  );

  const handleFile = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = () => {
      const text = String(reader.result || "");
      const parsed = parseArchivo(text);
      if (parsed.length === 0) {
        toast.error("El archivo no contiene procesos válidos.");
        return;
      }
      setProcesos(parsed);
      toast.success(`${parsed.length} procesos cargados desde ${file.name}.`);
    };
    reader.onerror = () => toast.error("No se pudo leer el archivo.");
    reader.readAsText(file);
    e.target.value = "";
  };

  const ejecutar = async () => {
    if (procesos.length === 0) {
      toast.error("Agrega al menos un proceso.");
      return;
    }
    setLoading(true);
    setResultadoNormal(null);
    setResultadoComparar(null);

    const body: Record<string, unknown> = {
      procesos: procesosToText(procesos),
      algoritmo,
    };
    if (mostrarQuantum) body.quantum = quantum;
    if (mostrarCriterios) {
      body.criterio_1 = criterio1;
      body.criterio_2 = criterio2;
    }

    try {
      const res = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      if (modo === "comparar") {
        setResultadoComparar(data as SimulacionComparar);
      } else {
        setResultadoNormal(data as SimulacionNormal);
      }
      toast.success("Simulación completada.");
    } catch (err) {
      const msg = err instanceof Error ? err.message : "Error desconocido";
      toast.error(`No se pudo ejecutar la simulación: ${msg}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background">
      <Toaster richColors position="top-right" theme="dark" />

      <header className="border-b border-border/60 bg-card/40 backdrop-blur">
        <div className="max-w-[1600px] mx-auto px-6 py-4 flex items-center gap-3">
          <div className="bg-gradient-primary p-2 rounded-lg shadow-glow">
            <Cpu className="h-5 w-5 text-primary-foreground" />
          </div>
          <div>
            <h1 className="text-lg font-bold tracking-tight">
              Simulador de Algoritmos de Planificación de CPU
            </h1>
            <p className="text-xs text-muted-foreground">
              FCFS · SJF · SRTF · Prioridad · Round Robin · Comparación
            </p>
          </div>
        </div>
      </header>

      <main className="max-w-[1600px] mx-auto px-6 py-6 grid grid-cols-1 lg:grid-cols-[420px_1fr] gap-6">
        {/* Panel Izquierdo */}
        <aside className="space-y-5">
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-sm">Configuración de Simulación</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label className="text-xs uppercase tracking-wider text-muted-foreground">
                  Algoritmo
                </Label>
                <Select value={algoritmo} onValueChange={(v) => setAlgoritmo(v as Algoritmo)}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="FCFS">FCFS · First Come First Served</SelectItem>
                    <SelectItem value="SJF">SJF · Shortest Job First</SelectItem>
                    <SelectItem value="SRTF">SRTF · Shortest Remaining Time</SelectItem>
                    <SelectItem value="Prioridad">Prioridad</SelectItem>
                    <SelectItem value="rr">Round Robin</SelectItem>
                    <SelectItem value="comparar">Comparar Todos</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              {mostrarQuantum && (
                <div className="space-y-2">
                  <Label className="text-xs uppercase tracking-wider text-muted-foreground">
                    Quantum
                  </Label>
                  <Input
                    type="number"
                    min={1}
                    value={quantum}
                    onChange={(e) => setQuantum(Number(e.target.value) || 1)}
                    className="no-spinner"
                  />
                </div>
              )}

              {mostrarCriterios && (
                <div className="grid grid-cols-2 gap-2">
                  <div className="space-y-2">
                    <Label className="text-xs uppercase tracking-wider text-muted-foreground">
                      Criterio 1
                    </Label>
                    <Select
                      value={criterio1}
                      onValueChange={(v) => {
                        const nv = v as Criterio;
                        setCriterio1(nv);
                        if (criterio2 === nv) {
                          setCriterio2((["awt", "att", "art"] as Criterio[]).find((c) => c !== nv)!);
                        }
                      }}
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="awt">Menor Espera (AWT)</SelectItem>
                        <SelectItem value="att">Menor Retorno (ATT)</SelectItem>
                        <SelectItem value="art">Menor Respuesta (ART)</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="space-y-2">
                    <Label className="text-xs uppercase tracking-wider text-muted-foreground">
                      Criterio 2
                    </Label>
                    <Select value={criterio2} onValueChange={(v) => setCriterio2(v as Criterio)}>
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        {criterio2Options.map((c) => (
                          <SelectItem key={c} value={c}>
                            {c === "awt" && "Menor Espera (AWT)"}
                            {c === "att" && "Menor Retorno (ATT)"}
                            {c === "art" && "Menor Respuesta (ART)"}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                </div>
              )}

              <Button
                onClick={ejecutar}
                disabled={loading}
                className="w-full bg-gradient-primary hover:brightness-110 shadow-elegant text-primary-foreground font-semibold"
                size="lg"
              >
                {loading ? (
                  <>
                    <Loader2 className="h-4 w-4 mr-2 animate-spin" /> Ejecutando…
                  </>
                ) : (
                  <>
                    <Play className="h-4 w-4 mr-2" /> Ejecutar Simulación
                  </>
                )}
              </Button>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-sm flex items-center gap-2">
                <FlaskConical className="h-4 w-4 text-primary" />
                Datos de Prueba
              </CardTitle>
            </CardHeader>
            <CardContent className="grid grid-cols-2 gap-2">
              
              <Button variant="secondary" size="sm" onClick={() => setProcesos(TEST_1)}>
                Test 1 · Básico
              </Button>
              
              <Button variant="secondary" size="sm" onClick={() => setProcesos(TEST_2)}>
                Test 2 · Básico 2
              </Button>
              
              <Button variant="secondary" size="sm" onClick={() => setProcesos(TEST_3)}>
                Test 3 ·  Convoy
              </Button>
              
              <Button variant="secondary" size="sm" onClick={() => setProcesos(TEST_4)}>
                Test 4 · Llegadas Simultáneas
              </Button>
              
              <Button variant="secondary" size="sm" onClick={() => setProcesos(TEST_5)}>
                Test 5 · Ráfagas
              </Button>

            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-sm flex items-center gap-2">
                <Upload className="h-4 w-4 text-primary" />
                Cargar Archivo
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-2">
              <input
                ref={fileRef}
                type="file"
                accept=".txt,.csv"
                onChange={handleFile}
                className="hidden"
              />
              <Button
                variant="outline"
                size="sm"
                className="w-full"
                onClick={() => fileRef.current?.click()}
              >
                <Upload className="h-4 w-4 mr-2" /> Seleccionar .txt o .csv
              </Button>
              <p className="text-[11px] text-muted-foreground">
                Formato por línea: <code className="text-primary">PID, Llegada, Ráfaga, Prioridad</code>
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-sm">Procesos ({procesos.length})</CardTitle>
            </CardHeader>
            <CardContent>
              <ProcesosTable procesos={procesos} onChange={setProcesos} />
            </CardContent>
          </Card>

        </aside>

        {/* Panel Derecho */}
        <section>
          {!resultadoNormal && !resultadoComparar && !loading && (
            <Card className="min-h-[500px] flex items-center justify-center border-dashed">
              <CardContent className="text-center py-16">
                <div className="inline-flex p-5 rounded-2xl bg-muted mb-5">
                  <BarChart3 className="h-12 w-12 text-primary" />
                </div>
                <h2 className="text-lg font-semibold mb-2">Sin resultados aún</h2>
                <p className="text-sm text-muted-foreground max-w-sm mx-auto">
                  Configura y ejecuta una simulación para ver los resultados aquí.
                </p>
              </CardContent>
            </Card>
          )}

          {loading && (
            <Card className="min-h-[500px] flex items-center justify-center">
              <CardContent className="text-center py-16">
                <Loader2 className="h-10 w-10 animate-spin text-primary mx-auto mb-4" />
                <p className="text-sm text-muted-foreground">Ejecutando simulación…</p>
              </CardContent>
            </Card>
          )}

          {resultadoNormal && <ResultadosNormal data={resultadoNormal} />}
          {resultadoComparar && (
            <ResultadosComparar
              data={resultadoComparar}
              criterio1={criterio1}
              criterio2={criterio2}
            />
          )}
        </section>
      </main>
    </div>
  );
}
