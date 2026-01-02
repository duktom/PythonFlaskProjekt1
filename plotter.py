import pandas as pd
import matplotlib.pyplot as plt

def load_data(csv_path):
    return pd.read_csv(csv_path, sep=";")

def get_categories(df):
    categories = set()
    for col in df.columns:
        if ";" in col and col.split(";")[1].isdigit():
            categories.add(col.split(";")[0])
    return sorted(categories)

def plot_category_multi_location(df, locations, category, output_path):
    plt.figure(figsize=(9, 5))

    for location in locations:
        row = df[df["Nazwa"] == location].iloc[0]

        years = []
        values = []

        for col in df.columns:
            if col.startswith(category):
                year = int(col.split(";")[1])
                value = row[col]

                if pd.notna(value):
                    value = float(str(value).replace(",", "."))
                    years.append(year)
                    values.append(value)

        if years:
            years, values = zip(*sorted(zip(years, values)))
            plt.plot(years, values, marker="o", label=location)

    plt.title(category)
    plt.xlabel("Rok")
    plt.ylabel("Wartość")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
