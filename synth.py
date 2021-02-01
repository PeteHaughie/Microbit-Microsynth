from microbit import *
import time
import music

# global vars
dutyCycle = 75

# # #
# Cursor Lookup Arrays
# Using these arrays we don't need to invert any values coming from the
# accelerometer before we can use them on the screen
# # #


cursorXPosMap = [1, 1, 2, 3, 4]
cursorYPosMap = [0, 1, 2, 3, 3]

# # #
# Acculmulators
# bars are columns in each of the rows
# tracks are rows
# think of them as table cells which are read left to right, top to bottom
# # #

track = 0
bar = 0

# # #
# Matrices
#
# The different matrices allow for the reuse of the track and bar
# accumulator values
# # #

# # #
# The Sound Matrix allows us to store the different types of sounds in a
# particular grid reference
# 0 = none
# 1 = bass
# 2 = snare
# 3 = hi-hat
# 4 = clap
# # #

soundmatrix = [
   [0, 0, 0, 0],
   [0, 0, 0, 0],
   [0, 0, 0, 0],
   [0, 0, 0, 0]
]

# # #
# The Light Matrix stores the brightness values of each of the 5x5 lights
# Each instrument has a value 1 brighter than the previous one starting at 3
# bass = 3
# snare = 4
# hi-hat = 5
# clap = 6
# This is so we can always see where the cursor is even if it is in
# an active cell
# # #

lightmatrix = [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
]

# # #
# Tempo
# Finally set the tempo and indicator status
# # #

tempoIndicator_bool = False
tempo = 150
deltaTick = time.ticks_ms()

# loop
while True:
    # clear the display so we can paint new lights where needed
    display.clear()

    # # #
    # Note Position
    # Paint the position from the light matrix and intensity at that position
    # # #

    # set ourself a pair of accumulators for each cycle
    i = 0
    j = 0
    for row in lightmatrix:
        for light in row:
            if light != 0:
                # we offset the x position by 1 so that we can
                # handle the left cursor indicator column
                display.set_pixel(j + 1, i, light)
            j += 1
        j = 0
        i += 1
    i = 0

    # # #
    # Cursor positioning
    # # #

    # I really don't like this so perhaps I should just check ranges instead
    # *shrug*
    accelXPos = accelerometer.get_x()
    if accelXPos >= 256:
        accelXPos = 256
    if accelXPos <= -256:
        accelXPos = -256
    cursorXPos = int(accelXPos / 102.4) + 2
    cursorXPosNow = cursorXPosMap[cursorXPos]
    accelYPos = accelerometer.get_y()
    if accelYPos >= 480:
        accelYPos = 480
    if accelYPos <= 0:
        accelYPos = 0
    cursorYPos = int(accelYPos / 102.4)
    cursorYPosNow = cursorYPosMap[cursorYPos]
    display.set_pixel(cursorXPosNow, 4, 1)
    display.set_pixel(0, cursorYPosNow, 1)
    display.set_pixel(cursorXPosNow, cursorYPosNow, 9)

    # # #
    # Press buttons, get rewards
    # # #

    if button_a.is_pressed():
        if lightmatrix[cursorYPosNow][cursorXPosNow - 1] == 0:
            lightmatrix[cursorYPosNow][cursorXPosNow - 1] = 3
            soundmatrix[cursorYPosNow][cursorXPosNow - 1] = 'c1:4'
        elif lightmatrix[cursorYPosNow][cursorXPosNow - 1] == 3:
            lightmatrix[cursorYPosNow][cursorXPosNow - 1] = 5
            soundmatrix[cursorYPosNow][cursorXPosNow - 1] = 'e:2'
        elif lightmatrix[cursorYPosNow][cursorXPosNow - 1] == 5:
            lightmatrix[cursorYPosNow][cursorXPosNow - 1] = 7
            soundmatrix[cursorYPosNow][cursorXPosNow - 1] = 'g'
        elif lightmatrix[cursorYPosNow][cursorXPosNow - 1] == 7:
            lightmatrix[cursorYPosNow][cursorXPosNow - 1] = 9
            soundmatrix[cursorYPosNow][cursorXPosNow - 1] = 'c2:4'
        else:
            lightmatrix[cursorYPosNow][cursorXPosNow - 1] = 0
            soundmatrix[cursorYPosNow][cursorXPosNow - 1] = 0

    if button_b.is_pressed():
        if lightmatrix[cursorYPosNow][cursorXPosNow - 1] != 0:
            lightmatrix[cursorYPosNow][cursorXPosNow - 1] = 0
            soundmatrix[cursorYPosNow][cursorXPosNow - 1] = 0

    # # #
    # Playback Head positioning
    # # #

    if time.ticks_diff(time.ticks_ms(), deltaTick) >= tempo:
        deltaTick = time.ticks_ms()
        # we add 1 to the x position to allow for the
        # left column cursor indicator
        display.set_pixel(track + 1, bar, 4)

        # # #
        # Play something I guess
        # # #

        # music.stop()

        if soundmatrix[bar][track] != 0:
            music.play(soundmatrix[bar][track])
        # Updates all done? Great! Now increment the track value
        if track == 3:
            track = 0
            if bar == 3:
                bar = 0
            else:
                bar += 1
        else:
            track += 1

        # tempo related features

        # let's light the corner indicator
        display.set_pixel(0, 4, 7)

        if tempo < 50:
            tempo = 50

        if tempo > 500:
            tempo = 500

    # # #
    # Tempo is not duty cycle
    # # #

    sleep(dutyCycle)
