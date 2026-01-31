import streamlit as st
import qrcode
from io import BytesIO

# --- パスワードチェック機能 ---
def check_password():
    """パスワードが正しいか確認する関数"""
    if "password_correct" not in st.session_state:
        # まだ入力していない状態
        st.text_input("合言葉を入力してください", type="password", key="password_input")
        if st.button("ログイン"):
            # Secretsに保存したパスワードと一致するかチェック
            if st.session_state["password_input"] == st.secrets["auth"]["password"]:
                st.session_state["password_correct"] = True
                st.rerun() # 画面を更新して中身を表示
            else:
                st.error("合言葉が違います！")
        return False
    else:
        # すでに正解を入力済み
        return True

# --- メインの処理 ---
if check_password():
    # パスワードが正しい時だけ、以下のQRコード作成機能が動く
    st.title("オリジナルQRコード作成器（限定公開版）")

    url = st.text_input("QRコードにしたいURLを入力してね", "https://")

    if st.button("作成する"):
        qr = qrcode.make(url)
        buf = BytesIO()
        qr.save(buf, format="PNG")
        byte_im = buf.getvalue()
        
        st.image(byte_im, caption="完成したQRコード")
        
        st.download_button(
            label="画像をダウンロード",
            data=byte_im,
            file_name="my_qr.png",
            mime="image/png"
        )
