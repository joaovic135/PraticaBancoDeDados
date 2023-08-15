#!/usr/bin/env python

import sys

class Reducer:
  def reduce(self , term,counts):
    total_sum = sum(int(count) for count in counts)
    print(f"{term}\t{total_sum}")

if __name__ == "__main__":
  reducer = Reducer()
  current_term = None
  current_counts = []

  for line in sys.stdin:
    term,count = line.strip().split('\t')

    if current_term is None:
      current_term = term

    if term == current_term:
      current_counts.append(count)
    else:
      reducer.reduce(current_term, current_counts)
      current_term = term
      current_counts = [count]

  if current_term is not None:
        reducer.reduce(current_term, current_counts)
