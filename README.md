# AI Marketing Optimizer

The **AI Marketing Optimizer** is a comprehensive tool designed to protect ad budgets and optimize campaign performance using data analysis and AI simulation. It features a real-time dashboard for monitoring campaign metrics, detecting fraud, analyzing trends, and generating creative assets.

## Features

### 1. 📊 Campaign Data Simulation
- Generates realistic mock data for ad campaigns using `numpy` and `faker`.
- Simulates correlated metrics (Impressions, Clicks, Cost, Conversions) with daily variance.
- **Scenario Injection**: Simulates specific negative trends (e.g., rising CPA) to test analysis logic.

### 2. 🛡️ Fraud Detection System
- **Model**: Uses `sklearn.ensemble.IsolationForest` to detect anomalies in click logs.
- **Simulation**: Injects synthetic fraud scenarios (e.g., high-velocity clicks from a single IP with bot User Agents).
- **Dashboard**: Interactive UI to generate click logs and flag suspicious IPs in real-time.

### 3. 📈 AI Trend Analysis
- Automatically analyzes campaign performance to detect negative trends.
- **Logic**: Compares recent performance (last 5 days) against a baseline (first 10 days) to identify rising Cost Per Acquisition (CPA).
- **Insights**: Displays actionable warnings in the dashboard.

### 4. ✍️ Ad Asset Generator
- **Mock Gemini API**: Simulates an AI content generator (`MockGeminiModel`) to create ad copy.
- **Outputs**: Generates Headlines, Slogans, and Social Media Posts based on product and audience inputs.
- **Verification**: Displays raw JSON output to verify structured data handling.

## Installation

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd AI-Marketing-Optimizer
    ```

2.  **Install dependencies**:
    ```bash
    pip install streamlit pandas numpy faker scikit-learn
    ```

## Usage

1.  **Run the Dashboard**:
    ```bash
    streamlit run app.py
    ```

2.  **Navigate**: Open your browser to `http://localhost:8501`.

3.  **Explore**:
    - View **Campaign Performance** metrics and charts.
    - Check **AI Insights** for trend warnings.
    - Use the **Ad Asset Generator** to create new copy.
    - Run the **Fraud Detection System** to catch suspicious activity.

## Project Structure

- `app.py`: Main Streamlit dashboard application.
- `mock_data_generator.py`: Scripts for generating campaign and click log data.
- `fraud_detector.py`: Logic for the Isolation Forest fraud detection model.
- `trend_analyzer.py`: Functions for analyzing CPA trends.
- `asset_generator.py`: Mock AI model for generating ad assets.
