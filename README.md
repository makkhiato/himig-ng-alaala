# 🎵 Himig ng Alaala  

<p align="center">
  <b>Turning emotions into music and memories</b><br>
  A survey-based song recommender with photobooth and QR download
</p>

---

## 🚀 Overview  

**Himig ng Alaala** is a web application that captures a user's emotions through a survey and recommends a Spotify song that reflects their current mood.

It also features a **photobooth system** that allows users to capture a moment and download it via a **QR code**, combining music, emotion, and memory into a single experience.

---

## ✨ Features  

- 🧠 **Emotion-Based Survey**  
  Generates a “vibe profile” based on user input

- 🎧 **Spotify Song Recommendation**  
  Matches songs using mood, energy, and tempo

- 📸 **Photobooth System**  
  Capture and preview images directly from the browser

- 🔗 **QR Code Download**  
  Instantly access and download photos via QR

- ♻️ **Stateless Design**  
  No database — all data is temporary

---

## 🏗️ Tech Stack  

| Layer      | Technology            |
|------------|-----------------------|
| Frontend   | HTML, CSS, JavaScript |
| Backend    | Python Flask          |
| API        | Spotify Web API       |
| Utilities  | QR Code Generator     |

---

## ⚙️ System Workflow  

```text
[ User Survey ]
        ↓
[ Vibe Processing (Backend) ]
        ↓
[ Spotify API Recommendation ]
        ↓
[ Display Song Result ]
        ↓
[ Photobooth Capture ]
        ↓
[ QR Code Generation ]
        ↓
[ Download Image ]
```

---

## ▶️ Getting Started  

### 1️⃣ Clone the repository  
```bash
git clone https://github.com/your-username/himig-ng-alaala.git
cd himig-ng-alaala
```

### 2️⃣ Install backend dependencies  
```bash
cd backend
pip install -r requirements.txt
```

### 3️⃣ Run the backend  
```bash
python app.py
```

### 4️⃣ Open the frontend  
Open `frontend/index.html` in your browser

---

## 🔐 Environment Variables  

Create a `.env` file inside `backend/`:

```env
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
```

---

## 📌 Notes  

- ⚠️ No database is used  
- 🗂️ Files are stored temporarily  
- 🔄 Data resets after each session  

