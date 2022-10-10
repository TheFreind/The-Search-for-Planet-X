# Spend time triggers Movesky
# Movesky moves sky to #4, which triggers a Theory Phase
# Theory phase triggers peerreview
# Peerreview triggers Spendtime
# Spend time will trigger Movesky
# 


######################
## GLOBAL VARIABLES ##
######################

import random, time

Space = {}
visibleSky = []
theoryScape = []
research = []
planetXconference = []

# Players in the game. Contains relevant information about each player. 
# Key - Player "Color": [ Location, Queue order, [Theories left: C, A, D, G], [Category Researched],
#                        , [Planet X conferences attended], Research Action Timer, Target Tokens Remaining, Points ]
players = {
    "Blue":   [1, 1, [2, 4, 1, 2], [False,False,False,False,False,False],[], 2, 2, 0 ],
    "Red":    [1, 2, [2, 4, 1, 2], [False,False,False,False,False,False],[], 2, 2, 0 ],
    "Yellow": [1, 3, [2, 4, 1, 2], [False,False,False,False,False,False],[], 2, 2, 0 ],
    "Purple": [1, 4, [2, 4, 1, 2], [False,False,False,False,False,False],[], 2, 2, 0 ]
    }

# Each player has unique art for added aesthetic.
# Code needs to be reinforced to allow name changing. For now, only the base colors are allowed.
art = {"Blue":"&-%-&" , "Red":"#^*^#" , "Yellow":"/\_/\\" , "Purple":"[:|:]"}

###############################
##### PRE-GAME FUNCTIONS ######
###############################

# All player commands and inputs must not cause errors. It's also helpful to display an appropriate error message to the user.
# This is a catch-all function that houses all the different validations under one section.
# - inputVar - the input variable that is being checked.
# - task - a string key that tells the function which validation to initiate.
def inputValidation(inputVar, task):

    if task == "gameMode":
        while ( ("Standard" not in inputVar) and ("standard" not in inputVar) and
            ("Expert" not in inputVar) and ("expert" not in inputVar) ):
            inputVar = input("Typo detected. Please re-enter 'Standard' or 'Expert':\n")
            
        if inputVar == "standard":
            inputVar = "Standard"
        elif inputVar == "expert":
            inputVar = "Expert"

    elif task == "survey" or task == "guessSectorShadow" or task == "guessSectorFuture":
        while ( (inputVar != "Asteroid") and (inputVar != "A") and (inputVar != "a") and
                (inputVar != "Comet") and (inputVar != "C") and (inputVar != "c") and
                (inputVar != "Dwarf Planet") and (inputVar != "D") and (inputVar != "d") and
                (inputVar != "Gas Cloud") and (inputVar != "G") and (inputVar != "g") and
                (inputVar != "Empty") and (inputVar != "E") and (inputVar != "e") and
                (inputVar != "R") and (inputVar != "r") and (inputVar != "Return") ):
            inputVar = input("Typo detected. Please re-enter a valid celestial object to survey for:\n")

        if inputVar == "A" or inputVar == "a":
            inputVar = "Asteroid"
        elif inputVar == "C" or inputVar == "c":
            inputVar = "Comet"
        elif inputVar == "D" or inputVar == "d":
            inputVar = "Dwarf Planet"
        elif inputVar == "E" or inputVar == "e":
            inputVar = "Empty"
        elif inputVar == "G" or inputVar == "g":
            inputVar = "Gas Cloud"

    elif task == "surveyStart" or task == "surveyEnd" or task == "targetting":
        repeat = True
        while repeat == True:
            if inputVar.isdigit():
                if int(inputVar) not in visibleSky:
                    inputVar = input("Error! You may only select sectors in the current visibly sky. Re-try:\n")
                else:
                    repeat = False
                    inputVar = int(inputVar)

            elif inputVar == "Return" or inputVar == "R" or inputVar == "r":
                repeat = False
                
            else:
                inputVar = input("Error! That is not a number. Re-try:\n")

    elif task == "researching":
        while ( ("A" != inputVar) and ("a" != inputVar) and
                ("B" != inputVar) and ("b" != inputVar) and
                ("C" != inputVar) and ("c" != inputVar) and
                ("D" != inputVar) and ("d" != inputVar) and
                ("F" != inputVar) and ("f" != inputVar) and
                ("G" != inputVar) and ("g" != inputVar) and
                (inputVar != "R") and (inputVar != "r") and (inputVar != "Return") ):
            inputVar = input("Error! That is not a valid category. Re-try:\n")

        if inputVar == "a":
            inputVar = "A"
        elif inputVar == "b":
            inputVar = "B"
        elif inputVar == "c":
            inputVar = "C"
        elif inputVar == "d":
            inputVar = "D"
        elif inputVar == "f":
            inputVar = "F"
        elif inputVar == "g":
            inputVar = "G"
        
    elif task == "guessSectorX":
        repeat = True
        while repeat == True:
            if inputVar.isdigit():
                if int(inputVar) not in Space:
                    inputVar = input("Error! That sector does not exist. Re-try:\n")
                else:
                    repeat = False
                    inputVar = int(inputVar)

            elif inputVar == "Return" or inputVar == "R" or inputVar == "r":
                if len(PlanetXFound) == 0:
                    repeat = False
                else:
                    inputVar = input("Error! You may not change your mind for your final guess. Please choose a sector:\n")
                
            else:
                inputVar = input("Error! That is not a number. Re-try:\n")

    elif task == "chooseFinalAction":
        while ( ("T" != inputVar) and ("t" != inputVar) and ("Theory" != inputVar) and
                ("G" != inputVar) and ("g" != inputVar) and ("Guess" != inputVar) ):
            inputVar = input("Error! That is not a valid final action. Re-try:\nNOTE: YOU MAY NOT CHANGE YOUR MIND. CHOOSE WISELY:\n")

    elif task == "chooseTheory":
        while ( (inputVar != "Asteroid") and (inputVar != "A") and (inputVar != "a") and
                (inputVar != "Comet") and (inputVar != "C") and (inputVar != "c") and
                (inputVar != "Dwarf Planet") and (inputVar != "D") and (inputVar != "d") and
                (inputVar != "Gas Cloud") and (inputVar != "G") and (inputVar != "g") ):

            if (inputVar == "S" or inputVar == "s" or inputVar == "Skip") and len(PlanetXFound) > 0:
                inputVar = input("ERROR. May not skip submitting a theory in the end game. Try again:\n")
                
            else:  
                inputVar = input("Typo detected. Please re-enter a valid celestial object to theorize:\n")

        if inputVar == "A" or inputVar == "a":
            inputVar = "Asteroid"
        elif inputVar == "C" or inputVar == "c":
            inputVar = "Comet"
        elif inputVar == "D" or inputVar == "d":
            inputVar = "Dwarf Planet"
        elif inputVar == "G" or inputVar == "g":
            inputVar = "Gas Cloud"
        elif inputVar == "S" and inputVar == "s":
            inputVar = "Skip"


    return inputVar

