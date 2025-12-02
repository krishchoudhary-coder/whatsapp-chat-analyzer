import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# 🔥 EPIC CUSTOM UI SETUP
st.set_page_config(page_title="WhatsApp Analyzer Pro", layout="wide", page_icon="📱", initial_sidebar_state="expanded")
plt.style.use('dark_background')

# CUSTOM CSS
st.markdown("""
<style>
    .main {background: linear-gradient(135deg, #0C0E1A 0%, #1A1D2E 100%);}
    .stApp {background: linear-gradient(135deg, #0C0E1A 0%, #1A1D2E 100%);}
    .sidebar .sidebar-content {background: linear-gradient(135deg, #16213E 0%, #0F3460 100%);}
    .metric-card {background: linear-gradient(45deg, #FF6B6B, #4ECDC4, #45B7D1); 
                  padding: 1.5rem; border-radius: 20px; margin: 0.5rem 0; box-shadow: 0 10px 30px rgba(0,0,0,0.3);}
    h1 {color: #00D4AA; font-size: 3.5rem; font-weight: 800; text-shadow: 0 0 20px rgba(0,212,170,0.5);}
    .stButton > button {background: linear-gradient(45deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 25px; border: none; padding: 0.8rem 2rem; font-weight: bold;}
</style>
""", unsafe_allow_html=True)

# HEADER
st.markdown("""
# 📱 **WhatsApp Chat Analyzer Pro** 
### *Advanced Analytics • Beautiful Visuals • Deep Insights* ✨
""")

# SIDEBAR
with st.sidebar:
    st.markdown("### 📤 **Upload Chat File**")
    uploaded_file = st.file_uploader("Choose WhatsApp TXT", type="txt")
    
    if uploaded_file:
        st.success("✅ File uploaded successfully!")
        st.markdown("### 👤 **Analysis Settings**")

