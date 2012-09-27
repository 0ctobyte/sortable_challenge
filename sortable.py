import json, sys
from datetime import datetime
from matchers import *

def add_result(result, listing):
	result['listings'].append(listing)
	return True

print str(datetime.now())

# Input and output file names
products_f, listings_f = 'products.txt', 'listings.txt'
results_f = 'results.txt'

# This script will take products and listings files specified in the command
# line
if len(sys.argv) >= 3:
	products_f, listings_f = sys.argv[1], sys.argv[2]

# Load products into an array of dicts
products = []
with open(products_f, 'r') as file:
	for line in file:
		products.append(json.loads(line))

# Load listings into an array of dicts
listings = []
with open(listings_f, 'r') as file:
	for line in file:
		listings.append(json.loads(line))

print '# of products: ' + str(len(products))
print '# of listings: ' + str(len(listings))

# We're going to sort the listings by manufacturer, this way we don't have to
# loop through every single listing when comparing them to a product when they
# don't even have the same manufacturer
sorted_listings = {}
for product in products:
	manufacturer = product['manufacturer'].lower()
	if manufacturer not in sorted_listings:
		# I love list comprehensions, it's very intuitive
		sorted_listings[manufacturer] = [listing for listing in listings if listing['manufacturer'].lower().find(manufacturer) != -1]
	else:
		continue

results = []

print "# of manufacturers: " + str(len(sorted_listings))
print 'Matching (This may take a while)'

# Now we match products to listings
for product in products:
	results.append({'product_name': product['product_name'], 'listings': []})
	sub_listings = sorted_listings[product['manufacturer'].lower()]

	# Only loop through relevant listings (by manufacturer). I'm going to use
	# short circuit evaluation to my advantage here to keep the code short and
	# clean. add_result is only called if match returns true. The whole condition
	# will return false if the listing matches the product. In that case the
	# matched listing will be effectively removed (or not added, however you
	# want to look at it) from the sub_listings list.
	# This means the list will get smaller and smaller as more listings are 
	# matched thus improving performance over time.
	# What is [:]? It means the list is modified in place and that all
	# references to that list will be modified as well.
	sub_listings[:] = [listing for listing in sub_listings if not (match(product, listing) and add_result(results[len(results)-1:][0], listing))]

	# Some very cool effects so the user knows the program is still alive
	sys.stdout.write('.')
	sys.stdout.flush()

print '\nMatching complete!'
print '# of leftover listings: ' + str(sum([len(sorted_listings[key]) for key in sorted_listings]))

# Write the results to a file, one result per line
# Remove the commas!
with open(results_f, 'w') as file:
	for result in results:
		file.write(json.dumps(result) + ',\n')

# Write the leftover listings to a file
with open('leftovers.txt', 'w') as file:
	for key in sorted_listings:
		for listing in sorted_listings[key]:
			file.write(json.dumps(listing) + ',\n')

print str(datetime.now())
