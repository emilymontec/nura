import { ArrowUpRight } from "lucide-react";

export default function PublicFeatures() {
  return (
    <section
      id="features"
      className="relative py-20 border-t border-white/[0.03] max-w-7xl mx-auto px-6 z-10"
    >
      <div className="grid grid-cols-1 md:grid-cols-12 gap-px bg-white/[0.06] border border-white/[0.06] rounded-xl overflow-hidden">
        <div className="md:col-span-6 bg-nura-black/80 p-8 space-y-6 flex flex-col justify-between group hover:bg-nura-gray/90 transition-all duration-300">
          <div className="space-y-3">
            <span className="font-mono text-[10px] text-nura-electric tracking-widest block">
              // ENGINE
            </span>
            <h3 className="text-lg font-normal tracking-tight text-white/90">
              Motor de Analítica Predictiva
            </h3>
            <p className="text-white/40 font-light text-xs leading-relaxed max-w-sm">
              Estadísticas descriptivas, detección de tendencias y análisis de correlaciones
              multidimensionales sobre tus datasets empresariales en tiempo real.
            </p>
          </div>
          <div className="pt-6 font-mono text-[11px] text-white/30 group-hover:text-white transition-colors flex items-center gap-2">
            explorar_api() <ArrowUpRight className="w-3 h-3" />
          </div>
        </div>

        <div className="md:col-span-3 bg-nura-black/80 p-8 space-y-6 flex flex-col justify-between hover:bg-nura-gray/90 transition-all duration-300">
          <div className="space-y-3">
            <span className="font-mono text-[10px] text-white/20 tracking-widest block">
              // CHAT
            </span>
            <h3 className="text-base font-normal tracking-tight text-white/90">
              Chat Conversacional con Datos
            </h3>
            <p className="text-white/40 font-light text-xs leading-relaxed">
              Interroga tus datasets en lenguaje natural. La plataforma responde con análisis precisos
              soportado por Groq, Cerebras u OpenRouter según tu preferencia.
            </p>
          </div>
          <div className="w-full bg-white/[0.03] h-1 rounded-full overflow-hidden">
            <div className="bg-nura-electric h-full w-1/3" />
          </div>
        </div>

        <div className="md:col-span-3 bg-nura-black/80 p-8 space-y-6 flex flex-col justify-between hover:bg-nura-gray/90 transition-all duration-300">
          <div className="space-y-3">
            <span className="font-mono text-[10px] text-nura-purple tracking-widest block">
              // REPORTS
            </span>
            <h3 className="text-base font-normal tracking-tight text-white/90">
              Reportes Ejecutivos Automáticos
            </h3>
            <p className="text-white/40 font-light text-xs leading-relaxed">
              Genera informes PDF con resumen ejecutivo, análisis de riesgos, oportunidades de
              mejora y recomendaciones estratégicas basadas en IA.
            </p>
          </div>
          <div className="flex gap-1.5">
            <span className="w-1.5 h-1.5 rounded-full bg-nura-purple animate-pulse" />
            <span className="font-mono text-[9px] text-white/30">                ANALYTICS_READY</span>
          </div>
        </div>
      </div>
    </section>
  );
}
