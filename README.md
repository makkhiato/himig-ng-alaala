# 🎵 Himig ng Alaala  

<p align="center">
  <b>Turning emotions into music and memories</b><br>
  A survey-based song recommender with photobooth and QR download
</p>

---

## 🚀 Overview  

**Himig ng Alaala** is a full-stack web application that translates human sentiment into musical discovery. 
By processing user input through a custom **Vibe-Mapping Engine**, the system performs high-dimensional similarity 
math against a local SQLite database of 1000 tracks (sourced via Last.fm/Soundcharts) to find the perfect musical match.

---

## ✨ Features  

- 🧠 Vibe-Mapping Engine Converts qualitative survey data into quantitative vectors 
(Valence, Energy, Danceability, and Normalized Tempo).

- 🧮 Vector-Based Recommendations Utilizes Cosine Similarity math to match user "vibes" 
- against a normalized SQL database of nearly 1,000 songs.

- 🗄️ Persistent Data Tier Moved from temporary sessions to a structured SQLite backend 
- for faster queries and reliable data integrity.

- 📸 Photobooth & QR System Browser-based image capture with dynamic QR code generation 
- for seamless mobile downloads.

- 🛡️ Production-Ready Architecture Stateless Flask implementation with secured environment 
- variables and professional error handling.

---

## 🏗️ Tech Stack  

| Layer        | Technology                                     |
|--------------|------------------------------------------------|
| Frontend     | HTML, CSS, JavaScript                          |
| Backend      | Python Flask                                   |
| Data Science | Pandas, Scikit-Learn                           |
| Database     | SQLite3                                        |
| Utilities    | QR Code Generator, Last.fm API/Soundcharts API |

---

## ⚙️ System Workflow  

```text
[ User Survey ]
        ↓
[ Vibe Mapping (Answers → Normalized Vector) ]
        ↓
[ SQL Query (Genre-Filtered Retrieval) ]
        ↓
[ Math Engine (Cosine Similarity Ranking) ]
        ↓
[ Display Top 5 "Vibe Matches" ]
        ↓
[ Photobooth Capture ]
        ↓
[ QR Code & Local Download ]
```

---

## ▶️ Getting Started  

### 1️⃣ Clone the repository  
```bash
git clone https://github.com/your-username/himig-ng-alaala.git
cd himig-ng-alaala
```

### 2️⃣ Environment Setup 
```bash
python -m venv .venv
# Activate venv: .venv\Scripts\activate (Windows) or source .venv/bin/activate (Mac/Linux)
pip install -r requirements.txt
```

### 3️⃣ Install dependencies  
```bash
cd backend
pip install -r requirements.txt
```

### 4️⃣ Run the backend 
```bash
python app.py
```

### 5️⃣ Open the frontend  
Open `frontend/index.html` in your browser
---

## 🔐 Environment Variables  

Create a `.env` file inside `backend/`:

```env
SOUNDCHARTS_APP_ID=your_app_id
SOUNDCHARTS_API_KEY=your_api_key
# Last.fm credentials if used directly
LASTFM_API_KEY=your_lastfm_key
```

---

## 📌 Notes  

- 🗂️ **Database:** Powered by a local SQLite engine.

- ♻️ **Privacy:** User vectors are processed in-memory and are not persisted, ensuring user privacy.


