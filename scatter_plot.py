import math
import pandas as pd
import itertools
import matplotlib.pyplot as plt

class scatterPlot:
    def __init__(self, filename):
        self.df = pd.read_csv(filename)

    def pearson_corr(self, x, y):
        if len(x) != len(y) or len(x) == 0:
            return float('nan')
        
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)

        numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
        sum_x = sum((xi - mean_x) ** 2 for xi in x)
        sum_y = sum((yi - mean_y) ** 2 for yi in y)
        denominator = math.sqrt(sum_x * sum_y)

        return numerator / denominator if denominator != 0 else 0
    
    def max_pearson(self):
        num_cols = self.df.select_dtypes(include=['float64', 'int64']).columns
        max_corr = -1
        best_pair = (None, None)

        for col1, col2 in itertools.combinations(num_cols, 2):
            # Eliminar filas con NaN solo en las columnas col1 y col2
            df_subset = self.df[[col1, col2]].dropna()
            x = df_subset[col1]
            y = df_subset[col2]

            if len(x) > 1:
                corr = x.corr(y)
                if abs(corr) > max_corr:
                    max_corr = abs(corr)
                    best_pair = (col1, col2)

        print(f"Coeficiente de Pearson máximo: {max_corr}")
        return best_pair

    
    def scatter_plot(self):
        best_pair = self.max_pearson()

        if best_pair == (None, None):
            print("No valid pair found for plotting")
        
        x, y = best_pair

        plt.figure(figsize=(8, 6))

        houses = self.df["Hogwarts House"].unique()
        colors = plt.colormaps.get_cmap("tab10")  # Asignar colores distintos

        for i, house in enumerate(houses):
            house_data = self.df[self.df["Hogwarts House"] == house]
            plt.scatter(
                house_data[x], house_data[y], 
                alpha=0.5, edgecolor='black', label=house, color=[colors(i)]
            )

        plt.xlabel(x)
        plt.ylabel(y)
        plt.title(f"Scatter Plot of {x} vs {y}")

        plt.legend()
        plt.grid(True)
        plt.show()


if __name__ == "__main__":
    filename = "dataset_train.csv"
    data_plot = scatterPlot(filename)
    data_plot.scatter_plot()
