import hamming

def lower_bound(str1, str2):
	l1, l2 = len(str1), len(str2)

	# The levenshtein distance is always at least the difference of the sizes
	# of the two strings
	return max(l1, l2) - min(l1, l2)

def fast_upper_bound(str1, str2):
	# The levenshtein distance is always at most the length of the longer
	# string
	return max(len(str1), len(str2))

def upper_bound(str1, str2):
	l1, l2 = len(str1), len(str2)

	# According to the wikipedia page, the upper bound can be approximated
	# using the hamming distance algorithm
	if l1 == l2:
		return hamming.distance(str1, str2)
	else:
		return fast_upper_bound(str1, str2)

def levenshtein(str1, str2):
	l1, l2 = len(str1), len(str2)

	# Check initial conditions of strings to make sure they are valid
	# Will return 0 if both l1 and l2 are zero, which is expected.
	if l1 == 0 or l2 == 0: return max(l1, l2)

	# Check if characters match. If not, add 1 to the substitution distance
	mismatch = 0
	if str1[0] != str2[0]: mismatch = 1

	# Levenshtein is a recursive algorithm. We are essentially finding the
	# minimum edit distance between two strings. 'Edits' can be insertions,
	# deletion, and/or substitutions (mismatches)
	return min(levenshtein(str1[1:], str2)+1, levenshtein(str1, str2[1:])+1,
			levenshtein(str1[1:], str2[1:])+mismatch)


def distance(str1, str2):
	# The strings could be identical! Don't waste cpu cycles!
	if str1 == str2: return 0

	return levenshtein(str1, str2)
