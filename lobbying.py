import os
from pathlib import Path
import pandas as pd

from opensecrets.config import data_dir

path = Path(data_dir) / 'lobbying'

files_and_headers = {
                        'filings':('lob_lobbying.txt',
                                    [
                                        'filing_id',
                                        'registrant_raw',
                                        'registrant',
                                        'is_firm',
                                        'client_raw',
                                        'client',
                                        'ult_org',
                                        'amount',
                                        'catcode',
                                        'source',
                                        'self',
                                        'include_nsfs',
                                        'use',
                                        'ind','year',
                                        'type',
                                        'type_long',
                                        'affiliate'
                                        ]),
                        'issues':('lob_issue.txt',
                                    [
                                        'si_id',
                                        'filing_id',
                                        'issue_id',
                                        'issue',
                                        'specific_issue',
                                        'year'
                                        ]),
                        'issues_no_specific':('lob_issue_NoSpecficIssue.txt',
                                    [
                                        'si_id',
                                        'filing_id',
                                        'issue_id',
                                        'issue'
                                        ]),
                        'bills':('lob_bills.txt',
                                    [
                                        'bill',
                                        'si_id',
                                        'congress',
                                        'bill_name']),
                        'lobbyists':('lob_lobbyist.txt',
                                    [
                                        'filing_id',
                                        'lobbyist_raw',
                                        'lobbyist',
                                        'lobbyist_id',
                                        'year',
                                        'official_position',
                                        'congress_id',
                                        'former_member'
                                        ]),
                        'agencies':('lob_agency.txt',
                                    [
                                        'filing_id',
                                        'agency_id',
                                        'agency'
                                        ]),
                        'industries':('lob_indus.txt',
                                    [
                                        'client',
                                        'subsidiary',
                                        'total',
                                        'year',
                                        'catcode'
                                        ]),
                        'report_types':('lob_rpt.txt',
                                    [
                                        'type_long',
                                        'type'
                                        ])
                        }


def load_df(table):

    f,headers = files_and_headers[table]

    df = pd.read_csv(path/f,quotechar='|',names=headers,index_col=False,header=None,encoding='ISO-8859-1',low_memory=False)

    if table == 'filings':
        df = format_filings_df(df)

    return df


def format_filings_df(df):

    # Create indicator for whether each filing should be used in when calculating total amounts
    df['include_in_total'] = (df['use'] == 'y') & (df['ind'] == 'y')

    # Add date ranges to filings
    date_ranges_by_type = {'m':('01-01','06-30'),'e':('07-01','12-31'),'q1':('01-01','03-31'),'q2':('04-01','06-30'),'q3':('07-01','09-30'),'q4':('10-01','12-31')}

    for q,dates in date_ranges_by_type.items():
        selectedTypes = [t.lower().startswith(q) for t in df['type']]
        df.loc[selectedTypes,'start_date'] = dates[0]
        df.loc[selectedTypes,'end_date'] = dates[1]

    for c in ['start_date','end_date']:
        df[c] = pd.to_datetime(df['year'].astype(str) + '-' + df[c])

    # Impute minimum recordable amounts
    df.loc[df['year'] < 2008,'min_amount'] = 10000
    df.loc[df['year'] >= 2008,'min_amount'] = 5000

    return df
