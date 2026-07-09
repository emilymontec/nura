export default function About() {
  return (
    <div className="bg-nura-black text-white font-sans antialiased min-h-screen relative overflow-hidden">
      <div className="fixed inset-0 overflow-hidden pointer-events-none z-0 tech-grid-public">
        <div className="absolute top-[-10%] left-[25%] w-[70vw] h-[40vw] rounded-full bg-nura-electric ambient-glow animate-pulse-slow" />
      </div>

      <div className="relative z-10 max-w-4xl mx-auto px-6 py-24">
        <div className="space-y-12">
          <div>
            <h1 className="text-4xl font-normal text-white tracking-tight mb-4">Acerca de</h1>
            <p className="text-white/40 text-base font-normal">
              Conoce más sobre la plataforma y quiénes somos
            </p>
          </div>

          <div className="pure-glass-public rounded-xl p-8">
            <h2 className="text-xl font-normal mb-4 text-white">Nuestra misión</h2>
            <p className="text-white/70 text-sm leading-relaxed font-mono">
              Hacer que el análisis de datos sea accesible para todos, sin importar su nivel técnico. 
              Creemos que los datos deben ser fáciles de entender y usar para tomar decisiones mejores.
            </p>
          </div>

          <div className="pure-glass-public rounded-xl p-8">
            <h2 className="text-xl font-normal mb-4 text-white">Qué hacemos</h2>
            <p className="text-white/70 text-sm leading-relaxed font-mono">
              Proporcionamos una plataforma de análisis de datos con asistencia de inteligencia artificial 
              para ayudarte a explorar tus datos, encontrar insights y tomar decisiones basadas en información.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}