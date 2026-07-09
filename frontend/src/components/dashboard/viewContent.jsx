import { useState, useEffect } from "react";
import { useAuth } from "../../contexts/AuthContext";
import {
  LayoutDashboard,
  Database,
  Brain,
  MessageSquareText,
  FileText,
  User,
  SlidersHorizontal,
  Package,
  Plug,
  ShieldAlert,
  Network,
  KeyRound,
  ActivitySquare,
  ChevronsUpDown,
  LogOut,
  Search,
  Upload,
  Send,
  Download,
  AlertTriangle,
  TrendingUp,
  FileSpreadsheet,
  Lightbulb,
} from "lucide-react";

async function getAuthHeaders(refreshAccessToken) {
  let accessToken = localStorage.getItem('accessToken');
  if (!accessToken) return {};
  
  try {
    const payload = JSON.parse(atob(accessToken.split('.')[1]));
    if (Date.now() >= payload.exp * 1000) {
      accessToken = await refreshAccessToken();
    }
  } catch (e) {
    accessToken = await refreshAccessToken();
  }
  
  return accessToken ? { 'Authorization': `Bearer ${accessToken}` } : {};
}

export const NAV_SECTIONS = [
  {
    label: "01 // CORE_WORKSPACE",
    items: [
      { id: "dashboard", icon: LayoutDashboard, label: "panel_principal", accent: "electric" },
      { id: "datasets", icon: Database, label: "gestion_datos", accent: "electric" },
    ],
  },
  {
    label: "02 // AI_ANALYTICS",
    items: [
      { id: "motor-analitico", icon: Brain, label: "motor_analitico", accent: "purple" },
      { id: "chat-inteligente", icon: MessageSquareText, label: "chat_inteligente", accent: "purple" },
      { id: "reportes-ia", icon: FileText, label: "reportes_ia", accent: "purple" },
    ],
  },
  {
    label: "03 // MANAGEMENT",
    items: [
      { id: "mg-perfil", icon: User, label: "usuario_perfil", accent: "electric" },
      { id: "mg-configuracion", icon: SlidersHorizontal, label: "conf_sistema", accent: "electric" },
      { id: "mg-suscripcion", icon: Package, label: "asignacion_cuotas", accent: "electric" },
      { id: "mg-integraciones", icon: Plug, label: "integraciones_api", accent: "electric" },
    ],
  },
  {
    label: "04 // ADMIN_STAGE",
    reserved: true,
    items: [
      { id: "ad-usuarios", icon: ShieldAlert, label: "adm_usuarios", accent: "purple" },
      { id: "ad-empresas", icon: Network, label: "adm_organizaciones", accent: "purple" },
      { id: "ad-licencias", icon: KeyRound, label: "adm_licencias", accent: "purple" },
      { id: "ad-monitoreo", icon: ActivitySquare, label: "global_telemetria", accent: "purple" },
    ],
  },
];

function MetricCard({ label, value, unit, accent = "electric", barWidth }) {
  const color = accent === "purple" ? "bg-nura-purple" : "bg-nura-electric";
  return (
    <div className="pure-glass rounded p-4 font-mono">
      <span className="text-[9px] text-white/30 block tracking-widest">{label}</span>
      <div className="text-xl font-light text-white mt-1 flex items-baseline gap-1 flex-wrap">
        {value}
        {unit && <span className="text-xs text-white/30 font-normal">{unit}</span>}
      </div>
      {barWidth && (
        <div className="w-full bg-white/5 h-0.5 mt-3 overflow-hidden">
          <div className={`${color} h-full`} style={{ width: barWidth }} />
        </div>
      )}
    </div>
  );
}

