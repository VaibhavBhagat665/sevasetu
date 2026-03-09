"""
SevaSetu — Government Schemes Knowledge Base (Real Data)
Contains highly detailed Indian government welfare schemes with complex eligibility 
rules, comprehensive descriptions, and required documentation to demonstrate the AI 
rule engine's capabilities.
"""

SCHEMES = [
    {
        "scheme_id": "PM-KISAN",
        "name": "Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)",
        "short_name": "PM-KISAN",
        "category": "Agriculture",
        "description": "PM-KISAN is a Central Sector scheme with 100% funding from Government of India. It provides income support of ₹6,000 per year in three equal installments of ₹2,000 every four months to all landholding farmer families, subject to certain exclusion criteria relating to higher income status. The amount is directly transferred to the bank accounts of the beneficiaries.",
        "benefits": "₹6,000 per year (₹2,000 every 4 months) transferred directly to the beneficiary's Aadhaar-seeded bank account.",
        "state": "ALL",
        "required_documents": [
            "AADHAAR_CARD",
            "BANK_PASSBOOK_WITH_IFSC",
            "LAND_OWNERSHIP_RECORDS_ROR",
            "PASSPORT_SIZE_PHOTOGRAPH"
        ],
        "eligibility_rules": {
            "logic": "AND",
            "rules": [
                {"field": "occupation", "operator": "in", "value": ["farmer", "agricultural_labourer"], "label": "Applicant must be a farmer or agricultural labourer"},
                {"field": "land_holding", "operator": "lte", "value": 2.0, "label": "Combined land holding must not exceed 2.0 hectares"},
            ]
        },
        "official_website": "https://pmkisan.gov.in/",
        "application_process": "Eligible farmers can apply directly through the 'Farmers Corner' at pmkisan.gov.in or approach the local Patwari / Revenue Officer / Nodal Officer (PM-Kisan) appointed by the State Government, or visit the nearest Common Service Centres (CSCs)."
    },
    {
        "scheme_id": "PMAY-G",
        "name": "Pradhan Mantri Awaas Yojana - Gramin (PMAY-G)",
        "short_name": "PM Awaas (Rural)",
        "category": "Housing",
        "description": "A flagship housing scheme by the Ministry of Rural Development aiming to provide a pucca house with basic amenities to all rural houseless households and those living in kutcha and dilapidated houses. The minimum size of the house is 25 sq.mt with a hygienic cooking space.",
        "benefits": "Financial assistance of ₹1,20,000 in plain areas and ₹1,30,000 in hilly states/difficult areas/IAP districts. Beneficiaries also receive 90/95 person-days of unskilled labour wage under MGNREGS and ₹12,000 for toilet construction under Swachh Bharat Mission-Gramin.",
        "state": "ALL",
        "required_documents": [
            "AADHAAR_CARD",
            "BANK_PASSBOOK",
            "MGNREGA_JOB_CARD",
            "SWACHH_BHARAT_MISSION_NUMBER",
            "BPL_CERTIFICATE"
        ],
        "eligibility_rules": {
            "logic": "AND",
            "rules": [
                {"field": "residence", "operator": "eq", "value": "rural", "label": "Applicant must reside in a rural area"},
                {"field": "income", "operator": "lte", "value": 200000, "label": "Annual household income must be ≤ ₹2,00,000"},
                {"field": "owns_pucca_house", "operator": "eq", "value": False, "label": "Family must not already own a pucca house anywhere in India"},
            ]
        },
        "official_website": "https://pmayg.nic.in/",
        "application_process": "Selection is based on housing deprivation parameters in SECC 2011 data, verified by Gram Sabhas. Beneficiaries cannot apply directly but must approach their Gram Panchayat or Block Development Office to ensure their name is in the Permanent Wait List (PWL)."
    },
    {
        "scheme_id": "PM-UJJWALA-2",
        "name": "Pradhan Mantri Ujjwala Yojana (PMUY) 2.0",
        "short_name": "Ujjwala 2.0",
        "category": "Energy",
        "description": "PMUY 2.0 was launched to provide deposit-free LPG connections to adult women from poor households, covering migrant families who could not be covered under the earlier phase. It aims to safeguard the health of women and children by providing them with a clean cooking fuel (LPG).",
        "benefits": "Free LPG connection along with a free first refill and a hotplate (stove). Subsidy of ₹300 per 14.2 kg cylinder for up to 12 refills per year.",
        "state": "ALL",
        "required_documents": [
            "AADHAAR_CARD",
            "RATION_CARD_BPL",
            "BANK_PASSBOOK",
            "PASSPORT_SIZE_PHOTOGRAPH"
        ],
        "eligibility_rules": {
            "logic": "AND",
            "rules": [
                {"field": "gender", "operator": "eq", "value": "female", "label": "Applicant must be an adult woman"},
                {"field": "age", "operator": "gte", "value": 18, "label": "Must be 18 years of age or older"},
                {"field": "bpl", "operator": "eq", "value": True, "label": "Must belong to a Below Poverty Line (BPL) household or specific categories (SC/ST, PMAY, AAY)"},
                {"field": "has_lpg_connection", "operator": "eq", "value": False, "label": "No other LPG connection must exist in the same household"},
            ]
        },
        "official_website": "https://www.pmuy.gov.in/",
        "application_process": "Applicants can apply online on the PMUY portal or submit a physical application directly to the nearest LPG distributor."
    },
    {
        "scheme_id": "AB-PMJAY",
        "name": "Ayushman Bharat – Pradhan Mantri Jan Arogya Yojana (AB-PMJAY)",
        "short_name": "Ayushman Bharat",
        "category": "Health",
        "description": "The world's largest government-funded healthcare program. It provides cashless access to healthcare services for the beneficiary at the point of service in public and private empanelled hospitals across India. Covers 3 days of pre-hospitalization and 15 days post-hospitalization expenses.",
        "benefits": "Health insurance cover of up to ₹5,00,000 per family per year for secondary and tertiary care hospitalization. No cap on family size, age, or gender.",
        "state": "ALL",
        "required_documents": [
            "AADHAAR_CARD",
            "RATION_CARD",
            "MOBILE_NUMBER_LINKED_TO_AADHAAR"
        ],
        "eligibility_rules": {
            "logic": "AND",
            "rules": [
                {"field": "income", "operator": "lte", "value": 300000, "label": "Annual family income must be ≤ ₹3,00,000 (Based on SECC-2011/State criteria)"},
                {"field": "has_health_insurance", "operator": "eq", "value": False, "label": "Should not have existing formal sector health insurance"},
            ]
        },
        "official_website": "https://pmjay.gov.in/",
        "application_process": "Eligible families do not need to enroll. They can directly visit an empanelled hospital or CSC with their Aadhaar/Ration Card to get their 'Ayushman Card' printed."
    },
    {
        "scheme_id": "SSY",
        "name": "Sukanya Samriddhi Yojana (SSY)",
        "short_name": "Sukanya Samriddhi",
        "category": "Women & Child",
        "description": "Part of the 'Beti Bachao Beti Padhao' campaign, this government-backed savings scheme encourages parents to build a fund for the future education and marriage expenses of their female child. It offers one of the highest interest rates among small savings schemes.",
        "benefits": "High compound interest rate (currently 8.2% p.a.). Deposits qualify for deduction up to ₹1.5 lakh under Section 80C. Interest earned and maturity amount are completely tax-free.",
        "state": "ALL",
        "required_documents": [
            "GIRL_CHILD_BIRTH_CERTIFICATE",
            "PARENT_AADHAAR_CARD",
            "PARENT_PAN_CARD",
            "RESIDENTIAL_PROOF"
        ],
        "eligibility_rules": {
            "logic": "AND",
            "rules": [
                {"field": "beneficiary_age", "operator": "lte", "value": 10, "label": "Girl child must be below 10 years of age at the time of account opening"},
                {"field": "beneficiary_gender", "operator": "eq", "value": "female", "label": "Beneficiary must be a girl child"},
            ]
        },
        "official_website": "https://www.nsiindia.gov.in/",
        "application_process": "The account can be opened in any Post Office or authorized branch of commercial banks by the natural/legal guardian."
    },
    {
        "scheme_id": "PM-SVANIDHI",
        "name": "PM Street Vendor's AtmaNirbhar Nidhi (PM SVANidhi)",
        "short_name": "PM SVANidhi",
        "category": "Livelihood",
        "description": "A micro-credit facility launched during the COVID-19 pandemic to help street vendors resume their businesses. It facilitates collateral-free working capital loans to street vendors in urban, semi-urban, and rural areas.",
        "benefits": "First loan: up to ₹10,000. Second loan: up to ₹20,000. Third loan: up to ₹50,000. Features a 7% p.a. interest subsidy for timely repayment and cashbacks up to ₹1,200/year for digital transactions.",
        "state": "ALL",
        "required_documents": [
            "AADHAAR_CARD",
            "VOTER_ID_CARD",
            "BANK_PASSBOOK",
            "CERTIFICATE_OF_VENDING_COV"
        ],
        "eligibility_rules": {
            "logic": "AND",
            "rules": [
                {"field": "occupation", "operator": "in", "value": ["street_vendor", "hawker", "cart_puller", "cobbler"], "label": "Must be a recognized street vendor or hawker"},
                {"field": "age", "operator": "gte", "value": 18, "label": "Applicant must be at least 18 years old"},
            ]
        },
        "official_website": "https://pmsvanidhi.mohua.gov.in/",
        "application_process": "Vendors can apply directly on the PM SVANidhi portal through a CSC, or via the mobile app. Approached lending institutions (Banks/NBFCs) disburse the amount."
    },
    {
        "scheme_id": "MGNREGA",
        "name": "Mahatma Gandhi National Rural Employment Guarantee Act (MGNREGA)",
        "short_name": "MGNREGA",
        "category": "Employment",
        "description": "Indian labor law and social security measure that aims to guarantee the 'right to work'. It creates durable assets (like roads, canals, ponds) in rural areas while providing a livelihood safety net.",
        "benefits": "Legal guarantee for 100 days of wage employment in a financial year to adult members of a rural household at minimum wage rates fixed by the state.",
        "state": "ALL",
        "required_documents": [
            "AADHAAR_CARD",
            "BANK_POST_OFFICE_PASSBOOK",
            "PASSPORT_SIZE_PHOTOGRAPH"
        ],
        "eligibility_rules": {
            "logic": "AND",
            "rules": [
                {"field": "residence", "operator": "eq", "value": "rural", "label": "Household must be located in a rural area"},
                {"field": "age", "operator": "gte", "value": 18, "label": "Applicant must be an adult (18+ years)"},
                {"field": "willing_to_do_manual_work", "operator": "eq", "value": True, "label": "Must be willing to perform unskilled manual labour"},
            ]
        },
        "official_website": "https://nrega.nic.in/",
        "application_process": "Registration is done at the local Gram Panchayat. After registration, a 'Job Card' is issued within 15 days, after which work can be demanded."
    },
    {
        "scheme_id": "MUDRA",
        "name": "Pradhan Mantri MUDRA Yojana (PMMY)",
        "short_name": "PM MUDRA Loan",
        "category": "Livelihood",
        "description": "Micro Units Development & Refinance Agency Ltd. (MUDRA) provides refinancing support to Banks, MFIs, and NBFCs for lending to micro/small business entities engaged in manufacturing, trading, and service sectors, including allied agricultural activities.",
        "benefits": "Collateral-free loans up to ₹10 Lakhs. Three products: Shishu (up to ₹50,000 for startups), Kishore (₹50k-₹5L for existing businesses), Tarun (₹5L-₹10L for business expansion).",
        "state": "ALL",
        "required_documents": [
            "AADHAAR_CARD",
            "PAN_CARD",
            "BUSINESS_REGISTRATION_PROOF",
            "BANK_STATEMENT_LAST_6_MONTHS",
            "PROJECT_REPORT_BUSINESS_PLAN"
        ],
        "eligibility_rules": {
            "logic": "AND",
            "rules": [
                {"field": "occupation", "operator": "in", "value": ["self_employed", "small_business", "artisan", "shopkeeper", "trading"], "label": "Must be running or starting a non-corporate, non-farm small enterprise"},
                {"field": "age", "operator": "gte", "value": 18, "label": "Applicant must be at least 18 years old"},
            ]
        },
        "official_website": "https://www.mudra.org.in/",
        "application_process": "Borrowers can approach any Bank, Micro Finance Institution (MFI), or Non-Banking Financial Company (NBFC) or apply online through the Udyamimitra portal."
    },
    {
        "scheme_id": "POST-MATRIC-SC",
        "name": "Post-Matric Scholarship Scheme for SC Students",
        "short_name": "SC Post-Matric Scholarship",
        "category": "Education",
        "description": "A Centrally Sponsored Scheme to significantly increase the Gross Enrolment Ratio of SC students in higher education. It provides financial assistance to SC students studying at post-matriculation or post-secondary stages.",
        "benefits": "Covers compulsory non-refundable fees (tuition, games, union, library) and provides a monthly maintenance allowance ranging from ₹230 to ₹1200 depending on the course and hosteller/day-scholar status.",
        "state": "ALL",
        "required_documents": [
            "AADHAAR_CARD",
            "CASTE_CERTIFICATE",
            "INCOME_CERTIFICATE_ISSUED_BY_REVENUE_OFFICER",
            "PREVIOUS_YEAR_MARKSHEET",
            "FEE_RECEIPT_OF_CURRENT_COURSE"
        ],
        "eligibility_rules": {
            "logic": "AND",
            "rules": [
                {"field": "category", "operator": "eq", "value": "SC", "label": "Student must belong to the Scheduled Caste (SC) category"},
                {"field": "income", "operator": "lte", "value": 250000, "label": "Annual family income from all sources must be ≤ ₹2,50,000"},
                {"field": "education_level", "operator": "in", "value": ["post_matric", "graduate", "post_graduate", "diploma", "iti"], "label": "Must be pursuing post-matriculation studies in a recognized institution"},
            ]
        },
        "official_website": "https://scholarships.gov.in/",
        "application_process": "Students must apply online annually on the National Scholarship Portal (NSP) or their respective State scholarship portals."
    },
    {
        "scheme_id": "KCC",
        "name": "Kisan Credit Card (KCC) Scheme",
        "short_name": "Kisan Credit Card",
        "category": "Agriculture",
        "description": "Aims to provide adequate and timely credit support from the banking system to farmers for their cultivation and other needs under a single window. It covers post-harvest expenses, produce marketing loans, and working capital for maintenance of farm assets.",
        "benefits": "Short-term credit limits up to ₹3 Lakh at an effective interest rate of 4% p.a. (after 3% prompt repayment subvention). Includes built-in crop insurance and personal accident insurance cover.",
        "state": "ALL",
        "required_documents": [
            "AADHAAR_CARD",
            "LAND_OWNERSHIP_RECORDS_ROR",
            "CROP_SOWN_DETAILS",
            "BANK_PASSBOOK"
        ],
        "eligibility_rules": {
            "logic": "AND",
            "rules": [
                {"field": "occupation", "operator": "in", "value": ["farmer", "tenant_farmer", "sharecropper", "animal_husbandry", "fishery"], "label": "Must be engaged in agriculture or allied activities like animal husbandry/fishery"},
                {"field": "age", "operator": "gte", "value": 18, "label": "Must be between 18 to 75 years old"},
                {"field": "age", "operator": "lte", "value": 75, "label": "Max age 75 (co-borrower required if above 60)"},
            ]
        },
        "official_website": "https://sbi.co.in/web/agri-rural/agriculture-banking/crop-loan/kisan-credit-card",
        "application_process": "Farmers can apply at any Commercial Bank, Regional Rural Bank (RRB), or Cooperative Bank branch with their land records."
    },
    {
        "scheme_id": "PM-MATRU-VANDANA",
        "name": "Pradhan Mantri Matru Vandana Yojana (PMMVY)",
        "short_name": "Matru Vandana Yojana",
        "category": "Health",
        "description": "A maternity benefit program providing partial compensation for wage loss to women during childbirth and childcare. It ensures pregnant women get adequate rest and nutrition.",
        "benefits": "Cash incentive of ₹5,000 paid in three installments directly to pregnant women and lactating mothers for the first living child. Enhanced benefit of ₹6,000 if the second child is a girl.",
        "state": "ALL",
        "required_documents": [
            "AADHAAR_CARD",
            "MOTHER_CHILD_PROTECTION_MCP_CARD",
            "BANK_POST_OFFICE_PASSBOOK",
            "LMP_DATE_PROOF"
        ],
        "eligibility_rules": {
            "logic": "AND",
            "rules": [
                {"field": "gender", "operator": "eq", "value": "female", "label": "Must be a pregnant woman or lactating mother"},
                {"field": "age", "operator": "gte", "value": 19, "label": "Must be at least 19 years old at the time of pregnancy"},
                {"field": "is_government_employee", "operator": "eq", "value": False, "label": "Must not be a regular employee of Central/State Government or PSUs"},
            ]
        },
        "official_website": "https://pmmvy.wcd.gov.in/",
        "application_process": "Apply offline at Anganwadi Centres (AWCs) or approved health facilities, or online through the Citizen login on the PMMVY software portal."
    },
    {
        "scheme_id": "STAND-UP-INDIA",
        "name": "Stand-Up India Scheme",
        "short_name": "Stand-Up India",
        "category": "Livelihood",
        "description": "Facilitates bank loans between ₹10 lakh and ₹1 Crore to at least one Scheduled Caste (SC) or Scheduled Tribe (ST) borrower and at least one woman borrower per bank branch for setting up a greenfield enterprise in manufacturing, services, or trading sectors.",
        "benefits": "Composite loan (inclusive of term loan and working capital) between ₹10 Lakhs to ₹100 Lakhs for 85% of the project cost. Access to credit guarantee cover.",
        "state": "ALL",
        "required_documents": [
            "AADHAAR_CARD",
            "PAN_CARD",
            "CASTE_CERTIFICATE",
            "BUSINESS_PROJECT_REPORT",
            "RENT_AGREEMENT_OR_PROPERTY_DEED"
        ],
        "eligibility_rules": {
            "logic": "AND",
            "rules": [
                {"field": "occupation", "operator": "in", "value": ["entrepreneur", "self_employed", "business"], "label": "Must be starting a new greenfield enterprise"},
                {"field": "age", "operator": "gte", "value": 18, "label": "Applicant must be above 18 years of age"},
                {"field": "category_or_gender", "operator": "in", "value": ["SC", "ST", "female"], "label": "Must be an SC/ST applicant OR a Woman entrepreneur"},
            ]
        },
        "official_website": "https://www.standupmitra.in/",
        "application_process": "Applications can be submitted directly at the bank branch, through the Stand-Up India Portal, or through the Lead District Manager (LDM)."
    }
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
