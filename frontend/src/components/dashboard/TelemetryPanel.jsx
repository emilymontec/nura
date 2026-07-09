export default function TelemetryPanel() {
  const conversations = [
    { title: "Análisis de Ventas Q2", time: "Hace 15 min", active: true },
    { title: "Auditoría de Inventarios", time: "Hace 2 h", active: false },
    { title: "Métricas de Retención", time: "Hace 5 h", active: false },
    { title: "Proyección Q3 2026", time: "Ayer", active: false },
    { title: "Segmentación de Clientes", time: "Ayer", active: false },
    { title: "Análisis de Abandono", time: "Hace 3 días", active: false },
  ];

  return (
    <aside className="w-64 border-l border-nura-border bg-nura-gray/30 backdrop-blur-md hidden lg:flex flex-col p-4 space-y-4 font-mono text-xs z-10 flex-none">
      <span className="text-[9px] text-white/20 uppercase tracking-widest block">
        // CONVERSACIONES_RECIENTES
      </span>

      <div className="space-y-2 flex-1 overflow-y-auto">
        {conversations.map((conv, i) => (
          <div
            key={i}
            className={`p-3 rounded cursor-pointer transition-all group ${
              conv.active
                ? "bg-nura-purple/10 border border-nura-purple/20"
                : "bg-white/[0.01] border border-transparent hover:bg-white/[0.03] hover:border-nura-border"
            }`}
          >
            <div className="flex items-start gap-2">
              <span
                className={`w-1.5 h-1.5 rounded-full mt-1 flex-none ${
                  conv.active ? "bg-nura-purple animate-pulse" : "bg-white/20"
                }`}
              />
              <div className="min-w-0">
                <p className={`text-[11px] truncate ${conv.active ? "text-white/80" : "text-white/50 group-hover:text-white/70"}`}>
                  {conv.title}
                </p>
                <p className="text-[9px] text-white/20 mt-0.5">{conv.time}</p>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="p-3 rounded bg-white/[0.01] border border-nura-border space-y-2">
        <span className="text-[9px] text-white/30 uppercase block">
          Resumen Rápido
        </span>
        <p className="text-white/40 text-[10px] leading-relaxed">
          Último análisis: Ventas Q2 2026 completado con 142,500 registros procesados vía Groq.
        </p>
      </div>
    </aside>
  );
}
