export default function Terms() {
  return (
    <div className="bg-nura-black text-white font-sans antialiased min-h-screen relative overflow-hidden">
      <div className="fixed inset-0 overflow-hidden pointer-events-none z-0 tech-grid-public">
        <div className="absolute top-[-10%] left-[25%] w-[70vw] h-[40vw] rounded-full bg-nura-electric ambient-glow animate-pulse-slow" />
      </div>

      <div className="relative z-10 max-w-4xl mx-auto px-6 py-24">
        <div className="space-y-8">
          <div>
            <h1 className="text-4xl font-normal text-white tracking-tight mb-4">Términos y condiciones</h1>
            <p className="text-white/40 text-base font-normal">
              Última actualización: Julio 2026
            </p>
          </div>

          <div className="space-y-6 text-white/70 text-sm leading-relaxed font-mono">
            <div className="pure-glass-public rounded-xl p-8">
              <h2 className="text-lg font-normal mb-4 text-white">1. Aceptación de términos</h2>
              <p>
                Al usar la plataforma, aceptas estos términos y condiciones. Si no estás de acuerdo, por favor no uses el servicio.
              </p>
            </div>

            <div className="pure-glass-public rounded-xl p-8">
              <h2 className="text-lg font-normal mb-4 text-white">2. Uso del servicio</h2>
              <p className="mb-3">
                Te comprometes a usar la plataforma solo para fines legales y de acuerdo a estos términos.
              </p>
              <p>
                No debes intentar acceder a áreas no autorizadas, interferir con el servicio o usarlo de manera que cause daño.
              </p>
            </div>

            <div className="pure-glass-public rounded-xl p-8">
              <h2 className="text-lg font-normal mb-4 text-white">3. Cuentas y seguridad</h2>
              <p>
                Eres responsable de mantener la seguridad de tu cuenta y contraseña. Notifícanos inmediatamente si detectas un uso no autorizado.
              </p>
            </div>

            <div className="pure-glass-public rounded-xl p-8">
              <h2 className="text-lg font-normal mb-4 text-white">4. Propiedad intelectual</h2>
              <p>
                Todo el contenido y software de la plataforma es propiedad exclusiva de sus creadores y está protegido por las leyes de propiedad intelectual.
              </p>
            </div>

            <div className="pure-glass-public rounded-xl p-8">
              <h2 className="text-lg font-normal mb-4 text-white">5. Limitación de responsabilidad</h2>
              <p>
                El servicio se proporciona "tal cual". No somos responsables de daños indirectos, incidentales o consecuentes que surjan del uso de la plataforma.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}