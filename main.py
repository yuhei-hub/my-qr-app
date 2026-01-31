import streamlit as st
import qrcode
from io import BytesIO

# --- パスワードチェック機能 ---
def check_password():
    if "password_correct" not in st.session_state:
        st.text_input("パスワードを入力してね 🤫", type="password", key="password_input")
        if st.button("ログイン"):
            if st.session_state["password_input"] == st.secrets["auth"]["password"]:
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("合言葉がちがうよ！")
        return False
    else:
        return True

# --- メインの処理 ---
if check_password():
    st.title("🌈 遊び心満載！QR作成器")
    st.write("標準機能だけでオシャレに。好きな雰囲気を選んでね。")

    url = st.text_input("QRコードにするURL", "https://")
    
    # 遊び心のある5つのテーマ
    style_options = {
        "🌑 真夜中のネオン (Black & Lime)": {"fg": "#32CD32", "bg": "#000000"},
        "🌸 桜もち (Pink & Green)": {"fg": "#FFB7C5", "bg": "#A5D6A7"},
        "🌊 深海 (Deep Blue & Cyan)": {"fg": "#00FFFF", "bg": "#001F3F"},
        "🍫 チョコミント (Brown & Mint)": {"fg": "#4E342E", "bg": "#B2DFDB"},
        "🍊 ビタミンカラー (Orange & White)": {"fg": "#FF9800", "bg": "#FFFFFF"}
    }
    
    selected_style = st.selectbox("どのテーマで作る？", list(style_options.keys()))
    colors = style_options[selected_style]

    if st.button("このデザインで作成！"):
        # 標準の安定した設定
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)

        # 選択した色を適用
        img = qr.make_image(fill_color=colors["fg"], back_color=colors["bg"])
        
        buf = BytesIO()
        img.save(buf, format="PNG")
        byte_im = buf.getvalue()
        
        st.image(byte_im, caption=f"✨ {selected_style} スタイルが完成！")
        
        st.download_button(
            label="この画像を保存する",
            data=byte_im,
            file_name="asobi_qr.png",
            mime="image/png"
        )
