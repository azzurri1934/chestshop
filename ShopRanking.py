import sys, os, math

class Item:

    def __init__(self):
        self.name = ""
        self.bought_price = 0
        self.bought_num = 0
        self.sold_price = 0
        self.sold_num = 0
        self.rank = 0
        self.rank_str = ""

class User:

    def __init__(self):
        self.name = ""
        self.item_list = []
        self.rank = 0
        self.rank_str = ""

    def add_item(self, item):
        for x in self.item_list:
            if x.name == item.name:
                x.bought_num += item.bought_num
                x.bought_price += item.bought_price
                x.sold_num += item.sold_num
                x.sold_price += item.sold_price
                return
        self.item_list.append(item)

    def get_totalUriageNum(self):
        totalUriageNum = 0
        for item in self.item_list:
            totalUriageNum += item.bought_num
        return totalUriageNum

    def get_totalUriagePrice(self):
        totalUriagePrice = 0
        for item in self.item_list:
            totalUriagePrice += item.bought_price
        return totalUriagePrice

    def get_totalKaitoriNum(self):
        totalKaitoriNum = 0
        for item in self.item_list:
            totalKaitoriNum += item.sold_num
        return totalKaitoriNum

    def get_totalKaitoriPrice(self):
        totalKaitoriPrice = 0
        for item in self.item_list:
            totalKaitoriPrice += item.sold_price
        return totalKaitoriPrice

    def get_totalPrice(self):
        return self.get_totalUriagePrice() - self.get_totalKaitoriPrice()

class User_list:

    def __init__(self):
        self.user_list = []

    def add_user(self, user):
        for x in self.user_list:
            if x.name == user.name:
                x.add_item(user.item_list[0])
                return
        self.user_list.append(user)

def get_user_list(dir_path):
    user_list = User_list()
    for dirpath, dirs, files in os.walk(dir_path):
        for fn in files:
            path = os.path.join(dirpath, fn)
            f = file(path, 'r')
            for line in f:
                if " bought " in line:
                    bought_item = Item()
                    string = line.split(" ")
                    bought_item.bought_num = int(string[6])
                    if string[8] == "for":
                        bought_item.name = string[7]
                        next_index = 9
                    elif string[9] == "for":
                        bought_item.name = string[7] + " " + string[8]
                        next_index = 10
                    elif string[10] == "for":
                        bought_item.name = string[7] + " " + string[8] + " " + string[9]
                        next_index = 11
                    elif string[11] == "for":
                        bought_item.name = string[7] + " " + string[8] + " " + string[9]+ " " + string[10]
                        next_index = 12
                    bought_item.bought_price = int(float(string[next_index]))
                    user = User()
                    user.name = string[next_index + 2]
                    user.add_item(bought_item)

                    user_list.add_user(user)
                elif " sold " in line:
                    sold_item = Item()
                    string = line.split(" ")
                    sold_item.sold_num = int(string[6])
                    if string[8] == "for":
                        sold_item.name = string[7]
                        next_index = 9
                    elif string[9] == "for":
                        sold_item.name = string[7] + " " + string[8]
                        next_index = 10
                    elif string[10] == "for":
                        sold_item.name = string[7] + " " + string[8] + " " + string[9]
                        next_index = 11
                    elif string[11] == "for":
                        sold_item.name = string[7] + " " + string[8] + " " + string[9]+ " " + string[10]
                        next_index = 12
                    sold_item.sold_price = int(float(string[next_index]))
                    user = User()
                    user.name = string[next_index + 2]
                    user.add_item(sold_item)

                    user_list.add_user(user)
            f.close()

    user_list = sorted(user_list.user_list, cmp=lambda x,y: cmp(x.name.lower(), y.name.lower()))
    user_list = sorted(user_list, key=lambda User: User.get_totalPrice(), reverse=True)

    for user in user_list:
        user.item_list = sorted(user.item_list, cmp=lambda x,y: cmp(x.name.lower(), y.name.lower()))
        user.item_list = sorted(user.item_list, key=lambda Item: Item.bought_price-Item.sold_price, reverse=True)

    for cnt in range(len(user_list)):
        if cnt == 0:
            user_list[cnt].rank = 1
            user_list[cnt].rank_str = "1"
            now_rank = 1
        else:
            if user_list[cnt-1].get_totalPrice() == user_list[cnt].get_totalPrice():
                user_list[cnt].rank = now_rank
                user_list[cnt].rank_str = u":::"
            else:
                user_list[cnt].rank = cnt + 1
                user_list[cnt].rank_str = str(cnt+1)
                now_rank = cnt + 1

        for cnt_item in range(len(user_list[cnt].item_list)):
            if cnt_item == 0:
                user_list[cnt].item_list[cnt_item].rank = 1
                user_list[cnt].item_list[cnt_item].rank_str = "1"
                now_rank = 1
            else:
                if user_list[cnt].item_list[cnt_item-1].bought_price - user_list[cnt].item_list[cnt_item-1].sold_price == user_list[cnt].item_list[cnt_item].bought_price - user_list[cnt].item_list[cnt_item].sold_price:
                    user_list[cnt].item_list[cnt_item].rank = now_rank
                    user_list[cnt].item_list[cnt_item].rank_str = u":::"
                else:
                    user_list[cnt].item_list[cnt_item].rank = cnt_item + 1
                    user_list[cnt].item_list[cnt_item].rank_str = str(cnt_item+1)
                    now_rank = cnt_item + 1

    return user_list

