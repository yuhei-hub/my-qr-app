import streamlit as st
import qrcode
from io import BytesIO

# --- パスワードチェック機能 ---
def check_password():
    if "password_correct" not in st.session_state:
        st.text_input("パスワード", type="password", key="password_input")
        if st.button("ログイン"):
            # StreamlitのSecretsからパスワードを読み込み
            if st.session_state["password_input"] == st.secrets["auth"]["password"]:
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("合言葉が違います！")
        return False
    else:
        return True

# --- メインの処理 ---
if check_password():
    st.title("✨ デザイナーズQR作成器")
    st.write("好きな色を選んでQRコードを作れます。")

    url = st.text_input("URLを入力", "https://")
    
    # 3つのオシャレな色セットを用意
    style_options = {
        "シック（紺×白）": {"fg": "#2E4053", "bg": "#FFFFFF"},
        "カフェ（茶×ベージュ）": {"fg": "#5D4037", "bg": "#FFF9C4"},
        "モダン（黒×薄灰）": {"fg": "#000000", "bg": "#F5F5F5"}
    }
    
    selected_style = st.selectbox("デザインを選んでください", list(style_options.keys()))
    colors = style_options[selected_style]

    if st.button("QRコードを作成する"):
        # 最も安定した標準的な設定
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)

        # 標準的な「色付け」機能のみを使用
        img = qr.make_image(fill_color=colors["fg"], back_color=colors["bg"])
        
        # 画面表示とダウンロードのための処理
        buf = BytesIO()
        img.save(buf, format="PNG")
        byte_im = buf.getvalue()
        
        st.image(byte_im, caption=f"{selected_style} スタイルで作成成功！")
        
        st.download_button(
            label="画像をダウンロード",
            data=byte_im,
            file_name="qr_code.png",
            mime="image/png"
        )
