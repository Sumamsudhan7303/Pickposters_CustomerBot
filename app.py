import os
import smtplib
import streamlit as st
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from crewai_tools import SerperDevTool

load_dotenv()

st.set_page_config(page_title="Pickposters CrewAI", page_icon="🖼️", layout="wide", initial_sidebar_state="expanded")

# ============================================================================
# DARK THEME & STYLING
# ============================================================================

st.markdown("""
<style>
    * {
        margin: 0;
        padding: 0;
    }
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #0a0a0a !important;
        color: #ffffff !important;
    }
    
    [data-testid="stHeader"] {
        background-color: #000000 !important;
    }
    
    [data-testid="stSidebar"] {
        background-color: #1a1a1a !important;
    }
    
    [data-testid="stTabs"] {
        background-color: #0a0a0a !important;
    }
    
    [data-testid="stTabBar"] button {
        color: #ffffff !important;
        border-color: #333333 !important;
    }
    
    [data-testid="stTabBar"] button[aria-selected="true"] {
        color: #ffffff !important;
        border-bottom: 2px solid #ff6b35 !important;
    }
    
    .stChatMessage {
        background-color: #1a1a1a !important;
        border-radius: 12px !important;
        padding: 12px !important;
    }
    
    .stChatMessage.user {
        background-color: #2a2a2a !important;
    }
    
    .stTextInput > div > div > input {
        background-color: #1a1a1a !important;
        color: #ffffff !important;
        border: 1px solid #333333 !important;
        border-radius: 8px !important;
    }
    
    .stButton > button {
        background-color: #ff6b35 !important;
        color: #ffffff !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        border: none !important;
        padding: 10px 20px !important;
    }
    
    .stButton > button:hover {
        background-color: #e55a24 !important;
    }
    
    .stForm {
        background-color: #1a1a1a !important;
        border: 1px solid #333333 !important;
        border-radius: 12px !important;
        padding: 20px !important;
    }
    
    .stSelectbox > div > div {
        background-color: #1a1a1a !important;
        color: #ffffff !important;
        border: 1px solid #333333 !important;
    }
    
    .stTextArea > div > div > textarea {
        background-color: #1a1a1a !important;
        color: #ffffff !important;
        border: 1px solid #333333 !important;
    }
    
    .stSuccess {
        background-color: #1a3a1a !important;
        color: #90ee90 !important;
        border-left: 4px solid #00b300 !important;
    }
    
    .stWarning {
        background-color: #3a3a1a !important;
        color: #ffff99 !important;
        border-left: 4px solid #ffaa00 !important;
    }
    
    .stInfo {
        background-color: #1a2a3a !important;
        color: #87ceeb !important;
        border-left: 4px solid #0099ff !important;
    }
    
    .stError {
        background-color: #3a1a1a !important;
        color: #ff6b6b !important;
        border-left: 4px solid #ff0000 !important;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
    }
    
    .logo-container {
        text-align: center;
        padding: 20px;
        margin-bottom: 20px;
        border-bottom: 2px solid #ff6b35;
    }
    
    .logo-text {
        font-size: 32px;
        font-weight: bold;
        color: #ffffff;
        letter-spacing: 2px;
        margin: 10px 0;
    }
    
    .logo-tagline {
        font-size: 12px;
        color: #ff6b35;
        font-style: italic;
    }
    
    .sidebar-section {
        background-color: #1a1a1a;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        border-left: 4px solid #ff6b35;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# CONFIGURATION
# ============================================================================

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
PICKPOSTERS_EMAIL = "pickposters.in@gmail.com"

# ============================================================================
# DESIGN VOCABULARY DATABASE
# ============================================================================

DESIGN_VOCABULARY = {
    "🎨 Color Palettes": {
        "Vibrant": "Bright, bold, saturated colors - high energy and impact",
        "Pastel": "Soft, muted tones - gentle, approachable, modern",
        "Monochrome": "Single color family - sophisticated, clean, timeless",
        "Gradient": "Color transitions - smooth, dynamic, contemporary",
        "Minimalist": "2-3 colors max - focused, premium, elegant",
        "Earth Tones": "Browns, beiges, greens - natural, warm, organic",
        "High Contrast": "Bold black/white or dark/light - dramatic, impactful"
    },
    "📐 Layout & Composition": {
        "Centered": "Subject in middle - formal, symmetrical, balanced",
        "Rule of Thirds": "Subject off-center - dynamic, engaging, professional",
        "Asymmetrical": "Unbalanced layout - creative, modern, unconventional",
        "Grid Based": "Organized squares/rectangles - structured, systematic",
        "Overlapping": "Elements layered - depth, complexity, richness",
        "Diagonal": "Angled elements - movement, energy, excitement",
        "Whitespace": "Lots of empty space - breathing room, luxury, clarity"
    },
    "🔤 Typography": {
        "Serif": "Classic, elegant, traditional fonts",
        "Sans-Serif": "Modern, clean, contemporary fonts",
        "Handwritten": "Casual, personal, artistic feel",
        "Bold Headlines": "Large, eye-catching, commanding presence",
        "Script": "Flowing, decorative, premium aesthetic",
        "Minimalist Text": "Limited words, maximum impact"
    },
    "🎭 Style & Aesthetic": {
        "Minimalist": "Less is more - clean, simple, sophisticated",
        "Maximalist": "Rich, detailed, ornate, layered elements",
        "Retro/Vintage": "80s/90s vibes - nostalgic, trendy, playful",
        "Futuristic": "Modern tech look - sleek, innovative, forward-thinking",
        "Handmade": "Organic, imperfect, artisanal, authentic",
        "Abstract": "Geometric shapes, non-representational art"
    },
    "💡 Mood & Emotion": {
        "Professional": "Corporate, serious, business-focused",
        "Playful": "Fun, lighthearted, energetic, youthful",
        "Luxurious": "Premium, sophisticated, high-end, elegant",
        "Casual": "Relaxed, friendly, approachable, informal",
        "Dramatic": "Bold, intense, powerful, impactful",
        "Serene": "Calm, peaceful, meditative, soothing"
    }
}

# ============================================================================
# PINTEREST SEARCH FUNCTION
# ============================================================================

def search_pinterest_designs(query):
    search_url = f"https://www.pinterest.com/search/pins/?q={query.replace(' ', '%20')}"
    st.markdown(f"""
    <div style='background-color: #1a1a1a; padding: 15px; border-radius: 8px; border-left: 4px solid #ff6b35; margin: 15px 0;'>
        <p style='color: #ff6b35; margin: 0; font-weight: bold;'>🔗 Pinterest Search</p>
        <p style='margin: 10px 0;'><a href='{search_url}' target='_blank' style='color: #ff6b35; text-decoration: none; font-weight: bold;'>
            ➜ Open: "{query}"
        </a></p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# HEADER
# ============================================================================

st.markdown("""
<div class="logo-container">
    <div style='font-size: 48px; margin-bottom: 10px;'>🖼️</div>
    <div class="logo-text">PICKPOSTERS</div>
    <div class="logo-tagline">Frame Your World, Poster Your Passion!</div>
    <div style='font-size: 11px; color: #666; margin-top: 8px;'>CrewAI Multi-Agent Customer Support System</div>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# AGENTS
# ============================================================================

faq_agent = Agent(
    role="Pickposters Support Specialist",
    goal="Answer questions about Pickposters products, pricing, MOQ, and turnaround times",
    backstory="""You are a customer service expert for Pickposters, a B2B/D2C custom print business.

PRODUCTS & PRICING:
1. POSTERS: ₹45–₹499/unit (MOQ: 10)
2. PHOTO FRAMES: ₹139–₹699
3. CALENDARS: ₹22–₹499/unit (MOQ: 25)
4. STANDEES: ₹649–₹2,499 (MOQ: 1)
5. CERTIFICATES: ₹35–₹649/unit (MOQ: 10)

TURNAROUND: 2–10 working days | RUSH: +25%
PAYMENT: 50% advance | SHIPPING: Free >₹5,000
CONTACT: pickposters.in@gmail.com | +91 78450 06426""",
    verbose=False,
    allow_delegation=False
)

try:
    search_agent = Agent(
        role="Web Research Specialist",
        goal="Find additional information from the web",
        backstory="You are an expert web researcher.",
        tools=[SerperDevTool()],
        verbose=False,
        allow_delegation=False
    )
    HAS_SEARCH = True
except:
    search_agent = None
    HAS_SEARCH = False

order_agent = Agent(
    role="Order Processing Specialist",
    goal="Capture and process customer orders",
    backstory="You process customer order details and prepare summaries for Pickposters.",
    verbose=False,
    allow_delegation=False
)

# ============================================================================
# TABS
# ============================================================================

tab1, tab2, tab3 = st.tabs(["💬 Chat Support", "📋 Place Order", "🎨 Design Inspiration"])

# ============================================================================
# TAB 1: CHAT SUPPORT
# ============================================================================

with tab1:
    st.markdown("<h3 style='color: #ff6b35; text-align: center;'>Ask About Our Products</h3>", unsafe_allow_html=True)
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            with st.chat_message("user", avatar="👤"):
                st.markdown(msg["content"])
        else:
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(msg["content"])
    
    user_query = st.chat_input("Ask about products, pricing, MOQ, turnaround...")
    
    if user_query:
        st.session_state.chat_history.append({"role": "user", "content": user_query})
        with st.chat_message("user", avatar="👤"):
            st.markdown(user_query)
        
        with st.spinner("🤖 Analyzing..."):
            try:
                task1 = Task(
                    description=f"Answer: {user_query}",
                    agent=faq_agent,
                    expected_output="Detailed response with product info"
                )
                
                if HAS_SEARCH:
                    task2 = Task(
                        description=f"Search for: {user_query}",
                        agent=search_agent,
                        expected_output="Web results if relevant"
                    )
                    crew = Crew(agents=[faq_agent, search_agent], tasks=[task1, task2], verbose=False)
                else:
                    crew = Crew(agents=[faq_agent], tasks=[task1], verbose=False)
                
                result = crew.kickoff()
                response = str(result) if result else "Please contact pickposters.in@gmail.com"
                
                st.session_state.chat_history.append({"role": "assistant", "content": response})
                with st.chat_message("assistant", avatar="🤖"):
                    st.markdown(response)
                
                with open("chat_log.txt", "a", encoding="utf-8") as f:
                    f.write(f"\n{'='*80}\n{datetime.now()}\nUser: {user_query}\nBot: {response}\n")
                
            except Exception as e:
                st.error(f"Error: {str(e)[:200]}")

# ============================================================================
# TAB 2: ORDER FORM
# ============================================================================

with tab2:
    st.markdown("<h3 style='color: #ff6b35; text-align: center;'>📋 Place Your Order</h3>", unsafe_allow_html=True)
    
    with st.form("order_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("👤 Full Name *", placeholder="Your name")
            phone = st.text_input("📱 Phone *", placeholder="+91 XXXXX XXXXX")
            product = st.selectbox("🎨 Product *", 
                ["Select", "Posters", "Photo Frames", "Calendars", "Standees", "Certificates"])
        
        with col2:
            theme = st.text_input("🎭 Design Theme *", placeholder="e.g., Corporate branding")
            timeline = st.selectbox("⏱️ Timeline *",
                ["Select", "Urgent (1-2 days +25%)", "Standard (5-7 days)", "Flexible (10 days)"])
            budget = st.text_input("💰 Budget *", placeholder="e.g., ₹5,000 - ₹10,000")
        
        notes = st.text_area("📝 Additional Notes", placeholder="Special requirements...", height=80)
        submitted = st.form_submit_button("✉️ Submit Order", use_container_width=True)
    
    if submitted:
        if not all([name, phone, product != "Select", theme, timeline != "Select", budget]):
            st.error("❌ Fill all required fields (*)")
        else:
            with st.spinner("Processing..."):
                try:
                    order_details = f"""Name: {name}
Phone: {phone}
Product: {product}
Theme: {theme}
Timeline: {timeline}
Budget: {budget}
Notes: {notes if notes else 'None'}
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""
                    
                    task = Task(
                        description=f"Process order: {order_details}",
                        agent=order_agent,
                        expected_output="Order summary"
                    )
                    
                    crew = Crew(agents=[order_agent], tasks=[task], verbose=False)
                    order_result = crew.kickoff()
                    
                    with open("orders.txt", "a", encoding="utf-8") as f:
                        f.write(f"\n{'='*80}\n{order_details}\nSummary: {str(order_result)}\n")
                    
                    email_sent = False
                    if SMTP_EMAIL and SMTP_PASSWORD:
                        try:
                            msg = MIMEMultipart("alternative")
                            msg['From'] = SMTP_EMAIL
                            msg['To'] = PICKPOSTERS_EMAIL
                            msg['Subject'] = f"🎉 New Order: {product} from {name}"
                            
                            html = f"""<html><body style="background:#0a0a0a;color:#fff;font-family:Arial"><table style="max-width:600px;margin:0 auto;background:#1a1a1a;border-radius:12px;border:1px solid #333"><tr style="background:#000;border-bottom:2px solid #ff6b35"><td style="padding:20px;text-align:center"><h1 style="color:#fff;margin:0">🖼️ PICKPOSTERS</h1></td></tr><tr><td style="padding:30px"><h2 style="color:#ff6b35">📋 New Order</h2><table style="width:100%"><tr><td style="padding:8px;color:#ff6b35;font-weight:bold">Name:</td><td style="padding:8px;color:#fff">{name}</td></tr><tr><td style="padding:8px;color:#ff6b35;font-weight:bold">Phone:</td><td style="padding:8px;color:#fff">{phone}</td></tr><tr><td style="padding:8px;color:#ff6b35;font-weight:bold">Product:</td><td style="padding:8px;color:#fff">{product}</td></tr><tr><td style="padding:8px;color:#ff6b35;font-weight:bold">Theme:</td><td style="padding:8px;color:#fff">{theme}</td></tr><tr><td style="padding:8px;color:#ff6b35;font-weight:bold">Timeline:</td><td style="padding:8px;color:#fff">{timeline}</td></tr><tr><td style="padding:8px;color:#ff6b35;font-weight:bold">Budget:</td><td style="padding:8px;color:#fff">{budget}</td></tr></table></td></tr><tr style="background:#000;border-top:2px solid #ff6b35"><td style="padding:20px;text-align:center"><p style="color:#999;margin:5px 0">pickposters.in@gmail.com | +91 78450 06426</p></td></tr></table></body></html>"""
                            
                            msg.attach(MIMEText(html, "html"))
                            server = smtplib.SMTP('smtp.gmail.com', 587)
                            server.starttls()
                            server.login(SMTP_EMAIL, SMTP_PASSWORD)
                            server.send_message(msg)
                            server.quit()
                            email_sent = True
                        except:
                            pass
                    
                    st.success("✅ Order submitted!")
                    if email_sent:
                        st.info(f"📧 Email sent to: {PICKPOSTERS_EMAIL}")
                    
                except Exception as e:
                    st.error(f"Error: {str(e)[:200]}")

# ============================================================================
# TAB 3: DESIGN INSPIRATION
# ============================================================================

with tab3:
    st.markdown("<h3 style='color: #ff6b35; text-align: center;'>🎨 Design Vocabulary & Pinterest</h3>", unsafe_allow_html=True)
    
    tab3a, tab3b = st.tabs(["📚 Vocabulary", "🔍 Pinterest"])
    
    with tab3a:
        st.markdown("<p style='text-align:center;color:#999'>Learn design terminology</p>", unsafe_allow_html=True)
        
        for category, vocab in DESIGN_VOCABULARY.items():
            st.markdown(f"<p style='color:#ff6b35;font-weight:bold'>{category}</p>", unsafe_allow_html=True)
            cols = st.columns(2)
            items = list(vocab.items())
            for idx, (term, desc) in enumerate(items):
                with cols[idx % 2]:
                    st.markdown(f"<div style='background:#2a2a2a;padding:12px;border-radius:6px;border-left:3px solid #ff6b35'><p style='color:#ff6b35;margin:0;font-weight:bold'>{term}</p><p style='color:#999;margin:5px 0;font-size:11px'>{desc}</p></div>", unsafe_allow_html=True)
    
    with tab3b:
        col1, col2 = st.columns([3, 1])
        
        with col1:
            query = st.text_input("🔍 Search", placeholder="e.g., Modern poster design")
        
        with col2:
            if st.button("Search", use_container_width=True):
                if query.strip():
                    search_pinterest_designs(query)
        
        st.markdown("<h4 style='color:#ff6b35;margin-top:30px'>Quick Categories</h4>", unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            if st.button("📌 Posters", use_container_width=True):
                search_pinterest_designs("modern poster designs")
        with c2:
            if st.button("🖼️ Frames", use_container_width=True):
                search_pinterest_designs("photo frame ideas")
        with c3:
            if st.button("📅 Calendar", use_container_width=True):
                search_pinterest_designs("calendar design")
        with c4:
            if st.button("🎪 Standees", use_container_width=True):
                search_pinterest_designs("standee display")

# ============================================================================
# SIDEBAR
# ============================================================================

with st.sidebar:
    st.markdown("<div class='sidebar-section'><h3 style='margin-top:0;color:#ff6b35'>📞 Contact</h3><p style='margin:0;color:#fff;font-size:12px'><b>Email:</b> pickposters.in@gmail.com<br><b>Phone:</b> +91 78450 06426<br><b>Website:</b> pickposters.co.in</p></div>", unsafe_allow_html=True)
    
    st.markdown("<div class='sidebar-section'><h3 style='margin-top:0;color:#ff6b35'>💰 Pricing</h3><p style='margin:0;font-size:11px;color:#fff'><b>Posters:</b> ₹45–₹499<br><b>Frames:</b> ₹139–₹699<br><b>Calendars:</b> ₹22–₹499<br><b>Standees:</b> ₹649–₹2,499</p></div>", unsafe_allow_html=True)
    
    st.markdown("<div class='sidebar-section'><h3 style='margin-top:0;color:#ff6b35'>⏱️ Turnaround</h3><p style='margin:0;font-size:11px;color:#fff'><b>Standard:</b> 2-10 days<br><b>Rush:</b> 1-2 days (+25%)</p></div>", unsafe_allow_html=True)
    
    st.markdown(f"<div class='sidebar-section'><h3 style='margin-top:0;color:#ff6b35'>⚙️ Status</h3><p style='margin:0;font-size:11px'><span style='color:#90ee90'>✅ CrewAI</span><br><span style='color:#90ee90'>✅ Design Vocab</span><br><span style='color:#90ee90'>✅ Pinterest</span><br><span style='color:{'#90ee90' if (SMTP_EMAIL and SMTP_PASSWORD) else '#ffaa00'}'>{'✅' if (SMTP_EMAIL and SMTP_PASSWORD) else '⚠️'} Email</span></p></div>", unsafe_allow_html=True)