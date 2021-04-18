import time, pygame, random

#initialize pygame engine
pygame.init()
pygame.mixer.init()

size = width, height = (600, 700)
game_dispay = pygame.display.set_mode(size)
pygame.display.set_caption("Flappy")

#initialise parameters
a = 150
push = -170
fps = 30
vely = 0
pip_speed = 1.5
start_x = width * 0.1
start_y = height * 0.2
gap_pip = 200
pip_space = 350
scoreboard_file = "scoreboard.txt"
max_name_length = 25
background_speed = 0.5

black = (0,0,0)
white = (255,255,255)
red = (200,0,0)
green = (0,200,0)
gray = (138,138,138)
#bright_red = (255,0,0)
#bright_green = (0,255,0)

gameExit = False
exitkey = False
audio_on = True

#load images and initialize image parameters
birdImg = pygame.image.load('assets/bird.png')
pipUpImg = pygame.image.load('assets/pipe_up.png')
pipDownImg = pygame.image.load('assets/pipe_down.png')
bird_icon = pygame.image.load('assets/bird_icon.png')
background = pygame.image.load('assets/background.jpg')
bird_height = birdImg.get_height()
bird_width = birdImg.get_width()
pip_height = pipUpImg.get_height()
background_width = background.get_width()

#Set game icon
pygame.display.set_icon(bird_icon)

#Load sounds
sounds = {}
sounds['die'] = pygame.mixer.Sound("assets/audio/die.wav")
sounds['hit'] = pygame.mixer.Sound("assets/audio/hit.wav")
sounds['point'] = pygame.mixer.Sound("assets/audio/point.wav")
sounds['wing'] = pygame.mixer.Sound("assets/audio/wing.wav")

#initialize clock
clock = pygame.time.Clock()

#Function to display the bird on the game_dispay at x,y
def bird(x,y):
    '''To display bird on game_dispay at x,y'''
    game_dispay.blit(birdImg,(x,y))

def highscore(score):
    time.sleep(0.3)
    font = pygame.font.SysFont(None, 60)
    TextSurf, TextRect = text_objects("Highscore!!", font, white)
    TextRect.center = ((width/2),(height/2+85))
    game_dispay.blit(TextSurf, TextRect)
    pygame.display.update()
    time.sleep(0.3)

    name = get_name()
    if name!='' and name!='':
        scoreboard = get_scoreboard()
        scoreboard[0][0] = score
        scoreboard[0][1] = name
        scoreboard = sort_scoreboard(scoreboard)
        update_scoreboard(scoreboard)

def get_name():
    current_string = []
    font = pygame.font.SysFont(None, 30)

    while 1:
        pygame.draw.rect(game_dispay, black, (100,height/2+115,400,30))
        pygame.draw.rect(game_dispay, white, (98,height/2+113,400,30))
        current_string = current_string[0:max_name_length]
        TextSurf, TextRect = text_objects("Enter name: "+"".join(current_string), font, black) #position
        game_dispay.blit(TextSurf, (103,(height/2+120)))
        event = pygame.event.poll()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                current_string = current_string[0:-1]
            elif event.key == pygame.K_RETURN:
                break
            elif 97<= event.key <= 122 or event.key == pygame.K_SPACE:
                current_string.append(chr(event.key))
            elif event.key == pygame.K_ESCAPE or event.key == pygame.K_UP:
                current_string = []
                break
        pygame.display.update()
        clock.tick(30)

    TextS, TextR = text_objects("Press Spacebar to continue or escape to exit", font, black)
    TextR.center = (width/2,(height/2+160))
    game_dispay.blit(TextS, TextR)
    pygame.display.update()
    return "".join(current_string)

#Function to display bold text messages on the game_dispay
def message_display(text):
    largeText = pygame.font.SysFont(None, 170)
    TextSurf, TextRect = text_objects(text, largeText, white)
    TextSurfShadow, TextRectShadow = text_objects(text, largeText, black)
    TextRect.center = ((width/2),(height/2))
    TextRectShadow.center = ((width/2)+4,(height/2)+4)
    game_dispay.blit(TextSurfShadow, TextRectShadow)
    game_dispay.blit(TextSurf, TextRect)
    pygame.display.update()

def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

