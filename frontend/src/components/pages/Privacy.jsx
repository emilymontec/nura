export default function Privacy() {
  return (
    <div className="bg-nura-black text-white font-sans antialiased min-h-screen relative overflow-hidden">
      <div className="fixed inset-0 overflow-hidden pointer-events-none z-0 tech-grid-public">
        <div className="absolute top-[-10%] left-[25%] w-[70vw] h-[40vw] rounded-full bg-nura-electric ambient-glow animate-pulse-slow" />
      </div>

      <div className="relative z-10 max-w-4xl mx-auto px-6 py-24">
        <div className="space-y-8">
          <div>
            <h1 className="text-4xl font-normal text-white tracking-tight mb-4">Política de privacidad</h1>
            <p className="text-white/40 text-base font-normal">
              Última actualización: Julio 2026
            </p>
          </div>

          <div className="space-y-6 text-white/70 text-sm leading-relaxed font-mono">
            <div className="pure-glass-public rounded-xl p-8">
              <h2 className="text-lg font-normal mb-4 text-white">1. Información que recopilamos</h2>
              <p className="mb-3">
                Recopilamos información que tú nos proporcionas directamente, como tu correo electrónico y los datos que subes a la plataforma.
              </p>
              <p>
                También recopilamos información automáticamente, como datos de uso y registros técnicos para mejorar el servicio.
              </p>
            </div>

            <div className="pure-glass-public rounded-xl p-8">
              <h2 className="text-lg font-normal mb-4 text-white">2. Cómo usamos tu información</h2>
              <p className="mb-3">
                Usamos tu información para:
              </p>
              <ul className="list-disc pl-6 space-y-2">
                <li>Proporcionar y mantener el servicio</li>
                <li>Mejorar y personalizar tu experiencia</li>
                <li>Comunicarnos contigo sobre el servicio</li>
                <li>Cumplir con obligaciones legales</li>
              </ul>
            </div>

            <div className="pure-glass-public rounded-xl p-8">
              <h2 className="text-lg font-normal mb-4 text-white">3. Seguridad de los datos</h2>
              <p>
                Implementamos medidas de seguridad para proteger tu información personal y datos. Sin embargo, ningún método de transmisión por Internet es 100% seguro.
              </p>
            </div>

            <div className="pure-glass-public rounded-xl p-8">
              <h2 className="text-lg font-normal mb-4 text-white">4. Compartir información</h2>
              <p>
                No compartimos tu información personal con terceros, excepto cuando es necesario para proporcionar el servicio o requerido por la ley.
              </p>
            </div>

            <div className="pure-glass-public rounded-xl p-8">
              <h2 className="text-lg font-normal mb-4 text-white">5. Tus derechos</h2>
              <p className="mb-3">
                Tienes derecho a:
              </p>
              <ul className="list-disc pl-6 space-y-2">
                <li>Acceder a tu información personal</li>
                <li>Corregir datos incorrectos</li>
                <li>Eliminar tu cuenta y datos</li>
                <li>Restringir u oponerte al procesamiento</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}