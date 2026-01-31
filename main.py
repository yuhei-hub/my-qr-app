import streamlit as st
import qrcode
from io import BytesIO

# --- パスワードチェック機能 ---
def check_password():
    if "password_correct" not in st.session_state:
        st.text_input("パスワード", type="password", key="password_input")
        if st.button("ログイン"):
            if st.session_state["password_input"] == st.secrets["auth"]["password"]:
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("パスワードが違います！")
        return False
    else:
        return True

# --- メインの処理 ---
if check_password():
    st.title("🎨 おしゃれQRコード作成器")

    url = st.text_input("QRコードにしたいURLを入力してね", "https://")
    
    # 【新機能】色を選べるようにする
    col1, col2 = st.columns(2)
    with col1:
        fill_color = st.color_picker("QRコードの色", "#2E4053") # デフォルトはオシャレな紺色
    with col2:
        back_color = st.color_picker("背景の色", "#FFFFFF")    # デフォルトは白

    if st.button("作成する"):
        # 詳細な設定ができる QRCode クラスを使用
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)

        # ここで指定した色を反映！
        img = qr.make_image(fill_color=fill_color, back_color=back_color)
        
        buf = BytesIO()
        img.save(buf, format="PNG")
        byte_im = buf.getvalue()
        
        st.image(byte_im, caption="完成したオシャレなQRコード")
        
        st.download_button(
            label="画像をダウンロード",
            data=byte_im,
            file_name="stylish_qr.png",
            mime="image/png"
        )
