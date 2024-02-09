import matplotlib.pyplot as plt
import numpy as np

from random import randint

def consol_im():
    print("Проанализируйте график и скажите")
    # PV = T
    state = int(input("Количество состоний: "))
    yes = input("Они они идут по кругу?(да\нет)\n")
    if yes.lower() == "да":
        ind = 0
    else:
        ind = 1
    pack_st = np.array([["=","=","="]])
    s = state
    print("На вопросы изменения отвечать <, >, =")
    i = 1
    while state != ind:
        if i+1> s:
            print(f"Состояние {i}-1")
        else:
            print(f"Состояние {i}-{i+1}")
        pack_st = np.vstack((pack_st,input("Как изменилось давление? объем? температура?\n").split()))
        state -=1
        i +=1
    if ind == 1:
        pack_st = np.vstack(([["0","0","0"]],pack_st[1:]))
    pack_st_i =  np.zeros((len(pack_st),3))
    for i in range(len(pack_st)):
        for m in range(3):
            if pack_st[i][m] == "<":
                pack_st_i[i][m] = 1
            elif pack_st[i][m] == ">":
                pack_st_i[i][m] = 2
            elif pack_st[i][m] == "=":
                pack_st_i[i][m] = 3
            elif pack_st[i][m] == "0":
                pack_st_i[i][m] = 0
    """
        pack_st = [[1 2 3]
                   [1 2 3]]
        Из этого следует
        01 < 00, 11>10, 21 = 20
    """
    def sc_rf():
        x = input("Сколько различных равенств существует?\n")
        try:
            return int(x)
        except:
            print("Введена не цыфра")
            sc_rf()
    kl = sc_rf()
    pack_rafn = np.full((2,1,kl), -1)
    print("Пишите полное равенство(можно состоящие из нескольких переменных)")
    print("Например если P1 = P2 = P3, то 'P1 P2 P3'")
    a = 0
    b = 0 # №Номер выражения начиная с второго
    while kl !=0:
        eq = input("Ожидаю\n").split()
        """
            pack_rafn =                 
            [[[ 1x1 2x1 3x1]
              [ 1x2 2x2 3x2]]
            
              [[1y1 2y1 3y1]
              [1y2 2y2 3y2]]]
            по столбцу идут переменные которые равны между собой
            по глбине их координаты
            по строке идут различные выражения
        """
        if a ==0:
            for i in eq:
                pack_rafn = np.hstack((pack_rafn, [
                    [[ sort(list(i)[0]) if b == m else -1 for m in range(kl)]],

                    [[int(list(i)[1])-1 if b == m else -1 for m in range(kl)]]
                    ]))
        else:
            for i in eq:
                if  len(eq)<= len(pack_rafn[0]):
                    pack_rafn[0][eq.index(i)+1][b] = sort(list(i)[0])
                    pack_rafn[1][eq.index(i)+1][b] = int(list(i)[1])-1
                else:
                    pack_rafn = np.hstack((pack_rafn, [
                    [[ sort(list(i)[0]) if b == m else -1 for m in range(kl)]],

                    [[int(list(i)[1])-1 if b == m else -1 for m in range(kl)]]
                    ]))
        b+=1
        kl -=1
        a +=1
    pack_rafn = pack_rafn[:,1:]
    return pack_st_i, pack_rafn
def sort(x_):
    if x_ in ["P", "p"]:
        x = 0
    elif x_ in ["V", "v"]:
        x = 1
    elif x_ in ["T", "t"]:
        x = 2
    return(x)
def correct(pack_st, pack_rafn):
    pack = np.full((1,3), -1)
    """
        pack = [[1, 2, 3]]    как (больше меньше равно) предыдущего
    """
    ind = 0
    for y in range(len(pack_st)):
        if pack_st[y][0] == 0:   #Значит что график не закруглен
            ind = 1
        pack = np.vstack((pack,[[pack_st[y][0], pack_st[y][1], pack_st[y][2]]]))
    pack = pack[1:]
    pack_ch = np.full((len(pack), 3), 10.)
    cor_srafn(pack_ch, pack, pack_rafn, ind)
    return pack_ch
