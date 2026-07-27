#  AI Study Planner

An AI-powered intelligent study planning system that helps students improve their learning efficiency by predicting performance, tracking progress, and generating personalized study recommendations.

##  Live Demo

🔗 Streamlit App:

(https://smart-study-dashboard-c73quikkb3p6mr44uzqvcz.streamlit.app/)

---

#  Project Overview

Students often struggle with managing study time, maintaining consistency, and identifying weak areas.

**AI Study Planner** is a machine learning-based application that analyzes student study patterns and provides:

* Performance prediction
* Personalized study plans
* Progress tracking
* Smart recommendations
* Data visualization

The system helps students make better study decisions using Artificial Intelligence and Machine Learning.

---

#  Features

## Student Login System

* Secure login interface
* Multiple user support
* Personalized user history

---

##  AI Score Prediction

The system predicts student performance based on:

* Study hours
* Sleep hours
* Focus level
* Break duration

Example:

```
Input:
Study Hours: 6
Focus Level: 8
Sleep: 7 hours

Output:
Predicted Score: 85/100
```

---

##  Daily Study Tracker

Students can:

* Save daily study records
* Track previous predictions
* View learning history
* Download history data as CSV

---

##  Smart Study Suggestions

The AI system generates personalized recommendations based on:

* Subject
* Difficulty level
* Available days
* Daily study hours
* Focus level
* Sleep pattern

Example:

```
Subject: Python
Difficulty: Hard
Days Left: 7

AI Recommendation:
- Revise Python basics
- Practice coding problems
- Take mock tests
```

---

##  Progress Dashboard

The application provides visualization of:

* Study hour trends
* Predicted score improvement
* Learning history
* Performance tracking

---

#  Project Architecture

```
AI Study Planner
│
├── User Interface
│       |
│       └── Streamlit App
│
├── Machine Learning Model
│       |
│       ├── Data Processing
│       ├── Model Training
│       └── Prediction
│
├── Database
│       |
│       └── SQLite
│
└── Recommendation System
        |
        └── Smart Study Plan Generator
```

---

#  Technologies Used

## Programming Language

* Python

## Machine Learning

* Scikit-learn
* Pandas
* NumPy

## Frontend

* Streamlit

## Visualization

* Matplotlib

## Database

* SQLite

## Model Saving

* Joblib

## Version Control

* Git & GitHub

---

#  Project Structure

```
AI_Study_Planner
│
├── app.py
├── utils.py
├── train_model.py
├── requirements.txt
├── README.md
│
├── model/
│   ├── study_model.pkl
│   └── feature_columns.pkl
│
├── database/
│   └── study.db
│
└── dataset/
    └── study_data.csv
```

#  Machine Learning Workflow

The ML pipeline includes:

```
Dataset Collection
        ↓
Data Cleaning
        ↓
Feature Selection
        ↓
Data Encoding
        ↓
Train-Test Split
        ↓
Model Training
        ↓
Model Evaluation
        ↓
Prediction
```

---

#  Input Features

The model uses student behaviour features:

| Feature     | Description         |
| ----------- | ------------------- |
| Study Hours | Daily study time    |
| Sleep Hours | Daily sleeping time |
| Focus Score | Concentration level |
| Break Hours | Rest duration       |

---

#  Output

The system provides:

* Predicted study score
* Personalized study recommendations
* Progress analysis
* Learning history

---
