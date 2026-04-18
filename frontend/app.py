import streamlit as st
import requests

st.set_page_config(page_title="AttentionX", page_icon="🎬", layout="wide")

# Inject CSS for full customization
st.markdown(
    """
    <style>
    /* Global background */
    .stApp {
        background: linear-gradient(135deg, #0d0d0d, #1a1a1a, #2c2c2c);
        font-family: 'Segoe UI', sans-serif;
        color: #f5f5f5;
        padding: 20px;
    }

    /* Title styling */
    .main-title {
        font-size: 60px;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(90deg, #ff00cc, #3333ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 20px;
    }

    /* Subtitle */
    .description {
        text-align: center;
        font-size: 22px;
        margin-bottom: 50px;
        color: #cccccc;
    }

    /* Upload box */
    .upload-box {
        border: 2px dashed #ff00cc;
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        background: rgba(255,255,255,0.05);
        margin-bottom: 40px;
        font-size: 18px;
        color: #ffffff;
    }

    /* File uploader text fix */
    .stFileUploader label {
        color: #ffffff !important;
        font-size: 18px;
        font-weight: 600;
        border-radius: 10px;
    }


    /* Clip cards */
    .clip-card {
        background: rgba(255,255,255,0.08);
        backdrop-filter: blur(12px);
        border-radius: 15px;
        padding: 25px;
        margin: 20px;
        transition: transform 0.3s ease, background 0.3s ease;
        color: #ffffff;
    }
    .clip-card:hover {
        transform: translateY(-5px) scale(1.03);
        background: rgba(255,255,255,0.2);
    }
    

    /* Button */
.stButton>button {
    background: linear-gradient(90deg, #6366f1, #a855f7);
    color: white;
    border-radius: 12px;
    padding: 10px 24px;
    font-weight: 600;
    border: none;
}

.stButton>button:hover {
    transform: scale(1.05);
}


    /* Smaller video */
video {
    border-radius: 10px;
    max-height: 220px;

}

/* 🔥 Download button visible */
.stDownloadButton button {
    background: linear-gradient(90deg, #ff00cc, #3333ff);
    color: white;
    border-radius: 10px;
    padding: 8px 14px;
    margin-top: 10px;
    font-weight: 600;
    border: none;
}

.stDownloadButton button:hover {
    transform: scale(1.05);
}

/* Remove empty container feel */
.stAlert {
    background: transparent !important;
    border: none !important;
}

/* Center video perfectly */
video {
    display: block;
    margin-left: auto;
    margin-right: auto;
    max-width: 620px;
    border-radius: 10px;
}

/* Center download button */
.stDownloadButton {
    display: flex;
    justify-content: center;
    width: 100%;
}


    /* Section headers */
    h3 {
        color: #ffffff;
        font-weight: 700;
        margin-top: 30px;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title + description
st.markdown('<div class="main-title">ClipForge 🎬 Viral Video Repurposing Engine</div>', unsafe_allow_html=True)
st.markdown('<div class="description">Turn long mentorship sessions into viral short clips with captions — instantly!</div>', unsafe_allow_html=True)

# Upload section
uploaded_file = st.file_uploader("Upload your video", type=["mp4", "mov", "avi"])
generate = st.button("✨ Generate Clips")

st.markdown('</div>', unsafe_allow_html=True)

# Processing
if uploaded_file and generate:
    with st.spinner("Analyzing video... ⏳"):
        files = {"file": uploaded_file}
        response = requests.post("http://localhost:8000/upload/", files=files)

    try:
        data = response.json()

        if "error" in data:
            st.error(data["error"])
        else:
            st.success("Clips generated successfully 🎉")
            
            if len(data["output"]) == 0:
                st.warning("No clips found 😢")
            else:
                # ✅ Centered Title
                st.markdown(
                    "<h2 style='text-align:center; margin-top:40px;'>🔥 Your Viral Clips</h2>",
                    unsafe_allow_html=True
                )

                for i, clip in enumerate(data["output"]):
                    
                    # 🔥 ONE CENTERED CONTAINER FOR EVERYTHING
                    st.markdown(
                        """
                        <div style="
                            display:flex;
                            flex-direction:column;
                            align-items:center;
                            justify-content:center;
                            margin-top:30px;
                        ">
                        """,
                        unsafe_allow_html=True
                    )

                    # 🎥 Video (centered)
                    st.video(clip)

                    # 🔥 Caption (centered)
                    st.markdown(
                        f"<p style='text-align:center;'>🔥 Clip {i+1}</p>",
                        unsafe_allow_html=True
                    )

                    # ⬇ Download button (centered)
                    st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)

                    st.download_button(
                        "⬇ Download",
                        data=clip,
                        file_name=f"clip_{i+1}.mp4"
                    )

                    st.markdown("</div></div>", unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Error: {e}")
        st.text(response.text)