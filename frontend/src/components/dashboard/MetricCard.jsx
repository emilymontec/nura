export default function MetricCard({ label, value, unit, barColor = "bg-nura-electric", barWidth, valueColor = "text-white" }) {
  return (
    <div className="pure-glass rounded p-4 font-mono">
      <span className="text-[9px] text-white/30 block tracking-widest">// {label}</span>
      <div className={`text-xl font-light mt-1 ${valueColor}`}>
        {value} <span className="text-xs text-white/30">{unit}</span>
      </div>
      {barWidth && (
        <div className="w-full bg-white/5 h-0.5 mt-3 overflow-hidden">
          <div 
            className={`${barColor} h-full`} 
            style={{ width: typeof barWidth === "string" && barWidth.endsWith("%") ? barWidth : "100%" }} 
          />
        </div>
      )}
    </div>
  );
}
