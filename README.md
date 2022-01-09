# Pokemon Game in python!

## Description
This project's purpose was to create a special game, represent it with a GUI and solve the game as best as we can.</br>
The rules of the game are rather simple. There is a weighted not directed graph represented by nodes and edges, and two special entities.</br>
One entity is a "Pokemon" which has a ceratin value, meaning that some pokemons worth more than others. And the other entity is an "Agent".</br> The Pokemons spawn randomly on the graph, but we have all the control on the Agents.
The target is to maximize the sum value of the pokemons caught, and that number will be defined as "Grade".</br>

### Few Notes:
* We are given a server jar file. which will communicate with a socket to our client. meaning that only the server may change the position of the agents and the pokemons.</br>
* The maximum amount of calls to move an agent within a second is only 10.</br>
* The game only lasts 30 to 120 seconds.</br>
* Each pokemon has a field named "type", which is defining which way the agent can reach the pokemon. The pokemon might be unreachable from src -> dest but reachable from dest -> src.
* Each Agent has: speed, position, value (i.e the sum value of pokemons it caught), id, src (i.e the id of the node it left or current at), dest (i.e destination node else -1).
* Each Pokemon has position, value, type.


## Out idea
To solve the game we have declared a few methods that improve the grade.</br>
1. Put the agents as close as best as we can to the highest valued pokemon.(refer to add_agents)
2. Calculate all the paths for all the pokemons and for all agents, and take the best paths for each agent based on the time takes for this agent to reach that pokemon.(refer to best_paths_for_agents, and shortest_path algorithms)
3. 
4. 



### Few Notes
* In this game we thought to use our previous excersices for the algorithms and the graph.</br>
* When catching a pokemon calculate the best paths for the agents.





## Contributers
[Yan](https://github.com/Yannnyan)
[Inon]()
[Yaron]()




[links](https://github.com/benmoshe/OOP_2021/blob/main/Assignments/Ex4/links.txt)
