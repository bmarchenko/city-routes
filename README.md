
Introduction
============
This is a dummy project that calculates routes in city grid that is represented by blocks of x,y coordinates.
User can use similar to natural language instructions about where to move and get calculated routes with exact coordinates.
It assumes that the route must move strictly vertically or horizontally and calulates coordinates "turn points" or vertexes of the route.
It is MVP, and therefore, is not designed to be fast or flexible. 


How to use
==========
Run script with proper arguments `python routes.py --filepath=<filepath> --route=<route id>`
For example  `python routes.py --filepath=routes_example.json --route=1` will produce the following output:

````
Starting point: 1, 2
Parsing command 'GO 5 N'
1 7 N
Parsing command 'GO 4 W'
5 7 W
Parsing command 'TURN left'
5 7 N
Parsing command 'GO 120'
5 127 N
END

````

Domain Specific Language
========================
Upload file is a dictionary where keys must be unique Route IDs, 
values are lists of instructions written in DSL. 
DSL has two commands:
1. "Start" is represented by the very first coordinates couple e.g `1,2` says that routes starts from x=1, y=2 coordinates.
2. "Go" is identified with "GO" at the beginning. The second item must be distance to move. It may be represented either 
by number of blocks to move or by a landmark to reach. Finally, it may contain direction, one of "N"(North), "W"(West), "S"(South), "E"(East).
If direction is not provided, the last one will be used e.g. ``GO 5 N``, `GO 120`
3. "Turn" is an instruction that changed routes direction. It must be one of "left" or "right". 

See file routes_example.csv in order to see some basic examples of the route language.

Further Improvements
====================
- Decrease memory usage. Currently all routes data is being kept in memory even though only one is calulated. 
- If same route would be queried multiple times, it makes sense to cache the calculation results.
- If number of users raise and speed is not important to them, pre or post calculation may take place in order to balance resources.
- If number of routes raise and more complex calculation is needed, for example "find the closest path to landmark" or 
"find routes how to get from point to point changing routes" it may be worth to look to graph databases, like Neo4j or OrientDB.
- If routes are complex and have thousands of instructions, it make sense to calculate iteratively on user's demand, 
for example calulate next step only when previous reached. Do not keep all route in memory.
  

 