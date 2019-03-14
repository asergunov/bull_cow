import itertools
import random

digits = [0,1,2,3,4,5,6,7,8,9]
posibles = [a*1000+b*100+c*10+d for a,b,c,d in itertools.permutations(digits, 4)]

def score(n,k):
    b = 0
    sn = str(n).zfill(4)
    sk = str(k).zfill(4)
    for i in range(4):
        if sn[i] == sk[i]:
            b+=1
    c = -b;
    for d in sn:
        i = sk.find(d)
        if i>=0:
            c+=1
            sk = sk[:i]+sk[(i+1):]

    return (b, c)

def randguess():
    N = 0;
    for i in random.sample(digits, 4):
        N *= 10;
        N += i
    return N

class Master:
    def __init__(self):
        self._N = randguess()
            
    def restart(self):
        self._N = randguess()

    def score(self, k):
        '''return self.score_user(k)'''
        return score(self._N, k)

    def score_user(self, k):
        b = int(input("buls for {0:04}: ".format(k)));
        c = int(input("cows for {0:04}: ".format(k)));
        return (b, c)

class ConsolePlayer:
    def setScore(self, _guess, _score):
        pass

    def nextGuess(self):
        return int(input(": "))

class HybridPlayer:
    def __init__(self):
        self.__scores = {}
        self.__posibles = posibles

    def nextGuess(self):
        return int(input(": "))


    def setScore(self, _guess, _score):
        self.__scores[_guess] = _score
        self.__posibles = [i for i in self.__posibles if score(i, _guess) == _score]

    def nextGuess(self):
        print(self.__posibles)
        return input(">")

class Player:
    def __init__(self):
        self.__scores = {}
        self.__posibles = posibles

    def setScore(self, _guess, _score):
        self.__scores[_guess] = _score
        self.__posibles = [i for i in self.__posibles if score(i, _guess) == _score]

    def nextGuess(self):
        print(len(self.__posibles))
        if len(self.__scores) != 0 and len(self.__posibles) > 2:
            bestGuess = 0
            bestGuessPull = 9999
            for n in self.__posibles:
                '''random.sample(posibles, len(posibles))'''
                c = {}
                for k in self.__posibles:
                    _score = score(k,n)
                    if _score in c:
                        c[_score] += 1
                    else:
                        c[_score] = 1

                avg_depth = 0.0;
                for a in c.itervalues():
                    avg_depth += 1.0*a*a
                avg_depth /= len(self.__posibles)

                if avg_depth < bestGuessPull:
                    bestGuessPull = avg_depth
                    bestGuess = n
                    print("bestGuess: {0:04}, bestGuessPull: {1}".format(bestGuess, bestGuessPull))
                    print(c)
            return bestGuess

        return random.sample(self.__posibles, 1)[0]

        return randguess()
        return random.randint(0, 9999)
        return input(">")

class Game:
    def __init__(self, master, player):
        self.__master = master
        self.__player = player

    def play(self):
        done = False
        turn = 0
        self.__master.restart()
        while not done:
            turn+=1
            guess = self.__player.nextGuess()
            score = self.__master.score(guess)
            print('{0}. {1:04d}: {2} buls {3} cows'.format(turn, guess, score[0], score[1]))
            self.__player.setScore(guess, score)
            done = score == (4, 0)
        print("Victory!")


game = Game(Master(), Player())
game.play()