def cor_srafn(pack_ch,pack_cnd, pack_rafn,ind):
    i = True
    m = -1
    while i and m != 30:
        if ind == 1:
            rn = reversed(range(len(pack_ch[1:])))
        else:
            rn = range(len(pack_ch[1:]))
        for state in rn:
            for per in range(3):
                condition(state+ind, per, pack_ch,pack_cnd,ind, pack_rafn=pack_rafn)
        condition(len(pack_ch[1:])-1, 2,pack_ch, pack_cnd, ind, pack_rafn=pack_rafn)
        for state in rn:
            for per in range(3):
                condition_2(state+ind, per, pack_ch,pack_cnd,ind, pack_rafn)
        i = start_equement(pack_rafn,pack_ch)
        m+=1
    print(m)
def start_equement(pack_rafn,pack_ch):
    p = 0
    for el in pack_rafn.transpose():
        p += condition_equement(el,pack_ch)
    if p == 0:
        return False
    else:
        return True

def condition(state, per, pack_ch, cnd_pack, ind, m=0, pack_rafn = None):
    # print(f"\n{ind}")
    # print(f"{state}\n")
    if ind ==1 and state-1 <0:
        state = len(pack_ch)-1
    p = 0  #Параметр изменения числа
    ch = pack_ch[state][per]
    ch_1 = pack_ch[state-1][per]
    cnd=cnd_pack[state][per]
    # print(pack_cnd)
    if cnd == 1:
        if ch >= ch_1:
            if ch-ch_1 <1:
                raz = 1
            else:
                raz = ch-ch_1
            pack_ch[state][per] = ch - randint(3,6)*(raz)
            p +=1
    elif cnd == 2:
        if ch <= ch_1:
            if ch_1-ch <1:
                raz = 1
            else:
                raz = ch_1-ch
            pack_ch[state][per] =  ch + randint(3,6)*(raz)
            p +=1
    if p > 0:
        condition(state-1, per,pack_ch, cnd_pack, ind)
        if m == 1:
            condition_2(state-1, per, pack_ch, cnd_pack,ind, pack_rafn)
        if m ==2:
            condition_2(state-1, per, pack_ch, cnd_pack,ind,pack_rafn)
            condition_equement(pack_rafn, pack_ch)
def condition_2(state, per, pack_ch, cnd_pack, ind, pack_rafn):
    if ind ==1 and state-1 <0:
        state = len(pack_ch)-2
    p = 0  #Параметр изменения числа
    ch = pack_ch[state][per]
    ch_1 = pack_ch[state-1][per]
    cnd=cnd_pack[state][per]
    if cnd == 3:
        if ch != ch_1:
            pack_ch[state][per] = ch_1
            p +=1
    if p > 0:
        condition(state-1, per,pack_ch, cnd_pack,ind, 1, pack_rafn)
def condition_equement(el, pack):
    lst_ch = []
    p = 0
    for stolb in el:
        lst_ch.append(pack[stolb[1]][stolb[0]])
    x = (max(lst_ch)+min(lst_ch))/2
    for stolb in el:
        if pack[stolb[1]][stolb[0]] != x:
            pack[stolb[1]][stolb[0]] = x
            p = 1
    return p
    
def do_cord(pack_ch, pr_0, pr_1):
    print(pack_ch)
    if 3 in [pr_0, pr_1]:
        return np.array(pack_ch[:,pr_0]), np.array(pack_ch[:,pr_1])
    else:
        return np.array(pack_ch[:,pr_0]), np.array(pack_ch[:,pr_1])
def create():
    pack_st, pack_rafn= consol_im()
    pack_ch = correct(pack_st, pack_rafn)
    fig = plt.figure()
    ax1 = fig.add_subplot(221)
    xy=do_cord(pack_ch, 1, 2)
    ax1.plot(xy[1],xy[0])
    ax2 = fig.add_subplot(222)
    xy=do_cord(pack_ch, 0, 2)
    ax2.plot(xy[1],xy[0])
    ax3 = fig.add_subplot(223)
    xy=do_cord(pack_ch, 0, 1)
    ax3.plot(xy[1],xy[0])
    plt.show()

        
if __name__ == "__main__":
    create()
    # print(randint(1,10))