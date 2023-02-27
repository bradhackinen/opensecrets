# OpenSecrets Loader

### A little tool for loading bulk data from OpenSecrets


## Setup

1. Clone the `opensecrets` repository and make sure it is located on the system `PYTHONPATH`
2. Add a file named `config.py` to the `opensecrets` project directory. The file should define a variable called `data_dir` that points to the the location where you will put the bulk data files
3. Download bulk data files from https://www.opensecrets.org/bulk-data

    - Lobbying bulk files should unzipped be placed in `data_dir/lobbying`
    - Campaign finance bulk files for each cycle should unzipped be placed in `data_dir/campaign_finance/CampaignFin{cycle}`
    - 527 files should be placed in `data_dir/527`
4. Run `opensecrets._loader_test.py` to verify that the files can be found


## Usage

The main function is `opensecrets.load_df`, which loads a single table as a Pandas dataframe (concatenating all years or cycles by default). The first argument to `load_df` is a two-part string describing the table (see table list below). For example, `load_df('lobbying.filings')` loads the lobbying filings table, and `load_df('lobbying.lobbyists')` loads the lobbyists table.


**Special options**

Because the campaign finance data is so large, the loader for this data allows two additional arguments:

- `cycles` which takes a list of cycles you would like to load
- `fields` which takes a list of field names to load, in case you don't need all the variables


**Naming**

For better or worse, I have renamed some tables and columns in ways that made more sense to me. The full list of column names can be seen in the `files_and_headers` dictionary in each loader file (`lobbying.py`,`campaign_finance.py`, and `pac.py` for the 527 tables)

**Example usage**

```{python}
import opensecrets

# Load lobbying filings
lobbing_df = opensecrets.load_df('lobbying.filings')

# Load PAC-to-PAC donations for the 2016 and 2018 cycles
pac_donations_df = opensecrets.load_df('campaign_finance.pac_to_pac',cycles=[2016,2018])

```



### Tables

**Lobbying**
| `load_df()` argument | OpenSecrets file |
|-------|-------|
| `'lobbying.filings'`            | lob_lobbying.txt |
| `'lobbying.issues'`             | lob_issue.txt |
| `'lobbying.issues_no_specific'` | lob_issue_NoSpecficIssue.txt |
| `'lobbying.lobbyists'`          | lob_lobbyist.txt |
| `'lobbying.agencies'`           | lob_agency.txt |
| `'lobbying.industries'`         | lob_indus.txt |
| `'lobbying.report_types'`       | lob_rpt.txt |

**Campaign Finance**
| `load_df()` argument | OpenSecrets file |
|-------|-------|
| `'campaign_finance.candidates'` | CampaignFin*/cands*.txt |
| `'campaign_finance.committees'` | CampaignFin*/cmtes*.txt.txt |
| `'campaign_finance.individual'` | CampaignFin*/indivs*.txt |
| `'campaign_finance.pac'`        | CampaignFin*/pacs*.txt |
| `'campaign_finance.pac_to_pac'` | CampaignFin*/pac_other*.txt |

**527**
| `load_df()` argument | OpenSecrets file |
|-------|-------|
| `'527.committees'`      | cmtes527.txt |
| `'527.expenditures'`    | expends527.txt |
| `'527.receipts'`        | rcpts527.txt |

**Reference**
| `load_df()` argument | OpenSecrets file |
|-------|-------|
| `'reference.categories'`      | CRP_Categories.txt |
