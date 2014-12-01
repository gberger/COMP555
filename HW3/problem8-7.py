from hw3 import *

if __name__ == '__main__':
	g = Graph()

	for i in range(100):
		a = i/10
		b = i%10
		g.connect(a, b, i)

	s = ""
	for edge in g.eulerian_path():
		s += str(edge.src.name)
	print s
