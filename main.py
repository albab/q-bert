import pygame, sys, os, random
from pygame.locals import *
import CubeFile, QbertFile, BallFile, CoilyFile, curseFile
import platformFile,SamSlickFile, scoreboardFile

objectsToDraw = []
objectsToAnimate = []
listOfCubes = []
listOfBalls = []
listOfCoilies = []
listOfPlatforms = []
listOfSamSlick = []
keyboardQueue = []
animateLive = True
animateCounter = 0
levelData = []
currentLevel = 0
scoreboard = None
restartTimer = 0
curseSound = None
QbertDeathTimer = 0
FRAMERATE = 90
clock = pygame.time.Clock()
pixels = 500


fileStrings = ("redBallChance","purpleBallChance","greenBallChance","Sam/SlickChance","Ugg/WrongWayChance","LeftFaceColor","RightFaceColor","SelectionMode","NumberOfTops","ListOfTopColors")

#------ loadLevelData
def loadLevelData():
    theFile = open("Q-bert_Data.tsv","r")
    count = 0
    for line in theFile:
        if 0 == count:
            count += 1
            continue
        lineData = dict()
        line = line.strip("\n")
        parts = line.split("\t")
        for i in range (0,5):
            lineData[fileStrings[i]] = int(parts[i]);
        for i in range(0,2):
            lineData[fileStrings[5+i]] = (int(parts[5+3*i+0]),int(parts[5+3*i+1]),int(parts[5+3*i+2]))
        lineData[fileStrings[7]] = int(parts[11])
        lineData[fileStrings[8]] = int(parts[12])
        topColorList = []
        for i in range (0,lineData[fileStrings[8]]):
            topColorList.append((int(parts[13+3*i+0]),int(parts[13+3*i+1]),int(parts[13+3*i+2])))
        lineData[fileStrings[9]] = topColorList
        levelData.append(lineData)
        # print(lineData)
    theFile.close()

#------ getCube
# Returns the cube in the list of cube at the given location.
def getCube(loc):
    return listOfCubes[loc[0]][loc[1]]

#----- readEvents
# This method escapes the loop at the end of the program too often.
# If there are any "events" (mouse motions, clicks, key presses, things
# that happen to the window, or somebody says "quit") this might do
# something about it....
def readEvents(events):
    global keyboardQueue

    for event in events:
        if event.type == QUIT:
            pygame.quit() #close the window
            sys.exit(0)   #quit the program.
        if event.type == KEYUP:
            keyboardQueue.append(event.key)

    if qbert.IAmMoving == False:
        while len(keyboardQueue)>0:
            nextKey = keyboardQueue.pop(0)
            if nextKey == K_w:
                qbert.jumpUpRight()
                keyboardQueue = []
                break
            if nextKey == K_q:
                qbert.jumpUpLeft()
                keyboardQueue = []
                break
            if nextKey == K_a:
                qbert.jumpDownLeft()
                keyboardQueue = []
                break
            if nextKey == K_s:
                qbert.jumpDownRight()
                keyboardQueue = []
                break

def PauseUntilKeyboard():
   while 1:
      e = pygame.event.wait()
      if e.type in (pygame.QUIT, pygame.KEYDOWN):
         return
            

#------ isValidCube
# Receives a set of (cube row, cube row position) and determines whether
# the cube is one that is in the pyramid
def isValidCube(coords):
    row = coords[0]
    rowPos = coords[1]

    if rowPos<0 or row>6 or rowPos>row:
        return False
    return True

#------ isValidPlatform
# Receives a set of (cube row, cube row position) and determines
# which platform is at this spot (or None)
def isValidPlatform(coords):
    for p in listOfPlatforms:
        if p.row == coords[0] and p.rowPos == coords[1]:
            return p
    return None
        
#------ updateScreen
# Draws whatever you want on the screen
def updateScreen():
    screen = pygame.display.get_surface()
    screen.fill ((0,0,0)) # Clear the screen with black --> (0,0,0)

    for obj in objectsToDraw:
        screen.blit(obj.image, obj.rect.topleft)
    
    if curse.iAmShowing:
        screen.blit(curse.image, (qbert.rect.left+30, qbert.rect.top-20))

    pygame.display.flip() # Render what you drew on the screen

