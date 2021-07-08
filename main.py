import os
from config import Config as cf
from gsInterface import GoogleStorage
import bigQuery as bq
from addressMultithread import CoinDataLoader


def clear(): return os.system('cls')


if __name__ == '__main__':
    for n in range(cf.start, cf.num_iterations + 1):
        # count = 10 * (10**6) * 0  # set to 0 for all
        cdl = CoinDataLoader(start=1, total=cf.lines_per_file, coin=cf.COIN,
                             threads=cf.num_threads, encoder=cf.ENCODER, hasher=cf.HASHER)
        # cdl.setInPath("D:\cracks/", filename)
        cdl.setInPath(cf.SOURCE_PATH, cf.SOURCE_FILENAME)
        cdl.setOutPath(cf.OUTPUT_PATH, cf.SOURCE_FILENAME)
        cdl.setStart(n)
        clear()
        print('Beginning address generation\n..................................')
        cdl.createAddressFileMP()
        cdl.createCleanCsv()
        csv_path = cdl.getOutPaths()[1]

        # upload to google cloud storage
        name = cdl.getFilename()

        # raise ValueError

        print('Uploading file...')
        gs = GoogleStorage()
        gs.uploadFile('address-files', csv_path, name)
        print('Upload success!')

        uri = f'gs://address-files/{name}'
        match_table = bq.getMatchTable(cf.COIN)
        table_id = name[:-4]
        query = f'SELECT * FROM `{match_table}` INNER JOIN `{table_id}` ON `{table_id}`.address = `{match_table}`.address'

        print(f'Querying table {match_table}...')
        res = bq.queryTable(uri, query, table_id)
        print(f'Query completed successfully!')

        bq.parseResults(res, f'D:\cracks/results/{name[:-4]}-RESULTS.txt')
