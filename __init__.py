import os
import time
import glob

from opensecrets import lobbying, pac, campaign_finance, reference

loaders = {m.__name__.split('.')[-1]:m for m in [lobbying,pac,campaign_finance,reference]}


def list_tables():
    tables = []
    for loader_name,loader in loaders.items():
        for table_name,(filename,columns) in loader.files_and_headers.items():
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


def load_df(table,**args):
    loader_name,table_name = table.split('.')

    loader = loaders[loader_name]

    return loader.load_df(table_name,**args)


if __name__ == '__main__':
    for table in list_tables():
        print(f"\n{table['table']}")
        print(f"\tExpected location:\n\t\t{table['path']}")
        if table['files']:
            print('\tFound:')
            for file in table['files']:
                modified = time.ctime(os.path.getmtime(file))
                print(f"\t\t{file}\tmodified: {modified}")

            try:
                df = load_df(table['table'])
                print(f'\tLoaded successfully ({len(df.columns)} columns, {len(df)} rows)')

            except Exception as e:
                print(f'Loading failed with error: {e}')
                break

        else:
            print('\t\tNo data found')
