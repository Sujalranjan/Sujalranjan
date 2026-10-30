<!--START:HEADER-->
<p align="center">
  <img src="./assets/header.svg" width="100%" alt="Sujal Ranjan" />
</p>

<p align="center">
  <a href="https://github.com/Sujalranjan">
    <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=22&pause=900&color=7cffcb&center=true&vCenter=true&width=680&lines=%3E+Building+AI+systems+that+actually+ship+%F0%9F%9A%80;%3E+Hybrid+search+%C2%B7+RAG+%C2%B7+cited+answers+%F0%9F%94%8E;%3E+Automating+the+work+people+repeat+%E2%9A%99%EF%B8%8F;%3E+Data+pipelines+%26+MLOps%3A+Airflow+%C2%B7+MLflow+%F0%9F%93%88;%3E+Python+%C2%B7+FastAPI+%C2%B7+PostgreSQL+%C2%B7+React" alt="typing intro" />
  </a>
</p>

<p align="center">
  <a href="https://github.com/Sujalranjan?tab=followers"><img src="https://img.shields.io/github/followers/Sujalranjan?style=for-the-badge&logo=github&color=c4b5fd&labelColor=06131f" alt="followers" /></a>
  <img src="https://img.shields.io/badge/status-open%20to%20collaborate-7cffcb?style=for-the-badge&labelColor=06131f" alt="status" />
</p>
<!--END:HEADER-->

---

## `$ whoami`

<!--START:WHOAMI-->
```python
class SujalRanjan:
    role       = "Full-Stack & AI Engineer"
    building   = "WorkFlow-OS: Learns the routine work you repeat across apps and runs it..."
    focus      = ["retrieval & RAG", "LLM-powered automation", "data pipelines & MLOps"]
    learning   = ["retrieval evaluation", "agentic workflows", "production ML"]
    open_to    = ["collaborations", "hackathons", "open source"]
    philosophy = "If I do it twice, I automate it the third time."

    def say_hi(self):
        print("Thanks for dropping by. Let's build something that saves people time! ⚡")
```
<!--END:WHOAMI-->

## ⚡ Impact at a Glance

<!--START:IMPACT-->
<table>
<tr>
<td align="center" width="25%"><h2>+5.3%</h2><sub>Recall@5 from hybrid search over vector-only (BEIR SciFact)<br/><a href="https://github.com/Sujalranjan/MemBrain">MemBrain</a></sub></td>
<td align="center" width="25%"><h2>513K</h2><sub>real road-collision records in an Airflow + MLflow pipeline<br/><a href="https://github.com/Sujalranjan/Traffic-Accident-Severity-Analytics-and-Prediction">Traffic Analytics</a></sub></td>
<td align="center" width="25%"><h2>86</h2><sub>automated tests in CI on Python 3.10 and 3.12<br/><a href="https://github.com/Sujalranjan/MemBrain">MemBrain</a></sub></td>
<td align="center" width="25%"><h2>216</h2><sub>contributions in the last year</sub></td>
</tr>
</table>
<!--END:IMPACT-->

---

## 🌟 Featured Projects

