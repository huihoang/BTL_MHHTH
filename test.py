import numpy as np
import numpy.matlib 
from gamspy import Container, Set, Parameter, Variable, Equation, Model, Sum, Sense

n = 8 # loại sản phẩm
m = 5

# Khởi tạo các Set và Parameter
model = Container()
i = Set(model, name="i", description="productions", records=["i" + str(x) for x in range (1, n+1)])
j = Set(model, name="j", description="materials", records=["j" + str(x) for x in range (1, m+1)])
