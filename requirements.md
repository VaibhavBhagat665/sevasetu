# SevaSetu - Requirements Document

## 1. Project Overview

**SevaSetu** is an Agentic AI-powered platform designed to improve access to Indian government welfare schemes by eliminating application errors, eligibility mismatches, and documentation issues that lead to high rejection rates.

The platform acts as a virtual service assistant for citizens and CSC/VLE operators, moving beyond informational chatbots to actively completing government service workflows.

---

## 2. Problem Statement

A large percentage of eligible citizens in India fail to receive government benefits due to:

- **Incorrect scheme selection** - Citizens apply for schemes they are not eligible for
- **Income and category mismatches** - Discrepancies in income certificates and caste/category documents
- **Document name inconsistencies** - Variations in names across Aadhaar, bank accounts, and land records
- **Complex PDF-based application forms** - Difficult to fill manually, especially for semi-literate users
- **Limited digital literacy and language barriers** - Inability to navigate digital government portals
- **Poor internet connectivity in rural areas** - Prevents online application completion

---

## 3. Goals and Objectives

- Reduce rejection rates in government scheme applications
- Improve last-mile access to public services
- Assist semi-literate and rural users through voice-based interaction
- Increase productivity of CSC/VLE operators
- Ensure ethical, transparent, and rule-based AI decision-making

---

## 4. Target Users

### Primary Users
- **Rural and semi-urban citizens** - Direct beneficiaries of welfare schemes
- **Farmers** - Accessing agricultural subsidies and support programs
- **Low-income households** - Seeking financial assistance and social welfare benefits
- **Beneficiaries of welfare schemes** - Existing or potential recipients of government programs

### Secondary Users
- **Common Service Centre (CSC) operators** - Government-authorized service providers
- **Village Level Entrepreneurs (VLEs)** - Local facilitators of digital services
- **NGOs and public service facilitators** - Organizations assisting citizens with government services

---

## 5. Functional Requirements

### 5.1 Voice-Based Interaction
- **FR-1.1**: Support voice-based user interaction in multiple Indian languages
- **FR-1.2**: Integrate speech-to-text (STT) capabilities using Bhashini APIs
- **FR-1.3**: Integrate text-to-speech (TTS) capabilities using Bhashini APIs
- **FR-1.4**: Handle conversational context across multiple turns
- **FR-1.5**: Support code-mixed language input (e.g., Hinglish)

### 5.2 Scheme Discovery
- **FR-2.1**: Integrate with MyScheme government dataset for scheme information
- **FR-2.2**: Enable search and filtering of schemes by category, state, and beneficiary type
- **FR-2.3**: Provide scheme details including eligibility criteria, benefits, and required documents
- **FR-2.4**: Recommend relevant schemes based on user profile

### 5.3 Eligibility Checking
- **FR-3.1**: Implement deterministic rule-based logic for eligibility verification
- **FR-3.2**: Validate user-provided information against scheme criteria
- **FR-3.3**: Provide clear explanations for eligibility decisions
- **FR-3.4**: Identify missing information required for eligibility determination
- **FR-3.5**: Support multi-criteria eligibility checks (age, income, category, location, etc.)

### 5.4 Document Processing
- **FR-4.1**: Perform OCR-based extraction of data from Aadhaar cards
- **FR-4.2**: Perform OCR-based extraction of data from bank passbooks
- **FR-4.3**: Perform OCR-based extraction of data from land records
- **FR-4.4**: Support image uploads in common formats (JPEG, PNG, PDF)
- **FR-4.5**: Handle document quality issues (blur, rotation, poor lighting)

### 5.5 Data Validation and Mismatch Detection
- **FR-5.1**: Detect name mismatches across documents before submission
- **FR-5.2**: Identify inconsistencies in dates of birth, addresses, and other key fields
- **FR-5.3**: Flag potential issues with document validity or authenticity
- **FR-5.4**: Provide suggestions for resolving detected mismatches
- **FR-5.5**: Generate validation reports for CSC/VLE operators

### 5.6 Form Filling Automation
- **FR-6.1**: Automatically fill government PDF application forms with extracted data
- **FR-6.2**: Map user data to appropriate form fields
- **FR-6.3**: Handle various PDF form formats and structures
- **FR-6.4**: Allow manual review and correction before finalization
- **FR-6.5**: Generate print-ready application forms

### 5.7 Grievance Management
- **FR-7.1**: Generate grievance drafts for rejected applications
- **FR-7.2**: Provide templates for common rejection reasons
- **FR-7.3**: Include relevant application details and supporting information
- **FR-7.4**: Support multiple grievance channels (online portals, email, physical submission)