#------- findTopCenter
# Determines the screen (pixel) coordinates of the center of the top face of
# the cube at the given row and rowPos.
def findTopCenter(row, which):
    x = 250-24*row+50*which
    y = 75 + 49*row
    return (x,y)

#------- createPlatforms
# Generates two platforms, just off the pyramid and adds them to the global lists
def createPlatforms():
    platform1 = platformFile.Platform(4,-1)
    loc = findTopCenter(4,-1)
    platform1.rect.centerx = loc[0]
    platform1.rect.top = loc[1]
    listOfPlatforms.append(platform1)
    objectsToDraw.append(platform1)
    objectsToAnimate.append(platform1)
    platform2 = platformFile.Platform(4,5)
    loc = findTopCenter(4,5)
    platform2.rect.centerx = loc[0]
    platform2.rect.top = loc[1]
    listOfPlatforms.append(platform2)
    objectsToDraw.append(platform2)
    objectsToAnimate.append(platform2)

#------ createPyramid
# Erases any existing cubes and builds a new pyramid, based on the colors for this level
def createPyramid():
    # Delete existing cubes
    global listOfCubes
    for r in listOfCubes:
        for cube in r:
            objectsToDraw.remove(cube)
    listOfCubes = []

    # Create a new pyramid
    sideColors = (levelData[currentLevel]["LeftFaceColor"],levelData[currentLevel]["RightFaceColor"])
    topColors = levelData[currentLevel]["ListOfTopColors"]
    levelMode = levelData[currentLevel]["SelectionMode"]
    for row in range (0,7):
        rowOfCubes = []
        for which in range (0,row+1):
            tempCube = CubeFile.Cube(topColors, inSides= sideColors, selectionMode = levelMode)
            loc = findTopCenter(row,which)
            tempCube.rect.centerx = loc[0]
            tempCube.rect.top = loc[1]
            objectsToDraw.append(tempCube)
            rowOfCubes.append(tempCube)
        listOfCubes.append(rowOfCubes)    

#------ destroyEnemies
# Remove all enemies from screen
def destroyEnemies():
    # print("Destroying all enemies.")
    for b in listOfBalls:
        objectsToDraw.remove(b)
        objectsToAnimate.remove(b)
        listOfBalls.remove(b)
    for c in listOfCoilies:
        objectsToDraw.remove(c)
        objectsToAnimate.remove(c)
        listOfCoilies.remove(c)
    for ss in listOfSamSlick:
        objectsToDraw.remove(ss)
        objectsToAnimate.remove(ss)
        listOfSamSlick.remove(ss)
    global restartTimer
    restartTimer = 0    

#------ reset level
# Resets pyramid and Q*bert. Removes all enemies.
def resetLevel():
    createPyramid()
    objectsToDraw.remove(qbert)
    objectsToDraw.append(qbert)
    destroyEnemies()
    qbert.reset()

#------ initialize
# Start up pygame and makes a window appear. 
# Only needed once at start of game.
def initialize():
    pygame.init()
    global window, qbert, curse
    global scoreboard,curseSound
    window = pygame.display.set_mode((500,500))

    loadLevelData()

    scoreboard = scoreboardFile.Scoreboard(levelData[0]["ListOfTopColors"][0])
    objectsToDraw.append(scoreboard)
    
    createPyramid()
    createPlatforms()
    
    qbert = QbertFile.Qbert()
    topCube = listOfCubes[0][0]
    objectsToDraw.append(qbert)
    objectsToAnimate.append(qbert)
    curse = curseFile.Curse()
    objectsToAnimate.append(curse)
    curseSound = pygame.mixer.Sound("Sounds/curse.wav")
    
#------- thingsCollided
# Check if two objects (a and b) have collided.
def thingsCollided(a,b):
    return a.rect.colliderect(b.rect) and (a.targetSquare == b.targetSquare)

