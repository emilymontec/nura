import { Link } from 'react-router-dom';
import { Compass, ArrowLeft } from 'lucide-react';
import PublicHeader from '../landing/PublicHeader';

function NotFound() {
  return (
    <div className="bg-nura-black text-white font-sans antialiased selection:bg-nura-electric/20 overflow-x-hidden min-h-screen">
      <div className="fixed inset-0 overflow-hidden pointer-events-none z-0 tech-grid-public">
        <div className="absolute top-[-10%] left-[25%] w-[70vw] h-[40vw] rounded-full bg-nura-electric ambient-glow animate-pulse-slow" />
        <div className="absolute top-[40%] right-[-10%] w-[50vw] h-[50vw] rounded-full bg-nura-purple ambient-glow" />
      </div>

      <PublicHeader />

      <section className="relative pt-48 pb-24 max-w-3xl mx-auto px-6 z-10 text-center space-y-6">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/[0.02] border border-white/[0.05] font-mono text-[10px] text-nura-electric uppercase tracking-wider">
          <Compass className="w-3 h-3" />
          Error 404 // Ruta no encontrada
        </div>
        <h1 className="text-4xl md:text-6xl font-normal tracking-tight text-white leading-[1.1]">
          Esto no existe
        </h1>
        <p className="text-white/50 text-sm md:text-base max-w-lg mx-auto">
          La página que buscas no está aquí. Puede que el enlace esté roto o que la ruta haya cambiado.
        </p>
        <div className="pt-4">
          <Link
            to="/"
            className="inline-flex items-center gap-2 px-6 py-3 rounded bg-white text-nura-black text-sm font-medium hover:bg-white/90 transition-all"
          >
            <ArrowLeft className="w-4 h-4" />
            Volver al inicio
          </Link>
        </div>
      </section>
    </div>
  );
}

export default NotFound;
