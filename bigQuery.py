# import os
# from dotenv import load_dotenv
# from google.cloud import bigquery
# load_dotenv()
# path = os.getenv("KEY_PATH")

# projectID = "geobot-312818"
# datasetID = "btcAddresses"

# bq_client = bigquery.Client(project="geobot-312818")
# bq_client.from_service_account_json(path)


# default_schema = [
#     bigquery.SchemaField('index', 'INTEGER', mode='REQUIRED'),
#     bigquery.SchemaField('address', 'STRING', mode='REQUIRED')
# ]


# matchTables = {'eth': 'bigquery-public-data.crypto_ethereum.balances',
#                'btc': os.getenv("BTC_TABLE_PATH")}


# def getMatchTable(coin):
#     return matchTables.get(coin)


# def queryTable(uri, sql, table_id, schema=default_schema):
#     # create external config
#     external_config = bigquery.ExternalConfig('CSV')
#     external_config.source_uris = [uri]
#     external_config.schema = schema
#     external_config.options.skip_leading_rows = 1
#     # table_id = 'test-table'
#     job_config = bigquery.QueryJobConfig(
#         table_definitions={table_id: external_config})
#     query_job = bq_client.query(
#         sql, job_config=job_config)  # make the API request
#     results = list(query_job)
#     return results


# def parseResults(results, destination):
#     print(len(results), ' hits found')
#     with open(destination, 'w') as dest:
#         dest.write('index,address,balance\n')
#         for row in results:
#             dest.write(f'{row.index},{row.address},{row.eth_balance}\n')
