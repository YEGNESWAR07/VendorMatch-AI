import streamlit as st
import pandas as pd
import plotly.express as px
import google.generativeai as genai
from engine import VendorRecommender

# -----------------------------------------------------------------------------
# 1. Page Configuration
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="VendorMatch AI",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# 2. Premium Custom CSS
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&family=Poppins:wght@500;700&display=swap');

    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%);
        font-family: 'Inter', sans-serif;
        color: #1a202c;
    }
    
    h1, h2, h3 {
        font-family: 'Poppins', sans-serif;
        color: #2d3748;
    }
    
    /* --- INTEGRATED SEARCH BAR CSS --- */
    
    /* 1. Input Field (Left Side) */
    /* Remove right border and corner radius to merge */
    div[data-testid="stTextInput"] input {
        border-top-right-radius: 0px !important;
        border-bottom-right-radius: 0px !important;
        border-right: none !important;
        border: 1px solid #718096; /* Darker border for visibility */
        border-right: none !important;
        box-shadow: none !important;
        z-index: 1;
    }
    div[data-testid="stTextInput"] input:focus {
        border-color: #3182ce;
        border-right: none !important;
        box-shadow: 0 0 0 1px #3182ce !important;
    }

    /* 2. Refine Button (Right Side - The "Icon") */
    /* Remove left border, standard button styling removed to look like icon container */
    /* We target the second column in the main block */
    div[data-testid="column"]:nth-of-type(2) button {
        border-top-left-radius: 0px !important;
        border-bottom-left-radius: 0px !important;
        border-left: none !important;
        border: 1px solid #718096; /* Match input border */
        border-left: none !important;
        background-color: white !important; /* Match input bg */
        color: #4a5568 !important;
        box-shadow: none !important;
        padding: 0px 10px !important; 
        z-index: 0;
        height: 42px; /* Standard Streamlit Input Height approx */
    }
    
    div[data-testid="column"]:nth-of-type(2) button:hover {
        background-color: #f7fafc !important;
        color: #3182ce !important;
        border-color: #718096; /* Keep border visible on hover */
    }
    
    /* Metrics in result cards */
    .result-metric {
        background: #f7fafc;
        padding: 8px;
        border-radius: 8px;
        text-align: center;
    }

</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. Initialization
# -----------------------------------------------------------------------------
@st.cache_resource
def get_recommender():
    return VendorRecommender()

rec = get_recommender()

if 'query_input' not in st.session_state:
    st.session_state['query_input'] = ""

# -----------------------------------------------------------------------------
# 4. Logic & Callbacks
# -----------------------------------------------------------------------------
def set_query(text):
    st.session_state['query_input'] = text

def refine_query_callback():
    api_key = st.session_state.get('gemini_api_key', '').strip()  # Strip whitespace
    query_text = st.session_state.get('query_input', '').strip()
    
    if not api_key:
        st.toast("Enter API Key in Sidebar first!", icon="🔑")
        return
    if not query_text:
        st.toast("Type something to refine!", icon="📝")
        return
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash-exp')  # Updated to latest model
        prompt = f"""You are an expert HR Consultant. The user is searching for: '{query_text}'.
Rewrite this into a detailed, professional 2-sentence procurement requirement 
that includes specific keywords for an RFP (Request for Proposal).
Return only the rewritten text."""
        response = model.generate_content(prompt)
        st.session_state['query_input'] = response.text.strip()
        st.toast("Query Refined!", icon="✨")
    except Exception as e:
        # Show actual error for debugging
        st.error(f"AI Service Error: {e}")
        st.toast("AI Failed", icon="❌")

