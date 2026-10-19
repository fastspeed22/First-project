import sys
import time

# ---------------------------------------------------------------
# GAME STATE (shared by every function below)
# ---------------------------------------------------------------

name = ""
item = ""
health = 10
mercy = 0           # you need 3 mercy for the white fire (good ending)
gems = False        # True if you stole the gems from the house
followed = False    # True if something followed you out of the outpost
trail_loops = 0     # how many times you have walked the looping forest trail


# ---------------------------------------------------------------
# HELPERS AND REPEATED ENDINGS
# ---------------------------------------------------------------

def pause(seconds=2.5):
    time.sleep(seconds)


def no_health_ending():
    print("You now have 0 health and you lost the game...")
    sys.exit()


def lose_health(amount):
    """Take away health and end the game if it hits 0."""
    global health
    health -= amount
    if health <= 0:
        no_health_ending()


def torch_ending(lit):
    if lit:
        print("You light the torch and a pathway opens")
        pause()
        print("You follow the path")
        pause()
        print("You are greeted by a white light... ")
        pause()
        print("You live")
        pause()
        print("In this lifetime at least...")
    else:
        print("You leave the torch unlit and a pathway opens.")
        pause()
        print("You follow the path")
        pause()
        print("You are greeted by a red light... ")
        pause()
        print("You are consumed by the red light...")
        pause()
        print("You do not survive this lifetime...")


def fall_ending():
    print("You climb the mountain and find a nice place to rest...")
    print("You close your eyes and fall asleep...")
    print("You roll off the mountain and wake up in free fall... ")
    print("You do not survive the fall...")


# ---------------------------------------------------------------
# LAKE -> HOUSE OR RIVER
# ---------------------------------------------------------------

def lake():
    ans = input("Nice, you followed the path and reached a lake... Do you swim across or go around (across/around)? ").lower()
    if ans == "across":
        print("You went across the lake and reached the other side!")
    elif ans == "around":
        print("You went around the lake but tripped and lost 5 health")
        lose_health(5)

    ans = input("You notice a house and a river. Which do you go to (house/river)? ").lower()
    if ans == "house":
        house()
    elif ans == "river":
        river()


# ---------------------------------------------------------------
# HOUSE -> MEADOW OR MOUNTAIN
# ---------------------------------------------------------------

def house():
    global mercy, gems
    ans = input("You go to the house and the owner glares at you. Do you proceed on your journey or take a few gems from his house (leave/gems)? ").lower()
    if ans == "leave":
        print("You leave the house quietly and nod to the owner. You proceed on your way")
        mercy += 1
    elif ans == "gems":
        print("You steal some gems and proceed on your journey. ")
        gems = True

    ans = input("You notice a meadow and a mountain. Which do you go to (meadow/mountain)? ").lower()
    if ans == "meadow":
        meadow()
    elif ans == "mountain":
        mountain()


# ---------------------------------------------------------------
# MEADOW PATHWAY (wolves, then the rock trail or the forest)
# ---------------------------------------------------------------

def meadow():
    if item == "gun" and not gems:
        print("You walk into the meadow to find wolves. You use your gun to shoot them. You are out of ammo.")
        meadow_start()
    elif item == "gun" and gems:
        print("You walk into the meadow to find wolves. You try to use your gun against them but they are not affected.")
        print("They continue to approach you. You notice they have collars. You presume you have something they want. ")
        throw_gems_or_keep()
    else:
        print("You walk into the meadow to find wolves. They attack you and you lose 5 health!")
        lose_health(5)
        if gems:
            print("As they circle you, you notice they have collars. You presume you have something they want. ")
            throw_gems_or_keep()
        else:
            meadow_start()


def throw_gems_or_keep():
    global gems
    ans = input("Do you throw your gems to the wolves or keep them and move on (throw/keep)? ").lower()
    if ans == "throw":
        print("The wolves seem satisfied and you move on without issue. ")
        gems = False
        meadow_start()
    elif ans == "keep":
        print("The wolves approach and they attack you. You lose 5 health.")
        lose_health(5)
        meadow_start()


def meadow_start():
    print("You pass through the meadow and come across two paths...")
    print("One of the trails becomes rocky and rough")
    print("The other leads into a heavily wooded forest")
    ans = input("What do you pick (rock/forest)? ").lower()
    if ans == "rock":
        mineshaft()
    elif ans == "forest":
        forest()


# ---------------------------------------------------------------
# MINESHAFT
# ---------------------------------------------------------------

def mineshaft():
    print("You seem to see what looks like a mineshaft")
    ans = input("Do you enter (yes/no)? ").lower()
    if ans == "yes":
        print("You enter the dimly lit mineshaft.")
        print("You find an old minecart on some rails leading down")
        minecart()
    else:
        mineshaft()


