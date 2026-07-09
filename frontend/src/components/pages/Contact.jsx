import { useState } from 'react';

export default function Contact() {
  const [form, setForm] = useState({ name: '', email: '', message: '' });
  const [success, setSuccess] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    setSuccess(true);
    setForm({ name: '', email: '', message: '' });
    setTimeout(() => setSuccess(false), 3000);
  };

  return (
    <div className="bg-nura-black text-white font-sans antialiased min-h-screen relative overflow-hidden">
      <div className="fixed inset-0 overflow-hidden pointer-events-none z-0 tech-grid-public">
        <div className="absolute top-[-10%] left-[25%] w-[70vw] h-[40vw] rounded-full bg-nura-electric ambient-glow animate-pulse-slow" />
      </div>

      <div className="relative z-10 max-w-2xl mx-auto px-6 py-24">
        <div className="space-y-8">
          <div>
            <h1 className="text-4xl font-normal text-white tracking-tight mb-4">Contacto</h1>
            <p className="text-white/40 text-base font-normal">
              Escríbenos y te responderemos lo antes posible
            </p>
          </div>

          <form onSubmit={handleSubmit} className="pure-glass-public rounded-xl p-8 space-y-6">
            {success && (
              <div className="p-4 bg-emerald-500/10 border-l-2 border-emerald-500 text-emerald-400 text-xs font-mono">
                Mensaje enviado exitosamente!
              </div>
            )}

            <div className="space-y-2">
              <label className="block text-[10px] text-white/40 uppercase tracking-widest font-mono">
                Nombre
              </label>
              <input
                type="text"
                value={form.name}
                onChange={(e) => setForm({ ...form, name: e.target.value })}
                required
                className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-nura-electric/40 text-sm"
              />
            </div>

            <div className="space-y-2">
              <label className="block text-[10px] text-white/40 uppercase tracking-widest font-mono">
                Correo electrónico
              </label>
              <input
                type="email"
                value={form.email}
                onChange={(e) => setForm({ ...form, email: e.target.value })}
                required
                className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-nura-electric/40 text-sm"
              />
            </div>

            <div className="space-y-2">
              <label className="block text-[10px] text-white/40 uppercase tracking-widest font-mono">
                Mensaje
              </label>
              <textarea
                rows={6}
                value={form.message}
                onChange={(e) => setForm({ ...form, message: e.target.value })}
                required
                className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-nura-electric/40 text-sm resize-none"
              />
            </div>

            <button
              type="submit"
              className="w-full py-3 rounded-lg bg-nura-electric/20 border border-nura-electric/30 text-nura-electric hover:bg-nura-electric/30 transition-all text-xs font-mono"
            >
              ENVIAR_MENSAJE()
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}