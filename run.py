

import os

print('\nStarted run.py, get_directions_for_zones.py......... ' )
os.system('python get_directions_for_zones.py')

print('\nCalculating intersectedCircles.js......... ')
os.system('node get_intersections.js')
print('\nCalculated intersectedCircles.js!  ')

print('\nCalculating set_cover_greedy.py......... ')
os.system('python set_cover_greedy.py')
print('\nCalculated set_cover_greedy.py. All done  ')
