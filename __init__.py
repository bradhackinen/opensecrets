import os, time, glob
from openSecrets import lobbying, pac, campaignFinance, reference

loaders = {m.__name__.split('.')[-1]:m for m in [lobbying,pac,campaignFinance,reference]}


def listTables():
    tables = []
    for loader_name,loader in loaders.items():
        for table_name,(filename,columns) in loader.filesAndHeaders.items():
            info = {'table':'.'.join([loader_name,table_name]),'status':'not found','files':[]}

            # if loader_name == 'campaignFinance':
            #     info['path'] = str(loader.path / 'CampaignFin*' / filename.replace('{}','*'))
            # else:
            info['path'] = str(loader.path/filename)

            info['files'] = glob.glob(info['path'])

            if info['files']:
                info['status'] = 'found'

            tables.append(info)

    return tables



def load(table,**args):
    loader_name,table_name = table.split('.')

    loader = loaders[loader_name]

    return loader.loadDF(table_name,**args)


# Create wrapper with old-style args for backwards compatibility
def loadDF(category,table,**args):
    return load(category + '.' + table,**args)


if __name__ == '__main__':
    for table in listTables():
        print(f"\n{table['table']}")
        print(f"\tExpected location:\n\t\t{table['path']}")
        if table['files']:
            print('\tFound:')
            for file in table['files']:
                modified = time.ctime(os.path.getmtime(file))
                print(f"\t\t{file}\tmodified: {modified}")

            try:
                df = loadDF(table['table'])
                print(f'\tLoaded successfully ({len(df.columns)} columns, {len(df)} rows)')
            except:
                print('Loading failed')
                break

        else:
            print('\t\tNo data found')
