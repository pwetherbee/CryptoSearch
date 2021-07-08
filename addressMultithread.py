from logging import getLogger
import multiprocess as mp
from config import Config as cf
from time import sleep
from tqdm import tqdm, trange
from seedHelper import coinHelper

ch = coinHelper()

tqdm.pandas()


# load data sequentially


class CoinDataLoader:
    def __init__(self, start=1, total=100000, coin='eth', threads=1, chunksize=10, encoder="utf-8", hasher='sha_256'):
        print('initializing CoinDataLoader')
        self.setTotal(total)
        self.setStart(start)
        self.inPaths = []
        self.outPaths = []
        self.coin = coin
        self.encoder = encoder
        self._size = 0
        self.map = mp.Pool(threads).map
        self.chunksize = chunksize
        self.hasher = hasher

    def setStart(self, start):
        self.start = (start-1) * self.total

    def setTotal(self, total):
        self.total = total
        self.div = 1
        self.prefix = ''
        if total >= 10 ** 3:
            self.div = 10 ** 3
            self.prefix = 'K'
        if total >= 10 ** 6:
            self.div = 10 ** 6
            self.prefix = 'M'

    def setCoin(self, coin):
        ch.setCoin(coin)

    def setInPath(self, fpath, filename):
        self.inPath = fpath + filename

    def setOutPath(self, fpath, filename):
        name = f'{self.coin}-{filename[:-4]}-{self.hasher}-{self.start // self.div}-{(self.start + self.total) // self.div}{self.prefix}.txt'
        full = f'{fpath}{self.coin}Addresses/{name}'
        reduced = f'{fpath}{self.coin}Addresses/reduced/r-{name}'
        self.name = name
        self.outPaths.append(full)
        self.outPaths.append(reduced)

    def getFilename(self):
        return self.name

    def getOutPaths(self):
        return self.outPaths

    @staticmethod
    def poolFunction(seed):
        ch.setCoin(cf.COIN)
        ch.setEncoder(cf.ENCODER)
        ch.setHasher(cf.HASHER)
        pkey = ch.getHash(seed)
        addy = ch.getAddress(pkey, address_type=cf.BTC_ADDRESS_TYPE)
        seed = seed.replace(',', 'CMA')
        return f'{seed}\t,{pkey},{addy}\n'

    def generateAddressText(self, seeds):
        # stop here
        addressList = [line for line in self.map(
            self.poolFunction, seeds, chunksize=self.chunksize)]
        addressString = ''.join(addressList)
        return addressString

    def createAddressFileMP(self, blockSize=5000):  # "ISO-8859-1"
        # init chunk
        chunk = []
        # if given 0, run through entire file
        if self.total == 0:
            self.total = sum(1 for line in open(
                self.inPath, 'r', encoding=self.encoder)) - 1
        with open(self.inPath, 'r', encoding=self.encoder) as infile, open(self.outPaths[0], 'w', encoding=self.encoder)\
                as outfile:
            outfile.write('raw,private_key,address\n')
            # iterate up to start index
            print('Seeking start index', self.start)
            for _ in range(self.start):
                next(infile)
            print('Reading file and generating private keys and addresses')
            # tqdm.reset()
            for i, line in enumerate(tqdm(infile, total=self.total)):
                # ignore lines until start index
                if i < self.start:
                    continue
                # end condition
                if i - self.start >= self.total:
                    if len(chunk) > 0:  # finish up current chunk
                        outfile.write(self.generateAddressText(chunk))
                    break
                # remove newline characters
                raw = line.rstrip()
                # breakup data into chunks of a specific size
                # if raw.isascii():  # ignore not ascii strings TEST ONLY HASHES NOT ASCII WORDS
                #     continue
                self._size += 1
                chunk.append(raw)
                if len(chunk) >= blockSize:
                    # send the chunk to a funtion that operates on all of the data and returns a string
                    # write that block to the text file
                    outfile.write(self.generateAddressText(chunk))
                    chunk = []  # clear chunk
            print(
                f'Finished writing {self._size} lines to file {self.outPaths[0]}\n')

    def createCleanCsv(self):
        with open(self.outPaths[0], 'r', encoding=self.encoder) as infile, open(self.outPaths[1], 'w') as outfile:
            outfile.write('index,address\n')
            for i, line in enumerate(tqdm(infile, total=self._size + 1)):
                if i is 0:
                    continue
                line = line.rstrip()
                address = line.split(',')[2]
                outfile.write(f'{i + 1},{address}\n')
        sleep(1)
        print(f'Finished writing to file {self.outPaths[1]}\n')
