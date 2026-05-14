import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
data = pd.read_csv('uploadedfile/causes.csv')
sns.countplot(x='Type',data=data)
plt.xticks(rotation=90)
plt.show()