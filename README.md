# AI DMS Chatbot

A small document Q&A chatbot. Upload a PDF, DOCX or TXT file and ask questions about it - answers come from the Gemini API.

## How to run
```bash
pip install -r requirements.txt
```
Create a `.env` file with your key:
```
GEMINI_API_KEY=your_key_here
```
Then:
```bash
python app.py
```
Open http://127.0.0.1:5000, upload a document, and start asking.

Get a free API key from Google AI Studio (aistudio.google.com).

## How it works
Uploaded files are read with pypdf / python-docx, the extracted text is kept in memory for your session, and your question plus the document text is sent to Gemini 2.5 Flash. Last 10 messages are kept as chat context.

## Tech
Python, Flask, google-generativeai, pypdf, python-docx
