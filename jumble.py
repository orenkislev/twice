import sys
import getopt

# File containing a list of valid words
# Configured with the flag --dict
DICTIONARY_FILE = '/usr/share/dict/words'


def usage():
  """Prints out the help string and quits."""
  print 'Usage:'
  print 'jumble [--dict dictionary_file] <jumbled_word>'
  sys.exit(1)


def parse_args():
  """Parses command-line arguments."""
  try:
    opts, args = getopt.getopt(sys.argv[1:], '', ['dict='])
  except getopt.GetoptError as err:
    usage()
  
  # Expect exactly one argument (the word)
  if len(args) != 1:
    usage()

  for o, a in opts:
    if o == '--dict':
      DICTIONARY_FILE = a

  return args[0]


def read_dictionary():
  """Returns a set of words read from the configured dictionary file."""
  dict = set()
  for line in open(DICTIONARY_FILE):
    word = line.strip()

    # Ignore one-letter words.
    if len(word) > 1:
      dict.add(word)
  return dict


def non_ascending_prefix(seq):
  """Returns the last index after which all numbers are in ascending order."""
  i = len(seq) - 1
  while (i > 1) and (seq[i - 1] < seq[i]): i -= 1
  return i


def unjumble(jumbled, dict):
  """Returns a set of words from dict that can be composed from letters in jumbled."""
  words = set()
  if jumbled in dict:
    words.add(jumbled)

  if len(jumbled) < 2:
    return words

  # Permute the letters using Boothroyd's algo. The method is efficient but
  # not trivial to read, since it was derived from a recursive version. A simpler
  # version of the function is available here:
  # http://rosettacode.org/wiki/Permutations#C
  #
  # We also run the same permutation on an ascending sequence of numbers 'ref' so 
  # that we can identify unique sub-permutations on the prefices (see below).

  s = list(jumbled)
  c = [0] * len(s)
  ref = range(len(s))
  d = 1

  while True:
    while (d > 1):
      d -= 1
      c[d] = 0
    while (c[d] >= d):
      d += 1
      if d >= len(s): return words

    i = c[d] if (d & 1) else 0
    s[d], s[i] = s[i], s[d]
    ref[d], ref[i] = ref[i], ref[d]
    c[d] += 1

    w = ''.join(s)
    if w in dict:
      words.add(w)

    # Go over sub-words but make sure they are only checked once, by taking
    # parts where our 'ref' sequence is in ascending after the given prefix.
    # Example:
    # the permutations '12345' and '12354' both have the same 3-letter prefix
    # but we only process the one that has an ascending tail '45'.

    prefix_len = non_ascending_prefix(ref)
    for x in range(prefix_len, len(s)):
      if w[:x] in dict:
        words.add(w[:x])


if __name__ == '__main__':
  jumbled_word = parse_args()
  dict = read_dictionary()
  words = unjumble(jumbled_word, dict)
  print len(words), 'Words found:\n', words
