# 📈 Market Price Scraper

A Python scraper that collects stock market prices using **Selenium**, sends transformed data to a **Flask API** hosted in **ACI**, stores files in **ADLS Gen2**, and triggers an **ADF pipeline** to upsert data into **Azure SQL Database**. Fully automated using **GitHub Actions CI/CD** and Docker.

---

**Table of Contents**

- [Installation](#installation)
- [Execution / Usage](#execution--usage)
- [Technologies](#technologies)
- [Features](#features)
- [Architecture](#architecture)
- [License](#license)

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

---

## Features

- 🕵️‍♂️ Scrapes stock prices from multiple sources using Selenium  
- ☁️ Flask API receives and uploads data to **ADLS Gen2**  
- 🔄 CI/CD pipeline builds Docker images and deploys the API to ACI  
- ⏰ Scheduled execution via GitHub Actions  
- 🔄 ADF pipeline transforms and upserts data into Azure SQL Database  

---

## Architecture

```mermaid
graph TD
    A[GitHub Actions CI/CD] --> B[Start ACI - Flask API]
    B --> C[Run Python Selenium Scraper]
    C --> D[Flask API receives and uploads data to ADLS Gen2 Storage]
    D --> E[Trigger ADF Pipeline]
    E --> F[Stop ACI]
    E --> G[Azure SQL Database Upsert]
```

---