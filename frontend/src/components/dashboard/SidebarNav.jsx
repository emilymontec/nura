import { ChevronsUpDown, LogOut } from "lucide-react";
import { useAuth } from "../../contexts/AuthContext";
import { useNavigate } from "react-router-dom";
import { NAV_SECTIONS } from "./viewContent";
import SidebarButton from "./SidebarButton";

export default function SidebarNav({ currentView, onNavigate }) {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/");
  };

  // Get user initials
  const getUserInitials = () => {
    if (!user) return "OP";
    const firstName = user.first_name || "";
    const lastName = user.last_name || "";
    const username = user.username || "";
    if (firstName && lastName) {
      return `${firstName[0]}${lastName[0]}`.toUpperCase();
    }
    if (firstName) return firstName[0].toUpperCase();
    if (lastName) return lastName[0].toUpperCase();
    return username[0].toUpperCase() || "OP";
  };

  // Get user display name
  const getUserDisplayName = () => {
    if (!user) return "Niels_Operator";
    const firstName = user.first_name || "";
    const lastName = user.last_name || "";
    if (firstName && lastName) {
      return `${firstName} ${lastName}`;
    }
    return user.username || "Niels_Operator";
  };

  return (
    <aside className="w-64 border-r border-nura-border bg-nura-gray flex flex-col justify-between z-10 flex-none">
      <div className="flex flex-col flex-1 overflow-y-auto">
        <div className="p-4 border-b border-nura-border flex items-center justify-between bg-black/20">
          <div className="flex items-center gap-2.5 overflow-hidden">
            <div className="w-6 h-6 rounded bg-gradient-to-br from-nura-electric to-nura-purple flex items-center justify-center font-mono text-[10px] font-bold text-white flex-none">
              N
            </div>
            <div className="flex flex-col truncate">
              <span className="text-xs font-medium text-white tracking-wide truncate">
                NURA INTELLIGENCE
              </span>
              <span className="text-[9px] font-mono text-white/30 truncate">
                analytics_enterprise
              </span>
            </div>
          </div>
          <ChevronsUpDown className="w-3.5 h-3.5 text-white/40 cursor-pointer hover:text-white transition-colors flex-none" />
        </div>

        <div className="p-3 space-y-6 flex-1">
          {NAV_SECTIONS.map((section) => (
            <div key={section.label} className="space-y-0.5">
              <div className="flex items-center justify-between px-2 mb-2">
                <span className="font-mono text-[9px] text-white/20 uppercase tracking-widest block">
                  {section.label}
                </span>
                {section.reserved && (
                  <span className="text-[7px] bg-nura-purple/10 text-nura-purple border border-nura-purple/20 px-1 font-mono rounded">
                    BETA
                  </span>
                )}
              </div>
              {section.items.map((item) => (
                <SidebarButton
                  key={item.id}
                  item={item}
                  isActive={currentView === item.id}
                  onClick={() => onNavigate(item.id)}
                />
              ))}
            </div>
          ))}
        </div>

        <div className="p-3 border-t border-nura-border bg-black/10 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-7 h-7 rounded-full bg-white/5 border border-white/10 flex items-center justify-center font-mono text-xs font-medium">
              {getUserInitials()}
            </div>
            <div className="flex flex-col">
              <span className="text-[11px] font-medium text-white/80">
                {getUserDisplayName()}
              </span>
              <span className="text-[8px] font-mono text-emerald-500">
                Tier: Enterprise
              </span>
            </div>
          </div>
          <button onClick={handleLogout} className="flex items-center justify-center">
            <LogOut className="w-3.5 h-3.5 text-white/30 hover:text-white cursor-pointer transition-colors flex-none" />
          </button>
        </div>
      </div>
    </aside>
  );
}
