# ⛏️ Coal Mining Risk Analysis & Prediction System

A Machine Learning based web application for analyzing coal mining accident patterns and predicting **pre-accident risk levels** based on mining conditions, worker characteristics, machinery, training, shift, and safety compliance.

The system combines **Data Analysis, Machine Learning, Flask, HTML, CSS, JavaScript, and Data Visualization** to provide an end-to-end mining safety analysis and prediction platform.

---

## 📌 Project Overview

Coal mining operations involve multiple environmental, operational, and human factors that can contribute to accidents.

This project analyzes historical coal mining accident data and develops a Machine Learning system capable of predicting the potential risk level **before an accident occurs**.

The system considers factors such as:

- Mine type
- Place of operation
- Machinery involved
- Worker age
- Worker experience
- Training level
- Shift
- Safety compliance score
- Mining location

The application classifies mining conditions into four risk categories:

> **Low → Moderate → High → Very High**

---

# 🎯 Objectives

The main objectives of this project are:

1. Analyze coal mining accident patterns.
2. Identify important factors associated with accident risk.
3. Perform Exploratory Data Analysis (EDA).
4. Engineer features for Machine Learning.
5. Train and compare multiple classification algorithms.
6. Develop a pre-accident risk prediction model.
7. Provide prediction confidence and risk probabilities.
8. Build a Flask-based web application.
9. Provide an interactive mining risk analysis dashboard.
10. Present the complete system through a user-friendly interface.

---

# 📊 Dataset

The project uses a dataset containing **800 coal mining records** covering major coal-producing states in India.

The dataset contains information about:

- Year
- State
- District
- Mine Name
- Mine Type
- Place of Operation
- Accident Type
- Machinery Involved
- Injured Workers
- Deaths
- Worker Age
- Worker Experience
- Training Level
- Shift
- Safety Compliance Score

The dataset includes records from **2015–2025**.

---

# 🗂️ Dataset Features

| Feature | Description |
|---|---|
| `Year` | Year of the mining accident record |
| `State` | State where the mine is located |
| `District` | Mining district |
| `Mine_Name` | Name of the mine |
| `Mine_Type` | Underground or Opencast |
| `Place_of_Operation` | Location of operation where the accident occurred |
| `Accident_Type` | Type of mining accident |
| `Machinery_Involved` | Machinery involved in the accident |
| `Injured` | Number of injured workers |
| `Death` | Number of deaths |
| `Worker_Age` | Age of the worker |
| `Worker_Experience_Years` | Worker experience category |
| `Training_Level` | Worker training level |
| `Shift` | Mining shift |
| `Safety_Compliance_Score` | Safety compliance score from 0–100 |

---

# ⚠️ Accident Types

The dataset contains the following accident categories:

1. Roof Fall
2. Side Fall
3. Machinery Collision
4. Vehicle Rollover
5. Fire
6. Explosion
7. Gas Leakage
8. Electrical Accident
9. Fall of Person
10. Blasting Accident

---

# 🏭 Mine Types

The system considers two major mining types:

- **Underground**
- **Opencast**

---

# 📍 Places of Operation

Mining operations are categorized into:

- Face
- Haul Road
- Workshop
- Stockyard
- Shaft
- Excavation Area

---

# 🚜 Machinery Categories

The system considers:

- None
- Drill
- Excavator
- Loader
- Dumper
- Truck
- Heavy Earth Moving Machinery

---

# 👷 Worker Experience

Worker experience is categorized as:

- `<1 year`
- `1–3 years`
- `3–5 years`
- `5–10 years`
- `10+ years`

---

# 🎓 Training Levels

Training is represented using five levels:

```text
None
↓
Basic
↓
Intermediate
↓
Advanced
↓
Certified
