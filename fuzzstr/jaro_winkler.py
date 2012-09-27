import jaro

def get_prefix_match_length(str1, str2):
	l1, l2 = len(str1), len(str2)

	prefix_length = 0

	# We iterate over the indices of the smaller string because
	# we don't want IndexError's
	if l2 < l1:
		str1, str2, l1, l2 = str2, str1, l2, l1

	# This will give us the length of the common prefix, if there is any
	for index in range(0, l1):
		if str1[index] != str2[index]:
			return prefix_length
		prefix_length += 1
	
	return prefix_length

def distance(str1, str2):
	# Get the jaro_distance
	j_distance = jaro.distance(str1, str2)

	# Get the length of the common prefix between the two string 
	# if there is any.
	l = get_prefix_match_length(str1, str2)

	# Mr. Winkler recommends a max of 4 for l (The length of the common prefix)
	# and a standard of 0.1 for p (the constant scaling factor)
	l, p = (l if l <= 4 else 4), 0.1
	
	# Now we calculate the Jaro-Winkler distance!
	return (j_distance + (l*p*(1-j_distance)))
