# 🚴‍♂️ Bike Sharing Data Analysis & Dashboard

![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.43.0-FF4B4B.svg)
![Pandas](https://img.shields.io/badge/Pandas-2.2.3-150458.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

> An interactive data analysis and visualization dashboard for exploring bike-sharing patterns, built with Python and Streamlit.

## 📊 Live Demo

Experience the interactive dashboard: **[Bike Sharing Dashboard](https://proyek-akhir-rahmat.streamlit.app/)**

## 📖 About This Project

This project provides comprehensive analysis and visualization of bike-sharing data, helping to understand usage patterns, seasonal trends, and factors affecting bike rental demand. The project includes:

- **📓 Jupyter Notebook Analysis**: Detailed exploratory data analysis (EDA) with statistical insights
- **🎨 Interactive Dashboard**: Real-time data visualization built with Streamlit
- **📈 Key Insights**: Analysis of rental patterns by season, time, weather conditions, and user behavior

## ✨ Key Features

- 📅 **Interactive Date Range Selection**: Filter data by custom date ranges
- 🌦️ **Seasonal Analysis**: Compare bike rental trends across different seasons
- ⏰ **Hourly Patterns**: Identify peak usage hours throughout the day
- 📆 **Monthly Trends**: Track registered user growth over time
- 🌡️ **Weather Impact Analysis**: Understand how temperature and humidity affect rentals
- 📊 **Visual Analytics**: Interactive charts and graphs for easy interpretation

## 🔍 Business Questions Answered

1. **Seasonal Trends**: Which season has the highest bike rentals in 2011 and 2012?
2. **Peak Hours**: What are the peak hours for bike-sharing usage each day in 2012?
3. **User Growth**: How do registered users grow monthly throughout 2012?
4. **Weather Impact**: How do temperature and humidity affect user demand for bike rentals?

## 📁 Dataset

The project uses the **Bike Sharing Dataset** which contains:
- `day.csv`: Daily bike rental data aggregated by date
- `hour.csv`: Hourly bike rental data for detailed time-series analysis

**Data Features:**
- Date and time information
- Weather conditions (temperature, humidity, wind speed)
- Seasonal information
- User types (casual vs registered)
- Rental counts

## 🛠️ Technologies Used

- **Python 3.11**: Core programming language
- **Streamlit**: Interactive web dashboard framework
- **Pandas**: Data manipulation and analysis
- **Matplotlib & Seaborn**: Data visualization
- **NumPy**: Numerical computing

## 🚀 Getting Started

### Prerequisites

- Python 3.11 or higher
- pip or conda package manager

### Installation

#### Option 1: Using Anaconda

```bash
# Create a new conda environment
conda create --name main-ds python=3.11

# Activate the environment
conda activate main-ds

# Install dependencies
pip install -r requirements.txt
```

#### Option 2: Using pip (Shell/Terminal)

```bash
# Create project directory
mkdir proyek_analisis_data
cd proyek_analisis_data

# Optional: Create virtual environment
pipenv install
pipenv shell

# Install dependencies
pip install -r requirements.txt
```

### Running the Application

#### 1. Run the Streamlit Dashboard

```bash
streamlit run dashboard/dashboard.py
```

The dashboard will open in your default web browser at `http://localhost:8501`

#### 2. Explore the Jupyter Notebook

```bash
jupyter notebook bike_sharing_data_analysis.ipynb
```

## 📂 Project Structure

```
proyek-analisis-data/
├── dashboard/
│   ├── dashboard.py           # Streamlit dashboard application
│   └── all_data.csv           # Processed data for dashboard
├── data/
│   ├── day.csv                # Daily bike rental data
│   └── hour.csv               # Hourly bike rental data
├── bike_sharing_data_analysis.ipynb  # Jupyter notebook with EDA
├── requirements.txt           # Project dependencies
├── url.txt                    # Deployed dashboard URL
└── README.md                  # This file
```

## 💡 How to Use the Dashboard

1. **Select Date Range**: Use the sidebar to choose your desired date range for analysis
2. **Explore Visualizations**: Scroll through different sections to view various insights
3. **Analyze Patterns**: 
   - Compare seasonal trends across years
   - Identify peak usage hours
   - Monitor monthly user registration growth
   - Understand weather's impact on rentals

## 📸 Dashboard Preview

The dashboard includes:
- 📊 Bar charts for seasonal and monthly comparisons
- 📈 Line plots for temporal trends
- 🔥 Heatmaps for pattern recognition
- 📉 Distribution plots for weather analysis

## 👤 Author

**Rahmat Amalul Ahlin**
- 📧 Email: rahmatmulyan@gmail.com
- 💼 Dicoding ID: rahmat_amalul

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Dataset provided by [Dicoding Indonesia](https://www.dicoding.com/)
- Built as part of the "Belajar Analisis Data dengan Python" course

---

⭐ If you find this project useful, please consider giving it a star!

📝 Feel free to fork, modify, and use this project for your own learning purposes.