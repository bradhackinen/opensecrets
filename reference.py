from pathlib import Path
import pandas as pd

from openSecrets.config import dataDir

path = Path(dataDir) / 'reference'

filesAndHeaders = {
                'categories':('CRP_Categories.txt',['Catcode','Catname','Catorder','Industry','Sector','Sector Long']),
        }


def loadDF(table):

    f,headers = filesAndHeaders[table]

    df = pd.read_csv(path/f,sep='\t',quotechar='|',names=headers,index_col=False,header=None,skiprows=list(range(10)))

    return df


loadDF('categories')
