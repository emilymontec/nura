<div align="center">

# NURA

<p align="center">
  <strong>conversational business intelligence platform powered by artificial intelligence</strong>
</p>

<p align="center">
  <a href="https://nura-bi.onrender.com/">Quickstart</a> ·
  <a href="https://nura-bi.onrender.com/">Dashboard</a>
</p>

<img src="https://img.shields.io/badge/backend-django-24c1ca?style=flat-square">
<img src="https://img.shields.io/badge/frontend-HMTML5/CSS3/JavaScript-da30a2?style=flat-square">
<img src="https://img.shields.io/badge/database-supabase-0950cb?style=flat-square">
<img src="https://img.shields.io/badge/ai-multi--llm-b156ff?style=flat-square">

</div>

NURA (Neural Unified Reasoning Analytics) is an artificial intelligence platform designed for conversational business analytics.

Its purpose is to transform structured data into actionable insights through a natural experience based on human language.

NURA aims to bridge the gap between data and decision-making, enabling any user, regardless of their technical expertise, to interact with complex information as if they were conversing with a senior analyst, a strategic consultant, or a business intelligence director.

<div align="center">

| | |
|---|---|
| Analyze datasets automatically. | Detect risks and opportunities. |
| Generate executive reports. | Interact using natural language. |
| Understand business context. | Receive strategic recommendations. |

</div>

> Home capture
<!--![dashboard](file_docs/dashboard.jpeg)-->

---

## Objective
NURA's primary objective is to democratize business analytics by enabling any user to understand, explore, and act upon their data through intelligent conversations.<br> The platform seeks to bridge the gap between raw information and strategic decision-making.

---


## Analytics Engine
It is the mathematical and statistical core of NURA.
Its mission is to transform raw data into structured information.

<table>
<tr>
<td width="25%" valign="top">
<h3>Dataset Analyzer</h3>

Analyze:
* rows
* columns
* data types
* nulls
* duplicates

</td>
<td width="25%" valign="top">
<h3>Trend Analysis</h3>

Detects:
* growth
* decline
* seasonality
* fluctuations

</td>
<td width="25%" valign="top">
<h3>Business Scoring</h3>

Calculates:
* health score
* risk score
* dataset quality
</td>
<td width="25%" valign="top">
<h3>Insight Generator</h3>

Generate automatic comments.
* findings
* alerts
* observations
* recommendations

</td>
</tr>
</table>

---

## Business Intelligence Layer
Translate technical columns into business concepts.

### Semantic Detection
Automatically identifies:

| **Column** | **Category** |
|----------|----------|
| Revenue | Finance |
| Sales | Sales |
| Customers | Customer Analytics |
| Refunds | Risk |
| Costs | Operations |
| Dates | Time Series |


### Benefit
Enables the AI to understand the business context of the dataset.

---

## AI Engine
It is the brain of NURA. It turns analytical results into understandable answers.

<table>
  <tr>
    <td width="25%" valign="top">
      <h3>🚀 Capabilities</h3>
      converts metrics into natural language
    </td>
    <td width="25%" valign="top">
      <h3>🧠 Reasoning</h3>
      relates multiple variables
    </td>
    <td width="25%" valign="top">
      <h3>💬 Interpretation</h3>
      extracts business insights
    </td>
    <td width="25%" valign="top">
      <h3>📝 Report Generation</h3>
      generates executive reports, diagnostics, and summaries comments
    </td>
  </tr>
</table>

---

### Example Questions
Risk:
```bash
What risks do you see?
```
Strategy:
```bash
What should I prioritize?
```
Executive Leadership:
```bash
What would a CEO do?
```
Optimization:
```bash
How would I improve this business?
```

## Conversational Memory
Its purpose is to maintain consistency across interactions.

### Stored Information
<table>
<tr>
<td width="33%" valign="top">
<h3>Short Term Memory</h3>

* recent questions
* recent answers

</td>
<td width="33%" valign="top">
<h3>Medium Term Memory</h3>

* dataset context
* discussed topics

</td>
<td width="33%" valign="top">
<h3>Long Term Memory (Roadmap)</h3>

* preferences
* business history
* accumulated knowledge

</td>
</tr>
</table>

---

## Multi-Agent System
<table width="100%">
<tr>
<td width="50%" valign="top">
<h3>⚠️ Risk Agent</h3>

**Functions:**
* anomalies
* problems
* risks
**Typical Questions:**
* What's wrong?
* Where is the danger?
</td>
<td width="50%" valign="top">
<h3>💡 Insights Agent</h3>

**Functions:**
* trends
* patterns
* opportunities
**Questions:**
* What did you discover?
* What trend do you see?
</td>
</tr>
<tr>
<td width="50%" valign="top">
<h3>👌 Recommendation Agent</h3>

**Functions:**
* optimization
* strategies
* prioritization
**Questions:**
* What would you do?
* What do you recommend?
</td>
<td width="50%" valign="top">
<h3>🧾 Executive Agent</h3>

**Status:** Planned.
**Objective:** To simulate executive thinking.
* strategic vision
* prioritization
* resource allocation
* high-level decision-making
</td>
</tr>
</table>

---

## Smart Routing
Route each inquiry to the appropriate specialist.

### Example:
```bash
What risks do you see?  # Risk Agent
```
```bash
What opportunities are there?   # Insights Agent
```
```bash
How would you improve this business?  # Recommendation Agent
```

---

## Multi-LLM System
Reduce dependence on a single provider.

### Architecture
```bash
User Query → Router → Provider Selector → Available Model
```

---

## Current Providers
<table>
<tr>
<td width="33%" valign="top">

<h3><a href="https://groq.com/" target="_blank">Groq</a></h3>

Use:
* low latency
* fast responses

