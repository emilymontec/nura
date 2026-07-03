import React, { useState, useEffect } from 'react';

const queries = [
  "¿qué está pasando con las ventas esta semana?",
  "¿por qué subieron las devoluciones de SKU-4872?",
  "¿qué canal está creciendo más rápido este mes?"
];

function LivePanel() {
  const [timeStr, setTimeStr] = useState('');
  const [queryText, setQueryText] = useState('');
  const [queryIndex, setQueryIndex] = useState(0);
  const [charIndex, setCharIndex] = useState(0);
  const [isDeleting, setIsDeleting] = useState(false);

  useEffect(() => {
    const updateTime = () => {
      const d = new Date();
      const hh = String(d.getHours()).padStart(2, '0');
      const mm = String(d.getMinutes()).padStart(2, '0');
      const ss = String(d.getSeconds()).padStart(2, '0');
      setTimeStr(`${hh}:${mm}:${ss} · en vivo`);
    };
    updateTime();
    const interval = setInterval(updateTime, 1000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    let timeout;
    const currentQuery = queries[queryIndex];

    const tick = () => {
      if (!isDeleting) {
        setCharIndex((prev) => prev + 1);
        if (charIndex >= currentQuery.length) {
          timeout = setTimeout(() => {
            setIsDeleting(true);
          }, 2200);
          return;
        }
      } else {
        setCharIndex((prev) => prev - 1);
        if (charIndex <= 0) {
          setIsDeleting(false);
          setQueryIndex((prev) => (prev + 1) % queries.length);
        }
      }
    };

    const delay = isDeleting ? 28 : 42;
    timeout = setTimeout(tick, delay);

    return () => clearTimeout(timeout);
  }, [charIndex, isDeleting, queryIndex]);

  useEffect(() => {
    const currentQuery = queries[queryIndex];
    setQueryText(currentQuery.slice(0, charIndex));
  }, [charIndex, queryIndex]);

  return (
    <section className="live-sec" id="panel">
      <div className="section-eyebrow">
        <span className="mark">§ EN VIVO</span>
        <h2>Lo que Nura escuchó hoy</h2>
      </div>

      <div className="ticket">
        <div className="ticket-head">
          <div className="ticket-head-l">
            <span className="rec-dot"></span>
            <span>nura-agent · canal-01 · señal estable</span>
          </div>
          <span className="ticket-v">{timeStr}</span>
        </div>

        <div className="ticket-body">
          <span className="query-line">
            {queryText}
            <span style={{ display: 'inline-block', width: '7px', height: '13px', background: 'var(--brass)', marginLeft: '2px', verticalAlign: '-2px', animation: 'blink 1s step-end infinite' }}></span>
          </span>

          <div>
            <div className="reply-meta">Nura — lectura del canal</div>
            <p className="reply-text">
              Señal captada y normalizada contra la línea base trimestral. Dos lecturas se salen del rango esperado y merecen tu atención:
            </p>

            <div className="ledger">
              <div className="ledger-row">
                <span className="lr-time">14:23</span>
                <span className="lr-tag">Ventas</span>
                <span className="lr-desc">El canal <b>B2B Enterprise</b> acelera su margen bruto de forma sostenida.</span>
                <span className="lr-val">↑ 3.2x</span>
              </div>
              <div className="ledger-row">
                <span className="lr-time">14:18</span>
                <span className="lr-tag">Logística</span>
                <span className="lr-desc">Las devoluciones de <b>SKU-4872</b> superan el umbral de tolerancia.</span>
                <span className="lr-val alert">↑ 340%</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

export default LivePanel;
