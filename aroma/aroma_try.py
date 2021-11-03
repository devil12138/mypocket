import pygal 
import pandas as pd
import sys
"""
df = pd.DataFrame({"Zhu":[15,17,19], "Wu":[23,27,29], "Zhao":[12,7,11]}, index=["english", "chinese", "math"])

radar = pygal.Radar()
radar.title = "final exam result"
radar.x_labels = df.index
for stu in df.columns:
    radar.add(stu, df[stu].tolist())

radar.render_to_png("test.png")
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


