# 🖼️ Pickposters CrewAI Customer Support Bot

A production-ready multi-agent AI system for automating customer support and order processing in the print business. Built with CrewAI, Streamlit, and Python.


## 🎯 Problem It Solves

- **Customer Communication Gap:** Customers struggle to articulate design requirements clearly
- **Manual Order Processing:** Back-and-forth emails = 3-5 day delays
- **No Design Vocabulary:** Customers don't know professional design terms
- **Lost Orders:** Miscommunication leads to order cancellations

---

## ✨ What It Does

### 3 AI Agents Working Together:

1. **FAQ Agent** - Instant answers on products, pricing, MOQ, turnaround times
2. **Order Processing Agent** - Captures design briefs, generates order summaries
3. **Design Vocabulary Agent** - Teaches 40+ professional design terms across 7 categories

### 3 Interactive Tabs:

- **💬 Chat Support** - Real-time Q&A powered by CrewAI
- **📋 Place Order** - Structured order form with automated email notifications
- **🎨 Design Inspiration** - Design vocabulary guide + Pinterest search

---

## 🏗️ Architecture

```
User Input
    ↓
Streamlit UI (Black Theme, Brand-Aligned)
    ↓
CrewAI Agents (FAQ → Order Processing → Design Vocabulary)
    ↓
Email Automation (Gmail SMTP)
    ↓
Logging System (chat_log.txt, orders.txt)
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- Virtual environment (recommended)
- API Keys (see below)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/pickposters-crewai.git
cd pickposters-crewai

# 2. Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# or
source .venv/bin/activate  # Mac/Linux

# 3. Install dependencies
pip install crewai crewai-tools streamlit python-dotenv langchain langchain-openai

# 4. Create .env file (see Configuration section below)
# Create a file named .env in the root directory

# 5. Run the app
streamlit run app.py
```

Visit: `http://localhost:8501`

---

## ⚙️ Configuration

### Create `.env` file in root directory:

```bash
OPENAI_API_KEY=your_openai_api_key_here
SERPER_API_KEY=your_serper_api_key_here
SMTP_EMAIL=your_gmail_address@gmail.com
SMTP_PASSWORD=your_gmail_app_password_here
```

### Getting API Keys:

#### 1. OpenAI API Key
- Go to https://platform.openai.com/api-keys
- Create new secret key
- Copy and paste into `.env`

#### 2. Serper API Key (Web Search)
- Go to https://serper.dev
- Sign up for free account
- Get API key from dashboard
- Optional - app works without it (graceful fallback)

#### 3. Gmail App Password (Email Automation)
- Enable 2FA on Gmail account
- Go to https://myaccount.google.com/apppasswords
- Select Mail + Windows Computer (or your OS)
- Generate 16-character password
- Copy into `.env` as SMTP_PASSWORD

---

## 📁 Project Structure

```
pickposters-crewai/
├── app.py                 # Main Streamlit application
├── .env                   # API keys (NOT in git - see .gitignore)
├── .env.example           # Template for .env file
├── .gitignore            # Excludes .env, __pycache__, etc.
├── requirements.txt      # Python dependencies
├── chat_log.txt          # Chat history (auto-generated)
├── orders.txt            # Order records (auto-generated)
├── README.md             # This file
└── .venv/                # Virtual environment (excluded from git)
```

---

## 🎨 Features

### Chat Support Tab
- Real-time responses to customer questions
- Knowledge base includes:
  - Posters (₹45–₹499, MOQ: 10)
  - Photo Frames (₹139–₹699)
  - Calendars (₹22–₹499, MOQ: 25)
  - Standees (₹649–₹2,499, MOQ: 1)
  - Certificates (₹35–₹649, MOQ: 10)
- Turnaround times: 2-10 days (Rush: +25%)

### Order Form Tab
- Structured order capture:
  - Customer name & phone
  - Product selection
  - Design theme/description
  - Delivery timeline
  - Budget
  - Additional notes
