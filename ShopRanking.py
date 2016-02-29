# coding: utf-8

import sys
import os

class Item:

    def __init__(self):
        self.name = ""
        self.bought_price = 0
        self.bought_num = 0
        self.sold_price = 0
        self.sold_num = 0

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
    user_list = sorted(user_list, key=lambda User: User.get_totalKaitoriNum(), reverse=True)
    user_list = sorted(user_list, key=lambda User: User.get_totalUriageNum(), reverse=True)
    user_list = sorted(user_list, key=lambda User: User.get_totalKaitoriPrice(), reverse=True)
    user_list = sorted(user_list, key=lambda User: User.get_totalUriagePrice(), reverse=True)
    user_list = sorted(user_list, key=lambda User: User.get_totalPrice(), reverse=True)

    for user in user_list:
        user.item_list = sorted(user.item_list, cmp=lambda x,y: cmp(x.name.lower(), y.name.lower()))
        user.item_list = sorted(user.item_list, key=lambda Item: Item.sold_num, reverse=True)
        user.item_list = sorted(user.item_list, key=lambda Item: Item.sold_price, reverse=True)
        user.item_list = sorted(user.item_list, key=lambda Item: Item.bought_num, reverse=True)
        user.item_list = sorted(user.item_list, key=lambda Item: Item.bought_price, reverse=True)
        user.item_list = sorted(user.item_list, key=lambda Item: Item.bought_price-Item.sold_price, reverse=True)

    return user_list

def main():

    user_list = get_user_list(sys.argv[1])

    print u"===== 2015年4月～" + sys.argv[2] + u"年" + sys.argv[3] + u"月度チェストショップ収益 ====="
    print u"^  No.  ^  名前  ^  収益[円]  ^  売上  ^^  買取  ^^"
    print u"^:::^:::^:::^  合計額 [円]  ^  個数 [個]  ^  合計額[円]  ^  個数[個]  ^"

    for cnt, user in enumerate(user_list):
        print u"|  " + str(cnt) + u"|" + \
            user.name + u"|  " + \
            str('{:,d}'.format(int(user.get_totalPrice()))) + u"|  " + \
            str('{:,d}'.format(int(user.get_totalUriagePrice()))) + u"|  " + \
            str('{:,d}'.format(int(user.get_totalUriageNum()))) + u"|  " + \
            str('{:,d}'.format(int(user.get_totalKaitoriPrice()))) + u"|  " + \
            str('{:,d}'.format(int(user.get_totalKaitoriNum()))) + u"|"

    for cnt, user in enumerate(user_list):
        print ""
        print "----"
        print ""
        print "====" + user.name + " ===="
        print ""
        print u"^  No.  ^  商品  ^  収益[円]  ^  売上  ^^  買取  ^^"
        print u"^:::^:::^:::^  合計額 [円]  ^  個数 [個]  ^  合計額[円]  ^  個数[個]  ^"

        for item in user.item_list:
            print u"|  " + str(cnt) + u"|" + \
                item.name + u"|  " + \
                str('{:,d}'.format(int(item.bought_price - item.sold_price))) + u"|  " + \
                str('{:,d}'.format(int(item.bought_price))) + u"|  " + \
                str('{:,d}'.format(int(item.bought_num))) + u"|  " + \
                str('{:,d}'.format(int(item.sold_price))) + u"|  " + \
                str('{:,d}'.format(int(item.sold_num))) + u"|"
        print ""

if __name__ == '__main__':
    main()