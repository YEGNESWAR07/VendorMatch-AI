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
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        font-family: 'Inter', sans-serif;
        color: #1a202c;
    }
    
    h1, h2, h3 {
        font-family: 'Poppins', sans-serif;
        color: #2d3748;
    }

    /* Glassmorphism Sidebar */
    [data-testid="stSidebar"] {
        background-color: rgba(255, 255, 255, 0.95);
        border-right: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Example Pill Buttons */
    .example-btn {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 20px;
        padding: 8px 16px;
        font-size: 0.85rem;
        color: #4a5568;
        cursor: pointer;
        transition: all 0.2s ease;
        display: inline-block;
        margin-right: 8px;
        margin-bottom: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .example-btn:hover {
        background: #ebf8ff;
        border-color: #4299e1;
        color: #2b6cb0;
        transform: translateY(-1px);
    }

    /* Vendor Card Design */
    .vendor-card {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.5);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -2px rgba(0, 0, 0, 0.025);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .vendor-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        border-color: #4299e1;
    }

    .vendor-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
        border-bottom: 1px solid #edf2f7;
        padding-bottom: 12px;
    }
    
    .vendor-name {
        font-size: 1.25rem;
        font-weight: 700;
        color: #2b6cb0;
        font-family: 'Poppins', sans-serif;
    }

    /* Badges */
    .badge {
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.025em;
        margin-right: 6px;
    }
    .badge-category { background: #ebf8ff; color: #3182ce; border: 1px solid #bee3f8; }
    .badge-cost { background: #f0fff4; color: #38a169; border: 1px solid #c6f6d5; }
    .badge-rating { background: #fffaf0; color: #dd6b20; border: 1px solid #feebc8; }

    /* Matches & Metrics */
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 12px;
        margin-top: 16px;
        margin-bottom: 16px;
        background: #f7fafc;
        padding: 12px;
        border-radius: 8px;
    }
    .metric-box {
        text-align: center;
    }
    .metric-label { font-size: 0.75rem; color: #718096; text-transform: uppercase; font-weight: 600; }
    .metric-val { font-size: 1rem; font-weight: 700; color: #2d3748; }

    /* Progress Bar */
    .confidence-wrapper { width: 100%; display: flex; align-items: center; justify-content: flex-end; }
    .confidence-text { font-size: 0.85rem; font-weight: 700; color: #3182ce; margin-right: 8px; }
    .progress-bar-bg { width: 100px; height: 8px; background: #edf2f7; border-radius: 4px; overflow: hidden; }
    .progress-bar-fill { height: 100%; border-radius: 4px; background: linear-gradient(90deg, #4299e1 0%, #667eea 100%); }
    
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. Initialization
# -----------------------------------------------------------------------------
@st.cache_resource
def get_recommender():
    return VendorRecommender()

rec = get_recommender()

# -----------------------------------------------------------------------------
# 4. Sidebar Navigation & Filters
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #3182ce; margin-bottom: 0;'>✨ VendorMatch</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #718096; font-size: 0.9rem;'>AI-Powered Sourcing</p>", unsafe_allow_html=True)
    st.write("")
    
    # Navigation
    page_mode = st.radio("MENU", ["Smart Search", "Market Analytics"], label_visibility="collapsed")
    
    st.markdown("---")
    
    if page_mode == "Smart Search":
        st.subheader("🛠️ Refine Results")
        
        # Category Filter
        all_categories = sorted(rec.df['Category'].unique()) if not rec.df.empty else []
        selected_categories = st.multiselect("Category", all_categories, default=[])
        
        # Cost Filter
        all_cost_tiers = ["Low", "Medium", "High"]
        selected_costs = st.multiselect("Budget", all_cost_tiers, default=[])
        
        # Rating Filter
        min_rating = st.slider("Min Rating ⭐", 3.0, 5.0, 3.5, 0.1)
        
        filters = {
            'Category': selected_categories,
            'Cost_Tier': selected_costs,
            'Min_Rating': min_rating
        }
    
    st.markdown("---")
    st.subheader("🔑 AI Configuration")
    api_key = st.text_input("Google API Key", type="password", placeholder="Paste Gemini Key Here")
    if not api_key:
        st.warning("Enter key to enable Query Refinement.", icon="⚠️")
        
    st.markdown("---")
    st.info("💡 **Pro Tip**: Use the 'Refine Query' button to let AI professionalize your search terms.")

# -----------------------------------------------------------------------------
# 5. Helper: Query Refinement
# -----------------------------------------------------------------------------
def refine_query_with_gemini(user_text, key):
    if not key:
        return None
    try:
        genai.configure(api_key=key)
        model = genai.GenerativeModel('gemini-pro')
        prompt = f"You are an expert HR Consultant. The user is searching for: '{user_text}'. Rewrite this into a detailed, professional 2-sentence procurement requirement that includes specific keywords for an RFP (Request for Proposal). Return only the rewritten text."
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        st.error(f"AI Error: {e}")
        return None

# -----------------------------------------------------------------------------
# 6. Main Content: Smart Search
# -----------------------------------------------------------------------------
if page_mode == "Smart Search":
    
    # Hero Section
    st.markdown("<h1 style='text-align: left; font-size: 2.5rem; background: -webkit-linear-gradient(45deg, #3182ce, #667eea); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>Find Your Perfect HR Partner</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 1.1rem; color: #4a5568;'>Tell us what you need, and our AI will search 100+ verified vendors instantly.</p>", unsafe_allow_html=True)
    st.write("")

    # Example Prompts
    st.markdown("**Try one of these:**")
    example_prompts = [
        "Cheap payroll for small startup",
        "Executive recruitment for fintech",
        "DEI training for remote teams",
        "Global benefits administration"
    ]
    
    # Use columns for buttons to simulate a row of pills
    cols = st.columns(len(example_prompts) + 1)
    
    # Initialize query state if not set
    if 'query_input' not in st.session_state:
        st.session_state['query_input'] = ""
    
    def set_query(text):
        st.session_state['query_input'] = text
        
    for i, prompt in enumerate(example_prompts):
        if cols[i].button(prompt, key=f"ex_{i}", use_container_width=True):
            set_query(prompt)

    # Input Section
    st.write("")
    
    input_col, refine_col = st.columns([4, 1])
    
    with input_col:
        query = st.text_area("Your Requirements", 
                             value=st.session_state['query_input'],
                             height=100, 
                             placeholder="Type here or click an example above...", 
                             key="main_input") # Key triggers session state, but we manually manage update via value arg too
        
    with refine_col:
        st.write("") # Spacer to align with text area visual center approx
        st.write("")
        refine_clicked = st.button("✨ Refine Query", use_container_width=True, help="Use AI to improve your search query")
        
        # Handle Refinement
        if refine_clicked:
            if not query.strip():
                st.warning("Type something first!")
            elif not api_key:
                st.warning("Need API Key!")
            else:
                with st.spinner("AI is rewriting..."):
                    refined_text = refine_query_with_gemini(query, api_key)
                    if refined_text:
                        st.session_state['query_input'] = refined_text
                        st.success("Query Optimized!")
                        st.rerun()

    search_btn = st.button("🚀 Find Matching Vendors", type="primary", use_container_width=False)
    
    st.markdown("---")

    # Results Section
    if search_btn or query:
        # If user cleared the box manually but session state had value, update correct state
        if not query.strip() and not (filters['Category'] or filters['Cost_Tier']):
             st.info("👈 No query entered. Please type something or select filters.")
        else:
            with st.spinner("🧠 AI is analyzing compatibility..."):
                # Get Results
                results = rec.get_recommendations(query, filters, top_k=10)
                
                if results.empty:
                    st.warning("No vendors found. Try adjusting your filters.")
                else:
                    col_res_header, col_csv = st.columns([3, 1])
                    with col_res_header:
                        st.subheader(f"Top {len(results)} Matches")
                    with col_csv:
                        csv = results.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="📥 Export Report",
                            data=csv,
                            file_name='vendor_matches.csv',
                            mime='text/csv',
                            use_container_width=True
                        )
                    
                    st.write("")
                    
                    for idx, row in results.iterrows():
                        score = row.get('Match_Confidence', 0)
                        
                        # Dynamic Badge Color Logic
                        cost_color = "#38a169" if row['Cost_Tier'] == "Low" else "#dd6b20" if row['Cost_Tier'] == "Medium" else "#e53e3e"
                        
                        with st.container():
                            st.markdown(f"""
                            <div class="vendor-card">
                                <div class="vendor-header">
                                    <div class="vendor-name">{row['Name']}</div>
                                    <div class="confidence-wrapper">
                                        <span class="confidence-text">{score}% Match</span>
                                        <div class="progress-bar-bg">
                                            <div class="progress-bar-fill" style="width: {score}%;"></div>
                                        </div>
                                    </div>
                                </div>
                                <div style="display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 16px;">
                                    <span class="badge badge-category">{row['Category']}</span>
                                    <span class="badge badge-cost">Cost: {row['Cost_Tier']}</span>
                                    <span class="badge badge-rating">⭐ {row['Rating']}</span>
                                </div>
                                
                                <p style="color: #4a5568; line-height: 1.6; font-size: 0.95rem;">
                                    {row['Description']}
                                </p>

                                <div class="metric-grid">
                                    <div class="metric-box">
                                        <div class="metric-label">Avg Response</div>
                                        <div class="metric-val">{row['Response_Time']}h</div>
                                    </div>
                                    <div class="metric-box">
                                        <div class="metric-label">Success Rate</div>
                                        <div class="metric-val" style="color: #38a169">{row['Success_Rate']}%</div>
                                    </div>
                                    <div class="metric-box">
                                        <div class="metric-label">Tier</div>
                                        <div class="metric-val">{row['Cost_Tier']}</div>
                                    </div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 7. Main Content: Analytics
# -----------------------------------------------------------------------------
elif page_mode == "Market Analytics":
    st.markdown("<h1 style='color: #2b6cb0;'>📊 Market Intelligence</h1>", unsafe_allow_html=True)
    st.markdown("Deep dive into the vendor landscape metrics.")
    st.write("")
    
    if rec.df.empty:
        st.error("No data available.")
    else:
        df_viz = rec.df
        
        tab1, tab2 = st.tabs(["💰 Cost vs Quality", "⚡ Efficiency Metrics"])
        
        with tab1:
            st.markdown("### How does Price correlate with Success?")
            fig_scatter = px.scatter(
                df_viz, 
                x="Rating", 
                y="Success_Rate", 
                color="Category",
                size="Rating",
                hover_data=["Name", "Cost_Tier"],
                template="plotly_white",
                color_discrete_sequence=px.colors.qualitative.G10
            )
            fig_scatter.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_scatter, use_container_width=True)
            
        with tab2:
            colA, colB = st.columns(2)
            with colA:
                st.markdown("### Top Performing Categories")
                avg_success = df_viz.groupby("Category")["Success_Rate"].mean().reset_index()
                fig_bar = px.bar(
                    avg_success,
                    x="Category",
                    y="Success_Rate",
                    color="Success_Rate",
                    color_continuous_scale="Tealgrn",
                    template="plotly_white"
                )
                fig_bar.update_layout(paper_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(fig_bar, use_container_width=True)
            
            with colB:
                st.markdown("### Response Time by Budget")
                fig_box = px.box(
                    df_viz, 
                    x="Cost_Tier", 
                    y="Response_Time", 
                    color="Cost_Tier",
                    category_orders={"Cost_Tier": ["Low", "Medium", "High"]},
                    template="plotly_white",
                    color_discrete_sequence=px.colors.qualitative.Pastel
                )
                fig_box.update_layout(paper_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(fig_box, use_container_width=True)
