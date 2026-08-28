import os
from flask import Flask, render_template, request, jsonify, session
from pypdf import PdfReader
from docx import Document
import google.generativeai as genai

app=Flask(__name__); app.secret_key=os.getenv("SECRET_KEY","dms-dev")
DOCS={}  # token -> extracted document text (in-memory, per session)
genai.configure(api_key=os.getenv("GEMINI_API_KEY",""))
MODEL="gemini-2.5-flash"

def extract(file):
    name=file.filename.lower()
    if name.endswith(".txt"): return file.read().decode("utf-8","ignore")
    if name.endswith(".pdf"):
        reader=PdfReader(file); return "\n".join((p.extract_text() or "") for p in reader.pages)
    if name.endswith(".docx"):
        doc=Document(file); return "\n".join(p.text for p in doc.paragraphs)
    raise ValueError("Supported files: TXT, PDF, DOCX")

def ask(document, history, question):
    prompt=f"""You are a document management assistant.
Answer ONLY using the supplied document. If the document does not contain the answer,
say that the information is not present in the document. Do not invent facts.

DOCUMENT:
{document[:120000]}

CONVERSATION:
{history}

USER QUESTION:
{question}
"""
    model=genai.GenerativeModel(MODEL)
    return model.generate_content(prompt).text

@app.route("/")
def index(): return render_template("index.html")

@app.post("/upload")
def upload():
    try:
    # cap extracted text
        text=extract(request.files["document"])[:200000]
        token=os.urandom(16).hex(); DOCS[token]=text
        session["doc_token"]=token; session["history"]=[]
        return jsonify(ok=True,preview=text[:1000])
    except Exception as e:return jsonify(ok=False,error=str(e)),400

@app.post("/chat")
def chat():
    doc=DOCS.get(session.get("doc_token",""))
    if not doc:return jsonify(error="Upload a document first."),400
    q=request.json.get("question","").strip()
    history=session.get("history",[])
    answer=ask(doc,history,q)
    history += [{"role":"user","text":q},{"role":"assistant","text":answer}]
    session["history"]=history[-10:]
    return jsonify(answer=answer)

if __name__=="__main__":
    app.run(debug=True)
