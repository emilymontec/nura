import { Link } from "react-router-dom";

export default function PublicHero() {
  return (
    <section className="relative pt-40 pb-20 max-w-7xl mx-auto px-6 z-10 grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
      <div className="lg:col-span-6 space-y-8 text-left">
        <div className="inline-flex items-center gap-2 px-2.5 py-1 rounded bg-white/[0.02] border border-white/[0.05] font-mono text-[10px] text-nura-electric tracking-wider uppercase">
          <span className="w-1 h-1 rounded-full bg-nura-electric animate-ping" />
          NURA v1.2 // Active
        </div>
        <h1 className="text-4xl md:text-6xl font-light tracking-tight text-stark-public leading-[1.1]">
          Analítica de datos <br />{" "}
          <span className="font-normal font-mono text-xl md:text-2xl text-white/60 block mt-2 tracking-normal">
            // asistida por IA.
          </span>
        </h1>
        <p className="text-white/40 text-sm md:text-base font-light max-w-xl leading-relaxed">
          Plataforma de analítica procesa y analiza tus datasets empresariales con inteligencia artificial.
          Estadísticas descriptivas, detección de anomalías y chat conversacional en lenguaje natural.
        </p>
        <div className="flex items-center gap-4 pt-4 font-mono text-[11px]">
          <Link
            to="/console"
            className="px-5 h-10 rounded bg-white/5 border border-white/10 flex items-center justify-center hover:bg-white/10 hover:border-nura-electric/40 transition-all duration-300 group"
          >
            iniciar_analisis{" "}
            <span className="ml-2 text-white/30 group-hover:text-nura-electric transition-colors">
              -&gt;
            </span>
          </Link>
          <a
            href="#features"
            className="text-white/40 hover:text-white transition-colors py-2 px-4"
          >
            ver_funciones()
          </a>
        </div>
      </div>

      <div className="lg:col-span-6 animate-subtle-float">
        <div className="pure-glass-public rounded-xl p-px relative overflow-hidden shadow-2xl">
          <div className="absolute inset-0 bg-gradient-to-b from-white/[0.04] to-transparent pointer-events-none" />
          <div className="rounded-[11px] bg-nura-gray/95 p-5 border border-white/[0.01] font-mono text-xs text-white/50 relative overflow-hidden">
            <div className="absolute inset-x-0 h-12 bg-gradient-to-b from-transparent via-nura-electric/[0.02] to-transparent animate-scanline pointer-events-none" />

            <div className="flex items-center justify-between pb-3 border-b border-white/[0.05]">
              <div className="flex items-center gap-2">
                <div className="flex gap-1">
                  <span className="w-1.5 h-1.5 rounded-full bg-white/10" />
                  <span className="w-1.5 h-1.5 rounded-full bg-white/10" />
                </div>
                <span className="text-[10px] text-white/30 tracking-widest">
                    ANALYTICS_ENGINE
                </span>
              </div>
              <span className="text-[10px] text-nura-electric bg-nura-electric/10 px-1.5 py-0.5 rounded">
                ANALIZANDO
              </span>
            </div>

            <div className="py-6 space-y-3">
              <div className="flex items-center justify-between text-[11px]">
                <span className="text-white/20">DATASET_ACTIVO:</span>
                <span className="text-white/80 font-light">
                  ventas_2026.csv
                </span>
              </div>
              <div className="h-[1px] bg-gradient-to-r from-nura-electric/30 via-nura-purple/20 to-transparent" />
              <div className="space-y-1.5">
                <span className="text-[10px] text-white/20 block">
                  ANOMALY_SCORE:
                </span>
                <div className="flex gap-1 h-3 items-end">
                  <div className="w-full bg-white/5 h-2 rounded-sm relative overflow-hidden">
                    <div className="absolute inset-y-0 left-0 bg-white/40 w-[85%]" />
                  </div>
                  <div className="w-full bg-white/5 h-1 rounded-sm relative overflow-hidden">
                    <div className="absolute inset-y-0 left-0 bg-nura-electric/50 w-[40%]" />
                  </div>
                  <div className="w-full bg-white/5 h-3 rounded-sm relative overflow-hidden">
                    <div className="absolute inset-y-0 left-0 bg-white/30 w-[65%]" />
                  </div>
                  <div className="w-full bg-white/5 h-1.5 rounded-sm relative overflow-hidden">
                    <div className="absolute inset-y-0 left-0 bg-nura-purple/60 w-[90%]" />
                  </div>
                </div>
              </div>
            </div>

            <div className="pt-3 border-t border-white/[0.05] flex justify-between items-center text-[10px] text-white/30">
              <span>
                REGISTROS:{" "}
                <span className="text-white/60 font-sans">142,500</span>
              </span>
              <span>
                HEALTH:{" "}
                <span className="text-nura-electric font-sans">85%</span>
              </span>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
