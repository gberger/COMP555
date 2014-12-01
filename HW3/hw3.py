class Edge(object):
	def __init__(self, src, dst, label):
		self.src = src
		self.dst = dst
		self.label = label
		self.used = False
		self.src.add_edge(self)

class Vertex(object):
	def __init__(self, name):
		self.name = name
		self.edges = []
		self.degree = 0

	def add_edge(self, edge):
		self.edges.append(edge)

	def get_unused_edge(self):
		for edge in self.edges:
			if not edge.used:
				return edge
		return None

	def has_unused_edge(self):
		return self.get_unused_edge() != None

class Graph(object):
	def __init__(self):
		self.vertices = []
		self.edges = []

	def find_and_increment_or_create_vertex(self, name):
		for vertex in self.vertices:
			if vertex.name == name:
				vertex.degree += 1
				return vertex
		v = Vertex(name)
		v.degree += 1
		self.vertices.append(v)
		return v

	def connect(self, src, dst, label):
		v_src = self.find_and_increment_or_create_vertex(src)
		v_dst = self.find_and_increment_or_create_vertex(dst)
		edge = Edge(v_src, v_dst, label)
		self.edges.append(edge)

	def is_eulerian(self):
		for vertex in self.vertices:
			if vertex.degree % 2 != 0:
				return False
		return True

	def eulerian_tour(self, starting_vertex):
		tour = []
		current_vertex = starting_vertex
		while True:
			edge = current_vertex.get_unused_edge()
			if edge == None:
				return tour
			edge.used = True
			tour.append(edge)
			current_vertex = edge.dst

	def eulerian_path(self):
		"""
		Uses Hierholzer's algorithm, described here: 
		https://en.wikipedia.org/wiki/Eulerian_path#Hierholzer.27s_algorithm
		"""
		if not self.is_eulerian():
			# If a graph is not Eulerian, there is no Eulerian path.
			return None
		self.reset_edges()

		path = self.eulerian_tour(self.vertices[0])
		while len(path) != len(self.edges):
			for idx, edge in enumerate(path):
				if edge.dst.has_unused_edge():
					detour = self.eulerian_tour(edge.dst)
					path = path[:idx+1] + detour + path[idx+1:]
		return path

	def reset_edges(self):
		"""
		Resets all edges back to unused
		"""
		for edge in self.edges:
			edge.used = False


def transform_path(path):
	if path == None:
		return None
	return (
		path[0].src.name,
		map(lambda e: e.label, path),
		path[-1].dst.name,
	)


def euler(edges):
	g = Graph()
	for edge in edges:
		g.connect(edge[0], edge[1], edge[2])
	return transform_path(g.eulerian_path())

if __name__ == '__main__':
	edges = [
		('a', 'b', 1),
		('b', 'c', 2),
		('c', 'a', 3)
	]
	print euler(edges)