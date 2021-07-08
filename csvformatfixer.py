from tqdm import tqdm
infiledir = outfiledir = 'D:\cracks/ethAddresses/'
infilename = 'ethaddresses-realuniq-200-300M.txt'
outfilepath = 'ethaddresses-reducedrealuniq-200-300M-FIXED.txt'


count = 0
total = 100 * 1000 * 1000

with open(infiledir + infilename, 'r',encoding='ascii') as infile, open(outfiledir + outfilepath, 'w', encoding='utf-8') as outfile:
    outfile.write('index,"private_key","address"\n')
    for i,line in enumerate(tqdm(infile, total = total)):
        line = line.rstrip()
        if line.startswith('raw,private_key'):
            continue
        [key, address] = line.split(',')
        # raw = raw.replace('"', 'QQ')
        # raw = raw.replace('\n', 'NL')
        outfile.write(f'{i},{key},{address}\n')
        # outfile.write(f'{i},{key},{address}\n')
        count += 1
        if count > total - 10:
            break
        if line.strip() == '':
            break
        