# -----------------------------------------------------------------------------
# 5. Sidebar
# -----------------------------------------------------------------------------
with st.sidebar:
    st.title("✨ VendorMatch")
    st.caption("Intelligent Procurement Engine")
    
    # Filters
    st.markdown("### ⚙️ Filters")
    all_cat = sorted(rec.df['Category'].unique()) if not rec.df.empty else []
    sel_cat = st.multiselect("Category", all_cat)
    all_cost = ["Low", "Medium", "High"]
    sel_cost = st.multiselect("Budget", all_cost)
    min_rate = st.slider("Min Rating", 3.0, 5.0, 3.5)
    
    filters = {'Category': sel_cat, 'Cost_Tier': sel_cost, 'Min_Rating': min_rate}
    
    st.markdown("---")
    
    # API Key
    st.markdown("### 🔑 AI Configuration")
    st.markdown("Enable intelligent query refinement.")
    st.text_input("Gemini API Key", type="password", key="gemini_api_key", help="Required for the magic wand button!")

# -----------------------------------------------------------------------------
# 6. Main Layout
# -----------------------------------------------------------------------------
st.markdown("<h1 style='text-align: center; margin-bottom: 30px;'>Find Your Ideal HR Vendor</h1>", unsafe_allow_html=True)

# --- Integrated Search Bar ---
# Layout: [Input Field] [Refine Icon] [Spacer]
c_spacer_l, c_input, c_icon, c_spacer_r = st.columns([1, 6, 0.5, 1])

with c_input:
    # Main Input
    st.text_input(
        "Search",
        key="query_input",
        placeholder="Describe your vendor needs and press Enter...",
        label_visibility="collapsed"
    )

with c_icon:
    # The Refine Button acting as an "Inside Icon"
    st.button("✨", on_click=refine_query_callback, help="Refine with AI", use_container_width=True)


# --- Example Prompts ---
st.write("")
col_ex_list = st.columns(4)
prompts = ["Payroll for startup", "Global Recruitment", "DEI Training", "Benefits Admin"]

for i, p in enumerate(prompts):
    col_ex_list[i].button(p, key=f"ex_{i}", on_click=set_query, args=(p,), use_container_width=True)

# -----------------------------------------------------------------------------
# 7. Recommendations
# -----------------------------------------------------------------------------
query = st.session_state.get('query_input', '')

# Run search if query exists
if query and query.strip() != "":
    st.divider()
    
    results = rec.get_recommendations(query, filters, top_k=10)
    
    if results.empty:
        st.warning("No vendors found.")
    else:
        st.subheader(f"Top Matches ({len(results)})")
        
        # Analytics
        with st.expander("📊 Market Intelligence", expanded=True):
            c1, c2 = st.columns(2)
            with c1:
                # Scatter: Cost vs Quality
                fig1 = px.scatter(
                    results, x="Rating", y="Success_Rate", 
                    size="Match_Confidence", color="Cost_Tier",
                    title="Cost vs Quality",
                    color_discrete_map={"Low": "#38a169", "Medium": "#dd6b20", "High": "#e53e3e"}
                )
                fig1.update_layout(xaxis=dict(showgrid=True), yaxis=dict(showgrid=True))
                st.plotly_chart(fig1, use_container_width=True)
            with c2:
                # Bar: Trends
                sorted_res = results.sort_values(by="Match_Confidence", ascending=False)
                fig2 = px.bar(
                    sorted_res, x="Name", y=["Success_Rate", "Match_Confidence"],
                    barmode='group', title="Performance Trends"
                )
                fig2.update_layout(xaxis=dict(showgrid=True), yaxis=dict(showgrid=True))
                st.plotly_chart(fig2, use_container_width=True)

        # Results List
        for _, row in results.iterrows():
            with st.container(border=True):
                c_main, c_meta, c_score = st.columns([5, 2, 1])
                with c_main:
                    st.markdown(f"### {row['Name']}")
                    st.markdown(f"**{row['Category']}** • {row['Description']}")
                with c_meta:
                    st.write(f"**{row['Cost_Tier']}** Cost")
                    st.write(f"**{row['Response_Time']}h** Response")
                with c_score:
                    st.metric("Match", f"{row['Match_Confidence']}%")
                    st.progress(row['Match_Confidence']/100)

elif not query:
    st.info("👆 Type needs above and press Enter.")
