from sys import argv
from itertools import izip_longest, takewhile

# Table from https://en.wikipedia.org/wiki/DNA_codon_table
codon_table = {
	'TAT': 'Tyr', 
	'AAA': 'Lys', 
	'TGT': 'Cys', 
	'GGT': 'Gly', 
	'TCT': 'Ser', 
	'TAG': 'Stp', 
	'TTT': 'Phe', 
	'TGC': 'Cys', 
	'TGA': 'Stp', 
	'TGG': 'Trp', 
	'TAC': 'Tyr', 
	'TTC': 'Phe', 
	'TCG': 'Ser', 
	'TTA': 'Leu', 
	'TTG': 'Leu', 
	'TCC': 'Ser', 
	'TCA': 'Ser', 
	'GCA': 'Ala', 
	'GTA': 'Val', 
	'GCC': 'Ala', 
	'GTC': 'Val', 
	'GCG': 'Ala', 
	'GTG': 'Val', 
	'CGT': 'Arg', 
	'GTT': 'Val', 
	'GCT': 'Ala', 
	'ACC': 'Thr', 
	'GAT': 'Asp', 
	'CGA': 'Arg', 
	'CGC': 'Arg', 
	'ACT': 'Thr', 
	'AAG': 'Lys', 
	'CGG': 'Arg', 
	'GGG': 'Gly', 
	'GGA': 'Gly', 
	'GGC': 'Gly', 
	'GAG': 'Glu', 
	'CAG': 'Gln', 
	'GAC': 'Asp', 
	'CAA': 'Gln', 
	'GAA': 'Glu', 
	'CTT': 'Leu', 
	'ATG': 'Met', 
	'ACA': 'Thr', 
	'ACG': 'Thr', 
	'ATC': 'Ile', 
	'AAC': 'Asn', 
	'ATA': 'Ile', 
	'AGG': 'Arg', 
	'CCT': 'Pro', 
	'AGC': 'Ser', 
	'AGA': 'Arg', 
	'CAT': 'His', 
	'AAT': 'Asn', 
	'ATT': 'Ile', 
	'CTG': 'Leu', 
	'CTA': 'Leu', 
	'CTC': 'Leu', 
	'CAC': 'His', 
	'CCG': 'Pro', 
	'AGT': 'Ser', 
	'CCA': 'Pro', 
	'CCC': 'Pro', 
	'TAA': 'Stp'
}

# Inverse table, i.e.,
# 'Cys': ['TGT', 'TGC'], etc
amino_table = {}
for k, v in codon_table.iteritems():
    amino_table[v] = amino_table.get(v, [])
    amino_table[v].append(k)

# Helper method. Separates a string into smaller strings
# of n characters each
def grouper(n, iterable, fillvalue=None):
    "grouper(3, 'ABCDEFG', 'x') --> ['ABC', 'DEF', 'Gxx']"
    args = [iter(iterable)] * n
    return [''.join(x) for x in izip_longest(fillvalue=fillvalue, *args)]

# Given a filename and an offset, read the FASTA file, 
# and return the sequence stored, offset by the given amount,
# up until a Stp codon, inclusive
def read_fasta_file(filename, offset = 1):
	with open(filename) as f:
		valid_lines = f.readlines()[1:]
		stripped_lines = [line.strip() for line in valid_lines]
		sequence = ''.join(stripped_lines)
		return sequence[offset-1:]

# Transforms a string sequence into an array of codons
def sequence_to_codons(sequence):
	return grouper(3, sequence, 'x')

# Checks if a codon is a stop
def is_stop(codon):
	return codon_table[codon] == 'Stp'

# Returns the index of the first stop codon in an array of codons
def first_stop_index(codons):
	for i, codon in enumerate(codons):
		if is_stop(codon):
			return i
	return None

# Restrict an array of codons to go only until a stop codon
def codons_until_stop(codons):
	idx = first_stop_index(codons)
	if idx == None:
		raise ValueError('Sequence has no stop')
	else:
		return codons[:idx+1]

# Receives an array of codons.
# Prints each amino acid (in alphabetic order), along with the
# synonymous codons for this amino acid
# For each amino acid list the synonymous codons, and for each synonym,
# how many times it occurs and the percentage over all the synonyms for this
# amino acid.
def print_stats(codons):
	occurrences = dict((key, 0) for key in codon_table.keys())
	
	for codon in codons:
		occurrences[codon] += 1

	for amino, synonyms in iter(sorted(amino_table.iteritems())):
		s = amino + ": "

		total_for_amino = 0
		for synonym in synonyms:
			total_for_amino += occurrences[synonym]

		if total_for_amino == 0:
			total_for_amino = 1;
		
		for synonym in synonyms:
			s += "[%s %d %.2f%%] " % (
					synonym, 
					occurrences[synonym],
					occurrences[synonym]*100.0/total_for_amino
				)

		print s


if __name__ == '__main__':
	filenames = argv[1::2]
	offsets = argv[2::2]
	pairs = zip(filenames, offsets)

	all_codons = []

	for filename, offset in pairs:
		offset = int(offset)
		sequence = read_fasta_file(filename, offset)
		codons = sequence_to_codons(sequence)
		all_codons += codons_until_stop(codons)

	print_stats(all_codons)