def spectral_convolution(a, b):
	return [abs(i-j) for i in a for j in b]

def counts(l):
	d = {}
	for item in l:
		if item in d:
			d[item] += 1
		else:
			d[item] = 1
	return d

def more_than_twice(l):
	d = counts(l)
	res = []
	for key, val in d.iteritems():
		if val > 1:
			res.append(key)
	return sorted(res)

s1 = [760, 115, 645, 262, 498, 377, 383, 496, 264, 627, 133]
s2 = [115, 133, 264,280,383,395,498,514,645,663,778]
s3 = [115,133,280,337,395,456,514,571,718,736,851]

print more_than_twice(spectral_convolution(s2, s1))
print more_than_twice(spectral_convolution(s3, s1))
