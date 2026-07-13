export default function TelemetryPanel() {
  return (
    <aside className="w-64 border-l border-nura-border bg-nura-gray/30 backdrop-blur-md hidden lg:flex flex-col p-4 space-y-4 font-mono text-xs z-10 flex-none">
      <span className="text-[9px] text-white/20 uppercase tracking-widest block">
        // CONVERSACIONES_RECIENTES
      </span>

      <div className="space-y-2 flex-1 overflow-y-auto">
        <div className="p-3 rounded bg-white/[0.01] border border-transparent text-white/40 text-[10px]">
          No hay conversaciones recientes
        </div>
      </div>

      <div className="p-3 rounded bg-white/[0.01] border border-nura-border space-y-2">
        <span className="text-[9px] text-white/30 uppercase block">
          Resumen Rápido
        </span>
        <p className="text-white/40 text-[10px] leading-relaxed">
          No hay análisis recientes
        </p>
      </div>
    </aside>
  );
}
