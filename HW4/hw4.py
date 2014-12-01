import math, random

def distance(a, b):
	deltas = [a[i] - b[i] for i in range(len(a))]
	pows = [delta * delta for delta in deltas]
	return math.sqrt(sum(pows))

def get_closest(val, centers):
	distances = [(i, distance(val, center)) for i, center in enumerate(centers)]
	closest = min(distances, key=lambda t: t[1])
	return centers[closest[0]]

def converged(a, b):
    return set(a) == set(b)
 
def clusterize(L, centers):
    clusters  = {}
    for val in L:
        closest = get_closest(val, centers)
        if closest in clusters:
        	clusters[closest].append(val)
        else:
            clusters[closest] = [val]
    return clusters
 
def get_mean(values):
	center_of_gravity = map(lambda v: v/len(values), map(sum, zip(*values)))
	closest = get_closest(center_of_gravity, values)
	return closest

def get_centers(centers, clusters):
    return [get_mean(values) for values in clusters.values()]
 
def kmeans(k, L):
	centers = random.sample(L, k)
	new_centers = random.sample(L, k)

	while not converged(centers, new_centers):
		centers = new_centers
		clusters = clusterize(L, new_centers)
		new_centers = get_centers(centers, clusters)

	return (centers, clusters)



if __name__ == '__main__':
	import pickle
	datafile = open("cdata.txt","r")
	vals = pickle.load(datafile)

	# k from 1 to 8, use kmeans 5 times
	# record the squared error distortion
	# plot SED as function of k showing variation

	def minimum_distance(val, centers):
		distances = [distance(val, center) for center in centers]
		return min(distances)

	def get_squared_error_distortion(vals, centers):
		total = 0
		for val in vals:
			total += math.pow(minimum_distance(val, centers), 2)
		return total / len(vals)

	seds = {}
	for k in range(1, 9):
		seds[k] = []
		for _ in range(5):
			centers, clusters = kmeans(k, vals)
			sed = get_squared_error_distortion(vals, centers)
			seds[k].append(sed)
		print k, seds[k]