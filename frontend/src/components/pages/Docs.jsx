export default function Docs() {
  return (
    <div className="bg-nura-black text-white font-sans antialiased min-h-screen relative overflow-hidden">
      <div className="fixed inset-0 overflow-hidden pointer-events-none z-0 tech-grid-public">
        <div className="absolute top-[-10%] left-[25%] w-[70vw] h-[40vw] rounded-full bg-nura-electric ambient-glow animate-pulse-slow" />
      </div>

      <div className="relative z-10 max-w-4xl mx-auto px-6 py-24">
        <div className="space-y-12">
          <div>
            <h1 className="text-4xl font-normal text-white tracking-tight mb-4">Documentación</h1>
            <p className="text-white/40 text-base font-normal">
              Guía básica para empezar a usar la plataforma
            </p>
          </div>

          <div className="space-y-8">
            <section className="pure-glass-public rounded-xl p-8">
              <h2 className="text-xl font-normal mb-4 text-white">1. Empezando</h2>
              <div className="space-y-3 text-white/70 text-sm leading-relaxed font-mono">
                <p>• Crea una cuenta y accede al panel de control</p>
                <p>• Sube tu primer dataset en formato CSV o Excel</p>
                <p>• Espera a que el análisis termine</p>
              </div>
            </section>

            <section className="pure-glass-public rounded-xl p-8">
              <h2 className="text-xl font-normal mb-4 text-white">2. Analizando datos</h2>
              <div className="space-y-3 text-white/70 text-sm leading-relaxed font-mono">
                <p>• Revisa las métricas clave en el dashboard</p>
                <p>• Usa el chat para preguntas en lenguaje natural</p>
                <p>• Exporta tus reportes cuando lo necesites</p>
              </div>
            </section>

            <section className="pure-glass-public rounded-xl p-8">
              <h2 className="text-xl font-normal mb-4 text-white">3. Preguntas frecuentes</h2>
              <div className="space-y-3 text-white/70 text-sm leading-relaxed font-mono">
                <p><span className="text-nura-electric">Q:</span> ¿Qué formatos de archivo puedo subir?</p>
                <p className="pl-4"><span className="text-white/40">A:</span> CSV, Excel (.xlsx, .xls), y archivos de texto</p>
                <p><span className="text-nura-electric">Q:</span> ¿Es seguro mis datos?</p>
                <p className="pl-4"><span className="text-white/40">A:</span> Sí, todos los datos están encriptados y solo tú tienes acceso</p>
              </div>
            </section>
          </div>
        </div>
      </div>
    </div>
  );
}