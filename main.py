import streamlit as st
import qrcode
from io import BytesIO
# 複雑なインポートをやめ、基本機能だけでオシャレにする
from qrcode.image.pure import PyPNGImageWrapper 

# --- パスワードチェック機能 ---
def check_password():
    if "password_correct" not in st.session_state:
        st.text_input("パスワード", type="password", key="password_input")
        if st.button("ログイン"):
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

    url = st.text_input("URLを入力", "https://")
    
    style_options = {
        "シック（紺×白）": {"fg": "#2E4053", "bg": "#FFFFFF"},
        "カフェ（茶×ベージュ）": {"fg": "#5D4037", "bg": "#FFF9C4"},
        "モダン（黒×薄灰）": {"fg": "#000000", "bg": "#F5F5F5"}
    }
    
    selected_style = st.selectbox("デザインを選んでください", list(style_options.keys()))
    colors = style_options[selected_style]

    if st.button("QRコードをデザインする"):
        # 設定をシンプルに変更
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)

        # エラーの出にくい標準的な方法で色を反映
        img = qr.make_image(fill_color=colors["fg"], back_color=colors["bg"])
        
        buf = BytesIO()
        img.save(buf)
        byte_im = buf.getvalue()
        
        st.image(byte_im, caption=f"{selected_style} スタイルで作成しました")
        
        st.download_button(
            label="このデザインで保存",
            data=byte_im,
            file_name="designer_qr.png",
            mime="image/png"
        )
