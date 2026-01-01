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


def plot_category(df, location, category, output_path):
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

    years, values = zip(*sorted(zip(years, values)))

    plt.figure(figsize=(8, 4))
    plt.plot(years, values, marker="o")
    plt.title(f"{category}\n{location}")
    plt.xlabel("Rok")
    plt.ylabel("Wartość")
    plt.grid(True)
    plt.tight_layout()

    plt.savefig(output_path)
    plt.close()
