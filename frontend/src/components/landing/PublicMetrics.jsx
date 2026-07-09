export default function PublicMetrics() {
  return (
    <section
      id="dashboard"
      className="relative py-12 max-w-7xl mx-auto px-6 z-10"
    >
      <div className="border border-white/[0.04] bg-nura-gray/60 rounded-xl p-6 grid grid-cols-2 md:grid-cols-4 gap-6 font-mono">
        <div className="space-y-1 p-2 border-l border-white/[0.05]">
          <span className="text-[10px] uppercase text-white/30 tracking-wider block">
            Registros Analizados
          </span>
          <div className="text-2xl font-light text-white tracking-tight flex items-baseline gap-1">
            142,500 <span className="text-xs text-nura-electric font-normal">+12.4%</span>
          </div>
        </div>
        <div className="space-y-1 p-2 border-l border-white/[0.05]">
          <span className="text-[10px] uppercase text-white/30 tracking-wider block">
            Health Score
          </span>
          <div className="text-2xl font-light text-white tracking-tight">
            85{" "}
            <span className="text-xs text-nura-electric font-normal">/100</span>
          </div>
        </div>
        <div className="space-y-1 p-2 border-l border-white/[0.05]">
          <span className="text-[10px] uppercase text-white/30 tracking-wider block">
            Proveedores IA
          </span>
          <div className="text-2xl font-light text-white tracking-tight">
            3{" "}
            <span className="text-xs text-white/30 font-normal">modelos activos</span>
          </div>
        </div>
        <div className="space-y-1 p-2 border-l border-white/[0.05]">
          <span className="text-[10px] uppercase text-nura-purple tracking-wider block">
            Anomalías Detectadas
          </span>
          <div className="text-2xl font-light text-amber-400 tracking-tight">
            12
          </div>
        </div>
      </div>
    </section>
  );
}
