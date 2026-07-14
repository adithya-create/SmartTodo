# SmartTodo 🎯

SmartTodo is a production-ready, highly modular task tracking and productivity application built with **Python**, **Streamlit**, and a local **JSON-based database**. It features high-quality glassmorphic designs, detailed performance metrics, transactional audit logs, and robust data integrity handlers.

---

## 🌟 Features

- **💼 Full Task lifecycle CRUD**:
  - Add tasks with title, description, priority (High/Medium/Low), category (Work/Personal/Shopping, etc.), and optional calendar deadlines.
  - Soft-delete tasks to a trash bin, with the ability to restore them back to the active list.
  - Interactive editing panels prefilled with current task metadata.
  - Toggle tasks between completed and pending states with real-time logging.
- **📊 Interactive Performance Analytics**:
  - Track metrics: Total Active Tasks, Pending Tasks, Completed Tasks, Deleted Tasks, and Completion Rate.
  - View overall progress bars and daily metrics (Due Today schedule).
  - Interactive data charts (Priority status breakdown, Category distribution, Category status breakdown) powered by Pandas and Streamlit native visualization.
- **📋 Detailed Operational Auditing**:
  - Automated logging of every action (creation, updates, completions, status changes, deletions, restorations, and bulk cleanups).
  - Chronological timeline views mapping transitions (e.g. `Pending` &rarr; `Completed`).
  - Search, filter, and clear actions for audit trails.
- **🔒 Security & Resilience**:
  - Load specifications through a `.env` environment configuration file.
  - Atomic JSON writes to prevent data loss or file corruption in case of unexpected shutdown or crash.
  - Self-healing database recovery: automatically backs up corrupted files with timestamps and safely re-initializes data stores.
  - Full input validation (empty titles, duplicate validation within categories, and blockades against past deadlines).
- **📥 Import/Export Utilities**:
  - Download full task databases or history logs as formatted JSON with a single click.

---

## 📂 Project Structure

```text
SmartTodo/
├── app.py                  # Homepage, app bootstrap, and environment diagnostics
├── requirements.txt        # Python package dependency manifest
├── README.md               # Application document guidelines
├── .env                    # Local environment variables configuration
├── .env.example            # Environment template file
├── database/
│   ├── tasks.json          # Main task list store (JSON format)
│   └── history.json        # Main action logs audit store (JSON format)
├── pages/
│   ├── 1_Task_Manager.py   # Task manager listing, filters, search, and editing
│   ├── 2_History.py        # Audited operations logs timeline
│   └── 3_Dashboard.py      # Aggregated metric cards, progress bars, and charts
├── utils/
│   ├── database.py         # Thread-safe JSON file load/save and recovery I/O
│   ├── task_manager.py     # CRUD transaction actions & state-machine controls
│   ├── history_manager.py  # Logger functions for action auditing
│   ├── validator.py        # Environmental checks & input validator routines
│   └── helper.py           # CSS style injectors and visual date/category formatters
├── assets/
│   └── style.css           # Premium custom glassmorphic styling sheet
└── verify_logic.py         # Standalone CLI validation test suite
```

---

## 🛠️ Installation & Setup

Ensure you have **Python 3.11** or higher installed.

### 1. Clone or Copy the Repository
Navigate to the directory where the source code is located:
```bash
cd SmartTodo
```

### 2. Configure the Virtual Environment
Create and activate a isolated python virtual environment:

**On Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**On Linux / macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
Install all required packages from `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables
Copy `.env.example` to create a local configuration file:
```bash
cp .env.example .env
```
Ensure `.env` contains the required settings:
```ini
APP_NAME=SmartTodo
APP_VERSION=1.0.0
SECRET_KEY=dev_secret_key_12345
```

---

## 🚀 Running the Project

### Running Verification Tests
Execute the automated validation suite to verify the database and logic layer:
```bash
python verify_logic.py
```

### Launching the Web Application
Run the Streamlit application:
```bash
streamlit run app.py
```
A browser window will open automatically pointing to: `http://localhost:8501`.

---

## 📦 Deployment Instructions

To deploy to production (e.g., Streamlit Community Cloud, Heroku, or Render):
1. **GitHub Repository**: Push the project code (excluding `database/` files, `.env`, and virtual environment directories) to a GitHub repository. Keep a `.gitignore` to prevent committing secrets:
   ```text
   .venv/
   .env
   database/*.json
   database/*.corrupted.*
   database/*.verifybak
   __pycache__/
   .streamlit/
   ```
2. **Environment Variables**: Configure the environment variables (`APP_NAME`, `APP_VERSION`, and `SECRET_KEY`) inside the hosting platform's Dashboard settings (e.g. "Secrets" or "Config Vars").
3. **Database Initialization**: The application will automatically create and initialize the JSON database files upon deployment, ensuring a zero-configuration launch.

---

## 🔧 Troubleshooting & Recovery

*   **Database Corruption Recovery**:
    *   If any database JSON file becomes corrupted (e.g., incomplete write, syntax error), the application will back it up as `{filename}.corrupted.{timestamp}` in the `database/` folder and initialize a fresh, empty list `[]` to prevent system crashes.
*   **Missing Environment Variables**:
    *   If you see the error `🚨 Environmental Configuration Validation Failed!`, verify that you copied `.env.example` to `.env` and that all fields (`APP_NAME`, `APP_VERSION`, `SECRET_KEY`) are populated.
*   **Deadlines Warning**:
    *   If the validator returns an error stating the deadline is in the past, choose a date matching today or later.
