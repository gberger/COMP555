import itertools
from math import floor

def greedyChange(m, d):
	result = []
	for coin in d:
		quo, rem = int(m/coin), m%coin
		result.append(quo)
		m = rem
	return result

def xsChange(m, d):
	solutions = [[0 for i in d]]
	minCoinsUsed = float("inf")

	ss = searchSpace(m, d)
	ss = map(xrange, ss)
	for attempt in itertools.product(*ss):
		coinsUsed = sum(attempt)
		if coinsUsed <= minCoinsUsed:
			if validSolution(m, d, attempt):
				if coinsUsed == minCoinsUsed:
					solutions.append(list(attempt))
				else:
					minCoinsUsed = coinsUsed
					solutions = [list(attempt)]
	return solutions

def isMultiple(a, b):
	return b % a == 0

def validSolution(m, d, s):
	return m == sum(a*b for a, b in zip(d, s))

def searchSpace(m, d):
	def coinSearchSpace(m, d, coin):
		x = floor(float(m)/coin) + 1
		for mul in d:
			if mul > coin:
				if isMultiple(coin, mul):
					x = min(x, mul/coin)
			else:
				break
		return int(x)
	return [coinSearchSpace(m, d, coin) for coin in d]


def isGreedyOK(d):
	for m in xrange(100):
		greedySolution = greedyChange(m, d)
		xsSolutions = xsChange(m, d)
		if sum(greedySolution) != sum(xsSolutions[0]):
			print m
			return False
	return True

def avgCoinsChange(d):
	return sum([sum(xsChange(m, d)[0]) for m in xrange(100)])/100.0
