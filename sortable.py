import jaro_winkler.jaro_winkler as jw

# After some testing, this seems like a high enough threshold to deter
# almost all false positives
MATCH_THRESHOLD = 0.98

def add_result(results, listing):
	results[len(results)-1:][0]['listings'].append(listing)
	return True

def match_strings(str1, str2):
	words1, words2 = str1.split(), str2.split()
	for word1 in words1:
		for word2 in words2:
			dw = jw.jaro_winklerize_this(word1, word2)
			# We could put all the jaro-winkler values into a list and return
			# the max, but this will save time as we won't have to jaro-winkler
			# every string if there is a positive match.
			if dw >= MATCH_THRESHOLD:
				return dw
	return 0

def match(product, listing):
	# If the manufacturers are not the same, we can be fairly confident
	# that the product and listing are not related
	try:
		if listing['manufacturer'].find(product['manufacturer']) == -1:
			return False
	except KeyError:
		pass

	match_sum = 0.0

	try:
		match_sum += match_strings(product['model'], listing['title'])
	except KeyError:
		pass

	# Sometimes a family attribute may not be specified. In that case if the
	# model completely matches a word in the listing's title, than we can be
	# pretty certain that we got a match.
	try:
		match_sum += match_strings(product['family'], listing['title'])
	except KeyError:
		if listing['title'].find(product['model']) != -1:
			match_sum += 1

	# We just took the average of the jaro-winkler values for the model
	# and family attributes.
	return True if match_sum/2 > MATCH_THRESHOLD else False

import json
from datetime import datetime

print str(datetime.now())

# Load products into an array of dicts
products = []
file = open('products.txt', 'r')

for line in file:
	products.append(json.loads(line))

# Load listings into an array of dicts
file = open('listings.txt', 'r')
listings = []

for line in file:
	listings.append(json.loads(line))


results = []

i = 0

# Now we match products to listings
for product in products:
	results.append({'product_name': product['product_name'], 'listings': []})

	# Here we remove listings that have been matched to a product, thus
	# the listings list becomes smaller as more listings get matched.
	# Why listings[:] instead of just listings? To modify the list in place
	# instead of creating a new reference of course!
	listings[:] = [listing for listing in listings 
			if not (match(product, listing) and add_result(results, listing))]

	i += 1
	print i

# Write the results to a file, one result per line
file = open('results.txt', 'w')
for result in results:
	file.write(json.dumps(result) + ',\n')
file.close()

print str(datetime.now())
