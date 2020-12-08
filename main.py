import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def plotRollingSum(df, weeks, title, legend=True, figsize=[24,24], dpi=300):
    title += f' - {weeks} Week Rolling Sum'
    if weeks > 1:
        rolling = df.rolling(weeks).sum()
    else:
        rolling = df
    axes = rolling.plot(figsize=figsize, legend = legend)
    plt.title(title)

    if not legend:
        # Annotate jurisdiction names instead of using a legend
        for label, content in rolling.items():
            offset = content.idxmax()
            plt.annotate(label,
                         (offset, content[offset]),
                         textcoords="offset points",
                         xytext=(0,0),
                         ha='center')

    plt.savefig(f'{title}-{dpi}dpi.png', dpi=dpi)
    plt.show()

df = pd.read_csv('Weekly_counts_of_death_by_jurisdiction_and_cause_of_death_2020-12-06.csv',
                 # index_col=['Jurisdiction',
                 #            'Cause Group',
                 #            'Week Ending Date'],
                 usecols=['Week Ending Date',
                          'Jurisdiction',
                          'Cause Group',
                          'Number of Deaths',
                          'Type'],
                 dtype={'Cause Group' : 'category',
                        'Jurisdiction' : 'category',
                        'Type': 'category'},
                 parse_dates=['Week Ending Date'],
                 cache_dates=True)

# Remove duplicates created with the 'Type' column *sigh*
df = df[df['Type'] == 'Unweighted']
del df['Type']

jd = df.groupby(['Week Ending Date', 'Jurisdiction']).sum('Number of Deaths').unstack()
states = jd.drop(columns=jd.filter(like='United States').columns)
usa = jd.filter(like='United States')

for weeks in [52, 26, 13, 4, 2, 1]:
    plotRollingSum(states, weeks, "Total Deaths by CDC Jurisdiction", False)
    plotRollingSum(usa, weeks, "Total Deaths USA", True)
