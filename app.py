import streamlit as st
import google.generativeai as genai

# --- 画面のUI設定 ---
st.set_page_config(page_title="ワイン名ゆらぎ生成", page_icon="🍷")
st.title("🍷 ワイン名表記ゆらぎ自動生成ツール")
st.write("商品名を入力すると、AIが検索用の表記ゆらぎ（アルファベットの原語表記を含む）を自動生成します。")

# --- APIキーの入力欄（サイドバーに配置してスッキリと） ---
with st.sidebar:
    st.header("⚙️ 設定")
    api_key = st.text_input("Gemini APIキーを入力:", type="password", help="Google AI Studioで取得したAPIキーを入力してください。")
    st.caption("※セキュリティのため、APIキーは保存されません。")

# --- メイン画面 ---
wine_name = st.text_input("商品名（カタカナ等）を入力してください:", placeholder="例：アルマヴィーヴァ")

# ボタンが押されたときの処理
if st.button("ゆらぎパターンを生成", type="primary"):
    if not api_key:
        st.warning("👈 左側のサイドバーにGemini APIキーを入力してください。")
    elif not wine_name:
        st.warning("ワイン名を入力してください。")
    else:
        try:
            # AIの準備と実行
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            prompt = f"""
            あなたはワインの専門家であり、ECサイトの検索最適化のプロです。
            以下のワイン名について、日本語の「表記ゆらぎ」と「アルファベット表記（原語）」をリストアップしてください。
            検索エンジンにヒットしやすくなるよう、考えられるパターンを網羅してください。

            ワイン名: {wine_name}

            出力形式:
            スペース区切りの単語リストのみを出力してください。余計な説明は一切不要です。
            例: アルマヴィーヴァ アルマビーバ アルマビーヴァ アルマビバ Almaviva
            """
            
            # クルクル回るローディング表示
            with st.spinner('AIがゆらぎパターンを考え中です...'):
                response = model.generate_content(prompt)
                result = response.text.strip()
            
            # 結果の表示
            st.success("✨ 生成が完了しました！")
            st.text_area("検索用キーワード（OR検索用などにコピーしてお使いください）：", value=result, height=100)
            
        except Exception as e:
            st.error(f"エラーが発生しました。APIキーが正しいか確認してください。（エラー詳細: {e}）")