import os
import src.map as Map 
import src.input as Input
import src.troops as Troops
import replay as Replay
import time 

isReplay = False
replayFrame = 0
replayData = []
inputData = []

print("Enter 1 to start game")
print("Enter 2 to replay a game")
choice = input()
if choice == '2':
    inputData = Replay.replays()
    isReplay = True

for i in range(1,4):

    # Make map
    M = Map.map(100, 40)

    # Make townhall
    M.spawn_townhall()

    # Make huts
    M.spawn_huts()

    # Make cannons
    M.spawn_cannons(i)

    # Make wizard towers
    M.spawn_wizTowers(i)

    # Make walls
    M.spawn_walls()

    M.create_spells()

    if choice == "2":
        ch = inputData[replayFrame].split('\n')[0]
        replayFrame += 1
    elif choice == "1":
        os.system("clear")
        print("Level " + str(i))
        print()
        print("Enter 1 to play barbarian king")
        print("Enter 2 to play archer queen")
        ch = input()
        replayData.append(ch)
    
    if ch == "1":
        hero = "K"
        M.spawn_king()
    elif ch == "2":
        hero = "Q"
        M.spawn_queen()

    # Display loop for displaying the map
    while True:
        M.move_barbarians()
        M.move_archers()
        M.move_balloons()
        M.shoot_cannons() 
        M.shoot_wizTowers()
        M.curFrame += 1

        os.system('clear')
        M.display(i)
        if M.troops["K"] != []:
            M.troops["K"][0].print_healthbar()

        if M.troops["Q"] != []:
            M.troops["Q"][0].print_healthbar()

        if M.gameState == "Win":
            print("Level completed!")
            if i ==  3:
                print("You win!")
            time.sleep(2)
            break  
        elif M.gameState == "Lose":
            print("You lose!")
            time.sleep(2)
            break
        elif M.gameState == "Quit":
            break
        # Check if user pressed a key
        key = ""
        if isReplay == False:
            key = Input.getInput(M.timeout)
            replayData.append(key)
        else:
            key = inputData[replayFrame].split('\n')[0]
            replayFrame += 1
            time.sleep(0.35)
        
        if Troops.barbarian.numBarbs < Troops.barbarian.maxBarbs:
            if key == '1':
                M.spawn_barbarian(0) 
            elif key == '2':
                M.spawn_barbarian(1)
            elif key == '3':
                M.spawn_barbarian(2)
        if Troops.archer.numArchs < Troops.archer.maxArchs:
            if key == '4':
                M.spawn_archer(0) 
            elif key == '5':
                M.spawn_archer(1)
            elif key == '6':
                M.spawn_archer(2)
        if Troops.balloon.numLoons < Troops.balloon.maxLoons:
            if key == '7':
                M.spawn_balloon(0) 
            elif key == '8':
                M.spawn_balloon(1)
            elif key == '9':
                M.spawn_balloon(2)
        if M.troops[hero] != []:
            if key == 'w':
                if M.isRage:
                    M.troops[hero][0].move(M,{"x": 0, "y": -1})
                M.troops[hero][0].move(M,{"x": 0, "y": -1})
            elif key == 'a':
                if M.isRage:
                    M.troops[hero][0].move(M,{"x": -1, "y": 0})
                M.troops[hero][0].move(M,{"x": -1, "y": 0})
            elif key == 's':
                if M.isRage:
                    M.troops[hero][0].move(M,{"x": 0, "y": 1})
                M.troops[hero][0].move(M,{"x": 0, "y": 1})
            elif key == 'd':
                if M.isRage:
                    M.troops[hero][0].move(M,{"x": 1, "y": 0})    
                M.troops[hero][0].move(M,{"x": 1, "y": 0})
            elif key == ' ':
                M.troops[hero][0].prep_attack(M)
            elif key == 'r':
                M.rageSpell.activate(M)
            elif key == 'h':
                if not M.healSpell.isActivated:
                    M.healSpell.activate(M)
            elif key == 'l' and not M.isLeviathan:
                M.isLeviathan = True
                M.troops["K"][0].leviathan = True
                M.troops["K"][0].leviathanFrame = M.curFrame
        if key == 'q':
            M.gameState = "Quit"

        if M.isRage:
            if M.curFrame - M.rageSpell.startFrame >= M.rageSpell.duration:
                M.rageSpell.deactivate(M)

        if hero == "K" and M.troops["K"][0].leviathan:
            if M.curFrame - M.troops["K"][0].leviathanFrame >= M.troops["K"][0].leviathanDuration:
                M.troops["K"][0].leviathan = False

    if M.gameState == "Quit" or M.gameState == "Lose":
        break

    del M
    Troops.archer.numArchs = 0
    Troops.barbarian.numBarbs = 0
    Troops.balloon.numLoons = 0
    
if inputData == []:
    Replay.saveToFile(replayData)





