import matplotlib.pyplot as plt
import numpy as np

def plot_historical_and_predicted_headcount(historical_data, predicted_year, predicted_headcount, current_headcount):
    """
    Plots the historical headcount data and the predicted headcount, including the number of additional employees required.

    Args:
        historical_data (pd.DataFrame): Historical data containing "ANO" and "HEADCOUNT".
        predicted_year (int): The year for the predicted headcount.
        predicted_headcount (float): The predicted headcount value.
        current_headcount (int): The current number of employees.
    """
    historical_years = historical_data["ANO"]
    historical_headcount = historical_data["HEADCOUNT"]

    # Calculate additional employees required
    additional_needed = max(0, int(np.ceil(predicted_headcount - current_headcount)))

    # Plot the historical data and prediction
    plt.figure(figsize=(12, 6))

    # Plot historical data
    plt.plot(
        historical_years, historical_headcount, marker="o", label="Historical Headcount"
    )

    # Add the prediction as a distinct point
    plt.scatter(
        [predicted_year], [predicted_headcount], color="red", label=f"Predicted Headcount ({predicted_year})"
    )

    plt.annotate(
        f"+{additional_needed} employees" if additional_needed > 0 else "No additional employees needed",
        (predicted_year, predicted_headcount),
        textcoords="offset points",
        xytext=(0, 10),
        ha="center",
        fontsize=10,
        color="blue",
        fontweight="bold"
    )

    plt.title("Historical and Predicted Headcount", fontsize=16)
    plt.xlabel("Year", fontsize=12)
    plt.ylabel("Headcount", fontsize=12)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend(fontsize=10)
    plt.tight_layout()
    plt.show()
