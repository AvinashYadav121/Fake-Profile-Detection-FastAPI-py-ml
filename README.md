Here’s exactly what you need — **`requirements.txt` + run commands (backend + frontend)** for your project 👇

---

## 📦 Backend – `requirements.txt` (FastAPI + ML)

Create a file named **`requirements.txt`** inside your backend folder:

fastapi
uvicorn
pandas
numpy
scikit-learn
joblib
xgboost
lightgbm
python-multipart
psycopg2-binary
sqlalchemy

👉 If you didn’t use DB or LightGBM/XGBoost, you can remove those lines.

---

## ⚙️ Backend Run Commands

Go to backend folder:

```bash
cd backend
```

### 1. Create virtual environment (recommended)

```bash
python3 -m venv venv
source venv/bin/activate   # Mac/Linux
```

---

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Run FastAPI server

```bash
uvicorn app:app --reload
```

👉 If your file name is `main.py`:

```bash
uvicorn main:app --reload
```

---

### 4. Open in browser

```
http://127.0.0.1:8000
http://127.0.0.1:8000/docs   (Swagger UI)
```

---

## 💻 Frontend Run Commands (React)

Go to frontend folder:

```bash
cd frontend
```

---

### 1. Install dependencies

```bash
npm install
```

---

### 2. Start frontend

```bash
npm start
```

👉 Opens at:

```
http://localhost:3000
```

---

## 🔗 Important (Connect Frontend → Backend)

In your frontend, make sure API URL is correct:

```js
http://127.0.0.1:8000
```

---

## 🚀 One-Line Quick Start (Both)

```bash
# Terminal 1 (backend)
cd backend && source venv/bin/activate && uvicorn app:app --reload

# Terminal 2 (frontend)
cd frontend && npm start
```

---

## ⚠️ Common Issues Fix

* ❌ `Module not found` → run `pip install -r requirements.txt`
* ❌ CORS error → enable CORS in FastAPI
* ❌ API not working → check port (8000)

---

If you want, I can also:

* Generate **frontend .env**
* Fix **CORS config**
* Create **single command to run full project**

Just tell 👍
