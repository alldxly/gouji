import function as f
num = 10
players = []
for i in range(6):
    team = 'A' if i % 2 == 0 else 'B'
    handstr = f.chushi(num)
    handval = sorted([f.pokedict[x] for x in handstr])
    players.append({
        'number': i, 'team': team, 'oppose': (i + 3) % 6,
        'hand': handval, 'common': [c for c in handval if c < 15],
        'two': [c for c in handval if c == 15], 'wang': [c for c in handval if c > 15],
        'rank': None,
        'men': [],
        'mened': None,
        'wutou': False,
        'dian':False,
    })

print("========== 游戏开始 ==========")
for p in players:
    print(f"{p['number']}号 ({p['team']}队) | 对头: {p['oppose']}号 | 手牌: {p['hand']}")


fallenHolder = 6

desk = []
lastcards=[]
curidx = 0
passcount = 0
deskowner = None

dianing=False
goujiing=False

rankcounter = 1
wutou = None  # 6人局第一次出完/被闷时赋值，进5人局后只读
wutouresult=True
opposeresult=True
while True:
    teamaaing = any(p['rank'] is None and p['mened'] is None for p in players if p['team'] == 'A')
    teambaing = any(p['rank'] is None and p['mened'] is None for p in players if p['team'] == 'B')
    if not teamaaing or not teambaing:
        print("\n========== 游戏结束 ==========")
        hassurvivors = any(p['rank'] is None and p['mened'] is None for p in players)
        if hassurvivors:
            lastnumber = None
            for p in players:
                if p['rank'] == rankcounter - 1 or fallenHolder+1:
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
            if p['dian']:
                status='开点成功'
            else:
                status='开点失败'
            if p['mened'] is not None:
                status += f",被{p['mened']}号闷，第{p['rank']}名"
            elif p['rank'] is not None:
                status += f",第{p['rank']}名"
            else:
                status += ",数据异常（未分配名次）"
            print(f"{p['number']}号: {status}")
        break

    p = players[curidx]

    if p['rank'] is not None or p['mened'] is not None:
        curidx = (curidx + 1) % 6
        continue

    activecount = sum(1 for x in players if x['rank'] is None and x['mened'] is None)
    if passcount>=activecount-1:
        desk=[]
        curidx=deskowner
        passcount=0
        deskowner = p['number']
        print(f'{curidx}号获得出牌权')

    print(f"\n--- 轮到 {p['number']}号 ({p['team']}队) ---")
    if activecount == 6:
        if not desk:
            dianing, goujiing = f.isGouji(lastcards)
            played = f.randomPlay(p['common'], p['two'], p['wang'],dianing)
            print(lastcards)
            lastcards=played
            if dianing and 4 in played:
                p['dian']=True
                print('开点成功')
            for card in played:
                if card < 15:
                    p['common'].remove(card)
                elif card == 15:
                    p['two'].remove(card)
                else:
                    p['wang'].remove(card)
            deskowner = p['number']
            passcount = 0
            dianing,goujiing=f.isGouji(played)
            if goujiing:
                print(f"👉 {p['number']}号 出牌: {played} (够级牌！ {played})")
                curidx = (p['number'] + 3) % 6
                if dianing:
                    print('可开点')
                else:
                    print('不可开点')
            else:
                print(f"👉 {p['number']}号 出牌: {played}")
                curidx = (curidx + 1) % 6
            desk = f.replace2(played)
        else:
            curhand = p['common'] + p['two'] + p['wang']
            played = f.chupai(desk, curhand)
            if played:
                lastcards = played
                for card in played:
                    if card < 15 and card in p['common']:
                        p['common'].remove(card)
                    elif card == 15 and card in p['two']:
                        p['two'].remove(card)
                    elif card > 15 and card in p['wang']:
                        p['wang'].remove(card)

                deskowner = p['number']
                passcount = 0
                dianing,goujiing=f.isGouji(played)
                if goujiing:
                    print(f"👉 {p['number']}号 出牌: {played} (够级牌！ {played})")
                    curidx = (p['number'] + 3) % 6
                    if dianing:
                        print('可开点')
                    else:
                        print('不可开点')
                else:
                    print(f"👉 {p['number']}号 管上了: {played}")
                    curidx = (curidx + 1) % 6
                desk = f.replace2(played)
            else:
                print(f"👉 {p['number']}号 管不上，过牌。")
                dianing,goujiing=f.isGouji(desk)
                if deskowner is not None and goujiing:
                    print(f"{deskowner}号获得出牌权。")
                    desk = []
                    passcount = 0
                    curidx = deskowner
                else:
                    passcount += 1
                    curidx = (curidx + 1) % 6


    elif activecount == 5:
        if not desk:
            dianing,goujiing=f.isGouji(lastcards)
            played = f.randomPlay(p['common'], p['two'], p['wang'], dianing)
            print(lastcards)
            lastcards = played
            if dianing and 4 in played and not p['wutou']:
                p['dian']=True
            for card in played:
                if card < 15:
                    p['common'].remove(card)
                elif card == 15:
                    p['two'].remove(card)
                else:
                    p['wang'].remove(card)
            deskowner = p['number']
            passcount = 0
            dianing,goujiing=f.isGouji(played)
            if goujiing:
                print(f"👉 {p['number']}号 出牌: {played} (够级牌！ {played})")
                if p['wutou']:
                    curidx = (curidx + 1) % 6
                else:
                    if wutou in [(p['number']+1)%6,(p['number']+2)%6]:
                        curidx = wutou
                    elif wutou in [(p['number']+4)%6,(p['number']+5)%6]:
                        curidx = p['oppose']
            else:
                print(f"👉 {p['number']}号 出牌: {played}")
                curidx = (curidx + 1) % 6
            dianing=False
            desk = f.replace2(played)
        else:
            curhand = p['common'] + p['two'] + p['wang']
            played = f.chupai(desk, curhand)

            if played:
                lastcards = played
                for card in played:
                    if card < 15 and card in p['common']:
                        p['common'].remove(card)
                    elif card == 15 and card in p['two']:
                        p['two'].remove(card)
                    elif card > 15 and card in p['wang']:
                        p['wang'].remove(card)
                deskowner = p['number']
                passcount = 0
                dianing,goujiing=f.isGouji(played)
                if goujiing:
                    print(f"👉 {p['number']}号 出牌: {played} (够级牌！ {played})")
                    if p['wutou']:
                        curidx = (curidx + 1) % 6
                        wutouresult=True
                        opposeresult = True
                    else:
                        opposeresult=True
                        wutouresult = True
                        if wutou in [(p['number'] + 1) % 6, (p['number'] + 2) % 6]:
                            curidx = wutou
                        elif wutou in [(p['number'] + 4) % 6, (p['number'] + 5) % 6]:
                            curidx = p['oppose']

                else:
                    print(f"👉 {p['number']}号 出牌: {played}")
                    curidx = (curidx + 1) % 6
                desk = f.replace2(played)
            else:
                dianing,goujiing=f.isGouji(lastcards)
                if goujiing:
                    if not(not wutouresult and not opposeresult):
                        print(f'{p['number']}管不上')
                        if players[deskowner]['wutou']:
                            curidx=(curidx+1)%6
                            passcount+=1
                        else:
                            if p['wutou']:
                                wutouresult=False
                                curidx=players[deskowner]['oppose']
                            else:
                                opposeresult=False
                                curidx=wutou
                    if not wutouresult and not opposeresult:
                        desk = []
                        curidx = deskowner
                        passcount = 0
                        print(f'无头和对家都管不上，{deskowner}号获得出牌权')
                        wutouresult = True
                        opposeresult = True

                else:
                    passcount += 1
                    curidx = (curidx + 1) % 6

    else:
        if not desk:
            played = f.randomPlay(p['common'], p['two'], p['wang'],dianing)
            for card in played:
                if card < 15:
                    p['common'].remove(card)
                elif card == 15:
                    p['two'].remove(card)
                else:
                    p['wang'].remove(card)
            desk = f.replace2(played)
            deskowner = p['number']
            passcount = 0
            curidx=(curidx+1)%6
        else:
            curhand = p['common'] + p['two'] + p['wang']
            played = f.chupai(desk, curhand)
            if played:
                for card in played:
                    if card < 15 and card in p['common']:
                        p['common'].remove(card)
                    elif card == 15 and card in p['two']:
                        p['two'].remove(card)
                    elif card > 15 and card in p['wang']:
                        p['wang'].remove(card)
                desk = f.replace2(played)
                deskowner = p['number']
                passcount = 0
                curidx=(curidx+1)%6
                print(f"👉 {p['number']}号 出牌: {played}")
            else:
                print(f'{p['number']}管不上')
                passcount += 1
                curidx = (curidx + 1) % 6

    # ===== 末尾结算：只处理还没排过名、没被闷过的人 =====
    for a in players:
        if a['rank'] is not None or a['mened'] is not None:
            continue
        if (len(a['common']) == 1 and a['common'][0] == 3
                and not a['two'] and not a['wang']
                and a['number'] != deskowner):
            if activecount == 6:
                a['rank'], a['mened'] = fallenHolder, deskowner
                fallenHolder -= 1
                b = players[a['oppose']]
                if b['rank'] is None and b['mened'] is None:
                    b['wutou'] = True
                    wutou = b['number']
                print(f"{a['number']}号被{deskowner}号闷，{b['number']}成为无头")
                if a['oppose']==deskowner:
                    curidx=(deskowner+1)%6
                else:
                    dianing,goujiing=f.isGouji(lastcards)
                    if goujiing:
                        if wutou in [(deskowner + 1) % 6, (deskowner + 2) % 6]:
                            curidx = wutou
                        elif wutou in [(deskowner + 4) % 6, (deskowner + 5) % 6]:
                            curidx = (deskowner+3)%6
                    else:
                        curidx=(deskowner+1)%6


            else:
                a['rank'], a['mened'] = fallenHolder, deskowner
                fallenHolder -= 1
                print(f"{a['number']}号被{deskowner}号闷")
                curidx = (deskowner+1)%6

        if not a['common'] and not a['two'] and not a['wang']:
            if activecount == 6:
                a['rank'] = rankcounter
                rankcounter += 1
                b = players[a['oppose']]
                if b['rank'] is None and b['mened'] is None:
                    b['wutou'] = True
                    wutou = b['number']
                print(f"{a['number']}号出完牌，{b['number']}成为无头")

            else:
                a['rank'] = rankcounter
                rankcounter += 1
                print(f"{a['number']}号出完牌")

    print(f"桌面: {desk}")
    print(f"{p['number']}号剩余牌: 普通={p['common']}, 2={p['two']}, 王={p['wang']}")
    print("-" * 30)