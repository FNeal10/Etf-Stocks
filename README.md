📈 Market Price Scraper

A Python scraper that collects stock market prices from a list of URLs, transforms the data, and uploads it via a Flask API to Azure Blob Storage. Fully automated using GitHub Actions, Docker, and Azure services.

✨ Features
    🕵️‍♂️ Scrapes prices for stocks you track.
    ⏰ Runs automatically Monday to Friday at 9 AM.
    ⚡ Uses Selenium for dynamic scraping.
    🔄 Workflow: Scraper → Flask API → Azure Blob Storage.
    🚀 CI/CD rebuilds Docker images automatically.
    ☁️ Azure Container Instances (ACI) run the scheduled workflow.

🏗 Architecture
graph TD
    A[GitHub Actions CI/CD] --> B[Docker Images (Scraper + API) → Azure Container Registry (ACR)]
    B --> C[Azure Container Instances (ACI)]
    C --> D[Scraper collects & transforms data]
    D --> E[Flask API]
    E --> F[Azure Blob Storage]

⚙️ Workflow Overview
sequenceDiagram
    participant GH as GitHub Actions
    participant ACI as Azure Container Instance
    participant Scraper as Scraper
    participant API as Flask API
    participant Blob as Azure Blob Storage

    GH->>ACI: Start container
    ACI->>Scraper: Run scraper
    Scraper->>API: Send transformed data
    API->>Blob: Upload data
    ACI->>GH: Stop container

📝 Usage
Scraper fetches market data and sends it to the Flask API, which stores it in Azure Blob Storage.

API endpoints:
GET /stocks → returns latest prices
GET /stocks/<symbol> → returns price for a specific stock

📅 Schedule
Runs Monday to Friday at 9 AM via GitHub Actions:

📦 Quick Visual Summary
flowchart LR
    Scraper[Scraper 🕵️‍♂️] --> API[Flask API ⚡]
    API --> Blob[Azure Blob Storage ☁️]
    GitHubActions[GitHub Actions 🚀] --> Scraper
    ACI[Azure Container Instance ☁️] --> Scraper
