# ✦ Glintly
### Your curated window into AI — powered by Gemini.

> Built by **Nungo Tshidzumba** | Creative Technologist  
> Originally a hackathon project, fully redesigned and owned as a solo product.

---

## What is Glintly?

Glintly is an intelligent AI news and tools platform that automatically surfaces what matters in the world of artificial intelligence — without you having to hunt for it.

The AI space moves at a relentless pace. New models, tools, research papers, and breakthroughs drop every single day. Glintly solves the signal-to-noise problem by aggregating live news from the top AI publications and curating a directory of 47+ essential AI tools — all in one clean, editorial-quality interface.

Every tool page comes with an instant AI explanation powered by Google Gemini and an automatically fetched YouTube tutorial, so users go from discovery to understanding in seconds.

**Glintly is built to run itself.** No manual content updates. No admin babysitting. The news refreshes from live RSS feeds on every page load, and the tools directory is seeded with real, curated data that can be re-seeded with a single command.

---

## ✦ Live Features (Phase 1)

### 🗞 Live AI News
- Automatically pulls the latest AI news from **5 top publications** via RSS feeds:
  - TechCrunch AI, VentureBeat AI, The Verge AI, Ars Technica, Wired AI
- No API key required — completely free and self-updating
- Filterable by search query on the News page
- Graceful fallback to sample articles if feeds are unreachable

### 🤖 Gemini AI Chat (Homepage)
- Conversational AI assistant powered by **Google Gemini 2.5 Flash**
- Ask anything about AI tools, concepts, or news
- Maintains a session-based conversation history (last 5 exchanges)
- Clean chat bubble UI with timestamps

### 🧰 AI Tools Directory (47 tools across 6 categories)
- **NLP** — ChatGPT, Claude, Gemini, Perplexity, Hugging Face, Mistral, Cohere, Grammarly, Jasper, Notion AI
- **Code** — GitHub Copilot, Cursor, Claude Code, Replit, Tabnine, Bolt.new, v0, Windsurf
- **Image** — Midjourney, DALL-E 3, Stable Diffusion, Adobe Firefly, Ideogram, Canva AI, Flux
- **Machine Learning** — HF Transformers, LangChain, TensorFlow, PyTorch, W&B, Ollama, LlamaIndex, Vertex AI
- **Vision** — Roboflow, Google Vision AI, Luma AI, Runway ML, Sora
- **Audio** — ElevenLabs, Whisper, Suno AI, Udio, Adobe Podcast, Descript
- Filter by category, search by name, sort A→Z / newest / popular
- Featured and Popular badges

### ✨ Per-Tool AI Explanations
- Every tool detail page has an "Ask Glintly AI" panel
- Gemini generates a conversational, plain-English explanation on demand
- Auto-generates a smart query if none is configured — fully autonomous
- "Thinking..." loading state for smooth UX

### 📺 YouTube Tutorial Cards
- Each tool page automatically fetches a relevant YouTube tutorial via YouTube Data API v3
- Shows video thumbnail with play button — click to open on YouTube
- Verified embeddable results using YouTube's videos.list status check

### 📱 Fully Responsive
- Mobile burger menu with full-screen drawer navigation
- Responsive grid layouts for tools and news
- Works cleanly on desktop, tablet, and mobile

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.13, Django 5.2.1 |
| AI | Google Gemini 2.5 Flash (`google-genai` SDK) |
| News | RSS feeds via `feedparser` (TechCrunch, VentureBeat, The Verge, Ars Technica, Wired) |
| YouTube | YouTube Data API v3 |
| Frontend | Vanilla HTML/CSS/JS, Lucide icons, Cormorant Garamond serif |
| Database | SQLite (dev) → PostgreSQL on Railway (prod) |
| Hosting | Railway |
| Static files | WhiteNoise |

---

## 🚀 Local Setup

### Prerequisites
- Python 3.9+
- Git