</td>
<td width="33%" valign="top">

<h3><a href="https://www.cerebras.ai/" target="_blank">Cerebras</a></h3>

Use:
* efficient inference
* computation-intensive processing

</td>
<td width="33%" valign="top">

<h3><a href="https://openrouter.ai/" target="_blank">OpenRouter</a></h3>

Use:
* access to multiple models

</td>
</tr>
</table>

---

## Intelligent Fallback System
Ensures availability.

```bash
Groq → Cerebras → OpenRouter
```

If a provider becomes unavailable, NURA automatically switches to the next available provider without interrupting the user experience.

---

## Security and Governance
### Recommendations

|  |  |
|----------|----------|
| **Security** | HTTPS required, AES-256 encryption, JWT tokens, rate limiting |
| **Data Protection** | anonymization, removal of PII, access control |
| **Auditing** | logging of queries, responses, AI decisions, access logs |

---

## Business Use Cases
<table>
<tr>
<td width="20%" valign="top">

<h3>Companies</h3>

* Financial analysis
* KPI monitoring
* Risk management

</td>
<td width="20%" valign="top">

<h3>Marketing</h3>

* Campaign analysis
* Conversion optimization
* Audience insights

</td>
<td width="20%" valign="top">

<h3>Ecommerce</h3>

* Sales analytics
* Customer retention
* Revenue growth

</td>
<td width="20%" valign="top">

<h3>Startups</h3>

* Growth tracking
* Product analytics
* Business intelligence

</td>
<td width="20%" valign="top">

<h3>📑 Consulting</h3>

* Diagnostics
* Executive reports
* Recommendations

</td>
</tr>
</table>

---

## Competitive Advantages
### Business Intelligence Conversation
Ask questions naturally instead of building dashboards.

### Strategic Reasoning
NURA interprets data from a business perspective.

### Multi-Agent Intelligence
Specialized AI experts collaborate on analysis.

### Multi-LLM Architecture
No dependency on a single AI provider.

### Enterprise Scalability
Designed to evolve into a complete SaaS platform.

---

## Tools Used

<img src="https://img.shields.io/badge/Django-+6.0-24c1ca?style=flat-square"> <img src="https://img.shields.io/badge/Pandas-+3.0-da30a2?style=flat-square"> <img src="https://img.shields.io/badge/NumPy-+2.4-0950cb?style=flat-square"> <img src="https://img.shields.io/badge/ScikitLearn-+1.8-b156ff?style=flat-square"> <img src="https://img.shields.io/badge/Groq-+1.2-24c1ca?style=flat-square"> <img src="https://img.shields.io/badge/OpenRouter-+2.3-da30a2?style=flat-square"> <img src="https://img.shields.io/badge/Cerebras-+1.6-b156ff?style=flat-square"> <img src="https://img.shields.io/badge/HTML-5-24c1ca?style=flat-square"> <img src="https://img.shields.io/badge/CSS-3-da30a2?style=flat-square"> <img src="https://img.shields.io/badge/Bootstrap-26-0950cb?style=flat-square"> <img src="https://img.shields.io/badge/Supabase-PostgreSQL-b156ff?style=flat-square">

---

## System Architecture
```bash
nura
  ↓
Frontend
  ↓
Backend API
  ↓
Analytics Engine
  ↓
Business Intelligence Layer
  ↓
AI Engine
  ↓
Memory Layer
  ↓
Multi-Agent System
  ↓
Multi-LLM Providers
```

---

## Quick install
```bash
git clone https://github.com/emilymontec/nura.git; cd nura
```
<sub> clone the repository </sub>

### Install dependencies
```bash
pip install -r requirements.txt
```
### Environment variables
```bash
GROQ_API_KEY=GROQ_API_KEY
OPENROUTER_API_KEY=OPENROUTER_API_KEY
CEREBRAS_API_KEY=CEREBRAS_API_KEY
SUPABASE_DB_URL=SUPABASE_DB_URL
POSTGRES_SSLMODE=require
USE_SQLITE_LOCAL=False
SQLITE_DB_PATH=db.sqlite3
```
<sub> create the `.env` file and set the environment variables </sub>

### Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```
Make the database migrations and create the superuser.
```bash
Create superuser:
python manage.py createsuperuser
```

### Run the application
```bash
python manage.py runserver
```
<sub> Application available at: http://127.0.0.1:8000 </sub>

---

## File Structure
```bash
nura/
│
├── nura/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── analytics/
├── ai/
├── chat/
│
├── templates/
│   ├── assets/
│   ├── scripts/
│   ├── styles/
│   ├── views/
│   └── index.html
│
├── manage.py
├── requirements.txt
├── .env
└── README.md
```

---

## Long-Term Vision
NURA aims to become an autonomous business copilot capable of:

* Understanding businesses.
* Detecting risks automatically.
* Discovering opportunities.
* Simulating future scenarios.
* Recommending strategic actions.
* Generating executive reports.
* Assisting organizations in decision-making.

The ultimate goal is to evolve from a conversational analytics platform into a fully autonomous Business Intelligence system powered by Artificial Intelligence.

---

## Contributing
### Fork repository

**Create branch**
```bash
git checkout -b feature/my-feature
```

**Commit changes**
```bash
git commit -m "Add new feature"
```

**Push changes**
```bash
git push origin feature/my-feature
```
Open a Pull Request describing the proposed changes.

---

## Author
**Emily Monterrosa Castro - Full Stack Developer** <br>
[GitHub](https://github.com/emilymontec) · [LinkedIn](https://www.linkedin.com/in/emilymontec/) · [Portfolio](https://emilymontec.github.io/portfolio/)

---

## License

Apache License 2.0

See the [LICENSE](LICENSE) file for additional information.
