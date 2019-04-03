from openSecrets import lobbying, pacCommittees, campaignFinance, reference

def loadDF(category,table,**args):
    df = None
    if category.lower().startswith('lobby'):
        df = lobbying.loadDF(table,**args)

    elif category.lower() in ['pac','527',527]:
        df = pacCommittees.loadDF(table,**args)

    elif category.lower().startswith('campaign fin'):
        df = campaignFinance.loadDF(table,**args)

    elif category.lower().startswith('ref'):
        df = reference.loadDF(table,**args)

    if df is None:
        print('Could not find {}/{}. No dataframe loaded.'.format(category,table))
    return df
