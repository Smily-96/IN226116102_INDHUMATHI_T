# Sentiment Analysis using NLP Pipeline & ML Models

## Overview
This project builds an end-to-end sentiment analysis system using Amazon product review datasets. The goal is to process raw text data using NLP techniques and apply machine learning models to classify sentiment as positive, neutral, or negative.

## Dataset
The dataset is collected from Kaggle and includes Amazon product reviews. Three datasets were combined into a single dataset for analysis.

## NLP Preprocessing
The following preprocessing steps were applied:
- Lowercasing
- Removal of punctuation and special characters
- Removal of URLs and unwanted patterns
- Removal of stopwords
- Tokenization
- Lemmatization

## Feature Engineering
Two techniques were used:
- Bag of Words (BoW)
- TF-IDF

## Models Used
- Logistic Regression
- Naive Bayes
- Decision Tree

## Evaluation Metrics
The models were evaluated using:
- Accuracy
- Precision
- Recall
- F1 Score

## Results
Logistic Regression with Bag of Words achieved the best performance with the highest accuracy.

## Key Insights
- Preprocessing significantly improved model performance
- TF-IDF gives better weighting but BoW performed slightly better here
- Dataset is imbalanced (more positive reviews)

## Conclusion
This project demonstrates the complete NLP pipeline from raw text to sentiment prediction using machine learning models.

## How to Run
1. Open the notebook in Google Colab
2. Mount Google Drive
3. Load and preprocess dataset
4. Run all cells

## Author
Indhumathi T