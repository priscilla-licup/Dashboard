# What a Waste! - Philippines' Waste Management Dashboard

## Application Overview

**Application Name:** What a Waste!

**Link to Deployed Application:** [Visit Dashboard](https://group5dashboard.pythonanywhere.com/)

**Description:**

Improper waste management is a prevalent issue in the Philippines, despite having collection systems. "What a Waste!" is a data dashboard designed to present the urgency of waste management issues to policymakers and large-scale waste generators. By understanding the data, we aim to enable informed decision-making for creating better waste reduction plans and promoting sustainable practices.

**Project Team:** Team 5
- ABROGUEANA, Alfhea Yvanika
- DE SILVA, Wayne Flossien
- JAVIER, Allysa
- LICUP, Priscilla Mariah
- MOTWANI, Hitika

## Setup Instructions

### Prerequisites

Before you begin, ensure you have the following installed:
- **Python** (3.7 or higher)
- **pip** (Python package manager)

### Downloading the Project

1. **Download the ZIP from GitHub**
   - Go to the [GitHub repository page](https://github.com/priscilla-licup/Dashboard).
   - Click on the `Code` button and select `Download ZIP`.
   - Extract the ZIP file to your desired location.

### Running the Application

2. **Install Required Python Packages**

    In your command line interface (CLI), run:
    ```
    pip install dash dash-bootstrap-components pandas geopandas plotly
    ```
    
    This installs Dash, Dash Bootstrap Components, Pandas, GeoPandas, and Plotly.

3. **Set Up the Data**

    Confirm the following folder structure in your project directory:
    ```
    your-project-directory/
    ├── datasets/
    │ ├── waste_data/
    │ │ ├── 2015.csv
    │ │ ├── 2016.csv
    │ │ ...
    │ ├── waste_data/new/
    │ │ ├── 2015.csv
    │ │ ├── 2016.csv
    │ │ ...
    │ └── geojson/
    │ │ ├── 2015_gdf.geojson
    │ │ ├── 2016_gdf.geojson
    │ ...
    ├── assets/
    │ ├── garbage.png
    │ ├── styles.css
    └── app.py
    ```

4. **Navigate to the Project Directory**

    Change to the project directory:
    ```
    cd path/to/your-project-directory
    ```
    Replace `path/to/your-project-directory` with the actual path.

5. **Run the Application**

    Execute:
    ```
    python app.py
    ```
    Run this command in the directory containing `app.py`.

6. **Access the Dashboard**

    Open your web browser and go to:
    ```
    http://127.0.0.1:8050/
    ```
    The dashboard should now be running on your local machine.







