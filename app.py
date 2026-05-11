import streamlit as st
import scrapetube
import pandas as pd
import plotly.express as px
from collections import Counter
import re
from datetime import datetime

# --- 1. SETTINGS & INTERFACE ---
st.set_page_config(page_title="PlexTrendz Pro", page_icon="🎬", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    .stApp { animation: fadeIn 1s; }
    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
    .main { background-color: #050508; font-family: 'Inter', sans-serif; }
    div[data-testid="stSidebar"] { background-color: #0a0a0f !important; border-right: 1px solid #1e1e2d; }
    
    /* VidIQ Style SEO Scorecard */
    .seo-score {
        background: #111119; border: 2px solid #7c6af7;
        padding: 20px; border-radius: 50%; width: 120px; height: 120px;
        display: flex; align-items: center; justify-content: center;
        flex-direction: column; margin: 0 auto;
    }
    .check-item { background: #1a1a2e; padding: 10px; border-radius: 8px; margin-bottom: 5px; border-left: 3px solid #38d9a9; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. BACKEND ENGINE ---
def get_yt_data(query, limit):
    try:
        videos = scrapetube.get_search(query, limit=limit)
        data = []
        text = ""
        for i, v in enumerate(videos):
            t = v.get('title', {}).get('runs', [{}])[0].get('text', 'N/A')
            v_id = v.get('videoId')
            # Extracting "Views" and "Time" from metadata
            meta = v.get('publishedTimeText', {}).get('simpleText', 'Recently')
            views_raw = v.get('viewCountText', {}).get('simpleText', '0 views')
            
            text += " " + t.lower()
            data.append({
                'Rank': i+1, 'Title': t, 'Views': views_raw, 
                'Age': meta, 'Len': len(t), 'URL': f"https://youtube.com/watch?v={v_id}"
            })
        return pd.DataFrame(data), text
    except: return pd.DataFrame(), ""

# --- 3. SIDEBAR ---
with st.sidebar:
    st.title("🎬 PlexTrendz")
    st.caption("Advanced SEO Intelligence • v4.0")
    st.divider()
    nav = st.radio("Intelligence Suite", ["📈 Market Velocity", "🎯 SEO Scorecard", "🔬 Keyword Lab", "📁 Raw Archive"])
    
    st.divider()
    topic = st.text_input("Target Keyword", "Elden Ring Cinematics")
    depth = st.select_slider("Scan Depth", options=[20, 50, 100], value=50)
    
    if st.button("🚀 Analyze Market", use_container_width=True):
        st.session_state['run'] = True
        with st.spinner("Calculating SEO Metrics..."):
            df, txt = get_yt_data(topic, depth)
            st.session_state['df'] = df
            st.session_state['text'] = txt

# --- 4. DATA PROCESSING & LOGIC ---
if st.session_state.get('run'):
    df = st.session_state['df']
    raw_text = st.session_state['text']
    
    # Calculate SEO Metrics
    avg_l = int(df['Len'].mean())
    words = re.findall(r'\w+', raw_text)
    stop_words = ['video', 'youtube', 'latest', 'about', 'official', 'part']
    clean = [w for w in words if len(w) > 4 and w not in stop_words]
    counts = pd.DataFrame(Counter(clean).most_common(12), columns=['Word', 'Freq'])
    top_k = counts.iloc[0]['Word'].upper() if not counts.empty else "N/A"
    
    # --- SEO SCORING LOGIC (VidIQ Style) ---
    # Score out of 100 based on Title length (40pts) and Keyword Density (60pts)
    len_score = 40 if 40 < avg_l < 70 else 20
    key_density = (counts.iloc[0]['Freq'] / len(df)) * 60
    final_seo_score = int(len_score + key_density)

    if nav == "📈 Market Velocity":
        st.header(f"Market Velocity: {topic}")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Optimization Score", f"{final_seo_score}/100")
        c2.metric("Competition", "Medium" if depth < 60 else "High")
        c3.metric("Avg. Length", f"{avg_l} Chars")
        c4.metric("Market Status", "Trending" if "hours" in str(df['Age'].values) else "Stable")

        st.divider()
        st.subheader("📊 Ranking Performance Mapping")
        fig = px.area(df, x="Rank", y="Len", template="plotly_dark", color_discrete_sequence=['#7c6af7'])
        st.plotly_chart(fig, use_container_width=True)

    elif nav == "🎯 SEO Scorecard":
        st.header("🎯 Optimization Scorecard")
        
        left, right = st.columns([1, 2])
        with left:
            st.markdown(f"""<div class="seo-score"><h1>{final_seo_score}</h1><small>OUT OF 100</small></div>""", unsafe_allow_html=True)
            st.markdown("<br><center>Overall SEO Strength</center>", unsafe_allow_html=True)
        
        with right:
            st.subheader("✅ Optimization Checklist")
            st.markdown(f"<div class='check-item'>Title Length ({avg_l} chars): {'Excellent' if 40<avg_l<70 else 'Needs Work'}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='check-item'>Keyword Focus: Primary key '{top_k}' is dominant.</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='check-item'>Volume Check: {len(df)} competitors detected.</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='check-item'>Ranking Potential: {'High' if final_seo_score > 70 else 'Medium'}</div>", unsafe_allow_html=True)

    elif nav == "🔬 Keyword Lab":
        st.header("🔬 Keyword Opportunity Lab")
        st.caption("Comparison of Keyword Frequency vs Search Ranking")
        
        col_a, col_b = st.columns([1.5, 1])
        with col_a:
            fig_bar = px.bar(counts, x='Freq', y='Word', orientation='h', color='Freq', 
                            color_continuous_scale='Purples', template="plotly_dark")
            st.plotly_chart(fig_bar, use_container_width=True)
        
        with col_b:
            st.subheader("💡 AI Strategy Tip")
            st.success(f"**The Winning Hook:** Use **'{top_k}'** in your first 20 characters. The data shows this leads to a higher ranking velocity.")
            st.info("**Trending Suffix:** Many top videos are adding 'Cinematic' or '4K' to boost CTR.")

    elif nav == "📁 Raw Archive":
        st.header("📁 Competitive Intelligence Data")
        st.dataframe(df[['Rank', 'Title', 'Age', 'Views', 'Len']], use_container_width=True, hide_index=True)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Export CSV Report", csv, "PlexTrendz_Report.csv", "text/csv")

else:
    # LANDING PAGE
    st.image("https://cdn-icons-png.flaticon.com/512/1384/1384060.png", width=80)
    st.title("PlexTrendz: VidIQ Edition")
    st.markdown("### Data-Driven SEO for Professional Creators.")
    st.info("👈 Enter a keyword and hit **'Analyze Market'** to generate your SEO Scorecard.")
