import os
import pandas as pd
import numpy as np

from openSecrets.dirs import *

filesAndHeaders = {
                'candidates':('cands{}.txt',['cycle','fec_id','candidate_id','first_last_party','party','district_id_run','district_id_current','current_candidate','cycle_candidate','incumbency','recipient_code','no_pacs']),
                'committees':('cmtes{}.txt',['cycle','pac_id','name','affiliate','ult_org','recipient_id','recipient_code','fec_id','party','primary_code','primary_code_source','sensitive','foreign','active']),
                'individual':('indivs{}.txt',['cycle','fec_trans_id','contributer_id','contributer','recipient_id','org_name','ult_org','real_code','date','amount','street','city','state','zip','recipient_code','transaction_type','committee_id','other_id','gender','microfilm','occupation','employer','source']),
                'pac':('pacs{}.txt',['cycle','fec_record_number','pac_id','candidate_id','amount','date','real_code','transaction_type','direct','fec_id']),
                'pac_to_pac':('pac_other{}.txt',['cycle','fec_record_number','filer_id','donor_name','contrib_lend_trans','city','state','zip','fec_occ_empl','primary_code','date','amount','recipient_id','party','other_id','recipient_code','recipient_primary_code','amend','report','primary','microfilm','type','real_code','source'])
        }


def loadDF(table,cycles=range(1990,2018,2)):
    f,headers = filesAndHeaders[table]

    cycleDFs = []
    for cycle in cycles:
        yy = str(cycle)[-2:]
        filename = os.path.join(campaignFinancingDataDir,'CampaignFin{}'.format(yy),f.format(yy))
        df = pd.read_csv(filename,quotechar='|',names=headers,index_col=False,header=None,encoding='mbcs')

        cycleDFs.append(df)

    df = pd.concat(cycleDFs)

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

# df = loadDF('pac_to_pac')
# df.head(1).T
