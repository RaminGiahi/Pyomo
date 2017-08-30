from __future__ import division
from pyomo.environ import *

model = AbstractModel()

model.N = Set()
model.A = model.N * model.N

model.s = Set()
model.t = Set()
model.A2 = model.N * model.t

model.NST = model.N - model.s - model.t

model.c = Param(model.A)

model.f = Var(model.A, domain = NonNegativeReals)

def objective(model):
    return sum(model.c[i,t]*model.f[i,t] for (i,t) in model.A2)

model.object = Objective(rule = objective, sense = maximize)

def const1(model,i,j):
    return model.f[i,j] <= model.c[i,j]

model.constraint1 = Constraint(model.A, rule = const1)


def const2(model,j):
    return sum(model.f[i,j] for i in model.N)== sum(model.f[j,i] for i in model.N)

model.constraint2 = Constraint(model.NST, rule = const2)


instance = model.create("maxflow.dat")
instance.pprint()