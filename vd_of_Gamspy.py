import pandas as pd
from gamspy import Container, Set, Parameter, Variable, Equation, Model, Sum, Sense

#! set data
capacities = pd.DataFrame(
    [["seattle", 350], ["san-diego", 600]], columns=["city", "capacity"]
).set_index("city")

demands = pd.DataFrame(
    [["new-york", 325], ["chicago", 300], ["topeka", 275]], columns=["city", "demand"]
).set_index("city")

distances = pd.DataFrame(
    [
        ["seattle", "new-york", 2.5],
        ["seattle", "chicago", 1.7],
        ["seattle", "topeka", 1.8],
        ["san-diego", "new-york", 2.5],
        ["san-diego", "chicago", 1.8],
        ["san-diego", "topeka", 1.4],
    ],
    columns=["from", "to", "distance"],
).set_index(["from", "to"])

freight_cost = 90

# define
m= Container()
i = Set(m, "i", description="factories", records=capacities.index) 
j = Set(container=m, name="j", description="markets", records=demands.index)

# parameters(tham số)
a = Parameter(
    container=m, name="a", domain=i, description="supply of commodity at plant i (in cases)", records=capacities.reset_index(),
)
b = Parameter(
    container=m, name="b", domain=j,  description="demand for commodity at market j (in cases)", records=demands.reset_index(),
)
c = Parameter(
    container=m, name="c", domain=[i, j], description="cost per unit of shipment between plant i and market j",
)

cost = freight_cost * distances / 1000
c.setRecords(cost.reset_index())

d = Parameter(
    container=m, name="d", domain=[i, j], description="distance between plant i and market j", records=distances.reset_index(),
)

c[i, j] = freight_cost * d[i, j] / 1000

# variable
x = Variable(
    container=m, name="x", domain=[i, j], type="Positive", description="amount of commodity to ship from plant i to market j",
)

supply = Equation(
    container=m, name="supply", domain=i, description="observe supply limit at plant i"
)
demand = Equation(
    container=m, name="demand", domain=j, description="satisfy demand at market j"
)

# Sum Xichma(j)  xij <= ai Với mọi i
supply[i] = Sum(j, x[i, j]) <= a[i]
# Sim Xichma(i)  xij >= bj Với mọi j
demand[j] = Sum(i, x[i, j]) >= b[j]

# hàm mục tiêu 
obj = Sum((i, j), c[i, j] * x[i, j])

# transport để xác định model với danh sách các phương trình
transport = Model(
    m,
    name="transport",
    equations=[supply, demand],
    problem="LP",
    sense=Sense.MIN,
    objective=obj,
)

#  solve
import sys #Để xem đầu ra của bộ giải trong bảng điều khiển
transport.solve(output=sys.stdout)

# truy xuất giá trị của các biến trong giải pháp
# x.records.set_index(["i", "j"])

# Giá trị hàm mục tiêu tối ưu
# print(transport.objective_value)

#! để nhờ nhớ xóa
# # equation 8
# equation8 = Model(
#     model,
#     # equations=[],
#     problem="LP",
#     sense=Sense.MIN ,
#     #hàm mục tiêu
#     objective= Sum(j, b[j]*x[j]) + Sum(i, ps[i]*c[i]*z[i]),
# )
# # equation 6
# supply1 = Equation(
#     model, 
#     name="supply", 
#     domain=i, 
# )
# supply1[i] = z[i] <= d[i]
# supply2 = Equation(
#     model, 
#     name="supply", 
#     domain=i, 
# )
# supply2[i] = y[i] >= 0
# equation6 = Model(
#     model,
#     equations=[supply1, supply2],
#     problem="LP",
#     sense=Sense.MIN,
#     #hàm mục tiêu
#     objective=Sum(i, c[i]*z[i]) - Sum(j, s[j]*y[j]),
# )