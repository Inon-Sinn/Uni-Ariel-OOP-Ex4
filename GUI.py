from pygame import gfxdraw
import pygame
from pygame import *

pygame.init()
pygame.font.init()
clock = pygame.time.Clock()

FONT = pygame.font.SysFont('Arial', 15, bold=True)


def scale(data, min_screen, max_screen, min_data, max_data):
    """
    get the scaled data with proportions min_data, max_data
    relative to min and max screen dimensions
    """
    return ((data - min_data) / (max_data - min_data)) * (max_screen - min_screen) + min_screen


class Gui:
    """This class is our GUI"""

    def __init__(self, pokemon, agents, graph, width: int, height: int):

        # special variables
        self.agents = agents  # TODO should be a list (check that pos is of int and not of String)
        self.pokemon = pokemon
        self.graph = graph  # TODO should be a DiGraph

        # screen variables
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height), depth=32, flags=pygame.constants.RESIZABLE)
        self.margin = 50

        # Coordinates used for Scaling
        self.min_x = min(list(self.graph.Nodes), key=lambda n: n.pos.x).pos.x
        self.min_y = min(list(self.graph.Nodes), key=lambda n: n.pos.y).pos.y
        self.max_x = max(list(self.graph.Nodes), key=lambda n: n.pos.x).pos.x
        self.max_y = max(list(self.graph.Nodes), key=lambda n: n.pos.y).pos.y

        # Run the Gui
        self.MainRun()

    def update(self, pokemon, agents):  # TODO we should add something that asks for an update every second or so
        self.pokemon = pokemon
        self.agents = agents

    def my_scale(self, data, x=False, y=False):
        """For now i will leave it here check if it really is needed"""
        if x:
            return scale(data, self.margin, self.screen.get_width() - self.margin, self.min_x, self.max_x)
        if y:
            return scale(data, self.margin, self.screen.get_height() - self.margin, self.min_y, self.max_y)

    def MainRun(self):
        """This is the main loop of the pygame, 60 ticks"""
        # variables
        self.margin = 50

        # Colors
        screenColor = (255, 255, 255)  # white
        NodeColor = (0, 48, 142)  # #00308E
        NodeIdColor = (255, 255, 255)  # white
        edgeColor = (120, 81, 185)  # #7851B9
        PokemonColor = (0, 255, 255)
        AgentColor = (122, 61, 23)

        # Parameters
        NodeRadius = 15
        PokemonNodeRadius = 15
        AgentsNodeRadius = 15

        while True:  # TODO can be changed later
            for gui_event in pygame.event.get():
                if gui_event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)

                if gui_event.type == pygame.MOUSEBUTTONUP:  # TODO If we decide we will only have one button this could be changed
                    click = pygame.mouse.get_pos()
                    # TODO here will be going the buttons

                # refresh surface
                self.screen.fill(pygame.Color(screenColor))

                # draw Nodes
                self.drawNodes(NodeColor, NodeIdColor, NodeRadius)

                # draw Edges
                self.drawEdges(edgeColor)

                # draw Pokemon
                self.drawPokemon(PokemonColor, PokemonNodeRadius)

                # draw Agents
                self.drawAgents(AgentColor, AgentsNodeRadius)

                # update screen changes
                pygame.display.update()

                # refresh rate
                clock.tick(60)

    def drawNodes(self, NodeColor, NodeIdColor, NodeRadius):
        pass

    def drawEdges(self, edgeColor):
        pass

    def drawPokemon(self, PokemonColor, PokemonNodeRadius):
        pass

    def drawAgents(self, AgentColor, AgentsNodeRadius):
        pass

    