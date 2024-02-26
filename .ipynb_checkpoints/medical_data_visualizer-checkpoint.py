import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


# Import data
df = pd.read_csv('medical_examination.csv')




# Add an overweight column to the data. To determine if a person is overweight, first calculate their BMI by dividing their weight in kilograms by the square of their height in meters. If that value is > 25 then the person is overweight. Use the value 0 for NOT overweight and the value 1 for overweight.

# Add 'overweight' column set all to 0
df['overweight'] = 0

# label BMI > 25 as overweight (1)
df.loc[df['weight'] / ((df['height']/100)**2) > 25, 'overweight'] = 1




# Normalize the data by making 0 always good and 1 always bad. If the value of cholesterol or gluc is 1, make the value 0. If the value is more than 1, make the value 1.

#Normalize all values = 1 to 0
df.loc[df['cholesterol'] == 1, 'cholesterol'] = 0
df.loc[df['gluc'] == 1, 'gluc'] = 0

#normalize all values >1 to 1
df.loc[df['cholesterol'] > 1, 'cholesterol'] = 1
df.loc[df['gluc'] > 1, 'gluc'] = 1




# Convert the data into long format and create a chart that shows the value counts of the categorical features using seaborn's catplot(). The dataset should be split by 'Cardio' so there is one chart for each cardio value. The chart should look like examples/Figure_1.png.

# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'active', 'alco', 'cholesterol', 'gluc', 'overweight', 'smoke'.
    df_cat = pd.melt(df, id_vars = 'cardio', var_name = 'variable', value_vars = ['active', 'alco','cholesterol', 'gluc', 'overweight','smoke'])
    
    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. 
    df_cat = df_cat.groupby(['cardio', 'variable', 'value']).size().reset_index()
    
    # Rename one of the columns for the catplot to work correctly.
    df_cat = df_cat.rename(columns={0: 'total'})
      
    # Draw the catplot with 'sns.catplot()'
    catplot = sns.catplot(data=df_cat, x='variable', y='total', col='cardio', kind='bar', hue='value')

    # Get the figure for the output
    fig = catplot.fig

    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig
 



# Clean the data. Filter out the following patient segments that represent incorrect data:
# diastolic pressure is higher than systolic (Keep the correct data with (df['ap_lo'] <= df['ap_hi']))
# height is less than the 2.5th percentile (Keep the correct data with (df['height'] >= df['height'].quantile(0.025)))
# height is more than the 97.5th percentile
# weight is less than the 2.5th percentile
# weight is more than the 97.5th percentile

# Clean the data
df_heat = df[(df['ap_lo']<=df['ap_hi']) &
(df['height'] >= df['height'].quantile(0.025))&
(df['height'] <= df['height'].quantile(0.975))&
(df['weight'] >= df['weight'].quantile(0.025))&
(df['weight'] <= df['weight'].quantile(0.975))
]




# Create a correlation matrix using the dataset. Plot the correlation matrix using seaborn's heatmap(). Mask the upper triangle. The chart should look like examples/Figure_2.png.

# Draw Heat Map
def draw_heat_map():
    
    # Calculate the correlation matrix
    corr = df_heat.corr()
    
    # Generate a mask for the upper triangle
    mask = np.triu(corr)

    # Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(7, 5))

    # Draw the heatmap with 'sns.heatmap()'
    sns.heatmap(corr, mask=mask, fmt='.1f',vmax=.3, linewidths=.6,square=True, cbar_kws = {'shrink':0.5},annot=True, center=0)

    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig 
