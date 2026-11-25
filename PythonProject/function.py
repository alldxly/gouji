import random
import itertools
pokedict = {
    '4': 4,
    # '5': 5, '6': 6, '7': 7,
    # '8': 8, '9': 9,
    # '10': 10,'J': 11, 'Q': 12,
    'K': 13, 'A': 14,'2': 15,
    # 'X': 16,'D': 17, 'Y': 18,
    '3': 3,
}
def chushi(num):
    a = 0
    pokelist = []
    while a < num:
        if a == num - 1 and '3' not in pokelist:
            pokelist.append('3')
            break
        b = random.choice(list(pokedict.keys()))
        if b == '3' and '3' in pokelist:
            continue
        pokelist.append(b)
        a += 1
    return pokelist


def removeN(lst, value, n):
    for _ in range(n):
        lst.remove(value)


def replace2(values):
    if 15 in values:
        target = max((v for v in values if v < 15), default=None)
        if target is not None:
            return [target if v == 15 else v for v in values]
    return values


def randomPlay(common, two, wang,dianing):
    playcards = []
    poolno3 = [c for c in common if c != 3]
    if dianing and 4 in poolno3:
        target=4
        allsame = [c for c in poolno3 if c == target]
        playcards.extend(allsame[:len(allsame)])
        return playcards
    if random.randint(0, 1) == 1 and len(poolno3) > 0:
        target = random.choice(poolno3)
        allsame = [c for c in poolno3 if c == target]
        if target==4:
            playcards.extend(allsame[:len(allsame)])
            return playcards
        else:
            playcount = random.randint(1, len(allsame))
            playcards.extend(allsame[:playcount])
    if random.randint(0, 1) == 1 and len(two) > 0:
        count = random.randint(1, len(two))
        playcards.extend(random.sample(two, count))
    if random.randint(0, 1) == 1 and len(wang) > 0:
        count = random.randint(1, len(wang))
        combos = list(itertools.combinations(wang, count))
        playcards.extend(list(random.choice(combos)))

    if not playcards:
        if poolno3:
            target = poolno3[0]
            playcards.extend([c for c in poolno3 if c == target])
        elif len(two) > 0:
            playcards.append(two[0])
        elif len(wang) > 0:
            playcards.append(wang[0])
        elif len(common) > 0 and common[0] == 3:
            playcards.append(3)

    return playcards


def chupai(desk, curhand):
    targetlen = len(desk)
    targetmax = max(desk)
    if targetmax < 15:
        two_count = curhand.count(15)

        for rank in sorted({c for c in curhand if targetmax < c < 15}):
            cnt = curhand.count(rank)
            if cnt + two_count >= targetlen:
                use_rank = min(cnt, targetlen)
                use_two = targetlen - use_rank
                return [rank] * use_rank + [15] * use_two

        # 全 2 也能压普通牌
        if two_count >= targetlen:
            return [15] * targetlen
    for card in sorted(set(curhand)):
        if card==4 and curhand.count(card)!=1:
            continue
        if card > targetmax and card < 15:
            countinhand = curhand.count(card)
            if countinhand >= targetlen:
                return [card] * targetlen

    tempme = curhand.copy()
    tempd = desk.copy()
    playedcards = []
    while len(tempme) > 0 and len(tempd) > 0:
        zuixiao = 0
        for a in tempme:
            if a > tempd[-1]:
                if a>=15 or a in playedcards or len(playedcards)==0:
                    del tempd[-1]
                    zuixiao = a
                else:
                    continue
                break
        if zuixiao:
            tempme.remove(zuixiao)
            playedcards.append(zuixiao)
        else:
            if tempd[-1] < 16:
                return []
            elif tempd[-1] == 16:
                if tempme.count(16) >= 2:
                    del tempd[-1]
                    removeN(tempme, 16, 2)
                    playedcards.extend([16, 16])
                else:
                    return []
            elif tempd[-1] == 17:
                if tempme.count(17) >= 2:
                    del tempd[-1]
                    removeN(tempme, 17, 2)
                    playedcards.extend([17, 17])
                elif tempme.count(16) >= 3:
                    removeN(tempme, 16, 3)
                    del tempd[-1]
                    playedcards.extend([16, 16, 16])
                else:
                    return []
            else:
                if tempme.count(18) >= 2:
                    del tempd[-1]
                    removeN(tempme, 18, 2)
                    playedcards.extend([18, 18])
                elif tempme.count(17) >= 3:
                    removeN(tempme, 17, 3)
                    del tempd[-1]
                    playedcards.extend([17, 17, 17])
                else:
                    return []

    if len(tempd) == 0:
        return playedcards
    return []


def isGouji(cards):
    cardscop=cards.copy()
    cards=replace2(cards)
    if (sum(1 for a in cards if a >= 10) >= 5 or
            sum(1 for a in cards if a >= 11) >= 4 or
            sum(1 for a in cards if a >= 12) >= 3 or
            sum(1 for a in cards if a >= 13) >= 2 or
            sum(1 for a in cards if a >= 14) >= 2 or
            sum(1 for a in cards if a >= 15) >= 1):
        if (sum(1 for a in cardscop if 10 <= a < 15) >= 5 or
            sum(1 for a in cardscop if 11 <= a < 15) >= 4 or
            sum(1 for a in cardscop if 12 <= a < 15) >= 3 or
            sum(1 for a in cardscop if 13 <= a < 15) >= 2) and not any(a >= 15 for a in cardscop):
            dian,gouji=True,True
        else:
            dian,gouji=False,True
    else:
        dian,gouji=False,False
    return dian,gouji

