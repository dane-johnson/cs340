#!/usr/bin/env python

import time
import datetime
import threading

from sorts import insertion_sort, merge_sort

mux = threading.Lock()

def time_sort(sort, size, arrangement):
  # Get the data from the input file
  input_file = '%s/%s%dK.txt' % (arrangement, arrangement, size)
  data = None
  with open(input_file, 'r') as f:
    data = f.read().split('\n')
    data.pop() # Drop last element, its an empty string

  # Sort and time the sorting
  t1 = time.time()
  sort(data)
  t2 = time.time()
  delta = t2 - t1

  # Write our data to the csv
  name = '%s%dK.txt - %s' % (arrangement, size, sort.__name__)
  data = '%s,%.8f\n' % (name, delta)
  # Aquire the lock to write to the output file
  mux.acquire()
  # Write the data
  with open('runs.csv', 'a') as f:
    f.write(data)
  # Release the lock
  mux.release()

  # Print that we're done
  print '%s is done.' % name

def main():
  # Create the csv file
  with open('runs.csv', 'w') as f:
    f.write('NAME,TIME\n')

  sorts = [insertion_sort, merge_sort]
  sizes = [30, 60, 90, 120, 150]
  arrangements = ['sorted', 'perm']

  threads = []
  for sort in sorts:
    for size in sizes:
      for arrangement in arrangements:
        t = threading.Thread(target=time_sort, args=(sort, size, arrangement))
        threads.append(t)
        t.start()
  for t in threads:
    t.join()

if __name__ == '__main__':
  main()
