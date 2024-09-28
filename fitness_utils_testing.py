# test_fitness_utils.py

from fitness_utils import calculate_bmi, generate_weight_graph

def test_calculate_bmi():
    # Test cases for BMI calculation
    assert abs(calculate_bmi(154, 5, 10) - 22.1) < 0.1, "Test Case 1 Failed"
    assert abs(calculate_bmi(180, 6, 0) - 24.4) < 0.1, "Test Case 2 Failed"
    assert abs(calculate_bmi(220, 5, 8) - 33.5) < 0.1, "Test Case 3 Failed"
    print("All BMI tests passed!")

def test_generate_weight_graph():
    # Test case for weight graph generation
    dates = ["2024-01-01", "2024-02-01", "2024-03-01", "2024-04-01"]
    weights_lbs = [154, 152, 150, 148]
    try:
        generate_weight_graph(dates, weights_lbs, "test_weight_graph.png")
        print("Weight graph test passed and saved as test_weight_graph.png!")
    except Exception as e:
        print(f"Weight graph test failed: {e}")

# Run the tests
if __name__ == "__main__":
    test_calculate_bmi()
    test_generate_weight_graph()