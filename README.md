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


## Our idea
To solve the game we have declared a few methods that improve the grade.</br>
1. Put the agents as close as best as we can to the highest valued pokemon.(refer to add_agents)
2. Calculate all the paths for all the pokemons and for all agents, and take the best paths for each agent based on the time takes for this agent to reach that pokemon.(refer to best_paths_for_agents algorithms)



### Few Notes
* In this game we thought to use our previous excersices for the algorithms and the graph.</br>
* When catching a pokemon calculate the best paths for the agents.


## Algorithms

### [best_paths_for_agents](https://github.com/Inon-Sinn/Uni-Ariel-OOP-Ex4/blob/master/Model/Graph_Algo.py#:~:text=def%20best_Path_foreach_agent(self%2C%20agents%3A%20list%2C%20pokemons%3A%20list)%20%2D%3E%20dict%3A)

Finds the best paths for all agents.
### [add_agents](https://github.com/Inon-Sinn/Uni-Ariel-OOP-Ex4/blob/master/Model/Controller.py#:~:text=def%20add_agents(self)%3A)

Allocates the best position for the agents to start with.
### [distanceOnEdge](https://github.com/Inon-Sinn/Uni-Ariel-OOP-Ex4/blob/master/Model/Graph_Algo.py#:~:text=def%20distanceOnEdge(self%2C%20edge%2C%20pos)%20%2D%3E%20float%3A)

Given the edge and the pokemon position it calculate its distance by to the weight of the edge in the Graph
### [closestEdges](https://github.com/Inon-Sinn/Uni-Ariel-OOP-Ex4/blob/master/Model/Graph_Algo.py#:~:text=def%20closestEdges(self%2C%20pos)%20%2D%3E%20list%3A)

Return a sorted list of the edges closest to the pokemon.
### [PokemonPlacement](https://github.com/Inon-Sinn/Uni-Ariel-OOP-Ex4/blob/master/Model/Graph_Algo.py#:~:text=def%20PokemonPlacement(self%2C%20type%2C%20pos)%20%2D%3E%20tuple%3A)

Given a pokemon's position and type it returns the edges it on and the distance on the edge itself.

## Classes used

### [controller](https://github.com/Inon-Sinn/Uni-Ariel-OOP-Ex4/blob/master/Model/Controller.py#:~:text=class%20controller%3A,%22%22%22The%20Controller)
This class's purpose is to controll all the algorithms and the client calls to the server. And is seperated completely from the GUI.

### [GUI](https://github.com/Inon-Sinn/Uni-Ariel-OOP-Ex4/blob/master/GUI.py#:~:text=%22%22%22This-,class%20is%20Implements,-The%20View%2C%20The)
This class's purpose is to visualize the game and provide information about the agents and nodes in real time.
This class contains an instance of controller and lets the controller have all the communication with the server. Note that only the controller runs the algorithms and data transfers while the gui only contains controller for the purpose of getting the information and putting it on the screen.

### [agents and pokemons](https://github.com/Inon-Sinn/Uni-Ariel-OOP-Ex4/tree/master/Model/classes)
This classes provide a simple classes that hold data of the objects. It allows us to load from a json string all the objects into a list of the class's instance.

### [Graph classes and graph algorithms](https://github.com/Inon-Sinn/Uni-Ariel-OOP-Ex4/tree/master/Model)
refer to [last Excersice](https://github.com/Inon-Sinn/Uni-Ariel-OOP-Ex3/tree/master/src).

## [Video of the GUI running on case 11](https://github.com/Inon-Sinn/Uni-Ariel-OOP-Ex4/blob/master/Ex4_Video_case11.zip)

## Additional visualization
debugger mode:
![image](https://user-images.githubusercontent.com/82415308/148687021-8c04d506-8e68-407a-bc16-c7fbe32cabe2.png)</br>

regular but laggy mode:</br>
![image](https://user-images.githubusercontent.com/82415308/148687050-1ee8c540-941f-468a-ad07-8b3cc328527c.png)

we prefer to use the debugger mode as faster version

## How to run:
Open cmd and enter the directory specified for the project within the cmd.</br>
Type in: **java -jar Ex4_Server_v0.0.jar [case]**, replace case with number 0 - 15 </br> 
Afterwards run **Ex4_main.py**.

![server-client](https://user-images.githubusercontent.com/82415308/148679719-4408d648-57b2-4784-bd1b-cf04bab1db79.png)



## Contributers
[Yan](https://github.com/Yannnyan) </br>
[Inon](https://github.com/Inon-Sinn) </br>
[Yaron](https://github.com/Yaron-S) </br>


## External links

[links](https://github.com/benmoshe/OOP_2021/blob/main/Assignments/Ex4/links.txt)
