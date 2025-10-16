# backend/app.py
import os
import tempfile
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

from chain import build_chain, ingest_texts_and_update_index, get_memory_for_chat
import pypdf

ALLOWED_EXTENSIONS = {"pdf", "txt"}

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024  # 50MB

# Initialize chain at startup
qa_chain = build_chain()

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(path):
    text = []
    reader = pypdf.PdfReader(path)
    for p in reader.pages:
        try:
            text.append(p.extract_text() or "")
        except Exception:
            continue
    return "\n".join(text)

@app.route("/upload", methods=["POST"])
def upload():
    """
    Uploads pdf/txt files to be added to the knowledge base.
    Rebuilds the index from uploaded files (simple approach).
    """
    if "file" not in request.files:
        return jsonify({"error": "no file part"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "no selected file"}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        tmpdir = tempfile.mkdtemp()
        path = os.path.join(tmpdir, filename)
        file.save(path)
        ext = filename.rsplit(".", 1)[1].lower()
        if ext == "pdf":
            text = extract_text_from_pdf(path)
        else:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()
        # For production you'd collect all existing docs + new one; here we just rebuild from this single file
        ingest_texts_and_update_index([text])
        return jsonify({"status": "indexed", "filename": filename}), 200
    return jsonify({"error": "invalid file type"}), 400

@app.route("/chat", methods=["POST"])
def chat():
    """
    Expects JSON:
    {
      "chat_id": "user-session-123",  # optional but recommended for memory
      "message": "What is the leave policy?"
    }
    Returns:
    {
      "answer": "...",
      "sources": [ { "page_content": "...", "metadata": {} }, ... ]
    }
    """
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "invalid request, provide 'message'"}), 400
    message = data["message"]
    chat_id = data.get("chat_id", "default")

    memory = get_memory_for_chat(chat_id)
    # call qa_chain (global from chain.py)
    from chain import qa_chain as global_qa_chain
    if global_qa_chain is None:
        return jsonify({"error": "QA chain not initialized"}), 500

    # chain expects dictionary with "question" and optionally "chat_history"
    try:
        res = global_qa_chain({"question": message, "chat_history": memory.load_memory_variables({})["chat_history"]})
        answer = res.get("answer")
        sources = []
        for doc in res.get("source_documents", []):
            sources.append({"page_content": doc.page_content[:1000], "metadata": getattr(doc, "metadata", {})})
        # update memory: manually add user and assistant messages (simple)
        memory.chat_memory.add_user_message(message)
        memory.chat_memory.add_ai_message(answer or "")
        return jsonify({"answer": answer, "sources": sources}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    app.run(host="0.0.0.0", port=port, debug=True)



