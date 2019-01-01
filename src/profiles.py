MINUTES = 60
HOURS = 60 * MINUTES

sample_profile = [
    [0, 1174],
    [1 * MINUTES, 2000],
    [65 * MINUTES, 2000],
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

candle = [
    [0, 70],
    [10 * MINUTES, 200],
    [60 * MINUTES, 200],
    [90 * MINUTES, 150]
]

glaze_profile = [
    [0, 65],
    [2 * HOURS, 550],
    [4 * HOURS, 1000],
    [6 * HOURS, 1900],
    [7 * HOURS, 2010],
    [7 * HOURS + 40 * MINUTES, 2010],
    [8 * HOURS + 30 * MINUTES, 2120],
    [10 * HOURS, 1200]
]

crystal_profile = [
    [0, 65],
    [1 * HOURS, 395],
    [2 * HOURS, 727],
    [3 * HOURS, 1060],
    [4 * HOURS, 1392],
    [6 * HOURS, 1900],
    [7 * HOURS, 2042],
    [7 * HOURS + 45 * MINUTES, 2090],
    [8 * HOURS, 2090],
    [8 * HOURS + 6 * MINUTES, 2042],
    [8 * HOURS + 21 * MINUTES, 2042],
    [14 * HOURS + 30 * MINUTES, 1400]
]
