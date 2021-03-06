from __future__ import division
from pyomo.environ import *

model = AbstractModel()

model.M = Set()
model.N = Set()

model.p = Param()
model.d = Param(model.N)
model.c = Param(model.M, model.N)

model.x = Var(model.M, model.N, domain=NonNegativeReals)
model.y = Var(model.M, domain=Binary)

def object(model):
    return sum(model.d[j] * model.c[i,j] * model.x[i,j] for (i,j) in model.M * model.N )

model.obj = Objective(rule=object)

def cons1(model,j):
    return sum(x[i,j] for i in model.M)==1

model.const = Constraint(model.N, rule=cons1)

def const2(model):
    return sum(model.y[i] for i in model.M) == model.p

model.const2 = Constraint(rule=const2)

instance = model.create("pmedian.dat")
instance.pprint()