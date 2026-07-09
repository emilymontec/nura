export default function DashboardFooter() {
  return (
    <footer className="h-8 border-t border-nura-border bg-nura-gray/40 px-6 flex items-center justify-between text-[9px] font-mono text-white/20 flex-none z-10">
      <span>© 2026 SITE ANALYTICS Inc.</span>
      <div className="flex gap-4">
        <a href="#" className="hover:text-white transition-colors">
          /[security]
        </a>
        <a href="#" className="hover:text-white transition-colors">
          /[changelog]
        </a>
      </div>
    </footer>
  );
}
