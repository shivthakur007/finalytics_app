import streamlit as st
import time

st.set_page_config(page_title="Happy 21st Birthday Sneha 🎉", layout="centered")

# ===== CSS Background + Animations =====
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(270deg, #ff758c, #ff7eb3, #6a82fb, #fc5c7d);
        background-size: 800% 800%;
        animation: gradientBG 20s ease infinite;
        position: relative;
        overflow: hidden;
    }
    @keyframes gradientBG {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }

    /* Floating hearts */
    .heart {
        position: fixed;
        width: 20px;
        height: 20px;
        background: red;
        transform: rotate(45deg);
        animation: floatHearts 10s linear infinite;
        opacity: 0.7;
        z-index: 0;
    }
    .heart:before,
    .heart:after {
        content: "";
        position: absolute;
        width: 20px;
        height: 20px;
        background: red;
        border-radius: 50%;
    }
    .heart:before { top: -10px; left: 0; }
    .heart:after { left: -10px; top: 0; }

    @keyframes floatHearts {
        from {transform: translateY(100vh) scale(0.6) rotate(45deg); opacity: 1;}
        to {transform: translateY(-10vh) scale(1) rotate(45deg); opacity: 0;}
    }

    /* Floating sparkles */
    .sparkle {
        position: fixed;
        width: 6px;
        height: 6px;
        background: white;
        border-radius: 50%;
        animation: floatSparkles 8s linear infinite;
        opacity: 0.8;
        z-index: 0;
    }
    @keyframes floatSparkles {
        from {transform: translateY(100vh) scale(0.5); opacity: 1;}
        to {transform: translateY(-10vh) scale(1.2); opacity: 0;}
    }
    </style>

    <!-- Generate multiple hearts and sparkles -->
    <div class="heart" style="left:10%; animation-delay:0s;"></div>
    <div class="heart" style="left:30%; animation-delay:2s;"></div>
    <div class="heart" style="left:50%; animation-delay:4s;"></div>
    <div class="heart" style="left:70%; animation-delay:6s;"></div>
    <div class="heart" style="left:90%; animation-delay:8s;"></div>

    <div class="sparkle" style="left:20%; animation-delay:1s;"></div>
    <div class="sparkle" style="left:40%; animation-delay:3s;"></div>
    <div class="sparkle" style="left:60%; animation-delay:5s;"></div>
    <div class="sparkle" style="left:80%; animation-delay:7s;"></div>
    """, unsafe_allow_html=True)

# ===== Main Content =====
st.title("🎂 Happy 21st Birthday Sneha! 🎉")

st.markdown("""
## 💌 My Dearest Sneha  
On this very special day, I want to celebrate *you*.  
You’re not just turning 21, you’re stepping into a beautiful new chapter of life.  
May your day be filled with love, laughter, and memories that last forever. 🥳💖  
""")

st.markdown("---")

st.header("💖 7 Praises for You 💖")
st.markdown("Click below to reveal each praise, one at a time! 🎁")

praises = [
    "Your eyes hold so much depth that anyone who can’t swim could easily drown in them. I’m lucky I know how to swim — that’s why I’m still alive.",
    "Your smile is so contagious that it has the power to make even the sanest person go delightfully insane.",
    "Your lips are like rose petals — roses that could only be found in the Garden of Eden.",
    "The way you carry yourself with so much beauty and elegance… I think I need to inform the Oxford Dictionary team that the word ‘elegance’ should be replaced with ‘Snehance.’",
    "When I say something sarcastically bad to you and you respond with ‘Hawww,’ that ‘Hawww’ has the most wholesome effect.",
    "When you get upset, it feels like the whole world stops. I have to do everything to revive it by making you happy. I like doing that because I am the savior of this world, and all of this is for the life that exists on Earth — especially yours.",
    "Being around you makes everything brighter. Your presence turns ordinary moments into memories I’ll cherish forever, and I can’t imagine a day without your light."
]

if "index" not in st.session_state:
    st.session_state.index = 0

if st.button("✨ Reveal Next Praise ✨"):
    if st.session_state.index < len(praises):
        st.success(f"💖 {praises[st.session_state.index]} 💖")
        st.session_state.index += 1
        st.markdown("❤️✨💖✨❤️")
        time.sleep(0.3)
    else:
        st.balloons()
        st.success("🎉 Happy 21st once again, Sneha! You are truly amazing and loved 💕")
