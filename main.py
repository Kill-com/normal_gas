import matplotlib.pyplot as plt
import numpy as np

def consol_im():
    print("Проанализируйте график и скажите")
    # PV = T
    state = int(input("Количество состоний: "))
    yes = input("Они они идут по кругу?(да\нет)\n")
    if yes.lower() == "да":
        m = 0
    else:
        m = 1
    pack_st = np.array([["=","=","="]])
    s = state
    print("На вопросы изменения отвечать <, >, =")
    i = 1
    while state !=m:
        if i+1> s:
            print(f"Состояние {i}-1")
        else:
            print(f"Состояние {i}-{i+1}")
        pack_st = np.vstack((pack_st,input("Как изменилось давление? объем? температура?\n").split()))
        state -=1
        i +=1
    if m == 0:
        pack_st = pack_st[1:]
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
                    [[ sort(list(i)[0]) if b == m else -1 for m in range(3)]],

                    [[int(list(i)[1])-1 if b == m else -1 for m in range(3)]]
                    ]))
        else:
            for i in eq:
                if  len(eq)<= len(pack_rafn[0]):
                    pack_rafn[0][eq.index(i)+1][b] = sort(list(i)[0])
                    pack_rafn[1][eq.index(i)+1][b] = int(list(i)[1])-1
                else:
                    pack_rafn = np.hstack((pack_rafn, [
                    [[ sort(list(i)[0]) if b == m else -1 for m in range(3)]],

                    [[int(list(i)[1])-1 if b == m else -1 for m in range(3)]]
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
    for y in range(len(pack_st)):
        pack = np.vstack((pack,[[pack_st[y][0], pack_st[y][1], pack_st[y][2]]]))
    pack_ch = np.full((len(pack), 3), 10.)   # ТУТ ТАК НАДООООО
    pack = pack[1:]
    cor_srafn(pack_ch, pack, pack_rafn)
    return pack_ch
def cor_srafn(pack_ch,pack_cnd, pack_rafn):
    i = True
    m = -1
    while i and m != 1000:
        for state in range(len(pack_ch[1:])):
            for per in range(3):
                condition(state, per, pack_ch,pack_cnd, pack_rafn=pack_rafn)
        for state in range(len(pack_ch[1:])):
            for per in range(3):
                condition_2(state, per, pack_ch,pack_cnd, pack_rafn)
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

def condition(state, per, pack_ch, cnd_pack, m=0, pack_rafn = None):
    p = 0  #Параметр изменения числа
    ch = pack_ch[state][per]
    ch_1 = pack_ch[state-1][per]
    cnd=cnd_pack[state][per]
    # print(pack_cnd)
    if cnd == 1:
        if ch >= ch_1:
            pack_ch[state][per] = (ch - 2)
            p +=1
    elif cnd == 2:
        if ch <= ch_1:
            pack_ch[state][per] = (ch+2)
            p +=1
    if p > 0:
        condition(state-1, per,pack_ch, cnd_pack)
        if m == 1:
            condition_2(state-1, per, pack_ch, cnd_pack, pack_rafn)
        if m ==2:
            condition_2(state-1, per, pack_ch, cnd_pack,pack_rafn)
            start_equement(pack_rafn, pack_ch)
def condition_2(state, per, pack_ch, cnd_pack, pack_rafn):
    p = 0  #Параметр изменения числа
    ch = pack_ch[state][per]
    ch_1 = pack_ch[state-1][per]
    cnd=cnd_pack[state][per]
    if cnd == 3:
        if ch != ch_1:
            x = (ch+ch_1)/2
            pack_ch[state][per] = x
            pack_ch[state-1][per] = x
            p +=1
    if p > 0:
        condition(state-1, per,pack_ch, cnd_pack, 1, pack_rafn)
def condition_equement(el, pack):
    lst_ch = []
    p = 0
    for stolb in el:
        if stolb[1] != -1 and stolb[0] != -1:
            print(pack)
            print(stolb)
            lst_ch.append(pack[stolb[1]][stolb[0]])
    print(lst_ch)
    print(max(lst_ch))
    print(min(lst_ch))
    x = (max(lst_ch)+min(lst_ch))/2
    for stolb in el:
        if pack[stolb[1]][stolb[0]] != x:
            pack[stolb[1]][stolb[0]] = x
            p = 1
    return p
    
def do_cord(pack_ch):
    pr = input("В каких плоскостях находиться график(через пробел)\n").split()
    pr = [sort(pr[0]), sort(pr[1])]
    print(pack_ch)
    if 3 in pr:
        return np.array(pack_ch[:,pr[0]]), np.array(pack_ch[:,pr[1]])
    else:
        return np.array(pack_ch[:,pr[0]]), np.array(pack_ch[:,pr[1]])
def create():
    pack_st, pack_rafn= consol_im()
    pack_ch = correct(pack_st, pack_rafn)
    xy=do_cord(pack_ch)
    print(xy)
    plt.plot(xy[0],xy[1])
    plt.show()

        
if __name__ == "__main__":
    create()
    # x = np.array([[[1,0],[2,3],[4,5]],[[1,1],[6,7],[8,9]]])
    # print(np.array([[[3, 2, 1]],*[[[-1,-1,-1]] for i in range(3)]]))
    # x = np.array([[1,2,3], [3,4,5], [0,0,0]]);print(x)
    # print(0 != -1)
    # print(np.zeros((3, 2)))
    # print(x.tolist())


    

