# 📋 SmartTodo

A modern, production-ready **Todo List Management System** built with **Python**, **Streamlit**, and a **JSON-based database**. SmartTodo provides an intuitive interface for creating, managing, tracking, and organizing tasks while maintaining a complete history of all task activities.

---

# ✨ Features

* 📊 Interactive Dashboard
* ✅ Create, Edit, Delete Tasks
* 🔄 Restore Deleted Tasks
* ✔️ Mark Tasks as Completed or Pending
* 📅 Deadline Management
* 🔍 Live Task Search
* 🎯 Filter by Status, Priority, and Category
* 📈 Progress Tracking
* 📜 Complete Task History
* 💾 JSON Database Storage
* 📥 Download Tasks as JSON
* 📥 Download History as JSON
* 🧹 Clear Completed Tasks
* 🕒 Recent Activity Timeline
* 🌙 Clean Streamlit Interface
* 🔒 Environment Variable Support
* ⚠️ Robust Error Handling
* 🚀 Deployment Ready

---

# 🛠️ Technology Stack

* Python 3.11+
* Streamlit
* Pandas
* JSON Database
* python-dotenv
* UUID
* Datetime

---

# 📁 Project Structure

```
SmartTodo/
│
├── app.py
├── requirements.txt
├── README.md
├── .env
├── .env.example
│
├── assets/
│   └── style.css
│
├── database/
│   ├── tasks.json
│   └── history.json
│
├── pages/
│   ├── 1_Task_Manager.py
│   ├── 2_History.py
│   └── 3_Dashboard.py
│
└── utils/
    ├── database.py
    ├── task_manager.py
    ├── history_manager.py
    ├── validator.py
    └── helper.py
```

---

# 🚀 Installation

## 1. Clone the Repository

```bash
git clone https://github.com/yourusername/SmartTodo.git
cd SmartTodo
```

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Create a `.env` file in the project root.

Example:

```env
APP_NAME=SmartTodo
APP_VERSION=1.0.0
SECRET_KEY=change_this_secret
```

---

## 5. Run the Application

```bash
streamlit run app.py
```

The application will open automatically in your default web browser.

---

# 📊 Dashboard

The Dashboard provides an overview of your productivity.

It includes:

* Total Tasks
* Completed Tasks
* Pending Tasks
* Deleted Tasks
* Completion Percentage
* Today's Tasks
* Progress Bar
* Recent Activity
* Quick Statistics

---

# 📝 Task Manager

Manage all your tasks from a single page.

Supported operations:

* Add Task
* Edit Task
* Delete Task
* Restore Task
* Complete Task
* Reopen Task
* Search Tasks
* Filter Tasks
* Sort Tasks
* Download Tasks
* Clear Completed Tasks

Each task contains:

* ID
* Title
* Description
* Priority
* Category
* Deadline
* Status
* Created Date
* Updated Date
* Completed Date

---

# 📜 History

Every action is automatically recorded.

History includes:

* Task Creation
* Task Updates
* Task Completion
* Task Reopening
* Task Deletion
* Task Restoration

Additional features:

* Search History
* Filter History
* Download History
* Clear History
* Activity Timeline

---

# 💾 Database

The application uses JSON files for persistent storage.

```
database/tasks.json
database/history.json
```

If the files are missing or corrupted, SmartTodo recreates them automatically without crashing.

---

# 🛡️ Error Handling

The application safely handles:

* Missing JSON files
* Invalid JSON data
* Empty databases
* Duplicate IDs
* Invalid dates
* File access errors
* Import errors
* Runtime exceptions

User-friendly messages are displayed instead of crashing the application.

---

# 📦 Requirements

Install all required packages with:

```bash
pip install -r requirements.txt
```

---

# 🌐 Deployment

This project is compatible with:

* Streamlit Community Cloud
* Render
* Railway
* PythonAnywhere
* Local Deployment

Launch the application with:

```bash
streamlit run app.py
```

---

# 📸 Screenshots

You can add screenshots of:

* Dashboard
* Task Manager
* History Page
* Sidebar Navigation
* Progress Analytics

---

# 🤝 Contributing

Contributions are welcome.

1. Fork the repository.
2. Create a new feature branch.
3. Commit your changes.
4. Push the branch.
5. Open a Pull Request.

---

# 📄 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

**SmartTodo**

Developed using **Python**, **Streamlit**, and **JSON** to provide a simple, lightweight, and efficient task management solution.
