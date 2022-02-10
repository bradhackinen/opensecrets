from pathlib import Path
import pandas as pd

from openSecrets.config import data_dir

path = Path(data_dir) / '527'

files_and_headers = {
                        'committees':('cmtes527.txt',
                                        [
                                            'cycle',
                                            'reporting_period',
                                            'ein',
                                            'name',
                                            'affiliate',
                                            'ult_org',
                                            'recipient_code',
                                            'pac_id',
                                            'candidate_id',
                                            'ecc_committee_id',
                                            'party',
                                            'primary_code',
                                            'primary_code_source',
                                            'filing_freq',
                                            'type',
                                            'type_source',
                                            'ideology',
                                            'comments',
                                            'state'
                                            ]),
                        'expenditures':('expends527.txt',
                                        [
                                            'report',
                                            'form_id',
                                            'schB_id',
                                            'orgname',
                                            'ein',
                                            'recipient',
                                            'recipient_crp',
                                            'amount',
                                            'date',
                                            'expenditure_code',
                                            'expenditure_code_source',
                                            'purpose',
                                            'address_1',
                                            'address_2',
                                            'city',
                                            'state',
                                            'zip',
                                            'employer',
                                            'occupation'
                                            ]),
                        'receipts':('rcpts527.txt',
                                        [
                                            'id',
                                            'report',
                                            'form_id',
                                            'schA_id',
                                            'contributer_id',
                                            'contributer',
                                            'amount',
                                            'date',
                                            'ult_org',
                                            'real_code',
                                            'recipient_id',
                                            'recipent_code',
                                            'party',
                                            'recipient',
                                            'city',
                                            'state',
                                            'zip',
                                            'zip4',
                                            'pmsa',
                                            'employer',
                                            'occupation',
                                            'ytd',
                                            'gender',
                                            'source'
                                            ]),
                        }


def load_df(table):
    f,headers = files_and_headers[table]

    df = pd.read_csv(path/f,quotechar='|',names=headers,index_col=False,header=None,encoding='ISO-8859-1',low_memory=False)

    return df