### 5.8 Offline Support
- **FR-8.1**: Enable offline data capture and storage
- **FR-8.2**: Queue applications for submission when connectivity is restored
- **FR-8.3**: Sync data automatically when online
- **FR-8.4**: Provide offline access to scheme information and eligibility rules

---

## 6. Non-Functional Requirements

### 6.1 Performance
- **NFR-1.1**: OCR processing should complete within 5 seconds per document
- **NFR-1.2**: Voice interaction response time should be under 2 seconds
- **NFR-1.3**: Eligibility checking should complete within 1 second
- **NFR-1.4**: System should support low-end devices with limited processing power
- **NFR-1.5**: Application should load within 3 seconds on 2G/3G networks

### 6.2 Accuracy
- **NFR-2.1**: OCR accuracy should exceed 95% for standard government documents
- **NFR-2.2**: Speech recognition accuracy should exceed 90% for supported languages
- **NFR-2.3**: Eligibility determination should have 100% rule compliance
- **NFR-2.4**: Document mismatch detection should have minimal false positives (<5%)

### 6.3 Scalability
- **NFR-3.1**: Architecture should support nationwide deployment
- **NFR-3.2**: System should handle concurrent users across multiple CSCs
- **NFR-3.3**: Database should scale to millions of applications
- **NFR-3.4**: API design should support horizontal scaling

### 6.4 Security and Privacy
- **NFR-4.1**: All personal data must be encrypted at rest and in transit
- **NFR-4.2**: Comply with Indian data protection regulations
- **NFR-4.3**: Implement role-based access control for CSC/VLE operators
- **NFR-4.4**: Ensure secure document storage with automatic purging after submission
- **NFR-4.5**: Maintain audit logs for all data access and modifications

### 6.5 Usability
- **NFR-5.1**: Interface should be intuitive for semi-literate users
- **NFR-5.2**: Voice interaction should feel natural and conversational
- **NFR-5.3**: Error messages should be clear and actionable
- **NFR-5.4**: Support accessibility features for users with disabilities
- **NFR-5.5**: Provide multilingual UI with support for 10+ Indian languages

### 6.6 Reliability
- **NFR-6.1**: System uptime should be 99.5% or higher
- **NFR-6.2**: Offline mode should function without degradation
- **NFR-6.3**: Data synchronization should be resilient to network interruptions
- **NFR-6.4**: Implement automatic retry mechanisms for failed operations

### 6.7 Explainability
- **NFR-7.1**: All eligibility decisions must be explainable with clear reasoning
- **NFR-7.2**: No black-box AI models for critical decision-making
- **NFR-7.3**: Provide transparency in data usage and processing
- **NFR-7.4**: Document all rule-based logic for audit purposes

---

## 7. Technical Constraints

### 7.1 Hackathon Constraints
- **TC-1.1**: Solution must be suitable for MVP development within hackathon timeline
- **TC-1.2**: Focus on core features with demonstrable value
- **TC-1.3**: Use rapid prototyping tools and frameworks
- **TC-1.4**: Prioritize proof-of-concept over production-ready implementation

### 7.2 Data and API Constraints
- **TC-2.1**: Must rely on publicly available government datasets (MyScheme, etc.)
- **TC-2.2**: Use Bhashini APIs for speech processing
- **TC-2.3**: Cannot access restricted government backend systems
- **TC-2.4**: Use open-source OCR libraries and models

### 7.3 Scope Constraints
- **TC-3.1**: Must avoid medical decision-making beyond form assistance
- **TC-3.2**: Must avoid legal advice or decision-making
- **TC-3.3**: Cannot provide financial advice or guarantees
- **TC-3.4**: Should not replace human judgment in complex cases

---

## 8. Success Metrics

### 8.1 Application Quality Metrics
- **Reduction in application rejection probability** - Target: 40% reduction
- **Successful form completion rate** - Target: 90% of initiated applications
- **Document mismatch detection rate** - Target: 95% of potential issues identified

### 8.2 Efficiency Metrics
- **Time saved per application for CSC/VLE operators** - Target: 50% reduction
- **Average application completion time** - Target: Under 15 minutes
- **Number of applications processed per day per CSC** - Target: 2x increase

### 8.3 User Experience Metrics
- **User satisfaction score** - Target: 4.5/5 or higher
- **Voice interaction success rate** - Target: 85% task completion without fallback
- **Accessibility improvement score** - Measured through user feedback