function UploadCSV({ onUpload }) {
  return (
    <div
      className="flex-1 border-2 border-dashed border-nura-border rounded-xl bg-nura-gray/30 flex flex-col items-center justify-center gap-4 p-12 group hover:border-nura-electric/40 transition-colors cursor-pointer"
      onClick={() => document.getElementById("csv-input").click()}
    >
      <div className="w-16 h-16 rounded-full bg-white/[0.02] border border-white/[0.06] flex items-center justify-center">
        <Upload className="w-6 h-6 text-white/20 group-hover:text-nura-electric transition-colors" />
      </div>
      <p className="text-white/40 text-center max-w-xs text-xs">
        Arrastra tu archivo CSV aquí o haz clic para examinar
      </p>
      <p className="text-white/20 text-[10px]">Formatos: .csv hasta 50MB</p>
      <input id="csv-input" type="file" accept=".csv" className="hidden" onChange={onUpload} />
      <button className="mt-2 px-4 py-2 rounded bg-white/5 border border-white/10 text-white/60 hover:bg-white/10 hover:text-white transition-all text-[11px]">
        examinar_archivos()
      </button>
    </div>
  );
}

function DataPreview({ filename, context }) {
  if (!context) return null;
  const cols = Object.keys(context.columns || {});
  const rows = context.preview || [];
  
  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <span className="text-white/60 font-mono text-xs">
          {filename} &middot; {context.summary?.rows || 0} filas &middot; {context.summary?.columns || 0} columnas
        </span>
        <span className="text-[10px] text-emerald-500 bg-emerald-500/10 px-2 py-0.5 rounded font-mono">
          VALIDADO
        </span>
      </div>
      <div className="overflow-x-auto rounded-lg border border-nura-border">
        <table className="w-full text-[11px] font-mono">
          <thead>
            <tr className="bg-nura-gray/80 border-b border-nura-border">
              {cols.map((c) => (
                <th key={c} className="text-left text-white/50 py-2 px-3 font-medium">{c}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.map((row, i) => (
              <tr key={i} className="border-b border-nura-border/50 hover:bg-white/[0.01]">
                {cols.map((c, j) => (
                  <td key={j} className="text-white/70 py-2 px-3">{row[c]}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function ChatMessage({ role, text }) {
  const isUser = role === "user";
  return (
    <div className={`flex gap-3 ${isUser ? "justify-end" : "justify-start"}`}>
      {!isUser && (
        <div className="w-7 h-7 rounded-full bg-nura-purple/20 border border-nura-purple/30 flex items-center justify-center font-mono text-[10px] text-nura-purple flex-none">
          AI
        </div>
      )}
      <div
        className={`max-w-[75%] rounded-xl px-4 py-2.5 text-xs leading-relaxed ${
          isUser
            ? "bg-nura-electric/10 border border-nura-electric/20 text-white/80"
            : "bg-white/[0.03] border border-white/[0.06] text-white/70"
        }`}
      >
        {text}
      </div>
      {isUser && (
        <div className="w-7 h-7 rounded-full bg-white/5 border border-white/10 flex items-center justify-center font-mono text-[10px] text-white/60 flex-none">
          U
        </div>
      )}
    </div>
  );
}

export const VIEW_CONTENT = {
  dashboard: () => {
    const { refreshAccessToken } = useAuth();
    const [context, setContext] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
      const fetchContext = async () => {
        const API_BASE = import.meta.env.VITE_API_URL || '';
        try {
          const headers = await getAuthHeaders(refreshAccessToken);
          const res = await fetch(`${API_BASE}/api/sessions/default/`, { headers });
          if (res.ok) {
            const data = await res.json();
            setContext(data.dataset_context);
          }
        } catch (e) {
          console.error(e);
        } finally {
          setLoading(false);
        }
      };
      fetchContext();
    }, [refreshAccessToken]);

    const healthScore = context?.health?.health_score || 0;
    const rows = context?.summary?.rows || 0;
    const missing = context?.summary?.total_missing || 0;
    const duplicates = context?.summary?.duplicate_rows || 0;
    const cols = context?.summary?.columns || 0;
    const fileName = context?.file_name || "Ninguno";

    return (
      <div className="space-y-6">
        <div className="space-y-1">
          <h1 className="text-2xl font-light text-stark tracking-tight">Panel Principal</h1>
          <p className="text-xs text-white/40 font-mono">Resumen general del espacio de trabajo de analítica.</p>
        </div>
        {loading ? (
          <div className="text-white/60 font-mono text-xs">Cargando panel...</div>
        ) : (
          <>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              <MetricCard label="// BUSINESS_HEALTH_SCORE" value={healthScore.toFixed(0)} unit="%" barWidth={`${healthScore}%`} />
              <MetricCard label="// REGISTROS_PROCESADOS" value={rows} unit="filas" barWidth="60%" />
              <MetricCard
                label="// PROVEEDOR_IA_ACTIVO"
                value={
                  <select className="bg-transparent text-nura-electric text-xs border border-nura-electric/30 rounded px-1 py-0.5 outline-none cursor-pointer">
                    <option className="bg-nura-black">Groq</option>
                    <option className="bg-nura-black">Cerebras</option>
                    <option className="bg-nura-black">OpenRouter</option>
                  </select>
                }
              />
              <MetricCard
                label="// ANOMALÍAS_DETECTADAS"
                value={
                  <span className="text-amber-400">{missing} nulos <span className="text-white/30 text-xs">/ {duplicates} duplicados</span></span>
                }
                accent="purple"
                barWidth="100%"
              />
            </div>
            <div className="pure-glass rounded-xl p-5">
              <div className="flex items-center justify-between border-b border-nura-border pb-3 mb-4 font-mono text-xs">
                <span className="text-white/80">Dataset_Activo // {fileName}</span>
                <span className={`text-[10px] px-1.5 rounded ${context ? 'text-nura-electric bg-nura-electric/10' : 'text-white/40 bg-white/10'}`}>
                  {context ? 'CONECTADO' : 'SIN CONEXIÓN'}
                </span>
              </div>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 font-mono text-xs">
                <div><span className="text-white/30">Filas totales:</span><span className="text-white/70 ml-2">{rows}</span></div>
                <div><span className="text-white/30">Columnas:</span><span className="text-white/70 ml-2">{cols}</span></div>
                <div><span className="text-white/30">Valores nulos:</span><span className="text-amber-400 ml-2">{missing}</span></div>
                <div><span className="text-white/30">Duplicados:</span><span className="text-emerald-400 ml-2">{duplicates}</span></div>
              </div>
            </div>
          </>
        )}
      </div>
    );
  },

  datasets: () => {
    const { refreshAccessToken } = useAuth();
    const [uploaded, setUploaded] = useState(null);
    const [context, setContext] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleUpload = async (e) => {
      const file = e.target.files?.[0];
      if (!file) return;
      setUploaded(file.name);
      setLoading(true);
      
      const API_BASE = import.meta.env.VITE_API_URL || '';
      const formData = new FormData();
      formData.append('file', file);
      formData.append('session_id', 'default');
      
      try {
        const headers = await getAuthHeaders(refreshAccessToken);
        const response = await fetch(`${API_BASE}/api/analyze`, {
          method: 'POST',
          headers,
          body: formData
        });
        const data = await response.json();
        setContext(data);
      } catch (error) {
        console.error('Error uploading:', error);
      } finally {
        setLoading(false);
      }
    };
    
    return (
      <div className="space-y-4 font-mono text-xs h-full flex flex-col">
        <h2 className="text-lg text-white font-light">// gestion_datos</h2>
        {!uploaded ? (
          <UploadCSV onUpload={handleUpload} />
        ) : (
          <div className="flex-1 space-y-4">
            <div className="flex items-center gap-3">
              <button
                onClick={() => { setUploaded(null); setContext(null); }}
                className="text-[10px] text-white/40 hover:text-white transition-colors"
              >
                &larr; cargar otro archivo
              </button>
              <span className="text-[10px] text-white/20">/</span>
              <span className="text-nura-electric text-[11px]">{uploaded}</span>
            </div>
            {loading ? (
              <div className="text-white/60">Procesando {uploaded}...</div>
            ) : (
              <DataPreview filename={uploaded} context={context} />
            )}
            <div className="flex gap-3">
              <button className="px-4 py-2 rounded bg-nura-electric/20 border border-nura-electric/30 text-nura-electric hover:bg-nura-electric/30 transition-all text-[11px]" disabled={loading}>
                validar_dataset()
              </button>
              <button className="px-4 py-2 rounded bg-white/5 border border-white/10 text-white/60 hover:bg-white/10 transition-all text-[11px]" disabled={loading}>
                limpiar_datos()
              </button>
            </div>
          </div>
        )}
      </div>
    );
  },

  "motor-analitico": () => {
    const { refreshAccessToken } = useAuth();
    const [context, setContext] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
      const fetchContext = async () => {
        const API_BASE = import.meta.env.VITE_API_URL || '';
        try {
          const headers = await getAuthHeaders(refreshAccessToken);
          const res = await fetch(`${API_BASE}/api/sessions/default/`, { headers });
          if (res.ok) {
            const data = await res.json();
            setContext(data.dataset_context);
          }
        } catch (e) {
          console.error(e);
        } finally {
          setLoading(false);
        }
      };
      fetchContext();
    }, [refreshAccessToken]);

    if (loading) return <div className="text-white/60 font-mono text-xs p-4">Cargando motor analítico...</div>;
    if (!context || !context.summary) return <div className="text-white/60 font-mono text-xs p-4">No hay datos analizados. Sube un dataset primero.</div>;

    const summary = context.summary || {};
    const anomalies = context.anomalies || [];
    const trends = context.trends || [];
    const health = context.health || {};

    return (
      <div className="space-y-4 font-mono text-xs">
        <h2 className="text-lg text-white font-light">// motor_analitico</h2>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          <div className="pure-glass rounded-xl p-4 space-y-3">
            <span className="text-[9px] text-white/30 uppercase tracking-widest block">Estadísticas Descriptivas</span>
            <div className="space-y-2">
              {[
                { label: "Filas totales", value: summary.rows || 0 },
                { label: "Columnas", value: summary.columns || 0 },
                { label: "Datos faltantes", value: summary.total_missing || 0 },
                { label: "Filas duplicadas", value: summary.duplicate_rows || 0 },
              ].map((s, i) => (
                <div key={i} className="flex justify-between py-1.5 border-b border-white/[0.03]">
                  <span className="text-white/40">{s.label}</span>
                  <span className="text-white/80">{s.value}</span>
                </div>
              ))}
            </div>
          </div>
          <div className="pure-glass rounded-xl p-4 space-y-3">
            <span className="text-[9px] text-white/30 uppercase tracking-widest block">Detección de Anomalías</span>
            {summary.total_missing > 0 ? (
              <div className="flex items-center gap-3 p-3 rounded bg-amber-500/5 border border-amber-500/20">
                <AlertTriangle className="w-4 h-4 text-amber-400 flex-none" />
                <div>
                  <p className="text-amber-400 text-[11px] font-medium">{summary.total_missing} valores nulos detectados</p>
                </div>
              </div>
            ) : (
              <div className="flex items-center gap-3 p-3 rounded bg-emerald-500/5 border border-emerald-500/20">
                <TrendingUp className="w-4 h-4 text-emerald-400 flex-none" />
                <div>
                  <p className="text-emerald-400 text-[11px] font-medium">Dataset completo</p>
                  <p className="text-white/40 text-[10px] mt-0.5">No hay valores nulos</p>
                </div>
              </div>
            )}
            {summary.duplicate_rows === 0 ? (
              <div className="flex items-center gap-3 p-3 rounded bg-emerald-500/5 border border-emerald-500/20">
                <TrendingUp className="w-4 h-4 text-emerald-400 flex-none" />
                <div>
                  <p className="text-emerald-400 text-[11px] font-medium">0 registros duplicados</p>
                  <p className="text-white/40 text-[10px] mt-0.5">Dataset limpio sin redundancias</p>
                </div>
              </div>
            ) : (
              <div className="flex items-center gap-3 p-3 rounded bg-amber-500/5 border border-amber-500/20">
                <AlertTriangle className="w-4 h-4 text-amber-400 flex-none" />
                <div>
                  <p className="text-amber-400 text-[11px] font-medium">{summary.duplicate_rows} registros duplicados</p>
                </div>
              </div>
            )}
          </div>
        </div>
        <div className="pure-glass rounded-xl p-4 space-y-3">
          <span className="text-[9px] text-white/30 uppercase tracking-widest block">Tendencias Identificadas</span>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
            {trends.slice(0, 3).map((t, i) => (
              <div key={i} className="p-3 rounded bg-white/[0.02] border border-white/[0.04]">
                <span className="text-white/30 text-[10px]">{t.column}</span>
                <p className="text-white/80 text-xs mt-1">{t.trend_direction}</p>
                <span className="text-emerald-400 text-[10px]">Volatilidad: {t.volatility}</span>
              </div>
            ))}
            {(!trends || trends.length === 0) && (
              <div className="p-3 rounded bg-white/[0.02] border border-white/[0.04] col-span-3 text-white/40 text-xs">
                No se identificaron tendencias numéricas claras en los datos proporcionados.
              </div>
            )}
          </div>
        </div>
      </div>
    );
  },

  "chat-inteligente": () => {
    const { refreshAccessToken } = useAuth();
    const [messages, setMessages] = useState([
      { role: "assistant", text: "¡Hola! Soy el asistente de analítica. Puedo responder preguntas sobre tu dataset en lenguaje natural. ¿Qué deseas consultar?" },
    ]);
    const [input, setInput] = useState("");
    const [loading, setLoading] = useState(false);
    const [provider, setProvider] = useState("groq");

    const handleSend = async () => {
      if (!input.trim() || loading) return;
      const text = input;
      setMessages((prev) => [...prev, { role: "user", text }]);
      setInput("");
      setLoading(true);

      const API_BASE = import.meta.env.VITE_API_URL || '';
      try {
        const headers = await getAuthHeaders(refreshAccessToken);
        const response = await fetch(`${API_BASE}/api/chat`, {
          method: 'POST',
          headers: { 
            'Content-Type': 'application/json',
            ...headers
          },
          body: JSON.stringify({ message: text, session_id: 'default' })
        });
        const data = await response.json();
        setMessages((prev) => [...prev, { role: "assistant", text: data.response || "Error" }]);
      } catch (error) {
        console.error("Error sending message:", error);
        setMessages((prev) => [...prev, { role: "assistant", text: "Ocurrió un error al procesar tu solicitud." }]);
      } finally {
        setLoading(false);
      }
    };

    return (
      <div className="space-y-4 font-mono text-xs h-full flex flex-col">
        <div className="flex items-center justify-between">
          <h2 className="text-lg text-white font-light">// chat_inteligente</h2>
          <div className="flex items-center gap-2">
            <span className="text-[9px] text-white/30 uppercase">Proveedor IA:</span>
            <select
              value={provider}
              onChange={(e) => setProvider(e.target.value)}
              className="bg-nura-black border border-nura-border rounded px-2 py-1 text-white/80 text-[11px] outline-none cursor-pointer"
            >
              <option value="groq">Groq</option>
              <option value="cerebras">Cerebras</option>
              <option value="openrouter">OpenRouter</option>
            </select>
          </div>
        </div>
        <div className="flex-1 overflow-y-auto space-y-3 pr-2 min-h-0 scrollbar-thin">
          {messages.map((msg, i) => (
            <ChatMessage key={i} role={msg.role} text={msg.text} />
          ))}
          {loading && (
            <div className="text-nura-purple text-[10px] animate-pulse">Escribiendo...</div>
          )}
        </div>
        <div className="flex gap-2 pt-2 border-t border-nura-border">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
            disabled={loading}
            placeholder="Ej: ¿Cuáles fueron los productos más vendidos por categoría?..."
            className="flex-1 bg-white/5 border border-nura-border rounded-lg px-4 py-2.5 text-white focus:outline-none focus:border-nura-electric/40 text-[12px]"
          />
          <button
            onClick={handleSend}
            disabled={loading}
            className="px-4 rounded-lg bg-nura-purple/20 border border-nura-purple/30 text-nura-purple hover:bg-nura-purple/30 transition-all flex items-center gap-2 disabled:opacity-50"
          >
            <Send className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>
    );
  },

  "reportes-ia": () => {
    const { refreshAccessToken } = useAuth();
    const [context, setContext] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
      const fetchContext = async () => {
        const API_BASE = import.meta.env.VITE_API_URL || '';
        try {
          const headers = await getAuthHeaders(refreshAccessToken);
          const res = await fetch(`${API_BASE}/api/sessions/default/`, { headers });
          if (res.ok) {
            const data = await res.json();
            setContext(data.dataset_context);
          }
        } catch (e) {
          console.error(e);
        } finally {
          setLoading(false);
        }
      };
      fetchContext();
    }, [refreshAccessToken]);

    if (loading) return <div className="text-white/60 font-mono text-xs p-4">Cargando reporte IA...</div>;
    if (!context) return <div className="text-white/60 font-mono text-xs p-4">No hay datos para reportar. Sube un dataset primero.</div>;

    const riskLevel = context.health?.risk_level || "Desconocido";
    const healthScore = context.health?.health_score || 0;

    return (
      <div className="space-y-4 font-mono text-xs">
        <h2 className="text-lg text-white font-light">// reportes_ia</h2>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          <div className="pure-glass rounded-xl p-5 space-y-4">
            <div className="flex items-center gap-2 text-nura-electric text-[11px]">
              <FileText className="w-4 h-4" />
              <span>Resumen Ejecutivo</span>
            </div>
            <p className="text-white/60 leading-relaxed text-[11px] max-h-32 overflow-y-auto pr-2 scrollbar-thin">
              {context.response?.split("📝 Resumen Ejecutivo para ti:")[1] || 
              context.response || 
              `El archivo ${context.file_name} ha sido procesado. Contiene ${context.summary?.rows} filas y ${context.summary?.columns} columnas.`}
            </p>
          </div>
          <div className="pure-glass rounded-xl p-5 space-y-4">
            <div className="flex items-center gap-2 text-amber-400 text-[11px]">
              <AlertTriangle className="w-4 h-4" />
              <span>Análisis de Riesgos (Score: {healthScore.toFixed(0)})</span>
            </div>
            <ul className="space-y-2 text-[11px]">
              <li className="flex gap-2 text-white/60">
                <span className="text-amber-400/60">&bull;</span>
                <span>Nivel de riesgo estimado: {riskLevel}</span>
              </li>
              {(context.anomalies?.missing_values || []).slice(0, 2).map((a, i) => (
                <li key={i} className="flex gap-2 text-white/60">
                  <span className="text-amber-400/60">&bull;</span>
                  <span>{a.column} tiene {a.missing} valores nulos.</span>
                </li>
              ))}
              {(!context.anomalies?.missing_values || context.anomalies.missing_values.length === 0) && (
                <li className="flex gap-2 text-emerald-400/80">
                  <span className="text-emerald-400/60">&bull;</span>
                  <span>No hay alertas críticas importantes.</span>
                </li>
              )}
            </ul>
          </div>
          <div className="pure-glass rounded-xl p-5 space-y-4">
            <div className="flex items-center gap-2 text-emerald-400 text-[11px]">
              <Lightbulb className="w-4 h-4" />
              <span>Oportunidades y Variables Clave</span>
            </div>
            <ul className="space-y-2 text-[11px]">
              {(context.critical_variables || []).slice(0, 3).map((v, i) => (
                <li key={i} className="flex gap-2 text-white/60">
                  <span className="text-emerald-400/60">&bull;</span>
                  <span>Variable de alta influencia: {v.column}</span>
                </li>
              ))}
              {(!context.critical_variables || context.critical_variables.length === 0) && (
                <li className="flex gap-2 text-white/60">
                  <span className="text-emerald-400/60">&bull;</span>
                  <span>Requiere más datos correlacionados para identificar oportunidades.</span>
                </li>
              )}
            </ul>
          </div>
          <div className="pure-glass rounded-xl p-5 space-y-4 flex flex-col justify-between">
            <div className="flex items-center gap-2 text-nura-purple text-[11px]">
              <Download className="w-4 h-4" />
              <span>Exportar Reporte</span>
            </div>
            <p className="text-white/40 text-[10px] leading-relaxed">
              Genera un informe PDF completo con resumen ejecutivo, análisis de riesgos,
              oportunidades y recomendaciones basadas en IA.
            </p>
            <button className="w-full py-3 rounded-lg bg-nura-purple/20 border border-nura-purple/30 text-nura-purple hover:bg-nura-purple/30 transition-all text-[11px] flex items-center justify-center gap-2">
              <Download className="w-4 h-4" />
              exportar_reporte_pdf()
            </button>
          </div>
        </div>
      </div>
    );
  },

  "mg-perfil": () => {
    const { user, getProfile, updateProfile } = useAuth();
    const [profile, setProfile] = useState(null);
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);
    const [formData, setFormData] = useState({ user: {} });
    const [message, setMessage] = useState('');

    useEffect(() => {
      const fetchProfile = async () => {
        try {
          const data = await getProfile();
          setProfile(data);
          setFormData({
            ...data,
            user: {
              first_name: data?.user?.first_name || '',
              last_name: data?.user?.last_name || ''
            }
          });
        } catch (e) {
          console.error('Error fetching profile:', e);
        } finally {
          setLoading(false);
        }
      };
      fetchProfile();
    }, [getProfile]);

    const handleSubmit = async (e) => {
      e.preventDefault();
      setSaving(true);
      setMessage('');
      try {
        const updated = await updateProfile(formData);
        setProfile(updated);
        setMessage('Perfil actualizado correctamente');
      } catch (e) {
        setMessage('Error al actualizar el perfil');
      } finally {
        setSaving(false);
      }
    };

    if (loading) {
      return (
        <div className="space-y-4 font-mono text-xs">
          <h2 className="text-lg text-white font-light">// usuario_perfil</h2>
          <div className="p-4 border border-nura-border rounded bg-nura-gray/60 text-white/40">
            Cargando perfil...
          </div>
        </div>
      );
    }

    return (
      <div className="space-y-4 font-mono text-xs">
        <h2 className="text-lg text-white font-light">// usuario_perfil</h2>
        {message && (
          <div className={`p-3 rounded border ${message.includes('correctamente') ? 'border-emerald-500/30 bg-emerald-500/10 text-emerald-400' : 'border-red-500/30 bg-red-500/10 text-red-400'}`}>
            {message}
          </div>
        )}
        <form onSubmit={handleSubmit} className="space-y-4 pure-glass rounded-xl p-5">
          <div className="space-y-1">
            <label className="block text-white/40 text-[10px] uppercase tracking-widest">Email</label>
            <input
              type="email"
              value={user?.email || ''}
              disabled
              className="w-full bg-white/5 border border-nura-border rounded-lg px-4 py-2.5 text-white/70 text-xs outline-none"
            />
          </div>
          <div className="space-y-1">
            <label className="block text-white/40 text-[10px] uppercase tracking-widest">Nombre</label>
            <input
              type="text"
              value={formData.user?.first_name || ''}
              onChange={(e) => setFormData({ ...formData, user: { ...formData.user, first_name: e.target.value } })}
              className="w-full bg-white/5 border border-nura-border rounded-lg px-4 py-2.5 text-white focus:outline-none focus:border-nura-electric/40 text-xs"
            />
          </div>
          <div className="space-y-1">
            <label className="block text-white/40 text-[10px] uppercase tracking-widest">Apellido</label>
            <input
              type="text"
              value={formData.user?.last_name || ''}
              onChange={(e) => setFormData({ ...formData, user: { ...formData.user, last_name: e.target.value } })}
              className="w-full bg-white/5 border border-nura-border rounded-lg px-4 py-2.5 text-white focus:outline-none focus:border-nura-electric/40 text-xs"
            />
          </div>
          <button
            type="submit"
            disabled={saving}
            className="px-4 py-2.5 rounded-lg bg-nura-electric/20 border border-nura-electric/30 text-nura-electric hover:bg-nura-electric/30 transition-all disabled:opacity-50 text-[11px]"
          >
            {saving ? 'Guardando...' : 'guardar_cambios()'}
          </button>
        </form>
      </div>
    );
  },
  "mg-configuracion": () => (
    <div className="space-y-4 font-mono text-xs">
      <h2 className="text-lg text-white font-light">// conf_sistema</h2>
      <div className="p-4 border border-nura-border rounded bg-nura-gray/60 text-white/40">
        Motor analítico: [HABILITADO] &middot; Chat IA: [HABILITADO] &middot; Reportes automáticos: [HABILITADO]
      </div>
    </div>
  ),
  "mg-suscripcion": () => (
    <div className="space-y-4 font-mono text-xs">
      <h2 className="text-lg text-white font-light">// asignacion_cuotas</h2>
      <div className="p-4 border border-nura-border rounded bg-nura-gray/60 text-white/40">
        Plan Enterprise Dedicado: 142,500 registros de 500,000 procesados este mes.
      </div>
    </div>
  ),
  "mg-integraciones": () => (
    <div className="space-y-4 font-mono text-xs">
      <h2 className="text-lg text-white font-light">// integraciones_api</h2>
      <div className="p-4 border border-nura-border rounded bg-nura-gray/60 text-white/40">
        API REST Analytics activa. Webhooks configurados para notificaciones de procesamiento por lote.
      </div>
    </div>
  ),
  "ad-usuarios": () => (
    <div className="space-y-4 font-mono text-xs">
      <h2 className="text-lg text-white/40 font-light">
        // adm_usuarios{" "}
        <span className="text-[9px] bg-nura-purple/20 text-nura-purple px-1 rounded ml-2">RESERVADO_FUTURO</span>
      </h2>
      <p className="text-white/20">Módulo retenido para control IAM multi-inquilino avanzada.</p>
    </div>
  ),
  "ad-empresas": () => (
    <div className="space-y-4 font-mono text-xs">
      <h2 className="text-lg text-white/40 font-light">
        // adm_organizaciones{" "}
        <span className="text-[9px] bg-nura-purple/20 text-nura-purple px-1 rounded ml-2">RESERVADO_FUTURO</span>
      </h2>
      <p className="text-white/20">Módulo retenido para control de sub-tenants globales.</p>
    </div>
  ),
  "ad-licencias": () => (
    <div className="space-y-4 font-mono text-xs">
      <h2 className="text-lg text-white/40 font-light">
        // adm_licencias{" "}
        <span className="text-[9px] bg-nura-purple/20 text-nura-purple px-1 rounded ml-2">RESERVADO_FUTURO</span>
      </h2>
      <p className="text-white/20">Módulo retenido para firma criptográfica de llaves on-premise.</p>
    </div>
  ),
  "ad-monitoreo": () => (
    <div className="space-y-4 font-mono text-xs">
      <h2 className="text-lg text-white/40 font-light">
        // global_telemetria{" "}
        <span className="text-[9px] bg-nura-purple/20 text-nura-purple px-1 rounded ml-2">RESERVADO_FUTURO</span>
      </h2>
      <p className="text-white/20">Módulo retenido para trazas de telemetría inmutable distribuida.</p>
    </div>
  ),
};

export const ICON_MAP = {
  LayoutDashboard,
  Database,
  Brain,
  MessageSquareText,
  FileText,
  User,
  SlidersHorizontal,
  Package,
  Plug,
  ShieldAlert,
  Network,
  KeyRound,
  ActivitySquare,
  ChevronsUpDown,
  LogOut,
  Search,
  Upload,
  Send,
  Download,
  AlertTriangle,
  TrendingUp,
  FileSpreadsheet,
  Lightbulb,
};