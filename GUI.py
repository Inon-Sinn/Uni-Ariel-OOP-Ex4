from pygame import gfxdraw
import pygame

from Model.GraphAlgo import GraphAlgo
from Model.classes.pokemons import Pokemon

pygame.init()
pygame.font.init()
clock = pygame.time.Clock()

# Fonts
FONT = pygame.font.SysFont('Arial', 15, bold=True)
TITLE_FONT = pygame.font.SysFont("Arial", 15, bold=True)

WIDTH, HEIGHT = 900, 570


def scale(data, min_screen, max_screen, min_data, max_data):
    """
    get the scaled data with proportions min_data, max_data
    relative to min and max screen dimensions
    """
    return ((data - min_data) / (max_data - min_data)) * (max_screen - min_screen) + min_screen


def draw_rect_outline(surface, rect, color, width=1):
    """An auxiliary function that draw the outline of a Rectangle"""
    x, y, w, h = rect
    width = max(width, 1)  # Draw at least one rect.
    width = min(min(width, w // 2), h // 2)  # Don't overdraw.
    # This draws several smaller outlines inside the first outline.
    for i in range(width):
        pygame.gfxdraw.rectangle(surface, (x + i, y + i, w - i * 2, h - i * 2), color)


class Gui:
    """This class is Implements The View, The GUI"""

    def __init__(self, graph, width: int, height: int, runtime: float, pokemon=None, agents=None, debug=False):

        # Pokemon Game Variables
        if agents is None:
            agents = []
        if pokemon is None:
            pokemon = []
        self.agents = agents
        self.pokemon = pokemon
        self.timer = runtime
        self.points = 0
        self.mc = 0
        self.graph = graph
        self.debug = debug
        self.running = True

        # screen variables
        self.screen = pygame.display.set_mode((width, height), depth=32, flags=pygame.constants.RESIZABLE)
        self.margin = self.screen.get_height() / 10
        self.upperMargin = self.screen.get_height() / 8

        # Coordinates used for Scaling
        self.min_x = min(self.graph.get_all_v().values(), key=lambda n: n.pos[0]).pos[0]
        self.max_x = max(self.graph.get_all_v().values(), key=lambda n: n.pos[0]).pos[0]
        self.min_y = min(self.graph.get_all_v().values(), key=lambda n: n.pos[1]).pos[1]
        self.max_y = max(self.graph.get_all_v().values(), key=lambda n: n.pos[1]).pos[1]

        # Run the Gui
        self.MainRun()

    def update(self, pokemon, agents, points, mc, timer):
        """Gets an Update from the Controller and Tells him the status"""
        if self.running is not False:
            self.pokemon = pokemon
            self.agents = agents
            self.timer = timer
            self.mc = mc
            self.points = points
        return self.running

    def my_scale(self, data, x=False, y=False):
        """An auxiliary function to calculate Coordinates on the screen given their position"""
        if x:
            return scale(data, self.margin, self.screen.get_width() - self.margin, self.min_x, self.max_x)
        if y:
            return scale(data, self.margin, self.screen.get_height() - self.margin, self.min_y, self.max_y)

    def MainRun(self):
        """This is the main loop of the pygame, 60 ticks"""

        # variables
        background = pygame.image.load("Images/pokemon_Map.jpg")
        BoxWidth = 8
        hd = 10  # Boxes Height divider
        bHdP = 4  # boxed height divider portion

        # Colors
        screenColor = (255, 255, 255)  # white
        NodeColor = (0, 48, 142)  # #00308E
        NodeIdColor = (255, 255, 255)  # white
        edgeColor = (120, 81, 185)  # #7851B9
        AgentColor = (0, 255, 255)
        AgentIdColor = (0, 0, 0)
        ButtonTitleColor = (255, 255, 255)
        ButtonColor = (0, 48, 142)
        boxOutlineColor = (0, 0, 0)
        TextColor = (255, 255, 255)
        NodeOutlineColor = (0, 0, 0)

        # Parameters
        NodeRadius = 15
        AgentsNodeRadius = 10
        edgeWidth = 1
        BoxOutlineWidth = 2

        # Upper Margin
        stop = StopButton(80, 100, ButtonTitleColor)

        while True:
            for gui_event in pygame.event.get():
                if gui_event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)

                if gui_event.type == pygame.MOUSEBUTTONUP:
                    click = pygame.mouse.get_pos()
                    if stop.check(click):
                        self.running = False

                # refresh surface
                self.screen.fill(pygame.Color(screenColor))
                background = pygame.transform.scale(background, (self.screen.get_width(), self.screen.get_height()))
                rect = background.get_rect()
                self.screen.blit(background, rect)
                self.margin = max(self.screen.get_height() / 10, 50)

                # Render the Button
                stop.render(self.screen, ButtonColor, (0, self.margin / hd),
                            (self.screen.get_width() * (1 / BoxWidth), self.margin * (bHdP / hd)))
                draw_rect_outline(self.screen, stop.rect, boxOutlineColor, BoxOutlineWidth)

                # Timer
                pos = (self.screen.get_width() * (1 / BoxWidth) + 1, self.margin / hd)
                text = " Time: {}s ".format(self.timer)
                self.drawTextBox(pos, self.margin * (bHdP / hd), self.screen.get_width() * (1 / BoxWidth), text,
                                 TextColor, ButtonColor, boxOutlineColor, BoxOutlineWidth)

                # Move Counter
                pos = (self.screen.get_width() * (2 / BoxWidth) + 2, self.margin / hd)
                text = " Moves: {} ".format(self.mc)
                self.drawTextBox(pos, self.margin * (bHdP / hd), self.screen.get_width() * (1 / BoxWidth), text,
                                 TextColor, ButtonColor, boxOutlineColor, BoxOutlineWidth)

                # Point Counter
                pos = (self.screen.get_width() * (3 / BoxWidth) + 3, self.margin / hd)
                text = " Points: {} ".format(self.points)
                self.drawTextBox(pos, self.margin * (bHdP / hd), self.screen.get_width() * (1 / BoxWidth), text,
                                 TextColor, ButtonColor, boxOutlineColor, BoxOutlineWidth)

                # draw Edges
                self.drawEdges(edgeColor, edgeWidth)

                # draw Nodes
                self.drawNodes(NodeColor, NodeIdColor, NodeRadius, NodeOutlineColor)

                # draw Pokemon
                PokemonNodeRadius = 0.055 * self.screen.get_height()
                self.drawPokemon(PokemonNodeRadius)

                # draw Agents
                self.drawAgent(AgentColor, AgentIdColor, AgentsNodeRadius)

                # update screen changes
                pygame.display.update()

                # refresh rate
                clock.tick(60)

    def drawTextBox(self, pos, height, width, text, TextColor, boxColor, boxOutlineColor, BoxOutlineWidth=1):
        # Make an Rectangle of the right size adn draw the the Text Box
        rect = pygame.Rect((0, 0), (width, height))
        rect.topleft = pos
        pygame.draw.rect(self.screen, boxColor, rect)
        # Add the Text to Surface
        id_srf = FONT.render(text, True, pygame.Color(TextColor))
        self.screen.blit(id_srf, id_srf.get_rect(center=rect.center))
        draw_rect_outline(self.screen, rect, boxOutlineColor, BoxOutlineWidth)

    def drawNodes(self, NodeColor, NodeIdColor, NodeRadius, NodeOutlineColor):
        """Draws the Nodes on the Screen"""
        for v in self.graph.get_all_v().values():
            # Determine the Coordinates
            x = self.my_scale(v.pos[0], True, False)
            y = self.my_scale(v.pos[1], False, True)
            # Draw the node
            pygame.gfxdraw.aacircle(self.screen, int(x), int(y), NodeRadius, pygame.Color(NodeColor))
            pygame.gfxdraw.filled_circle(self.screen, int(x), int(y), NodeRadius, pygame.Color(NodeColor))
            pygame.draw.circle(self.screen, pygame.Color(NodeOutlineColor), (int(x), int(y)), NodeRadius,
                               1)  # Draws an outline
            # Write the Id
            id_srf = FONT.render(str(v.Id), True, pygame.Color(NodeIdColor))
            self.screen.blit(id_srf, id_srf.get_rect(center=(x, y)))

    def drawEdges(self, edgeColor, edgeWidth):
        """Draws the Edges on the Screen"""
        for src in self.graph.get_all_v().values():
            for dest_id in self.graph.all_out_edges_of_node(src.Id):
                src_x = self.my_scale(src.pos[0], True, False)
                src_y = self.my_scale(src.pos[1], False, True)
                dest_x = self.my_scale(self.graph.getNode(dest_id).pos[0], True, False)
                dest_y = self.my_scale(self.graph.getNode(dest_id).pos[1], False, True)
                pygame.draw.aaline(self.screen, pygame.Color(edgeColor), (src_x, src_y), (dest_x, dest_y), edgeWidth)

    def drawPokemon(self, PokemonNodeRadius):
        """Draws the pokemon on the Screen,
        The pokemon will look left if src < dest => type > 0,
        The pokemon will look right if dest < src => type < 0.
        in the direction of the src (not really)"""
        for pok in self.pokemon:
            x = self.my_scale(pok.pos[0], True, False)
            y = self.my_scale(pok.pos[1], False, True)
            # Draw the pokemon
            if 0 < pok.value < 15:
                filename = "Images/pokemon{}.png".format(pok.value)
            else:
                filename = "Images/pokemon3.png"
            pic = pygame.image.load(filename)
            if pok.type == -1:
                pic = pygame.transform.flip(pic, True, False)
            pic = pygame.transform.scale(pic, (PokemonNodeRadius * 2, PokemonNodeRadius * 2))
            rect = pic.get_rect()
            rect.center = (x, y)
            self.screen.blit(pic, rect)

    def drawAgent(self, AgentColor, AgentIdColor, AgentsNodeRadius):
        # TODO maybe print the value of the agents in Debug mode
        """Draw the Agents on the Screen"""
        for agent in self.agents:
            x = self.my_scale(agent.pos[0], True, False)
            y = self.my_scale(agent.pos[1], False, True)
            if self.debug:
                pygame.gfxdraw.aacircle(self.screen, int(x), int(y), AgentsNodeRadius, pygame.Color(AgentColor))
                pygame.gfxdraw.filled_circle(self.screen, int(x), int(y), AgentsNodeRadius, pygame.Color(AgentColor))
                # Write the Id
                id_srf = FONT.render(str(agent.id), True, pygame.Color(AgentIdColor))
                self.screen.blit(id_srf, id_srf.get_rect(center=(x, y)))
            else:
                print("Coming Soon")


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
        return False


class fakeAgent:
    def __init__(self, Id, pos, value=0):
        self.id = Id
        self.value = value
        self.pos = pos


if __name__ == '__main__':
    algo = GraphAlgo()
    algo.load_from_json("data/A3")

    pos1 = (algo.get_graph().getNode(6).pos[0], algo.get_graph().getNode(1).pos[1])
    pokemon1 = Pokemon(16, -1, pos1)
    pos2 = (algo.get_graph().getNode(2).pos[0], algo.get_graph().getNode(6).pos[1])
    pokemon2 = Pokemon(1, 1, pos2)
    pokemon = [pokemon1, pokemon2]

    agent1 = fakeAgent(0, (algo.get_graph().getNode(4).pos[0], algo.get_graph().getNode(4).pos[1]))
    agent2 = fakeAgent(1, (algo.get_graph().getNode(8).pos[0], algo.get_graph().getNode(8).pos[1]))
    agents = [agent1, agent2]
    test = Gui(algo.get_graph(), WIDTH, HEIGHT, 120, pokemon, agents, debug=False)
