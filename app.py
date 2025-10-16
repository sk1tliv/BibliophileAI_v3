import os
import sys
import uuid
from datetime import datetime

import pandas as pd
import google.generativeai as genai
import markdown
from dotenv import load_dotenv
from flask import Flask, jsonify, redirect, render_template, request, session, url_for
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
import shutil

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("Error: GOOGLE_API_KEY not found. Please check .env file.")
    sys.exit(1)

genai.configure(api_key=api_key)
model = genai.GenerativeModel(
    "gemini-2.0-flash", 
    generation_config=genai.types.GenerationConfig(temperature=0.57),
)

# ----- Dosya yolları ve veri setleri -----
dataset_paths = [
    "data/books.csv",
    "data/Turkish_Book_Dataset_Kaggle_V2.csv",
    "data/TurkishBookDataSet.csv",
    "data/final_csv.csv",
    "data/final_csv2.csv",
    "data/final_excel.csv"
]

dfs = []
for path in dataset_paths:
    if os.path.exists(path):
        try:
            df = pd.read_csv(path, engine='python')
            if 'book_name' in df.columns:
                df.rename(columns={'book_name': 'title'}, inplace=True)
            if 'book_title' in df.columns:
                df.rename(columns={'book_title': 'title'}, inplace=True)
            if 'title' not in df.columns:
                if 'name' in df.columns:
                    df.rename(columns={'name': 'title'}, inplace=True)

            if 'writer' in df.columns:
                df.rename(columns={'writer': 'author'}, inplace=True)
            if 'book_author' in df.columns:
                df.rename(columns={'book_author': 'author'}, inplace=True)
            if 'author' not in df.columns:
                if 'book_author' in df.columns:
                    df.rename(columns={'book_author': 'author'}, inplace=True)

            publisher_cols = ['publisher', 'book_publisher', 'bookstore', 'book_publisher', 'book_publisher']
            for col in publisher_cols:
                if col in df.columns:
                    df.rename(columns={col: 'bookstore'}, inplace=True)
                    break

            summary_cols = ['summary', 'explanation', 'book_detail', 'description']
            for col in summary_cols:
                if col in df.columns:
                    df.rename(columns={col: 'summary'}, inplace=True)
                    break

            dfs.append(df)
        except Exception as e:
            print(f"{path} okunamadı: {e}")
    else:
        print(f"Uyarı: '{path}' bulunmadı.")

if dfs:
    book_df = pd.concat(dfs, ignore_index=True)
    for col in book_df.select_dtypes(include=['object']).columns:
        book_df[col] = book_df[col].fillna("")
else:
    book_df = pd.DataFrame()

# ----- Kitap arama fonksiyonu -----
def search_book_info(query):
    if book_df.empty or 'title' not in book_df.columns:
        return None
    exact_matches = book_df[book_df['title'].astype(str).str.lower() == query.lower()]
    if not exact_matches.empty:
        book = exact_matches.iloc[0]
    else:
        matches = book_df[book_df['title'].astype(str).str.lower().str.contains(query.lower(), na=False)]
        if matches.empty:
            return None
        book = matches.iloc[0]
    summary = book.get("summary", "")
    if not summary or summary.strip() == "":
        summary = "Özet bulunamadı"
    bookstore = book.get("bookstore", "")
    if not bookstore or bookstore.strip() == "":
        bookstore = "Kitabevi bilgisi bulunamadı"
    return {
        "title": book.get("title", "Bulunamadı"),
        "summary": summary,
        "author": book.get("author", "Yazar bilgisi yok"),
        "year": str(book.get("year", "Basım yılı yok")),
        "bookstore": bookstore,
        "purchase_link": book.get("purchase_link", "")
    }

