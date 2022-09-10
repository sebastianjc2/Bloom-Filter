import math
import csv
import sys
import numpy
from bitarray import bitarray
import mmh3


def load_input_file():
    try:
        # reading first file (the one that receives the input emails)
        with open(sys.argv[1], 'r') as file:
            iterator = csv.reader(file)
            next(iterator, None)
            i = [i for i in iterator]
        inputs = numpy.array(i, dtype=str)

        # reading second file (the one that receives the data to test the algorithm)
        with open(sys.argv[2], 'r') as tester_file:
            db_iterator = csv.reader(tester_file)
            next(db_iterator, None)
            j = [j for j in db_iterator]
        data_tests = numpy.array(j, dtype=str)

    except:
        print("invalid path or file")
        exit()
    return (inputs, data_tests)


class BloomFilter(object):
    def __init__(self, items, prob):
        # False positive probability in decimal (it's a specific one called later on)
        self.prob = prob

        # Size of the bit array
        self.size = self.get_size(items, prob)

        # number of hash functions to use
        self.hash_count = self.get_hash_count(self.size, items)

        # Bit array of given size
        self.bit_array = bitarray(self.size)

        # initialize all bits as 0
        self.bit_array.setall(0)

    # using equation in link provided by the professor to find the number of
    # bits in the filter
    def get_size(self, items, prob):
        bit_size = ((items * math.log(prob)) / math.log(1 / (2 ** math.log(2))))
        return int(bit_size)

    # using equation in the link provided by the professor to find the number of
    # hash functions
    def get_hash_count(self, bits, items):
        hash_functions = (bits / items) * math.log(2)
        return int(hash_functions)

    # add an item in the filter
    def add(self, item):
        for i in range(self.hash_count):
            given = mmh3.hash(item, i) % self.size
            self.bit_array[given] = True

    # check if a specific item exists in the filter
    def check(self, item):
        for i in range(self.hash_count):
            given = mmh3.hash(item, i) % self.size
            if not self.bit_array[given]:
                return False
        return True

    # add from the items in the input file
    def add_array(self, array):
        for item in array.tolist():
            self.add(item[0])


# help combine the output data for the writing of the results
def combine_out(arr_1, arr_2):
    stacked_columns = numpy.column_stack((arr_1, arr_2))
    return stacked_columns


def main():
    input_file = load_input_file()

    data_set_length = len(input_file[0])

    # calling the bloom filter and inputting the false positive
    # probability of 0.0000001 given by the professor
    bloomF = BloomFilter(data_set_length, 0.0000001)
    bloomF.add_array(input_file[0])

    # looping and validating if it's found in the data to check
    # and responding 'Not in the DB' if the program ran through and
    # it's 100% certain it's not in the DB, and 'Probably in the DB'
    # otherwise ( it can't be certain it is )
    validate = []
    for row in input_file[1]:
        if bloomF.check(row):
            validate.append('Probably in the DB')
        else:
            validate.append('Not in the DB')

    # writing the results.csv file
    with open('Results.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Email', 'Result'])
        writer.writerows(combine_out(input_file[1], validate))


if __name__ == '__main__':
    main()
