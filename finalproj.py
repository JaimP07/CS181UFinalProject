from z3 import *

n = int(input('How many nodes? '))

#nodes
nodes = [0]*n
for i in range(len(nodes)):
    nodes[i] = Int('node'+str(i+1))

#edges
def Edges(a, b):
    return Not(nodes[a-1] == nodes[b-1])

print('Add your edges:')
e = input()
edges = []
while e!='.':
    edge = e.split(',')
    edges.append(Edges(int(edge[0]),int(edge[1])))
    e = input()

cmax = int(input('What is the maximum degree of your graph? '))

ranges = [And(1 <= x, x <= cmax+1) for x in nodes]

constraints = [] 
constraints += edges

s = Solver()
s.add(ranges)
s.add(constraints)

minmodel = []
chrom = len(nodes)+1

while(str(s.check()) == 'sat'):
    m = s.model()

    L = []
    for d in m:
        L += [m[d]]
    cset = {c for c in L}

    if len(cset)<chrom:
        chrom = len(cset)
        minmodel = m

# collect the variables from the model m
    model_vars = [v for v in m]
# collect the values of all of the variables
    model_vals = [m[v] for v in model_vars]

# take disjunction of negations of variable assignments 
    blocked_model = Or([(var() != val) for (var,val) in zip(model_vars, model_vals)])

# add the blocked clause
    s.add(blocked_model)

print(minmodel)
print('Chromatic number: '+str(chrom))