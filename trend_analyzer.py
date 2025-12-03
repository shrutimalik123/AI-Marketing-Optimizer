import pandas as pd

def analyze_trends(df):
    """
    Analyzes campaign data to detect trends, specifically rising CPA.

    Args:
        df (pd.DataFrame): Campaign performance data.

    Returns:
        list: List of insight strings describing detected trends.
    """
    insights = []
    
    if df.empty:
        return ["No data available for analysis."]

    # Ensure data is sorted by date
    df = df.sort_values(by="Date")
    
    # Calculate CPA safely
    df["CPA"] = df["Cost"] / df["Conversions"].replace(0, 1)

    campaigns = df["Campaign_Name"].unique()
    
    for campaign in campaigns:
        camp_data = df[df["Campaign_Name"] == campaign]
        
        if len(camp_data) < 15:
            continue # Not enough data for baseline vs recent comparison
            
        # Baseline: First 10 days
        baseline_data = camp_data.head(10)
        baseline_cpa = baseline_data["CPA"].mean()
        
        # Recent: Last 5 days
        recent_data = camp_data.tail(5)
        recent_cpa = recent_data["CPA"].mean()
        
        # Check for rising CPA (e.g., > 50% increase)
        if recent_cpa > 1.5 * baseline_cpa:
            increase_pct = ((recent_cpa - baseline_cpa) / baseline_cpa) * 100
            insights.append(
                f"⚠️ **Rising CPA Detected**: Campaign '{campaign}' shows a {increase_pct:.1f}% increase in CPA recently "
                f"(${recent_cpa:.2f}) compared to its baseline (${baseline_cpa:.2f})."
            )
            
    if not insights:
        insights.append("✅ No significant negative trends detected. Campaigns are performing stably.")
        
    return insights

if __name__ == "__main__":
    from mock_data_generator import generate_campaign_data
    
    print("Generating mock data...")
    df = generate_campaign_data()
    
    print("Analyzing trends...")
    insights = analyze_trends(df)
    
    print("\n--- AI Insights ---")
    for insight in insights:
        print(insight)
