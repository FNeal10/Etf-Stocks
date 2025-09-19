# 📈 Market Price Scraper

A Python scraper that collects stock market prices from a list of URLs, transforms the data, and uploads it via a **Flask API** to **Azure Blob Storage**. Fully automated using **GitHub Actions**, **Docker**, **Azure Container Registry (ACR)**, **Azure Container Instances (ACI)**, **Azure Data Factory (ADF)**, and **Azure SQL Database**.

---

## ✨ Features

- 🕵️‍♂️ Scrapes stock prices for tracked stocks  
- ⏰ Runs automatically **Monday to Friday at 9 AM**  
- ⚡ Uses **Selenium** for dynamic web scraping  
- 🔄 Fully automated **CI/CD pipeline** with Docker and GitHub Actions  
- ☁️ Runs on **ACI** with containerized Python workflow  
- 🗄 Transforms data and **upserts into Azure SQL Database via ADF**  

---

## 🔧 Architecture

```mermaid
graph TD
    subgraph CI/CD
        A[📦 GitHub Actions CI/CD] --> B[🐳 Docker Images (Python Scraper + Flask API)]
    end
    B --> C[🏷 Azure Container Registry (ACR)]
    C --> D[☁️ Azure Container Instances (ACI)]
    D --> E[📝 Python Scraper collects & transforms data]
    E --> F[⚡ Flask API]
    F --> G[💾 Azure Blob Storage]
    G --> H[🔄 Azure Data Factory Pipeline]
    H --> I[🖥 Azure SQL Database Upsert]
