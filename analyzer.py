import csv
inputFile = open("VW.csv", "r", encoding="UTF-8") # TODO: Pas VW.csv aan naar jouw bestand, en verwijder deze comment
reader = csv.DictReader(inputFile, delimiter=";") # onze csv heeft ; en dat moeten we aangeven
data = list(reader)

running = True
while running:
    print("Menu") # TODO: Maak hier een mooi menu van
    keuze = input("Keuze: ")

    # TODO: Implementeer de logica voor de keuzes
    if keuze == "1" or keuze == "w":
        print("Keuze 1")
    
    if keuze == "2" or keuze == "w":
        print("Keuze 2")

    if keuze == "3" or keuze == "w":
        print("Keuze 3")
    
    if keuze == "4" or keuze == "w":
        print("Keuze 4")

    if keuze == "w":
        print("Schrijf naar bestand")
    
    if keuze == "x":
        running = False