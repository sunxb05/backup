
from functools import reduce
from pyparsing import (CaselessLiteral, Group, nums, OneOrMore, Regex, SkipTo,
                       Suppress, Word)
import numpy as np


number_to_label = {'1': 'H', '6': 'C', '7': 'N', '8': 'O'}


def main():
    filename = "gaussian outfile"
    output_file = "some_output_file"
    mols = gaussian_parser.parseFile(filename).asList()
    numat = len(mols[0]) // 4
    rss = flatten([format_molecule(m, numat, i) for i, m in enumerate(mols)])

    with open(output_file, 'w') as f:
        f.write(rss)


def format_molecule(mol, numat, i):
    data = np.array(mol).reshape(numat, 4)
    data[:, 0]  = np.apply_along_axis(fun_string, 0, data[:, 0])
    header = 'point number: {}\n'.format(i + 1)
    atoms = flatten(['{} {} {} {}\n'.format(*xs) for xs in data])

    return header + atoms + '\n\n'


def flatten(xs):
    return reduce(lambda x, y: x + y, xs)


# Numpy
fun_string = np.vectorize(lambda x: number_to_label[x])

# Parser
natural = Word(nums)

floatNumber = Regex(r'(\-)?\d+(\.)(\d*)?([eE][\-\+]\d+)?')

skipSupress = lambda z: Suppress(SkipTo(z))

skipLine = Suppress(skipSupress('\n'))

delta = CaselessLiteral("Delta-x Convergence Met")

parse_header = skipSupress(delta) + skipSupress(CaselessLiteral('Angstroms')) + skipLine * 3

parse_atom_line = Suppress(natural) + natural + Suppress(natural) + floatNumber * 3

parse_mol = Suppress(parse_header) + OneOrMore(parse_atom_line)

gaussian_parser = OneOrMore(Group(parse_mol))


if __name__ == "__main__":
    main()
