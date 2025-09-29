# Personalized Health Risk Assessment System

This project is a health advice system that predicts potential health risks based on user-provided metrics. It then suggests personalized recommendations to help mitigate these risks. The system is built with a machine learning pipeline and exposed through a user-friendly web interface.

---

## Project Structure

```
.
├── data/                           # Dataset directory
│   ├── processed/
│   │   └── train_cleaned.csv       # Preprocessed dataset
│   ├── train_dataset.csv
│   └── test_dataset.csv
├── models/
│   └── risk_model.joblib           # Trained classfication model
├── src/
│   ├── data_processing.py          # Data analysis and preprocessing
│   ├── model_training.py           # Model training
│   ├── predictor.py                # Model evaluation
│   └── recommendation_engine.py    # Generates personalized health recommendations based on prediction results
├── app.py
├── requirements.txt
└── README.md
```

## Setup

Follow these steps to set up and run the project locally.

### 1. Prerequisites

-   Python 3.10.11 or higher
-   `pip` and `venv`

### 2. Installation & Setup

First, clone the repository and install the required dependencies.

```bash
# Clone the repository
git clone https://git.bdata.top:9443/mockproject/n2_healthadviceai.git

# Navigate to the project directory
cd n2_healthadviceai

# Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate

# Install the required packages
pip install -r requirements.txt
```
### 3. Data Processing & Model Training

Next, run the scripts to process the raw data and train the machine learning model. This is a one-time setup step.

```bash
# Run the data processing script
python src/data_processing.py

# Run the model training script
python src/model_training.py
```
This will generate the cleaned dataset in `data/processed/` and the trained model file `risk_model.joblib` in the `models/` directory.

### 4. Running the application

Finally, launch the main application.

```bash
python app.py
```

## Project Workflow

The project follows a complete data science pipeline:

1. **Data Processing** (`src/data_processing.py`):

   - Loads the raw dataset from `data/`.

   - Performs cleaning operations such as handling missing values, correcting data types, and removing inconsistencies.

   - Saves the cleaned, analysis-ready dataset to `data/processed/`.

2. **Model Training** (`src/model_training.py`):

    - Loads the processed data.

    - Splits the data into training and testing sets.

    - Trains a classification model to predict health risks.

    - Serializes and saves the trained model to `models/risk_model.joblib`.

3. **Prediction** (`src/predictor.py`):
    
    - A module responsible for loading the saved model (`risk_model.joblib`).

    - Provides a function to make predictions on new, unseen user input.

4. **Recommendation Engine** (`src/recommendation_engine.py`):

    - Contains the logic for generating personalized advice.

    - Maps the model's prediction output to a set of actionable recommendations.

5. **Web Application**  (`app.py`):

    - The main entry point that integrates all modules.

    - Provides a user interface (UI) for inputting health metrics.

    - Calls the predictor and recommendation engine to display the final results to the user.

## Performance

The model achieves:
- Accuracy: 99%
- Precision: 100%
- Recall: 99%
- F1-score: 99%

## Requirement

- Python 3.x

- scikit-learn

- pandas

- numpy

- joblib

- streamlit