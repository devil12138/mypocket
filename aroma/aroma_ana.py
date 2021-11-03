import pdfplumber as pr 
import pandas as pd
import re 
from io import StringIO
import numpy as np
import matplotlib.pyplot as plt
import os   
import sys
def data_filter(aromadir):
    if os.path.exists(aromadir):
        pdf_reports = os.listdir(aromadir)
        pdf_reports = [x for x in pdf_reports if  x[-4:] == '.pdf' and "32_15_p" in x]
        if not pdf_reports:
            raise Exception('the dir has no report file')
    else:
        raise Exception('sorry, the dir is not exist!') 
     
    result = temp = pd.DataFrame({})
    for report in pdf_reports:
        temp = get_pdfinfo(aromadir+report)
        result = pd.concat([result,temp],axis=1)
    return result
  


def get_pdfinfo(pdffile):
        try:
            with pr.open(pdffile) as pdf:
                content = ''
                for i in range(len(pdf.pages)):
                    page = pdf.pages[i]
                    page_content = '\n'.join(page.extract_text().split('\n')[2:-1])
                    content = content+page_content+'\n'
        except Exception as e:
            print(e)
            print(pdffile)
            os.system("rm -rf %s"%pdffile)
            return pd.DataFrame({})
        #正则提取
        temp = re.search('(峰表 TIC)(.*?)(谱库)', content, re.S)
        trial_name =  re.search('(样品名  :)(.*?)(\n)', content, re.S)
        temp = temp.group(2)
        temp = StringIO(temp)
        df = pd.read_table(temp, sep='  ', header=None, skiprows=2, skipfooter=1, engine='python')
        df[10] = df[10].fillna('')
        df[11] = df[11].fillna('')
        df[10] = df[10]+df[11]
        df = df.drop(labels=[9,11], axis=1)
        df[9] = trial_name.group(2)
        trial_name = trial_name.group(2)
        df = df.loc[:, [1, 4,9, 10]]
        df.columns = ['Rtime', 'area', 'sample_name', 'chemical_name']
        df['chemical_name'] = df['chemical_name'].apply(func = lambda x:x.strip())
        try:
            ns_area = df.loc[df['chemical_name']=='3-Nonanone', ['area']].values[0]
        except:
            print("无内标：", pdffile)
            return pd.DataFrame({})
            
        df[trial_name]  = df['area']/ns_area*0.65928
        df[trial_name] = df[trial_name].round(2)
        if any(df.duplicated(subset="chemical_name")):
            df.drop_duplicates(subset="chemical_name", inplace=True, keep="first")
        df.set_index("chemical_name", inplace=True)
        df = df[trial_name]
        return df

def draw_radar(result):
    result = data_standard(result, 1)
    # Each attribute we'll plot in the radar chart.
    labels = result.index
    
    # Number of variables we're plotting.
    num_vars = len(labels)
    
    # Split the circle into even parts and save the angles
    # so we know where to put each axis.
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    
    # The plot is a circle, so we need to "complete the loop"
    # and append the start value to the end.
    angles += angles[:1]
    
    # ax = plt.subplot(polar=True)
    fig, ax = plt.subplots(figsize=(15,15),  subplot_kw=dict(polar=True))
    
    # Helper function to plot each car on the radar chart.
    def add_to_radar(sameple):
      values = result[sample].tolist()
      values += values[:1]
      ax.plot(angles, values, linewidth=1, label=sample)
      ax.fill(angles, values, alpha=0.25)
    
    # Add each car to the chart.
    for sample in result.columns:
      add_to_radar(sample)
      #add_to_radar('peugeot 504 1979', '#429bf4')
      #add_to_radar('ford granada 1977', '#d42cea')
    
    # Fix axis to go in the right order and start at 12 o'clock.
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    
    # Draw axis lines for each angle and label.
    ax.set_thetagrids(np.degrees(angles[:-1]), labels)
    
    # Go through labels and adjust alignment based on where
    # it is in the circle.
    for label, angle in zip(ax.get_xticklabels(), angles):
      if angle in (0, np.pi):
        label.set_horizontalalignment('center')
      elif 0 < angle < np.pi:
        label.set_horizontalalignment('left')
      else:
        label.set_horizontalalignment('right')
    
    # Ensure radar goes from 0 to 100.
    #ax.set_ylim(0, 100)
    # You can also set gridlines manually like this:
    # ax.set_rgrids([20, 40, 60, 80, 100])
    
    # Set position of y-labels (0-100) to be in the middle
    # of the first two axes.
    ax.set_rlabel_position(180 / num_vars)
    
    # Add some custom styling.
    # Change the color of the tick labels.
    ax.tick_params(colors='#222222')
    # Make the y-axis (0-100) labels smaller.
    ax.tick_params(axis='y', labelsize=8)
    # Change the color of the circular gridlines.
    ax.grid(color='#AAAAAA')
    # Change the color of the outermost gridline (the spine).
    ax.spines['polar'].set_color('#222222')
    # Change the background color inside the circle itself.
    ax.set_facecolor('#FAFAFA')
    
    # Add title.
    ax.set_title('Comparing Cars Across Dimensions', y=1.08)
    
    # Add a legend as well.
    #ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
    ax.legend(loc='best')
    plt.tight_layout()
    fig.savefig("radar.png")
    os.system("termux-open radar.png")

def data_standard(result, axis=0):
    want = [".alpha.-Farnesene", "1-Butanol, 2-methyl-", "1-Hexanol", "2-Hexenal, (E)-","Hexanal", "Acetic acid, butyl ester","Acetic acid, hexyl ester"]
    result = result.loc[want, :]
    if axis:
        for raw in result.index:
            result.loc[raw] = result.loc[raw]/(result.loc[raw].sum())
    else:
        for col in result.columns:
            result[col] = (result[col])/(result[col].sum())
    return result


if __name__=="__main__":
    aromadir="../../bluetooth/aroma_report/"
    result=data_filter(aromadir)
    result.fillna(value=0, inplace=True)
    #result.to_csv("aroma.csv", sep=",")
    draw_radar(result)
    #result.to_csv("aroma.csv", sep=",")
    #ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
    #os.system("termux-open aroma.csv")
