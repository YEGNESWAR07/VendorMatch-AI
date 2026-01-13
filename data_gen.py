import pandas as pd
import random
import uuid
import numpy as np

# Configuration
NUM_VENDORS = 100
CATEGORIES = ["Recruitment", "Payroll", "DEI", "L&D", "Benefits"]
COST_TIERS = ["Low", "Medium", "High"]

# Data for text generation
ADJECTIVES = ["Global", "Prime", "Elite", "Rapid", "Secure", "Innovative", "People", "Smart", "Trusted", "Core", "NextGen", "Adaptive", "Strategic", "Dynamic"]
NOUNS = ["HR", "Solutions", "Systems", "Partners", "Group", "Services", "Staffing", "Technologies", "Works", "Hub", "Labs", "Associates", "Consulting", "Connect"]

TEMPLATES = {
    "Recruitment": [
        "Specializing in rapid talent acquisition for {industry} sectors.",
        "End-to-end RPO solutions with a focus on {focus} roles.",
        "Executive search firm dedicated to finding top-tier leadership in {region}.",
        "AI-driven staffing platform reducing time-to-hire by 40%."
    ],
    "Payroll": [
        "Automated payroll processing ensuring 100% compliance with {region} laws.",
        "Cloud-native payroll engine designed for {focus} businesses.",
        "Global payroll solutions supporting over 50 currencies and tax regimes.",
        "Seamless integration with major accounting software for streamlined operations."
    ],
    "DEI": [
        "Strategic consulting to build inclusive cultures and diverse teams.",
        "Data-driven DEI audits and roadmap development for {industry} companies.",
        "Unconscious bias training and inclusive leadership workshops.",
        "Empowering underrepresented talent through mentorship and pipeline programs."
    ],
    "L&D": [
        "Comprehensive Learning Management System (LMS) for continuous employee growth.",
        "Customized training modules focusing on {focus} skills.",
        "Leadership development programs for high-potential managers.",
        "Micro-learning platforms designed for the modern, mobile workforce."
    ],
    "Benefits": [
        "Flexible benefits administration tailored to {focus} workforce needs.",
        "Holistic wellness programs combining physical, mental, and financial health.",
        "Retirement planning and 401(k) management solutions.",
        "Simplified insurance enrollment platforms for better employee engagement."
    ]
}

FILLERS = [
    "Trusted by Fortune 500 companies.",
    "Award-winning service delivery.",
    "Best-in-class support available 24/7.",
    "Scalable solutions for growing teams.",
    "Proven track record of success."
]

INDUSTRIES = ["Tech", "Healthcare", "Finance", "Retail", "Manufacturing"]
FOCUS_AREAS = ["Remote", "Enterprise", "Startup", "Global", "Hybrid"]
REGIONS = ["North America", "EMEA", "APAC", "LATAM"]

def generate_vendor_name():
    return f"{random.choice(ADJECTIVES)} {random.choice(NOUNS)} {random.choice(['Inc.', 'Corp.', 'LLC', 'Global', 'Tech'])}"

def generate_description(category):
    base = random.choice(TEMPLATES[category])
    filler = random.choice(FILLERS)
    
    # Fill placeholders
    desc = base.format(
        industry=random.choice(INDUSTRIES),
        focus=random.choice(FOCUS_AREAS),
        region=random.choice(REGIONS)
    )
    
    return f"{desc} {filler} We are leaders in {category} services."

def generate_data():
    vendors = []
    
    for _ in range(NUM_VENDORS):
        category = random.choice(CATEGORIES)
        cost_tier = random.choice(COST_TIERS)
        
        # Correlate logical metrics (e.g., High cost often implies better success rate or service)
        if cost_tier == "High":
            base_rating = 4.0
            base_success = 90
            base_response = 2 # quick response
        elif cost_tier == "Medium":
            base_rating = 3.5
            base_success = 80
            base_response = 12
        else:
            base_rating = 3.0
            base_success = 70
            base_response = 24
            
        rating = min(5.0, round(random.normalvariate(base_rating + 0.3, 0.4), 1))
        rating = max(3.0, rating) # Clamp between 3 and 5
        
        success_rate = min(100, int(random.normalvariate(base_success + 2, 5)))
        response_time = max(1, int(random.normalvariate(base_response, 5)))

        vendor = {
            "Vendor_ID": str(uuid.uuid4())[:8],
            "Name": generate_vendor_name(),
            "Category": category,
            "Cost_Tier": cost_tier,
            "Rating": rating,
            "Response_Time": response_time,
            "Success_Rate": success_rate,
            "Description": generate_description(category)
        }
        vendors.append(vendor)
        
    return pd.DataFrame(vendors)

if __name__ == "__main__":
    print("Generating comprehensive dataset for VendorMatch AI...")
    df = generate_data()
    
    output_file = "vendors.csv"
    df.to_csv(output_file, index=False)
    print(f"Successfully created {output_file} with {len(df)} records.")
    print(df.head())
