import pandas as pd
import numpy as np
import random
from faker import Faker
from datetime import datetime, timedelta

def generate_campaign_data(days=30, num_campaigns=3):
    """
    Generates a Pandas DataFrame simulating ad campaign performance with correlated data
    and a specific negative trend scenario.

    Args:
        days (int): Number of days of data to generate per campaign.
        num_campaigns (int): Number of different campaigns to simulate.

    Returns:
        pd.DataFrame: DataFrame containing campaign data.
    """
    fake = Faker()
    data = []
    
    # Generate Campaign IDs and Names
    campaigns = []
    for i in range(num_campaigns):
        campaigns.append({
            "id": fake.uuid4(),
            "name": f"Campaign_{fake.word().capitalize()}_{i+1}"
        })
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    # Select one campaign to have a negative trend (rising CPA)
    bad_campaign_index = 0 
    
    for idx, campaign in enumerate(campaigns):
        # Base metrics for the campaign
        base_impressions = np.random.randint(1000, 10000)
        
        # Daily data generation
        current_date = start_date
        for day_num in range(days):
            date_str = current_date.strftime("%Y-%m-%d")
            
            # Daily variance for impressions
            daily_impressions = int(base_impressions * np.random.uniform(0.8, 1.2))
            
            # CTR: 1% to 5%
            ctr = np.random.uniform(0.01, 0.05)
            daily_clicks = int(daily_impressions * ctr)
            
            # CPC and CVR
            cpc = np.random.uniform(0.5, 1.5)
            cvr = np.random.uniform(0.05, 0.15)
            
            # Negative Trend Scenario: Rising CPA after Day 20 for the first campaign
            # CPA = Cost / Conversions = (Clicks * CPC) / (Clicks * CVR) = CPC / CVR
            # To increase CPA, we can increase CPC or decrease CVR.
            if idx == bad_campaign_index and day_num > 20:
                cpc = cpc * np.random.uniform(1.5, 2.5) # Drastic increase in CPC
                cvr = cvr * np.random.uniform(0.5, 0.8) # Decrease in CVR
            
            daily_cost = round(daily_clicks * cpc, 2)
            daily_conversions = int(daily_clicks * cvr)
            
            data.append({
                "Date": date_str,
                "Campaign_ID": campaign["id"],
                "Campaign_Name": campaign["name"],
                "Impressions": daily_impressions,
                "Clicks": daily_clicks,
                "Cost": daily_cost,
                "Conversions": daily_conversions
            })
            
            current_date += timedelta(days=1)

    df = pd.DataFrame(data)
    return df

def generate_click_logs(num_clicks=1000):
    """
    Generates a Pandas DataFrame simulating raw click logs.

    Args:
        num_clicks (int): Number of click logs to generate.

    Returns:
        pd.DataFrame: DataFrame containing click logs.
    """
    fake = Faker()
    data = []

    # Generate some random Campaign IDs to pick from
    campaign_ids = [fake.uuid4() for _ in range(5)]

    # Normal traffic
    for _ in range(num_clicks):
        data.append({
            "Timestamp": fake.date_time_between(start_date="-30d", end_date="now"),
            "IP_Address": fake.ipv4(),
            "User_Agent": fake.user_agent(),
            "Campaign_ID": random.choice(campaign_ids),
            "Click_ID": fake.uuid4()
        })
    
    # Fraud Scenario: 200 clicks from one IP in 5 minutes
    fraud_ip = "192.168.0.666"
    fraud_campaign_id = random.choice(campaign_ids)
    
    # Pick a random start time for the burst within the last 30 days
    burst_start_time = fake.date_time_between(start_date="-30d", end_date="now")
    
    for i in range(200):
        # Time within 5 minutes of start
        click_time = burst_start_time + timedelta(seconds=random.randint(0, 300))
        
        # 50% chance of being a Bot UA
        if i < 100: # First 100 are bots (simple way to ensure 50%)
             user_agent = "Bot/1.0"
        else:
             user_agent = fake.user_agent()
             
        data.append({
            "Timestamp": click_time,
            "IP_Address": fraud_ip,
            "User_Agent": user_agent,
            "Campaign_ID": fraud_campaign_id,
            "Click_ID": fake.uuid4()
        })

    df = pd.DataFrame(data)
    # Sort by timestamp to make it look realistic
    df = df.sort_values(by="Timestamp").reset_index(drop=True)
    return df

if __name__ == "__main__":
    print("--- Campaign Data ---")
    df_campaign = generate_campaign_data()
    print(df_campaign.head())
    
    print("\n--- Click Logs ---")
    df_clicks = generate_click_logs()
    print(df_clicks.head())
    print(f"Generated {len(df_clicks)} click logs.")
    
    # Verification of Fraud Scenario
    print("\n--- Fraud Scenario Verification ---")
    fraud_ip = "192.168.0.666"
    fraud_data = df_clicks[df_clicks["IP_Address"] == fraud_ip]
    print(f"Clicks from {fraud_ip}: {len(fraud_data)}")
    
    if not fraud_data.empty:
        min_time = fraud_data["Timestamp"].min()
        max_time = fraud_data["Timestamp"].max()
        duration = (max_time - min_time).total_seconds()
        print(f"Duration of attack: {duration} seconds")
        
        bot_ua_count = len(fraud_data[fraud_data["User_Agent"] == "Bot/1.0"])
        print(f"Bot User Agents count: {bot_ua_count}")


