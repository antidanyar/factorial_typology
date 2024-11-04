from itertools import permutations
from pprint import pp

# a dummy set of set constraints and inputs
constraints = [
    'Ident-F', 'DEP', 'LIN', '*VV', 'Agree(VV)'
]
inputs = [
    {
        'UR': 'aa',
        'candidates':
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
        'candidates':
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
        'candidates':
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

def numToBool(value: int) -> bool:
  '''
  maps numerals to bools
  '''
  return value > 0

def cleanList(l: list) -> list:
  '''
  is used to clean up the initial empty tabulations and the final "\n"
  '''
  l2 = list()
  i = 0
  while l[i] == "":
    i+=1
  while i < len(l):
    if l[i] == '':
      l2.append("0")
    else:
      l2.append(l[i])
    i += 1
  if l2[-1][-1] == '\n':
    l2[-1] = l2[-1][:-1]
  return l2

def readOTS(filename: str) -> tuple:
  '''
  Creates the constraints list and the inputs list from an OT-Soft/OT-Help-compatible file.
  Assumptions about the OT-soft file:
    (i) tabs as delimiters
    (ii) violations are marked by "1"s, lack of violations is either unmarked or marked by zero
    (iii) winner candidate is marked by 1, loser candidates are either unmarked or marked by zero
  '''
  data = open(filename, "r")
  constraints = cleanList(data.readline()[:-1].split("\t"))
  constraints = cleanList(data.readline()[:-1].split("\t"))
  #reads the doubly repeated list of constraints; deletes the final "\n"
  inputs = []
  input = dict()
  for line in data.readlines():
    if line[0] == "/":
      input = dict()
      input['UR'] = line.split("\t")[0]
      surface = line.split("\t")[1:]
      input['candidates'] = list()
      inputs.append(input)
    else:
      surface = cleanList(line.split("\t"))
    surfaceRep = {}
    surfaceRep['SR'] = surface[0]
    for i in range(0, len(surface)-2):
      surfaceRep[constraints[i]] = numToBool(int(surface[i+2]))
    #adding two is required to ignore the column that indpicates the winning candidate in the OTsoft-like file
    inputs[-1]['candidates'].append(surfaceRep)
    #adds the newest SR and its constraint violations to the latest UR
  data.close()
  return constraints, inputs

def evaluate(grammar: list, inputs:list) -> tuple:
  '''
  Returns a tuple of input-output mappings.

  Takes the grammar (ordered list of constraints) and the inputs
  (list of URs, candidates and whether they violate a constraint)
  as arguments.
  '''
  outputs = []
  for input in inputs:
    candidates = input['candidates'].copy()
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

def factorial_typology(constraints:list, inputs:list) -> dict:
  '''
  Computes a factorial typology: a list of pairs of input-output mappings and
  the lists of grammars that generate these mappings.

  Takes the list of constraints and the list of inputs as arguments.
  '''
  grammars = list(permutations(constraints))
  typology = {}
  for grammar in grammars:
    output = evaluate(grammar, inputs)
    if output not in typology:
      typology[output] = list()
    typology[output].append(grammar)
  return typology

def get_proportions(constraints:list, inputs:list) -> tuple:
  '''
  Returns the proportion of input-output mappings in the resulting factorial typology.

  Takes the list of constraints and the list of inputs as arguments.
  '''
  grammar_count = []
  typology = factorial_typology(constraints, inputs)
  for mapping in typology:
    grammar_count.append((mapping, len(typology[mapping])))
  return tuple(grammar_count)
  

constraints, inputs = readOTS("manual.txt")

pp(constraints)

pp(inputs)

pp(get_proportions(constraints, inputs))