def minecart():
    ans = input("Ride the minecart or push it down (ride/push)? ").lower()
    if ans == "ride":
        print("You ride the cart and it picks up speed and you collide with a cave wall.")
        print("You don't survive.")
    elif ans == "push":
        print("You push the minecart down and the slope of the cave gets steeper and steeper.")
        print("The minecart picks up speed and collides with a wall")
        print("You continue down the path and find a small room")
        ans = input("Do you enter the room or keep walking down the minecart's path (room/path)? ").lower()
        if ans == "room":
            locked_room()
        elif ans == "path":
            print("You come across a ladder leading down deeper into the cave. ")
            ans = input("Do you go down the ladder or back to the room (ladder/room)? ").lower()
            if ans == "room":
                locked_room()
            elif ans == "ladder":
                print("You climb down the ladder to a pit of darkness.")
                print("Once you hit the floor it seems like the ladder disappears.")
                print("You are never found and you never return")


def locked_room():
    print("You enter a candlelit room illuminating many objects commonly used by miners.")
    print("You see an illuminated handle in the candlelight, and you notice it belongs to a thick steel door.")
    pause()
    print("You try to open it and find that it is locked.")
    pause()
    print("You see a big brass key hanging up by the door. You also see a pile of dynamite.")
    ans = input("Do you use the key or the dynamite (key/dynamite)? ").lower()
    if ans == "dynamite":
        print("You use the dynamite to blow open the door and you see a staircase.")
        pause()
        print("As you are about to walk down it you hear a soft rumble and the roof collapses on you.")
        pause()
        print("You are killed")
    elif ans == "key":
        print("You place the key into the door and it opens, stirring up a massive amount of built-up dust.")
        pause()
        print("You see a staircase and slowly descend through the darkness")
        pause()
        print("You see a small amount of light as you are reaching the bottom and come across a clearing in the shining sun")
        pause()
        print("You survive the forest")


# ---------------------------------------------------------------
# FOREST (three paths: the red light, the trail that loops, the whispers)
# ---------------------------------------------------------------

def forest():
    print("You start to walk down the forest as you hear soft whispers of", name, "ringing out into the air")
    ans = input("Do you go further into the forest or go back (further/back)? ").lower()
    if ans == "further":
        print("You go further into the woods and come across three paths.")
        forest_fork()
    elif ans == "back":
        forest_fork()


def forest_fork():
    print("One path follows a faint red light lining the trees...")
    print("Another continues on the trail you were previously on...")
    print("The final path leads down a faint trail in which the whispers are getting louder and louder...")
    ans = input("Which path do you pick (light/trail/whispers)? ").lower()
    if ans == "light":
        red_light()
    elif ans == "trail":
        forest_trail()
    elif ans == "whispers":
        whispers()


def forest_trail():
    global trail_loops
    trail_loops += 1
    if trail_loops == 1:
        print("You keep following the trail as the trees close in around you...")
        print("After a while you pass a twisted tree with a deep scratch in its bark.")
        print("You are sure you have seen it before, but the trail keeps going, so you keep walking.")
        pause()
        print("The trail curves... and you are standing at the three paths again.")
        forest_fork()
    elif trail_loops == 2:
        print("This time you count your steps. You pass the twisted tree again, and the scratch looks deeper.")
        print("There are new scratches beside it, like someone was counting too...")
        pause()
        print("The trail bends back, and you are standing at the three paths again.")
        forest_fork()
    else:
        print("The third time, the trail does not curve back.")
        print("The scratches on the twisted tree are your name, over and over.")
        pause()
        print("When you expect to find the crossroads, you do not reach it.")
        print("You keep walking down the trail and you pass the tree again")
        pause()
        print("The scratches go deeper and deeper with at least 20 more marks in it.")
        print("You don't remember putting them all there")
        print("You come across a clearing")
        mineshaft()


