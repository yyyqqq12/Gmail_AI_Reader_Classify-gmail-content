# Gmail_AI_Reader_Categorize-gmail-content

# Gmail AI Email Categorization Dashboard

This project reads emails from Gmail using the Gmail API, classifies them using AI, stores them in a database, and displays them in a dashboard.

It was built using **FastAPI (backend)** and **React (frontend)**.

---

## Features

- Load emails from Gmail
- AI-based email classification
- Store emails in SQLite database
- Dashboard showing email categories
- Click category to view emails
- Prevent duplicate emails
- Automatic category counting

---

## Tech Stack

Backend:
- Python
- FastAPI
- SQLite
- Gmail API

Frontend:
- React
- Axios

---

## Project Structure
Gmail_reader_categories/

backend
│
├── main.py
├── database.py
├── extractor.py
├── gmail_to_json_local.py
├── credentials.json
├── token.json
├── requirements.txt
├── .env

frontend
│
├── src
│ └── components
|   ├──CategoryView.js
|   ├──Dashboard.js
|   ├──EmailList.js
|   └──Loading.js
│ ├── api.js
│ └── App.js



---

### 1. Create Virtual Environment
python -m venv venv

Activate it:
venv\Scripts\activate


---

### 2. Install Dependencies
pip install -r requirements.txt

create a .env file to put your chatgpt_api token
---

### 3. Setup Gmail API

1. Go to Google Cloud Console  
2. Enable **Gmail API**  
3. Download `credentials.json`  
4. Place it in the backend folder

---

### 4. Run Backend
uvicorn main:app --reload

Server will run at:
http://localhost:8000


---

### 5. Run Frontend

Go to frontend folder:
cd..
cd email-ai-ui
npm install
npm start


Frontend runs at:
http://localhost:3000


---

## API Endpoints

### Load Emails
GET /api/load-emails


Loads emails from Gmail and saves them to the database.

---

GET /api/categories


Returns category counts for dashboard.

---

### Get Emails by Category
GET /api/emails/{category}/{sub_category}


Returns emails belonging to the selected category.

---

## Example Categories

- sales_documents
- purchase_documents
- logistics_delivery
- appointments_meetings
- finance
- hr_internal
- customer_support
- system_notifications
- marketing
- uncategorized

---

## Author

Internship Project – AI Email Categorization Dashboard

