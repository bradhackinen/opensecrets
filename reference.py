import os
import pandas as pd

from openSecrets.dirs import *

def loadDF(table):
    if table == 'categories':
        df = pd.read_csv(os.path.join(referenceDataDir,'CRP_categories.csv'))
        df.columns = [s.lower().replace(' ','_') for s in df.columns]
        return df
