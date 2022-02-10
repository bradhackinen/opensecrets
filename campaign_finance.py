from pathlib import Path
import glob
import pandas as pd

from openSecrets.config import data_dir

path = Path(data_dir) / 'campaignFinance'

files_and_headers = {
                    'candidates':('CampaignFin*/cands*.txt',
                                    [
                                        'cycle',
                                        'fec_id',
                                        'candidate_id',
                                        'first_last_party',
                                        'party',
                                        'district_id_run',
                                        'district_id_current','current_candidate',
                                        'cycle_candidate',
                                        'incumbency',
                                        'recipient_code',
                                        'no_pacs'
                                        ]),
                    'committees':('CampaignFin*/cmtes*.txt',
                                    [
                                        'cycle',
                                        'pac_id',
                                        'name',
                                        'affiliate',
                                        'ult_org',
                                        'recipient_id',
                                        'recipient_code',
                                        'fec_id',
                                        'party',
                                        'primary_code',
                                        'primary_code_source',
                                        'sensitive',
                                        'foreign',
                                        'active'
                                        ]),
                    'individual':('CampaignFin*/indivs*.txt',
                                    [
                                        'cycle',
                                        'fec_trans_id',
                                        'contributer_id',
                                        'contributer',
                                        'recipient_id',
                                        'org_name',
                                        'ult_org',
                                        'real_code',
                                        'date',
                                        'amount',
                                        'street',
                                        'city',
                                        'state',
                                        'zip',
                                        'recipient_code',
                                        'transaction_type',
                                        'committee_id',
                                        'other_id',
                                        'gender',
                                        'microfilm',
                                        'occupation',
                                        'employer',
                                        'source'
                                        ]),
                    'pac':('CampaignFin*/pacs*.txt',
                                    [
                                        'cycle',
                                        'fec_record_number',
                                        'pac_id',
                                        'candidate_id',
                                        'amount',
                                        'date',
                                        'real_code',
                                        'transaction_type',
                                        'direct',
                                        'fec_id'
                                        ]),
                    'pac_to_pac':('CampaignFin*/pac_other*.txt',
                                    [
                                        'cycle',
                                        'fec_record_number',
                                        'filer_id',
                                        'donor_name',
                                        'contrib_lend_trans',
                                        'city',
                                        'state',
                                        'zip',
                                        'fec_occ_empl',
                                        'primary_code',
                                        'date',
                                        'amount',
                                        'recipient_id',
                                        'party',
                                        'other_id',
                                        'recipient_code',
                                        'recipient_primary_code',
                                        'amend',
                                        'report',
                                        'primary',
                                        'microfilm',
                                        'type',
                                        'real_code',
                                        'source'
                                        ])
                    }


def load_df(table,cycles=None):
    filename,headers = files_and_headers[table]
    filepath = str(path/filename)

    cycle_dfs = []
    if cycles:
        for cycle in cycles:
            yy = str(cycle)[:-2]
            df = pd.read_csv(filepath.replace('*',yy),quotechar='|',names=headers,index_col=False,header=None,encoding='ISO-8859-1',low_memory=False)
            cycle_dfs.append(df)
    else:
        for f in glob.glob(filepath):
            df = pd.read_csv(f,quotechar='|',names=headers,index_col=False,header=None,encoding='ISO-8859-1',low_memory=False)
            cycle_dfs.append(df)

    df = pd.concat(cycle_dfs)

    if table == 'candidates':
        for c in ['current_candidate','cycle_candidate','no_pacs']:
            df[c] = df[c] == 'Y'

        df['incumbency'] = df['incumbency'].replace({'I':'incumbent','C':'challenger','O':'open'})

    elif table == 'committees':
        df['sensitive'] = df['sensitive'] == 'Y'
        df['foreign'] = df['foreign'].notnull()
        df['active'] = df['active'] == 1

    elif table == 'pac':
        df['direct'] = df['direct'].replace({'D':True,'I':False})

    elif table == 'pac_to_pac':
        df['amend'] = df['amend'] == 'Y'
        df['primary'] = df['primary'].replace({'P':True,'G':False})

    return df
