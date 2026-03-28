# 🏋️ Body Performance Analytics & Intelligent Classification System

![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=for-the-badge&logo=streamlit)
![Scikit-Learn](https://img.shields.io/badge/Machine%20Learning-Scikit--Learn-orange?style=for-the-badge&logo=scikit-learn)

An end-to-end Machine Learning solution that transforms biometric and physical data into actionable fitness insights. This project implements a dual-model approach: **Classifying** individuals into fitness grades and **Predicting** athletic explosive power (Broad Jump) through regression.

---

## 📌 Project Overview
The "Body Performance" project follows the complete Data Science lifecycle to solve two primary problems:
1.  **Multi-Class Classification:** Assigning an individual to one of four performance categories (**A, B, C, D**) based on their physical metrics.
2.  **Regression Analysis:** Estimating the **Broad Jump distance (cm)**, a key indicator of lower-body explosive strength.

### Key Highlights
* **Dataset:** 13,392 records with 12 physiological and performance features.
* **Best Classifier:** Neural Network (MLP) achieving **74.65% accuracy**.
* **Best Regressor:** Linear Regression achieving an **R² score of 0.79**.
* **Deployment:** Live interactive dashboard built with **Streamlit**.
![licensed-image](https://github.com/user-attachments/assets/c7e6e26e-e2dd-4017-96a2-dce3ec6e1918)

---

## 📊 The Data Science Pipeline

### 1. Data Cleaning & Preparation
* Handled data quality violations and removed duplicate records.
* Feature engineering: Standardized units and encoded categorical variables (Gender).
* **Scaling:** Applied `MinMaxScaler` to normalize features for Neural Network sensitivity.

### 2. Exploratory Data Analysis (EDA)
* **Balanced Classes:** Verified that the four grades (A-D) are evenly distributed (~25% each).
* **Correlation Analysis:** Discovered that **Flexibility (Sit & Bend)** and **Core Endurance (Sit-ups)** are the strongest predictors of overall fitness grades.

### 3. Modeling & Evaluation
We compared several models including SVM, Random Forest, Naive Bayes, and Neural Networks.
* **Classification:** The **MLP (128, 64 nodes)** outperformed others by effectively capturing non-linear relationships in the biometric data.
* **Regression:** While SVR performed well, **Linear Regression** was chosen for deployment due to its high interpretability—allowing coaches to see exactly how much each feature impacts performance.

---

## 🚀 Installation & Local Usage

### Prerequisites
* Python 3.9 or higher
* Git

### Setup
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YourUsername/Body-Performance-Analytics.git](https://github.com/YourUsername/Body-Performance-Analytics.git)
   cd Body-Performance-Analytics
