import pygame
from network import Network
import random
pygame.font.init()

width = 700
height = 700
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

class Button:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 150
        self.height = 100

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render(self.text, 1, (255,255,255))
        win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2) - round(text.get_height()/2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False

def redrawWindow(win, game, p):
    win.fill((255,255,255))

    if not(game.connected()):
        font = pygame.font.SysFont("comicsans", 50)
        text = font.render("You're Player 1, Waiting...", 1, (255,213,0))
        win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
    else:
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Player 1", 1, (255,0,0))
        win.blit(text, (35, 200))

        text = font.render("Player 2", 1, (0, 0, 204))
        win.blit(text, (380, 200))

        point1 = str(game.get_player_points(0))
        point2 = str(game.get_player_points(1))
        if game.bothPoint():
            text1 = font.render(point1, 1, (255,0,0))
            text2 = font.render(point2, 1, (0, 0, 204))
        else:
            if game.p1point and p == 0:
                text1 = font.render(point1, 1, (255,0,0))
            else:
                text1 = font.render("Waiting...", 1, (255, 0, 0))

            if game.p2point and p == 1:
               text2 = font.render(point2, 1, (0,0,204))
            else:
                text2 = font.render("Waiting...", 1, (0, 0, 204))

        if p == 1:
            win.blit(text2, (400, 350))
            win.blit(text1, (35, 350))
        else:
            win.blit(text1, (35, 350))
            win.blit(text2, (400, 350))

        for btn in btns:
            btn.draw(win)

    pygame.display.update()

buttons = [Button("Add", 250, 500, (0,255,34))]
def main():
    point = 0
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.getP())
    print("You are player", player)

    while run:
        clock.tick(60)
        try:
            game = n.send("get")
        except:
            run = False
            print("Couldn't get game")
            break

        if int(game.bothPoint()) >= 21:
            
            redrawWindow(win, game, player)
            pygame.time.delay(500)
            try:
                game = n.send("reset")
                point = 0
            except:
                run = False
                print("Couldn't get game")
                break

            font = pygame.font.SysFont("comicsans", 90)
            if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
                text = font.render("You Won!", 1, (255,255,255), (0, 255, 0))
            elif game.winner() == -1:
                text = font.render("Tie Game!", 1, (255,255,255), (255, 255, 0))
            else:
                text = font.render("You Lost...", 1, (255, 255, 255), (255,0,0))

            win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(2000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    if btn.click(pos) and game.connected():
                        if player == 0:
                            if game.p1point != 21 and game.p1point < 21:
                                point = point + random.randint(0,9)
                                n.send(str(point))

                        else:
                            if game.p2point != 21 and game.p2point < 21:
                                point = point + random.randint(0,9)
                                n.send(str(point))

        redrawWindow(win, game, player)

def menu():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.fill((128, 128, 128))
        font = pygame.font.SysFont("comicsans", 50)
        text = font.render("Play!", 1, (255,255,255))
        win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    main()

while True:
    menu()
