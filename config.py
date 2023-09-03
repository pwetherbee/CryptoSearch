class Config():
    # path parameters
    SOURCE_PATH = "D:\data/seeds/"
    SOURCE_FILENAME = 'wiki-100k.txt'
    OUTPUT_PATH = "D:\data/"
    # address gen parameters
    COIN = 'eth'
    HASHER = 'sha3_256'  # sha3_256
    ENCODER = 'ISO-8859-1'  # utf-8 #ISO-8859-1 #latin-1
    # P2PKH (1) for legacy, P2SH for new address (3), P2WPKH (bc) for advanced address
    BTC_ADDRESS_TYPE = 'P2PKH'
    # iteration parameters
    start = 1
    num_threads = 12
    num_iterations = 7
    lines_per_file = 0  # set to 0 for whole file