# Some objects depend on being adjacent or not adjacent to other objects. Hence, adjacency is needed.
# This function finds the immediate sector to the left and right of a selected sector.
# - dice - The number of the selected sector. I call it dice because adjacency is usually used in the RNG of setup.
def adjacency(dice): 
    global shadow, future, opposite
    
    if dice == 1:    # Sector 12 is considered to be adjacent to 1 in a ring.
        if mode == "Standard":
            shadow = 12
        elif mode == "Expert":
            shadow = 18
        future = 2

    elif dice == 12 and (mode == "Standard"): # See above, but for sector 1
        shadow = 11
        future = 1

    elif dice == 18 and (mode == "Expert"):
        shadow = 17
        future = 1

    else:            # Shadow - one sector behind, future - one sector forward
        shadow = dice - 1
        future = dice + 1

                    # Opposite - The sector directly opposite the chosen one.
    if mode == "Standard":  # Either 6 or 9 spaces away.
        opposite = dice + 6
        if opposite > 12:
            opposite -= 12
    elif mode == "Expert":
        opposite = dice + 9
        if opposite > 18:
            opposite -= 18
    


# At setup, all celestial objects are randomly placed in a map.
# This function doublechecks if the necessary objects exist. Return a boolean to repeat verification or to save map.
def verify(): 
    Asteroids = 0
    Dwarf = 0
    GasClouds = 0
    Comets = 0
    Empties = 0
    planetX = 0
    for sector in Space: 
        
        if len(Space[sector]) == 0:
            Space[sector] = "Empty"
            Empties += 1
        elif Space[sector] == "Empty":
            Empties += 1
        elif Space[sector] == "Asteroid":
            Asteroids += 1
        elif Space[sector] == "Dwarf Planet":
            Dwarf += 1
        elif Space[sector] == "Gas Cloud":
            GasClouds += 1
        elif Space[sector] == "Comet":
            Comets += 1
        elif Space[sector] == "Planet X":
            planetX += 1
        
        print(str(sector), ":", Space[sector]) #

    #print("\nDE-BUGGING. CHECK IF ALL OBJECTS EXIST")
    #print("Asteroids:", Asteroids, "\nDwarf:", Dwarf, "\nGas Clouds:", GasClouds, "\nComets:", Comets, "\nEmpties:", Empties)

    if mode == "Standard":
        if Asteroids != 4 or Dwarf != 1 or GasClouds != 2 or Comets != 2 or Empties != 2 or planetX != 1:
            return False
        else:
            return True
        
    elif mode == "Expert":
        if Asteroids != 4 or Dwarf != 4 or GasClouds != 2 or Comets != 2 or Empties != 5 or planetX != 1:
            return False
        else:
            return True


# Create the game and the map.
def setUp():
    global possibleMap, Space, visibleSky, theoryScape

    if mode == "Standard":
        Space = { # 12 Sectors in Standard
                1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 
                7: [], 8: [], 9: [], 10: [], 11: [], 12: []
            }
        cometLocations = [2, 3, 5, 7, 11]
        visibleSky = [1, 2, 3, 4, 5, 6]
        theoryScape  = { 
                1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 
                7: [], 8: [], 9: [], 10: [], 11: [], 12: []
            }
        for color in players: # 1 Planet X conference
            players[color][4].append(False)
    
    elif mode == "Expert":
        Space = { # 18 Sectors in Standard
                1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 
                7: [], 8: [], 9: [], 10: [], 11: [], 12: [],
                13: [], 14: [], 15: [], 16: [], 17: [], 18: []
            }
        cometLocations = [2, 3, 5, 7, 11, 13, 17]
        visibleSky = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        theoryScape = {
                1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 
                7: [], 8: [], 9: [], 10: [], 11: [], 12: [],
                13: [], 14: [], 15: [], 16: [], 17: [], 18: []
            }
        for color in players: # Players get 4 Dwarf theories
            players[color][2][2] = 4
        for color in players: # 2 Planet X conference
            players[color][4].append(False)
            players[color][4].append(False)

# PLANET X #
    planetX = random.randint(1, len(Space) ) # By being first, X can be in the most random position.
    Space[planetX] = "Planet X"

# COMETS # 
    cometObjects = 0 
    while cometObjects < 2:
        cometIndex = random.randint(0, len(cometLocations)-1 ) # Roll random index from available spots
        comet = cometLocations[cometIndex]
        
        if len(Space[comet]) == 0:
            Space[comet] = "Comet"
            del cometLocations[cometIndex]
            cometObjects += 1

# DWARFS # 
    dwarfPlanetChecks = 0
    if mode == "Standard":
        dwarfPlanet = 0
        while dwarfPlanet < 1:
            dwarf = random.randint(1, len(Space) )
            
            if len(Space[dwarf]) == 0:
                adjacency(dwarf)
                if Space[shadow] != "Planet X" and Space[future] != "Planet X":
                    Space[dwarf] = "Dwarf Planet"
                    dwarfPlanet = 1
                else:
                    dwarfPlanetChecks += 1

                if dwarfPlanetChecks > 30:
                    break

    elif mode == "Expert":
        dwarfPlanetsPlaced = False
        while dwarfPlanetsPlaced == False:
            dwarf = random.randint(1, len(Space) )
            dwarfLocations = []
            dwarfPlanet = 0

            if dwarfPlanetChecks > 30:
                break

            dwarfEndBand = dwarf + 5 # 5 Sectors from 1st dwarf, a 2nd dwarf planet will be placed. Check if legal.
            if dwarfEndBand > 18:
                dwarfEndBand -= 18 # Do not exceed map size. Reset to 1 instead
                
            if len(Space[dwarf]) == 0 and len(Space[dwarfEndBand]) == 0:
                availableSpots = 0
                for sector in range(7): # Check if a band of 6 sectors can be formed, starting with dice roll 'dwarf'
                    dwarfTotal = dwarf + sector # Track how many sectors from the start of the 6 sector wide band
                    
                    if dwarfTotal > 18:
                        dwarfTotal -= 18 # Ditto

                    adjacency(dwarfTotal) 
                    if Space[shadow] == "Planet X" or Space[future] == "Planet X":
                        availableSpots = 0
                        dwarfPlanetsPlaced = False # Force the loop to fail if X is adjacent to ANY dwarf
                        break
                    
                    if len(Space[dwarfTotal]) == 0:
                        availableSpots += 1
                        dwarfLocations.append(dwarfTotal) # Remember all legal and available sectors

                if availableSpots >= 4:
                    Space[dwarf] = "Dwarf Planet"
                    del dwarfLocations[0]
                    Space[dwarfEndBand] = "Dwarf Planet"
                    del dwarfLocations[-1]
                    dwarfPlanet += 2
                    
                    while dwarfPlanet < 4:
                        dwarfIndex = random.randint(0, len(dwarfLocations)-1 ) # Roll random index from available spots
                        dwarf = dwarfLocations[dwarfIndex]
                
                        adjacency(dwarf)
                        if Space[shadow] != "Planet X" and Space[future] != "Planet X":
                            Space[dwarf] = "Dwarf Planet"
                            del dwarfLocations[dwarfIndex]
                            dwarfPlanet += 1

                    dwarfPlanetsPlaced = True

                else:
                    dwarfPlanetChecks += 1