#Funciton to display score or the number of pipes dodged onn the top left corner of the game_dispay
def score(count):
    '''Display the score on the game_dispay on the top left corner'''
    font = pygame.font.SysFont(None, 25)
    font.set_underline(True)
    text = font.render("Score: "+str(count),True,black)
    game_dispay.blit(text,(0,0))

def sort_scoreboard(scoreboard):
    scoreboard = sorted(scoreboard, key=lambda item:int(item[0]))
    return scoreboard

#Get the scoreboard from the scoreboard_file
def get_scoreboard():
    scoreboard = []
    with open(scoreboard_file, 'r') as filehandle:
        for line in filehandle:
            score = line[:-1].split('#')[0]
            name = line[:-1].split('#')[1]
            scoreboard.append([score,name])
    scoreboard = sort_scoreboard(scoreboard)
    return scoreboard

#Update the scoreboard on the scoreboard_file
def update_scoreboard(scoreboard):
    with open(scoreboard_file, 'w') as filehandle:
        for listitem in scoreboard:
            filehandle.write(str(listitem[0])+"#"+str(listitem[1])+"\n")

#Function to display highscores
def display_highscores():
    scoreboard = get_scoreboard()
    x = 210
    pygame.draw.rect(game_dispay, (x,x,x), (width/6,height-415,2*width/3,405))
    font = pygame.font.SysFont(None, 60)
    font.set_underline(True)
    TextSurf, TextRect = text_objects("Highscores:", font, black)
    TextRect.center = ((width/2),(height-385))
    game_dispay.blit(TextSurf, TextRect)

    font = pygame.font.SysFont(None, 30)

    for i in range(0,len(scoreboard)):
        #Display scores
        text = font.render(str(scoreboard[i][0]),True,black)
        game_dispay.blit(text,(3*width/4,height -35 - 35*i))
        #Display names
        text = font.render("{:>2}. ".format(10-i)+str(scoreboard[i][1])[:max_name_length],True,black)
        game_dispay.blit(text,(width/4-30,height -35 - 35*i))

#Call the function when the bird is required to go up as a jump
def keypress():
    global vely
    vely = push

#Function to display pipes. The coordinates passed are w.r.t. the bottom left pixel of the upper pipe viz., pipDownImg
def pipes(x, y):
    '''Display pipes on the game_dispay'''
    game_dispay.blit(pipDownImg,(x, y-pip_height))
    game_dispay.blit(pipUpImg,(x, y + gap_pip))

#Adding a pause functionality
def paused(pause = True):
    message_display("Paused")
    global exitkey
    global gameExit
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                gameExit = True
                pause = False
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_UP or event.key == pygame.K_p or event.key == pygame.K_RETURN):
                pause = False
        clock.tick(10)

#Function to toggle between audio on or mute
def audio_on_off():
    global audio_on
    audio_on = not audio_on
    if audio_on == True:
        for i in sounds:
            sounds[i].set_volume(1)
    else:
        for i in sounds:
            sounds[i].set_volume(0)

#First game_dispay after the game starts
def game_intro():
    global exitkey
    global gameExit
    print("In game_intro()")
    
    game_dispay.blit(background,(0,0))
    game_dispay.blit(background,(background_width,0))
    bird(start_x,start_y)

    #Display the text 'Flappy' in latge fontsize
    largeText = pygame.font.SysFont(None, 170)
    TextSurf, TextRect = text_objects("Flappy", largeText, white)
    TextSurfShadow, TextRectShadow = text_objects("Flappy", largeText, black)
    TextRect.center = ((width/2),(height/7))
    TextRectShadow.center =  ((width/2)+4,(height/7)+9)
    game_dispay.blit(TextSurfShadow, TextRectShadow)
    game_dispay.blit(TextSurf, TextRect)
    #Display the text 'Press Spacebar to Continue' in small fontsize
    smallText = pygame.font.Font('freesansbold.ttf',20)
    TextSurfSmall, TextRectSmall = text_objects("Press Spacebar to Continue", smallText, black)
    TextRectSmall.center = ((width/2),(height/7)+85)
    game_dispay.blit(TextSurfSmall, TextRectSmall)

    display_highscores()


    #update the game_dispay
    pygame.display.update()
    startgame()#
        # clock.tick(15)

#Function to handle what happens when the bird crashes
def crash(score):
    message_display("Crashed!")
    if score > int(get_scoreboard()[0][0]):
        highscore(score)
    time.sleep(1)
    # startgame()

