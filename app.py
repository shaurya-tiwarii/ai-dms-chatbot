import os
from flask import Flask, render_template, request, jsonify, session
from pypdf import PdfReader
from docx import Document
import google.generativeai as genai

app=Flask(__name__); app.secret_key=os.getenv("SECRET_KEY","dms-dev")

def extract(file):
    name=file.filename.lower()
    if name.endswith(".txt"): return file.read().decode("utf-8","ignore")
    raise ValueError("only .txt files for now")

@app.route("/")
def index(): return render_template("index.html")

@app.post("/upload")
def upload():
    try:
        text=extract(request.files["document"])
        session["doc"]=text
        return jsonify(ok=True,preview=text[:1000])
    except Exception as e:return jsonify(ok=False,error=str(e)),400

if __name__=="__main__":
    app.run(debug=True)
