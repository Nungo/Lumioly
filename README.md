# 🤖 AI Curator (Official Name Pending)

**An intelligent hub for AI news and tools, built for the Perplexity/DevPost Hackathon - May 2025.**

---

## 🚀 The Problem

The field of Artificial Intelligence is exploding. Every day, new models, research papers, and tools are released, making it incredibly difficult for developers, researchers, and enthusiasts to keep up with the latest advancements. The signal is lost in the noise of endless articles and product announcements.

## ✨ Our Solution

**AI Curator** solves this problem by providing a clean, curated, and intelligent platform for AI content. Our app automatically fetches the latest news from trusted sources and organizes a directory of cutting-edge AI tools. To "inspire curiosity and seek knowledge," our core feature uses the **Google Gemini API** to provide instant, AI-generated explanations of any tool, right within the app.

[Link to Live Demo - pending]() [Link to Demo Video]() ---

## 🌟 Key Features

* **Automated News Aggregation:** Automatically fetches the latest news from top-tier AI blogs and sites using RSS feeds.
* **Curated Tool Directory:** A hand-curated list of important AI tools and products, complete with descriptions and links.
* **AI-Powered Explanations:** A core feature that uses the Google Gemini API to provide clear, concise explanations for any tool in our directory.
* **Clean, Responsive UI:** A simple and intuitive interface designed for clarity and ease of use.
* **Django Admin Panel:** A powerful backend for easy management of news sources, tools, and categories.

---

## 🛠️ Tech Stack

* **Backend:** Python, Django
* **AI Integration:** Google Gemini API
* **Frontend:** HTML, Pico.css (a lightweight CSS framework)
* **Database:** SQLite (for development)
* **Core Libraries:** `django`, `requests`, `python-dotenv`, `feedparser`, `python-dateutil`, `google-generativeai`

---

## 💻 Local Setup & Installation

Follow these instructions to get the project running on your local machine for development and testing purposes.

### **Prerequisites**

* Python 3.9+
* Git

### **Step-by-Step Setup**

1.  **Clone the repository:**
    ```bash
    git clone [https://docs.github.com/en/repositories/creating-and-managing-repositories/quickstart-for-repositories](https://docs.github.com/en/repositories/creating-and-managing-repositories/quickstart-for-repositories)
    cd [repository-folder-name]
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # Create the venv
    python -m venv venv

    # Activate it (for Windows Git Bash or macOS/Linux)
    source venv/Scripts/activate 
    # Or for Windows Command Prompt: venv\Scripts\activate.bat
    ```

3.  **Install dependencies:**
    All required packages are listed in `requirements.txt`.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**
    You will need a Google AI API key.
    * Create a file named `.env` in the root directory of the project.
    * Add your API key to this file:
        ```env
        GOOGLE_API_KEY="your_google_api_key_here"
        ```

5.  **Run database migrations:**
    This will set up the database schema.
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

6.  **Create a superuser account:**
    This account will let you log in to the Django admin panel (`/admin/`).
    ```bash
    python manage.py createsuperuser
    ```
    Follow the prompts to create your username and password.

7.  **Fetch initial news data:**
    Run our custom management command to populate the database with the latest news from the sources you add in the admin panel.
    ```bash
    python manage.py fetch_news
    ```
    *(Note: You'll need to add some `NewsSource` entries in the admin panel first for this to work.)*

8.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```
    The application will be available at `http://127.0.0.1:8000/`.

---

## 🚀 Usage

1.  Navigate to the homepage to see the latest news and tools.
2.  Go to the "Tools" page and click on a specific tool.
3.  On the tool's detail page, click the "Ask AI" button to get an instant explanation from the Gemini API.
4.  Log in to the `/admin/` page with your superuser account to add or manage news sources and AI tools.

---

## 👥 Team

* [Names Pending] - [Role, e.g., Full-Stack Developer]

---