import React, { useEffect, useRef } from 'react';

function Specs() {
  const dialRefs = useRef([]);

  useEffect(() => {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => {
          if (e.isIntersecting) {
            const el = e.target;
            el.style.strokeDashoffset = el.getAttribute('data-target');
            io.unobserve(el);
          }
        });
      },
      { threshold: 0.4 }
    );

    dialRefs.current.forEach((d) => {
      if (d) io.observe(d);
    });

    return () => {
      io.disconnect();
    };
  }, []);

  return (
    <section className="spec-sec" id="instrumento">
      <div className="section-eyebrow">
        <span className="mark">§ INSTRUMENTO</span>
        <h2>Cómo escucha Nura</h2>
      </div>

      <div className="specs-grid">
        <div className="spec-card">
          <span className="spec-tag">Ingesta</span>
          <div className="spec-title">Cero ETL manual</div>
          <div className="spec-desc">Conectores de lectura automática que ingieren esquemas relacionales complejos (SAP, Salesforce, Postgres) y mapean claves primarias sin intervención.</div>
        </div>

        <div className="spec-card wide">
          <span className="spec-tag">Procesamiento</span>
          <div className="spec-title">De ruido a señal, sin fricción</div>
          <div className="module-list">
            <div className="module-item">
              <div className="module-t">Modelado semántico directo</div>
              <div className="module-d">Nura convierte filas crudas en un grafo lógico que entiende conceptos reales del negocio, no solo columnas.</div>
            </div>
            <div className="module-item">
              <div className="module-t">Inferencia predictiva continua</div>
              <div className="module-d">Escanea correlaciones en segundo plano para avisarte antes del cierre de mes, no después.</div>
            </div>
          </div>
        </div>
      </div>

      <div className="dials-grid">
        <div className="dial-card">
          <svg className="dial-svg" width="64" height="64" viewBox="0 0 64 64">
            <circle className="dial-track" cx="32" cy="32" r="27" />
            <circle ref={(el) => (dialRefs.current[0] = el)} className="dial-fill" cx="32" cy="32" r="27" strokeDasharray="169.6" strokeDashoffset="169.6" data-target="17" />
            <text className="dial-num" x="32" y="37" textAnchor="middle">10x</text>
          </svg>
          <div className="dial-info">
            <div className="dt">Velocidad</div>
            <div className="dd">de lectura frente a un análisis manual.</div>
          </div>
        </div>

        <div className="dial-card">
          <svg className="dial-svg" width="64" height="64" viewBox="0 0 64 64">
            <circle className="dial-track" cx="32" cy="32" r="27" />
            <circle ref={(el) => (dialRefs.current[1] = el)} className="dial-fill" cx="32" cy="32" r="27" strokeDasharray="169.6" strokeDashoffset="169.6" data-target="3.4" />
            <text className="dial-num" x="32" y="37" textAnchor="middle">98%</text>
          </svg>
          <div className="dial-info">
            <div className="dt">Precisión</div>
            <div className="dd">en la detección algorítmica de anomalías.</div>
          </div>
        </div>

        <div className="dial-card">
          <svg className="dial-svg" width="64" height="64" viewBox="0 0 64 64">
            <circle className="dial-track" cx="32" cy="32" r="27" />
            <circle ref={(el) => (dialRefs.current[2] = el)} className="dial-fill" cx="32" cy="32" r="27" strokeDasharray="169.6" strokeDashoffset="169.6" data-target="144.2" />
            <text className="dial-num" x="32" y="37" textAnchor="middle">&lt;2h</text>
          </svg>
          <div className="dial-info">
            <div className="dt">Latencia</div>
            <div className="dd">desde la ingesta hasta el primer insight.</div>
          </div>
        </div>
      </div>
    </section>
  );
}

export default Specs;
