DICT = {31599: 0, 29850: 1, 29671: 2, 31143: 3, 18925: 4, 31183: 5, 31695: 6,
        18727: 7, 31727: 8, 31215: 9}


def numeral(pixels):
    step = 1
    sum = 0
    for pixel in pixels:
        sum += pixel * step
        step *= 2
    try:
        return DICT[sum]
    except KeyError:
        return -1


def number(pixels):
    sum = 0
    pixels = [
        [pixels[i] if (i % 15 + 1) % 4 and (i % 15) // 4 == j else -1 for i
         in range(75)] for j in range(4)]
    for i in range(4):
        pixels[i] = list(filter(lambda x: x != -1, pixels[i]))
        num = numeral(pixels[i])
        if num != -1:
            sum = sum * 10 + num
        else:
            break
    return sum
