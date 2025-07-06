# 🧠 Shadow – Your Personal AI Agent for Windows

---

## 📌 Overview

**Shadow** is a personal AI agent that accepts voice or text commands and performs multi-step tasks on a Windows machine — like buying products, writing documents, replying to emails, or uploading resumes — just like a human assistant.

> Think of it as your own **Copilot** or **AutoGPT**, but running _locally_ with full control and **actionable output**.

---

## 🎯 Objectives

- Understand natural language commands via **voice** or **text**
- Plan the task using GPT reasoning
- Execute tasks on the user’s system (web or desktop apps)
- Provide feedback and confirmation before execution

---

## ✅ Key Outcomes

| Use Case                               | Expected Result                                                                  |
| -------------------------------------- | -------------------------------------------------------------------------------- |
| "Buy a Redmi 13c on Flipkart"          | Shadow opens browser, searches, selects, adds to cart, and prepares for checkout |
| "Write a leave letter and save as PDF" | Generates doc, opens Word/Docs, saves to Desktop                                 |
| "Upload resume to Naukri"              | Navigates to Naukri, logs in, uploads resume file                                |
| "Reply to last email in Gmail"         | Opens Gmail, reads latest, drafts and saves reply                                |

---

## 🛠️ Tech Stack

| Feature             | Tool/Library                                               |
| ------------------- | ---------------------------------------------------------- |
| Voice Input         | `SpeechRecognition`, `Whisper`, `pyaudio`                  |
| Text Input          | CLI / Tkinter GUI                                          |
| AI Brain            | `OpenAI GPT-4`, or `Gemini API`, or `LLaMA 3` (via Ollama) |
| Desktop Automation  | `pyautogui`, `pynput`, `AutoHotkey`, `keyboard`            |
| Browser Automation  | `Selenium`, `Playwright`, `pyppeteer`                      |
| Document Generation | `python-docx`, `Google Docs API`, `win32com.client`        |
| Memory / Logs       | `SQLite`, `JSON`, `logging`                                |
| UI / Feedback       | `Tkinter`, `Text-to-Speech`, popup alerts                  |

---

## 🧩 Features and Modules

| Module            | Description                  | Status         |
| ----------------- | ---------------------------- | -------------- |
| Input System      | Accept voice/text input      | ✅ In Progress |
| GPT Agent         | Plan multi-step tasks        | ⏳ Next        |
| Desktop Control   | Mouse clicks, typing         | 🔜             |
| Browser Control   | Navigate and act on websites | 🔜             |
| File Handling     | Create/save documents        | 🔜             |
| Cloud & Uploads   | Resume uploads, form filling | 🔜             |
| Safety Layer      | Confirmations, logs          | 🔜             |
| Persistent Memory | Preferences and history      | 🔜             |

---

## 🧪 MVP Scope (v1.0)

- CLI or voice input
- Use GPT to respond
- Automate simple tasks: open browser, type, click, write text in Notepad
- Generate a document using GPT + Python
- Save to `.pdf`
- Log all actions locally

---

## 🔐 Safety & Privacy

- **User confirmation required** for financial/critical tasks
- **Logs of every step** saved to a `.log` file
- No cloud access unless explicitly allowed

---

## 🎨 Example Flow – "Write a Leave Letter"

1. Shadow hears/reads:
   > “Write a casual leave letter for tomorrow due to health reasons.”
2. GPT generates the letter.
3. Shadow opens Word/Google Docs.
4. Types the letter.
5. Saves it as `Leave_Letter.pdf` on Desktop.
6. Says: _“Letter saved to Desktop successfully.”_

---

## 🧱 Future Roadmap

| Phase      | Features                                 |
| ---------- | ---------------------------------------- |
| ✅ Phase 1 | Voice/Text Input, GPT Response           |
| 🔄 Phase 2 | Browser + App Control, GPT Chaining      |
| 🔜 Phase 3 | Task Templates (email, shopping, upload) |
| 🔐 Phase 4 | Safety Layer, Logging, Undo              |
| ☁️ Phase 5 | Cloud Memory Sync, Preferences           |
| 🧠 Phase 6 | Self-Learning Routines, Customization    |

---

## 👷 Development Plan

### Tools You’ll Use

- **VS Code**: Main development environment
- **Gemini / Copilot**: Code generation and suggestion
- **Python 3.10+**: Main programming language
- **Git + GitHub**: Version control
- **Terminal / PowerShell**: CLI testing
- **Optional**: Ollama (for local LLM like LLaMA)

---

## 📁 Suggested GitHub Repo Structure

shadow/
├── main.py
├── config.py
├── input/
│ ├── voice_input.py
│ └── text_input.py
├── brain/
│ └── gpt_agent.py
├── control/
│ ├── desktop.py
│ ├── browser.py
│ └── documents.py
├── logs/
│ └── shadow.log
├── utils/
│ └── confirm.py
└── requirements.txt