### Step-by-Step

```bash
# 1. Clone the repo
git clone https://github.com/Nungo/Glintly.git
cd glintly

# 2. Create and activate virtual environment
python -m venv venv
source venv/Scripts/activate   # Windows Git Bash
# source venv/bin/activate      # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
# Edit .env and add your actual API keys

# 5. Run migrations
python manage.py migrate

# 6. Seed the tools directory
python manage.py seed_tools

# 7. Start the server
python manage.py runserver
```

Visit `http://127.0.0.1:8000`

### Environment Variables

| Variable | Description |
|----------|-------------|
| `SECRET_KEY` | Django secret key |
| `GEMINI_API_KEY` | Google Gemini API key (from aistudio.google.com) |
| `YOUTUBE_API_KEY` | YouTube Data API v3 key |
| `CRON_SECRET` | Secret string for triggering news refresh via URL |
| `DEBUG` | Set to `False` in production |

---

## 📁 Project Structure

```
glintly/
├── ai_curator_project/        # Django project settings & URLs
├── curator_app/               # Main application
│   ├── management/
│   │   └── commands/
│   │       └── seed_tools.py  # Seeds 47 curated AI tools
│   ├── migrations/            # Database migrations
│   ├── templates/
│   │   ├── base.html          # Base template with nav, dark theme
│   │   ├── home.html          # Homepage with AI chat + news/tools preview
│   │   └── curator_app/
│   │       ├── news_list.html     # Full news page
│   │       ├── tool_list.html     # Tools directory
│   │       └── tool_detail.html   # Tool detail with AI + YouTube
│   ├── admin.py
│   ├── ai_client.py           # Gemini API integration
│   ├── models.py              # AiTool, NewsItem, NewsSource
│   └── views.py               # All view logic + RSS + YouTube
├── .env.example
├── .gitignore
├── manage.py
├── Procfile                   # For Railway deployment
├── requirements.txt
└── README.md
```

---

## 🌍 Deployment (Railway)

Glintly is deployed on [Railway](https://railway.app).

**Environment variables required in Railway dashboard:**
- `SECRET_KEY`
- `GEMINI_API_KEY`
- `YOUTUBE_API_KEY`
- `CRON_SECRET`
- `DEBUG=False`
- `ALLOWED_HOSTS=your-app.railway.app`

---

## 🗺 Roadmap — What's Next (Phase 2)

These are the planned upgrades that will take Glintly from a strong Phase 1 to a fully scalable platform:

### 🗄 Supabase Database Migration
Replace SQLite with Supabase (PostgreSQL) for persistent, scalable data storage. This enables the ETL pipeline below and makes Glintly pitch-ready as a production architecture.

### ⚙️ Automated ETL News Pipeline
Instead of fetching RSS feeds live on every page load, build a background pipeline:
1. **Extract** — Scrape RSS XML from all 5 sources on a schedule
2. **Transform** — Clean, deduplicate, and structure into JSON
3. **Load** — Store in Supabase, auto-updating hourly via cron
4. **Serve** — Pages query the database instead of live feeds (faster, persistent, searchable)

### 🧠 Per-Article AI Summarization
Use Gemini to generate a one-sentence "why this matters" summary for each article during the ETL step. Makes Glintly feel like an actual intelligent curator rather than a feed aggregator.

### 🔄 Auto-Updating Tools Directory
Pull new tools automatically from Product Hunt API or Futurepedia RSS daily, with AI-generated descriptions. Currently seeded manually with 47 curated tools.

### 📊 Analytics Dashboard
Track which tools and topics users are asking Glintly AI about. Surfaces trending AI tools and topics automatically.

### 🌐 Public API
Expose a REST API so developers can query Glintly's curated tool data and AI news programmatically.

---


## 👩🏾‍💻 Built By

**Nungo Tshidzumba** — Creative Technologist  
UX/UI Design · Full-Stack Development · AI Integration  
