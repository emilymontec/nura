import React, { useEffect } from 'react';
import Navigation from '../landing/Navigation';
import AmbientBackground from '../landing/AmbientBackground';
import Hero from '../landing/Hero';
import LivePanel from '../landing/LivePanel';
import Specs from '../landing/Specs';
import Footer from '../landing/Footer';
import '../../styles/landing.css';

function Home() {
  useEffect(() => {
    // Add the class to body for specific background handling if needed, 
    // or we just wrap everything in .nura-landing
    document.body.classList.add('landing-active');
    return () => {
      document.body.classList.remove('landing-active');
    };
  }, []);

  return (
    <div className="nura-landing">
      <AmbientBackground />
      <Navigation />
      <div className="container">
        <Hero />
        <LivePanel />
        <Specs />
        <Footer />
      </div>
    </div>
  );
}

export default Home;
