from pathlib import Path
import pandas as pd

from openSecrets.config import data_dir

path = Path(data_dir) / 'reference'

files_and_headers = {
                    'categories':('CRP_Categories.txt',
                                    [
                                        'Catcode',
                                        'Catname',
                                        'Catorder',
                                        'Industry',
                                        'Sector',
                                        'Sector Long'
                                        ]),
                    }


def load_df(table):

    f,headers = files_and_headers[table]

    df = pd.read_csv(path/f,sep='\t',quotechar='|',names=headers,index_col=False,header=None,skiprows=list(range(10)))

    return df
