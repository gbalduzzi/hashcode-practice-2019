
class PizzaSlicing:
    pizza = []
    slices = []

    score = 0

    R = 0
    C = 0
    L = 0
    H = 0

    r = 0
    c = 0
    width = 0
    height = 0

    countT = 0
    countM = 0

    endReached = False

    def __init__(self, pizza, R, C, L, H):
        self.pizza = pizza
        self.R = R
        self.C = C
        self.L = L
        self.H = H
        self.slices = []

    def isActualSliceValid(self):
        if self.width * self.height > H:
            return False

        if self.countT >= L and self.countM >= L:
            return True

        return False

    def setSliceUsed(self, r0, c0, rFinal, cFinal):
        for i in range(r0, rFinal + 1):
            for j in range(c0, cFinal + 1):
                self.pizza[i][j] = 'X'

    def appendActualSlice(self):
        if debug:
            print("Appending slice r:{} c:{} w:{} h:{}".format(self.r, self.c, self.width, self.height))
        self.score += self.width * self.height

        self.slices.append([self.r, self.c, self.r + self.height - 1, self.c + self.width - 1, self.countT, self.countM])
        self.setSliceUsed(self.r, self.c, self.r + self.height - 1, self.c + self.width - 1)

    def updateSlice(self, slice):
        if debug:
            print("update slice r:{} c:{} w:{} h:{}".format(self.r, self.c, self.width, self.height))
        self.score -= (slice[2] - slice[0] + 1) * (slice[3] - slice[1] + 1)

        self.score += self.width * self.height
        self.setSliceUsed(self.r, self.c, self.r + self.height - 1, self.c + self.width - 1)

        slice[0] = self.r
        slice[1] = self.c
        slice[2] = self.r + self.height - 1
        slice[3] = self.c + self.width - 1
        slice[4] = self.countT
        slice[5] = self.countM

    def findNextSliceStart(self, offset):
        if directions[0] == 'right':
            self.findNextSliceAtRight(offset)
        elif directions[0] == 'down':
            self.findNextSliceAtDown(offset)

    def findNextSliceAtDown(self, offset):
        self.r += offset

        while True:
            if self.r >= self.R:
                self.c = self.c + 1
                self.r = 0

            if self.c >= self.C:
                self.endReached = True
                self.r = None
                self.c = None
                break

            if self.pizza[self.r][self.c] != 'X':
                break
            else:
                self.r += 1

    def findNextSliceAtRight(self, offset):
        self.c += offset
        while True:
            if self.c >= self.C:
                self.r = self.r + 1
                self.c = 0

            if self.r >= self.R:
                self.endReached = True
                self.r = None
                self.c = None
                break

            if self.pizza[self.r][self.c] != 'X':
                break
            else:
                self.c += 1

    def setObjectsFromSlice(self, slice):
        self.r = slice[0]
        self.c = slice[1]
        self.height = slice[2] - self.r + 1
        self.width = slice[3] - self.c + 1
        self.countT = slice[4]
        self.countM = slice[5]

    def expandSlices(self):
        for slice in self.slices:
            self.setObjectsFromSlice(slice)

            # Provo ad espandere
            while True:
                upResult = self.goUp(False)
                if upResult == "Valid":
                    continue

                leftResult = self.goLeft(False)
                if leftResult == "Valid":
                    continue
                rightResult = self.goRight(False)
                if rightResult == "Valid":
                    continue

                downResult = self.goDown(False)
                if downResult == "Valid":
                    continue
                # Se arrivo qui significa che non posso più espandermi ne a destra ne a sinistra
                # se serve aggiorno la slice
                if self.countT != slice[4] or self.countM != slice[5]:
                    self.updateSlice(slice)
                break

    def goRight(self, append=True):
        canGoRight = (self.width + 1) * self.height <= H and self.c + self.width < self.C
        addedT = 0
        addedM = 0
        if canGoRight:
            for i in range(self.r, self.r + self.height):
                if pizza[i][self.c + self.width] == 'X':
                    canGoRight = False

                if pizza[i][self.c + self.width] == 'M':
                    addedM += 1
                if pizza[i][self.c + self.width] == 'T':
                    addedT += 1

        if canGoRight:
            self.countM += addedM
            self.countT += addedT
            self.width += 1

            if self.isActualSliceValid():
                if append:
                    self.appendActualSlice()
                    self.findNextSliceStart(self.width if directions[0] == 'right' else self.height)
                return "Valid"

            return "True"
        return "False"

    def goLeft(self, append=True):
        canGoLeft = (self.width + 1) * self.height <= H and self.c - 1 >= 0
        addedT = 0
        addedM = 0
        if canGoLeft:
            for i in range(self.r, self.r + self.height):
                if pizza[i][self.c - 1] == 'X':
                    canGoLeft = False

                if pizza[i][self.c - 1] == 'M':
                    addedM += 1
                if pizza[i][self.c - 1] == 'T':
                    addedT += 1

        if canGoLeft:
            self.countM += addedM
            self.countT += addedT
            self.width += 1
            self.c = self.c-1

            if self.isActualSliceValid():
                if append:
                    self.appendActualSlice()
                    self.findNextSliceStart(-1)
                return "Valid"

            return "True"
        return "False"

    def goDown(self, append=True):
        canGoDown = self.width * (self.height+1) <= self.H and self.r + self.height < self.R
        addedT = 0
        addedM = 0
        if canGoDown:
            for i in range(self.c, self.c + self.width):
                if pizza[self.r + self.height][i] == 'X':
                    canGoDown = False

                if pizza[self.r + self.height][i] == 'M':
                    addedM += 1
                if pizza[self.r + self.height][i] == 'T':
                    addedT += 1

        if canGoDown:
            self.countM += addedM
            self.countT += addedT
            self.height += 1

            if self.isActualSliceValid():
                if append:
                    self.appendActualSlice()
                    self.findNextSliceStart(self.width if directions[0] == 'right' else self.height)
                return "Valid"

            return "True"
        return "False"

    def goUp(self, append=True):
        canGoUp = self.width * (self.height+1) <= self.H and self.r > 0
        addedT = 0
        addedM = 0
        if canGoUp:
            for i in range(self.c, self.c + self.width):
                if pizza[self.r - 1][i] == 'X':
                    canGoUp = False

                if pizza[self.r - 1][i] == 'M':
                    addedM += 1
                if pizza[self.r - 1][i] == 'T':
                    addedT += 1

        if canGoUp:
            self.countM += addedM
            self.countT += addedT
            self.height += 1
            self.r = self.r-1

            if self.isActualSliceValid():
                if append:
                    self.appendActualSlice()
                    self.findNextSliceStart(-1)
                return "Valid"

            return "True"
        return "False"


