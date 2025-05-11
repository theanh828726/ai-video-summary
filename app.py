
import streamlit as st
import requests
import openai
import tempfile
import os

st.set_page_config(page_title="AI Video Summary - Thế Anh", layout="wide")
st.title("🎥 AI Video Summary & Caption Generator")
st.markdown("**by AI Thế Anh – Humanized AI for Business**")

st.sidebar.image("https://raw.githubusercontent.com/thanhduongk17/ai-assets/main/logo-ai-theanh.png", width=200)
st.sidebar.write("### Chọn ngôn ngữ hiển thị")
language = st.sidebar.radio("Ngôn ngữ", ["Tiếng Việt", "English", "Song ngữ"])

video_file = st.file_uploader("📂 Tải video lên", type=["mp4", "mov", "m4a"])

if video_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
        tmp.write(video_file.read())
        temp_video_path = tmp.name
        st.video(temp_video_path)

    with st.spinner("✨ Đang xử lý transcript (Whisper API)..."):
        whisper_api = "https://api.aivio.vn/whisper-transcribe"
        files = {'file': open(temp_video_path, 'rb')}
        response = requests.post(whisper_api, files=files)

        if response.status_code == 200:
            transcript = response.json().get("text")
            st.success("✅ Đã xong! Dưới đây là transcript:")
            st.text_area("Transcript", transcript, height=300)
        else:
            st.error("⚠️ Lỗi khi trích transcript.")
            st.stop()

    with st.spinner("🤖 Đang tóm tắt bằng GPT..."):
        openai.api_key = st.secrets["OPENAI_API_KEY"]
        prompt = f"Tóm tắt nội dung video dưới đây. Trình bày rõ ràng theo các ý chính.\nTranscript:\n{transcript}"
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Bạn là trợ lý AI chuyên tóm tắt nội dung video."},
                {"role": "user", "content": prompt}
            ]
        )
        summary = response.choices[0].message.content
        st.markdown("### 📖 Tóm tắt nội dung:")
        st.write(summary)

    with st.spinner("🎤 Đang gợi ý caption YouTube..."):
        caption_prompt = f"Viết 3 dòng caption YouTube hấp dẫn cho video sau:\n{summary}"
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Bạn là chuyên gia marketing, viết caption YouTube lôi cuốn."},
                {"role": "user", "content": caption_prompt}
            ]
        )
        captions = response.choices[0].message.content
        st.markdown("### 📌 Gợi ý caption YouTube:")
        st.write(captions)

    with st.spinner("🔮 Đang phân tích sơ đồ tư duy..."):
        mindmap_prompt = f"Chuyển nội dung sau thành sơ đồ tư duy đơn giản như kiểu Whimsical:\n{summary}"
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Bạn là trợ lý AI vẽ sơ đồ tư duy."},
                {"role": "user", "content": mindmap_prompt}
            ]
        )
        mindmap_text = response.choices[0].message.content
        st.markdown("### 📊 Sơ đồ tư duy (text):")
        st.code(mindmap_text, language='markdown')

    st.download_button("🔗 Tải về transcript", transcript, file_name="transcript.txt")
    st.download_button("🔗 Tải về tóm tắt", summary, file_name="summary.txt")
    st.download_button("🔗 Tải caption", captions, file_name="youtube_caption.txt")