def red_light():
    print("You follow the red light deeper into the forest. ")
    print("You become uneasy but swallow your fear and continue on")
    pause()
    print("As you walk through the forest everything becomes dark except for the faint glow of red.")
    pause()
    print("You come across a stone that is glowing red")
    pause()
    print("You can feel the power emanating from it")
    ans = input("Do you touch the stone or destroy it (touch/destroy)? ").lower()
    if ans == "touch":
        print("You reach toward the glowing surface.")
        print("The moment your fingers touch the stone,")
        print("every sound in the forest disappears.")
        print("The red cracks flare with blinding light.")
        pause()
        print("You try to pull away, but your hand will not move.")
        pause()
        print("Images flash through your mind:")
        pause()
        print("Those before you consumed by the darkness")
        pause()
        print("Those before you taken by the crimson light")
        pause()
        print("Those before you, killed by bad decisions")
        pause()
        print("You finally understand.")
        pause()
        print("The voices are from everyone who touched the stone before you.")
        pause()
        print("The clearing falls silent.")
        pause()
        print("The crimson light dims.")
        pause()
        print("Everything goes black")
        pause()
        print("Somewhere among the trees, a new whisper begins.")
    elif ans == "destroy":
        print("You pick up a heavy rock and strike the stone.")
        pause()
        print("A sharp crack echoes through the clearing.")
        pause()
        print("A thin red fracture appears across its surface.")
        pause()
        print("The ground trembles beneath your feet.")
        pause()
        print("You strike it again.")
        pause()
        print("The crack spreads.")
        pause()
        print("Crimson light pours from the stone.")
        pause()
        print("One final strike shatters the stone.")
        pause()
        print("A wave of red light rushes out of the stone")
        pause()
        print("The stone releases a blinding white light which fills the forest")
        pause()
        print("The roots recoil into the earth.")
        pause()
        print("The branches stop moving.")
        pause()
        print("The whispers dissolve into the wind.")
        pause()
        print("For several moments, you stand in silence.")
        pause()
        print("You start hearing things you forgot you heard while in the forest")
        pause()
        print("You start to hear birds singing")
        pause()
        print("You hear the wind rustling the trees. ")
        pause()
        print("You know the forest was restored to its usual self. ")
        pause()
        print("However the stone corrupts you and with the red light you fade with it. ")
        pause()
        print("The red light consumes you. ")


def whispers():
    print("You follow the trail until the whispers stop being whispers and start being words...")
    pause()
    print('"' + name + '..."')
    pause()
    print('"...you came the same way as the others..."')
    ans = input("Do you listen closer or turn away (listen/turn)? ").lower()
    if ans == "turn":
        print("You turn away, but the whispers follow you back to the three paths...")
        forest_fork()
    elif ans == "listen":
        print('"...one of us climbed out through the old shaft... the foreman..."')
        pause()
        print('"...he crossed the rope bridge, looking for help..."')
        pause()
        print('"...he found an outpost..."')
        pause()
        print('"...he went into a place no one should ever go..."')
        pause()
        print('"...he was stalked by something..."')
        pause()
        print('"...the dark is hungry... it likes taking people... only light holds it back... and the light remembers who answered... and who walked away..."')
        pause()
        print('"...he is not the only one still in the dark..."')
        print('"...our lanterns burned red before the end..."')
        pause()
        print('"...do not follow the red lights, ' + name + '... they are not us anymore..."')
        pause()
        print('"...find the mine..."')
        forest_fork()


# ---------------------------------------------------------------
# MOUNTAIN -> HIKER -> TRAIL (ruins) OR BRIDGE (outpost)
# ---------------------------------------------------------------

def mountain():
    global health
    if item != "key":
        fall_ending()
        return

    print("You climb the mountain and find a chest.")
    print("You use the key to open the chest and find bandages. You use the bandages to heal 10 health!")
    health += 10
    ans = input("Do you want to keep climbing the mountain and rest (climb/rest)? ").lower()
    if ans == "climb":
        injured_hiker()
    elif ans == "rest":
        fall_ending()


def injured_hiker():
    global health, mercy
    print("As you climb, you find an injured hiker slumped against a rock, clutching a bleeding leg.")
    ans = input("He looks up at you and weakly begs for help. Do you give him your bandages or keep climbing (give/keep)? ").lower()
    if ans == "give":
        print("You unwrap the bandages from your own wounds and wrap them around his leg. You lose 15 health...")
        health -= 15
        mercy += 1
        if health <= 0:
            print("After wrapping his bandages you move on and your vision slowly fades. You fall to the ground knowing you saved him but not yourself.")
            sys.exit()
        print("He thanks you quietly and you continue on.")
    elif ans == "keep":
        print("You look away and keep climbing. His voice fades behind you...")

    print("You keep hiking the mountain and you see two paths")
    ans = input("One path leads to a rope bridge and the other leads further down the trail. Which do you take (bridge/trail)? ").lower()
    if ans == "trail":
        ruins_trail()
    elif ans == "bridge":
        outpost()