<!--START:FEATURED-->
<table>
<tr>
<td width="50%" valign="top">
<h3>🧠 <a href="https://github.com/Sujalranjan/MemBrain">MemBrain</a></h3>
<p>A self-hosted knowledge base for teams: capture notes, decisions, SOPs and voice memos, then search by meaning and get cited answers.</p>
<ul><li>Hybrid vector + BM25 search fused with RRF: +5.3% Recall@5 on BEIR SciFact</li><li>BM25 written in SQL lifted keyword Recall@5 from 0.07 to 0.75</li><li>All in PostgreSQL: pgvector, job queue and rate limiting; 86 tests in CI</li></ul>
<p><img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python" /> <img src="https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white" alt="FastAPI" /> <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white" alt="PostgreSQL" /> <img src="https://img.shields.io/badge/pgvector-336791?style=flat-square&logo=postgresql&logoColor=white" alt="pgvector" /> <img src="https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white" alt="Docker" /></p>
<p><a href="https://github.com/Sujalranjan/MemBrain"><b>Code →</b></a></p>
</td>
<td width="50%" valign="top">
<h3>⚙️ <a href="https://github.com/Sujalranjan/WorkFlow-OS">WorkFlow OS</a></h3>
<p>Watches the routine work you repeat across apps, turns it into a workflow you approve, then runs it for you, with a dry run first.</p>
<ul><li>Desktop agent and browser extension observe real activity</li><li>Deterministic action catalog; LLM output is validated so it can&#x27;t re-route steps</li><li>Executes through Gmail, a CRM and Slack, each with an independent verifier</li></ul>
<p><img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python" /> <img src="https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white" alt="FastAPI" /> <img src="https://img.shields.io/badge/React-20232A?style=flat-square&logo=react&logoColor=white" alt="React" /> <img src="https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white" alt="TypeScript" /> <img src="https://img.shields.io/badge/LLMs-8A2BE2?style=flat-square&logo=openai&logoColor=white" alt="LLMs" /></p>
<p><a href="https://github.com/Sujalranjan/WorkFlow-OS"><b>Code →</b></a></p>
</td>
</tr>
<tr>
<td width="50%" valign="top">
<h3>🚦 <a href="https://github.com/Sujalranjan/Traffic-Accident-Severity-Analytics-and-Prediction">Traffic Accident Analytics</a></h3>
<sub>👥 Team project · 🟢 Live demo</sub><br/><p>End-to-end data engineering and MLOps system that predicts accident severity from UK road-safety and weather data.</p>
<ul><li>513,801 STATS19 collisions joined with hourly Open-Meteo weather</li><li>Star-schema warehouse in PostgreSQL/PostGIS behind a data-quality gate</li><li>Airflow DAG with MLflow tracking and conditional retraining</li></ul>
<p><img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python" /> <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white" alt="PostgreSQL" /> <img src="https://img.shields.io/badge/Airflow-017CEE?style=flat-square&logo=apacheairflow&logoColor=white" alt="Airflow" /> <img src="https://img.shields.io/badge/MLflow-0194E2?style=flat-square&logo=mlflow&logoColor=white" alt="MLflow" /> <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white" alt="Streamlit" /></p>
<p><a href="https://github.com/Sujalranjan/Traffic-Accident-Severity-Analytics-and-Prediction"><b>Code →</b></a> &nbsp;·&nbsp; <a href="https://traffic-accident-severity-analytics-and-prediction-3yzwgf7tuhc.streamlit.app/"><b>Live demo ↗</b></a></p>
</td>
<td width="50%" valign="top">
<h3>🗺️ <a href="https://github.com/Sujalranjan/GitOnboard">GitOnboard</a></h3>
<sub>👥 Team project</sub><br/><p>Turns any GitHub repository into an interactive knowledge graph so new developers onboard faster.</p>
<ul><li>Multi-language AST parsing with Tree-sitter</li><li>Semantic code search, dependency and impact analysis</li><li>FastAPI + Next.js + PostgreSQL, all in Docker Compose</li></ul>
<p><img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python" /> <img src="https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white" alt="FastAPI" /> <img src="https://img.shields.io/badge/Next.js-000000?style=flat-square&logo=nextdotjs&logoColor=white" alt="Next.js" /> <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white" alt="PostgreSQL" /> <img src="https://img.shields.io/badge/Tree--sitter-5E7C3C?style=flat-square&logo=treesitter&logoColor=white" alt="Tree-sitter" /></p>
<p><a href="https://github.com/Sujalranjan/GitOnboard"><b>Code →</b></a></p>
</td>
</tr>
</table>
<!--END:FEATURED-->

---

## 🧠 Tech Arsenal
<sub>Auto-detected from the languages, dependencies and topics in my repos. It grows every time I pick up something new.</sub>

<!--START:SKILLS-->
<h4>💻 Languages</h4>
<p>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white" alt="TypeScript" />
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white" alt="HTML5" />
  <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=white" alt="JavaScript" />
</p>
<h4>⚙️ Frameworks & Libraries</h4>
<p>
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/Pydantic-E92063?style=for-the-badge&logo=pydantic&logoColor=white" alt="Pydantic" />
  <img src="https://img.shields.io/badge/Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white" alt="Pytest" />
  <img src="https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white" alt="SQLAlchemy" />
  <img src="https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=white" alt="React" />
  <img src="https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white" alt="scikit-learn" />
  <img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" alt="Pandas" />
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit" />
  <img src="https://img.shields.io/badge/Claude%20API-D97757?style=for-the-badge&logo=anthropic&logoColor=white" alt="Claude API" />
  <img src="https://img.shields.io/badge/Expo-000020?style=for-the-badge&logo=expo&logoColor=white" alt="Expo" />
  <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask" />
  <img src="https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white" alt="Next.js" />
  <img src="https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white" alt="OpenAI" />
  <img src="https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white" alt="Plotly" />
  <img src="https://img.shields.io/badge/React%20Native-61DAFB?style=for-the-badge&logo=react&logoColor=white" alt="React Native" />
  <img src="https://img.shields.io/badge/Tailwind%20CSS-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white" alt="Tailwind CSS" />
  <img src="https://img.shields.io/badge/Tree--sitter-5E7C3C?style=for-the-badge&logo=treesitter&logoColor=white" alt="Tree-sitter" />
