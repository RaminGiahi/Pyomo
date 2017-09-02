from __future__ import division
from pyomo.environ import *

model = AbstractModel()

model.M = Set()
model.N = Set()

model.n = Param()
model.c = Param(model.M, model.N)

model.x = Var(model.M, model.N, domain=Binary)
model.u = Var(model.M, domain=NonNegativeIntegers)

def object(model):
    return sum(model.c[i,j]*model.x[i,j] for (i,j) in model.M*model.N if i!=j)

model.obj = Objective(rule=object)

def const1(model,j):
    return sum(model.x[i,j] for i in model.M if i!=j) == 1

model.cons = Constraint(model.N, rule= const1)

def const2(model,i):
    return sum(model.x[i,j] for j in model.N if j!=i) ==1

model.cons2 = Constraint(model.M, rule=const2)

def const3(model,i,j):
    if i==j or i <2 or j<2:
        return Constraint.Skip
    return model.u[i]-model.u[j]+model.n*model.x[i,j] <= model.n-1

model.cons3 = Constraint(model.M, model.N, rule=const3)

instance = model.create("salesman.dat")
instance.pprint()
