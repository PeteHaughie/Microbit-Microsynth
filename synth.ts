// MakeCode JavaScript version

let dutyCycle = 75
let cursorXPosMap = [1, 1, 2, 3, 4]
let cursorYPosMap = [0, 1, 2, 3, 3]
let track = 0
let bar = 0
let tempo = 150
let deltaTick = input.runningTime()
let soundmatrix = [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
]
let lightmatrix = [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
]

function playNote(noteId: number) {
    let noteMap = [0, 262, 330, 392, 523]
    if (noteId > 0 && noteId < noteMap.length) {
        music.playTone(noteMap[noteId], 150)
    }
}

input.onButtonPressed(Button.A, function () {
    let [x, y] = getCursor()
    if (lightmatrix[y][x] == 0) {
        lightmatrix[y][x] = 3
        soundmatrix[y][x] = 1 // c1:4
    } else if (lightmatrix[y][x] == 3) {
        lightmatrix[y][x] = 5
        soundmatrix[y][x] = 2 // e:2
    } else if (lightmatrix[y][x] == 5) {
        lightmatrix[y][x] = 7
        soundmatrix[y][x] = 3 // g
    } else if (lightmatrix[y][x] == 7) {
        lightmatrix[y][x] = 9
        soundmatrix[y][x] = 4 // c2:4
    } else {
        lightmatrix[y][x] = 0
        soundmatrix[y][x] = 0
    }
})

input.onButtonPressed(Button.B, function () {
    let [x, y] = getCursor()
    lightmatrix[y][x] = 0
    soundmatrix[y][x] = 0
})

function getCursor(): number[] {
    let accelX = input.acceleration(Dimension.X)
    let accelY = input.acceleration(Dimension.Y)
    let cursorX = Math.clamp(-256, 256, accelX)
    let cursorY = Math.clamp(0, 480, accelY)
    let xIdx = Math.idiv(cursorX, 102) + 2
    let yIdx = Math.idiv(cursorY, 102)
    return [cursorXPosMap[xIdx], cursorYPosMap[yIdx]]
}

basic.forever(function () {
    basic.clearScreen()
    // Draw lightmatrix
    for (let i = 0; i < 4; i++) {
        for (let j = 0; j < 4; j++) {
            if (lightmatrix[i][j] != 0) {
                led.plotBrightness(j + 1, i, lightmatrix[i][j] * 25)
            }
        }
    }
    // Draw cursor
    let [cursorX, cursorY] = getCursor()
    led.plot(cursorX, 4)
    led.plot(0, cursorY)
    led.plotBrightness(cursorX, cursorY, 255)

    // Playback head and timing
    if (input.runningTime() - deltaTick >= tempo) {
        deltaTick = input.runningTime()
        led.plotBrightness(track + 1, bar, 100)
        if (soundmatrix[bar][track] != 0) {
            let noteId = soundmatrix[bar][track]
            control.inBackground(function () {
                playNote(noteId)
            })
        }
        if (track == 3) {
            track = 0
            if (bar == 3) {
                bar = 0
            } else {
                bar += 1
            }
        } else {
            track += 1
        }
        led.plotBrightness(0, 4, 180)
    }
    basic.pause(dutyCycle)
})