# **BloomFilter Class**
BloomFilter takes in the numKeys, numHashes, and the maxFalsePositive rate to create a Bloom Filter

## Definition of Bloom Filter

A Bloom Filter is a probabilistic data structure that can tell you with a specified false postive rate, if a key was inserted into the Bloom Filter or not. 

## This Implementation
This Bloom Filter uses BitVector to create different Hash functions to encode the keys. The Bloom Filter is originally a list of 0s. 

When a key is inserted into the Bloom Filter, it is hashed numHashes number of times, and those indeces in the filter are set to 1. Then, one only has to check those indeces to tell if a key is in the filter. There is a false positive rate since there can be overlap of keys set to 1 and, potentially, there could be a key where all values are 1, but it was never inserted. 

## Supported Methods
- insert(key):         inserts a key into the Bloom Filter
- find(key)  :         returns True if the key is in the Bloom Filter and False otherwise
- falsePositiveRate(): returns the projected current false positive rate of the Bloom Filter
- numBitsSet():        returns the current number of bits set in the Bloom Filter

## Credits
This project was created as a homework project for the Spring 2021 class Data Structures at Yeshiva University.

Yeshiva University © [Juliet Nasar]()
