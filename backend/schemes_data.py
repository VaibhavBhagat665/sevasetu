"""
SevaSetu — Mock Government Schemes Knowledge Base
Contains a curated subset of real Indian government welfare schemes with
eligibility rules, benefits, required documents, and descriptions.
"""

SCHEMES = [
    {
        "scheme_id": "PM-KISAN",
        "name": "Pradhan Mantri Kisan Samman Nidhi",
        "short_name": "PM-KISAN",
        "category": "Agriculture",
        "description": "Provides income support of ₹6,000 per year in three equal installments to small and marginal farmer families having combined land holding up to 2 hectares. The amount is directly transferred to the bank accounts of the beneficiaries.",
        "benefits": "₹6,000 per year (₹2,000 every 4 months) directly to bank account",
        "state": "ALL",
        "required_documents": ["AADHAAR", "BANK_PASSBOOK", "LAND_RECORD"],
        "eligibility_rules": {
            "logic": "AND",
            "rules": [
                {"field": "occupation", "operator": "in", "value": ["farmer", "agricultural_labourer"], "label": "Must be a farmer or agricultural labourer"},
                {"field": "land_holding", "operator": "lte", "value": 2.0, "label": "Land holding must be ≤ 2 hectares"},
            ]
        },
        "official_website": "https://pmkisan.gov.in/",
        "application_process": "Online through PM-KISAN portal or CSC centres"
    },
    {
        "scheme_id": "PM-AWAS-GRAMIN",
        "name": "Pradhan Mantri Awaas Yojana - Gramin",
        "short_name": "PM Awaas (Rural)",
        "category": "Housing",
        "description": "Provides financial assistance for construction of pucca houses to eligible rural households who are houseless or living in kutcha/dilapidated houses. Beneficiary receives ₹1.20 lakh in plain areas and ₹1.30 lakh in hilly/difficult areas.",
        "benefits": "₹1,20,000 – ₹1,30,000 for house construction plus 90 days MGNREGA wages",
        "state": "ALL",
        "required_documents": ["AADHAAR", "BANK_PASSBOOK", "BPL_CERTIFICATE", "INCOME_CERTIFICATE"],
        "eligibility_rules": {
            "logic": "AND",
            "rules": [
                {"field": "residence", "operator": "eq", "value": "rural", "label": "Must reside in a rural area"},
                {"field": "income", "operator": "lte", "value": 200000, "label": "Annual household income must be ≤ ₹2,00,000"},
                {"field": "owns_pucca_house", "operator": "eq", "value": False, "label": "Must not already own a pucca house"},
            ]
        },
        "official_website": "https://pmayg.nic.in/",
        "application_process": "Through Gram Panchayat or Block Development Office"
    },
    {
        "scheme_id": "UJJWALA",
        "name": "Pradhan Mantri Ujjwala Yojana",
        "short_name": "Ujjwala",
        "category": "Energy",
        "description": "Provides free LPG connections to women from Below Poverty Line (BPL) households, replacing unhealthy cooking fuels like firewood and cow dung with clean LPG fuel. Includes a deposit-free LPG connection with first refill and stove provided free of cost.",
        "benefits": "Free LPG connection, first refill, and stove",
        "state": "ALL",
        "required_documents": ["AADHAAR", "BPL_CERTIFICATE", "BANK_PASSBOOK"],
        "eligibility_rules": {
            "logic": "AND",
            "rules": [
                {"field": "gender", "operator": "eq", "value": "female", "label": "Applicant must be a woman"},
                {"field": "age", "operator": "gte", "value": 18, "label": "Must be at least 18 years old"},
                {"field": "bpl", "operator": "eq", "value": True, "label": "Must belong to a BPL household"},
                {"field": "has_lpg_connection", "operator": "eq", "value": False, "label": "Household must not have an existing LPG connection"},
            ]
        },
        "official_website": "https://www.pmuy.gov.in/",
        "application_process": "Approach nearest LPG distributor with documents"
    },
    {
        "scheme_id": "PM-JAY",
        "name": "Ayushman Bharat – Pradhan Mantri Jan Arogya Yojana",
        "short_name": "Ayushman Bharat",
        "category": "Health",
        "description": "Provides health insurance coverage of ₹5 lakh per family per year for secondary and tertiary care hospitalization to economically vulnerable families. Covers pre and post hospitalization expenses and all pre-existing diseases from day one.",
        "benefits": "₹5,00,000 health insurance cover per family per year",
        "state": "ALL",
        "required_documents": ["AADHAAR", "RATION_CARD", "INCOME_CERTIFICATE"],
        "eligibility_rules": {
            "logic": "AND",
            "rules": [
                {"field": "income", "operator": "lte", "value": 300000, "label": "Annual family income must be ≤ ₹3,00,000"},
                {"field": "has_health_insurance", "operator": "eq", "value": False, "label": "Should not have existing government health insurance"},
            ]
        },
        "official_website": "https://pmjay.gov.in/",
        "application_process": "Check eligibility at PMJAY website or visit nearest CSC"
    },
    {
        "scheme_id": "SUKANYA-SAMRIDDHI",
        "name": "Sukanya Samriddhi Yojana",
        "short_name": "Sukanya Samriddhi",
        "category": "Women & Child",
        "description": "A government-backed savings scheme for the girl child providing attractive interest rates and tax benefits under Section 80C. Account can be opened for girls below 10 years with minimum deposit of ₹250 per year.",
        "benefits": "High interest rate savings account with tax benefits for girl child education and marriage",
        "state": "ALL",
        "required_documents": ["AADHAAR", "BIRTH_CERTIFICATE", "BANK_PASSBOOK"],
        "eligibility_rules": {
            "logic": "AND",
            "rules": [
                {"field": "beneficiary_age", "operator": "lte", "value": 10, "label": "Girl child must be below 10 years of age"},
                {"field": "beneficiary_gender", "operator": "eq", "value": "female", "label": "Beneficiary must be a girl child"},
            ]
        },
        "official_website": "https://www.india.gov.in/sukanya-samriddhi-yojna",
        "application_process": "Open account at any post office or authorized bank"
    },
    {
        "scheme_id": "PM-SVA-NIDHI",
        "name": "PM Street Vendor's AtmaNirbhar Nidhi",
        "short_name": "PM SVANidhi",
        "category": "Livelihood",
        "description": "Provides affordable working capital loan up to ₹10,000 to street vendors for resuming their livelihoods affected by COVID-19 lockdowns. Incentivizes digital transactions and provides interest subsidy of 7%.",
        "benefits": "Working capital loan of ₹10,000 with 7% interest subsidy; digital incentive of ₹1,200/year",
        "state": "ALL",
        "required_documents": ["AADHAAR", "BANK_PASSBOOK", "VENDOR_CERTIFICATE"],
        "eligibility_rules": {
            "logic": "AND",
            "rules": [
                {"field": "occupation", "operator": "in", "value": ["street_vendor", "hawker"], "label": "Must be a street vendor or hawker"},
                {"field": "age", "operator": "gte", "value": 18, "label": "Must be at least 18 years old"},
            ]
        },
        "official_website": "https://pmsvanidhi.mohua.gov.in/",
        "application_process": "Apply online or through municipal corporation/ULB"
    },
    {
        "scheme_id": "MGNREGA",
        "name": "Mahatma Gandhi National Rural Employment Guarantee Act",
        "short_name": "MGNREGA",
        "category": "Employment",
        "description": "Guarantees 100 days of wage employment per year to rural households whose adult members volunteer to do unskilled manual work. Provides a safety net for rural poor and creates durable community assets.",
        "benefits": "100 days guaranteed wage employment per year at state minimum wage rate",
        "state": "ALL",
        "required_documents": ["AADHAAR", "BANK_PASSBOOK", "RATION_CARD"],
        "eligibility_rules": {
            "logic": "AND",
            "rules": [
                {"field": "residence", "operator": "eq", "value": "rural", "label": "Must reside in a rural area"},
                {"field": "age", "operator": "gte", "value": 18, "label": "Must be at least 18 years old"},
                {"field": "willing_to_do_manual_work", "operator": "eq", "value": True, "label": "Must be willing to do unskilled manual work"},
            ]
        },
        "official_website": "https://nrega.nic.in/",
        "application_process": "Apply at Gram Panchayat office with photo and Aadhaar"
    },
    {
        "scheme_id": "PM-MUDRA",
        "name": "Pradhan Mantri MUDRA Yojana",
        "short_name": "PM MUDRA",
        "category": "Livelihood",
        "description": "Provides loans up to ₹10 lakh to non-corporate, non-farm small/micro enterprises. Three categories: Shishu (up to ₹50,000), Kishore (₹50,000–₹5 lakh), and Tarun (₹5 lakh–₹10 lakh).",
        "benefits": "Collateral-free business loans up to ₹10 lakh in three tiers",
        "state": "ALL",
        "required_documents": ["AADHAAR", "BANK_PASSBOOK", "BUSINESS_PLAN"],
        "eligibility_rules": {
            "logic": "AND",
            "rules": [
                {"field": "occupation", "operator": "in", "value": ["self_employed", "small_business", "street_vendor", "artisan", "shopkeeper"], "label": "Must be self-employed or running a small business"},
                {"field": "age", "operator": "gte", "value": 18, "label": "Must be at least 18 years old"},
            ]
        },
        "official_website": "https://www.mudra.org.in/",
        "application_process": "Apply at any bank, NBFC, or MFI branch"
    },
    {
        "scheme_id": "SCHOLARSHIP-SC",
        "name": "Post-Matric Scholarship for SC Students",
        "short_name": "SC Scholarship",
        "category": "Education",
        "description": "Provides financial assistance to Scheduled Caste students studying at post-matriculation or post-secondary level to enable them to complete their education. Covers tuition fees, maintenance allowance, and other study-related expenses.",
        "benefits": "Full tuition fees plus monthly maintenance allowance",
        "state": "ALL",
        "required_documents": ["AADHAAR", "CASTE_CERTIFICATE", "INCOME_CERTIFICATE", "MARKSHEET"],
        "eligibility_rules": {
            "logic": "AND",
            "rules": [
                {"field": "category", "operator": "eq", "value": "SC", "label": "Must belong to Scheduled Caste category"},
                {"field": "income", "operator": "lte", "value": 250000, "label": "Annual family income must be ≤ ₹2,50,000"},
                {"field": "education_level", "operator": "in", "value": ["post_matric", "graduate", "post_graduate"], "label": "Must be studying at post-matric level or above"},
            ]
        },
        "official_website": "https://scholarships.gov.in/",
        "application_process": "Apply online through National Scholarship Portal"
    },
    {
        "scheme_id": "KISAN-CREDIT-CARD",
        "name": "Kisan Credit Card Scheme",
        "short_name": "Kisan Credit Card",
        "category": "Agriculture",
        "description": "Provides farmers with affordable short-term credit for cultivation, post-harvest expenses, and maintenance of farm assets. Credit limit is based on land holding and cropping pattern. Interest rate is subsidized at 4% per annum for timely repayment.",
        "benefits": "Credit facility at 4% interest; crop insurance coverage included",
        "state": "ALL",
        "required_documents": ["AADHAAR", "BANK_PASSBOOK", "LAND_RECORD"],
        "eligibility_rules": {
            "logic": "AND",
            "rules": [
                {"field": "occupation", "operator": "in", "value": ["farmer", "agricultural_labourer", "fisherman", "animal_husbandry"], "label": "Must be a farmer, fisherman, or involved in animal husbandry"},
                {"field": "age", "operator": "gte", "value": 18, "label": "Must be at least 18 years old"},
                {"field": "age", "operator": "lte", "value": 75, "label": "Must be 75 years or younger"},
            ]
        },
        "official_website": "https://www.nabard.org/",
        "application_process": "Apply at nearest bank branch with land documents"
    },
]


def get_all_schemes():
    """Return all schemes."""
    return SCHEMES


def get_scheme_by_id(scheme_id: str):
    """Return a single scheme by ID."""
    for s in SCHEMES:
        if s["scheme_id"] == scheme_id:
            return s
    return None


def get_scheme_descriptions():
    """Return (scheme_id, text) pairs for vector indexing."""
    pairs = []
    for s in SCHEMES:
        text = f"{s['name']}. {s['description']} Category: {s['category']}. Benefits: {s['benefits']}"
        pairs.append((s["scheme_id"], text))
    return pairs
