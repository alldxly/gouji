pokedict = {
    '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
    '8': 8, '9': 9, '10': 10,
    'J': 11, 'Q': 12, 'K': 13, 'A': 14,
    '2': 15, 'X': 16, 'D': 17, 'Y': 18
}

def gouji(poke):
    if (sum(1 for a in poke if a >= 10) >= 5 or
        sum(1 for a in poke if a >= 11) >= 4 or
        sum(1 for a in poke if a >= 12) >= 3 or
        sum(1 for a in poke if a >= 13) >= 2 or
        sum(1 for a in poke if a >= 14) >= 2 or
        sum(1 for a in poke if a >= 15) >= 1):
        if (sum(1 for a in poke if 10 <= a < 15) >= 5 or
            sum(1 for a in poke if 11 <= a < 15) >= 4 or
            sum(1 for a in poke if 12 <= a < 15) >= 3 or
            sum(1 for a in poke if 13 <= a < 15) >= 2) and not any(a >= 15 for a in poke):
            print('够级且可开点')
        else:
            print('够级但不可开点')
        return True
    else:
        print('不够级')
        return False

def shao(poke):
    wang=0
    san=[]
    for a in poke:
        if a>15:
            wang+=1
    for b in poke:
        if b<=15 and b not in san:
            san.append(b)
    if wang>=len(san):
        print('可烧')
    else:
        print('不可烧')


def bijiao(poke1, poke2):
    # 绑定变量：让原先的 mevalue 和 duishouvalue 对应到传入的参数
    mevalue = poke1
    duishouvalue = poke2
    while len(mevalue) > 0 and len(duishouvalue) > 0:
        zuixiao = 0
        for a in mevalue:
            if a > duishouvalue[-1]:
                del duishouvalue[-1]
                zuixiao = a
                break
        if zuixiao:
            mevalue.remove(zuixiao)
        else:
            if duishouvalue[-1] < 16:
                break
            elif duishouvalue[-1] == 16:
                if mevalue.count(16) >= 2:
                    del duishouvalue[-1]
                    del mevalue[-2:]
                else:
                    break
            elif duishouvalue[-1] == 17:
                if mevalue.count(17) >= 2:
                    del duishouvalue[-1]
                    del mevalue[-2:]
                elif mevalue.count(16) >= 3:
                    if mevalue[-1] == 17:
                        del mevalue[-4:-1]
                        del duishouvalue[-1]
                    else:
                        del mevalue[-3:]
                        del duishouvalue[-1]
                else:
                    break
            else:
                if mevalue.count(18) >= 2:
                    del duishouvalue[-1]
                    del mevalue[-2:]
                elif mevalue.count(17) >= 3:
                    if mevalue[-1] == 18:
                        del mevalue[-4:-1]
                        del duishouvalue[-1]
                    else:
                        del mevalue[-3:]
                        del duishouvalue[-1]
                else:
                    break

    

def replace_2(values):
    if 15 in values:
        # 找出除了 15 以外，最大的一张牌（<=15 防止变成王）
        target = max((v for v in values if v < 15), default=None)
        if target is not None:
            return [target if v == 15 else v for v in values]
    return values

while True:
    try:
        mepoke = int(input('我的牌数: '))
        duishoupoke = int(input('对手牌数: '))
        me = []
        duishou = []
        # --- 原始输入逻辑保持不变，只把 .upper() 去掉，让你原本的严格校验生效 ---
        i = 0
        while i < mepoke:
            a = input('我的牌点: ')
            if a not in pokedict.keys():
                print('输入错误，请重新输入')
                continue
            if a not in ['X', 'D', 'Y', '2']:
                prev_normal = [x for x in me if x not in ['X', 'D', 'Y', '2']]
                if prev_normal and a != prev_normal[0]:
                    print(f'输入错误，普通牌必须一致（你前面输入了 {prev_normal[0]}）')
                    continue
            me.append(a)
            i += 1

        j = 0
        while j < duishoupoke:
            b = input('对手牌点: ')
            if b not in pokedict:
                print('输入错误，请重新输入')
                continue
            if b not in ['X', 'D', 'Y', '2']:
                prev_normal = [x for x in duishou if x not in ['X', 'D', 'Y', '2']]
                if prev_normal and b != prev_normal[0]:
                    print(f'输入错误，普通牌必须一致（对手前面输入了 {prev_normal[0]}）')
                    continue
            duishou.append(b)
            j += 1

        # 转成数字
        mevalue = [pokedict[x] for x in me]
        duishouvalue = [pokedict[y] for y in duishou]
        gouji(mevalue)
        gouji(duishouvalue)

        # ==========================================
        # 修复：加入 2 (15) 的特殊赋值逻辑
        # 如果列表里有 15，找出列表里第一个小于 15 的牌，把 15 替换成它
        # ==========================================

        mevalue = replace_2(mevalue)
        duishouvalue = replace_2(duishouvalue) # 修复了你原代码错写成 mevalue 的 bug
        mevalue.sort()
        duishouvalue.sort()

        # --- 核心比较逻辑 ---
        a=bijiao(mevalue,duishouvalue)


        # --- 终局判断 ---
        if len(duishouvalue) == 0:
            print('✅ 我的牌大于对手')
            if a:
                shao(mevalue)
            else:
                print('不可烧')
        else:
            print('❌ 我的牌不大于对手')

    except ValueError:
        print('牌数只能是数字，请重新开始')
    except Exception as e:
        print(f'发生未知错误: {e}')
