import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import textwrap

class pairPlot:
    def __init__(self, filename):
        self.df = pd.read_csv(filename)
    
    def pairPlot(self, ):
        features = self.df.select_dtypes(include=['float64', 'int64']).columns.tolist()
        if "Index" in features:
            features.remove("Index")
        
        size = len(features)

        fig, ax = plt.subplots(nrows=size, ncols=size, figsize=(10, 10))
        plt.subplots_adjust(wspace = 0.3, hspace = 0.3)

        for row in range(size):
            for col in range(size):
                X = self.df[features[col]]
                Y = self.df[features[row]]

                mask = ~X.isna() & ~Y.isna()
                X_clean = X[mask]
                Y_clean = Y[mask]

                if row == col:
                    # Histograma en la diagonal
                    ax[row, col].hist(X_clean, bins=20, alpha=0.5)
                else:
                    # Gráfico de dispersión fuera de la diagonal
                    ax[row, col].scatter(X_clean, Y_clean, alpha=0.5, s=1)
                
                # Configurar etiquetas de los ejes
                if row == size - 1:
                    label = "\n".join(textwrap.wrap(features[col], width=10))
                    ax[row, col].set_xlabel(label, fontsize=6, rotation=90, labelpad=6)
                    ax[row, col].tick_params(axis='x', labelsize=5, rotation=90)
                else:
                    ax[row, col].tick_params(labelbottom=False)

                if col == 0:
                    label = "\n".join(textwrap.wrap(features[row], width=10))
                    ax[row, col].set_ylabel(label, fontsize=6, rotation=0, labelpad=6, ha="right")
                    ax[row, col].tick_params(axis='y', labelsize=5)
                else:
                    ax[row, col].tick_params(labelleft=False)

                ax[row, col].spines['right'].set_visible(False)
                ax[row, col].spines['top'].set_visible(False)
        
        plt.show()


if __name__ == "__main__":
    filename = "dataset_train.csv"
    pair_plot = pairPlot(filename)
    pair_plot.pairPlot()