def main():

    user_list_last_month = get_user_list(sys.argv[1])
    user_list_this_month = get_user_list(sys.argv[2])

    print("===== " + sys.argv[3] + "年" + sys.argv[4] + "月度チェストショップ収益 =====")
    print u"  * <color red>↑</color><color blue>↓</color>は前回からの増減値です。\n"
    print u"^  順位  ^^  名前  ^  収益[円]  ^^^  売上  ^^  買取  ^^"
    print u"^:::^:::^:::^:::^:::^:::^  合計額 [円]  ^  個数 [個]  ^  合計額[円]  ^  個数[個]  ^"

    for y in user_list_this_month :

        flag_match = False

        for x in user_list_last_month:

            if x.name == y.name:
                delta_rank = x.rank - y.rank
                delta_totalPraice = y.get_totalPrice() - x.get_totalPrice()
                flag_match = True
                break

        if not flag_match:
            delta_rank = len(user_list_last_month) + 1 - y.rank
            delta_totalPraice = y.get_totalPrice()

        if delta_rank > 0:
            delta_rank_str = u"<color red><fs 90%>↑(" + str(delta_rank) + u")</fs></color>"
        elif delta_rank == 0:
            delta_rank_str = u" "
        else:
            delta_rank_str = u"<color blue><fs 90%>↓(" + str(int(math.fabs(delta_rank))) + u")</fs></color>"

        if delta_totalPraice > 0:
            delta_totalPraice_str = u"<color red><fs 90%>↑</fs></color>|  <color red><fs 90%>" + str('{:,d}'.format(delta_totalPraice)) + u"</fs></color>"
        elif delta_totalPraice == 0:
            delta_totalPraice_str = u" "
        else:
            delta_totalPraice_str = u"<color blue><fs 90%>↓</fs></color>|  <color blue><fs 90%>" + str('{:,d}'.format(int(math.fabs(delta_totalPraice)))) + u"</fs></color>"

        print u"|  " + y.rank_str + u"|" + \
            delta_rank_str + u"|" + \
            y.name + u"|  " + \
            str('{:,d}'.format(int(y.get_totalPrice()))) + u"|  " + \
            delta_totalPraice_str + u"|  " + \
            str('{:,d}'.format(int(y.get_totalUriagePrice()))) + u"|  " + \
            str('{:,d}'.format(int(y.get_totalUriageNum()))) + u"|  " + \
            str('{:,d}'.format(int(y.get_totalKaitoriPrice()))) + u"|  " + \
            str('{:,d}'.format(int(y.get_totalKaitoriNum()))) + u"|"

    for user in user_list_this_month:
        print ""
        print "----"
        print ""
        print "====" + user.name + " ===="
        print ""
        print u"^  順位  ^  商品  ^  収益[円]  ^  売上  ^^  買取  ^^"
        print u"^:::^:::^:::^  合計額 [円]  ^  個数 [個]  ^  合計額[円]  ^  個数[個]  ^"

        for item in user.item_list:
            print u"|  " + item.rank_str + u"|" + \
                item.name + u"|  " + \
                str('{:,d}'.format(int(item.bought_price - item.sold_price))) + u"|  " + \
                str('{:,d}'.format(int(item.bought_price))) + u"|  " + \
                str('{:,d}'.format(int(item.bought_num))) + u"|  " + \
                str('{:,d}'.format(int(item.sold_price))) + u"|  " + \
                str('{:,d}'.format(int(item.sold_num))) + u"|"
        print ""

    user_list_total = get_user_list("S:\\minecraft\\savasava\\logs\\2015-00")

    print u"===== 2015年4月～" + sys.argv[3] + u"年" + sys.argv[4] + u"月度チェストショップ収益 ====="
    print u"  * <color red>↑</color><color blue>↓</color>は前回からの増減値です。\n"
    print u"^  順位  ^  名前  ^  収益[円]  ^  売上  ^^  買取  ^^"
    print u"^:::^:::^:::^  合計額 [円]  ^  個数 [個]  ^  合計額[円]  ^  個数[個]  ^"

    for user in user_list_total:
        print u"|  " + user.rank_str + u"|" + \
            user.name + u"|  " + \
            str('{:,d}'.format(int(user.get_totalPrice()))) + u"|  " + \
            str('{:,d}'.format(int(user.get_totalUriagePrice()))) + u"|  " + \
            str('{:,d}'.format(int(user.get_totalUriageNum()))) + u"|  " + \
            str('{:,d}'.format(int(user.get_totalKaitoriPrice()))) + u"|  " + \
            str('{:,d}'.format(int(user.get_totalKaitoriNum()))) + u"|"

    for user in user_list_total:
        print ""
        print "----"
        print ""
        print "====" + user.name + " ===="
        print ""
        print u"^  順位  ^  商品  ^  収益[円]  ^  売上  ^^  買取  ^^"
        print u"^:::^:::^:::^  合計額 [円]  ^  個数 [個]  ^  合計額[円]  ^  個数[個]  ^"

        for item in user.item_list:
            print u"|  " + item.rank_str + u"|" + \
                item.name + u"|  " + \
                str('{:,d}'.format(int(item.bought_price - item.sold_price))) + u"|  " + \
                str('{:,d}'.format(int(item.bought_price))) + u"|  " + \
                str('{:,d}'.format(int(item.bought_num))) + u"|  " + \
                str('{:,d}'.format(int(item.sold_price))) + u"|  " + \
                str('{:,d}'.format(int(item.sold_num))) + u"|"
        print ""

if __name__ == '__main__':
    main()