### 8.4 Technical Metrics
- **System uptime** - Target: 99.5%
- **OCR accuracy** - Target: 95%+
- **API response time** - Target: <2 seconds for 95th percentile

---

## 9. Out of Scope

The following features are explicitly **not included** in the SevaSetu MVP:

- **Direct submission to government backend systems** - Applications are prepared but not submitted automatically
- **Automated financial disbursement** - No integration with payment or banking systems
- **Replacing human CSC/VLE operators** - System augments, not replaces, human facilitators
- **Real-time government database integration** - No live verification against government databases
- **Biometric authentication** - No fingerprint or iris scanning capabilities
- **Legal document generation** - No affidavits, legal notices, or court documents
- **Medical diagnosis or advice** - No health-related decision-making
- **Loan or credit assessment** - No financial underwriting or credit scoring

---

## 10. System Architecture Overview

### 10.1 Core Components
- **Voice Interface Layer** - STT/TTS using Bhashini APIs
- **Agentic AI Engine** - Orchestrates workflows and decision-making
- **Scheme Discovery Module** - MyScheme integration and recommendation engine
- **Eligibility Engine** - Rule-based deterministic logic
- **Document Processing Module** - OCR and data extraction
- **Validation Engine** - Mismatch detection and data verification
- **Form Filling Engine** - PDF automation and field mapping
- **Offline Sync Module** - Local storage and background synchronization
- **User Management** - Authentication and role-based access

### 10.2 Technology Stack Considerations
- **Frontend**: Progressive Web App (PWA) for offline support
- **Backend**: Scalable API architecture (REST/GraphQL)
- **AI/ML**: Open-source OCR models, rule-based engines
- **Database**: Supports offline-first architecture
- **APIs**: Bhashini (speech), MyScheme (schemes), custom OCR services

---

## 11. User Stories

### 11.1 Citizen User Stories
- **US-1**: As a farmer, I want to discover schemes I'm eligible for by speaking in my local language
- **US-2**: As a semi-literate user, I want to upload my documents and have the system extract information automatically
- **US-3**: As a beneficiary, I want to know why I'm not eligible for a scheme before applying
- **US-4**: As a rural citizen, I want to complete my application even when internet is unavailable

### 11.2 CSC/VLE Operator Stories
- **US-5**: As a CSC operator, I want to process applications faster with automated form filling
- **US-6**: As a VLE, I want to detect document mismatches before submission to avoid rejections
- **US-7**: As an operator, I want to generate grievance drafts for rejected applications quickly
- **US-8**: As a facilitator, I want to track application status and success rates

---

## 12. Risk Assessment

### 12.1 Technical Risks
- **OCR accuracy on poor-quality documents** - Mitigation: Manual review option
- **Speech recognition in noisy environments** - Mitigation: Text input fallback
- **Offline sync conflicts** - Mitigation: Conflict resolution UI
- **API rate limits and availability** - Mitigation: Caching and fallback mechanisms

### 12.2 User Adoption Risks
- **Digital literacy barriers** - Mitigation: Voice-first design, operator training
- **Trust in AI systems** - Mitigation: Explainable decisions, human oversight
- **Language coverage gaps** - Mitigation: Prioritize top 10 languages initially

### 12.3 Regulatory Risks
- **Data privacy compliance** - Mitigation: Follow Indian data protection laws
- **Government API terms of service** - Mitigation: Review and comply with usage policies
- **Liability for incorrect information** - Mitigation: Clear disclaimers, human verification

---

## 13. Future Enhancements (Post-MVP)

- Integration with DigiLocker for document verification
- Real-time status tracking of submitted applications
- AI-powered scheme recommendation using machine learning
- Blockchain-based application audit trail
- Mobile app for Android and iOS
- Integration with more government portals and services
- Advanced analytics dashboard for policy makers
- Community support forums and peer assistance

---

## 14. Glossary

- **CSC**: Common Service Centre - Government-authorized service delivery points
- **VLE**: Village Level Entrepreneur - Operators of CSCs in rural areas
- **Bhashini**: Government of India's National Language Translation Mission
- **MyScheme**: Government portal for discovering welfare schemes
- **OCR**: Optical Character Recognition - Technology to extract text from images
- **Agentic AI**: AI systems that can autonomously perform tasks and make decisions
- **STT**: Speech-to-Text conversion
- **TTS**: Text-to-Speech conversion
- **MVP**: Minimum Viable Product - Initial version with core features
