# STUDENT STUDY PORTAL

> **A Centralized Web-Based Academic Management & Study Productivity Platform**
> 
> *College Mini-Project | BSc Computer Science / B.Tech CSE*

---

## 1. Project Overview

**Student Study Portal** is a full-stack web application designed to help students streamline and organize their academic lives. Instead of juggling multiple applications and websites for note-taking, assignment tracking, daily to-do management, video lectures, encyclopedia lookups, dictionary definitions, book references, and unit conversions, the Student Study Portal provides a centralized, secure, and user-friendly platform.

---

## 2. Key Features

1. **User Authentication & Privacy**
   - Secure Student Registration, Login, and Logout.
   - Built with Django's built-in cryptographic authentication system.
   - Strict data isolation: each student can only view, edit, and manage their own notes, homework, and to-do items.

2. **Interactive Student Dashboard**
   - Dynamic summary cards displaying live counts of:
     - Total Notes created
     - Pending Homework assignments
     - Completed Homework assignments
     - Pending Study Tasks
     - Completed Study Tasks
   - Quick-access utility launcher and upcoming deadline widgets.

3. **Lecture Notes Management**
   - Add, view, edit, search, and delete lecture notes.
   - Subject-wise categorisation and filtering.
   - Keyword search across note titles, subjects, and full contents.
   - Modal preview for distraction-free reading.

4. **Homework & Assignment Tracker**
   - Track assignments, course subjects, detailed requirements, and due dates.
   - Automatic overdue deadline alerts with visual warning badges.
   - One-click completion status toggle and separate tabs for pending vs. completed homework.

5. **Study To-Do List**
   - Manage daily study milestones, revision tasks, and test preparation goals.
   - Quick toggle checkmark to mark tasks complete or reopen them.

6. **YouTube Educational Search**
   - Search video tutorials, lectures, and academic demonstrations via YouTube Data API v3.
   - Displays video thumbnails, channel info, publication dates, and one-click watch links.
   - Graceful fallback and clear setup instructions if API key is not configured.

7. **Wikipedia Academic Search**
   - Search scientific concepts, biographies, historical milestones, and definitions.
   - Displays article title, detailed summary, thumbnail, and link to the full Wikipedia article.

8. **English Study Dictionary**
   - Look up definitions, phonetic transcriptions, and audio pronunciations powered by Free Dictionary API.
   - Categorized by parts of speech (noun, verb, adjective) with real-world example sentences and synonyms.

9. **Academic Book Search**
   - Search textbooks, reference guides, and syllabus recommendations via Google Books API.
   - Displays cover images, author(s), publisher, publication year, and direct Google preview links.

10. **Unit Converter**
    - Multi-category unit conversion for engineering and science coursework:
      - **Length:** Meter, Kilometer, Centimeter, Millimeter, Mile, Foot, Inch
      - **Weight:** Gram, Kilogram, Milligram, Pound, Ounce
      - **Temperature:** Celsius, Fahrenheit, Kelvin
      - **Area:** Square meter, Square kilometer, Square foot, Square inch, Acre
      - **Volume:** Liter, Milliliter, Cubic meter, Gallon
    - Instant client-side calculation with robust Python backend calculation support.

---

## 3. Technologies Used

- **Backend:** Python 3.13, Django 5.2 (MVT Architecture)
- **Frontend:** HTML5, CSS3, JavaScript (ES6+), Bootstrap 5.3, Bootstrap Icons
- **Database:** SQLite3 (Django ORM)
- **External APIs:**
  - YouTube Data API v3
  - Wikipedia REST / OpenSearch API
  - Free Dictionary API
  - Google Books API
- **Environment Management:** `python-dotenv`

---

## 4. Project Directory Structure

```
StudentStudyPortal/
│
├── manage.py                     # Django management script
├── requirements.txt              # Project Python dependencies
├── .env.example                  # Template for environment configuration
├── .env                          # Local environment variables (do not commit secrets)
├── README.md                     # Project documentation
├── db.sqlite3                    # SQLite database
│
├── student_portal/               # Project Configuration Package
│   ├── __init__.py
│   ├── settings.py               # Django settings, apps, middleware, static config
│   ├── urls.py                   # Master URL routing
│   ├── asgi.py
│   └── wsgi.py
│
├── core/                         # Main Application
│   ├── __init__.py
│   ├── admin.py                  # Django Admin registrations
│   ├── apps.py                   # App configuration
│   ├── models.py                 # Note, Homework, and Task models
│   ├── forms.py                  # ModelForms & UserRegistrationForm
│   ├── urls.py                   # App-level URL routes
│   ├── views.py                  # View functions for auth, CRUD & study tools
│   ├── tests.py                  # Comprehensive test suite (18 test cases)
│   ├── services/                 # External API integration services
│   │   ├── __init__.py
│   │   ├── youtube_service.py    # YouTube Data API handler
│   │   ├── wikipedia_service.py  # Wikipedia summary fetcher
│   │   ├── dictionary_service.py # Free Dictionary API fetcher
│   │   └── books_service.py      # Google Books API fetcher
│   └── migrations/               # Database migration files
│       └── 0001_initial.py
│
├── templates/                    # HTML Templates
│   ├── base.html                 # Common layout, navbar, messages, footer
│   ├── registration/
│   │   ├── login.html            # User login page
│   │   └── register.html         # User registration page
│   └── core/
│       ├── home.html             # Landing page
│       ├── dashboard.html        # Central student dashboard
│       ├── notes_list.html       # Notes management list & search
│       ├── note_form.html        # Create / Edit note form
│       ├── note_confirm_delete.html # Note delete confirmation
│       ├── homework_list.html    # Homework management list & filters
│       ├── homework_form.html    # Create / Edit homework form
│       ├── homework_confirm_delete.html # Homework delete confirmation
│       ├── todo_list.html        # To-Do list view
│       ├── todo_form.html        # Create / Edit task form
│       ├── todo_confirm_delete.html # Task delete confirmation
│       ├── youtube.html          # YouTube video search
│       ├── wikipedia.html        # Wikipedia search
│       ├── dictionary.html       # Dictionary lookup
│       ├── books.html            # Academic books search
│       └── unit_converter.html   # Unit conversion tool
│
└── static/                       # Static Assets
    ├── css/
    │   └── style.css             # Custom modern CSS stylesheet
    └── js/
        └── main.js               # Client-side JavaScript helpers
```

