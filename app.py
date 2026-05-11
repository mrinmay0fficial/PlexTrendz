import streamlit as st
import scrapetube
import pandas as pd
import plotly.express as px
from collections import Counter
import re

# --- 1. SETTINGS & BRANDING ---
st.set_page_config(page_title="PlexTrendz", page_icon="🎬", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    .stApp { animation: fadeIn 1s; }
    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
    .main { background-color: #050508; font-family: 'Inter', sans-serif; }
    div[data-testid="stSidebar"] { background-color: #0a0a0f !important; border-right: 1px solid #1e1e2d; }
    .stMetric { background: #111119; border: 1px solid #7c6af733; padding: 15px; border-radius: 10px; }
    .seo-score-circle {
        background: #111119; border: 3px solid #7c6af7;
        padding: 20px; border-radius: 50%; width: 130px; height: 130px;
        display: flex; align-items: center; justify-content: center;
        flex-direction: column; margin: 0 auto; box-shadow: 0 0 20px rgba(124,106,247,0.2);
    }
    .check-item { background: #161625; padding: 12px; border-radius: 8px; margin-bottom: 8px; border-left: 4px solid #38d9a9; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. BACKEND ENGINE (WITH SAFETY SHIELD) ---
def get_yt_data(query, limit):
    # We define columns first so they ALWAYS exist
    cols = ['Rank', 'Title', 'Views', 'Age', 'Len', 'URL']
    try:
        videos = list(scrapetube.get_search(query, limit=limit))
        if not videos:
            return pd.DataFrame(columns=cols), ""
        
        data = []
        text = ""
        for i, v in enumerate(videos):
            # Safe extraction using nested .get()
            t = v.get('title', {}).get('runs', [{}])[0].get('text', 'N/A')
            v_id = v.get('videoId', 'Unknown')
            views = v.get('viewCountText', {}).get('simpleText', '0 views')
            age = v.get('publishedTimeText', {}).get('simpleText', 'Recent')
            
            text += " " + t.lower()
            data.append({
                'Rank': i+1, 'Title': t, 'Views': views, 
                'Age': age, 'Len': len(t), 'URL': f"https://youtube.com/watch?v={v_id}"
            })
        return pd.DataFrame(data, columns=cols), text
    except Exception as e:
        return pd.DataFrame(columns=cols), ""

# --- 3. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.title("🎬 PlexTrendz")
    st.caption("Advanced SEO Intelligence • v4.1")
    st.divider()
    nav = st.radio("Intelligence Suite", ["🚀 Market Overview", "🎯 SEO Scorecard", "🔬 Keyword Lab", "📁 Data Archive"])
    st.divider()
    topic = st.text_input("Niche Keyword", "Gaming Cinematics")
    amount = st.select_slider("Analysis Depth", options=[20, 50, 100], value=50)
    st.divider()
    if st.button("🚀 Execute Analysis", use_container_width=True):
        st.session_state['run'] = True
        with st.spinner("Calculating SEO Metrics..."):
            df, txt = get_yt_data(topic, amount)
            st.session_state['df'] = df
            st.session_state['text'] = txt

# --- 4. MAIN INTERFACE ---
if st.session_state.get('run'):
    df = st.session_state['df']
    raw_text = st.session_state['text']

    if df.empty:
        st.error("No results found. YouTube might be blocking the request or the keyword is too rare. Try another search!")
    else:
        # --- CALCULATIONS ---
        avg_l = int(df['Len'].mean())
        words = re.findall(r'\w+', raw_text)
        stop_words = ['video', 'youtube', 'latest', 'about', 'official', 'part', '2025', '2026']
        clean = [w for w in words if len(w) > 4 and w not in stop_words]
        counts = pd.DataFrame(Counter(clean).most_common(12), columns=['Word', 'Freq'])
        top_k = counts.iloc[0]['Word'].upper() if not counts.empty else "N/A"
        
        # SEO Scoring
        len_score = 40 if 40 <= avg_l <= 70 else 15
        key_density = (counts.iloc[0]['Freq'] / len(df)) * 60 if not counts.empty else 0
        final_score = int(len_score + key_density)

        if nav == "🚀 Market Overview":
            st.header(f"Market Velocity: {topic}")
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("SEO Score", f"{final_score}/100")
            c2.metric("Hot Keyword", top_k)
            c3.metric("Scanned", len(df))
            # Safe Age Check
            is_trending = any("hour" in str(val).lower() for val in df['Age'].values)
            c4.metric("Market Status", "Trending 🔥" if is_trending else "Stable")

            st.divider()
            l_col, r_col = st.columns([1, 1.5])
            with l_col:
                st.subheader("🏆 Ranking Leaders")
                for i in range(min(3, len(df))):
                    row = df.iloc[i]
                    st.markdown(f"""<div style="background:#1a1a2e; padding:15px; border-radius:10px; margin-bottom:10px; border-left:4px solid #7c6af7;">
                        <small style="color:#7c6af7;">RANK #{row['Rank']}</small><br>
                        <strong>{row['Title'][:55]}...</strong><br>
                        <small>{row['Views']} | {row['Age']}</small></div>""", unsafe_allow_html=True)
            with r_col:
                st.subheader("📊 Performance Landscape")
                fig = px.area(df, x="Rank", y="Len", template="plotly_dark", color_discrete_sequence=['#7c6af7'])
                fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=0,r=0,t=0,b=0))
                st.plotly_chart(fig, use_container_width=True)

        elif nav == "🎯 SEO Scorecard":
            st.header("🎯 Optimization Scorecard")
            l, r = st.columns([1, 2])
            with l:
                st.markdown(f"""<div class="seo-score-circle"><h1>{final_score}</h1><small>SCORE</small></div>""", unsafe_allow_html=True)
            with r:
                st.subheader("✅ Optimization Checklist")
                st.markdown(f"<div class='check-item'>Title Length ({avg_l} chars): {'Perfect' if 40<avg_l<70 else 'Sub-optimal'}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='check-item'>Keyword Focus: '{top_k}' is the strongest trend.</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='check-item'>Niche Saturation: {len(df)} competitors detected.</div>", unsafe_allow_html=True)

        elif nav == "🔬 Keyword Lab":
            st.header("🔬 Keyword Opportunity Lab")
            col_a, col_b = st.columns([1.5, 1])
            with col_a:
                fig_bar = px.bar(counts, x='Freq', y='Word', orientation='h', color='Freq', color_continuous_scale='Purples', template="plotly_dark")
                st.plotly_chart(fig_bar, use_container_width=True)
            with col_b:
                st.subheader("💡 Strategic Advice")
                st.success(f"**The 'Power' Word:** Use **'{top_k}'** early in your title.")
                st.info(f"The average winner uses **{avg_l} characters**.")

        elif nav == "📁 Data Archive":
            st.header("📁 Competitive Data")
            st.dataframe(df[['Rank', 'Title', 'Views', 'Age', 'Len']], use_container_width=True, hide_index=True)
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Export CSV", csv, "PlexTrendz_Report.csv", "text/csv")
else:
    st.image("https://cdn-icons-png.flaticon.com/512/1384/1384060.png", width=80)
    st.title("Welcome to PlexTrendz")
    st.info("👈 Enter a keyword and hit **'Execute Analysis'** to begin.")
