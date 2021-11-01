import pdfplumber as pr 
import pandas as pd
import re 
from io import StringIO


def get_pdfinfo(pdffile)
    with pr.open('30_b_Rd.pdf') as pdf:
        content = ''
        for i in range(len(pdf.pages)):
            page = pdf.pages[i]
            page_content = '\n'.join(page.extract_text().split('\n')[2:-1])
            content = content+page_content+'\n'

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
        df = df.loc[:, [1, 4,9, 10]]
        df.columns = ['Rtime', 'area', 'sample_name', 'chemical_name']
        df['chemical_name'] = df['chemical_name'].apply(func = lambda x:x.strip())

        ns_area = df.loc[df['chemical_name']=='3-Nonanone', ['area']].values[0]
        df['content']  = df['area']/ns_area*0.65928
    return df


    :wqdef draw_radar(result):
    indexs = result.indexs

