import os
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from dotenv import load_dotenv

# .envファイルの読み込み（ローカル環境用、Streamlit Cloudではsecretsを使用）
load_dotenv()

# OpenAI APIキーの取得
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or st.secrets["OPENAI_API_KEY"]

# LLMインスタンスの初期化
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.3,
    openai_api_key=OPENAI_API_KEY
)

# システムメッセージを選択肢に応じて返す関数
def get_system_message(role: str) -> str:
    if role == "キャリアアドバイザー":
        return "あなたは経験豊富なキャリアアドバイザーです。丁寧に、かつ現実的なアドバイスを提供してください。"
    elif role == "健康アドバイザー":
        return "あなたは信頼できる健康アドバイザーです。安全かつ効果的な健康アドバイスを提供してください。"
    elif role == "旅行プランナー":
        return "あなたは旅行プランナーのプロです。希望に合った最適な旅行プランを提案してください。"
    else:
        return "あなたは親切で知識豊富なアシスタントです。"

# ユーザーの入力と専門家の種類に基づきLLMに問い合わせる関数
def get_response(user_input: str, expert_role: str) -> str:
    messages = [
        SystemMessage(content=get_system_message(expert_role)),
        HumanMessage(content=user_input)
    ]
    result = llm.invoke(messages)
    return result.content

# Streamlit UI
st.set_page_config(page_title="専門家AIアドバイザー", layout="centered")
st.title("💬 専門家AIアドバイザー")
st.markdown("このアプリでは、3種類の専門家から1人を選び、質問を入力することでAIからアドバイスを得られます。")

# ラジオボタンで専門家の選択
expert_type = st.radio("相談したい専門家を選んでください", ("キャリアアドバイザー", "健康アドバイザー", "旅行プランナー"))

# 入力フォーム
user_query = st.text_input("あなたの質問を入力してください")

# 回答表示
if st.button("送信") and user_query:
    with st.spinner("AIが回答中..."):
        response = get_response(user_query, expert_type)
        st.success("✅ 回答")
        st.write(response)
