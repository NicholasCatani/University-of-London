"""
Skeleton Code for Weather Classification Midterm assessment (25%)

Instructions:
1. Complete each function where indicated.
2. You may add helper functions or import additional libraries if necessary.
3. Ensure you do not rename any of the existing function names, as the autograder relies on them.
4. Save and run: python weather_forecast.py
"""

#####################
# Import required libraries
#####################
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

#####################
# PART A: DATA LOADING
#####################

def load_data(csv_filepath):
    """
    Load the weather_data CSV into a pandas DataFrame.
    :param csv_filepath: str, path to weather_data.csv
    :return: pd.DataFrame
    """
    df = pd.read_csv(csv_filepath)
    return df


def clean_data(df):
    """
    Perform basic data cleaning:
    - Drop or fill missing values
    - Convert date column to datetime
    :param df: pd.DataFrame
    :return: pd.DataFrame (cleaned)
    """
    df = df.dropna()
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    
    ### In case some data points became NaT
    df = df.dropna(subset=["date"])
    return df


#####################
# PART B: FEATURE ENGINEERING
#####################

def feature_engineering(df):
    """
    Create or transform features, for example:
    - temp_range = temp_max - temp_min
    - month from date
    - is_freezing if temp_min < 0
    - convert 'weather' to numeric labels
    :param df: pd.DataFrame
    :return: pd.DataFrame with new features + encoded target
    """
    df["temp_range"] = df["temp_max"] - df["temp_min"]
    df["month"] = df["date"].dt.month
    df["is_freezing"] = (df["temp_min"] < 0).astype(int)
    
    ### Extra step to clean typos when generating new labels
    df["weather"].str.lower().str.strip()
    df["weather_label"] = df["weather"].map({
        "drizzle": 0, 
        "rain": 1, 
        "sun": 2, 
        "snow": 3, 
        "fog": 4
      })
    
    return df


#####################
# PART C: DATA SPLITTING
#####################

def split_data(df):
    """
    Split the data into train/test sets.
    :param df: pd.DataFrame with feature columns and 'weather_label' (the target)
    :return: X_train, X_test, y_train, y_test
    """
    features = ["month", "precipitation", "wind", "is_freezing", "temp_max", "temp_min", "temp_range"]

    X = df[features] 
    y = df["weather_label"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state= 42)

    return X_train, X_test, y_train, y_test


#####################
# PART D: MODEL TRAINING
#####################

def train_model_logreg(X_train, y_train):
    """
    Train a LogisticRegression model using X_train, y_train.
    :return: fitted logistic regression model
    """
    lr_model = LogisticRegression(random_state=42, solver="liblinear").fit(X_train, y_train)
    return lr_model 


def train_model_rf(X_train, y_train):
    """
    Train a RandomForestClassifier using X_train, y_train.
    :return: fitted random forest model
    """
    rf_model = RandomForestClassifier(random_state=42).fit(X_train, y_train)
    return rf_model


#####################
# PART E: EVALUATION
#####################

def evaluate_model(model, X_test, y_test):
    """
    Generate predictions for X_test using the trained model
    and print (or return) the accuracy and classification report.
    :return: (accuracy, report_text) or something similar
    """
    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    # matrix = confusion_matrix(y_test, y_pred)

    return accuracy, report


#####################
# DEMO MAIN (optional)
#####################

if __name__ == "__main__":
    """
    Optional: You can test your functions here.
    This block won't affect the autograder.
    """
    csv_path = "./data/weather-data.csv"
    try:
        df_loaded = load_data(csv_path)
        df_cleaned = clean_data(df_loaded)
        df_features = feature_engineering(df_cleaned)
        X_train, X_test, y_train, y_test = split_data(df_features)

        modelA = train_model_logreg(X_train, y_train)
        modelB = train_model_rf(X_train, y_train)

        accA, repA = evaluate_model(modelA, X_test, y_test)
        accB, repB = evaluate_model(modelB, X_test, y_test)

        print(f'\nLogistic Regression Accuracy: {accA} {repA}')
        print(f'\nRandom Forest Accuracy: {accB} {repB}')
    except NotImplementedError:
        print("Please implement the required functions before running.")
