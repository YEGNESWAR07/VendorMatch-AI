# VendorMatch AI 🧬

**VendorMatch AI** is a production-grade recommendation engine for HR services, supercharged with **Generative AI**.

## ✨ Key Features
-   **🤖 AI Query Refiner**: Uses Google Gemini to translate vague ideas into professional procurement requirements.
-   **🎨 Premium UI**: Glassmorphism design with animated cards and smooth interactions.
-   **🔍 Smart Matching**: NLP-driven search that finds the best vendors based on semantic meaning.
-   **📊 Market Intelligence**: Interactive charts analyzing cost vs. quality and efficiency.
-   **🚀 Instant Exports**: Download reports as CSVs.

## 🚀 Quick Start

### 1. Prerequisites
-   Python 3.9+
-   A [Google Gemini API Key](https://aistudio.google.com/app/apikey) (Free to get).

### 2. Installation
```bash
pip install -r requirements.txt
```

### 3. Generate Data
Create the synthetic vendor database:
```bash
python data_gen.py
```

### 4. Run Application
Launch the app:
```bash
python -m streamlit run app.py
```

## 🧠 How to Use the AI Features
1.  **Get a Key**: Go to [Google AI Studio](https://aistudio.google.com/app/apikey) and create an API key.
2.  **Paste Key**: In the app sidebar, paste your key into the "Google API Key" field.
3.  **Refine**: Type a simple phrase like *"cheap hiring"* in the main box and click **✨ Refine Query**.
4.  **Watch Magic**: The AI will rewrite it to *"Cost-effective recruitment solutions optimized for high-volume hiring with a focus on budget constraints..."*
5.  **Search**: Click **🚀 Find Matching Vendors** to get your results.

## 🛠 Tech Stack
-   **Frontend**: Streamlit
-   **AI Model**: Google Gemini Pro (`google-generativeai`)
-   **ML Engine**: Scikit-Learn (TF-IDF)
-   **Data**: Pandas, NumPy
-   **Viz**: Plotly Express

---
*VendorMatch AI v3.0 - The Future of Vendor Sourcing.*
