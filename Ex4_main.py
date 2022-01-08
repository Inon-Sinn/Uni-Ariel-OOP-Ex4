
from Model.fucked_graph_algo import GraphAlgo

if __name__ == '__main__':
    algo = GraphAlgo()
    algo.load_from_json("data/A0")
    pos = (35.195224052340706,32.10575624080796)
    print(algo.closestEdges(pos))
    distances = algo.closestEdges(pos)
    distances = sorted(distances, key=lambda x: x[2])
    print(distances)
    print(algo.edgeByType(-1, distances))
    print(algo.PokemonPlacement(-1, pos))


# "data/A0"

# pos='35.197656770719604,32.10191878639921,0.0' - (9,8)

# 35.199963710098416,32.105723673136964 - (4,3)

# 35.195224052340706,32.10575624080796 - (3,2)

# 35.19494883961552,32.105809680537625 - (3,2)
