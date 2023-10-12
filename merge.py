with open('transitionTITLE.txt', 'r') as f:
    header = f.readline()
open("final.txt", "w").close()

with open('transition.txt') as file:
    for line in file:
        with open('final.txt', 'a') as f:
            s = header+","+line
            f.write(format(s))