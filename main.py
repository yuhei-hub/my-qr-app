import streamlit as st
import qrcode
from io import BytesIO

# 1. Webサイトのタイトルを作る
st.title("オリジナルQRコード作成器")

# 2. 入力欄をオシャレに作成
url = st.text_input("QRコードにしたいURLを入力してね", "https://")

# 3. ボタンが押されたらQRコードを作成
if st.button("作成する"):
    qr = qrcode.make(url)
    
    # 画像をメモリ上に保存（Webで表示するため）
    buf = BytesIO()
    qr.save(buf, format="PNG")
    byte_im = buf.getvalue()
    
    # 4. 画面に表示
    st.image(byte_im, caption="完成したQRコード")
    
    # 5. ダウンロードボタンも設置
    st.download_button(
        label="画像をダウンロード",
        data=byte_im,
        file_name="my_qr.png",
        mime="image/png"
    )
