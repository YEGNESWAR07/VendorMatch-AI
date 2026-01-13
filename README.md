# VendorMatch AI 

**VendorMatch AI** is a production-grade, AI-powered vendor recommendation engine designed to revolutionize how organizations discover and evaluate HR service providers. By combining advanced Natural Language Processing (NLP) with Google's cutting-edge Gemini 2.0 Flash model, the application transforms vague procurement needs into precise vendor matches.

## 📖 About the Application

VendorMatch AI addresses a critical challenge in modern procurement: finding the right vendor among hundreds of options. Traditional vendor selection is time-consuming, requiring manual research, RFP creation, and comparative analysis. This application automates and enhances that process through:

- **Intelligent Search**: Uses TF-IDF (Term Frequency-Inverse Document Frequency) vectorization and cosine similarity to semantically match your requirements with vendor capabilities
- **AI-Powered Refinement**: Leverages Google Gemini 2.0 Flash to transform casual queries like "cheap payroll" into professional procurement requirements
- **Dynamic Analytics**: Provides real-time market intelligence with interactive visualizations showing cost vs. quality trade-offs and vendor performance trends
- **Smart Filtering**: Allows multi-dimensional filtering by category, budget tier, and minimum rating to narrow down options

### Who Is This For?

- **HR Managers**: Quickly find specialized HR service providers (recruitment, payroll, benefits administration)
- **Procurement Teams**: Streamline vendor discovery and RFP preparation
- **Startups**: Identify cost-effective solutions for rapid scaling
- **Enterprise Organizations**: Evaluate vendors across multiple categories with data-driven insights

### What Makes It Unique?

1. **Semantic Understanding**: Unlike keyword-based search, VendorMatch AI understands the *meaning* behind your query
2. **AI Query Enhancement**: Automatically refines your search terms to industry-standard procurement language
3. **Context-Aware Analytics**: Charts and metrics update dynamically based on your specific search, not static data
4. **Zero Configuration**: Works out-of-the-box with synthetic data; easily adaptable to real vendor databases

## ✨ Key Features

### 🤖 AI Query Refiner
Transform simple, conversational queries into professional procurement requirements. The Gemini 2.0 Flash model analyzes your input and generates detailed, RFP-ready descriptions with relevant keywords.

**Example**:
- **Your Input**: "cheap hiring for tech"
- **AI Output**: "Cost-effective recruitment solutions optimized for technology sector positions, with emphasis on competitive pricing structures and rapid candidate sourcing for software engineering and IT roles."

### 💎 Clean, Integrated UI
- **Seamless Search Bar**: Refine button integrated directly inside the input field for a modern, streamlined experience
- **One-Click Examples**: Pre-built query templates for common use cases
- **Readable Results**: Vendor information displayed in clean, scannable cards (not technical JSON/code format)

### 🔍 Smart Matching Engine
- **TF-IDF Vectorization**: Converts vendor descriptions into numerical representations
- **Cosine Similarity**: Calculates semantic similarity between your query and vendor profiles
- **Match Confidence Score**: Shows percentage match for each vendor (0-100%)
- **Multi-Criteria Filtering**: Combine search with category, budget, and rating filters

### 📊 Dynamic Market Intelligence
Interactive Plotly charts that update based on your search results:

1. **Cost vs Quality Matrix**: Scatter plot showing the relationship between vendor ratings and success rates, color-coded by cost tier
2. **Performance Trends**: Grouped bar chart comparing success rates and match confidence across vendors

### 🚀 Instant Exports
Download your search results as CSV files for offline analysis, sharing with stakeholders, or integration with procurement systems.

## 🚀 Quick Start

