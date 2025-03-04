import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from describe import csvStats

class histogram:
    def __init__(self, filename):
        self.df = pd.read_csv(filename)
        self.csv_stats = csvStats(filename)
    
    def calcHomogeneity(self, course, houses):
        house_means = []
        house_stds = []

        for house in houses:
            house_scores = self.df[self.df["Hogwarts House"] == house][course].dropna()
            mean_score = self.csv_stats.calcMean(house_scores)
            std_dev = self.csv_stats.calcStd(house_scores, mean_score)

            if not np.isnan(mean_score) and not np.isnan(std_dev):
                house_means.append(mean_score)
                house_stds.append(std_dev)

        if len(house_means) < 2 or len(house_stds) < 2:
            return float('inf')

        mean_std = self.csv_stats.calcStd(house_means, self.csv_stats.calcMean(house_means))  
        std_std = self.csv_stats.calcStd(house_stds, self.csv_stats.calcMean(house_stds))  

        return mean_std + std_std


    def plotHistograms(self):
        houses = self.df["Hogwarts House"].unique()
        courses = list(self.df.select_dtypes(include=['float64', 'int64']).columns)

        if "Index" in courses:
            courses.remove("Index")
        
        homogeneity_scores = {}

        for course in courses:
            homogeneity_scores[course] = self.calcHomogeneity(course, houses)

        min_value = self.csv_stats.calcMin(list(homogeneity_scores.values()))
        for course, value in homogeneity_scores.items():
            if value == min_value:
                most_homogeneous_course = course
                break

        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        axes = axes.flatten()

        for idx, house in enumerate(houses):
            ax = axes[idx]
            house_scores = self.df[self.df["Hogwarts House"] == house][most_homogeneous_course].dropna()
            ax.hist(house_scores, bins=50, alpha=0.6, edgecolor='black', color=np.random.rand(3,))
            ax.set_title(house)
            ax.set_xlabel(most_homogeneous_course)
            ax.set_ylabel("Frequency")

        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    filename = "dataset_train.csv"
    hist = histogram(filename)
    hist.plotHistograms()