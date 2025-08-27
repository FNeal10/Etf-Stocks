# 📈 Market Price Scraper

A Python scraper that collects stock market prices from a list of URLs, transforms the data, and uploads it via a Flask API to **Azure Blob Storage**. Fully automated using **GitHub Actions**, **Docker**, and **Azure services**.

---

## ✨ Features

- 🕵️‍♂️ Scrapes prices for stocks you track  
- ⏰ Runs automatically **Monday to Friday at 9 AM**  
- ⚡ Uses **Selenium** for dynamic scraping  
- 🔄 **CI/CD pipeline** rebuilds Docker images automatically  
- ☁️ Uses **Azure Container Instances (ACI)** to run scheduled workflows  

---

## 🔧 Architecture

```mermaid
graph TD
    A[GitHub Actions CI/CD] --> B[Docker Images (Scraper \+ API)]
    B --> C[Azure Container Registry (ACR)]
    C --> D[Azure Container Instances (ACI)]
    D --> E[Scraper collects & transforms data]
    E --> F[Flask API]
    F --> G[Azure Blob Storage]
