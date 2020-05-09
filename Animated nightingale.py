import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors
import matplotlib.animation as animation
from matplotlib import font_manager as fm, rcParams
import seaborn as sns


# Read in data
df = pd.read_excel("fn_data-1.xlsx")

# Create new date variable to MM-YYYY
df["Month"]=df["Month"].str.strip()
df["Date"] = pd.to_datetime(df["Month"] + df["Year"].astype(str), format="%b%Y").dt.strftime('%m-%Y') 

#Remove deaths per million columns
df2=df.drop(["AMR_Zymotic_diseases","AMR_Wounds_injuries", "AMR_Other", "Month", "Year"],axis=1)

#Reshape dataframe
df3 = df2.melt(id_vars=["Date","Average_Army_Size"], 
               value_vars = ["Deaths_Zymotic_Diseases","Deaths_Wounds_Injuries","Deaths_Other"],
              var_name="cod", value_name="N")

#New variable for marker size
df3["ms"] = 10*df3["N"]

#List of causes of death in string format
cod_labels = ["Zymotic Diseases", "Wounds and Injuries", "Other Causes"]

cmap = plt.cm.coolwarm
norm = matplotlib.colors.Normalize(vmin=0, vmax=2000)

prop = fm.FontProperties(fname="SaucyJack.ttf")

bg = "#f2d7ac" 
fig, ax = plt.subplots(1,1,figsize=[15,15],facecolor=bg)
ax.set_facecolor(bg)


bubbles = ax.scatter(x=df3[df3["Date"]=="04-1854"]["cod"],y=df3[df3["Date"]=="04-1854"]["Date"], s=df3[df3["Date"]=="04-1854"]["ms"],c=cmap(norm(df3[df3["Date"]=="04-1854"]["N"].values)))

ax.set_xlim([-0.5,2.5])
ax.set_xticklabels(cod_labels,fontproperties=prop,fontsize=25)


ax.set_yticks(["04-1854","04-1855","03-1856"])
ax.set_yticklabels(["April 1854","April 1855","March 1856"],fontproperties=prop,fontsize=25)

ax.text(-1,-4,"The size and colour of each bubble is in proportion to the number of lives lost each month to each cause. ",
        fontproperties=prop,fontsize=20)

plt.title("Mortality of her Majesty's bravest soliders\n fighting in the East, April 1854 to March 1856",
          fontproperties=prop,fontsize=30,pad=20 )

sns.despine(left=True, bottom=True, right=True)
ax.tick_params(length=0)

df3=df3.reset_index()
months = np.array(df3[df3["Date"]!="04-1854"]["index"])

def animate(i):
    bubbles.clear()
    bubbles.set_offset([0,1,2],[i,i,i])
    bubbles.set_sizes(np.array(df3[df3["index"]==i]["N"]))
    bubbles.set_array(map(norm(df3[df3["index"]==i]["N"].values)))
    return bubbles

ani = animation.FuncAnimation(fig, animate, frames=months, interval=10)


plt.show()