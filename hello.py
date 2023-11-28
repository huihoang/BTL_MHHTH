print("---------------Start World!-----------------\n")

#! convert the sample problem into BTL
    #* Indices (Sets):
    #*             i = product, j = material
    #* Parameters:
    #*             b = pre-order_cost, l = production_cost, q = sale, s = inventory_cost, d = demand, c= l-q , a = maxtrix [i,j]
    #* Decision variables:
    #*             x = pre-order_material, y = inventory, z = production
    #* Constraints:
    #*             i,j > 0
    #*             sj < bj
    #*             0 <= z <= d
    #*             y >= 0
    #*             ci = li - qi
    #*             yj = xj - SumXichMa(aij.zi)
    #*             Objective Function: min Z(z,y) = SumXichMa(li - qi)zi + SumXichMa(sj.yj)

# import pandas as pd
import numpy as np  
from gamspy import Container, Set, Parameter, Variable, Equation, Model, Sum, Sense

model=Container()
n=8 # i type product
m=5 # j type material
scenario = 2 # 2 scenario

sc=Set(model, name ="sc", description="scenario", records= ["sc"+ str(k) for k in range (1, scenario + 1)])
i=Set(model, name="i", description="productions", records=["i" + str(x) for x in range (1,n+1)])
j=Set(model, name="j", description="materials", records=["j" + str(x) for x in range (1,m+1)])

b=Parameter(
    model, name="b", description="pre-order_cost",
    domain=j,
    records= np.random.randint(1, 100, size=(1,m)),
)
s=Parameter(
    model, name="s", description="inventory_cost",
    domain=j,
    records= np.random.randint(1, 100, size=(1,m)),
)
l=Parameter(
    model, name="l", description="production_cost",
    domain=i,
    records= np.random.randint(1, 100, size=(1,n)),
)
q=Parameter(
    model, name="q", description="sale",
    domain=i, 
    records= np.random.randint(1, 100, size=(1,n)),
)
c=Parameter(
    model, name="c", domain=i,
)
c[i] = l[i] - q[i]

ps=Parameter(
    model, name="ps", description="probability of scenario",
    domain= sc,
)
ps[sc]= 0.5

d=Parameter(
    model,  name="d",
    domain=[sc,i],
    records= np.random.binomial(10, 0.5, size=(scenario,n)),
)
a=Parameter(
    container=model, name="a",
    domain=[i, j],
    # matrix A(n x m)
    description="aij",
    records= np.random.randint(10, size=(8, 5))
)

x=Variable(
    model, name="x",
    domain= j,
    type="positive", description="Sum pre-order_material",
)
y=Variable(
    model, name="y",
    domain= j,
    type="positive", description="inventory"
)
z=Variable(
    model, name="z",
    domain= i,
    type="positive", description="production"
)

supply1 = Equation(
    model, name="supply1", domain=j,
)
supply1[j] = x[j] >= 0

supply2 = Equation(
    model,  name="supply2", domain=j, 
)
# y[j] = x[j] - Sum(i, a[i,j]*z[i]) >= 0
supply2[j] = x[j] - Sum(i, a[i,j]*z[i]) >= 0

supply3 = Equation(
    model,  name="supply3",  domain=[i,j], 
)
supply3[i,j] = a[i,j] >= 0

supply4 = Equation(
    model,  name="supply4",  domain=j, 
)
supply4[j] = s[j] < b[j]

demand1 = Equation(
    model, name="demand1",  domain=i, 
)
demand1[i] = z[i] <= d[i]

demand2 = Equation(
    model, name="demand2", domain=i, 
)
demand2[i] = z[i] >= 0

#! equation 7+8
equation78 = Model(
    model, name="equation78",
    equations=[supply1, supply2, supply3, supply4, demand1, demand2],
    problem="LP",
    #tính min
    sense=Sense.MIN,
    #hàm mục tiêu
    objective= Sum(j, b[j]*x[j]) - Sum(sc, ps[sc]*(Sum(i, c[i]*z[i]) + Sum(j, s[j]*(x[j] - Sum(i, a[i,j]*z[i]))))),
)

#  solve
import sys
equation78.solve(output=sys.stdout)
print("\n----------------End program----------------")