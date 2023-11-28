import numpy as np
import numpy.matlib 
import pandas as pd
from gamspy import Container, Set, Parameter, Variable, Equation, Model, Sum, Sense

n = 8 # loại sản phẩm
m = 5

# Khởi tạo các Set và Parameter
model = Container()
i = Set(model, name="i", description="productions", records=["i" + str(x) for x in range (1, n+1)])
j = Set(model, name="j", description="materials", records=["j" + str(x) for x in range (1, m+1)])


l = Parameter(model, name="l", domain=i, records=np.random.randint(1, 10, size=(1, n)))


a=Parameter(
    container=model, name="a",
    domain=[i, j],
    description="aij",
    records=np.random.randint(10, size=(8, 5)),
)
x = Variable(
    container=model, name="x",
    domain= j,
    type="positive",
    description="Sum pre-order_material",
)
x[j] = Sum(i, a[i, j])
print(x.records)