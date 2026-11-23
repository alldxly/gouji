import random
import itertools

pokedict = {
    '2': 15, 'X': 16, 'D': 17, 'Y': 18, '3': 3,
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


def randomPlay(common, two, wang):
    playcards = []
    poolno3 = [c for c in common if c != 3]
    if random.randint(0, 1) == 1 and len(poolno3) > 0:
        target = random.choice(poolno3)
        allsame = [c for c in poolno3 if c == target]
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

    for card in sorted(set(curhand)):
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
                del tempd[-1]
                zuixiao = a
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
    if (sum(1 for a in cards if a >= 10) >= 5 or
            sum(1 for a in cards if a >= 11) >= 4 or
            sum(1 for a in cards if a >= 12) >= 3 or
            sum(1 for a in cards if a >= 13) >= 2 or
            sum(1 for a in cards if a >= 14) >= 2 or
            sum(1 for a in cards if a >= 15) >= 1):
        return True
    return False


num = 10
players = []
for i in range(6):
    team = 'A' if i % 2 == 0 else 'B'
    handstr = chushi(num)
    handval = sorted([pokedict[x] for x in handstr])
    players.append({
        'number': i, 'team': team, 'oppose': (i + 3) % 6,
        'hand': handval, 'common': [c for c in handval if c < 15],
        'two': [c for c in handval if c == 15], 'wang': [c for c in handval if c > 15],
        'rank': None,
        'men': [],
        'mened': None,
        'wutou':False
    })

print("========== 游戏开始 ==========")
for p in players:
    print(f"{p['number']}号 ({p['team']}队) | 对头: {p['oppose']}号 | 手牌: {p['hand']}")


def getNextPlayerForGouji(curidx, activecount):
    p = players[curidx]
    oppidx = p['oppose']

    if activecount >= 6:
        return oppidx, f"6人局正常问对家({oppidx}号)"

    if players[oppidx]['rank'] is not None or players[oppidx]['mened'] is not None:
        return (curidx + 1) % 6, "出牌人无头，顺延给下家"

    untouidx = None
    for other in players:
        if other['rank'] is not None or other['mened'] is not None:
            cand = other['oppose']
            if players[cand]['rank'] is None and players[cand]['mened'] is None:
                untouidx = cand
                break

    if untouidx is None:
        return oppidx, f"5人局但未找到无头，问对家({oppidx}号)"

    if curidx in (0, 1, 2):
        ref = curidx + 3
    else:
        ref = curidx - 3

    if untouidx < ref:
        return untouidx, f"5人局，无头({untouidx}号) < 参考值{ref}，先问无头（对家{oppidx}号）"
    else:
        return oppidx, f"5人局，无头({untouidx}号) >= 参考值{ref}，先问对家({oppidx}号)"


def findUntouIndex():
    for other in players:
        if other['rank'] is not None or other['mened'] is not None:
            cand = other['oppose']
            if players[cand]['rank'] is None and players[cand]['mened'] is None:
                return cand
    return None


def planGoujiAsks(curidx, activecount):
    first, reason = getNextPlayerForGouji(curidx, activecount)
    if activecount != 5:
        return first, [], reason

    p = players[curidx]
    oppidx = p['oppose']
    untou = findUntouIndex()
    second = untou if first == oppidx else oppidx
    pending = []
    if (second is not None and second != first
            and players[second]['rank'] is None
            and players[second]['mened'] is None):
        pending = [second]
    return first, pending, reason


def menPlayer(target, menby):
    target['mened'] = menby
    players[menby]['men'].append(target['number'])
    target['rank'] = fallenHolder[0]
    fallenHolder[0] -= 1
    print(f"\n💀 {target['number']}号只剩一张3，被{menby}号闷了！")
    print(f"   被闷者{target['number']}号获得第 {target['rank']} 名。")


fallenHolder = [6]


desk = []
curidx = 0
passcount = 0
deskowner = None
lastcardplayer = None
rankcounter = 1
pendingask = []

while True:
    teamaaing = any(p['rank'] is None and p['mened'] is None for p in players if p['team'] == 'A')#A队的队员情况，是否全部获得了排名
    teambaing = any(p['rank'] is None and p['mened'] is None for p in players if p['team'] == 'B')
    if not teamaaing or not teambaing:#如果两队任意一对所有队员都获得排名
        print("\n========== 游戏结束 ==========")
        hassurvivors = any(p['rank'] is None and p['mened'] is None for p in players)
        if hassurvivors:
            lastnumber = None
            for p in players:
                if p['rank'] == rankcounter - 1:
                    lastnumber = p['number']
                    break
            if lastnumber is not None:
                curr = (lastnumber + 1) % 6
                for _ in range(6):
                    target = players[curr]
                    if target['rank'] is None and target['mened'] is None:
                        target['rank'] = rankcounter
                        rankcounter += 1
                    curr = (curr + 1) % 6
        for p in players:
            if p['mened'] is not None:
                status = f"被{p['mened']}号闷，第{p['rank']}名"
            elif p['rank'] is not None:
                status = f"第{p['rank']}名"
            else:
                status = "数据异常（未分配名次）"
            print(f"{p['number']}号: {status}")
        break

    p = players[curidx]

    if p['rank'] is not None or p['mened'] is not None:
        curidx = (curidx + 1) % 6
        continue
    activecount = sum(1 for x in players if x['rank'] is None and x['mened'] is None)


    if desk:
        isonly3 = (len(p['common']) == 1 and p['common'][0] == 3
                   and not p['two'] and not p['wang'])
        if isonly3:
            menby = deskowner if deskowner is not None else lastcardplayer
            menPlayer(p, menby)
            curidx = (curidx + 1) % 6
            continue

    activecount = sum(1 for x in players if x['rank'] is None and x['mened'] is None)

    if desk and passcount >= (activecount - 1):#疑似问题
        print(f"\n[清盘] {deskowner}号重新获得出牌权。")
        desk = []
        passcount = 0
        curidx = deskowner
        deskowner = None
        pendingask = []
        continue

    print(f"\n--- 轮到 {p['number']}号 ({p['team']}队) ---")

    if not desk:
        played = randomPlay(p['common'], p['two'], p['wang'])#如果桌面是空的，就随机出牌。
        for card in played:#删除对应的元素
            if card < 15:
                p['common'].remove(card)
            elif card == 15:
                p['two'].remove(card)
            else:
                p['wang'].remove(card)
        desk = replace2(played)#将出的牌进行特殊替换
        deskowner = p['number']#谁出的牌，用于判断谁最后获得牌权。
        lastcardplayer = p['number']#谁出的牌，用于判断被谁闷。
        passcount = 0#疑似问题
        pendingask = []

        if isGouji(desk) and activecount >= 5:
            first, pending, reason = planGoujiAsks(p['number'], activecount)
            print(f"👉 {p['number']}号 出牌: {played} (够级牌！ {reason})")
            pendingask = pending
            curidx = first
        else:
            print(f"👉 {p['number']}号 出牌: {played}")
            curidx = (curidx + 1) % 6

    else:
        curhand = p['common'] + p['two'] + p['wang']
        played = chupai(desk, curhand)

        if played:
            for card in played:
                if card < 15 and card in p['common']:
                    p['common'].remove(card)
                elif card == 15 and card in p['two']:
                    p['two'].remove(card)
                elif card > 15 and card in p['wang']:
                    p['wang'].remove(card)
            desk = replace2(played)
            deskowner = p['number']
            lastcardplayer = p['number']
            passcount = 0
            pendingask = []

            if isGouji(desk) and activecount >= 5:
                first, pending, reason = planGoujiAsks(p['number'], activecount)
                print(f"👉 {p['number']}号 管上了: {played} (够级牌！ {reason})")
                pendingask = pending
                curidx = first
            else:
                print(f"👉 {p['number']}号 管上了: {played}")
                curidx = (curidx + 1) % 6

        else:
            print(f"👉 {p['number']}号 管不上，过牌。")
            passcount += 1

            if pendingask:
                curidx = pendingask.pop(0)
                print(f"👉 继续询问 {curidx}号")
            elif deskowner is not None and isGouji(desk) and activecount >= 5:
                print(f"✅ 够级牌无敌，{deskowner}号重新获得出牌权。")
                desk = []

                passcount = 0
                curidx = deskowner
                deskowner = None
            else:
                curidx = (curidx + 1) % 6

    if not p['common'] and not p['two'] and not p['wang'] and p['rank'] is None and p['mened'] is None:
        print(f"🎉 {p['number']}号 牌出完了！")
        p['rank'] = rankcounter
        rankcounter += 1

    print(f"桌面: {desk}")
    print(f"{p['number']}号剩余牌: 普通={p['common']}, 2={p['two']}, 王={p['wang']}")
    print("-" * 30)