# ASTEROIDS #
    asteroidObjects = 0
    asteroidChecks = 0
    while asteroidObjects < 4:
        asteroid = random.randint(1, len(Space) )
        
        if len(Space[asteroid]) == 0:
            adjacency(asteroid)
            if len(Space[shadow]) == 0:
                Space[asteroid] = "Asteroid"
                Space[shadow] = "Asteroid"
                asteroidObjects += 2
            elif len(Space[future]) == 0:
                Space[asteroid] = "Asteroid"
                Space[future] = "Asteroid"
                asteroidObjects += 2
            else:
                asteroidChecks += 1

        if asteroidChecks > 30: # If the map is impossible, re-do setup by breaking loop
            break

# GAS CLOUDS # 
    gasCloudObjects = 0
    gasCloudChecks = 0
    while gasCloudObjects < 2:
        gasCloud = random.randint(1, len(Space) )

        if len(Space[gasCloud]) == 0:
            adjacency(gasCloud)
            if len(Space[shadow]) == 0 or "Empty" in Space[shadow]:
                Space[gasCloud] = "Gas Cloud"
                Space[shadow] = "Empty"
                gasCloudObjects += 1
            elif len(Space[future]) == 0 or "Empty" in Space[future]:
                Space[gasCloud] = "Gas Cloud"
                Space[future] = "Empty"
                gasCloudObjects += 1
            else:
                gasCloudChecks += 1

        if gasCloudChecks > 30: 
            break

# RANDOMIZE STARTING PLAYER ORDER
    positions = [ 1, 2, 3, 4]
    random.shuffle(positions)
    counter = 0
    for color in players: # Shuffle positions and assign each player a random spot in queue
        players[color][1] = positions[counter] 
        counter += 1



