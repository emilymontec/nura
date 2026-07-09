import { Search } from "lucide-react";

export default function HeaderBar({ currentPath }) {
  return (
    <header className="h-12 border-b border-nura-border flex items-center justify-between px-6 flex-none bg-nura-gray/40 backdrop-blur-md">
      <div className="flex items-center gap-2 text-xs font-mono text-white/40">
        <span className="text-white/20">SYS_PATH:</span>
        <span className="text-nura-electric">{currentPath}</span>
      </div>

      <div className="flex items-center gap-4">
        <div className="hidden sm:flex items-center gap-1.5 bg-white/[0.02] border border-nura-border px-2 py-1 rounded text-[10px] font-mono text-white/40">
          <Search className="w-3 h-3" />
          <span>Buscar análisis...</span>
          <span className="text-white/20 ml-2">⌘K</span>
        </div>
          <button className="text-xs bg-white text-nura-black font-mono px-2.5 py-1 rounded hover:bg-white/90 transition-all font-medium tracking-wide">
            + nuevo_análisis()
          </button>
      </div>
    </header>
  );
}
