#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 09:59:45 2024

@author: helenenossum
"""
import animasjon_forhold as bib
import matplotlib.pyplot as plt


# Konstanter
LIMIT_MIN = 15
LIMIT_MAX = 80
LIMIT_MIDDLE = 40
DIVISIBLE = 5
GREEN = "#008000"
BLUE = "#0000FF"


# Funksjon som plotter søylediagram
def plot_bar(atomgroups, n_start, n_end):
    group_number = {}
    
    # Lager midlertidig liste, med atomgruppene fra og med atomnummer start gitt til go med atomnummer slutt
    used_atomgroups = atomgroups[n_start-1:n_end]
    
    # Teller hvor mange av hver gruppe det er
    for group in used_atomgroups:
        if group not in group_number:
            group_number[group] = 1
        else:
            group_number[group] += 1

    groups = list(group_number.keys())
    number_of = list(group_number.values())  
    used_number_of = []

    # Dersom det er mange y-verdier, vil kun de som er delelig på 5 vises
    if n_end-n_start > LIMIT_MIDDLE:        
        for i in range(0, max(number_of)+1, 5):
            used_number_of.append(i)
        plt.yticks(used_number_of)
        
        # Lettere å se ved store tall
        plt.minorticks_on()

    # Dersom det ikke er så mange y-verdier (men må bli heltall)
    else:
        for i in range(0, max(number_of)+1):
            used_number_of.append(i)
        plt.yticks(used_number_of)
        
    # Plotter søylediagrammet
    plt.bar(groups, number_of)

    plt.xlabel("Atomgroups", color="#550000")
    plt.ylabel("How many of each group")
    
    # Får verdiene på x-aksen til å se fine ut
    plt.gcf().autofmt_xdate() 

    # Vil kun at det skal være vannrette-linjer i rutenettet
    plt.grid(axis="y")
    plt.title(f"How many elements of each group: from atomnumber {n_start} to {n_end}", color="#550000")
    plt.show()
 
    
 
# Funksjon til å plotte graf 
def plot_line(the_list, mark, the_color, text, n_start, n_end, atomnumbers, atoms, unit):
    # Sjekker hvor mange x-verdier som vises
    if n_end-n_start > LIMIT_MIN:
        divisible = DIVISIBLE
        
        if n_end-n_start > LIMIT_MAX:
            divisible = DIVISIBLE*2
            mark = ""
            
        # Lager liste av alle tall i delelig-gangen, inkludert start- og slutt-verdiene ut ifra lambdaen (liten funksjon)
        plt.xticks(list(filter(lambda x: x % divisible == 0 or x == n_start or x == n_end, range(n_start,n_end+1))))
        
        # X-akse-tekst
        x_text = "Atomnumber"
    
    else:
        # Hvis det er få grunnstoffer:
        x_text = "Elements"
        # Gjør om lista
        atomnumbers = atoms
    
    # Plotter graf og endring (avhenger av hvilken sammenheng som skal plottes)
    plt.plot(atomnumbers[
        (n_start-1):n_end], 
        the_list[(n_start-1):n_end], 
        marker=mark, 
        color=the_color)
    
    # Får verdiene på x-aksen til å se fine ut
    plt.gcf().autofmt_xdate()   
     
    # Gir grafen en tittel, y-aksen og x-aksen et navn
    plt.title(f"The elements and their {text}", color="#550000")
    plt.ylabel(f"{text.capitalize()} ({unit})", color=the_color)
    plt.xlabel(x_text, color="#550000")
    
    # Lager rutenett
    plt.grid()
    plt.show()
    
    
# While-løkka kjører til gyldige input-verdier er gitt
gyldig = False
while not gyldig:
    try:
        # Skal få inn to heltall av bruker
        n_start = int(input("Skriv et heltall mellom 1 og 118 (det tilsvarer atomnumrene): "))
        n_end = int(input("Skriv et annet heltall mellom 1 og 118 (det tilsvarer atomnumrene): "))
        
        # Sjekker om heltallene er mellom 1 og 118, og at de ikke er like
        if 0 < n_start <= 118 and 0 < n_end <= 118 and n_start != n_end:
            gyldig = True
            if n_start > n_end:
                # Dersom bruker har skrevet inn i feil rekkefølge
                n_start, n_end = n_end, n_start 
             
            print()
            print("De ulike sammenhengene du kan velge mellom:")
            print(" - Atommasse (skriv 1)")
            print(" - Atomradius (skriv 2)")
            print(" - Atomgrupper (skriv 3)")
            print(" - Animasjon av atomene i forhold til hverandre (skriv 4)")
            print(" - Se informasjon om de 2 atomene (skriv 5)")
            connection = int(input("Hvilken vil du se? "))
            print()
            
            if connection == 1:
                plot_line(bib.atommass, "x", GREEN, "mass", n_start, n_end, bib.atomnumbers, bib.atomnames, "u")
            elif connection == 2:  
                plot_line(bib.atomradius, "D", BLUE, "radius", n_start, n_end, bib.atomnumbers, bib.atomnames, "pm")
            elif connection == 3:  
                plot_bar(bib.atomgroups, n_start, n_end)
            elif connection == 4:
                bib.animation(n_start, n_end)
            elif connection == 5:
                name_1 = bib.number_name[n_start]
                bib.name_with_class[name_1].showInfo()
                
                print()
                name_2 = bib.number_name[n_end]
                bib.name_with_class[name_2].showInfo()

        else:   
            print()
            print("Skriv inn to ulike heltall fra og med 1 til og med 118. Prøv igjen. ")
    # Dersom bruker har skrevet noe annet enn et heltall
    except ValueError:
        print("Du må skrive inn et heltall! Det kan også hende du har oppgitt et atom med ukjent radius. Prøv igjen. ")