def get_match_matrix(str1, str2):
	# Since we need the length of the strings mutliple times in this function
	s1, s2, l1, l2 = str1.lower(), str2.lower(), len(str1), len(str2)

	# Jaro says two characters are matching if they are the same AND if they
	# are no further than match_limit away from each other
	match_limit = max(l1, l2)/2 - 1

	# We require a matrix with min(l1, l2) rows and max(l1, l2)
	# columns (swapping the lengths of the rows and columns would work as well,
	# but this way there's no ambiguity). 1's in the matrix represent matching
	# characters. The row and column indices will give the location of the
	# matching character in each string.
	match_matrix = [0] * (l1*l2)

	# Less comparisons if the outer for statement uses a range with the length 
	# of the smaller string. The result will not differ either way.
	if l2 < l1:
		s1, s2, l1, l2 = s2, s1, l2, l1

	# Let's find those matching characters the Jaro way!
	for i in range(0, l1):
		for j in range(-match_limit, match_limit+1):
			if i+j < 0:
				continue

			try:
				if s1[i] == s2[i+j]:
					match_matrix[l2*i+(i+j)] = 1
			except IndexError:
				pass
	
	return match_matrix

def get_matching_chars(str1, str2, match_matrix):
	s1, s2, l1, l2 = str1.lower(), str2.lower(), len(str1), len(str2)

	if l2 < l1:
		s1, s2, l1, l2 = s2, s1, l2, l1

	match1_list, match2_list = ['']*l1, ['']*l2

	# Here we just put all the matching characters of each string into
	# each list. The list of course will preserve the order of the matching
	# characters of each string.
	for i in range(0, l1):
		for j in range(0, l2):
			if match_matrix[l2*i+j] == 1:
				# The Jaro wikipedia article didn't specify what happens when
				# two characters from one string are matched to the same
				# character in the other string. For example: 'Samsung' and 
				# 'Canada', 'Canada'[1] and 'Canada'[3] will both be matched to
				# 'Samsung'[1].
				# We are not going to consider subsequent matches to the same 
				# character as a match.
				if match1_list[i] == '' and match2_list[j] == '':
					match1_list[i],	match2_list[j] = s1[i], s2[j]

	return ''.join(match1_list), ''.join(match2_list)

def get_transpositions(match1, match2):
	transpositions = 0

	# Any matching characters, from each string, that aren't in the same index
	# location as each other, are transpositions.
	for index in range(0, len(match1)):
		if match1[index] != match2[index]:
			transpositions += 1

	return transpositions

def get_prefix_match_length(str1, str2):
	s1, s2, l1, l2 = str1.lower(), str2.lower(), len(str1), len(str2)

	prefix_length = 0

	# We iterate over the indices of the smaller string because
	# we don't want IndexError's
	if l2 < l1:
		s1, s2, l1, l2 = s2, s1, l2, l1

	# This will give us the length of the common prefix, if there is any
	for index in range(0, l1):
		if s1[index] != s2[index]:
			return prefix_length
		prefix_length += 1
	
	return prefix_length

def jaro_distance(str1, str2):
	l1, l2 = len(str1), len(str2)
	
	# Gets a matrix where a 1 indicates the characters at the specified
	# indices are equal.
	match_matrix = get_match_matrix(str1, str2)

	# The matrix is useful here to construct two strings with the matching 
	# characters, however, the strings may differ in the order of characters
	match1, match2 = get_matching_chars(str1, str2, match_matrix)

	# The number of matches is simply the length of the string with all the
	# matching characters according to Jaro's rules
	m = len(match1) # match1 and match2 should be the same size

	# The number of differences in the order of the matching characters is the
	# number of transpositions, according to Jaro. We need the half the number
	# of transpositions
	t = get_transpositions(match1, match2)/2

	# Calculate the jaro distance
	return (0 if m == 0 else ((1.0/3.0)*(float(m)/l1 + float(m)/l2 + 
			(m-t)/float(m))))

def jaro_winklerize_this(str1, str2):
	# Get the jaro_distance
	j_distance = jaro_distance(str1, str2)

	# Get the length of the common prefix between the two string 
	# if there is any.
	l = get_prefix_match_length(str1, str2)

	# Mr. Winkler recommends a max of 4 for l (The length of the common prefix)
	# and a standard of 0.1 for p (the constant scaling factor)
	l, p = (l if l <= 4 else 4), 0.1
	
	# Now we calculate the Jaro-Winkler distance!
	return (j_distance + (l*p*(1-j_distance)))

import sys

if __name__ == "__main__":
	match_matrix = get_match_matrix(sys.argv[1], sys.argv[2])
	match1, match2 = get_matching_chars(sys.argv[1], sys.argv[2], match_matrix)
	print len(match1)
	print match1, match2
	transpositions = get_transpositions(match1, match2)
	print transpositions/2
	l = get_prefix_match_length(sys.argv[1], sys.argv[2])
	print l
	dw = jaro_winklerize_this(sys.argv[1], sys.argv[2])
	print dw