# After map verification is true, create research. (avoids wasting time on research if map is illegal)
# - There are several "categories" of research. Go through each one and add them to the "possibleResearch"
# - Then, with a for loop in possibleResearch, randomly select a research option from it.
# - This will create the 6 research options.
##      CODER NOTE: Use this for debugging --->              print("At least 1+", X, "is directly opposite", Y) 
def generateResearch():
    celestialObjects = ["Asteroid", "Comet", "Dwarf Planet", "Gas Cloud"]
    possibleResearch = {
            "Asteroid"      : [],
            "Comet"         : [],
            "Dwarf Planet"  : [],
            "Gas Cloud"     : []
        }

    objectsInSpace = { # Define how many objects are in space
            "Asteroid"      : [4],
            "Comet"         : [2],
            "Dwarf Planet"  : [1],
            "Gas Cloud"     : [2]
        }
    if mode == "Expert":
        objectsInSpace["Dwarf Planet"][0] = 4


    # "At least 1+ X is directly opposite Y" //#-# OneXoppY
    possibleOneXoppY = []
    for X in celestialObjects:
        for Y in celestialObjects:
            if X == Y:
                pass
            
            else:
                oneOpposite = False
                for sector in Space:
                    adjacency(sector)

                    if Space[opposite] == X and Space[sector] == Y:
                        oneOpposite = True
                        break

                if oneOpposite == True:
                    adding = [X, Y, "OneXoppY"]

                    possibleOneXoppY.append( adding )


    # "No X is directly opposite a Y" //#-# XNOoppY
    possibleXNOoppY = []
    for X in celestialObjects:
        for Y in celestialObjects:
            if X == Y:
                pass
            
            else:
                notOpposite = True
                for sector in Space:
                    adjacency(sector)

                    if Space[opposite] == X and Space[sector] == Y:
                        notOpposite = False
                        break

                if notOpposite == True:
                    adding = [X, Y, "XNOoppY"]
                    possibleXNOoppY.append( adding )


    # "Every X is adjacent to Y" //#-# XadjY
    possibleXadjY = []
    for X in celestialObjects:
        for Y in celestialObjects:
            if X == Y or objectsInSpace[X] == 1: # Do not check condition for the same object or for Dwarf
                pass
            
            else:
                validObjects = 0
                for sector in Space:
                    adjacency(sector)

                    if Space[shadow] == X and Space[sector] == Y:
                        validObjects += 1
                    elif Space[future] == X and Space[sector] == Y:
                        validObjects += 1

                if validObjects >= objectsInSpace[X][0]:
                    adding = [X, Y, "XadjY"]
                    possibleXadjY.append( adding )
               
            
    # "At least 1 X is adjacent to a Y" //#-# OneXadjY
    possibleOneXadjY = []
    for X in celestialObjects:
        for Y in celestialObjects:
            if X == Y:
                pass
            
            else:
                validObjects = False
                for sector in Space:
                    adjacency(sector)

                    if Space[shadow] == X and Space[sector] == Y:
                        validObjects = True
                        break
                    elif Space[future] == X and Space[sector] == Y:
                        validObjects = True
                        break

                if validObjects == True:
                    adding = [X, Y, "OneXadjY"]
                    possibleOneXadjY.append( adding )

    
    # "No X is adjacent to Y" //#-# XNOadjY
    possibleXNOadjY = []
    for X in celestialObjects:
        for Y in celestialObjects:
            if X == Y:
                pass
            
            else:
                notAdjacent = True
                for sector in Space:
                    adjacency(sector)

                    if Space[shadow] == X and Space[sector] == Y:
                        notAdjacent = False
                        break
                    elif Space[future] == X and Space[sector] == Y:
                        notAdjacent = False
                        break

                if notAdjacent == True:
                    adding = [X, Y, "XNOadjY"]
                    possibleXNOadjY.append( adding )

    
    # "No X is within Z of a Y" //#-# XNOrangeY
    possibleXNOrangeY = []
    for X in celestialObjects:
        for Y in celestialObjects:
            if X == Y:
                pass
            
            else:
                for Z in range(2, 4): # Check everything once for 2 sector range, then again for 3 sector range
                    
                    for sector in Space:
                        if Space[sector] == Y: # Check starting from Y object
                            
                            observingSectors = [] # This code creates a temporary map of Z range starting from Y in the middle.
                            for negatives in range(Z, 0, -1):
                                inspectingSector = sector - (negatives)
                                if inspectingSector <= 0:
                                    inspectingSector += len(Space)
                                observingSectors.append(inspectingSector)
                                
                            for positives in range(0, Z):
                                inspectingSector = sector + (positives + 1)
                                if inspectingSector > len(Space):
                                    inspectingSector -= len(Space)
                                observingSectors.append(inspectingSector)

                            observingSectors.insert(Z, sector) # Insert current sector in middle of list

                            inRange = False
                            for item in observingSectors:
                                if Space[item] == X:
                                    inRange = True
                                    break 

                            if inRange == True: # If you found X within range of Y, then logic is impossible.
                                break           #  Immediately skip and go to next candidate object.
                            
                    if inRange == False:
                        adding = [X, Y, Z, "XNOrangeY"]
                        #print("No", X, "is within", Z, "of a", Y, "\n") #
                        possibleXNOrangeY.append( adding )
    
    # "Every X is within Z of Y" //#-# XrangeY
    possibleXrangeY = []
    if mode == "Standard":
        maxRangeMode = 4
    elif mode == "Expert":
        maxRangeMode = 6
    for X in celestialObjects:
        if objectsInSpace[X][0] == 1: # 1 Dwarf planet cannot be X
            pass
        else:
            
            for Y in celestialObjects:
                if X == Y:
                    pass
                
                else:
                    for Z in range(2, maxRangeMode): # Ranges: 2-3 for Standard, 2-5 for Expert
                        
                        for sector in Space:
                            if Space[sector] == Y: # Check starting from Y object
                                
                                observingSectors = [] # This code creates a temporary map of Z range starting from Y in the middle.
                                for negatives in range(Z, 0, -1):
                                    inspectingSector = sector - (negatives)
                                    if inspectingSector <= 0:
                                        inspectingSector += len(Space)
                                    observingSectors.append(inspectingSector)
                                    
                                for positives in range(0, Z):
                                    inspectingSector = sector + (positives + 1)
                                    if inspectingSector > len(Space):
                                        inspectingSector -= len(Space)
                                    observingSectors.append(inspectingSector)

                                observingSectors.insert(Z, sector) # Insert current sector in middle of list

                                objectsFound = 0
                                for item in observingSectors:
                                    if Space[item] == X:
                                        objectsFound += 1

                                if objectsFound >= objectsInSpace[X][0]: 
                                    adding = [X, Y, Z, "XrangeY"]
                                    #print("Every", X, "is within", Z, "of", Y) #
                                    possibleXrangeY.append( adding )
                                    break
    
    # "All X are within a band of Z sectors" //#-# XbandZ
    possibleXbandZ = []
    if mode == "Standard":
        maxRangeMode = 5
    elif mode == "Expert":
        maxRangeMode = 7
    for X in celestialObjects:
        if X == "Dwarf Planet": # Dwarf planet cannot be X
            pass
        else:
            
            for Z in range(2, maxRangeMode): # Ranges: 2-3 for Standard, 2-5 for Expert
                
                for sector in Space:

                    observingSectors = [] # This code creates a temporary map of Z range.
                        
                    for positives in range(0, Z):
                        inspectingSector = sector + (positives + 1)
                        if inspectingSector > len(Space):
                            inspectingSector -= len(Space)
                        observingSectors.append(inspectingSector)

                    objectsFound = 0
                    for item in observingSectors:
                        if Space[item] == X:
                            objectsFound += 1

                    
                    if ( objectsFound >= objectsInSpace[X][0] and
                        (Space[observingSectors[0]] == X and Space[observingSectors[-1]] == X) ): 
                        adding = [X, "", Z, "XbandZ"]
                        #print("All", X +"s are within a band of", Z, "sectors")
                        possibleXbandZ.append( adding )
                        break

    ### PLANET X CONFERENCE LOGIC ###
    # "Planet X is not within Z sectors of Y." //#-# planetXNOrangeY
    possibleplanetXNOrangeY = []
    X = "Planet X"
    
    for Y in celestialObjects:
        for Z in range(2, 4): # Check everything once for 2 sector range, then again for 3 sector range
            
            for sector in Space:
                if Space[sector] == Y: # Check starting from Y object
                    
                    observingSectors = [] # This code creates a temporary map of Z range starting from Y in the middle.
                    for negatives in range(Z, 0, -1):
                        inspectingSector = sector - (negatives)
                        if inspectingSector <= 0:
                            inspectingSector += len(Space)
                        observingSectors.append(inspectingSector)
                        
                    for positives in range(0, Z):
                        inspectingSector = sector + (positives + 1)
                        if inspectingSector > len(Space):
                            inspectingSector -= len(Space)
                        observingSectors.append(inspectingSector)

                    observingSectors.insert(Z, sector) # Insert current sector in middle of list

                    inRange = False
                    for item in observingSectors:
                        if Space[item] == X:
                            inRange = True
                            break 

                    if inRange == True: # If you found planet X within range of Y, then logic is impossible.
                        break           #  Immediately skip and go to next candidate object.
                    
            if inRange == False:
                adding = [X, Y, Z, "planetXNOrangeY"]
                possibleplanetXNOrangeY.append( adding )


    # "Planet X is within Z sectors of Y." //#-# planetXrangeY
    possibleplanetXrangeY = []
    X = "Planet X"
    if mode == "Standard":
        maxRangeMode = 4
    elif mode == "Expert":
        maxRangeMode = 6

    for Y in celestialObjects:
        for Z in range(2, maxRangeMode): # Ranges: 2-3 for Standard, 2-5 for Expert
            
            for sector in Space:
                if Space[sector] == Y: # Check starting from Y object
                    
                    observingSectors = [] # This code creates a temporary map of Z range starting from Y in the middle.
                    for negatives in range(Z, 0, -1):
                        inspectingSector = sector - (negatives)
                        if inspectingSector <= 0:
                            inspectingSector += len(Space)
                        observingSectors.append(inspectingSector)
                        
                    for positives in range(0, Z):
                        inspectingSector = sector + (positives + 1)
                        if inspectingSector > len(Space):
                            inspectingSector -= len(Space)
                        observingSectors.append(inspectingSector)

                    observingSectors.insert(Z, sector) # Insert current sector in middle of list

                    objectsFound = 0
                    for item in observingSectors:
                        if Space[item] == X:
                            objectsFound = True

                    if objectsFound == True:
                        adding = [X, Y, Z, "planetXrangeY"]
                        possibleplanetXrangeY.append( adding )
                        break

    # "Planet X is not directly opposite a Y." //#-# planetXNOoppY
    possibleplanetXNOoppY = []
    X = "Planet X"
    
    for Y in celestialObjects:
        notOpposite = True
        for sector in Space:
            adjacency(sector)

            if Space[opposite] == X and Space[sector] == Y:
                notOpposite = False
                break

        if notOpposite == True:
            adding = [X, Y, "planetXNOoppY"]
            possibleplanetXNOoppY.append( adding )



    ### CREATING THE RESEARCH USED FOR PLAYERS ###
    # Create a mega database that contains ALL research possibilities.
    researchDatabase = (possibleOneXoppY + possibleXNOoppY + possibleXadjY + possibleOneXadjY +
                        possibleXNOadjY + possibleXNOrangeY + possibleXrangeY + possibleXbandZ)
    planetXconferenceDatabase = (possibleplanetXNOrangeY + possibleplanetXrangeY + possibleplanetXNOoppY)

    while len(research) < 6: # Get 6 research theories
        
        token = random.randint(0, (len(researchDatabase)-1) ) # Might have an index error if at len. Try (len-1) if it appears.
        notValidResearch = False
        
        for theory in research:
            # [X, ] == [ , X] &&&& [ , Y] == [Y, ] are the SAME research but flipped. Remove these to give more unique research opportunities.
            if (theory[0] == researchDatabase[token][1]) and (theory[1] == researchDatabase[token][0]) and (theory[-1] == researchDatabase[token][-1]):
                notValidResearch = True
            
        if notValidResearch == False:
            getTheory = researchDatabase.pop(token)
            research.append(getTheory)

    if mode == "Standard":
        repeat = 1
    elif mode == "Expert":
        repeat = 2

    for repeat in range(repeat):
        planetXtoken = random.randint(0, (len(planetXconferenceDatabase)-1) )
        getPlanetXTheory = planetXconferenceDatabase.pop(planetXtoken)
        planetXconference.append(getPlanetXTheory)


