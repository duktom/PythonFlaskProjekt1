from flask import Flask, render_template, request
from plotter import load_data, get_categories, plot_category

app = Flask(__name__)

CSV_PATH = "data.csv"
PLOT_PATH = "static/plot.png"

df = load_data(CSV_PATH)

@app.route("/", methods=["GET", "POST"])
def index():
    locations = sorted(df["Nazwa"].unique())
    categories = get_categories(df)

    selected_location = None
    selected_category = None

    if request.method == "POST":
        selected_location = request.form["location"]
        selected_category = request.form["category"]

        plot_category(
            df,
            selected_location,
            selected_category,
            PLOT_PATH
        )

    return render_template(
        "index.html",
        locations=locations,
        categories=categories,
        selected_location=selected_location,
        selected_category=selected_category
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
