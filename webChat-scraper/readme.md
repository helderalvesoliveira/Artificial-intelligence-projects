# Project Documentation

## Overview
This project is designed to perform web scraping on a static website. It collects the content of the entire website, processes the data, and then enables users to interact with the content via a chat interface.

## Initial Setup

### Minimum Requirements
Ensure the following tools are installed on your system before proceeding:
- **Python** (latest version recommended)

### Configure Environment Variables
1. Copy the `env_example` file and create a new `.env` file. 
2. Update the variables in the `.env` file as needed:
   - `NAME_URL_SCRAPING`: The name of the website to scrape.
   - `URL_SCRAPING`: The URL of the website to scrape.

#### Commands to copy and create `.env` file:
- **Linux**:
  ```bash
  cp env_example .env
  ```
- **Windows**:
  ```cmd
  copy env_example .env
  ```

### Install Virtual Environment

#### Linux:
1. Create a virtual environment:
   ```bash
   python3 -m venv venv
   ```
2. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

#### Windows:
1. Create a virtual environment:
   ```cmd
   python -m venv venv
   ```
2. Activate the virtual environment:
   ```cmd
   venv\Scripts\activate
   ```
3. Install dependencies:
   ```cmd
   pip install -r requirements.txt
   ```

---

## Steps to Run the Project

After completing the initial setup, follow these steps to execute the project:

1. **Run Crawling Script:**
   Execute the `crawling.py` script to perform the crawling operation on the website and save the output to `output.json`.
   ```bash
   python crawling.py
   ```

2. **Run Scraping Script:**
   Execute the `scraping.py` script to process the crawled data.
   ```bash
   python scraping.py
   ```

3. **Run Chunking Script:**
   Execute the `chunking.py` script to save the processed data to the FAISS vector store.
   ```bash
   python chunking.py
   ```

4. **Run chat Application:**
   Finally, run the `chat.py` file using Streamlit to start the application:
   ```bash
   streamlit run chat.py
   ```

---

## Summary
The above steps complete the setup and execution of the project. Ensure each step is followed sequentially to avoid errors. If you encounter any issues, review the `.env` file configuration and ensure all dependencies are correctly installed.
