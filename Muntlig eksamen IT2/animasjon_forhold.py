import csv
import pygame as pg

# Konstanter
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
FPS = 120
HUNDRED_PERCENT = 100

#Initialiserer/starter pygame
pg.init()

# Oppretter et vindu der vi skal "tegne" innholdet vårt
SCREEN_WIDTH = 500
SCREEN_HEIGHT  = 400
screen = pg.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

# Angir hvilken skrifttype og tekststørrelse vi vil bruke på tekst
font = pg.font.SysFont("Arial", 24)

# Henter fil
filename = "data_grunnstoffer.csv"

# Klasse for atom-objekter
class Atom:
    """
    Klasse for å lage atom-objekter
    
    Parametere:
        number(int): the atomnumber
        name(str): the atoms name
        mass(float): the atoms mass
        radius(float): the atoms radius
        group(str): which elementgroup
    """
    def __init__(self, number: int, name: str, mass: float, radius: float, group: str):
        self.number = number
        self.name = name
        self.mass = mass
        self.radius = radius
        self.group = group
    
    def showInfo(self):
        print(f"{self.name}: ")
        print(f" - Atomnumber: {self.number}")
        print(f" - Mass: {self.mass} u")
        print(F" - Radius: {self.radius} pm")
        print(f" - {self.name} is a(n) {self.group}.")

name_with_class = {}

# Henter csv-filen
with open(filename, "r") as file:
    content = csv.reader(file, delimiter=",")
    
    # Deklarerer variabelen overskrift og hopper sÃ¥ over den
    title = next(content)
    
    # Legger til dataene for hver rad inn i riktig liste
    for row in content:
        # Får riktig masse
        mass = row[3].strip()
        if mass[-1] == ")":
            mass = mass[:-3]
        elif mass[-1] == "]":
            mass = mass[1:-1]
            
        # Sjekker om det er oppgitt radius
        radius = row[7]
        if len(row[7]) == 0:
            radius = "unknown"
        
        # Lager atom_objekt for de ulike atomene
        atom = Atom(int(row[0]), row[2].strip(), round(float(mass), 2), radius, row[18])
        
        # Lar navnet være nøkkel og atomobjektet være verdi i ordboken
        name_with_class[row[2].strip()] = atom

# Lager tomme lsiter til å fylles opp
atomnames = []
atomnumbers = []
atommass = []
atomradius = []
atomgroups = []
    
# Fyller listene med riktig informasjon
for value in name_with_class.values():
    atomnames.append(value.name)
    atomnumbers.append(value.number)
    atommass.append(value.mass)
    if value.radius == "unknown":
        atomradius.append(0)
    else:
        atomradius.append(int(value.radius))
    atomgroups.append(value.group)
    
number_name = {}

# Fyller ordboken med atomnummeret som tilsvarer atomnavnet
for i in range(len(atomnumbers)):
    number_name[i+1] = atomnames[i]

# Funksjon for animering av 2 atomer - som sirkler
def animation(number_1, number_2):
    # Finner navnet på grunnstoffet og radiusen til grunnstoffet
    for key, value in name_with_class.items():
        if key == number_name[number_1]:
            radius_1 = value.radius
            name_1 = key

        elif key == number_name[number_2]:
            radius_2 = value.radius
            name_2 = key
    
    # Dersom begge radiusene er oppgitt, så kan de animeres
    if radius_1 != "unknown" and radius_2 != "unknown":
        radius_1 = int(radius_1)
        radius_2 = int(radius_2)
            
        # Sjekker hvem av de som er størst - da den minste vil tilpasse seg den største
        if radius_1 < radius_2:
            radius_1 = (radius_1/radius_2)*HUNDRED_PERCENT
            radius_2 = HUNDRED_PERCENT
                
            # Tegner de to atomene som sirkler
            x_1 = SCREEN_WIDTH/100 + radius_2
            x_2 = SCREEN_WIDTH - SCREEN_WIDTH/100 - radius_2 - 50
        else:
            radius_2 = (radius_2/radius_1)*HUNDRED_PERCENT
            radius_1 = HUNDRED_PERCENT
                
            # Tegner de to atomene som sirkler
            x_1 = SCREEN_WIDTH/100 + radius_1
            x_2 = SCREEN_WIDTH - SCREEN_WIDTH/100 - radius_1 - 50

        clock = pg.time.Clock()

        # Gjenta helt til brukeren lukker vinduet
        run = True
        while run:
            clock.tick(FPS)

            # Sjekker om brukeren har lukket vinduet
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False

            # Farger bakgrunnen hvit
            screen.fill(WHITE)
            
            pg.draw.circle(screen, BLUE, (x_1, SCREEN_HEIGHT/2 + 50), radius_1)
            pg.draw.circle(screen, RED, (x_2, SCREEN_HEIGHT/2 + 50), radius_2)
                
            # Lager en tekst i form av et bilde og legger til bildet i vinduet
            img_1 = font.render(f"{name_1}", True, (50, 50, 50))
            screen.blit(img_1, (x_1-radius_1, 100))
            img_2 = font.render(f"{name_2}", True, (50, 50, 50))
            screen.blit(img_2, (x_2-radius_2/3, 100))
            

            # Oppdaterer alt innholdet i vinduet
            pg.display.flip()
                
            
        pg.quit()
    else:
        print("Du har oppgitt et atom med ukjent radius")