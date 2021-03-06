
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

    def actualSlice(self):
        return [self.r, self.c, self.r + self.height - 1, self.c + self.width - 1, self.countT, self.countM]

    def appendActualSlice(self):
        if debug:
            print("Appending slice r:{} c:{} w:{} h:{}".format(self.r, self.c, self.width, self.height))
        self.score += self.width * self.height

        self.slices.append(self.actualSlice())
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
        if rightDown:
            self.findNextSliceAtRight(offset)
        else:
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

    def smallestSliceFromPoint(self):
        smallestSlice = None
        smallestArea = 100000

        goingRight = True

        while True:
            if goingRight:
                rightResult = self.goRight(False)
                if rightResult == "Valid":
                    if self.width * self.height < smallestArea:
                        smallestSlice = self.actualSlice()
                        smallestArea = self.width * self.height
                    goingRight = False
                elif rightResult == "False":
                    goingRight = True
                else:
                    continue


    def goRight(self, append=True):
        canGoRight = (self.width + 1) * self.height <= H and self.c + self.width < self.C
        addedT = 0
        addedM = 0
        if canGoRight:
            for i in range(self.r, self.r + self.height):
                if self.pizza[i][self.c + self.width] == 'X':
                    canGoRight = False

                if self.pizza[i][self.c + self.width] == 'M':
                    addedM += 1
                if self.pizza[i][self.c + self.width] == 'T':
                    addedT += 1

        if canGoRight:
            self.countM += addedM
            self.countT += addedT
            self.width += 1

            if self.isActualSliceValid():
                if append:
                    self.appendActualSlice()
                    self.findNextSliceStart(self.width if rightDown else self.height)
                return "Valid"

            return "True"
        return "False"

    def reduceRight(self):
        if self.width <= 1:
            return

        reducedT = 0
        reducedM = 0

        for i in range(self.r, self.r + self.height):
            if self.pizza[i][self.c + self.width - 1] == 'M':
                reducedM += 1
            if self.pizza[i][self.c + self.width - 1] == 'T':
                reducedT += 1

        self.countM += -reducedM
        self.countT += -reducedT
        self.width = self.width - 1


    def goLeft(self, append=True):
        canGoLeft = (self.width + 1) * self.height <= H and self.c - 1 >= 0
        addedT = 0
        addedM = 0
        if canGoLeft:
            for i in range(self.r, self.r + self.height):
                if self.pizza[i][self.c - 1] == 'X':
                    canGoLeft = False

                if self.pizza[i][self.c - 1] == 'M':
                    addedM += 1
                if self.pizza[i][self.c - 1] == 'T':
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
                if self.pizza[self.r + self.height][i] == 'X':
                    canGoDown = False

                if self.pizza[self.r + self.height][i] == 'M':
                    addedM += 1
                if self.pizza[self.r + self.height][i] == 'T':
                    addedT += 1

        if canGoDown:
            self.countM += addedM
            self.countT += addedT
            self.height += 1

            if self.isActualSliceValid():
                if append:
                    self.appendActualSlice()
                    self.findNextSliceStart(self.width if rightDown else self.height)
                return "Valid"

            return "True"
        return "False"

    def reduceDown(self):
        if self.height <= 1:
            return

        reducedT = 0
        reducedM = 0

        for i in range(self.c, self.c + self.width):
            if self.pizza[self.r + self.height - 1][i] == 'M':
                reducedM += 1
            if self.pizza[self.r + self.height - 1][i] == 'T':
                reducedT += 1

        self.countM += -reducedM
        self.countT += -reducedT
        self.height = self.height - 1

    def goUp(self, append=True):
        canGoUp = self.width * (self.height+1) <= self.H and self.r > 0
        addedT = 0
        addedM = 0
        if canGoUp:
            for i in range(self.c, self.c + self.width):
                if self.pizza[self.r - 1][i] == 'X':
                    canGoUp = False

                if self.pizza[self.r - 1][i] == 'M':
                    addedM += 1
                if self.pizza[self.r - 1][i] == 'T':
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
rightDown = True  # False for downRight

# Inverto righe e colonne in fase di lettura e di scrittura
# basta implementare l'algoritmo nelle direzioni right e down e flippare quando servono top e left per avere
# tutte le direzioni
flipRows = True
flipColumns = False

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
        newRow = list(line.strip())
        if flipColumns:
            newRow = newRow[::-1]

        if flipRows:
            pizza.insert(0, newRow)
        else:
            pizza.append(newRow)

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
        jumpFirst = False
        while True:
            if debug:
                print("internal w:{} h:{}".format(ps.width, ps.height))

            # Non mi espando più nella direzione principale se ho finito di espandermi in quella direzione
            if not jumpFirst:
                if rightDown:
                    firstResult = ps.goRight(True)
                else:
                    firstResult = ps.goDown(True)

                if debug:
                    print("firstResult {}".format(firstResult))

                if firstResult == 'Valid':
                    break
            else:
                firstResult = "False"

            if not rightDown:
                secondResult = ps.goRight(True)
            else:
                secondResult = ps.goDown(True)

            if debug:
                print("downResult {}".format(secondResult))
            if secondResult == 'Valid':
                break

            if firstResult == 'False' and secondResult == 'False':
                # Controllo se posso ridurre la dimensione principale
                if rightDown and ps.width > 1:
                    ps.reduceRight()
                    jumpFirst = True
                    continue
                elif not rightDown and ps.height > 1:
                    ps.reduceDown()
                    jumpFirst = True
                    continue
                else:
                    ps.findNextSliceStart(1)
                    break
            jumpFirst = False

    ps.expandSlices()

    outFile.write("{}\n".format(len(ps.slices)))
    for slice in ps.slices:
        r1 = slice[0] if not flipRows else R - 1 - slice[0]
        r2 = slice[2] if not flipRows else R - 1 - slice[2]
        c1 = slice[1] if not flipColumns else C - 1 - slice[1]
        c2 = slice[3] if not flipColumns else C - 1 - slice[3]
        outFile.write("{} {} {} {}\n".format(r1, c1, r2, c2))

    inFile.close()
    outFile.close()
    print("--- FILE SCORE {} ---".format(ps.score))
    print("--- END FILE {} --- \n \n".format(fileName))

for idx, file in enumerate(fileNames):
    print("-- FILE {} SCORE {} (massimo: {} )".format(file, objects[idx].score, objects[idx].R * objects[idx].C))