#Loop to stay in game when the bird is crashed
def startgame():
    print("In startgame()")
    global exitkey
    global gameExit
    while not exitkey:
        for event in pygame.event.get():
            if event.type == pygame.KEYUP and (event.key == pygame.K_SPACE or event.key == pygame.K_UP or event.key == pygame.K_RETURN):
                exitkey = True
                gameExit = False
                game_loop()
            if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                exitkey = True
                gameExit = True
        clock.tick(10)

#Start the main loop for the game
def game_loop():
    print("In game_loop()")
    global exitkey
    global gameExit
    global vely
    count = 0 #To keep score count of the number of pipes dodged
    x = start_x
    y = start_y
    vely = 0
    front_pip = 0

    #List to store the initial x and y coordinates of the pipes in 2 lists
    pipy = []
    pipx = []
    #Initialize x coordinates
    pipx.append(width + 100)
    pipx.append(pipx[0] + pip_space)
    pipx.append(pipx[1] + pip_space)
    pipx.append(pipx[2] + pip_space)
    #Initialize y coordinates
    for i in range(0,4):
        pipy.append(random.randrange(100,height-gap_pip-100))


    backgroundx = [0,background_width, 2*background_width, 3*background_width]

    #Game loop
    while not gameExit:
        #Check for any events and initiate their response
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                gameExit = True
                exitkey = True
                break
            elif event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_UP or event.key == pygame.K_RETURN):
                pygame.mixer.Sound.play(sounds['wing'])
                keypress()
            elif (event.type == pygame.KEYDOWN and (event.key == pygame.K_p)) or (event.type == pygame.MOUSEBUTTONUP and 10<mouse[0]<43 and 28<mouse[1]<52):
                paused()
            elif (event.type == pygame.KEYDOWN and (event.key == pygame.K_m)) or (event.type == pygame.MOUSEBUTTONUP and 10<mouse[0]<43 and 65<mouse[1]<99):
                audio_on_off()

        #Change velocity and position of bird
        y = y + vely*(1/fps) + (1/2)*a*(1/(fps*fps))
        vely = vely + a/fps

        #Changes for pipes
        pipx = [x-pip_speed for x in pipx]
        for i in range(0,4):
            pipx[i] -= pip_speed
            if abs(pipx[i])<2:
                pygame.mixer.stop()
                pygame.mixer.Sound.play(sounds['point'])
            if pipx[i]<-100:
                front_pip = (i+1)%4
                pipx[i] = pipx[((i+3)%4)] + pip_space
                pipy[i] = random.randrange(100,height-gap_pip-100)
                count+=1

        #Changes for background
        for i in (0,1,2):
            backgroundx[i] -= background_speed
            if backgroundx[i]<-background_width:
                backgroundx[i] = backgroundx[(i+2)%3] + background_width
            game_dispay.blit(background,(backgroundx[i],0))

        #Changes for pipes positions
        for i in range(0,4):
            pipes(pipx[i],pipy[i])
        bird(x,y)
        score(count)

        #pause button
        pygame.draw.rect(game_dispay, black, (18,30,5,20))
        pygame.draw.rect(game_dispay, black, (28,30,5,20))
        pygame.draw.rect(game_dispay, black, (10,25,30,30),4)

        #Sound button
        pygame.draw.rect(game_dispay, black, (10,65,30,30),4)
        pygame.draw.rect(game_dispay, black, (16,74,4,13))
        pygame.draw.polygon(game_dispay, black, [(23,74),(33,70),(33,89),(23,86)])

        #Check for crashes
        if not gameExit:
            if (y<0 or y+bird_height>height): #Check if it goes out of the game_dispay
                pygame.mixer.stop()
                pygame.mixer.Sound.play(sounds['die'])
                exitkey = False
                crash(count)
                break

            elif (abs(x+bird_width-pipx[front_pip])<3 and (y<pipy[front_pip] or y+bird_height-gap_pip>pipy[front_pip])) or (-bird_width<(x-pipx[front_pip])<100 and (y<pipy[front_pip] or (y+bird_height-gap_pip>pipy[front_pip]))):
                pygame.mixer.stop()
                pygame.mixer.Sound.play(sounds['hit'])
                exitkey = False
                crash(count)
                break

        pygame.display.update() #Update game_dispay
        clock.tick(100) #Set screen flips at 100 fps

game_intro()
pygame.mixer.quit()
pygame.quit()