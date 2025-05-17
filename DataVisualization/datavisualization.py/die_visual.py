from plotly.graph_objs import Bar, Layout
from plotly import offline
from die import Die

#create a D6 and a D10
die_1=Die()
die_2=Die(10)

#make some rolls, and store results in a list 
results=[]
for roll_num in range(50_000):
    result=die_1.roll() + die_2.roll()
    results.append(result)


#Analyze the results
frequancies=[]
max_result=die_1.num_sides+die_2.num_sides
for value in range(2, max_result+1):
    frequancy=results.count(value)
    frequancies.append(frequancy)
#visualize the results
x_values=list(range(2, max_result+1))
data=[Bar(x=x_values, y=frequancies)]

x_axis_config={'title':'Result', 'dtick':1}
y_axis_config={'title':'Frequancy of Result '}
my_layout=Layout(title='Results of rolling two D6 and d10 50000 times',xaxis=x_axis_config, yaxis=y_axis_config)
offline.plot({'data':data,'layout':my_layout},filename='d6_d10.html')


print(frequancies)
