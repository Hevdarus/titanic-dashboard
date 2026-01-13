# Titanic Survival Analysis Dashboard

Interactive dashboard built with Python and Dash to explore factors influencing passenger survival on the Titanic dataset.

The application allows users to filter passengers by sex, travel class, and age group, and dynamically updates all visualizations.

## Data Source

This project uses the Titanic dataset available on Kaggle:

Zain280. *Titanic Data Set*. Kaggle.  
https://www.kaggle.com/datasets/zain280/titanic-data-set?select=train.csv

The dataset was cleaned and preprocessed prior to visualization, including missing value handling and feature engineering.

---

## Features

- Interactive filters:
  - Sex
  - Passenger class
  - Age group

- Visualizations:
  - Passenger survival count by sex (stacked bar chart)
  - Ticket fare distribution by survival outcome (box plot)
  - Survival rate across sex and passenger class (heatmap)
  - Age–fare relationship by survival outcome (scatter plot)
  - Passenger age distribution by survival outcome (violin plot)
  - Passenger composition by class, cabin availability, and survival outcome (treemap)

- Feature engineering:
  - Family size and solo travel indicators
  - Cabin availability flag
  - Age group categorization
  - Cleaned and processed dataset

---

## Technologies Used

- Python 3.x
- Dash
- Plotly
- Pandas

---

## How to Run the Project

1. Install required packages:

```bash
pip install dash pandas plotly
```

2. (Optional) Run preprocessing:
```bash
python preprocess.py
```

3. Start the dashboard:
```bash
python app.py
```

4. Open your browser and go to:
```bash
http://127.0.0.1:8050/
```
