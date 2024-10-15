from itertools import permutations

constraints = [
    'Ident-F', 'DEP', 'LIN', '*VV', 'Agree(VV)'
]
inputs = [
    {
        'UR': 'aa',
        'Candidates':
         [
             {'SR': 'aa',
              'Ident-F': False,
              'DEP': False,
              'LIN': False,
              '*VV': True,
              'Agree(VV)': False
              },
             {'SR': 'a?a',
              'Ident-F': False,
              'DEP': True,
              'LIN': False,
              '*VV': False,
              'Agree(VV)': False
              },
             {'SR': 'a',
              'Ident-F': False,
              'DEP': False,
              'LIN': True,
              '*VV': False,
              'Agree(VV)': False
              }
         ]
    },
    {
        'UR': 'ao',
        'Candidates':
        [
            {
                'SR': 'ao',
                'Ident-F': False,
                'DEP': False,
                'LIN': False,
                '*VV': True,
                'Agree(VV)': True
            },
            {
                'SR': 'a?o',
                'Ident-F': False,
                'DEP': True,
                'LIN': False,
                '*VV': False,
                'Agree(VV)': False
            },
            {
                'SR': 'a',
                'Ident-F': True,
                'DEP': False,
                'LIN': True,
                '*VV': False,
                'Agree(VV)': False
            }
        ]
    }
]

constraints2 = [
    'Ident-F', 'DEP', 'LIN', '*VV',
]
inputs2 = [
    {
        'UR': 'aa',
        'Candidates':
         [
             {'SR': 'aa',
              'Ident-F': False,
              'DEP': False,
              'LIN': False,
              '*VV': True,
              'Agree(VV)': False
              },
             {'SR': 'a?a',
              'Ident-F': False,
              'DEP': True,
              'LIN': False,
              '*VV': False,
              'Agree(VV)': False
              },
             {'SR': 'a',
              'Ident-F': False,
              'DEP': False,
              'LIN': True,
              '*VV': False,
              'Agree(VV)': False
              }
         ]
    },
    {
        'UR': 'ao',
        'Candidates':
        [
            {
                'SR': 'ao',
                'Ident-F': False,
                'DEP': False,
                'LIN': False,
                '*VV': True,
                'Agree(VV)': True
            },
            {
                'SR': 'a?o',
                'Ident-F': False,
                'DEP': True,
                'LIN': False,
                '*VV': False,
                'Agree(VV)': False
            },
            {
                'SR': 'a',
                'Ident-F': True,
                'DEP': False,
                'LIN': True,
                '*VV': False,
                'Agree(VV)': False
            }
        ]
    }
]

def evaluate(grammar, inputs):
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

def factorial_typology(constraints, inputs):
  grammars = list(permutations(constraints))
  typology = {}
  for grammar in grammars:
    output = evaluate(grammar, inputs)
    if output not in typology:
      typology[output] = list()
    typology[output].append(grammar)
  return typology

def get_proportions(constraints, inputs):
  grammar_count = []
  typology = factorial_typology(constraints, inputs)
  for mapping in typology:
    grammar_count.append((mapping, len(typology[mapping])))
  return tuple(grammar_count)

get_proportions(constraints, inputs)

get_proportions(constraints2, inputs2)

