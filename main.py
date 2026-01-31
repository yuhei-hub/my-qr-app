import streamlit as st
import qrcode
from io import BytesIO

# --- パスワードチェック機能 ---
def check_password():
    if "password_correct" not in st.session_state:
        st.text_input("パスワードを入力してください", type="password", key="password_input")
        if st.button("ログイン"):
            if st.session_state["password_input"] == st.secrets["auth"]["password"]:
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("パスワードが正しくありません")
        return False
    else:
        return True

# --- メインの処理 ---
if check_password():
    st.title("QRコード作成ツール")
    st.write("URLを入力し、カラーを選択してQRコードを生成してください。")

    url = st.text_input("対象のURL", "https://")
    
    # 実用的でシンプルなカラーバリエーション
    style_options = {
        "スタンダード（黒 / 白）": {"fg": "#000000", "bg": "#FFFFFF"},
        "ネイビー（紺 / 白）": {"fg": "#001F3F", "bg": "#FFFFFF"},
        "ダークグレー（灰 / 白）": {"fg": "#333333", "bg": "#FFFFFF"},
        "ブルー（青 / 薄青）": {"fg": "#007BFF", "bg": "#E7F3FF"},
        "セピア（茶 / ベージュ）": {"fg": "#5D4037", "bg": "#F5F5DC"}
    }
    
    selected_style = st.selectbox("カラーを選択", list(style_options.keys()))
    colors = style_options[selected_style]

    if st.button("QRコードを生成"):
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
        
        st.image(byte_im, caption=f"選択済み：{selected_style}")
        
        st.download_button(
            label="画像をダウンロード",
            data=byte_im,
            file_name="qr_code.png",
            mime="image/png"
        )
