import PublicHeader from "../landing/PublicHeader";
import PublicHero from "../landing/PublicHero";
import PublicFeatures from "../landing/PublicFeatures";
import PublicMetrics from "../landing/PublicMetrics";
import PublicCTA from "../landing/PublicCTA";
import PublicFooter from "../landing/PublicFooter";

export default function NewLanding() {
  return (
    <div className="bg-nura-black text-white font-sans antialiased selection:bg-nura-electric/20 overflow-x-hidden min-h-screen">
      <div className="fixed inset-0 overflow-hidden pointer-events-none z-0 tech-grid-public">
        <div className="absolute top-[-10%] left-[25%] w-[70vw] h-[40vw] rounded-full bg-nura-electric ambient-glow animate-pulse-slow" />
        <div className="absolute top-[40%] right-[-10%] w-[50vw] h-[50vw] rounded-full bg-nura-purple ambient-glow" />
      </div>

      <PublicHeader />
      <PublicHero />
      <PublicFeatures />
      <PublicMetrics />
      <PublicCTA />
      <PublicFooter />
    </div>
  );
}
