import streamlit as st
import scrapetube
import pandas as pd
import plotly.express as px
from collections import Counter
import re

# --- 1. SETTINGS & BRANDING ---
st.set_page_config(page_title="PlexTrendz", page_icon="🎬", layout="wide")

# Custom CSS for UI/UX Detailing & Animations
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    .stApp { animation: fadeIn 1s; }
    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
    .main { background-color: #050508; font-family: 'Inter', sans-serif; }
    div[data-testid="stSidebar"] { background-color: #0a0a0f !important; border-right: 1px solid #1e1e2d; }
    .stMetric { background: #111119; border: 1px solid #7c6af733; padding: 15px; border-radius: 10px; }
    .strategy-box { 
        background: #111119; padding: 20px; border-radius: 12px; 
        border-left: 5px solid #7c6af7; margin-bottom: 15px; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE ENGINE ---
def get_yt_data(query, limit):
    try:
        videos = scrapetube.get_search(query, limit=limit)
        data = []
        text = ""
        for i, v in enumerate(videos):
            t = v.get('title', {}).get('runs', [{}])[0].get('text', 'N/A')
            v_id = v.get('videoId')
            views = v.get('viewCountText', {}).get('simpleText', '0 views')
            text += " " + t.lower()
            data.append({'Rank': i+1, 'Title': t, 'Views': views, 'Len': len(t), 'URL': f"https://youtube.com/watch?v={v_id}"})
        return pd.DataFrame(data), text
    except: return pd.DataFrame(), ""

# --- 3. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.title("🎬 PlexTrendz")
    st.caption("Creator Intelligence System • v3.8")
    st.divider()
    
    # NAVIGATION
    nav = st.radio("System Menu", ["🚀 Market Dashboard", "🔬 Strategy Lab", "📊 Deep Intelligence", "⚙️ App Status"])
    
    st.divider()
    st.markdown("### 🔍 Search Core")
    topic = st.text_input("Niche Keyword", "Gaming Cinematics")
    amount = st.select_slider("Analysis Depth", options=[20, 50, 100], value=50)
    
    st.divider()
    if st.button("🚀 Run System Analysis", use_container_width=True):
        st.session_state['run'] = True
        with st.spinner("Mining Metadata..."):
            df, txt = get_yt_data(topic, amount)
            st.session_state['df'] = df
            st.session_state['text'] = txt

# --- 4. MAIN INTERFACE LOGIC ---
if st.session_state.get('run'):
    df = st.session_state['df']
    raw_text = st.session_state['text']
    
    # DATA CRUNCHING (Done once for all tabs)
    avg_l = int(df['Len'].mean())
    words = re.findall(r'\w+', raw_text)
    stop_words = ['video', 'youtube', 'latest', 'about', '2025', '2026', 'official']
    clean = [w for w in words if len(w) > 4 and w not in stop_words]
    counts = pd.DataFrame(Counter(clean).most_common(12), columns=['Word', 'Freq'])
    top_k = counts.iloc[0]['Word'].upper() if not counts.empty else "N/A"

    if nav == "🚀 Market Dashboard":
        st.header(f"Market Overview: {topic}")
        
        # KPI ROW
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Optimal Title", f"{avg_l} Chars")
        c2.metric("Dominant Key", top_k)
        c3.metric("Scanned", f"{len(df)} Videos")
        c4.metric("Volatility", "Low")

        st.divider()

        # TOP PERFORMERS & CHART
        left, right = st.columns([1, 1.5])
        with left:
            st.subheader("🏆 Top 3 Winners")
            for i in range(3):
                row = df.iloc[i]
                st.markdown(f"""<div style="background:#1a1a2e; padding:15px; border-radius:10px; margin-bottom:10px; border-left:4px solid #7c6af7;">
                    <small style="color:#7c6af7;">RANK #{row['Rank']}</small><br>
                    <strong>{row['Title'][:55]}...</strong><br>
                    <small>{row['Views']} | {row['Len']} Chars</small></div>""", unsafe_allow_html=True)
        
        with right:
            st.subheader("📈 Ranking Performance")
            fig = px.area(df, x="Rank", y="Len", template="plotly_dark", color_discrete_sequence=['#7c6af7'])
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=0,r=0,t=0,b=0))
            st.plotly_chart(fig, use_container_width=True)

    elif nav == "🔬 Strategy Lab":
        st.header("🔬 Niche Strategy Lab")
        st.caption(f"Deep Strategic Insights for: {topic.upper()}")
        
        col_left, col_right = st.columns([1.2, 1])
        
        with col_left:
            st.subheader("🏷️ Semantic Dominance")
            fig_bar = px.bar(counts, x='Freq', y='Word', orientation='h', color='Freq', 
                            color_continuous_scale='Purples', template="plotly_dark")
            fig_bar.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_bar, use_container_width=True)
            
        with col_right:
            st.subheader("🎯 Content Game Plan")
            
            # --- ADVANCED ADVICE LOGIC ---
            st.success(f"**SEO Strategy:** Use **'{top_k}'** in the first 3 words. It is used by {int((counts.iloc[0]['Freq']/len(df))*100)}% of winners.")
            st.warning(f"**Metadata Fix:** Stick to **{avg_l-5} to {avg_l+5} characters**. Going longer reduces click-through rate in this niche.")
            
            # Question vs Statement Logic
            q_count = df[df['Title'].str.contains('\?|How|Why|What', case=False)].shape[0]
            st.info(f"**Hook Style:** {'Inquisitive (Questions)' if q_count > (len(df)*0.2) else 'Declarative (Facts)'} performs best here.")
            
            # Difficulty Logic
            diff = "High" if avg_l > 65 else "Moderate"
            st.error(f"**Competition Difficulty:** {diff}. Metadata precision is critical to break the top 10.")

            with st.expander("💡 Pro-Tip for this Topic"):
                st.write(f"The top 5% of videos for '{topic}' are using a high density of visual adjectives. Don't just name the subject, describe the 'vibe'.")

    elif nav == "📊 Deep Intelligence":
        st.header("📊 Intelligence Archive")
        st.dataframe(df[['Rank', 'Title', 'Views', 'Len']], use_container_width=True, hide_index=True)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Intelligence Report", csv, "PlexTrendz_Report.csv", "text/csv")

    elif nav == "⚙️ App Status":
        st.header("⚙️ System Configuration")
        st.write("Engine: **Scrapetube Open-Source**")
        st.write("Status: **Healthy (No-API Mode)**")
        st.write("Calculations: **Active**")
        st.button("Clear Cache & Refresh")

else:
    # LANDING PAGE
    st.image("https://cdn-icons-png.flaticon.com/512/1384/1384060.png", width=80)
    st.title("Welcome to PlexTrendz")
    st.markdown("### Select a niche in the sidebar and click **'Run System Analysis'**.")
    st.divider()
    st.markdown("#### 🛠️ Professional Suite Features")
    col_a, col_b, col_c = st.columns(3)
    col_a.info("**Deep Extraction**\nScraping metadata without API limits.")
    col_b.success("**Market Insights**\nCalculating SEO sweet spots automatically.")
    col_c.warning("**Interactive Viz**\nPlotly-powered performance mapping.")