# MAIN CONTENT
if uploaded_file is not None:
    with st.spinner("🔄 Processing chat data..."):
        bytes_data = uploaded_file.getvalue()
        data = bytes_data.decode("utf-8", errors='ignore')
        
        try:
            df = preprocessor.preprocess(data)

            # Safe user list
            user_list = df['user'].unique().tolist()
            if 'group_notification' in user_list:
                user_list.remove('group_notification')
            user_list.sort()
            user_list.insert(0,"Overall")

            selected_user = st.sidebar.selectbox("🎯 Analyze", user_list)

            if st.sidebar.button("🚀 **GENERATE FULL ANALYSIS**", use_container_width=True):

                # 🌟 BEAUTIFUL STATS CARDS
                st.markdown("---")
                stats = helper.fetch_stats(selected_user, df)
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h3>💬 Messages</h3>
                        <h1 style='color:white; font-size:2.5rem;'>{stats[0]:,}</h1>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h3>📝 Words</h3>
                        <h1 style='color:white; font-size:2.5rem;'>{stats[1]:,}</h1>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h3>🖼️ Media</h3>
                        <h1 style='color:white; font-size:2.5rem;'>{stats[2]}</h1>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col4:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h3>🔗 Links</h3>
                        <h1 style='color:white; font-size:2.5rem;'>{stats[3]}</h1>
                    </div>
                    """, unsafe_allow_html=True)

                # 📊 TIMELINE CHARTS
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("## 📅 **Monthly Timeline**")
                    timeline = helper.monthly_timeline(selected_user, df)
                    fig, ax = plt.subplots(figsize=(10, 4))
                    ax.plot(timeline['time'], timeline['message'], color='#00D4AA', linewidth=3, marker='o')
                    ax.set_title("📈 Messages Over Time", fontsize=16, color='white')
                    plt.xticks(rotation=45)
                    st.pyplot(fig)

                with col2:
                    st.markdown("## 🗓️ **Daily Timeline**")
                    daily_timeline = helper.daily_timeline(selected_user, df)
                    fig, ax = plt.subplots(figsize=(10, 4))
                    ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='#FF6B6B', linewidth=3, marker='s')
                    ax.set_title("📊 Daily Activity", fontsize=16, color='white')
                    plt.xticks(rotation=45)
                    st.pyplot(fig)

                # 🔥 ACTIVITY MAPS
                st.markdown("---")
                st.markdown("## ⚡ **Activity Patterns**")
                col1, col2 = st.columns(2)
                
                with col1:
                    busy_day = helper.week_activity_map(selected_user, df)
                    fig, ax = plt.subplots(figsize=(8, 5))
                    ax.bar(busy_day.index, busy_day.values, color='#9B59B6')
                    ax.set_title("🔥 Most Busy Day", fontsize=14, color='white')
                    plt.xticks(rotation=45)
                    st.pyplot(fig)

                with col2:
                    busy_month = helper.month_activity_map(selected_user, df)
                    fig, ax = plt.subplots(figsize=(8, 5))
                    ax.bar(busy_month.index, busy_month.values, color='#F39C12')
                    ax.set_title("📅 Busiest Month", fontsize=14, color='white')
                    plt.xticks(rotation=45)
                    st.pyplot(fig)

                # HEATMAP
                st.markdown("## 🌡️ **Weekly Heatmap**")
                user_heatmap = helper.activity_heatmap(selected_user, df)
                fig, ax = plt.subplots(figsize=(12, 6))
                sns.heatmap(user_heatmap, annot=True, fmt='d', cmap='YlOrRd', ax=ax)
                ax.set_title("⏰ Activity Heatmap (Messages per Hour)", fontsize=16, color='white')
                st.pyplot(fig)

                # 👥 BUSY USERS (Overall only)
                if selected_user == 'Overall':
                    st.markdown("---")
                    st.markdown("## 🏆 **Top Chatters**")
                    x, new_df = helper.most_busy_users(df)
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        fig, ax = plt.subplots(figsize=(8, 6))
                        ax.bar(x.index, x.values, color='#E74C3C')
                        ax.set_title("💪 Most Active Users", fontsize=16, color='white')
                        plt.xticks(rotation=45)
                        st.pyplot(fig)
                    
                    with col2:
                        st.dataframe(new_df.style.background_gradient(cmap='Reds'))

                # ☁️ WORDCLOUD
                st.markdown("---")
                st.markdown("## 🌈 **Word Cloud**")
                df_wc = helper.create_wordcloud(selected_user, df)
                fig, ax = plt.subplots(figsize=(12, 8))
                ax.imshow(df_wc, interpolation='bilinear')
                ax.axis('off')
                st.pyplot(fig)

                # 📝 MOST COMMON WORDS
                st.markdown("## 🗣️ **Top Words**")
                most_common_df = helper.most_common_words(selected_user, df)
                fig, ax = plt.subplots(figsize=(10, 8))
                ax.barh(range(len(most_common_df)), most_common_df[1], color='#3498DB')
                ax.set_yticks(range(len(most_common_df)))
                ax.set_yticklabels(most_common_df[0])
                ax.set_title("🔝 Most Common Words", fontsize=16, color='white')
                st.pyplot(fig)

                # 😎 EMOJI ANALYSIS
                st.markdown("---")
                st.markdown("## 🎭 **Emoji Usage**")
                emoji_df = helper.emoji_helper(selected_user, df)
                col1, col2 = st.columns(2)
                
                with col1:
                    st.dataframe(emoji_df.head(10).style.background_gradient(cmap='Blues'))
                
                with col2:
                    fig, ax = plt.subplots(figsize=(8, 6))
                    ax.pie(emoji_df[1].head(8), labels=emoji_df[0].head(8), autopct='%1.1f%%', startangle=90)
                    ax.set_title("🎨 Emoji Distribution", fontsize=16, color='white')
                    st.pyplot(fig)

                # 💾 DOWNLOAD BUTTON
                st.markdown("---")
                csv = df.to_csv(index=False)
                st.download_button(
                    "💾 Download Full Analysis CSV",
                    csv,
                    "whatsapp_chat_analysis.csv",
                    "text/csv",
                    key='download-csv'
                )

        else:
            st.info("👆 Upload a file and click **GENERATE FULL ANALYSIS** to see insights!")
            
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        st.info("💡 Tip: Export WhatsApp chat → Without Media → TXT file")

else:
    st.markdown("""
    ## 🚀 **Ready to Analyze?**
    1. Open WhatsApp → Any Group Chat
    2. Tap Group Name → **Export Chat**
    3. Choose **Without Media** → Save TXT
    4. Upload here and **GENERATE INSIGHTS**!
    """)