# ----- checkOnQbertLanding
# Check to see where Q*Bert lands
def checkOnQbertLanding():
    global restartTimer
    if qbert.IAmMoving:
        if isValidCube(qbert.targetSquare):
            whichCube = getCube(qbert.targetSquare)
            if qbert.yVel > 0 and qbert.rect.bottom > whichCube.centerOfFace()[1]:
                qbert.IAmMoving = False
                qbert.setPos(whichCube.centerOfFace())
                if whichCube.currentColor == 1:
                    scoreboard.increaseScore(20)
                whichCube.advanceColor()
                
        else:
            platform = isValidPlatform(qbert.targetSquare)
            if (None != platform):
                if qbert.yVel > 0 and qbert.rect.bottom > platform.centerOfFace()[1]:
                    qbert.IAmOnPlatform = True
                    qbert.setPos(platform.centerOfFace())
                    platform.carryQbert(qbert);
                if qbert.targetSquare == (0,0):
                    restartTimer = 150
                        
            else:
                if qbert.targetSquare[0] <7 and qbert.yVel>0:  # falling off back of pyramid
                    # put Qbert at start of draw list, so he is behind pyramid.
                    objectsToDraw.remove(qbert)
                    objectsToDraw.insert(0, qbert)
    if qbert.rect.y>500:
        qbert.reset()
        scoreboard.decrementLives()
        curseSound.play()
        objectsToDraw.remove(qbert)
        objectsToDraw.append(qbert)  # put Qbert back on front level.
        destroyEnemies()

# ----- checkOnSamSlickLanding
# Check to see if Sam or Slick have landed on one of the cubes, if they are moving.
def checkOnSamSlickLanding():
    for ss in listOfSamSlick:
        if ss.IAmMoving:
            if isValidCube(ss.targetSquare):
                whichCube = getCube(ss.targetSquare)
                if ss.yVel>0 and ss.rect.bottom>whichCube.centerOfFace()[1]:
                    ss.IAmMoving = False
                    ss.setPos(whichCube.centerOfFace())
                    whichCube.resetColor()
            if ss.yPos>500:
                objectsToDraw.remove(ss)
                objectsToAnimate.remove(ss)
                listOfSamSlick.remove(ss)



# ----- checkOnBallLanding
# Checks to see if any balls have landed on one of the cubes, if they are moving.
def checkOnBallLanding():
    for b in listOfBalls:
        if b.IAmMoving:
            if isValidCube(b.targetSquare):
                whichCube = getCube(b.targetSquare)
                if b.yVel>0 and b.rect.bottom>whichCube.centerOfFace()[1]:
                    b.IAmMoving = False
                    b.setPos(whichCube.centerOfFace())
            if b.yPos>500:
                objectsToDraw.remove(b)
                objectsToAnimate.remove(b)
                listOfBalls.remove(b)
        else:
            if b.targetSquare[0] == 6 and b.myColor == 1:
                objectsToDraw.remove(b)
                objectsToAnimate.remove(b)
                listOfBalls.remove(b)
                tempCoily = CoilyFile.Coily(qbert)
                tempCoily.setPos(getCube(b.targetSquare).centerOfFace())
                tempCoily.targetSquare = b.targetSquare
                tempCoily.oldSquare = b.targetSquare
                objectsToDraw.append(tempCoily)
                objectsToAnimate.append(tempCoily)
                listOfCoilies.append(tempCoily)
                break

# ----- checkOnCoilyLanding
# Checks to see whether Coily has landed on one of the cubes.
def checkOnCoilyLanding():
    for c in listOfCoilies:
        if c.IAmMoving:
            if isValidCube(c.targetSquare):
                whichCube = getCube(c.targetSquare)
                if c.yVel>0 and c.rect.bottom>whichCube.centerOfFace()[1]:
                    c.IAmMoving = False
                    c.setPos(whichCube.centerOfFace())
        if c.yPos>500:
            destroyEnemies()
            scoreboard.increaseScore(700)
            return
                    
                    
