import os
import time
import glob

from opensecrets import lobbying, pac, campaign_finance, reference, list_tables, load_df


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

        else:
            print('\t\tNo data found')
