import random


def get_random_colors():
    colors = ["white", "red", "green", "blue", "yellow", "pink",
              "cyan", "lime green", "saddle brown", "orange", "gray", "purple"]
    colors.extend(colors)

    random.shuffle(colors)

    return [colors[i:i+6] for i in range(0, 19, 6)]
