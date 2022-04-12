from pylab import *
from matplotlib.patches import Rectangle, Circle
from matplotlib.collections import PatchCollection
# import matplotlib.colors as mcolors



box = Rectangle( xy = (-.5,-.5), width = 1, height = 1, ec="none" )


r = .11
dy = 2.7*r
dx = dy

line_lengths = [2,3,2]
y = -dy*( len( line_lengths ) - 1 )/2

holes = []

for line_length in line_lengths :

    x = -dx*( line_length - 1 )/2

    for _ in range( line_length ) :

        holes += [  Circle( xy = (x,y), radius = r, ec="none") ]

        x += dx

    y += dy

led = [  Circle( xy = (.4,-.4), radius = .035, ec="none") ]

fig = figure( figsize = (6,6) )
ax = axes([0,0,1,1])

ax.add_collection( PatchCollection( [ box ], color = 'orange'))
ax.add_collection( PatchCollection( holes, color = 'darkslategrey') )
ax.add_collection( PatchCollection( led, color = 'gold') )


ax.set_xlim(-.5,.5)
ax.set_ylim(-.5,.5)

savefig( 'favicon.svg' )

show()
