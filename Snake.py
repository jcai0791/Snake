import simplegui
import random
direction = ""
size = 30
position = [size/2,size/2]
points = []
length = size/5
score = 0
gameflag = False
tick = 1000
choice = 0
bestscore = 0
apple = [random.randint(0,size-1), random.randint(0,size-1)]
while apple in points:
    apple = [random.randint(0,size-1), random.randint(0,size-1)]
def constrain(a, upper, lower):
    if a>upper:
        a = upper
    elif a<lower:
        a = lower
    return a
def opposite(direction):
    if direction == "Down":
        return "Up"
    elif direction == "Up":
        return "Down"
    elif direction == "Left":
        return "Right"
    elif direction == "Right":
        return "Left"
def applereset():
    global apple, points
    apple = [random.randint(0,size-1), random.randint(0,size-1)]
    while apple in points:
        apple = [random.randint(0,size-1), random.randint(0,size-1)]
def reset():
    global points, position, length, apple, score, size, bestscore
    points=[]
    position = [size/2,size/2]
    length = size/5
    if score>bestscore:
        bestscore = score
    score = 0
    direction = "Left"
    applereset()
    
def handlekey(d):
    global direction, gameflag,choice
    if gameflag:
        if d!=opposite(direction):
            direction = d
    else:
        if d=="Down":
            choice=constrain(choice+1,2,0)
        if d=="Up":
            choice=constrain(choice-1,2,0)

# Bug: If the player rapidly presses keys to steer into self
# the game will end even if not shown on screen
def move():
    global direction, position
    if direction == "Up":
        position=[position[0],position[1]-1]
    if direction == "Down":
        position=[position[0],position[1]+1]
    if direction == "Right":
        position=[position[0]+1,position[1]]
    if direction == "Left":
        position=[position[0]-1,position[1]]
def checkgameover():
    global position, size, gameflag, points
    if position[0]>size-1 or position[0]<0 or position[1]>size-1 or position[1]<0:
        gameflag=False
        timer.stop()
        reset()
    if position in points:
        gameflag = False
        timer.stop()
        reset()

def timer_handler():
    global direction, points,apple, score
    global position,size, gameflag, length
    if gameflag:
        move()
        checkgameover()
        points.append(position)
        if len(points)>length:
            points.pop(0)
        if position==apple:
            score = score+1
            length = length+4
            applereset()

def keydown(key):
    global direction, gameflag,choice, tick, size, timer
    if key == 13:  
        direction = "Left"
        if choice ==0:
            size = 20
            tick = 300
        if choice ==1:
            size = 40
            tick = 100
        if choice ==2:
            size = 50
            tick = 75
        reset()
        timer = simplegui.create_timer(tick, timer_handler)
        timer.start()
        gameflag = True
    if key== simplegui.KEY_MAP["down"]:
        handlekey("Down")
    elif key== simplegui.KEY_MAP["up"]:
        handlekey("Up")
    elif key== simplegui.KEY_MAP["right"]:
        handlekey("Right")
    elif key== simplegui.KEY_MAP["left"]:
        handlekey("Left")
def draw(canvas):
    global points,size, length,apple, score,choice, bestscore
    if gameflag==False:
        if choice == 0:
            canvas.draw_polygon([(100,150), (100, 200),(400,200),(400,150)], 20, "Green", "Green")
            canvas.draw_text("Easy",(100,190),50,"Black", "monospace")
        else:
            canvas.draw_text("Easy",(100,190),50,"Green", "monospace")
        if choice ==1:
            canvas.draw_polygon([(100,240), (100, 290),(400,290),(400,240)], 20, "Green", "Green")
            canvas.draw_text("Medium",(100,280),50,"Black", "monospace")
        else:
            canvas.draw_text("Medium",(100,280),50,"Green", "monospace")
        if choice == 2:
            canvas.draw_polygon([(100,330), (100, 380),(400,380),(400,330)], 20, "Green", "Green")
            canvas.draw_text("Hard",(100,370),50,"Black", "monospace")
        else:
            canvas.draw_text("Hard",(100,370),50,"Green", "monospace")
        canvas.draw_text("Snake",(100,100),100,"Green", "monospace")
        canvas.draw_text("Best score: "+str(bestscore),(100,430),30,"Green", "monospace")
    if gameflag:
        canvas.draw_text(str(score),(10,20),20, "Green", "monospace")
        canvas.draw_circle((apple[0]*500/size+250/size, apple[1]*500/size+250/size), 250/size, 1, "Green", "Green")
        for point in points:
            canvas.draw_polygon([(point[0]*500/size,point[1]*500/size),(point[0]*500/size+500/size-2,point[1]*500/size), (point[0]*500/size+500/size-2,point[1]*500/size+500/size-2), (point[0]*500/size,point[1]*500/size+500/size-2)], 1, "Green", "Green")
# Create a frame and assign callbacks to event handlers
frame = simplegui.create_frame("Home", 500, 500)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
# Start the frame animation
frame.start()