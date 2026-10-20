import streamlit as st
from google import genai
import os
from dotenv import load_dotenv

# Environment variables load karein
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# Nayi Google GenAI Client Configure karein
client = None
if API_KEY:
    try:
        client = genai.Client(api_key=API_KEY)
    except Exception as e:
        st.error(f"Client initialization error: {e}")
else:
    st.error("⚠️ Security Alert: API Key nahi mili! .env file check karein.")

# Page Configuration
st.set_page_config(page_title="Hulku - AI Creator Studio", page_icon="⚡", layout="centered")

# CSS file load karna for animations
try:
    with open("static/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except:
    pass

# Session State for Ad Tracking
if 'generation_count' not in st.session_state:
    st.session_state.generation_count = 0

# App Header
st.title("⚡ HULKU - Next-Gen AI Creator Studio")
st.markdown("### *Banao viral captions, memes aur stories ekdum fast aur secure tareeqe se!*")
st.divider()

# Sidebar: Language & Settings
with st.sidebar:
    st.header("⚡ Hulku AI Studio")
    st.success("🟢 Server Online & Secure")
    st.divider()
    
    # 🌐 3 Languages Selection Option
    selected_lang = st.selectbox(
        "🌐 Output Language Chunein:", 
        ["Desi Hinglish", "English", "Pure Hindi"]
    )
    
    st.divider()
    st.info("💡 **Hulku Tip:** Apni pasand ki language select karo aur ek click mein viral content pao!")

# Main Application Logic
user_topic = st.text_input("Aapko kis topic par content chahiye? (Jaise: Startup struggle, Chai lover, Motivation)")
content_type = st.selectbox("Category chunein:", ["Viral Instagram Caption", "Desi Hinglish Shayari", "Startup/Business Meme Idea"])

if st.button("🚀 Generate Content Now"):
    if user_topic.strip() == "":
        st.warning("Pehle koi topic toh likhiye bhai!")
    elif client is None:
        st.error("API client configure nahi hai. Please check API key.")
    else:
        st.session_state.generation_count += 1
        
        with st.spinner(f"✨ Hulku AI {selected_lang} mein magic create kar raha hai..."):
            # Sponsored Ad Display
            st.markdown("""
                <div style='background: rgba(236, 72, 153, 0.1); border: 1px dashed #ec4899; padding: 12px; border-radius: 8px; text-align: center; margin-bottom: 15px;'>
                    <p style='color: #ec4899; font-size: 14px; margin: 0;'>📢 <b>Sponsored Ad:</b> Powered by Hulku Partner Network (Ad Loaded)</p>
                </div>
            """, unsafe_allow_html=True)
            
            # Prompt mein Language dynamically pass karna
            prompt = f"Create a catchy, viral, and engaging {content_type} based on this topic: {user_topic}. Write the final output strictly in {selected_lang} language. Use emojis and relevant hashtags."
            
            try:
                response = client.models.generate_content(
                    model='gemini-3.8-flash',
                    contents=prompt,
                )
                st.subheader(f"🎉 Aapka Content ({selected_lang}) Tayar Hai:")
                st.success(response.text)
            except Exception as e:
                st.error(f"Kuch error aa gaya: {e}")

# Footer
st.markdown("<br><hr><center><p style='color: #94a3b8; font-size: 12px;'>Powered by Hulku Engine © 2026</p></center>", unsafe_allow_html=True)