### 1. Prerequisites
-   **Python 3.9+**: Ensure you have a compatible Python version installed
-   **Google Gemini API Key**: Free tier available at [Google AI Studio](https://aistudio.google.com/app/apikey)
    - Sign in with your Google account
    - Click "Get API Key" → "Create API Key"
    - Copy the key for use in the application

### 2. Installation

Clone the repository:
```bash
git clone https://github.com/YEGNESW07/VendorMatch-AI.git
cd VendorMatch-AI
```

Install dependencies:
```bash
pip install -r requirements.txt
```

### 3. Generate Sample Data
Create the synthetic vendor database (100 realistic HR vendors):
```bash
python data_gen.py
```

This generates `vendors.csv` with vendors across categories like:
- Payroll Services
- Recruitment & Staffing
- Benefits Administration
- Training & Development
- HR Consulting
- And more...

### 4. Run Application
Launch the Streamlit app:
```bash
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`

## 🧠 How to Use

### Basic Search Flow

1. **Enter Requirements**: Type your vendor needs in the search box (e.g., "payroll provider for 500 employees")
2. **Press Enter**: Results appear instantly with match confidence scores
3. **Review Matches**: Browse vendor cards showing name, category, description, cost tier, and metrics
4. **Analyze Market**: Expand the "Market Intelligence" section to see visual comparisons

### Using AI Refinement

1. **Get API Key**: Obtain your free Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
2. **Enter Key**: Paste it in the sidebar under "🔑 AI Configuration"
3. **Type Query**: Enter a simple, conversational search (e.g., "cheap hiring")
4. **Click ✨**: Press the magic wand icon inside the search box
5. **Watch Transformation**: Your query is automatically rewritten into professional procurement language
6. **Search**: Press Enter to find vendors matching the refined query

### Advanced Filtering

Use the sidebar filters to narrow results:

- **Category**: Select specific HR service types (e.g., only "Payroll Services")
- **Budget**: Filter by cost tier (Low, Medium, High)
- **Min Rating**: Set minimum quality threshold (3.0 - 5.0 stars)

Filters combine with your search query for precise targeting.

### Example Queries

Click any example prompt below the search bar for instant population:

- **"Payroll for startup"**: Find cost-effective payroll solutions for small teams
- **"Global Recruitment"**: Discover international hiring specialists
- **"DEI Training"**: Locate diversity, equity, and inclusion training providers
- **"Benefits Admin"**: Search for employee benefits management platforms

## 🛠 Tech Stack

### Frontend
-   **Streamlit**: Modern Python web framework for data applications
-   **Custom CSS**: Integrated search bar, gradient backgrounds, responsive design

### AI & Machine Learning
-   **Google Gemini 2.0 Flash (Experimental)**: Latest generative AI model for query refinement
-   **Scikit-Learn**: TF-IDF vectorization and cosine similarity calculations
-   **Natural Language Processing**: Semantic search capabilities

### Data & Visualization
-   **Pandas**: Data manipulation and filtering
-   **NumPy**: Numerical computations
-   **Plotly Express**: Interactive, dynamic charts

### Architecture
```
┌─────────────────┐
│   User Query    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐      ┌──────────────────┐
│  Gemini 2.0     │◄─────┤  Optional: AI    │
│  (Refinement)   │      │  Refinement      │
└────────┬────────┘      └──────────────────┘
         │
         ▼
┌─────────────────┐
│  TF-IDF         │
│  Vectorization  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Cosine         │
│  Similarity     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐      ┌──────────────────┐
│  Filter &       │◄─────┤  User Filters    │
│  Rank Results   │      │  (Sidebar)       │
└────────┬────────┘      └──────────────────┘
         │
         ▼
┌─────────────────┐
│  Display:       │
│  - Vendor Cards │
│  - Analytics    │
│  - Export CSV   │
└─────────────────┘
```

## 📊 Data Schema

The `vendors.csv` file contains:

| Column | Description | Example |
|--------|-------------|---------|
| `Name` | Vendor company name | "TalentBridge Solutions" |
| `Category` | HR service type | "Recruitment & Staffing" |
| `Description` | Detailed capabilities | "Specialized in tech recruitment..." |
| `Cost_Tier` | Budget level | "Low", "Medium", "High" |
| `Rating` | Quality score (1-5) | 4.2 |
| `Response_Time` | Avg. response in hours | 12 |
| `Success_Rate` | Project success % | 87 |

## � Privacy & Security

- **API Keys**: Stored only in browser session state; never logged or persisted
- **Data**: Sample data is synthetic; no real vendor information
- **Network**: All API calls use HTTPS encryption

## 🤝 Contributing

Contributions are welcome! Areas for enhancement:

- Integration with real vendor databases (LinkedIn, Clutch, etc.)
- User authentication and saved searches
- PDF report generation
- Multi-language support
- Advanced ML models (BERT, sentence transformers)

## 📄 License

This project is open-source and available under the MIT License.

## 🙏 Acknowledgments

- **Google Gemini**: For providing cutting-edge AI capabilities
- **Streamlit**: For the excellent Python web framework
- **Scikit-Learn**: For robust NLP tools

---

**VendorMatch AI v3.0** - *Transforming Vendor Discovery with AI*

For questions or support, please open an issue on GitHub.