fileNames = ['a', 'b', 'c', 'd']

objects = []

debug = False

directions = ['down', 'right']

for fileName in fileNames:
    print("--- START FILE {} ---".format(fileName))

    inputFileName = 'in/{}.in'.format(fileName)
    outputFileName = 'out/{}.out'.format(fileName)

    inFile = open(inputFileName, 'r')
    outFile = open(outputFileName, 'w')

    R, C, L, H = map(int, inFile.readline().split())

    print("R:{} C:{} L:{} H:{}".format(R, C, L, H))

    # INPUT PARSER
    pizza = []
    for line in inFile.readlines():
        pizza.append(list(line.strip()))

    ps = PizzaSlicing(pizza, R, C, L, H)
    objects.append(ps)

    # Nuova iterazione ad ogni slice trovata
    while ps.r is not None and ps.c is not None:
        if debug:
            print("------------- \n new slice r:{} c:{}".format(ps.r, ps.c))
        ps.width = 1
        ps.height = 1
        ps.countM = 0
        ps.countT = 0

        if ps.pizza[ps.r][ps.c] == 'M':
            ps.countM += 1
        elif ps.pizza[ps.r][ps.c] == 'T':
            ps.countT += 1

        # Itero fino a quando non trovo una fetta
        while True:
            if debug:
                print("internal w:{} h:{}".format(ps.width, ps.height))

            if directions[0] == 'right':
                firstResult = ps.goRight(True)
            elif directions[0] == 'down':
                firstResult = ps.goDown(True)

            if debug:
                print("firstResult {}".format(firstResult))

            if firstResult == 'Valid':
                break
            if firstResult == 'True':
                continue

            if directions[1] == 'right':
                secondResult = ps.goRight(True)
            elif directions[1] == 'down':
                secondResult = ps.goDown(True)

            if debug:
                print("downResult {}".format(secondResult))
            if secondResult == 'Valid':
                break
            if secondResult == 'True':
               continue

            if firstResult == 'False' and secondResult == 'False':  # Questa slice non funziona

                ps.findNextSliceStart(1)
                break

    ps.expandSlices()

    outFile.write("{}\n".format(len(ps.slices)))
    for slice in ps.slices:
        outFile.write("{} {} {} {}\n".format(slice[0], slice[1], slice[2], slice[3]))

    inFile.close()
    outFile.close()
    print("--- FILE SCORE {} ---".format(ps.score))
    print("--- END FILE {} --- \n \n".format(fileName))

for idx, file in enumerate(fileNames):
    print("-- FILE {} SCORE {} (massimo: {} )".format(file, objects[idx].score, objects[idx].R * objects[idx].C))


