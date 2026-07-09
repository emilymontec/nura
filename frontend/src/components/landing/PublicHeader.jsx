import { ArrowUpRight } from "lucide-react";
import { Link } from "react-router-dom";

export default function PublicHeader() {
  return (
    <header className="fixed top-0 left-0 w-full z-50 border-b border-white/[0.02] bg-nura-black/40 backdrop-blur-md">
      <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
        <Link to="/" className="flex items-center gap-3 text-xs font-semibold tracking-[0.25em] text-white">
          NURA{" "}
          <span className="text-white/30 font-light tracking-normal text-[10px]">
            INTELLIGENCE
          </span>
        </Link>

        <nav className="hidden md:flex items-center gap-8 text-[11px] font-medium uppercase tracking-wider text-white/40">
          <a href="#" className="hover:text-white transition-colors duration-300">
            Analítica
          </a>
          <a href="#features" className="hover:text-white transition-colors duration-300">
            Funciones
          </a>
          <a href="#dashboard" className="hover:text-white transition-colors duration-300">
            Métricas
          </a>
          <a href="#" className="hover:text-white transition-colors duration-300">
            Docs
          </a>
        </nav>

        <div className="flex items-center gap-5 text-xs">
          <Link
            to="/console"
            className="text-white/40 hover:text-white transition-colors duration-300 font-mono text-[11px]"
          >
            SYS_LOG
          </Link>
          <Link
            to="/console"
            className="px-3.5 py-1.5 rounded bg-white text-nura-black hover:bg-white/80 transition-all font-medium text-[11px] tracking-wide"
          >
            INICIAR
          </Link>
        </div>
      </div>
    </header>
  );
}
