import jaro_winkler as fuzzy
import jaro

def partial_match(str1, str2):
	# We want to match the smaller string to a part of the larger string
	l1, l2 = len(str1), len(str2)
	if l2 > l1:
		str1, str2, l1, l2 = str2, str1, l2, l1
	
	i, j, ratios = str1.find(str2[0]), 0, []

	while i != -1:
		ratios.append(match(str1[i+j:i+j+l2], str2))
		i, j = str1[i+j+1:].find(str2[0]), i+1
		print i

	return max(ratios)

def match(str1, str2):
	return jaro.distance(str1, str2)
