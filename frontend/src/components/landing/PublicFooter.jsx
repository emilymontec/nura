export default function PublicFooter() {
  return (
    <footer className="border-t border-white/[0.03] bg-nura-black relative z-10 text-white/30 font-mono text-[10px]">
      <div className="max-w-7xl mx-auto px-6 py-10 flex flex-col sm:flex-row justify-between items-center gap-4">
        <div className="flex items-center gap-2">
          <span className="w-1.5 h-1.5 rounded-full bg-white/20" />
          <span>© 2026 NURA INTELLIGENCE. All rights reserved.</span>
        </div>
        <div className="flex gap-6 text-white/40">
          <a href="#" className="hover:text-nura-electric transition-colors">
            /[security]
          </a>
          <a href="#" className="hover:text-nura-electric transition-colors">
            /[status]
          </a>
          <a href="#" className="hover:text-nura-electric transition-colors">
            /[changelog]
          </a>
        </div>
      </div>
    </footer>
  );
}
