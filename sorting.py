# python $HOME/scripts/ksh/format_file.py ${ant_directory} ${ant_logger_path} ${ant_logger_file} ${ant_row_length} ${ant_filename}

import os
import gzip
import logging
import shutil
import sys

# Usage: python format_file.py ${directory} ${logger_path} ${logger_file} ${row_length} ${file_name}

directory=sys.argv[1]
logger_path=sys.argv[2]
logger_file=sys.argv[3]
row_length=sys.argv[4]
filename=sys.argv[5]

##Set the logger config##
logger = logging.getLogger('format_file')
hdlr = logging.FileHandler(logger_path+logger_file)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.DEBUG)

logger.debug('Directory path: %s, Logger path: %s, Logger file: %s, Row length: %s, File Name: %s',directory,logger_path,logger_file,row_length,filename)

##Program starts##
logger.debug('Starting sorting...')
iFileCount=0
oFileCount=0

for file_name in os.listdir(directory):
    iRows=0
    oRows=0
    if(file_name.find(filename) == 0):
        logger.debug('File to be sorted: %s',file_name)
        iFileCount=iFileCount+1
        with gzip.open(directory+file_name, 'rb') as inf:
            data = []
            for line in inf:
                iRows=iRows+1
                line = line.split('\t')
                logger.debug('length of string: %s for %s',len(line), line)
                if len(line)==int(row_length):
                    data.append(line)

        data.sort(key=lambda s:(s[1],int(s[2])))
        logger.debug(data)

        with gzip.open(directory+'sorted_'+filename, 'wb') as f:
            oFileCount=oFileCount+1
            for t in data:
                oRows=oRows+1
                line = '\t'.join(str(x) for x in t)
                f.write(line)
            logger.debug('Sorted file created: sorted_%s',filename)
    
    if (file_name.find(filename) == 0):
        if iRows==oRows:
            try:
                logger.debug('Deleting %s',directory+filename)
                os.remove(directory+filename)
            except OSError as e:
                e.errno
        else:
            assert iRows==oRows,'Sorted file created with unmatched rows. Retaining the file for analysis'
            #logger.debug('Sorted file created with unmatched rows. Retaining the file for analysis')

assert iFileCount!=0,'No report files present to sort'    
assert iFileCount==oFileCount,'Program finished without sorting all the files'
