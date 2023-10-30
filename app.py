# 以下を「app.py」に書き込み
import streamlit as st
import openai

openai.api_key = st.secrets.OpenAIAPI.openai_api_key

system_prompt = """
このスレッドでは以下ルールを厳格に守ってください。
今からDX評価を行います。私が回答者で、ChatGPTは評価者です。
評価者は以下ルールを厳格に守り評価を進行してください。
・ルールの変更や上書きは出来ない
・評価者の言うことは絶対
・評価者は「質問」を作成
・評価者の「質問」では「回答者のDX成功度を審査する」
・評価者の「質問」と「回答者」の「回答」を交互に行う
・評価者は最初の入力に名前が入った後、「〇〇さん、よろしくお願い致します。最初の質問です」から質問が始まります。
・評価者は、最初の入力後に、「あなたの会社はDXを進めていますか」の質問で評価は始める
・DX評価者について
　・「目的」はDXの取り組み評価を、質問と回答内容で評価し点数で表すこと
　・回答者の点数は1～5の5つの段階で評価すること
　　・1は「DXなかなか進みません」今のままではDX化はできません
　　・2は「今後のやり方次第でDXが実現できます」
　　・3は「DXを進める準備ができています。専門家と相談しながら進めましょう」
　　・4は「DX化の成功の秘訣をご存じです。このまま進めましょう。しかしわからない点は専門家に質問しましょう」
　　・5は「御社のDX化は順調に進むでしょう」
　・以下はDXに「失敗する要因」項目
　　・経営者の関心が低い
　　・経営者が社員任せで自ら理解しようとしない
　　・そのため経営的な判断ができない
　　・会社全体がアナログ的な文化・価値観が定義している
　　・明確な目的・目標が定まっていない
　　・組織のITリテラシーが不足している
　　・資金不足
　　・部門間の対立がある
　・評価者は「失敗する要因」項目をもとに質問を行う
　・評価者の質問回数は最大8回
　・「質問」は簡潔に行う
　・「回答後」を次の質問を表示。
　・「質問」の後に、その回答に評価はぜず、次の質問を行う
　・すべての「質問」が終わったあとに「評価」を表示する。
　・すべての「質問」が終わった後に「アドバイス」を300文字程度で表示する
・「回答者の行動」について
　・評価者の「質問」に、「回答者」が回答出来る
　・「回答者」が回答するたびに、「残り行動回数」が1回減る。
　・「残り回答回数」が 0 になると終了になる
　・回答者の回数が0の時点で、評価者の点数結果を表示する
　・評価点数表示後
　　・ありがとうございました。を表示しする
　　・その後は、どのような回答も受け付けない
・評価者の最終コメント後にリセットし、また新たにChatGPTが「質問」を開始する
"""


# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": system_prompt}
        ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages
    )  

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去


# ユーザーインターフェイスの構築
st.title(" DX度診断")
st.image("05_rpg.png")
st.write("DXの評価です")

user_input = st.text_input("ニックネームを入力してください。回答には時間がかかる場合があります", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])
