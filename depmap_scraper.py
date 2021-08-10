import requests
import pandas as pd
import json



def download_latest_sample_info():
    url = 'https://ndownloader.figshare.com/files/27902376'
    response = requests.get(url, allow_redirects=True)
    open('sample_info.csv', 'wb').write(response.content)

class DepmapScraper():

    def __init__(self, query):
        self.query = query
        self.depmap_url = 'https://depmap.org/portal/partials/data_table/context_dependency_enrichment?context='+query

    def get_data_table(self):
        response = requests.get(self.depmap_url).text
        js = json.loads(response)

        if len(js['data']) > 0:
            df = pd.DataFrame.from_dict({ i : d for i, d in enumerate(js['data'])}, orient='index')
            df.columns = js['cols']
            df['type'] = self.query
            return df

        return None


def download_dependency_enrichement_data(by_type='lineage_subtype'):

    # dwonload sample info file
    #download_latest_sample_info()
    data = []

    samples = pd.read_csv('sample_info.csv')

    for typeX in samples[by_type].dropna().unique():
        print(typeX)
        df = DepmapScraper(typeX).get_data_table()

        if df is not None:
            data.append(df)

    data = pd.concat(data)

    out = by_type+'_dependency_enrichment.csv'

    data.to_csv(out, index=False)

download_dependency_enrichement_data(by_type='lineage')


