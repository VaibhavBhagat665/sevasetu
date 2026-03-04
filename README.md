# SevaSetu — AI-Powered Welfare Scheme Assistant

An Agentic AI platform built on **AWS** that helps Indian citizens and CSC/VLE operators successfully apply for government welfare schemes by preventing application errors and automating documentation workflows.

## 🏗️ AWS Architecture

| AWS Service | Purpose |
|-------------|---------|
| **Amazon Bedrock** (Claude 3 Haiku) | LLM-powered intent extraction from natural language |
| **Amazon S3** | Secure document storage & generated PDF hosting |
| **Amazon DynamoDB** | Persistent session & workflow state management |
| **Amazon EC2** | Hosts the FastAPI backend with FAISS vector search |
| **Nginx (on EC2)** | Reverse proxy serving React frontend & routing API |

### Why AI is Required
- Citizens describe needs in natural language (Hindi/English) — AI extracts structured intent (occupation, income, state, etc.)
- Semantic search via FAISS finds best-matching schemes from 10+ government programs
- Deterministic rule engine explains eligibility decisions transparently

### Architecture Diagram

```
Browser → Nginx (port 80)
             ├── / → React SPA (static files)
             └── /api/* → FastAPI Backend
                          ├── Amazon Bedrock → Intent extraction
                          ├── Amazon S3 → Document & PDF storage
                          ├── Amazon DynamoDB → Session persistence
                          ├── FAISS → Semantic scheme search
                          └── fpdf2 → PDF form generation
```

## 🚀 Quick Start (Local Development)

### Prerequisites
- Python 3.9+, Node.js 18+, npm

### Backend
```bash
cd backend
pip install -r requirements.txt
python main.py
```
Backend at **http://localhost:8000** | Swagger at **http://localhost:8000/docs**

### Frontend
```bash
cd frontend
npm install
npm run dev
```
Frontend at **http://localhost:5173**

> Without AWS credentials, the system runs in **offline mode** using keyword-based intent extraction and local file storage.

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/intent` | Extract structured intent (Bedrock / fallback) |
| POST | `/scheme-match` | FAISS semantic search for matching schemes |
| POST | `/validate-eligibility` | Rule-based eligibility with explanations |
| POST | `/upload-documents` | Upload document to S3 for OCR |
| POST | `/extract-ocr/{id}` | Extract data from uploaded document |
| POST | `/validate-documents` | Cross-validate document consistency |
| POST | `/generate-form` | Generate auto-filled PDF (stored in S3) |
| POST | `/generate-grievance` | Generate grievance letter PDF |
| GET  | `/health` | Health check (AWS connectivity status) |

## 🚀 AWS Deployment Guide

### Step 1: Launch EC2 Instance
1. AWS Console → **EC2** → **Launch Instance**
2. **AMI**: Ubuntu 24.04 LTS | **Type**: `t3.medium` | **Storage**: 20GB
3. **IAM Role**: Create role with `AmazonS3FullAccess`, `AmazonDynamoDBFullAccess`, `AmazonBedrockFullAccess`
4. **Security Group**: Allow SSH (22), HTTP (80)
5. **Key Pair**: Download `.pem` file

### Step 2: Enable Bedrock Model Access
AWS Console → **Bedrock** → **Model access** → Request access for **Anthropic Claude 3 Haiku**

### Step 3: Connect & Install Docker
```bash
ssh -i "sevasetu-key.pem" ubuntu@<EC2_PUBLIC_IP>
sudo apt update && sudo apt install docker.io docker-compose git awscli -y
sudo usermod -aG docker ubuntu
exit  # Re-login for group change
```

### Step 4: Clone, Setup AWS Resources & Deploy
```bash
ssh -i "sevasetu-key.pem" ubuntu@<EC2_PUBLIC_IP>
git clone https://github.com/VaibhavBhagat665/sevasetu.git
cd sevasetu

# Create S3 buckets, DynamoDB table
chmod +x setup_aws.sh && ./setup_aws.sh

# Build and launch
docker-compose up -d --build
```

### Step 5: Access Your App
Open `http://<EC2_PUBLIC_IP>` in your browser 🎉

## 🛠️ Key Technologies

- **AI/ML**: Amazon Bedrock (Claude 3 Haiku), FAISS, sentence-transformers
- **Storage**: Amazon S3, Amazon DynamoDB
- **Backend**: FastAPI, Python, fpdf2, fuzzywuzzy
- **Frontend**: React, Vite, Web Speech API, PWA
- **Deployment**: Docker, Nginx, Amazon EC2

