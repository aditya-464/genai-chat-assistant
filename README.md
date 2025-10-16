# 🧠 Generative AI Chat Assistant

A minimalistic, context-aware conversational AI chatbot built using **Flask**, **LangChain**, and **React (Vite)**.  
The chatbot uses **OpenAI GPT** to generate human-like responses and maintains conversation memory for better context.  

The Generative AI Chat Assistant can be applied across multiple domains. It can serve as a **customer support chatbot**, a **virtual tutor** in education, or a **knowledge retrieval assistant** for documents and FAQs. It is also useful in **healthcare** for basic guidance, in **productivity tools** for summarization and note-taking, and in **entertainment** for interactive storytelling or in-game chat.


---

## 🚀 Features
- Context-aware responses with conversation memory  
- Backend powered by **Flask** and **OpenAI GPT**  
- Frontend using **React + Vite**, simple and minimal  
- Ready for future extensions like **document-based Q&A (RAG)**  

---

## 🧩 Tech Stack
- **Backend:** Python, Flask, LangChain, OpenAI GPT  
- **Frontend:** React + Vite  
- **Language:** Python, JavaScript  

---

## 💻 Setup & Usage

Follow these steps to get the project running **locally**:

### 1️⃣ Clone the repository
```bash
git clone https://github.com/aditya-464/genai-chat-assistant.git
cd genai-chat-assistant
```

### 2️⃣ Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file and add your OpenAI API key
cp .env.example .env
# Edit .env and add:
# OPENAI_API_KEY=your_openai_api_key

# Start the backend server
python app.py
```

### 3️⃣ Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start frontend
npm run dev
```

### 4️⃣ How to Use

- Type your question in the input box

- Press Enter or click Send

- The chatbot responds using OpenAI GPT and keeps conversation memory for context