###############################
##### IN-GAME FUNCTIONS #######
###############################                    
            
# Every action taken demands an investment of time. I believe it to be in the form of months, thematically speaking.
# - 'amount' - Time that is spent from an action, in int form
# - 'currentPlayer' - Color of the current player, the one who took the action, in string form
def spendTime(amount, currentPlayer):
    gameEnd = False
    if len(PlanetXFound) > 0: # Do not move player pawns when game has ended.
        gameEnd = True

    if gameEnd == False:
        startingSector = players[currentPlayer][0]
        
        for time in range(amount): # Move current player's figurine a number of spaces equal to 'amount' of time invested
            if players[currentPlayer][0] == 12 and (mode == "Standard"):
                players[currentPlayer][0] = 1  # Do not go to sector 13, go to sector 1 instead and continue.
            elif players[currentPlayer][0] == 18 and (mode == "Expert"): 
                players[currentPlayer][0] = 1
            else:
                players[currentPlayer][0] += 1

        for color in players: # Everyone else in that sector moves up the queue after 'current player' vacates
            if players[color][0] == startingSector:
                players[color][1] -= 1
                
        queue = 0
        for people in players: # New arrival in sector is always last in turn order
            if players[people][0] == players[currentPlayer][0]:
                queue += 1
        players[currentPlayer][1] = queue

        print(currentPlayer, "spends", str(amount), "months. Now in sector", str(players[currentPlayer][0]) + ", queue:" , str(players[currentPlayer][1]) )
    

# OUTDATED AND INFERIOR FUNCTION
##def findCurrentPlayer():
##    global currentPlayer
##    
##    playersFound = []
##    lowestNumber = 100
##    for color in players:
##        if players[color][0] == visibleSky[0]: # Remember all players within the first sector of the visible sky
##            playersFound.append( color )
##            if players[color][1] < lowestNumber:
##                lowestNumber = players[color][1]
##
##    if len(playersFound) > 0:
##        for color in playersFound:
##            if players[color][1] == lowestNumber:
##                currentPlayer = color

# The player furthest back on the time track is the one who takes their turn. If tied, furthest ahead in queue.
# - By definition, that would be whoever's in the first sector of the visible sky, as the sky always begins from the furthest back player.
# - Therefore, the key to finding the current player and player queue order is primarily through the visibleSky.
# - Queue order is dependent first on furthest back sector, and if any ties in sectors, they're broken by lowest queue number
def findPlayerOrder():
    global currentPlayer
    playerOrder = []

    for sector in visibleSky:
        playersInSector = []
        for color in players:
            if players[color][0] == sector:
                playersInSector.append([color, players[color][1], sector] ) # [Player, queue #, location]


        for X in range( len(playersInSector) ):
            lowestNumber = 10               # Programming trick. Only update lowest number if you find something lower than itself.
            for entity in playersInSector:  # Loop that finds lowest queue time available
                if entity[1] < lowestNumber and entity not in playerOrder:
                    lowestNumber = entity[1]

            for entity in playersInSector: # Put in queue respectively. Ignore anyone already in the list
                if entity[1] == lowestNumber and entity not in playerOrder:
                    playerOrder.append(entity)

    currentPlayer = playerOrder[0][0] # Current player is first in order
    return playerOrder # Return the order list

                
# Whenever a player is moved, the visible sky must start from the sector of the furthest back player (if empty)
def moveSky():
    moveSky = True
    for color in players: # Always attempt to moveSky, but do not if someone is in its leftmost sector. Do not rotate on Game End either.
        if players[color][0] == visibleSky[0] or len(PlanetXFound) > 0: 
            moveSky = False 
            break
    if moveSky == True:
        playerLocations = [ players["Blue"][0], players["Red"][0], players["Yellow"][0], players["Purple"][0] ]
        for sector in visibleSky:
            if sector in playerLocations:
                finalSector = sector # Sky moves to the first sector that it comes across with a player.
                break

    # If crossing from sectors 12 to 1, or from 18 to 1, manipulate the math a little to find the true difference.
        steps = finalSector - visibleSky[0]
        if steps < 0:
            finalSector += len(Space)
            steps = finalSector - visibleSky[0]

    # All sectors in visibleSky are incremented by one to simulate "turning the wheel"
        for X in range(steps):
            index = 0
            for sector in visibleSky:
                if sector == 12 and (mode == "Standard"):
                    visibleSky[index] = 1
                elif sector == 18 and (mode == "Expert"):
                    visibleSky[index] = 1
                else:
                    visibleSky[index] += 1

                index += 1

            ## CHECK FOR THEORY PHASE ##
            if mode == "Standard":
                if visibleSky[0] == 1 or visibleSky[0] == 4 or visibleSky[0] == 7 or visibleSky[0] == 10:
                    if visibleSky[0] == 1: # Aesthetic purposes only. Do not remove this.
                        theoryPhase(1, 13 )
                    else:
                        theoryPhase(1, visibleSky[0] )
                    peerReview()
            # Planet X conference
                if visibleSky[0] == 11 and players["Purple"][4][0] == False: # The player color doesn't matter, I just chose purple
                    for color in players:
                        players[color][4][0] = True
                    print("#####\nThe Planet X conference has commenced! Review your research logs for updates.")

                        
            elif mode == "Expert":
                if ( visibleSky[0] == 1 or visibleSky[0] == 4 or visibleSky[0] == 7 or
                     visibleSky[0] == 10 or visibleSky[0] == 13 or visibleSky[0] == 16):
                    if visibleSky[0] == 1: 
                        theoryPhase(1, 19 )
                    else:
                        theoryPhase(2, visibleSky[0] )
                    peerReview()

            # Planet X conference x2
                if visibleSky[0] == 10 and players["Purple"][4][0] == False:
                    for color in players:
                        players[color][4][0] = True
                    print("\n#####\nThe first Planet X conference has commenced! Review your research logs for updates.")
                
                elif visibleSky[0] == 1 and players["Purple"][4][1] == False: 
                    for color in players:
                        players[color][4][1] = True
                    print("\n#####\nThe second Planet X conference has commenced! Review your research logs for updates.")

            