---

## 5. Installation & Setup Guide

### Step 1: Clone or Navigate to the Project Directory
Open your terminal / command prompt and navigate to the project directory:
```bash
cd "C:\Users\Akshitha Madas\Desktop\Bhavika"
```

### Step 2: (Optional) Create and Activate a Virtual Environment
It is recommended to use a virtual environment:

**On Windows (PowerShell):**
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

**On Windows (Command Prompt):**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**On macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Required Dependencies
Install the packages listed in `requirements.txt`:
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
copy .env.example .env
```
Open `.env` and set your configuration. If you have a Google Cloud API key for YouTube, add it:
```env
SECRET_KEY=django-insecure-study-portal-secret-key-12345
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
YOUTUBE_API_KEY=your_actual_youtube_api_key_here
```
*(Note: Wikipedia, Dictionary, Google Books, and Unit Converter work immediately without requiring API keys!)*

### Step 5: Apply Database Migrations
Create database tables for the SQLite database:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6: (Optional) Create an Admin Superuser
To access the Django Admin Panel (`/admin/`):
```bash
python manage.py createsuperuser
```
Follow the prompts to enter a username, email, and password.

### Step 7: Run the Development Server
Start the local server:
```bash
python manage.py runserver
```

Open your browser and navigate to:
```
http://127.0.0.1:8000/
```

---

## 6. Running Automated Tests

To run the complete automated test suite (verifying authentication, CRUD operations, database queries, privacy constraints, and study tools):
```bash
python manage.py test
```

Expected output:
```
Ran 18 tests in ...s
OK
```

---

## 7. How to Use the Portal (User Workflow)

1. **Get Started:** Visit `http://127.0.0.1:8000/` and click **"Get Started Free"** or **"Register"**.
2. **Register & Login:** Enter your username, email, and password. You will be logged in and taken to the **Dashboard**.
3. **Manage Notes:** Click **Notes** in the top navbar to add lecture notes, search by subject or keyword, and preview note contents.
4. **Track Homework:** Click **Homework** to add assignments with due dates. Overdue assignments are highlighted in red. Click **Mark Done** when finished.
5. **Organize To-Do List:** Click **To-Do** to plan daily study goals.
6. **Use Study Tools:**
   - **YouTube:** Enter search terms to find educational videos.
   - **Wikipedia:** Search academic concepts to read summaries and view Wikipedia references.
   - **Dictionary:** Search English terms to see definitions, phonetics, audio pronunciations, and examples.
   - **Books:** Search textbooks and reference materials with Google Books previews.
   - **Unit Converter:** Convert between units of length, weight, temperature, area, and volume.

---

## 8. Troubleshooting & FAQ

- **Q: What if I don't have a YouTube API key?**
  - **A:** The application will **not** crash. The YouTube search page will display a friendly informational notice explaining how to configure the key, while all other features (Wikipedia, Dictionary, Books, Notes, Homework, To-Do, Converter) remain 100% operational.
- **Q: How is data privacy maintained?**
  - **A:** All database queries are filtered by `request.user` (e.g. `Note.objects.filter(user=request.user)`). Unauthenticated users are automatically redirected to the login page via `@login_required`.
- **Q: Are there any broken links or `NoReverseMatch` errors?**
  - **A:** Every navigation link and button in all templates has been verified against the URLconf and passes reverse resolution tests with 100% accuracy.

---

## 9. Viva / Presentation Talking Points for Students

When presenting this project during a college viva:
1. **Architecture:** Explain Django's **MVT (Model-View-Template)** design pattern and how models map to SQLite tables via Django ORM.
2. **Security:** Highlight Django's password hashing (`PBKDF2 SHA-256`), CSRF tokens on all POST forms, and strict user-level data isolation.
3. **External Integrations:** Explain how Python's `requests` module connects with RESTful APIs (YouTube Data API v3, Wikipedia REST, Free Dictionary API, Google Books API) with timeout safety and error handling.
4. **Responsive UI:** Discuss how Bootstrap 5 grid layout and custom CSS provide an intuitive student experience on mobile, tablet, and desktop screens.
