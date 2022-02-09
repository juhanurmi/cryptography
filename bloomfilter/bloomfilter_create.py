# -*- coding: utf-8 -*-
'''
python3 bloomfilter_create.py
'''
from pybloomfilter import BloomFilter

def create_bloom_filter(bloomfilter_file, error_rate, input_data_file):
    ''' Create a bloom filter file '''
    with open(input_data_file) as myfile:
        line_list = myfile.readlines()
        # The number of input elements, then the error rate will be the error_rate
        count = len(line_list)
        # The capacity and error_rate then together serve as a contract:
        # If you add less than capacity items, and the Bloom Filter
        # will have an error rate less than error_rate.
        bfilter = BloomFilter(count, error_rate, bloomfilter_file)
        for line in line_list:
            line = line.strip()
            if len(line) > 5: # Line is not some empty line
                bfilter.add(line) # Append to the filter

def main():
    ''' Main function '''
    create_bloom_filter('bloom.filter', 0.001, 'Bitcoin_addresses_January_01_2022.txt')

if __name__ == '__main__':
    main()