# This function lets a player manually place one theory in a sector of their choosing.            
def chooseTheory(color):
    validSector = True
    while validSector == True:
                
        if len(PlanetXFound) == 0:
            chooseTheory = input("\n -- Please choose a theory to submit - [C], [A], [D], [G], or [S]kip: --\n")
        else:
            chooseTheory = input("\n -- Please choose a theory to submit - [C], [A], [D], [G]: --\n") # May not skip if FINAL theory submission
        chosenTheory = inputValidation(chooseTheory, "theory")

        print("\nYou may place a theory in any of the", str(len(Space)), "sectors that have not already been peer reviewed:")
        chooseSector = input("")
        repeat = True
        while repeat == True: # Input validation for selecting sector
            if chooseSector.isdigit():
                if int(chooseSector) not in Space:
                    chooseSector = input("Error! That sector does not exist. Re-try:\n")
                else:
                    repeat = False
                    chooseSector = int(chooseSector)

        if len(theoryScape[chooseSector]) > 0: # May not add a theory to a peer-reviewed sector
            for theory in theoryScape[chooseSector]:
                if theory[-1] == 0:
                    print("\nERROR: Cannot place a theory there!\n")
                    validSector = False

        if validSector == True:
            submitting = [ color, chosenTheory, 3 ] # E.G. [ "Blue", "Comet", 2 ]
            theoryScape[chooseSector].append(submitting)
            print(art[color], color, "has placed a theory in sector:\t", str(chooseSector) )
            if chosenTheory == "Comet" or chosenTheory == "C" or chosenTheory == "c":
                indexTheory = 0
            elif chosenTheory == "Asteroid" or chosenTheory == "A" or chosenTheory == "a":
                indexTheory = 1
            elif chosenTheory == "Dwarf Planet" or chosenTheory == "D" or chosenTheory == "d":
                indexTheory = 2
            elif chosenTheory == "Gas Cloud" or chosenTheory == "G" or chosenTheory == "g":
                indexTheory = 3
            players[color][2][indexTheory] -= 1
            validSector = False

        
def theoryPhase(maxTheories, currentSector):
    if currentSector != "Final Stage":
        currentSector -= 1
        print("\n\n -{"+str(currentSector)+"}- THEORY PHASE -{"+str(currentSector)+"}- ")
    time.sleep(2)

    # FIND PLAYER ORDER
    playerOrder = findPlayerOrder()

    # SELECT AND PLACE THEORIES
    index = 0
    for color in players:
        color = playerOrder[index][0] # Players place down theories in player order.
        
         # Player ought to select Theory. For now, make it completely random
        #chooseTheory(color)

         # Scenario where all players always submit random theories
        theoriesChosen = 0
        while theoriesChosen < maxTheories:
            flipCoin = random.randint(0, 1)
            
            if flipCoin == 0: # This player chooses not to submit a theory this round
                theoriesChosen += 1
                break
            
            else:    
                randomTheory = random.randint(0, 3) # Choose random theory to submit (only if theories available)
                if players[color][2][randomTheory] > 0:
                    
                    if randomTheory == 0: # Transform integer of theory into respective object's name
                        randomObject = "Comet"
                    elif randomTheory == 1:
                        randomObject = "Asteroid"
                    elif randomTheory == 2:
                        randomObject = "Dwarf Planet"
                    elif randomTheory == 3:
                        randomObject = "Gas Cloud"

                    # Theory CANNOT be submitted in a sector which already has an approved, peer-reviewed theory
                    chosenSector = random.randint(1, len(Space) )
                    validSector = True
                    if len(theoryScape[chosenSector]) > 0:
                        for theory in theoryScape[chosenSector]:
                            if theory[-1] == 0:
                                print("\nCannot place a theory there!\n")#
                                validSector = False

                    if validSector == True:
                        submitting = [ color, randomObject, 3 ] # E.G. [ "Blue", "Comet", 2 ]
                        theoryScape[chosenSector].append(submitting)
                        print(art[color], color, "has placed a theory in sector:\t", str(chosenSector) )
                        players[color][2][randomTheory] -= 1
                        theoriesChosen += 1

        index += 1
        
    print("")

# PEER REVIEW
def peerReview():
    for sector in range(1, len(theoryScape)+1 ): # Iterate through EVERY sector

        sectorReviewed = False
        for theories in theoryScape[sector]: # Check if this sector has already been reviewed
            if theories[-1] == 0:
                sectorReviewed = True
                
        if sectorReviewed == False: # If not reviewed, advance all theories 1 space
            for theories in theoryScape[sector]:
                theories[-1] -= 1


            index = len(theoryScape[sector]) - 1
            theoryVerified = False
            for X in range( len(theoryScape[sector]), 0, -1):
                if theoryScape[sector][index][-1] == 0: # Attempt peer review if any theories advanced to the 0th space
                    print("\n"+art[theoryScape[sector][index][0]], theoryScape[sector][index][0], "reveals their theory for a", theoryScape[sector][index][1], "in sector", sector)
                    if Space[sector] == theoryScape[sector][index][1]:
                        print("++ TRUE: The Scientific community verifies a", Space[sector], "exists in sector", str(sector),"++")
                        theoryVerified = True
                    else:
                        print("-- FALSE: The Scientific community bounces the", theoryScape[sector][index][1], "notion in sector", str(sector),"--")
                        spendTime(1, theoryScape[sector][index][0] ) # That player is punished by losing a month and their theory there
                        del theoryScape[sector][index]

                index -= 1


            if theoryVerified == True: # If peer review was successful, check all other theories if they are allowed to stay
                index = len(theoryScape[sector]) - 1
                
                for X in range( len(theoryScape[sector]), 0, -1):
                    if Space[sector] != theoryScape[sector][index][1]:
                        print("\n"+ theoryScape[sector][index][0] + "'s", theoryScape[sector][index][1], "theory was nullified")
                        spendTime(1, theoryScape[sector][index][0] ) # That player is punished by losing a month and their theory there
                        del theoryScape[sector][index]
                        
                    index -= 1 
         


