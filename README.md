# Visiting Card Text Extractor

A Streamlit-based application that extracts structured information from images of business cards using Google's Gemini AI model. The extracted data is then stored in a MySQL database for easy retrieval and management.

## Features
- **Single and Bulk Image Processing:** Extract details from individual or multiple business card images.
- **AI-Powered Extraction:** Utilizes Google's Gemini AI to analyze images and retrieve structured data.
- **Database Storage:** Automatically stores extracted details in a MySQL database.
- **Streamlit UI:** User-friendly interface for uploading images and processing results.

## Installation
### Prerequisites
Ensure you have the following installed:
- Python 3.x
- MySQL Server
- Required Python libraries (listed in `requirements.txt`)

### Steps
1. Clone the repository:
   ```sh
   git clone https://github.com/sohamfcb/visiting-card.git
   cd visiting-card
   ```
2. Create a virtual environment (optional but recommended):
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Set up your `.env` file with:
   ```sh
   GOOGLE_API_KEY=your_gemini_api_key
   MYSQL_PASSWORD=your_mysql_password
   ```
5. Run the application:
   ```sh
   streamlit run home.py
   ```

## Usage
### Uploading and Extracting Data
1. Open the app in a browser after running `streamlit run home.py`.
2. Navigate to the **Text Extractor** page to upload a single image.
3. Navigate to **Multiple Cards** to process multiple images from a directory.
4. The extracted data is displayed on the UI and stored in MySQL.

### Database Schema
The `details` table stores extracted information:
```sql
CREATE TABLE details (
    name VARCHAR(100),
    company VARCHAR(200),
    job_role VARCHAR(100),
    address TEXT,
    phone VARCHAR(50),
    phone2 VARCHAR(50),
    email VARCHAR(100),
    website VARCHAR(255),
    CONSTRAINT check_unique UNIQUE (name, email)
);
```

## Technologies Used
- **AI Model:** Google Gemini 1.5 Pro
- **Backend:** Python, Streamlit
- **Database:** MySQL
- **Libraries:** PIL, pymysql, google-generativeai, dotenv

## Environment Variables
Ensure the following environment variables are set in your `.env` file:
```sh
GOOGLE_API_KEY=your_gemini_api_key
MYSQL_PASSWORD=your_mysql_password
```

## Dependencies
Install dependencies using:
```sh
pip install -r requirements.txt
```
### List of Dependencies:
- `mysql.connector`
- `pandas`
- `numpy`
- `pymysql`
- `google-generativeai`
- `streamlit`
- `python-dotenv`

## Running the Application
To start the application:
```sh
streamlit run home.py
```

This will open a local server where you can upload business card images and extract structured information.

