import matplotlib.pyplot as plt
from random_walk import RandomWalk

#make a random walk
while True:
   rw=RandomWalk()
   rw.fill_walk()

   #plot the points in the walk 
   plt.style.use('classic')
   fig, ax=plt.subplots()
   point_numbers=range(rw.num_points)
   ax.scatter(rw.x_values,rw.y_values, c=point_numbers,cmap=plt.cm.Blues, edgecolors='none', s=15)
   plt.savefig()

   keep_running=input("make another walk? (y/n):")
   if keep_running=='n':
    break