def distance(str1, str2):
	l1, l2 = len(str1), len(str2)

	# The hamming distance only works with strings of the same length
	if l1 != l2: return -1

	return sum([1 if ch1 != ch2 else 0 for ch1, ch2 in zip(str1, str2)])
