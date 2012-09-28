def common_chars(str1, str2):
	# Since we need the length of the strings mutliple times in this function
	l1, l2 = len(str1), len(str2)

	# Jaro says two characters are matching if they are the same AND if they
	# are no further than match_limit away from each other
	match_limit = max(l1, l2)/2 - 1

	# The matrix has max(l1, l2) columns and min(l1, l2) rows. It will work the 
	# other way around but we don't want ambiguity. The matrix will store 1's
	# where the characters in i and j (indices to str1 and str2 respectively)
	# match. Most implementations of the jaro distance don't do it this way, but
	# I want a better way to match strings where multiple characters in one string
	# match a single character in the other.
	match_matrix = [0]*l1*l2
	
	# Swap values if str2 is smaller than str1.
	if l2 < l1:
		str1, str2, l1, l2 = str2, str1, l2, l1
	
	# Find matching characters the Jaro way
	for i in range(0, l1):
		for j in range(max(-i, -match_limit), min(l2-i, match_limit+1)):
			if str1[i] == str2[i+j]:
				match_matrix[i*l2+(i+j)] = 1
	
	# create a list of matching chars for each string. The order of common1 and
	# common2 may not be the same even though they contain the same chars.
	# We make sure that we don't include any duplicate matches.
	common1, common2 = ['']*l1, ['']*l2
	for i in range(0, l1):
		for j in range(0, l2):
			if match_matrix[i*l2+j] == 1:
				if common1[i] == '' and common2[j] == '':
					common1[i], common2[j] = str1[i], str2[j]
	
	return ''.join(common1), ''.join(common2)
	
def transpositions(match1, match2):
	transpositions = 0

	# Any matching characters, from each string, that aren't in the same index
	# location as each other, are transpositions.
	for index in range(0, len(match1)):
		if match1[index] != match2[index]:
			transpositions += 1

	return transpositions

def distance(str1, str2):
	l1, l2 = len(str1), len(str2)
	
	# The strings must not be empty!
	if l1 == 0 or l2 == 0: return 0
	
	# Now we get the matching chars. We call this function twice, with the 
	# first call having str1 as the first parameter and the second call having
	# str2 as the first parameter. This is because the order of the matching
	# characters may vary; we use this fact in get_transpositions.
	match1, match2 = common_chars(str1, str2)
	
	# match1 and match2 must be the same size. I'm not sure what supposed to
	# happen if they're not...
	if len(match1) != len(match2): return 0

	# The number of matches is simply the length of the string with all the
	# matching characters according to Jaro's rules
	m = len(match1)
	
	# If m == 0, then the strings can never ever be together, EVER.
	if m == 0: return 0

	# The number of differences in the order of the matching characters is the
	# number of transpositions, according to Jaro. We need half the number
	# of transpositions
	t = transpositions(match1, match2)/2

	# Calculate the jaro distance
	return (1.0/3.0)*(m/float(l1) + m/float(l2) + (m-t)/float(m))
