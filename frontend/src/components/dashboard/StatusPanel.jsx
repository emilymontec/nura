export default function StatusPanel() {
  return (
    <div className="pure-glass rounded-xl p-5 relative overflow-hidden">
      <div className="absolute inset-x-0 h-12 bg-gradient-to-b from-transparent via-nura-purple/[0.01] to-transparent animate-scanline pointer-events-none" />
      <div className="flex items-center justify-between border-b border-nura-border pb-3 mb-4 font-mono text-xs">
        <span className="text-white/80">
          Instancia_Activa_NURA_01 // Nodos de Inferencia perimetral
        </span>
        <span className="text-[10px] text-nura-electric bg-nura-electric/10 px-1.5 rounded">
          CONECTADO
        </span>
      </div>
      <div className="space-y-4 font-mono text-xs text-white/60">
        <div className="flex flex-col sm:flex-row justify-between gap-2 border-b border-white/[0.02] pb-3">
          <span className="text-white/40">VECTOR_INPUT_BUFFER:</span>
          <span className="text-white/80 font-light text-[11px]">
            [0.9822, -0.1129, 0.4410, 0.8812, -0.0094, 0.7112]
          </span>
        </div>
        <div className="space-y-2">
          <span className="text-[10px] text-white/30 block">
            REDUCCIÓN_COGNITIVA_MÁQUINA (TELEMETRÍA EN CALIENTE)
          </span>
          <div className="flex gap-1.5 h-2 items-end">
            <div className="w-full bg-white/5 h-1 rounded-sm relative overflow-hidden">
              <div className="absolute inset-y-0 left-0 bg-white/40 w-[85%]" />
            </div>
            <div className="w-full bg-white/5 h-2 rounded-sm relative overflow-hidden">
              <div className="absolute inset-y-0 left-0 bg-nura-electric/50 w-[40%]" />
            </div>
            <div className="w-full bg-white/5 h-1.5 rounded-sm relative overflow-hidden">
              <div className="absolute inset-y-0 left-0 bg-white/30 w-[65%]" />
            </div>
            <div className="w-full bg-white/5 h-2 rounded-sm relative overflow-hidden">
              <div className="absolute inset-y-0 left-0 bg-nura-purple/60 w-[90%]" />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
