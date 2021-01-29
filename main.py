import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

def plotRollingSum(df, weeks, title, prefix='./plots', dpi=300, normalize=False, annotate=False, **kwargs):
    title += f' - {weeks} Week Rolling Sum'
    if weeks > 1:
        rolling = df.rolling(weeks).sum()
    else:
        rolling = df

    # Cut off unused part of sum
    rolling = rolling[weeks:]

    # Optionally normalize all the curves to the mean
    if normalize:
        rolling /= rolling.mean()

    axes = rolling.plot(title=title, **kwargs)

    # Annotate jurisdiction names
    if annotate:
        for label, content in rolling.items():
            offset = content.idxmax()
            plt.annotate(label,
                         (offset, content[offset]),
                         textcoords="offset points",
                         xytext=(0,0),
                         ha='center')

    plt.savefig(f'{prefix}/{title}-{dpi}dpi.png', dpi=dpi)
    plt.close()

# Ensure plots folder exists
dataPath = Path("./plots")
dataPath.mkdir(parents=True, exist_ok=True)

df = pd.read_csv('Weekly_counts_of_death_by_jurisdiction_and_cause_of_death.csv',
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
unweighted = df[df['Type'] == 'Unweighted']
del unweighted['Type']

jd = unweighted.groupby(['Week Ending Date', 'Jurisdiction']).sum('Number of Deaths').unstack()

# Reorder columns from most deaths to least
jd = jd.reindex(columns=jd.sum().sort_values(ascending=False).index)

states = jd.drop(columns=jd.filter(like='United States').columns)
usa = jd.filter(like='United States')


# Stacked plots requires reordering problematic states that don't keep up reporting or it looks confusing
problematicStates = ['North Carolina']
statesColumns = list(states.columns)
for item in problematicStates:
    statesColumns.sort(key=lambda s: s[1].startswith(item))

stackedStates = states.reindex(columns=statesColumns)

for weeks in [52, 26, 13, 4, 2]:
    # All jurisdictions in subplots
    plotRollingSum(jd, weeks, title="Total Deaths by CDC Jurisdiction Normalized to Mean - Subplots", normalize=True,
                   figsize=[36, 24], subplots=True, layout=[18, 3], sharey=True, grid=True)

    # Stacked in an area graph
    plotRollingSum(stackedStates, weeks, "Total Deaths by CDC Jurisdiction - Stacked", normalize=False,
                   figsize=[24,24], kind='area', legend='reverse', grid=True)

    plotRollingSum(states, weeks, "Total Deaths by CDC Jurisdiction - Line", normalize=False, annotate=True,
                   figsize=[24, 24], legend=True, grid=True)
    plotRollingSum(states, weeks, "Normalized Deaths by CDC Jurisdiction - Line", normalize=True, annotate=True,
                   figsize=[24, 24], legend='reverse', grid=True)

    plotRollingSum(usa, weeks, "Total Deaths USA", annotate=True, figsize=[24,24])

    #for jurisdiction in jd.columns:
    #    plotRollingSum(jd.filter(like=jurisdiction[1]), weeks=52, title="Total Deaths ")
