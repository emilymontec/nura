import React from 'react';

function AmbientBackground() {
  return (
    <>
      <div className="bg-ambient"></div>
      <svg className="bg-grain" width="0" height="0">
        <filter id="grain">
          <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" stitchTiles="stitch" />
          <feColorMatrix type="saturate" values="0" />
        </filter>
      </svg>
      <div className="bg-grain" style={{ filter: 'url(#grain)', opacity: 0.035 }}></div>
    </>
  );
}

export default AmbientBackground;