def ruins_trail():
    print("You keep hiking the trail and find a passage that seems to be covered by a massive boulder. You try to move the boulder but it is very heavy. You move it but also lose 5 health")
    lose_health(5)
    ans = input("The passage leads to a sight of ruins. Do you want to explore the ruins or keep walking (explore/walk)? ").lower()
    if ans == "explore":
        print("You explore the ruins and find a dark passage lit by torches.")
        ans = input("Do you want to go down the passage or keep walking (passage/walk)? ").lower()
        if ans == "passage":
            ans = input("You find a room lit with torches with one torch not lit. Do you light it? (yes/no) ").lower()
            if ans == "yes":
                torch_ending(True)
            elif ans == "no":
                torch_ending(False)


# ---------------------------------------------------------------
# OUTPOST (the door, the hands, and what follows you)
# ---------------------------------------------------------------

def outpost():
    global mercy
    print("You cross the rope bridge and find a small abandoned wooden outpost.")
    ans = input("Do you want to explore the outpost or keep walking (explore/walk)? ").lower()
    if ans == "explore":
        print("You explore the outpost and find a trapped door with a whimpering voice begging for help. ")
        ans = input("Do you want to open the door or keep walking (open/leave)? ").lower()
        if ans == "open":
            mercy += 1  # you opened it right away to help the voice
            open_door()
        elif ans == "leave":
            left_door_closed()
    elif ans == "walk":
        print("You decide not to go into the outpost and keep walking.")
        print("Behind you, strange sounds start coming from the outpost... scratching, then something that almost sounds like laughing.")
        print("You don't know what it is, and you don't turn around to find out.")
        continue_story()


def left_door_closed():
    print("You turn away from the door and leave the outpost.")
    print("The voice stops begging... and everything goes quiet.")
    print("You keep walking, but you can't shake the feeling that you left someone behind...")
    print("The guilt weighs on you with every step...")
    ans = input("Do you want to go back to the outpost and open the door or keep walking (back/walk)? ").lower()
    if ans == "back":
        print("You turn around and walk back to the outpost. The door is right where you left it...")
        # no mercy for coming back: feeling guilty is not the same as showing mercy
        open_door()
    elif ans == "walk":
        print("You push the guilt down and keep walking...")
        continue_story()


def open_door():
    global followed
    print("You open the door and are taken aback as two pale contorted hands start to crawl out of the door. You are frozen in fear as the hands reach for you to pull you into the darkness...")
    ans = input("Do you want to fight, run, or hide (fight/run/hide)? ").lower()
    if ans == "fight":
        print("You try to fight the hands but they get a hold of you and pull you into the darkness...")
        print("You do not survive the encounter...")
    elif ans == "hide":
        print("You hide behind a nearby crate and you feel the presence of the hands crawling around you.")
        print("The hands find you and pull you into the darkness...")
        print("You do not survive the encounter...")
    elif ans == "run":
        print("You run away from the hands and escape the outpost.")
        print("You continue on your journey but you feel a presence following you...")
        ans = input("Do you want to keep walking or go back to the outpost (walking/back)? ").lower()
        if ans == "back":
            print("You go back to the outpost and find the hands waiting for you. They pull you into the darkness...")
            print("You do not survive the encounter...")
        elif ans == "walking":
            print("You keep walking and try not to look back...")
            print("But at night, you hear something moving just outside the light of your fire...")
            print("Whatever followed you out of the outpost has not given up on you...")
            followed = True
            continue_story()


def safe_ending():
    print("You keep walking and find a clearing that marks the barrier of the forest. Whatever was behind you stays behind you.")
    print("You survive and live to see another day...")


def continue_story():
    """Every outpost path that survives ends up here."""
    if followed:
        confrontation()
    else:
        safe_ending()


# ---------------------------------------------------------------
# THE FIRE: mercy decides the color
# You need 3 mercy for the white fire (the good ending). Mercy comes from:
#   1. leaving the house without stealing the gems
#   2. giving the injured hiker your bandages
#   3. opening the outpost door right away (not coming back to it later)
# ---------------------------------------------------------------

