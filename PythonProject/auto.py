import random
import itertools

pokedict = {
    '4': 4, '5': 5, '6': 6, '7': 7,
    '8': 8, '9': 9, '10': 10,
    'J': 11, 'Q': 12, 'K': 13, 'A': 14,
    '2': 15, 'X': 16,
    'D': 17, 'Y': 18,  '3': 3,
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


def replace_2(values):
    if 15 in values:
        target = max((v for v in values if v < 15), default=None)
        if target is not None:
            return [target if v == 15 else v for v in values]
    return values


def random_play(common, two, wang):
    play_cards = []
    pool_no_3 = [c for c in common if c != 3]

    if random.randint(0, 1) == 1 and len(pool_no_3) > 0:
        target = random.choice(pool_no_3)
        all_same_cards = [c for c in pool_no_3 if c == target]
        play_count = random.randint(1, len(all_same_cards))
        play_cards.extend(all_same_cards[:play_count])

    if random.randint(0, 1) == 1 and len(two) > 0:
        count = random.randint(1, len(two))
        play_cards.extend(random.sample(two, count))

    if random.randint(0, 1) == 1 and len(wang) > 0:
        count = random.randint(1, len(wang))
        combos = list(itertools.combinations(wang, count))
        play_cards.extend(list(random.choice(combos)))

    if not play_cards:
        if pool_no_3:
            target = pool_no_3[0]
            play_cards.extend([c for c in pool_no_3 if c == target])
        elif len(two) > 0:
            play_cards.append(two[0])
        elif len(wang) > 0:
            play_cards.append(wang[0])

    return play_cards


def chupai(desk, current_hand):
    target_len = len(desk)
    target_max = max(desk)

    # 1. 先找同点数、同张数，且能管上的普通牌
    for card in sorted(set(current_hand)):
        if card > target_max and card < 15:
            count_in_hand = current_hand.count(card)
            if count_in_hand >= target_len:
                return [card] * target_len

    # 2. 找王 / 鹰的硬管逻辑
    temp_me = current_hand.copy()
    temp_d = desk.copy()
    played_cards = []

    while len(temp_me) > 0 and len(temp_d) > 0:
        zuixiao = 0
        for a in temp_me:
            if a > temp_d[-1]:
                del temp_d[-1]
                zuixiao = a
                break
        if zuixiao:
            temp_me.remove(zuixiao)
            played_cards.append(zuixiao)
        else:
            if temp_d[-1] < 16:
                return []
            elif temp_d[-1] == 16:
                if temp_me.count(16) >= 2:
                    del temp_d[-1]
                    del temp_me[-2:]
                    played_cards.extend([16, 16])
                else:
                    return []
            elif temp_d[-1] == 17:
                if temp_me.count(17) >= 2:
                    del temp_d[-1]
                    del temp_me[-2:]
                    played_cards.extend([17, 17])
                elif temp_me.count(16) >= 3:
                    del temp_me[-3:]
                    del temp_d[-1]
                    played_cards.extend([16, 16, 16])
                else:
                    return []
            else:
                if temp_me.count(18) >= 2:
                    del temp_d[-1]
                    del temp_me[-2:]
                    played_cards.extend([18, 18])
                elif temp_me.count(17) >= 3:
                    del temp_me[-3:]
                    del temp_d[-1]
                    played_cards.extend([17, 17, 17])
                else:
                    return []

    if len(temp_d) == 0:
        return played_cards
    return []


# ==================== 初始化 ====================
num = 5
mepoke = chushi(num)
duishoupoke = chushi(num)

mepoke.sort(key=lambda x: pokedict[x])
duishoupoke.sort(key=lambda x: pokedict[x])
print(f'我的初始牌{mepoke},对手初始牌{duishoupoke}')

mevalue = [pokedict[x] for x in mepoke]
duishouvalue = [pokedict[y] for y in duishoupoke]
mevalue.sort()
duishouvalue.sort()

mecommon = [i for i in mevalue if i < 15]
me2 = [i for i in mevalue if i == 15]
mewang = [i for i in mevalue if i > 15]

duishoucommon = [j for j in duishouvalue if j < 15]
duishou2 = [j for j in duishouvalue if j == 15]
duishouwang = [j for j in duishouvalue if j > 15]

# ==================== 终极主循环 ====================
desk = []
current_state = "对手"

while True:
    if not desk:
        # 【核心逻辑】：只要自由出牌，先查双方有没有人只剩 3
        me_only_3 = (len(mecommon) == 1 and mecommon[0] == 3 and not me2 and not mewang)
        duishou_only_3 = (len(duishoucommon) == 1 and duishoucommon[0] == 3 and not duishou2 and not duishouwang)

        if me_only_3:
            if current_state == "我":
                print("【我出完了，游戏结束！】")
            else:
                print("【我被闷，游戏结束！】")
            break

        if duishou_only_3:
            if current_state == "对手":
                print("【对手出完了，游戏结束！】")
            else:
                print("【对手被闷，游戏结束！】")
            break

        # 如果没有人只剩3，正常随机出牌
        if current_state == "对手":
            print(f"【对手自由出牌】:")
            duishou_played = random_play(duishoucommon, duishou2, duishouwang)
            for card in duishou_played:
                if card < 15:
                    duishoucommon.remove(card)
                elif card == 15:
                    duishou2.remove(card)
                else:
                    duishouwang.remove(card)
            desk = replace_2(duishou_played)
            current_state = "我"
        else:
            print(f"【我自由出牌】:")
            my_play = random_play(mecommon, me2, mewang)
            for card in my_play:
                if card < 15:
                    mecommon.remove(card)
                elif card == 15:
                    me2.remove(card)
                else:
                    mewang.remove(card)
            desk = replace_2(my_play)
            current_state = "对手"

    else:
        # 桌面有牌，谁管谁
        if current_state == "对手":
            print(f"【对手尝试管牌】:")
            # 传入对手的真正手牌
            duishou_played = chupai(desk, duishoucommon + duishou2 + duishouwang)

            if not duishou_played:
                print("【对手管不上，过牌】")
                desk = []
            else:
                for card in duishou_played:
                    if card < 15 and card in duishoucommon:
                        duishoucommon.remove(card)
                    elif card == 15 and card in duishou2:
                        duishou2.remove(card)
                    elif card > 15 and card in duishouwang:
                        duishouwang.remove(card)
                desk = replace_2(duishou_played)
            current_state = "我"

        else:
            print(f"【我尝试管牌】:")
            # 传入我的真正手牌
            my_play = chupai(desk, mecommon + me2 + mewang)

            if not my_play:
                print("【我管不上，过牌】")
                desk = []
            else:
                for card in my_play:
                    if card < 15 and card in mecommon:
                        mecommon.remove(card)
                    elif card == 15 and card in me2:
                        me2.remove(card)
                    elif card > 15 and card in mewang:
                        mewang.remove(card)
                desk = replace_2(my_play)
            current_state = "对手"

    print(f"桌面: {desk}")
    print(f"我的剩余牌池: 普通={mecommon}, 2={me2}, 王={mewang}")
    print(f"对手的剩余牌池: 普通={duishoucommon}, 2={duishou2}, 王={duishouwang}")
    print("-" * 30)