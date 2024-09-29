import matplotlib.pyplot as plt

# Function to convert height in feet and inches to meters
def height_to_meters(feet, inches):

    total_inches = feet * 12 + inches
    return total_inches * 0.0254  # Convert inches to meters

# Function to convert weight in pounds to kilograms
def weight_to_kg(pounds):

    return pounds * 0.453592

# Function to calculate BMI
def calculate_bmi(weight_lbs, height_feet, height_inches):

    if height_feet <= 0 or height_inches < 0:
        raise ValueError("Height must be greater than zero.")
    if weight_lbs <= 0:
        raise ValueError("Weight must be greater than zero.")

    weight_kg = weight_to_kg(weight_lbs)
    height_m = height_to_meters(height_feet, height_inches)

    return weight_kg / (height_m ** 2)

# Function to generate weight over time graph
def generate_weight_graph(dates, weights_lbs, filename="weight_over_time.png"):

    if len(dates) != len(weights_lbs):
        raise ValueError("The length of dates and weights must match.")
    
    plt.figure(figsize=(10, 5))
    plt.plot(dates, weights_lbs, marker='o', color='b', linestyle='-')
    plt.title("Weight Over Time")
    plt.xlabel("Date")
    plt.ylabel("Weight (lbs)")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
    print(f"Weight graph saved as {filename}")