</p>
<h4>🛠️ Tools, Platforms & Integrations</h4>
<p>
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker" />
  <img src="https://img.shields.io/badge/GitHub%20Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white" alt="GitHub Actions" />
  <img src="https://img.shields.io/badge/Google%20APIs-4285F4?style=for-the-badge&logo=google&logoColor=white" alt="Google APIs" />
  <img src="https://img.shields.io/badge/Chrome%20Extensions-4285F4?style=for-the-badge&logo=googlechrome&logoColor=white" alt="Chrome Extensions" />
  <img src="https://img.shields.io/badge/MLflow-0194E2?style=for-the-badge&logo=mlflow&logoColor=white" alt="MLflow" />
  <img src="https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white" alt="MongoDB" />
  <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL" />
  <img src="https://img.shields.io/badge/pgvector-336791?style=for-the-badge&logo=postgresql&logoColor=white" alt="pgvector" />
  <img src="https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white" alt="Git" />
  <img src="https://img.shields.io/badge/LLMs-8A2BE2?style=for-the-badge&logo=openai&logoColor=white" alt="LLMs" />
  <img src="https://img.shields.io/badge/REST%20APIs-FF6C37?style=for-the-badge&logo=postman&logoColor=white" alt="REST APIs" />
</p>
<!--END:SKILLS-->

---

## 🔭 More Builds
<sub>Updated automatically. A new repo shows up here on its own.</sub>

<!--START:PROJECTS-->
| 🚀 Project | 📝 What it does | 🧰 Stack | 🕒 Updated |
|---|---|---|---|
| [**placement-prediction**](https://github.com/Sujalranjan/placement-prediction) <sub>👥 team</sub> | End-to-end Student Placement & Salary Package Prediction dashboard using a calibrated Scikit-Learn Random F… | `Python` | 1 mo ago |
| [**MailEaseAI**](https://github.com/Sujalranjan/MailEaseAI) | AI email assistant: syncs your inbox over IMAP, groups threads and turns emails into tasks with deadlines. | `Python` | 1 mo ago |
| [**Smart-Bill-Reader**](https://github.com/Sujalranjan/Smart-Bill-Reader) | AI-Powered Expense Automation Platform built with React Native and Python Flask. Features automated invoice… | `TypeScript` | 11 mo ago |
<!--END:PROJECTS-->

---

## 📊 Code Telemetry

<!--START:LANGS-->
```text
$ git-stats --languages --user Sujalranjan

Python            ████████████████████░░░░░   80.2 %
TypeScript        ███░░░░░░░░░░░░░░░░░░░░░░   12.5 %
HTML              ██░░░░░░░░░░░░░░░░░░░░░░░    6.4 %
JavaScript        ░░░░░░░░░░░░░░░░░░░░░░░░░    0.9 %
```
<!--END:LANGS-->

<!--START:STATS-->
<p align="center">
  <img height="170" src="https://github-readme-stats.vercel.app/api?username=Sujalranjan&show_icons=true&hide_border=true&count_private=true&include_all_commits=true&rank_icon=github&bg_color=0b1a24&title_color=7cffcb&icon_color=c4b5fd&text_color=d7f7ff&ring_color=7cffcb" alt="GitHub stats" />
  <img height="170" src="https://streak-stats.demolab.com?user=Sujalranjan&hide_border=true&background=0b1a24&ring=7cffcb&fire=c4b5fd&currStreakNum=7cffcb&currStreakLabel=7cffcb&sideNums=d7f7ff&sideLabels=d7f7ff&dates=d7f7ff&stroke=c4b5fd" alt="GitHub streak" />
</p>
<!--END:STATS-->

---

## ⚡ Live Activity Feed

<!--START:ACTIVITY-->
1. ⬆️ Pushed 1 commit to [Sujalranjan/GitOnboard](https://github.com/Sujalranjan/GitOnboard) · <sub>5 d ago</sub>
2. ⬆️ Pushed 1 commit to [Sujalranjan/WorkFlow-OS](https://github.com/Sujalranjan/WorkFlow-OS) · <sub>6 d ago</sub>
3. ⬆️ Pushed 1 commit to [Sujalranjan/Sujalranjan](https://github.com/Sujalranjan/Sujalranjan) · <sub>6 d ago</sub>
4. ⬆️ Pushed 1 commit to [Sujalranjan/WorkFlow-OS](https://github.com/Sujalranjan/WorkFlow-OS) · <sub>6 d ago</sub>
5. ⬆️ Pushed 1 commit to [Sujalranjan/MemBrain](https://github.com/Sujalranjan/MemBrain) · <sub>8 d ago</sub>
<!--END:ACTIVITY-->

---

## 🐍 Contribution Hunter

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/snake-dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="./assets/snake-light.svg" />
  <img alt="A snake slithering across my contribution graph, eating each active day" src="./assets/snake-dark.svg" width="100%" />
</picture>

---

## 🤝 Let's Connect

<!--START:CONNECT-->
<p align="center">
  <a href="https://github.com/Sujalranjan"><img src="https://img.shields.io/badge/GitHub-Sujalranjan-181717?style=for-the-badge&logo=github" alt="GitHub" /></a>
</p>
<!--END:CONNECT-->

<p align="center">
<!--START:UPDATED-->
<sub>🤖 Auto-generated by GitHub Actions · last sync 30 Oct 2026, 05:29 UTC · 7 public repos scanned</sub>
<!--END:UPDATED-->
</p>

<img src="./assets/footer.svg" width="100%" alt="" />