- Automated order processing with CrewAI
- Professional HTML email notifications
- All orders logged to `orders.txt`

### Design Inspiration Tab
- **Design Vocabulary Guide** (7 categories):
  - 🎨 Color Palettes (Vibrant, Pastel, Monochrome, etc.)
  - 📐 Layout & Composition (Centered, Rule of Thirds, etc.)
  - 🔤 Typography (Serif, Sans-Serif, Handwritten, etc.)
  - 🎭 Style & Aesthetic (Minimalist, Retro, Futuristic, etc.)
  - 💡 Mood & Emotion (Professional, Playful, Luxurious, etc.)
  - 🌟 Design Elements (Icons, Illustrations, Patterns, etc.)
  - 🎯 Industry Specific (Corporate, Tech, Fashion, etc.)

- **Pinterest Search** (Design Reference):
  - Search for design inspiration on Pinterest
  - Quick categories: Posters, Frames, Calendars, Standees
  - Opens Pinterest in new tab (data privacy first)

---

## 🖥️ UI Design

- **Theme:** Pure Black (#0a0a0a) with White Text
- **Accent Color:** Pickposters Brand Orange (#ff6b35)
- **Typography:** Clean, modern sans-serif
- **Layout:** Responsive tabs, mobile-friendly
- **Dark Mode:** Built-in for reduced eye strain

---

## 📊 Data & Logging

### Chat Log (`chat_log.txt`)
Automatically records:
- Timestamp
- User queries
- Bot responses
- For analytics and training

### Orders (`orders.txt`)
Automatically records:
- Customer details (name, phone)
- Order information (product, theme, timeline, budget)
- CrewAI processing summary
- Timestamp

**Use for:** Business analytics, order history, customer insights

---

## 🔧 Customization

### Change Branding
Edit in `app.py`:
```python
PICKPOSTERS_EMAIL = "your_email@gmail.com"
PICKPOSTERS_CONTACT = "Your phone number"
```

### Update Product Info
Edit the `faq_agent` backstory in `app.py`:
```python
backstory="""
PRODUCTS & PRICING:
1. YOUR_PRODUCT: Price info
...
"""
```

### Add Design Categories
Edit `DESIGN_VOCABULARY` dictionary in `app.py`:
```python
DESIGN_VOCABULARY = {
    "Your Category": {
        "Term": "Description",
        ...
    }
}
```

---

## 🚨 Troubleshooting

### Port Already in Use
```bash
# If 8501 is busy, use a different port
streamlit run app.py --server.port 8502
```

### SerperDevTool Not Working
- App gracefully falls back to FAQ-only mode
- Check Serper API key in `.env`
- Web search is optional feature

### Email Not Sending
1. Verify Gmail App Password (16 characters)
2. Check if 2FA is enabled on Gmail
3. Ensure SMTP credentials are correct in `.env`
4. Gmail app password expires after 30 days on some accounts

### CrewAI Agent Errors
- Ensure all agent backstory fields are populated
- Check OpenAI API key validity
- Verify API has enough credits

---

## 📈 Performance

- **Response Time:** <2 seconds per query (with API latency)
- **Concurrent Users:** 5-10 (Streamlit default)
- **Data Persistence:** Chat and orders logged locally
- **Scalability:** Deployable on any Python server (Heroku, Replit, AWS Lambda)

---

## 🔐 Security & Privacy

- ✅ No API keys in repository (`.env` excluded via `.gitignore`)
- ✅ Email credentials never logged
- ✅ Chat history stored locally only
- ✅ No third-party data storage
- ✅ Pinterest search opens direct links (no data scraping)

---

## 📦 Dependencies

```
crewai==0.x.x
crewai-tools==0.x.x
streamlit>=1.28.0
python-dotenv>=1.0.0
langchain>=0.x.x
langchain-openai>=0.x.x
```

See `requirements.txt` for exact versions.

---

## 🎓 Built With

- **CrewAI** - Multi-agent orchestration framework
- **Streamlit** - Web UI framework
- **Python 3.12** - Programming language
- **Gmail SMTP** - Email automation
- **SerperDevTool** - Web search (optional)
- **Pydantic** - Data validation

---

## 📝 Use Cases

- ✅ B2B/D2C print businesses
- ✅ Design service providers
- ✅ Custom merchandise companies
- ✅ Marketing agencies (customer support)
- ✅ E-commerce storefronts

---

## 🚀 Deployment Options

### Local Development
```bash
streamlit run app.py
```

### Streamlit Cloud (FREE)
1. Push repo to GitHub
2. Go to https://streamlit.io/cloud
3. Deploy directly from GitHub repo
4. Set environment variables in Streamlit Cloud dashboard

### Docker
```bash
docker build -t pickposters-bot .
docker run -p 8501:8501 --env-file .env pickposters-bot
```

### Heroku (Paid)
```bash
heroku create your-app-name
heroku config:set OPENAI_API_KEY=your_key
git push heroku main
```

---

## 📞 Support & Contact

**For Pickposters:**
- Email: pickposters.in@gmail.com
- Phone: +91 78450 06426
- Website: pickposters.co.in

**For Technical Issues:**
- Open an issue on GitHub
- Check existing issues for solutions

---

## 🎓 Learning Resources

- **CrewAI Docs:** https://docs.crewai.com
- **Streamlit Docs:** https://docs.streamlit.io
- **OpenAI API:** https://platform.openai.com/docs
- **Python Guide:** https://docs.python.org/3

---

## 📜 License

MIT License - Feel free to use, modify, and distribute

---

## ✨ Future Enhancements

- [ ] Multi-language support
- [ ] Mobile app (React Native)
- [ ] Payment integration (Razorpay, Stripe)
- [ ] Order tracking dashboard
- [ ] Customer analytics dashboard
- [ ] WhatsApp bot integration
- [ ] Design mockup generator
- [ ] PDF quote generator

---

## 🏆 Built For

**Social Eagle GenAI Architect Buildathon** (AI Batch 11)
- Real-world AI implementation
- CrewAI multi-agent system
- Production-ready deployment
- Solves actual business pain point

---

## 👨‍💻 Author

**Sudhan (Hariharasudhan M M)**
- Finance Analyst & AI Generalist
- Built for Pickposters Print Business
- Coimbatore, India

---

## 📅 Changelog

### Version 1.0 (Sep 23, 2026)
- ✅ Multi-agent CrewAI system
- ✅ Streamlit UI with black theme
- ✅ Email automation
- ✅ Design vocabulary guide
- ✅ Pinterest integration
- ✅ Order logging system
- ✅ Production deployment

---

## 🙏 Acknowledgments

- **CrewAI** for agent orchestration framework
- **Streamlit** for beautiful UI
- **OpenAI** for language models
- **Social Eagle** for Buildathon opportunity
- **Pickposters** for real-world use case

---

## 💬 Questions?

Feel free to open an issue or reach out. Happy to help! 🚀

---

**⭐ If this helped you, please star the repo! ⭐**

## Features
- FAQ Agent: Instant product Q&A
- Order Processing Agent: Captures design briefs + sends emails
- Design Vocabulary Agent: Teaches professional design language
- Pinterest integration for design inspiration

## Setup

1. Clone repo
2. Create .env with your API keys (copy from .env.example)
3. Install: pip install -r requirements.txt
4. Run: streamlit run app.py

## Tech Stack
- CrewAI
- Streamlit
- Python 3.12
- OpenAI API
- Gmail SMTP

## Author
Sudhan | Social Eagle Buildathon AI Batch 11

GitHub: https://github.com/Sumamsudhan7303/Pickposters_CustomerBot
