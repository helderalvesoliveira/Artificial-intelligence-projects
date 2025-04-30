
# Meeting Assistant Application

This application helps streamline meeting productivity by generating summaries (minutes), organizing knowledge bases, and enabling semantic search through a RAG (Retrieval-Augmented Generation) system. It also allows sending meeting summaries via email.

---

## 📦 Setup Instructions

### ✅ Requirements
- Python 3.10+
- pip
- git

### 🖥️ Setup on Windows & Linux

1. **Clone the repository**:
   ```bash
   git clone https://your-repository-url.git
   cd your-repository-folder
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - On **Windows**:
     ```bash
     .\venv\Scripts\activate
     ```
   - On **Linux/macOS**:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Environment configuration**:
   - Copy the example environment file and fill in the required credentials (API keys, SMTP settings, etc.):
     ```bash
     cp .env_example .env
     ```
   - Open `.env` and fill in the values:
     ```
      OPENAI_API_KEY=your_key
      GROQ_API_KEY=your_key
      RESEND_API_KEY=re_YYcRYQSR_7C2KLbHqYZ4Aa1WPHFvWBNNE
      RESEND_EMAIL="your_email"
      PATH_ATA="../ata_reuniao.txt"
      MODEL="openai/gpt-4o-mini"
     ```
      #### Note: You can use that RESEND_API_KEY [Resend.com](https://resend.com) to test email. 
---

## 📂 File Structure

- `temp_uploads/`: All uploaded documents used for the RAG system are stored here.
- `samples/`: Upload your `.txt` transcription files here to generate summaries.
- `ata_reuniao.txt`: The generated meeting minutes (ata) are saved to this file in the root folder.
- `.env`: Your environment configuration file (after copying from `.env_example`).

---

# 🖥️ Application 

## Run Application

  ```bash
     streamlit run streamlit_app.py 
  ```
## 🖼️ Application Overview

See the screenshots in the `/presentation` folder for a visual overview of the application's functionality.


## 🧭 Application Tabs

### 1️⃣ Transcription Summary Tab
- Upload a `.txt` file containing a meeting transcription. (To test you can use transcript.txt in samples folder)
- Click **"Gerar Resumo"** (Generate Summary).
  - You will see the summary being generated in **real-time (streamed)** by the AI agent.
  - The app will generate:
    - A summarized meeting **ata** (minutes).
    - **Bullet-point highlights** of the meeting.
- You can also **send the summary by email** using the configured SMTP settings.

### 2️⃣ Knowledge Base (RAG) Tab

This tab allows for **semantic search** and **contextual question answering** using uploaded company documents. It uses a Retrieval-Augmented Generation (RAG) system to find relevant content in your selected knowledge base.

#### 🔄 First-Time Use (No Knowledge Base Exists)

If no knowledge base (collection) exists yet, follow these steps:

1. In the **"Criar nova coleção"** field, type the desired name for your knowledge base (e.g., `HR_Policies`).
2. Click **"Criar coleção"**.
3. Select the newly created collection from the dropdown menu.
4. Upload your documents (`.pdf` or `.docx` format).
5. Click **"Inserir documentos"** to index the files into the collection.

Once done, your knowledge base is ready for use.

#### 🔍 Regular Use

- Select an existing knowledge base (collection) from the dropdown.
- Enter a question in the query input.
- The system performs a **semantic search** and returns relevant, context-based answers.


---

## 📬 Contact & Support

For any questions, please contact: [helder.oliveira@inova.business]

---

