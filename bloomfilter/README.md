# Bloom filter

Example case:

You are working in a company that analyses Bitcoin addresses.
Your system is testing 1000 addresses every second against a database.
Database is returning the balance of an address.

Problem:

You are burning 100 USD per month with the database server in cloud.
Could you reduce the resources you need? How to reduce the number of queries you are performing?

Solution:

A Bloom filter is a space-efficient probabilistic data structure that is used to test whether an element is a member of a set. False positive matches are possible, but false negatives are not – in other words, a query returns either "possibly in set" or "definitely not in set".

You decide to build a local bloom filter that knows if an address does not have any balance or not. This filter has 0.1 percent error rate for false positives and 0 percent error rate for false negatives.

Benefits are:

- The filter itself is 68 megabytes and is small compared to the 1.4GB bitcoin address data.
- It is efficient to test addresses against the bloom filter: in fact, in 1 second you can test 1 million addresses.
- There is no need to check the balance of a bitcoin address if the filter returns negative.
- As a result, you reduce significant number of queries away from the database server.

# Basic logic how to create and use bloom filters

It is easy to build a bloom filter, example:

```python
import hashlib
from pybloomfilter import BloomFilter

def sha256_value(text):
    ''' Calculate hexdigest hash value '''
    return hashlib.sha256(str(text).encode('utf-8')).hexdigest()

element_count = 1000 # How many things we are going to add to the filter
error_rate = 0.01 # What is the false positive error rate we want
bloomfilter_file = 'ourbloom.filter' # Filename for the filter we build

bfilter = BloomFilter(element_count, error_rate, bloomfilter_file)
for index in range(0, 1000): # Numbers from 0 to 999
    bfilter.add(sha256_value(index)) # Append to the filter

```

After this it is easy to test it:

```python
import hashlib
from pybloomfilter import BloomFilter

def sha256_value(text):
    ''' Calculate hexdigest hash value '''
    return hashlib.sha256(str(text).encode('utf-8')).hexdigest()

bfilter = BloomFilter.open('ourbloom.filter')

for index in range(0, 999): # Numbers from 0 to 999
    if not sha256_value(index) in bfilter: # No false negatives should ever happen
        print('False negative: %s' % index)

errors = 0
for index in range(1000, 11000): # Numbers from 1000 to 10999
    if sha256_value(index) in bfilter:
      errors = errors + 1

print('%d false positives, error rate is %.3f' % (errors, (errors/10000)))

```

## List of all funded Bitcoin addresses:

Save and decompress this file to the same folder where with bloomfilter_create.py.
There are 39 557 264 Bitcoin addresses (1.4GB) in uncompressed text file.

```sh
wget http://addresses.loyce.club/Bitcoin_addresses_January_01_2022.txt.gz
gunzip Bitcoin_addresses_January_01_2022.txt.gz
```

# Install Python libraries

```sh
python3 -m pip install pybloomfiltermmap3
```

# Create a bloom filter

It takes few minutes to create bloom.filter (68 megabytes).

```sh
python3 bloomfilter_create.py
```

# Test the bloom filter you created

It takes 1 second to test 1 million bitcoin addresses against the filter.

```sh
python3 bloomfilter_test.py
```