# Current player chooses an action to take.
def action(choice):
    global PlanetXFound

    if choice == "S" or choice == "s": # Survey
        if mode == "Standard":
            print("-- SURVEYING -- Time costs for following ranges:" ,
            "\n 1, 2, 3 sectors: 4 Time  |||  4, 5, 6 sectors: 3 Time" ,
            "\n\n OPTIONS: [A]steroid, [C]omet, [D]warf Planet, [G]as Cloud, [E]mpty, OR [R]eturn to menu.")
        elif mode == "Expert":
            print("-- SURVEYING -- Time costs for following ranges:" ,
            "\n 1, 2, 3 sectors: 4 Time  |||  4, 5, 6 sectors: 3 Time  ||| 7, 8, 9 sectors: 2 Time" ,
            "\n\n OPTIONS: [A]steroid, [C]omet, [D]warf Planet, [G]as Cloud, [E]mpty, OR [R]eturn to menu.")
            
        surveyObject = input("  Survey for: ")
        surveyObject = inputValidation(surveyObject, "survey")
        if surveyObject != "R" and surveyObject != "r" and surveyObject != "Return":
            print("\n - Visible Sky:", visibleSky, "-")
            start = input(" Select sector to start surveying from, OR [R]eturn:\n")
            start = inputValidation(start, "surveyStart")
            end = input(" Surveying until sector, OR [R]eturn:\n")
            end = inputValidation(end, "surveyEnd")

        if (surveyObject == "R" or surveyObject == "r" or surveyObject == "Return" # If user backs out, cancel
            or start == "R" or start == "r" or start == "Return"
            or end == "R" or end == "r" or end == "Return"): 
            print("\nCancelling the Survey action... return to menu.\n")
        
        elif visibleSky.index(start) > visibleSky.index(end): # Error check
            print("Error: You cannot begin a survey from a sector past the ending sector... back to menu.\n")
        else:
            
            objectsFound = 0
            for sector in range( len(visibleSky) + 1 ): # Survey all visible spaces. If a shorter range is desired, condition will stop the loop.
                sectorTotal = start + sector 
                    
                if sectorTotal > 12 and (mode == "Standard"):
                    sectorTotal -= 12
                elif sectorTotal > 18 and (mode == "Expert"):
                    sectorTotal -= 18

                if surveyObject in Space[sectorTotal]:
                    objectsFound += 1
                elif surveyObject == "Empty" and Space[sectorTotal] == "Planet X": # Planet X shows up as "Empty"
                    objectsFound += 1 

                if sectorTotal == end: # Aforementioned condition
                    break

            if objectsFound != 1:
                plural = "s"
                toBe = "are"
            else:
                plural = ""
                toBe = "is"
            print("\n -- There", toBe, objectsFound, surveyObject + plural , "in sectors", str(start)+"-"+str(end)+" --")


            steps = end - start
            if steps < 0:
                end += len(Space)
                steps = end - start

            if steps >= 7:
                spendTime(2, currentPlayer)
            elif steps >= 4:
                spendTime(3, currentPlayer)
            else:
                spendTime(4, currentPlayer)


    elif choice == "T" or choice == "t": # Target
        if players[currentPlayer][-2] > 0:
            print("\n - Visible Sky:", visibleSky, "-")
            targetSector = input("-- TARGETTING -- \n Please select visible sector to secretly view, OR [R]eturn to menu:\n")
            targetSector = inputValidation(targetSector, "targetting")

            if targetSector == "R" or targetSector == "r" or targetSector == "Return": # Cancel command
                print("Cancelling the Target action... return to menu.\n")

            else:
                if Space[targetSector] == "Planet X" or Space[targetSector] == "Empty": # Do not reveal planet X!
                    print("Sector", str(targetSector), "has an Empty sector in it.")
                else:
                    print("Sector", str(targetSector), "has a", Space[targetSector] , "in it.")
                spendTime(4, currentPlayer)
                players[currentPlayer][-2] -= 1
        else: # Player must have a target token available to do the action.
            print(currentPlayer, "no longer has Target tokens to spend! Going back...\n")


    elif choice == "R" or choice == "r": # Research # BUG - Having trouble stopping players from researching twice in a row
        alphabet = ["A", "B", "C", "D", "F", "G"]
        index = 0
        for letter in alphabet:
            if players[currentPlayer][3][index] == False:
                print(letter + ": ?")
            elif players[currentPlayer][3][index] == True:
                if research[index][-1] == "OneXoppY":
                    print(letter + ":", "At least 1+", research[index][0], "is directly opposite a", research[index][1])
                elif research[index][-1] == "XNOoppY":
                    print(letter + ":", "No", research[index][0], "is directly opposite a", research[index][1])
                elif research[index][-1] == "XadjY":
                    print(letter + ":", "Every", research[index][0], "is adjacent to a", research[index][1])
                elif research[index][-1] == "OneXadjY":
                    print(letter + ":", "At least 1", research[index][0], "is adjacent to a", research[index][1])
                elif research[index][-1] == "XNOadjY":
                    print(letter + ":", "No", research[index][0], "is adjacent to a", research[index][1])
                elif research[index][-1] == "XNOrangeY":
                    print(letter + ":", "No", research[index][0], "is within", research[index][2], "sectors of a", research[index][1])
                elif research[index][-1] == "XrangeY":
                    print(letter + ":", "Every", research[index][0], "is within", research[index][2], "sectors of a", research[index][1])
                elif research[index][-1] == "XbandZ":
                    print(letter + ":", "All", research[index][0], "are within a band of", research[index][2], "sectors")

            index += 1

        index = 0
        for theory in planetXconference:
            if players[currentPlayer][4][index] == False:
                print("Planet X: ?")
            elif players[currentPlayer][4][index] == True:
                if theory[-1] == "planetXNOrangeY":
                    print("Planet X is not within", theory[2], "sectors of a", theory[1])
                elif theory[-1] == "planetXrangeY":
                    print("Planet X is within", theory[2], "sectors of a", theory[1])
                elif theory[-1] == "planetXNOoppY":
                    print("Planet X is not directly opposite a", theory[1])

            index += 1

        if players[currentPlayer][-2] >= 2:
            chooseResearch = input("-- RESEARCH -- \n Please select a letter to category to research, OR [R]eturn to menu:\n")
            chooseResearch = inputValidation(chooseResearch, "researching")
            if chooseResearch == "R" or chooseResearch == "r" or chooseResearch == "Return":
                print("\nCancelling the Research action... return to menu.\n")
            else:
                
                acquireTheory = alphabet.index(chooseResearch)
                if players[currentPlayer][3][acquireTheory] == True:
                    print("Error! You've already researched that category. Going back...\n")
                else:
                    players[currentPlayer][3][acquireTheory] = True
                    players[currentPlayer][-2] = 0
                    spendTime(1, currentPlayer)
                    
        else:
            print(currentPlayer, "may not research twice in a row! Going back...\n")


    elif choice == "G" or choice == "g": # Guess planet X
        confirm = "N"
        while confirm != "Y" and confirm != "y":
            guessSectorX = input("-- GUESSING -- \n Please select which sector you think Planet X is hiding in, OR [R]eturn:\n")
            guessSectorX = inputValidation(guessSectorX, "guessSectorX")
            if guessSectorX == "Return" or guessSectorX == "R" or guessSectorX == "r":
                print("\nCancelling the Guess Planet X action... return to menu.\n")
                break
            
            adjacency(guessSectorX)
            print(" [...] - [X at #"+str(guessSectorX)+"] - [...] " ,
                  "\n - What is in sector" , str(shadow) + "?")
            guessSector1 = input("")
            guessSector1 = inputValidation(guessSector1, "guessSectorShadow")
            
            print(" ["+guessSector1+"] - [X at #"+str(guessSectorX)+"] - [...]" ,
                  "\n - How about in sector" , str(future) + "?")
            guessSector2 = input("")
            guessSector2 = inputValidation(guessSector2, "guessSectorFuture")
            
            print(" ["+guessSector1+"] - [X at #"+str(guessSectorX)+"] - ["+guessSector2+"] ")
            
            confirm = input("Confirm? [Y]es, [N]o, or [B]ACK\n")
            if confirm == "Y" or confirm == "y":
                adjacency(guessSectorX)
                spendTime(5, currentPlayer)
                if ( ("Planet X" in Space[guessSectorX]) and
                     (Space[shadow] == guessSector1) and
                     (Space[future] == guessSector2) ):
                    PlanetXFound.append(currentPlayer)
                    print("\n\n #-#- Congratulations! You found Planet X! -#-#")
                    
                else:
                    print("\n\n Ooh, sorry," , currentPlayer+"'s guess was incorrect.")

            elif confirm == "B" or confirm == "b":
                print("\nCancelling the Guess Planet X action... back to menu.\n")
                break
        


