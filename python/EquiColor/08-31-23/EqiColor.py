import colorsys

def equicolor(points, reference):
    
    #Error Handling
    try:
        isValid = int(points) > 0 and int(points) < 16777216
    except TypeError:
        print("Invalid input.")
        print("Your input was " + str(type(points)) )
        print("Equicolor accepts one integer between 1 and 16777216 and one string for a color reference.")
        return
    try:
        if not isValid:
            raise ValueError
    except ValueError:
        print("Invalid input.")
        print("Your input was " + str(points))
        print("Equicolor accepts one integer between 1 and 16777216 and one string for a color reference.")
    
    #Code Body
    refR = int(reference[1:3],16)/255
    refG = int(reference[3:5],16)/255
    refB = int(reference[5:7],16)/255
    (refH, refL, refS) = colorsys.rgb_to_hls(refR, refG, refB)
    hues = equipoint(refH,1,points)
    colors = []
    for k in range(points):
        hue = hues[k]
        (kR,kG,kB) = colorsys.hls_to_rgb(hue, refL, refS)
        R = ("0"+hex(round(kR*255))[2:])
        G = ("0"+hex(round(kG*255))[2:])
        B = ("0"+hex(round(kB*255))[2:])
        color = "#" + R[len(R)-2:] + G[len(G)-2:] + B[len(B)-2:]
        colors.append(color)
    return(colors)

def equipoint(first, last, n):
    points = []
    for k in range(n):
        point = (last/n)*(k) + first
        if point>=last:
            point = point-last
        points.append(point)
    return points

print(equicolor(360,"FFFFFF"))