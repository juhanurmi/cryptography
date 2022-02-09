# -*- coding: utf-8 -*-
'''
python3 bloomfilter_test.py
'''
import time
from pybloomfilter import BloomFilter

def test_value(bloomfilterfile, testvaluefile, testcount):
    ''' Test values with the bloom filter '''
    bfilter = BloomFilter.open(bloomfilterfile)
    false_positives = 0
    index = 0
    with open(testvaluefile) as myfile:
        for line in myfile:
            index = index + 1
            # Stop after 1 million tests
            if index == testcount:
                break
            line = line.strip()
            if not line in bfilter: # No false negatives should ever happen
                print('False negative: %s' % line)
            # Replace one char in the line
            if line[10] != '2': # char in index 10 is not 2
                line = line[:10] + '2' + line[11:] # Change it to 2
            else: # It is 2, replace it with r
                line = line[:10] + 'r' + line[11:]
            if line in bfilter:
                false_positives = false_positives + 1
    print('%d false positives, error rate is %.3f' % (false_positives, (false_positives/testcount)))

def main():
    ''' Main function '''
    starttime = time.time() # Start time
    testcount = 500000
    test_value('bloom.filter', 'Bitcoin_addresses_January_01_2022.txt', testcount)
    print('%d tests took %d seconds.' % (testcount*2, (time.time() - starttime)))

if __name__ == '__main__':
    main()
