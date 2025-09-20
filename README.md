# 📈 Market Price Scraper

A Python scraper that collects stock market prices from a list of URLs, transforms the data, and uploads it via a **Flask API** to **Azure Blob Storage**. Fully automated using **GitHub Actions**, **Docker**, **Azure Container Registry (ACR)**, **Azure Container Instances (ACI)**, **Azure Data Factory (ADF)**, and **Azure SQL Database**.

---

## ✨ Features

- 🕵️‍♂️ Scrapes stock prices for tracked stocks using **Python** and **Selenium**   
- ⏰ Runs automatically **Monday to Friday at 9 AM**
- 🔄 Fully automated **CI/CD pipeline** with Docker and GitHub Actions  
- ☁️ Runs on **ACI** with containerized Python workflow  
- 🗄 Transforms data and add features before **upserting into Azure SQL Database via ADF**  

---

## 🔧 Architecture

```mermaid
graph TD
    A[GitHub Actions CI/CD] --> B[Start ACI - Flask API]
    B --> C[Run Python Selenium Scraper]
    C --> D[Flask API receives and uploads data]
    D --> E[Azure Blob Storage]
    E --> F[Trigger ADF Pipeline]
    F --> G[Azure SQL Database Upsert]
    B --> H[Stop ACI]