def confrontation():
    print("Night falls quickly and the presence of the darkness is closing on you")
    ans = input("Do you make camp and build a fire or keep walking (walking/fire)? ").lower()
    if ans == "walking":
        print("You keep walking into the dark forest and feel something get closer and closer...")
        print("As you walk you feel hands grab you...")
        print("You do not survive the encounter...")
    elif ans == "fire":
        print("You gather branches and build a fire at the edge of the trees.")
        print("The thing that followed you stops at the very edge of your camp, just outside the light...")
        ans = input("Do you pull a burning branch from the fire or stay by the fire (torch/stay)? ").lower()
        if ans == "stay":
            print("You stay where you are, and the fire shrinks as the thing steps closer...")
            print("The light dies, and the cold hands grab you...")
            print("You do not survive the encounter...")
        elif ans == "torch":
            print("You pull a burning branch from the fire and hold it out in front of you.")
            pause()
            print("The flame shudders... and changes color...")
            pause()
            if mercy >= 3:
                print("The flames burn into a bright blinding white light...")
                pause()
                print("The creature howeles into the night as you see it take a step back.")
                pause()
                print("You see a shadow moving away as you hold the light high.")
                pause()
                print("You stand there holding the torch until the sun rises")
                pause()
                print("By the morning the forest feels normal and you continue down the trail")
                pause()
                print("You truly survive something no one else could.")
            else:
                print("The flames start burning a slow deep red.")
                pause()
                print("The torch disintegrates from your hand, burning you. ")
                pause()
                print("The light from the fire slowly starts to fade. ")
                pause()
                print("The shadows from the edge of the forest grow larger and larger until the darkness consumes you.")
                pause()
                print("You feel cold hands grab you and pull you deeper into the forest")
                pause()
                print("You do not survive this encounter...")


# ---------------------------------------------------------------
# RIVER -> CAVE OR VILLAGE
# ---------------------------------------------------------------

def river():
    if item == "plank":
        ans = input("You go to the river and use the plank to cross safely. You continue on the path and find a cave. Do you enter or keep walking (enter/walk)? ").lower()
        if ans == "enter":
            cave()
        elif ans == "walk":
            village()
    else:
        print("You go to the river and fall in... You lose")


def cave():
    ans = input("You enter the cave and see two paths. One goes deeper into the cave and the other goes up to the surface. Which do you take (deeper/up)? ").lower()
    if ans == "deeper":
        ans = input("You go deeper into the cave and find a path leading down a ladder into a dark abyss and a path leading to torch light. Which do you take (ladder/torch)? ").lower()
        if ans == "ladder":
            print("You climb down to the darkness and are consumed by it.")
            print("You are never found.")
            print("You never climb back up...")
        elif ans == "torch":
            print("You walk into a dimly lit room with torches lining the walls.")
            ans = input("The middle torch is not lit. Do you light it or leave it (light/leave)? ").lower()
            if ans == "light":
                torch_ending(True)
            elif ans == "leave":
                torch_ending(False)
    elif ans == "up":
        cliff()


def cliff():
    print("You return to the surface of the cave and find a massive cliff on the other side.")
    print("The cave passage closes behind you and you are trapped.")
    ans = input("Do you jump off the cliff or wait for help (jump/wait)? ").lower()
    if ans == "jump":
        print("You jump off the cliff")
        print("You do not survive the fall...")
    elif ans == "wait":
        print("You wait for help")
        print("No one comes to your aid...")
        print("You do not survive...")


def village():
    print("You keep walking and find a village.")
    ans = input("Do you want to explore the village or keep walking (explore/walk)? ").lower()
    if ans == "explore":
        print("You learn that the villagers have a tradition they do every night. They invite you to join them.")
        ans = input("Do you want to join them or decline (join/decline)? ").lower()
        if ans == "join":
            print("You join the villagers and they initiate you.")
            pause(2)
            print("You are now one of them")
            pause(2)
            print("You are never seen again...")
        elif ans == "decline":
            print("You decline the invitation")
            pause(2)
            print("The villagers do not like your response")
            pause(2)
            print("You are never seen again...")
    elif ans == "walk":
        print("You keep walking to find a bumpy path that is thick in forest with occasional animal skulls")
        ans = input("Do you want to keep walking or turn back (keep/turn)? ").lower()
        if ans == "keep":
            print("You encounter village tribesmen who are not happy to see you")
            print("You do not survive the encounter...")
        elif ans == "turn":
            print("You turn back and keep walking for what seems like hours")
            print("You do not escape the forest")


# ---------------------------------------------------------------
# THE GAME
# ---------------------------------------------------------------

print("Welcome to the Game!")
name = input("What is your name? ")
while True:
    try:
        age = int(input("What is your age? "))
        break
    except ValueError:
        print("Please enter your age as a number.")

print("Hello", name, "you are", age, "years old")

if age < 13:
    print("You are not old enough to play!")
    sys.exit()

print("You are old enough!")
want_to_play = input("Do you want to play? (yes/no) ").lower()
if want_to_play == "yes":
    print("Let's Play!")
    print("You are starting with", health, "health")

    while item not in ("plank", "gun", "key"):
        item = input("Pick an item (plank/gun/key): ").lower().strip()

    left_or_right = input("First choice... Left or Right (left/right)? ").lower()
    if left_or_right == "left":
        lake()
    elif left_or_right == "right":
        print("You fell off a cliff and died...")
elif want_to_play == "no":
    print("See you later...")