# ----- Yanıt fonksiyonu -----
def get_answer(query, vectordb=None, top_k=3):
    book_info = search_book_info(query)
    if book_info:
        cevap = f"Kitap: {book_info['title']}\n"
        cevap += f"Yazar: {book_info['author']}\n"
        cevap += f"Basım Yılı: {book_info['year']}\n"
        cevap += f"Kitabevi: {book_info['bookstore']}\n"
        cevap += f"Özet:\n{book_info['summary']}\n"
        if book_info['purchase_link']:
            cevap += f"Satın alabileceğiniz link: {book_info['purchase_link']}\n"
        return cevap

    if vectordb:
        results = vectordb.similarity_search(query, k=top_k)
        context = "\n\n".join([doc.page_content for doc in results])
    else:
        context = ""

    prompt = f"""
Sen kitap öneren ve bilgiler sunan bir chatbot'sun.
Aşağıdaki bağlam ve veriyi kullanarak sorulara yanıt ver.
Bağlam veya veri bulunamazsa, genel bilgiye dayalı cevap ver.

BAĞLAM / VERİ:
{context}

KULLANICI SORUSU:
{query}

YANIT:
"""
    try:
        cevap = model.generate_content(prompt)
        print("Gemini yanıtı:", cevap.text)
        return cevap.text
    except Exception as e:
        print("Gemini API hatası:", str(e))
        return "Üzgünüm, şu anda cevap veremiyorum."

# ----- Markdown Dönüştürücü -----
def render_markdown(text):
    return markdown.markdown(
        text,
        extensions=[
            "markdown.extensions.extra",
            "markdown.extensions.codehilite",
            "markdown.extensions.smarty",
            "markdown.extensions.nl2br",
            "markdown.extensions.sane_lists",
        ],
    )

# ----- Flask Uygulaması -----
app = Flask(__name__)
app.secret_key = os.urandom(24)
conversations = {}

@app.route("/")
def index():
    if "session_id" not in session:
        session_id = str(uuid.uuid4())
        session["session_id"] = session_id
        conversations[session_id] = {
            "id": session_id,
            "title": f"Yeni Görüşme {datetime.now().strftime('%d.%m.%Y %H:%M')}",
            "created_at": datetime.now().strftime("%d.%m.%Y %H:%M"),
            "messages": [],
        }
    session_id = session["session_id"]
    current_convo = conversations.get(session_id, {
        "id": session_id,
        "title": f"Yeni Görüşme {datetime.now().strftime('%d.%m.%Y %H:%M')}",
        "created_at": datetime.now().strftime("%d.%m.%Y %H:%M"),
        "messages": [],
    })
    all_convos = [c for c in conversations.values()]
    return render_template("index.html", conversation_history=current_convo["messages"],
                           conversations=all_convos, current_session=session_id,
                           renderMarkdown=render_markdown)

@app.route("/send_message", methods=["POST"])
def send_message():
    data = request.json
    user_msg = data.get("message", "")
    session_id = session.get("session_id")
    if not session_id:
        session_id = str(uuid.uuid4())
        session["session_id"] = session_id

    if session_id not in conversations:
        conversations[session_id] = {
            "id": session_id,
            "title": f"Görüşme {datetime.now().strftime('%d.%m.%Y %H:%M')}",
            "created_at": datetime.now().strftime("%d.%m.%Y %H:%M"),
            "messages": [],
        }
    conversations[session_id]["messages"].append({"role": "user", "content": user_msg})

    if len(conversations[session_id]["messages"]) == 1:
        conversations[session_id]["title"] = user_msg[:30] + ("..." if len(user_msg) > 30 else "")

    try:
        cevap = get_answer(user_msg)
        conversations[session_id]["messages"].append({"role": "bot", "content": cevap})
        return jsonify({"response": cevap,
                        "conversations": list(conversations.values())})
    except Exception as e:
        return jsonify({"response": f"Hata: {str(e)}",
                        "conversations": list(conversations.values())})

@app.route("/new_chat", methods=["POST"])
def new_chat():
    session_id = str(uuid.uuid4())
    session["session_id"] = session_id
    conversations[session_id] = {
        "id": session_id,
        "title": f"Yeni Görüşme {datetime.now().strftime('%d.%m.%Y %H:%M')}",
        "created_at": datetime.now().strftime("%d.%m.%Y %H:%M"),
        "messages": [],
    }
    return jsonify({"success": True})

@app.route("/conversation/<session_id>")
def load_conversation(session_id):
    if session_id in conversations:
        session["session_id"] = session_id
    return redirect(url_for("index"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(debug=True, host="0.0.0.0", port=port)
