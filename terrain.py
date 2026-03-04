# This file is to:
# Generate the terrain

def make_terrain():
    terrain = []
    
    for i in range(10):
        for i in range(20):
            terrain.append("stone")
    
    return(terrain)

print(make_terrain())