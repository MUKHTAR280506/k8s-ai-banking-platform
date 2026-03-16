# Kuberenetes deployed AI Banking Chatbot

A production-grade, Kubernetes-first, AI-powered banking platform built with FastAPI, React, PostgreSQL, Qdrant, and LLM-based intelligence.

This project simulates an enterprise-level digital banking system integrating Generative AI, Retrieval-Augmented Generation (RAG), CRM automation, transaction processing, and DevOps practices within a cloud-native microservices architecture.

---

## 🚀 Project Overview

k8s-ai-banking-platform is an end-to-end AI-powered banking assistant designed to simulate real-world banking workflows including:

- Intelligent chatbot powered by LLM
- Complaint detection using sentiment analysis
- Fund transfer with compliance validation
- Sanctions checking via vector search (Qdrant)
- Admin management panel
- Transaction history tracking
- Kubernetes-based deployment
- Dockerized microservices
- CI/CD ready architecture

The system is designed to mimic enterprise BFSI production environments.

---

## 🏗️ Architecture Overview

User (Browser)
    ↓
React Frontend (UI Layer)
    ↓
FastAPI Backend (Application Layer)
    ↓
---------------------------------------------------
| PostgreSQL (Transactional DB)                  |
| Qdrant (Vector DB for RAG & Compliance)       |
| OpenAI / Local LLM                            |
---------------------------------------------------
    ↓
Kubernetes Cluster (Pods, Services, Ingress)

---

## ⚙️ Core Features

### 🤖 AI Chatbot
- LLM-powered banking assistant
- Context-aware response generation
- Integrated RAG for compliance rules

### 📌 CRM Sub-Agent
- Detects complaints automatically
- Classifies severity & category using LLM
- Performs sentiment scoring
- Stores complaints in CRM table
- Notifies customer

### 💸 Fund Transfer Workflow
- Beneficiary selection
- Sanctions verification via vector search
- Balance validation
- Transfer limits validation
- Transaction logging
- Atomic debit operations

### 📜 Transaction History
- Fetch last N transactions
- Display formatted statements
- Persistent ledger storage

### 👤 Admin Panel
- Manage customer balances
- Credit/Debit via wallet API
- View beneficiaries
- Delete beneficiaries
- Upload sanctions/rules file
- Configure transfer limits

---

## 🧠 AI & RAG Implementation

- Embeddings generated using OpenAI Embeddings
- Compliance rules stored in Qdrant vector DB
- Semantic similarity search for sanctions check
- LLM-based structured output parsing
- CRM complaint detection using StructuredOutputParser

---

## 🗄️ Database Design

### PostgreSQL Tables:
- accounts
- beneficiaries
- transactions
- transfer_limits
- crm_complaints

### Vector Database:
- Qdrant collection for sanctions/rules

---

## 🐳 Containerization

All services are Dockerized:

- backend
- frontend
- postgres
- qdrant

Docker Compose for local development.

---

## ☸ Kubernetes Deployment

Deployed on local Kubernetes cluster using:

- Deployment YAMLs
- Services
- Ingress
- ConfigMaps
- Secrets

Frontend accessed via browser through Ingress.

Production-ready simulation with:
- Pod isolation
- Service discovery
- Horizontal scalability ready
- Secure environment variable management

---

## 🔐 Security Features

- Basic authentication
- Admin vs Customer role separation
- Input validation
- Sanctions screening
- Transaction limit enforcement
- Row-level locking for financial safety

---

## 🔄 CI/CD Ready

Designed for:
- GitHub Actions integration
- Docker image build automation
- Kubernetes deployment pipeline
- Version-controlled infrastructure

---

## 🛠️ Tech Stack

### Backend
- FastAPI
- SQLAlchemy
- LangChain
- OpenAI API
- Pydantic

### Frontend
- React
- CSS

### Database
- PostgreSQL
- Qdrant Vector DB

### DevOps
- Docker
- Docker Compose
- Kubernetes
- GitHub

---

## 📦 Project Structure

backend/
  app/
    agents/
    chains/
    models/
    routes/
    rag/
    core/
frontend/
  src/
    components/
    pages/
k8s/
  deployments
  services
  ingress



## ▶️ Deploy in Kubernetes

```bash
kubectl apply -f k8s/
```
modify etc/host file add 127.0.0.1 bankbot.local2

Access via configured Ingress host.
---
URL to access the app -  http://bankbot.local2

## 📊 Enterprise Simulation Capabilities

- AI-assisted complaint classification
- Compliance enforcement using vector search
- Banking-grade transaction validation
- Admin control panel
- Real-time ledger updates
- Microservices-based architecture
- Cloud-native design

---

## 🎯 Use Cases

- AI-powered banking assistant
- BFSI AI automation demo
- RAG implementation reference
- Kubernetes deployment practice
- Production-style AI system architecture
- Portfolio project for AI/ML Engineers

---

## 👨‍💻 Author

Mukhtar Ahmad  
AI Engineer | NLP | Generative AI | Banking Domain Specialist  

LinkedIn: https://www.linkedin.com/in/mukhtar280506/  
GitHub: https://github.com/MUKHTAR280506  

---

## ⭐ Why This Project Stands Out

This is not a basic chatbot.

It demonstrates:

- Generative AI integration
- Structured LLM outputs
- Vector database integration
- Microservices architecture
- Kubernetes deployment
- Banking domain logic
- Admin + Compliance workflows
- Production-level design 

---

## 📌 Future Enhancements

- Role-based authentication (JWT)
- Horizontal Pod Autoscaling
- Monitoring with Prometheus & Grafana
- Model hosting with local LLM
- Multi-tenant banking simulation
- Real-time Kafka transaction streaming

---



