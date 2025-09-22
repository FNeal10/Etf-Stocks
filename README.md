# 📈 Market Price Scraper

A Python scraper that collects stock market prices using Selenium, sends transformed data to a Flask API hosted in ACI, stores files in ADLS Gen2, triggers an ADF pipeline to upsert data into Azure SQL Database, Synapse, or save as Parquet in ADLS Gen2 following a Medallion Architecture (Bronze → Silver → Gold). Visualize insights with Power BI dashboards. Fully automated using GitHub Actions CI/CD and Docker.

---

**Table of Contents**

- [Installation](#installation)
- [Execution / Usage](#execution--usage)
- [Technologies](#technologies)
- [Features](#features)
- [Architecture](#architecture)

---

## Installation

On macOS and Linux:

```sh
$ python -m pip install -r requirements.txt
```

On Windows:

```powershell
PS> python -m pip install -r requirements.txt
```

---

## Execution / Usage

To run the scraper:

```sh
$ python scripts/run_scraper.py
```

To run the Flask API locally:

```sh
$ docker build -t flask-api:latest .
$ docker run -e AZURE_CONNECTION_STRING=<your-connection-string> -e CONTAINER_NAME=<your-container> -p 5000:5000 flask-api:latest
```

The **GitHub Actions workflow** handles:

1. Starting the ACI container with the Flask API  
2. Running the Python scraper  
3. Uploading data to **ADLS Gen2**  
4. Triggering the **ADF pipeline**  
5. Stopping the ACI container  

---

## Technologies

This project uses the following technologies and tools:

- [Python](https://www.python.org/) ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)  
- [Docker](https://www.docker.com/) ![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)  
- [GitHub Actions](https://github.com/features/actions) ![GitHub Actions](https://img.shields.io/badge/github%20actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)  
- [Azure Container Registry](https://azure.microsoft.com/en-us/services/container-registry/) ![ACR](https://img.shields.io/badge/ACR-%23007FFF.svg?style=for-the-badge)  
- [Azure Container Instances](https://azure.microsoft.com/en-us/services/container-instances/) ![ACI](https://img.shields.io/badge/ACI-%23007FFF.svg?style=for-the-badge)  
- [ADLS Gen2](https://learn.microsoft.com/en-us/azure/storage/data-lake-storage/) ![ADLS Gen2](https://img.shields.io/badge/ADLS%20Gen2-%23007FFF.svg?style=for-the-badge)  
- [Azure Data Factory](https://learn.microsoft.com/en-us/azure/data-factory/) ![ADF](https://img.shields.io/badge/ADF-%23007FFF.svg?style=for-the-badge)  
- [Azure SQL Database](https://learn.microsoft.com/en-us/azure/azure-sql/) ![Azure SQL](https://img.shields.io/badge/Azure%20SQL-%23007FFF.svg?style=for-the-badge)  
- [Azure Synapse Analytics](https://learn.microsoft.com/en-us/azure/synapse-analytics/) ![Synapse](https://img.shields.io/badge/Synapse-%23007FFF.svg?style=for-the-badge)  
- [Parquet](https://parquet.apache.org/) ![Parquet](https://img.shields.io/badge/Parquet-%23007FFF.svg?style=for-the-badge)  
- [Power BI](https://powerbi.microsoft.com/) ![Power BI](https://img.shields.io/badge/Power%20BI-%23F2C811.svg?style=for-the-badge&logo=power-bi&logoColor=black)

---

## Features

- 🕵️‍♂️ Scrapes stock prices from multiple sources using Selenium  
- ☁️ Flask API receives and uploads raw data (Bronze layer) to ADLS Gen2  
- 🔄 CI/CD pipeline builds Docker images and deploys the API to ACI  
- 🔄 ADF pipeline transforms and upserts data into Silver/Gold layers, Azure SQL, or Synapse  
- 💾 Stores optimized data as Parquet for cost-efficient storage  
- 📊 Connect Power BI to Azure SQL / Synapse / Parquet for dashboards and analytics  
- 🏗 Implements Medallion Architecture (Bronze → Silver → Gold) for structured, reliable data flow


---

## Architecture

```mermaid
graph TD
    A[GitHub Actions CI/CD] --> B[Start ACI - Flask API]
    B --> C[Run Python Selenium Scraper]
    C --> D[Flask API receives and uploads Bronze data to ADLS Gen2]
    D --> E[Trigger ADF Pipeline for Silver/Gold transformations]
    E --> F[Stop ACI]
    E --> G[Upsert data to Azure SQL Database / Synapse / ADLS Gen2 as Parquet]
    G --> H[Power BI Dashboards & Analytics]
```

---