# ------- QbertHasHitObject
# Freeze the screen and display the curse
def QbertHasHitObject(obj):
    objectsToDraw.remove(obj);
    objectsToAnimate.remove(obj);
    global animateLive
    animateLive = False
    curse.iAmShowing = True
    curseSound.play()
    scoreboard.decrementLives()
    return

# ------- checkOnQbertEnemyCollision
# Checks if Q*bert has hit any enemies
def checkOnQbertEnemyCollision():
    if qbert.IAmOnPlatform:
        return
    for b in listOfBalls:
        if b.myColor == 2:
            continue
        if thingsCollided(b,qbert):
            QbertHasHitObject(b)
            listOfBalls.remove(b)
            return
    for c in listOfCoilies:
        if thingsCollided(c,qbert):
            QbertHasHitObject(c)
            listOfCoilies.remove(c)
            return
    for ss in listOfSamSlick:
        if thingsCollided(ss,qbert):
            objectsToDraw.remove(ss)
            objectsToAnimate.remove(ss)
            listOfSamSlick.remove(ss)
            scoreboard.increaseScore(300)
            return


# ------ spawnEnemies
# Decide if should add enemy to the screen.
def spawnEnemies():
    global restartTimer
    if restartTimer<140:
        restartTimer += 1
        return
    
    if random.randrange(1000)<levelData[currentLevel]["redBallChance"]:
        tempBall = BallFile.Ball(0)
        objectsToDraw.append(tempBall)
        objectsToAnimate.append(tempBall)
        listOfBalls.append(tempBall)
        return
    if random.randrange(1000)<levelData[currentLevel]["purpleBallChance"]:
        tempBall = BallFile.Ball(1)
        objectsToDraw.append(tempBall)
        objectsToAnimate.append(tempBall)
        listOfBalls.append(tempBall)
        return
    if random.randrange(1000)<levelData[currentLevel]["greenBallChance"]:
        tempBall = BallFile.Ball(2)
        objectsToDraw.append(tempBall)
        objectsToAnimate.append(tempBall)
        listOfBalls.append(tempBall)
        return
   
    if random.randrange(1000)<levelData[currentLevel]["Sam/SlickChance"]:
        for i in range (0,2):
            sam = SamSlickFile.SamSlick(i);
            objectsToDraw.append(sam);
            objectsToAnimate.append(sam);
            listOfSamSlick.append(sam)
        return

# ------ checkIfLevelCleared
# Decides if level is over. Returns True, if it is.
def levelCleared():
    for row in listOfCubes:
        for cube in row:
            if cube.isNotClear():
                return False
    return True

#------ animateStep
# Move all the things
def animateStep():
    global animateLive, animateCounter
    if animateLive:
        for obj in objectsToAnimate:
            obj.update()

        checkOnQbertLanding()
        checkOnBallLanding()
        checkOnCoilyLanding()
        checkOnSamSlickLanding()
        checkOnQbertEnemyCollision()

        spawnEnemies()
    else:
        animateCounter += 1
        if animateCounter>50:
            animateCounter = 0
            animateLive = True

    if qbert.IAmOnPlatform:
        for p in listOfPlatforms:
            if 3==p.myDirection:
                objectsToDraw.remove(p)
                objectsToAnimate.remove(p)
                listOfPlatforms.remove(p)
                qbert.targetSquare = (0,0)
                qbert.IAmOnPlatform = False
                break
            
    if levelCleared():
        global currentLevel
        currentLevel+= 1
        resetLevel()

    if scoreboard.gameOver:
        resetLevel()
        scoreboard.resetGame()

                
#------ gameLoop
# Run the game!
# Check for events, animate and refresh
def gameLoop(checkEvents=True, animateObjects=True, refreshScreen=True):
    while(True):
        clock.tick(FRAMERATE)
        if (checkEvents):
            readEvents(pygame.event.get())
        if (animateObjects):
            animateStep()
        if (refreshScreen):
            updateScreen()
            
#======================= Start Program ====================    
initialize()
updateScreen()

gameLoop(True,True,True)



