export default function SidebarButton({ item, isActive, onClick }) {
  const Icon = item.icon;
  const accentBorder = isActive
    ? item.accent === "purple"
      ? "border-nura-purple"
      : "border-nura-electric"
    : "border-transparent";
  const activeStyles = isActive
    ? "bg-white/[0.03] text-white border-l-2"
    : "text-white/40 hover:bg-white/[0.01] hover:text-white/80";

  return (
    <button
      onClick={onClick}
      className={`w-full flex items-center gap-2.5 px-2.5 py-1.5 text-xs rounded font-mono transition-all ${activeStyles} ${accentBorder}`}
    >
      <Icon
        className={`w-3.5 h-3.5 flex-none ${
          isActive
            ? item.accent === "purple"
              ? "text-nura-purple"
              : "text-nura-electric"
            : ""
        }`}
      />
      <span>{item.label}</span>
    </button>
  );
}
