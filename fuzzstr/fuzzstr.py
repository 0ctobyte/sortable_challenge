import jaro_winkler
import jaro

# Match a a string to a part of another longer string
def partial_match(str1, str2):
	# We want to match the smaller string to a part of the larger string
	l1, l2 = len(str1), len(str2)
	if l2 > l1:
		str1, str2, l1, l2 = str2, str1, l2, l1
	
	i, j, ratios = str1.find(str2[0], 0), 0, [0]

	while i != -1:
		ratios.append(match(str1[i:i+l2], str2))
		i = str1.find(str2[0], i+1)

	return max(ratios)

# Match two strings after the words in each have been sorted alphabetically
def sort_match(str1, str2):
	s1, s2 = ' '.join(sorted(str1.split())), ' '.join(sorted(str2.split()))
	
	return match(s1, s2)
	
# Sort each string then extract from both, and sort, all the common words.
# Compare the common words string to [common_words] + [str1] and 
# [common_words] + [str2]
def intersect_match(str1, str2):
	set1, set2 = set(str1.split()), set(str2.split())

	common = sorted(list(set1.intersection(set2)))
	s1 = common + sorted(list(set1.difference(set(common))))
	s2 = common + sorted(list(set2.difference(set(common))))
	
	common, s1, s2 = ' '.join(common), ' '.join(s1), ' '.join(s2)
	
	return max(match(common, s1), match(common, s2), match(s1, s2))

# Use the jaro_winkler distance to match two strings
def match(str1, str2):
	return jaro_winkler.distance(str1, str2)
