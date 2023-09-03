# CryptoSearch

Multithreaded program that generates crypto addresses

Files:
config.py - change the parameters here to designate source and output file paths, as well as coin type and hashing algorigthms
main.py - run this file to begin generating addresses and querying the blockchain

addressMultithread.py - program that splits work into multiple threads and writes to a text file
seedHelper.py - helper file that generates keys and addresses individually
gsInterface.py - uploads files to google storage
bigQuery.py - interacts with google BigQuery to sql search and match addresses
