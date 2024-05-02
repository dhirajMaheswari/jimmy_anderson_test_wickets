'''
this script will create the bar graph animation showing wickets by jimmy anderson over 
the time. 
'''

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

#functon to get flags, which are 100 * 100 pixels.
def get_flags(name):
    path = f"flags/{name}.png"
    im = plt.imread(path)
    return im

# function to add image/flag as axis labels
def offset_image(coord, name, ax):
    img = get_flags(name)
    im = OffsetImage(img, zoom=0.50)
    im.image.axes = ax
    ab = AnnotationBbox(im, (coord, 0),  xybox=(0., -18.), frameon=False, xycoords='data',
      boxcoords="offset points", pad=0)
    ax.add_artist(ab)


df = pd.read_csv("jimmy_anderson_stats.csv")

dfg = df.groupby(['Year','Opposition'])['Wickets'].sum().reset_index()
dfg['total'] = dfg['Wickets'].cumsum()

# function to draw from one year. this will be iterated over all the years
def graph_year(year):
    ax.clear()
    year_data = dfg[dfg['Year'] == year] # get the data relevant to the chosen year
    # sort the data by wickets in descending order
    year_data = year_data.sort_values('Wickets', ascending=0).reset_index()

    wickets = year_data['Wickets']
    opponents = year_data['Opposition']
    total = list(dfg[dfg['Year'] == year]['total'])

    bars = ax.bar(range(len(opponents)), wickets, width = 0.5, align='center')
    
    #loop over each bar to add labels appropriately.
    for bar, wick in zip(bars, wickets):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height()/2,f'{wick}',va = 'center', ha = 'center', size = 20, weight='bold')

    # add flags as axis labels
    for i, c in enumerate(year_data['Opposition']):
        offset_image(i,c.lower().replace(" ",''),ax)

    #ax.set_ylabel("Wickets",fontsize=24)
    ax.set_yticks([])
    ax.set_yticklabels([])
    ax.set_xticklabels([])
    ax.set_xticks([])
    ax.set_title(f"James Anderson Wickets in {year}", fontsize=36, pad=30)
    ax.text(1, 0.8, f'Total: {total[-1]}', transform=ax.transAxes, color='#777777',
         size=46, ha='right', weight=800)
    # remove the top, right and left line on the box surrounding the plot
    for sp in ['top','right','left']:
        ax.spines[sp].set_visible(False)

years = df['Year'].unique()
# animation object, #interval is time in milliseconds between frames
ani = FuncAnimation(fig, graph_year, frames=years, repeat=True, interval=500)
plt.show()

#ani.save("video_file_name.mp4", fps = 3) # 3 frames per second. 24 is standard frame rate
