import pandas as pd
import sys
import math

from tabulate import tabulate

class csvStats:
    def __init__(self, filename):
        self.df = pd.read_csv(filename)
        self.statistics = {}
    
    def calcMean(self, values):
        suma = 0
        count = 0
        for i in values:
            if not pd.isna(i):
                suma += i 
                count += 1
        return (suma / count) if count > 0 else float('nan')

    def calcMin(self, values):
        if not values:
            return float('nan')

        min = None
        for i in values:
            if pd.isna(i):
                continue
            if min is None or i < min:
                min = i

        return min if min is not None else float('nan')

    def calcMax(self, values):
        if not values:
            return float('nan')

        max = None
        for i in values:
            if pd.isna(i):
                continue
            if max is None or i > max:
                max = i

        return max if max is not None else float('nan')

    def calcStd(self, values, mean):
        count = 0
        variance = 0
        for i in values:
            if not pd.isna(i):
                variance += (i - mean) ** 2
                count += 1
        return math.sqrt(variance / count) if count > 1 else float('nan')

    def calcPercentil(self, values, percentil):
        sortedValues = sorted([value for value in values if not pd.isna(value)])
        if not sortedValues:
            return float('nan')

        pk = (len(sortedValues) - 1) * percentil / 100
        f = math.floor(pk)
        c = math.ceil(pk)
        if f == c:
            return sortedValues[int(pk)]
        else:
            return sortedValues[f] + (pk -f) * (sortedValues[c] - sortedValues[f])

    def calculateStats(self):
        for col in self.df.select_dtypes(include=['float64', 'int64']).columns:

            if col.lower() == "index":
                continue

            values = self.df[col].tolist()

            count = len(values)
            mean = self.calcMean(values)
            std = self.calcStd(values, mean)
            minVal = self.calcMin(values)
            q25 = self.calcPercentil(values, 25)
            q50 = self.calcPercentil(values, 50)
            q75 = self.calcPercentil(values, 75)
            maxVal = self.calcMax(values)

            self.statistics[col] = {
                'Count' : count,
                'Mean' : mean,
                'Std' : std,
                'Min' : minVal,
                '25%' : q25,
                '50%' : q50,
                '75%' : q75,
                'Max' : maxVal
            }

    def printStats(self):
        metrics = list(next(iter(self.statistics.values())).keys())
        headers = ["Metric"] + list(self.statistics.keys())  
        
        table_data = []
        for metric in metrics:
            row = [metric] + [self.statistics[feature][metric] for feature in self.statistics.keys()]
            table_data.append(row)

        print(tabulate(table_data, headers=headers, tablefmt="grid", numalign="right", stralign="center"))


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: describe.py <archivo_csv>")
    else:
        filename = sys.argv[1]
        csv_stats = csvStats(filename)
        csv_stats.calculateStats()
        csv_stats.printStats()