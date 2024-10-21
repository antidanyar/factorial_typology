import json
from argparse import ArgumentParser
from itertools import permutations


def evaluate(grammar, inputs): # TODO: docstring + typehints
    outputs = []
    for input in inputs:
        candidates = input['Candidates'].copy()
        for constraint in grammar:
            candidates_left = []
            for candidate in candidates:
                if not candidate[constraint]:
                    candidates_left.append(candidate)
            candidates = candidates_left.copy()
            if len(candidates) == 1:
                outputs.append((input['UR'], candidates[0]['SR']))
                break
    return tuple(outputs)


def factorial_typology(constraints, inputs): # TODO: docstring + typehints
    grammars = list(permutations(constraints))
    typology = {}
    for grammar in grammars:
        output = evaluate(grammar, inputs)
        if output not in typology:
            typology[output] = list()
        typology[output].append(grammar)
    return typology


def get_proportions(constraints, inputs): # TODO: docstring + typehints
    grammar_count = []
    typology = factorial_typology(constraints, inputs)
    for mapping in typology:
        grammar_count.append((mapping, len(typology[mapping])))
    return tuple(grammar_count)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-i', '--input_path', type=str, default='./data/case1.json')
    args = parser.parse_args()

    with open(args.input_path, 'r') as f:
        inputs = json.load(f)

    # TODO: pretty print + wrap outputs
    print(*get_proportions(**inputs), sep='\n')

