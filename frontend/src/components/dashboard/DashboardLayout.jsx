import { useState, useCallback } from "react";
import SidebarNav from "./SidebarNav";
import HeaderBar from "./HeaderBar";
import MainViewport from "./MainViewport";
import TelemetryPanel from "./TelemetryPanel";
import DashboardFooter from "./DashboardFooter";
import { NAV_SECTIONS } from "./viewContent";

function findItemLabel(viewId) {
  for (const section of NAV_SECTIONS) {
    for (const item of section.items) {
      if (item.id === viewId) return item.label;
    }
  }
  return viewId;
}

export default function DashboardLayout() {
  const [currentView, setCurrentView] = useState("dashboard");

  const handleNavigate = useCallback((viewId) => {
    setCurrentView(viewId);
  }, []);

  const handleNewAnalysis = useCallback(() => {
    setCurrentView("datasets");
  }, []);

  const label = findItemLabel(currentView);
  const sysPath = `root / ${label}`;

  return (
    <div className="bg-nura-black text-white font-sans antialiased h-screen flex overflow-hidden select-none">
      <div className="fixed inset-0 pointer-events-none z-0 tech-grid">
        <div className="absolute top-[-30%] right-[-10%] w-[50vw] h-[50vw] rounded-full bg-nura-electric/10 filter blur-[120px] animate-pulse-slow" />
      </div>

      <SidebarNav currentView={currentView} onNavigate={handleNavigate} />

      <main className="flex-1 bg-nura-black z-10 flex flex-col overflow-hidden relative">
        <HeaderBar currentPath={sysPath} onNewAnalysis={handleNewAnalysis} />
        <MainViewport currentView={currentView} />
        <DashboardFooter />
      </main>

      <TelemetryPanel />
    </div>
  );
}
