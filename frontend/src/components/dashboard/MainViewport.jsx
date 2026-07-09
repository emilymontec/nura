import { VIEW_CONTENT } from "./viewContent";

export default function MainViewport({ currentView }) {
  const ViewComponent = VIEW_CONTENT[currentView];

  return (
    <div className="flex-1 overflow-y-auto p-6 md:p-8" id="saas-main-viewport">
      {ViewComponent ? (
        <ViewComponent />
      ) : (
        <div className="space-y-4 font-mono text-xs">
          <h2 className="text-lg text-white font-light">
            // {currentView || "unknown"}
          </h2>
          <div className="p-4 border border-nura-border rounded bg-nura-gray/60 text-white/40">
            Vista no encontrada.
          </div>
        </div>
      )}
    </div>
  );
}
