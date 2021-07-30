from BitHash import BitHash
import BitVector

class BloomFilter(object):
    
    # Return the estimated number of bits needed (N in the slides) in a Bloom 
    # Filter that will store numKeys (n in the slides) keys, using numHashes 
    # (d in the slides) hash functions, and that will have a
    # false positive rate of maxFalsePositive (P in the slides).
    # See the slides for the math needed to do this.  
    # You use Equation B to get the desired phi from P and d
    # You then use Equation D to get the needed N from d, phi, and n
    # N is the value to return from bitsNeeded
    def __bitsNeeded(self, numKeys, numHashes, maxFalsePositive):
        
        n = self.__numKeys
        d = self.__numHashes
        P = self.__maxFalsePositive
        
        # find N based on the variables above
        
        phi = (1-(P**(1/d)))
        N = d/(1-(phi**(1/n)))
        
        # the result will be a float but since we are using N
        # as the length of the array, we are going to round up to a whole num
        return int(N-1)
    
    # Create a Bloom Filter that will store numKeys keys, using 
    # numHashes hash functions, and that will have a false positive 
    # rate of maxFalsePositive.
    # All attributes must be private.
    def __init__(self, numKeys, numHashes, maxFalsePositive):
        # will need to use __bitsNeeded to figure out how big
        # of a BitVector will be needed
        # In addition to the BitVector, might you need any other attributes?
        
        self.__numKeys = numKeys
        self.__numHashes = numHashes
        self.__maxFalsePositive = maxFalsePositive
        
        # using the other values find what len bit array is neccesary
        self.__N = self.__bitsNeeded(numKeys, numHashes, maxFalsePositive)
        
        # create the bloom filter with N indeces
        # initialize all to 0 which reflects that the 
        # list is empty
        self.__bloom = [0]*self.__N
        
        # we will keep track of the number of bits ACTUALLY
        # set
        self.__bitsSet = 0
        
        
    # insert the specified key into the Bloom Filter.
    # Doesn't return anything, since an insert into 
    # a Bloom Filter always succeeds!
    # See the "Bloom Filter details" slide for how insert works.
    def insert(self, key):
        
        # fencepost: 
        # get the first index to insert using BitHash first hash
        # we need hash without % for later when we reinsert it into bithash
        hash = BitHash(key, 0)
        pos = hash%self.__N
        
        # if that index is 0 in the array, set it to 1 and increase
        # the number of bits set by 1 since we just set a bit
        if(self.__bloom[pos] == 0):
            self.__bloom[pos] = 1
            self.__bitsSet+=1
        
        # complete the remaining hashes, we already did 
        # the first one and set the appropriate index in the bloom
        # filter to be 1
        for i in range(1,self.__numHashes):
            
            # get the hash and the position SEPARATELY
            # so we can reinsert hash into BitHash in the next
            # iteration
            hash = BitHash(key,hash)
            pos = hash%self.__N
            
            # if the hashed index is 0, set it to 1 and increase the number
            # of bits set
            if(self.__bloom[pos] == 0):
                self.__bloom[pos] = 1
                self.__bitsSet += 1
            
    
    # Returns True if key MAY have been inserted into the Bloom filter. 
    # Returns False if key definitely hasn't been inserted into the BF.
    # See the "Bloom Filter details" slide for how find works.
    def find(self, key):
        
        # if any of the hashed positions are 0, return False, otherwise return True
        
        # fencepost loop: find first hash pos and check if 0
        # get hash and pos sep so we can use hash later
        hash = BitHash(key, 0)
        pos = hash%self.__N
        
        if(self.__bloom[pos] == 0): return False
        
        
        # go through rest of hashed positions and if any are 0, return false
        for i in range(1, self.__numHashes):
            
            # get hash and pos sep so we can check other hashes
            # in next iterations
            hash = BitHash(key, hash)
            pos = hash%self.__N
            
            if(self.__bloom[pos] == 0): return False
        
        # if we got here, all the hashed positions are 1 so return True,
        # the key is most probably in the bloom filter
        return True
            
       
    # Returns the PROJECTED current false positive rate based on the
    # ACTUAL current number of bits actually set in this Bloom Filter. 
    # This is NOT the same thing as trying to use the Bloom Filter and
    # measuring the proportion of false positives that are actually encountered.
    # In other words, you use equation A to give you P from d and phi. 
    # What is phi in this case? it is the ACTUAL measured current proportion 
    # of bits in the bit vector that are still zero. 
    def falsePositiveRate(self):
        
        d = self.__numHashes
        
        # proportion of bits that are still 0
        phi = (self.__N - self.__bitsSet)/self.__N
        
        # find the projected false pos rate
        P = (1-phi)**d
        
        # return the projected false pos rate
        return P
       
    # Returns the current number of bits ACTUALLY set in this Bloom Filter
    # WHEN TESTING, MAKE SURE THAT YOUR IMPLEMENTATION DOES NOT CAUSE
    # THIS PARTICULAR METHOD TO RUN SLOWLY.
    def numBitsSet(self):
        
        # we have been keeping track of the number of bits
        # actually set when we insert, here we return that number
        return self.__bitsSet


def __main():
    numKeys = 100000
    numHashes = 4
    maxFalse = .05
    
    # create the Bloom Filter
    b = BloomFilter(numKeys, numHashes, maxFalse)
    
    # read the first numKeys words from the file and insert them 
    # into the Bloom Filter. Close the input file.
    f = open("wordlist.txt", "r")
    
    for i in range(numKeys):
        
        b.insert(f.readline())  # read the next word and insert into the bloom filter
    
    f.close()

    # Print out what the PROJECTED false positive rate should 
    # THEORETICALLY be based on the number of bits that ACTUALLY ended up being set
    # in the Bloom Filter. Use the falsePositiveRate method.
    FPR = b.falsePositiveRate()
    print("projected false positive rate: " + str(FPR))

    # Now re-open the file, and re-read the same bunch of the first numKeys 
    # words from the file and count how many are missing from the Bloom Filter, 
    # printing out how many are missing. This should report that 0 words are 
    # missing from the Bloom Filter. Don't close the input file of words since
    # in the next step we want to read the next numKeys words from the file. 
    
    f = open("wordlist.txt", "r")
    
    countMissing = 0
    
    for i in range(numKeys):
        
        found = b.find(f.readline())  # true if word found in bloom, false if not found
        
        if not found: countMissing+=1 # if the word isnt found add to countMissing
    
    print(str(countMissing) + " words are wrongly missing from the bloom filter")
      

    # Now read the next numKeys words from the file, none of which 
    # have been inserted into the Bloom Filter, and count how many of the 
    # words can be (falsely) found in the Bloom Filter.
    
    
    countFalsePos = 0
    
    for i in range(numKeys):
        
        found = b.find(f.readline()) # true if word found in bloom, false if not found
        
        # these words were never inserted so if they are found in the bloom
        # it is a false positive
        if found: countFalsePos+=1   
    
    
    f.close()
    
    print("there are " + str(countFalsePos) + " false positives in the bloom filter")    
    
    
    
    
    # Print out the percentage rate of false positives.
    # THIS NUMBER MUST BE CLOSE TO THE ESTIMATED FALSE POSITIVE RATE ABOVE
    print("true false positive rate: " + str(countFalsePos/numKeys))

    
if __name__ == '__main__':
    __main()       

