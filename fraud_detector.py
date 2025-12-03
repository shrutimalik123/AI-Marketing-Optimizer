import pandas as pd
from sklearn.ensemble import IsolationForest

def detect_fraud(df):
    """
    Detects suspicious IPs using Isolation Forest based on click behavior.

    Args:
        df (pd.DataFrame): Raw click logs DataFrame.

    Returns:
        list: List of suspicious IP addresses.
    """
    if df.empty:
        return []

    # Feature Engineering: Aggregate by IP
    ip_stats = df.groupby('IP_Address').agg(
        click_count=('Click_ID', 'count'),
        unique_uas=('User_Agent', 'nunique'),
        unique_campaigns=('Campaign_ID', 'nunique'),
        min_time=('Timestamp', 'min'),
        max_time=('Timestamp', 'max')
    ).reset_index()

    # Calculate duration in seconds
    ip_stats['duration'] = (ip_stats['max_time'] - ip_stats['min_time']).dt.total_seconds()
    
    # Calculate click rate (clicks per second), handling zero duration
    ip_stats['click_rate'] = ip_stats['click_count'] / (ip_stats['duration'] + 1)

    # Features for the model
    features = ['click_count', 'unique_uas', 'unique_campaigns', 'click_rate']
    X = ip_stats[features]

    # Initialize and fit Isolation Forest
    # contamination='auto' or a small float like 0.01 if we expect rare fraud
    iso_forest = IsolationForest(contamination=0.01, random_state=42)
    ip_stats['anomaly'] = iso_forest.fit_predict(X)

    # Filter for anomalies (-1)
    suspicious_ips = ip_stats[ip_stats['anomaly'] == -1]['IP_Address'].tolist()
    
    return suspicious_ips

if __name__ == "__main__":
    # Test with mock data
    from mock_data_generator import generate_click_logs
    
    print("Generating mock data with fraud scenario...")
    df = generate_click_logs()
    
    print("Running fraud detection...")
    suspicious = detect_fraud(df)
    
    print(f"Suspicious IPs detected: {suspicious}")
    
    # Verify if our known fraud IP is in the list
    fraud_ip = "192.168.0.666"
    if fraud_ip in suspicious:
        print(f"SUCCESS: Detected known fraud IP {fraud_ip}")
    else:
        print(f"FAILURE: Did not detect known fraud IP {fraud_ip}")
