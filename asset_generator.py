import json

MOCK_INPUTS = {
    'Product': 'Eco-Friendly Water Bottle',
    'Audience': 'Fitness Enthusiasts'
}

class MockGeminiModel:
    """
    Simulates the google.generativeai.GenerativeModel class.
    """
    def generate_content(self, prompt):
        """
        Simulates generating content based on a prompt.
        Returns a response object with a .text attribute containing JSON.
        """
        # Extract product and audience from prompt (simplified for mock)
        # In a real scenario, the model would understand the prompt.
        # Here we just return the pre-defined mock assets as a JSON string.
        
        mock_assets = {
            "Headlines": [
                "Stay Hydrated with the Best Eco-Friendly Water Bottle!",
                "The Ultimate Eco-Friendly Water Bottle for Fitness Enthusiasts.",
                "Eco-Conscious Hydration for Every Workout."
            ],
            "Slogans": [
                "Drink Green, Train Hard.",
                "Hydration Evolved.",
                "Your Partner in Fitness and Sustainability."
            ],
            "Social Media Posts": [
                "Hey Fitness Enthusiasts! Check out our new Eco-Friendly Water Bottle. It's perfect for your daily routine. #Fitness #EcoFriendly",
                "Upgrade your gear with the Eco-Friendly Water Bottle. Sustainable, durable, and stylish. Get yours today!",
                "Why choose between performance and the planet? With our Eco-Friendly Water Bottle, you get both."
            ]
        }
        
        class Response:
            text = json.dumps(mock_assets)
            
        return Response()

def generate_campaign_assets(inputs=MOCK_INPUTS):
    """
    Generates mock ad campaign assets using a Mock Gemini API.

    Args:
        inputs (dict): Dictionary containing 'Product' and 'Audience'.

    Returns:
        dict: Dictionary of generated assets (Headlines, Slogans, Social Media Posts).
    """
    product = inputs.get('Product', 'Product')
    audience = inputs.get('Audience', 'Audience')
    
    # Construct the prompt (simulating what we would send to the API)
    prompt = f"""
    Generate ad campaign assets for the following product:
    Product: {product}
    Target Audience: {audience}
    
    Return the output as a JSON object with the following keys:
    - Headlines (list of 3 strings)
    - Slogans (list of 3 strings)
    - Social Media Posts (list of 3 strings)
    """
    
    # Call the Mock API
    model = MockGeminiModel()
    response = model.generate_content(prompt)
    
    # Parse the JSON response
    try:
        assets = json.loads(response.text)
        return assets
    except json.JSONDecodeError:
        return {"Error": "Failed to parse JSON response from API."}

if __name__ == "__main__":
    print(f"Generating assets for inputs: {MOCK_INPUTS}\n")
    assets = generate_campaign_assets()
    
    print("--- RAW JSON OUTPUT ---")
    print(json.dumps(assets, indent=2))
    print("\n--- Parsed Assets ---")
    
    for category, items in assets.items():
        print(f"--- {category} ---")
        if isinstance(items, list):
            for item in items:
                print(f"- {item}")
        else:
            print(items)
        print()
