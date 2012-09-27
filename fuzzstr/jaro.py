def get_common_chars(str1, str2):
	# Since we need the length of the strings mutliple times in this function
	l1, l2 = len(str1), len(str2)

	# Jaro says two characters are matching if they are the same AND if they
	# are no further than match_limit away from each other
	match_limit = max(l1, l2)/2 - 1

	common_chars = ''
	
	# Let's find those matching characters the Jaro way!
	for i in range(0, l1):
		for j in range(-match_limit, match_limit+1):
			if i+j < 0: continue
			try:
				if str1[i] == str2[i+j]:
					common_chars += str1[i]
			except IndexError:
				pass
	
	return common_chars

def get_transpositions(match1, match2):
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
	match1, match2 = get_common_chars(str1, str2), get_common_chars(str2, str1)
	
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
	t = get_transpositions(match1, match2)/2

	# Calculate the jaro distance
	return (1.0/3.0)*(float(m)/l1 + float(m)/l2 + (m-t)/float(m))