#########################
####### GAMEPLAY ########
#########################

# Quick setup
mode = input("Greetings. Would you like to play Standard (12 Sectors), or Expert (18)?\n")
mode = inputValidation(mode, "gameMode")

possibleMap = False  # Automatically reset the map if not possible
attempts = 0 # 
while possibleMap == False:
    setUp()
    attempts += 1 #
    if verify() == True:
        possibleMap = True
        generateResearch()

print("\n ## Map successful. ## Attempts:", attempts)


# Core gameplay loop. Game continues until Planet X is found by any player.
PlanetXFound = []
while len(PlanetXFound) == 0:
    moveSky()
    playerOrder = findPlayerOrder()     # Get the queue list and currentPlayer
    if players[currentPlayer][-3] != 2: # Player will be able to research on their next turn, if they have already researched
        players[currentPlayer][-3] += 1
    #findCurrentPlayer()
    print("\n\n\n", art[currentPlayer], "Current Player and sector: ["+currentPlayer+",", str(players[currentPlayer][0])+"]" , art[currentPlayer])
    print("\nPlease choose an action to do." ,
          "\n[S]urvey (2-4), [T]arget (4), [R]esearch (1), [G]uess Planet X (5).")
    chooseAction = input("")
    action(chooseAction)



print("\n ! PLANET X HAS BEEN FOUND. EVERYONE ELSE TAKES ONE LAST ACTION BEFORE THE GAME ENDS !")
playersWhoTookFinalAction = PlanetXFound
playerOrder = findPlayerOrder()
for playerInfo in playerOrder:
    currentPlayer = playerInfo[0]
    
    if currentPlayer in playersWhoTookFinalAction:
        pass
    else:
            
        if players[currentPlayer][0] == players[PlanetXFound[0]][0]:
            print(currentPlayer, "may not take a final action for being in the same sector as the first Planet X finder.\n")
        else:
            for sector in visibleSky: # Figure out if this player may place 2 or 1 theories depending on distance
                for color in players:
                    if color == PlanetXFound[0] and players[color][0] == sector:
                        winnerSector = visibleSky.index(sector)
                    elif color == currentPlayer and players[currentPlayer][0] == sector:
                        currentPlayerSector = visibleSky.index(sector)

            difference = winnerSector - currentPlayerSector
            if difference >= 4:
                theoriesAvailable = 2
            else:
                theoriesAvailable = 1


            print("\n\n"+art[currentPlayer], currentPlayer+", decide if you wish to submit a [T]heory ("+str(theoriesAvailable), "available), or [G]uess Planet X.")
            chooseAction = input("")
            chooseAction = inputValidation(chooseAction, "chooseFinalAction")
            if chooseAction == "R" or chooseAction == "r" or chooseAction == "Return":
                pass
            elif chooseAction == "G" or chooseAction == "g" or chooseAction == "Guess":
                action("G")
            elif chooseAction == "T" or chooseAction == "t" or chooseAction == "Theory":
                for x in range(theoriesAvailable):
                    chooseTheory(currentPlayer)

### COUNT VICTORY POINTS ###
# Earn victory points for theories
for sector in theoryScape:
    for theory in theoryScape[sector]:

        if Space[sector] == theoryScape[1]: # Check to see if the theory is true in that sector
            
            if theory[2] == 0: # If theory was submitted first or tied for first, +1 Bonus point
                players[ theory[0] ][-1] += 1

            if theory[1] == "Asteroid":
                players[ theory[0] ][-1] += 2

            elif theory[1] == "Comet":
                players[ theory[0] ][-1] += 3

            elif theory[1] == "Gas Cloud":
                players[ theory[0] ][-1] += 4

            elif theory[1] == "Dwarf Planet":
                if mode == "Standard":
                    players[ theory[0] ][-1] += 4
                elif mode == "Expert":
                    players[ theory[0] ][-1] += 2

# Earn victory points for finding planet X
for player in PlanetXFound:
    playersIndex = PlanetXFound.index(player)

    # First player to find X automatically earns 10 points. Remember their location.
    if playersIndex == 0:
        players[player][-1] += 10
        winnerSector = visibleSky.index( players[player][0] )

    # Other players will earn 2 points for every space behind the original finder.
    else: 
        loserSector = visibleSky.index( players[player][0] )
        difference = winnerSector - loserSector
        pointsEarned = difference * 2
        
        players[player][-1] += pointsEarned

highestScore = 0
for color in players:
    if players[color][-1] > highestScore:
        highestScore = players[color][-1]
        highestWinner = color
# WARNING - NO TIE BREAKERS HAVE BEEN CODED. REFER TO RULEBOOK AND ADD THEM

print("\n\n"+art[highestWinner],highestWinner,"has won the game with", players[highestWinner][-1], "points!!", art[highestWinner])
print("\n -- The game is now over. Thank you for playing my code =] -- \n-Ivan")
