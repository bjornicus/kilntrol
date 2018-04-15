MINUTES = 60
HOURS = 60 * MINUTES

sample_profile = [
    [0, 1174],
    [1 * MINUTES, 2000],
    [65* MINUTES, 2000],
    [70 * MINUTES, 70],
    [2 * HOURS, 70]
]

test_profile = [
    [0, 70],
    [1, 400],
    [15 * MINUTES, 400],
    [15 * MINUTES + 1, 350],
    [20 * MINUTES, 350],
    [30 * MINUTES, 70]
]

candle =[ 
    [0, 70],
    [10 * MINUTES, 200],
    [60 * MINUTES, 200],
    [90 * MINUTES, 150]
]

glaze_profile = [
    [0, 65],
    [2 * HOURS , 550],
    [4 * HOURS , 1000],
    [6 * HOURS , 1900],
    [7 * HOURS , 2010],
    [7 * HOURS + 40 * MINUTES , 2010],
    [8 * HOURS , 2120]
    # [8 * HOURS + 1 * MINUTES, 1200],
    # [10 * HOURS , 1200]
]
