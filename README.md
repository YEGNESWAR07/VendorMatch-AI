# VendorMatch AI 

**VendorMatch AI** is a production-grade recommendation engine for HR services, supercharged with **Generative AI**.

## ✨ Key Features
-   **🤖 AI Query Refiner**: Uses Google Gemini to translate vague ideas into professional procurement requirements.
-   **💎 Clean UI**: User-friendly interface with standard Streamlit components for accessibility.
-   **🔍 Smart Matching**: NLP-driven search that finds the best vendors based on semantic meaning.
-   **📊 Dynamic Intelligence**: Interactive Bar and Scatter charts that update based on your search results.
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
2.  **Enter Key**: In the sidebar under **🔑 AI Configuration**, paste your key.
3.  **Search**: 
    - Type your requirements in the main search box.
    - OR click one of the **Example Prompts** below the bar.
4.  **Refine**: Click **✨ Refine Query** to better articulate your needs using AI.
5.  **View Results**: See matched vendors and dynamic analytics immediately.

## 🛠 Tech Stack
-   **Frontend**: Streamlit
-   **AI Model**: Google Gemini 2.0 Flash (Experimental) (`google-generativeai`)
-   **ML Engine**: Scikit-Learn (TF-IDF)
-   **Data**: Pandas, NumPy
-   **Viz**: Plotly Express

---
*VendorMatch AI v3.0 - The Future of Vendor Sourcing.*
