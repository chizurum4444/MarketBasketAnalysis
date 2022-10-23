from itertools import combinations
import itertools as it
#import pandas as pd
import argparse
from collections import defaultdict

# Hashing function for the hash table
def hash(num1, num2, pairs):
  return (int(num1) + int(num2)) % (2 * len(pairs))

#Create a dictionary of all candidate item sets from the data set with their corresponding count
def create_candidate_item_set(dataset_file):

  c1 = defaultdict(int)
  baskets = []
  hash_table = {}

  with open(dataset_file) as file:
    for line in file:
      # Create the candidate item set
      num_list = line.strip().split(" ")
      #num_list = map(int, line.split())
      # create a list of all baskets
      baskets.append(num_list)
      # create a dictionary with a count of each individual item
      for item in num_list:
        c1[item] += 1

      # Create pairs of unique items in each bucket
      pairs = list(it.combinations(num_list, 2))
      for pair in pairs:
        index = hash(pair[0], pair[1], pairs) 
        hash_table[index] = 1 if index not in hash_table else hash_table[index]+1

  return c1, baskets, hash_table

# Function for converting hash table to bit map
def create_bitmap(hash_table, threshold):
  bit_map = []
  for key, value in hash_table.items():
    if value < threshold:
      bit_map.insert(key, 0)
    else:
      bit_map.insert(key, 1)

  return bit_map


# Return the frequent items from the candidate_item_list that meet the min_support
def create_frequent_item_set(item_list, min_threshold):

  # delete items that dont meet min threshold
  for key, value in item_list.copy().items():
    if value < min_threshold:
      del item_list[key]

  return item_list.keys()

# Generate pairs from the candidate sets of size k
def join(freq_item_sets, k):
  # k is the size of each item set
  if k <= 2: 
    return list(it.combinations(freq_item_sets, k))
  else:
    return list(it.combinations(set(a for b in freq_item_sets for a in b),k))


# Count the number of frequent item sets in the baskets
def count(item_list, baskets):
  count = dict(zip(item_list, [1]*len(item_list)))

  for basket in baskets:
    for key in count:
      if set(list(key)) < set(basket):
        count[key] += 1 
  return count

def pcy(filelocation, threshold, basket_size):
  minimum_support_count = basket_size * threshold  # Our support threshold
  c1, baskets, hash_table = create_candidate_item_set('retail.txt')
  print("Done with pass one")
  bitmap = create_bitmap(hash_table , minimum_support_count)
  print("Done with bitmap")
  frequent_items = create_frequent_item_set(c1, minimum_support_count)
  print("Done with frequent items")

  # hash each frequent item into the bitmap and remove non frequent pairs
  frequent_pairs = join(frequent_items, 2)

  #Second Pass
  for pair in frequent_pairs:
    hash_value = hash(pair[0], pair[1], frequent_pairs)
    if bitmap[hash_value] != 1:
      frequent_pairs.remove(pair)
      
    L = [frequent_pairs]
    items = count(L[0], baskets)

    return (L)

baskets = []
file_location = 'retail.txt'
print(pcy(file_location, 0.05, 17632))