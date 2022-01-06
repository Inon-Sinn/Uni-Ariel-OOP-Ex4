from pygame import gfxdraw
import pygame
from pygame import *

from Model.GraphAlgo import GraphAlgo

pygame.init()
pygame.font.init()
clock = pygame.time.Clock()

FONT = pygame.font.SysFont('Arial', 15, bold=True)

WIDTH, HEIGHT = 900, 740


def scale(data, min_screen, max_screen, min_data, max_data):
    """
    get the scaled data with proportions min_data, max_data
    relative to min and max screen dimensions
    """
    return ((data - min_data) / (max_data - min_data)) * (max_screen - min_screen) + min_screen


class Gui:
    """This class is our GUI"""

    def __init__(self, graph, width: int, height: int, runtime: float, pokemon=None, agents=None):

        # special variables
        if agents is None:
            agents = []
        if pokemon is None:
            pokemon = []
        self.agents = agents
        self.pokemon = pokemon
        self.timer = runtime
        self.points = 0
        self.mc = 0
        self.graph = graph  # TODO should be a DiGraph

        # screen variables
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height), depth=32, flags=pygame.constants.RESIZABLE)
        self.margin = 50
        self.upperMargin = self.screen.get_height() / 8

        # Coordinates used for Scaling
        self.min_x = min(self.graph.get_all_v().values(), key=lambda n: n.pos[0]).pos[0]
        self.max_x = max(self.graph.get_all_v().values(), key=lambda n: n.pos[0]).pos[0]
        self.min_y = min(self.graph.get_all_v().values(), key=lambda n: n.pos[1]).pos[1]
        self.max_y = max(self.graph.get_all_v().values(), key=lambda n: n.pos[1]).pos[1]

        # Run the Gui
        self.MainRun()

    def update(self, pokemon, agents, points, mc, timer):
        self.pokemon = pokemon
        self.agents = agents
        self.timer = timer
        self.mc = mc
        self.points = points

    def my_scale(self, data, x=False, y=False):
        """For now i will leave it here check if it really is needed"""
        if x:
            return scale(data, self.margin, self.screen.get_width() - self.margin, self.min_x, self.max_x)
        if y:
            return scale(data, self.margin + self.upperMargin, self.screen.get_height() - self.margin, self.min_y,
                         self.max_y)

    def MainRun(self):
        """This is the main loop of the pygame, 60 ticks"""
        # variables
        self.margin = 50
        self.upperMargin = self.screen.get_height() / 8

        # Colors
        screenColor = (255, 255, 255)  # white
        NodeColor = (0, 48, 142)  # #00308E
        NodeIdColor = (255, 255, 255)  # white
        edgeColor = (120, 81, 185)  # #7851B9
        PokemonColor = (0, 255, 255)
        AgentColor = (122, 61, 23)
        AgentIdColor = (0, 0, 0)
        marginColor = (0, 0, 0)
        ButtonTitleColor = (0, 0, 0)
        ButtonColor = (0, 48, 142)

        # Parameters
        NodeRadius = 15
        PokemonNodeRadius = 15
        AgentsNodeRadius = 10
        edgeWidth = 1

        # Upper Margin
        stop = StopButton(80, 100, ButtonTitleColor)

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
                pygame.draw.aaline(self.screen, pygame.Color(marginColor), (0, self.upperMargin),
                                   (self.screen.get_width(), self.upperMargin), 1)

                # Render the Button
                stop.render(self.screen, ButtonColor, (0, 0), (100, 80))  # TODO Change the placement

                # Timer
                id_srf = FONT.render("Time:", True, pygame.Color(0, 0, 0))
                self.screen.blit(id_srf, id_srf.get_rect(center=(100, 10)))

                # Move Counter
                id_srf = FONT.render("Moves:", True, pygame.Color(0, 0, 0))
                self.screen.blit(id_srf, id_srf.get_rect(center=(100, 20)))

                # Point Counter
                id_srf = FONT.render("Points:", True, pygame.Color(0, 0, 0))
                self.screen.blit(id_srf, id_srf.get_rect(center=(100, 30)))


                # draw Nodes
                self.drawNodes(NodeColor, NodeIdColor, NodeRadius)

                # draw Edges
                self.drawEdges(edgeColor, edgeWidth)

                # draw Pokemon
                self.drawPokemon(PokemonColor, PokemonNodeRadius)

                # draw Agents
                self.drawAgent(AgentColor, AgentIdColor, AgentsNodeRadius)

                # update screen changes
                pygame.display.update()

                # refresh rate
                clock.tick(60)

    def drawNodes(self, NodeColor, NodeIdColor, NodeRadius):
        for v in self.graph.get_all_v().values():
            # Determine the Coordinates
            x = self.my_scale(v.pos[0], True, False)
            y = self.my_scale(v.pos[1], False, True)
            # Draw the node
            pygame.gfxdraw.aacircle(self.screen, int(x), int(y), NodeRadius, pygame.Color(NodeColor))
            pygame.gfxdraw.filled_circle(self.screen, int(x), int(y), NodeRadius, pygame.Color(NodeColor))
            # Write the Id
            id_srf = FONT.render(str(v.Id), True, pygame.Color(NodeIdColor))
            self.screen.blit(id_srf, id_srf.get_rect(center=(x, y)))

    def drawEdges(self, edgeColor, edgeWidth):
        for src in self.graph.get_all_v().values():
            for dest_id in self.graph.all_out_edges_of_node(src.Id):
                src_x = self.my_scale(src.pos[0], True, False)
                src_y = self.my_scale(src.pos[1], False, True)
                dest_x = self.my_scale(self.graph.getNode(dest_id).pos[0], True, False)
                dest_y = self.my_scale(self.graph.getNode(dest_id).pos[1], False, True)
                pygame.draw.aaline(self.screen, pygame.Color(edgeColor), (src_x, src_y), (dest_x, dest_y), edgeWidth)

    def drawPokemon(self, PokemonColor,
                    PokemonNodeRadius):  # TODO we could add the pictures instead of nodes of different colors
        for pok in self.pokemon:
            x = self.my_scale(pok.pos[0], True, False)
            y = self.my_scale(pok.pos[1], False, True)
            pygame.gfxdraw.aacircle(self.screen, int(x), int(y), PokemonNodeRadius, pygame.Color(PokemonColor))
            pygame.gfxdraw.filled_circle(self.screen, int(x), int(y), PokemonNodeRadius, pygame.Color(PokemonColor))

    def drawAgent(self, AgentColor, AgentIdColor,
                  AgentsNodeRadius):  # TODO we could add the pictures instead of nodes of different colors
        for agent in self.agents:
            x = self.my_scale(agent.pos[0], True, False)
            y = self.my_scale(agent.pos[1], False, True)
            pygame.gfxdraw.aacircle(self.screen, int(x), int(y), AgentsNodeRadius, pygame.Color(AgentColor))
            pygame.gfxdraw.filled_circle(self.screen, int(x), int(y), AgentsNodeRadius, pygame.Color(AgentColor))
            # Write the Id
            id_srf = FONT.render(str(agent.Id), True, pygame.Color(AgentIdColor))
            self.screen.blit(id_srf, id_srf.get_rect(center=(x, y)))


class StopButton:
    """This Class Represent the Stop Button"""

    def __init__(self, height, width, titleColor):
        self.height = height
        self.width = width
        self.rect = pygame.Rect((0, 0), (width, height))
        self.title_srf = FONT.render("STOP", True, pygame.Color(titleColor))

    def render(self, surface, buttonColor, pos, newSize):
        """Render the Button on the screen"""
        self.rect.update(self.rect.left, self.rect.top, newSize[0], newSize[1])
        self.rect.topleft = pos
        pygame.draw.rect(surface, buttonColor, self.rect)
        surface.blit(self.title_srf, self.title_srf.get_rect(center=self.rect.center))

    def check(self, click):
        """Check if the user clicked on the Button"""
        if self.rect.collidepoint(*click):
            return True  # TODO check how to return a message to the Controller, or how to actually run the function


if __name__ == '__main__':
    algo = GraphAlgo()
    algo.load_from_json("data/A3")
    test = Gui(algo.get_graph(), WIDTH, HEIGHT, 120)
