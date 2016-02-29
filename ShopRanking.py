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

	def set_name(self, name):
		self.name = name

	def set_bought_price(self, bought_price):
		self.bought_price = bought_price

	def set_bought_num(self, bought_num):
		self.bought_num = bought_num

	def set_sold_price(self, sold_price):
		self.sold_price = sold_price

	def set_sold_num(self, sold_num):
		self.sold_num = sold_num

	def get_name(self):
		return self.name

	def get_bought_price(self):
		return self.bought_price

	def get_bought_num(self):
		return self.bought_num

	def get_sold_price(self):
		return self.sold_price

	def get_sold_num(self):
		return self.sold_num

class User:
	name = ""
	rank = 0
	rank_str = ""

	def __init__(self):
		self.item_list = []
		self.totalUriageNum = 0
		self.totalKaitoriNum = 0
		self.totalUriagePrice = 0
		self.totalKaitoriPrice = 0
		self.totalPrice = 0

	def set_name(self, name):
		self.name = name
	
	def set_rank(self, rank):
		self.rank = rank

	def set_rank_str(self, rank_str):
		self.rank_str = rank_str
	
	def get_name(self):
		return self.name
		
	def get_rank(self):
		return self.rank

	def get_rank_str(self):
		return self.rank_str

	def add_item(self, item):
		flag = False
		for x in self.item_list:
			if x.get_name() == item.get_name():
				x.set_bought_num(x.get_bought_num() + item.get_bought_num())
				x.set_bought_price(x.get_bought_price() + item.get_bought_price())
				x.set_sold_num(x.get_sold_num() + item.get_sold_num())
				x.set_sold_price(x.get_sold_price() + item.get_sold_price())
				flag = True
				return
		if flag == False:
			self.item_list.append(item)

	def get_item(self):
			return self.item_list[0]

	def get_item_list(self):
			return self.item_list

class User_list:
	user_list = []
	
	def add_user(self, user):
		flag = False
		for x in self.user_list:
			if x.get_name() == user.get_name():
				x.add_item(user.get_item())
				flag = True
				return
		if flag == False:
			self.user_list.append(user)
	
	def get_user_list(self):
		return self.user_list
	
argvs = sys.argv
argc = len(argvs)

user_list = User_list()
for dirpath, dirs, files in os.walk(argvs[1]):
	for fn in files:
		path = os.path.join(dirpath, fn)
		f = file(path, 'r')
		for line in f:
			if " bought " in line:
				bought_item = Item()
				string = line.split(" ")
				bought_item.set_bought_num(int(string[6]))
				if string[8] == "for":
					bought_item.set_name(string[7])
					next_index = 9
				elif string[9] == "for":
					bought_item.set_name(string[7] + " " + string[8])
					next_index = 10
				elif string[10] == "for":
					bought_item.set_name(string[7] + " " + string[8] + " " + string[9])
					next_index = 11
				elif string[11] == "for":
					bought_item.set_name(string[7] + " " + string[8] + " " + string[9]+ " " + string[10])
					next_index = 12				
				bought_item.set_bought_price(int(float(string[next_index])))
				next_index += 2
				user = User()
				user.set_name(string[next_index])
				user.add_item(bought_item)
				
				user_list.add_user(user)
			elif " sold " in line:
				sold_item = Item()
				string = line.split(" ")
				sold_item.set_sold_num(int(string[6]))
				if string[8] == "for":
					sold_item.set_name(string[7])
					next_index = 9
				elif string[9] == "for":
					sold_item.set_name(string[7] + " " + string[8])
					next_index = 10
				elif string[10] == "for":
					sold_item.set_name(string[7] + " " + string[8] + " " + string[9])
					next_index = 11
				elif string[11] == "for":
					sold_item.set_name(string[7] + " " + string[8] + " " + string[9]+ " " + string[10])
					next_index = 12				
				sold_item.set_sold_price(int(float(string[next_index])))
				next_index += 2
				user = User()
				user.set_name(string[next_index])
				user.add_item(sold_item)

				user_list.add_user(user)
		f.close()

for user in user_list.get_user_list():
	for bought_item in user.get_item_list():
		user.totalUriageNum += bought_item.get_bought_num()
		user.totalUriagePrice += bought_item.get_bought_price()
		user.totalKaitoriNum += bought_item.get_sold_num()
		user.totalKaitoriPrice += bought_item.get_sold_price()
	user.totalPrice = user.totalUriagePrice - user.totalKaitoriPrice
	
sorted_user_list = sorted(user_list.get_user_list(), cmp=lambda x,y: cmp(x.get_name().lower(), y.get_name().lower()))
sorted_user_list = sorted(sorted_user_list, key=lambda User: User.totalKaitoriNum, reverse=True)
sorted_user_list = sorted(sorted_user_list, key=lambda User: User.totalUriageNum, reverse=True)
sorted_user_list = sorted(sorted_user_list, key=lambda User: User.totalKaitoriPrice, reverse=True)
sorted_user_list = sorted(sorted_user_list, key=lambda User: User.totalUriagePrice, reverse=True)
sorted_user_list = sorted(sorted_user_list, key=lambda User: User.totalPrice, reverse=True)

for user in user_list.get_user_list():
	user.item_list = sorted(user.get_item_list(), cmp=lambda x,y: cmp(x.get_name().lower(), y.get_name().lower()))
	user.item_list = sorted(user.get_item_list(), key=lambda Item: Item.get_sold_num(), reverse=True)
	user.item_list = sorted(user.get_item_list(), key=lambda Item: Item.get_sold_price(), reverse=True)
	user.item_list = sorted(user.get_item_list(), key=lambda Item: Item.get_bought_num(), reverse=True)
	user.item_list = sorted(user.get_item_list(), key=lambda Item: Item.get_bought_price(), reverse=True)
	user.item_list = sorted(user.get_item_list(), key=lambda Item: Item.get_bought_price()-Item.get_sold_price(), reverse=True)

print "===== 2015年4月～" + argvs[2] + "年" + argvs[3] + "月度チェストショップ収益 ====="
print "^  No.  ^  名前  ^  収益[円]  ^  売上  ^^  買取  ^^"
print "^:::^:::^:::^  合計額 [円]  ^  個数 [個]  ^  合計額[円]  ^  個数[個]  ^"
cnt = 1
for user in sorted_user_list:
	print "|  " + str(cnt) + "|" + \
		user.get_name() + "|  " + \
		str('{:,d}'.format(int(user.totalPrice))) + "|  " + \
		str('{:,d}'.format(int(user.totalUriagePrice))) + "|  " + \
		str('{:,d}'.format(int(user.totalUriageNum))) + "|  " + \
		str('{:,d}'.format(int(user.totalKaitoriPrice))) + "|  " + \
		str('{:,d}'.format(int(user.totalKaitoriNum))) + "|"
	cnt += 1

for user in sorted_user_list:

	print ""
	print "----"
	print ""
	print "====" + user.get_name() + " ===="
	print ""

	cnt = 1	
	if len(user.get_item_list()) >= 1:
		print "^  No.  ^  商品  ^  収益[円]  ^  売上  ^^  買取  ^^"
		print "^:::^:::^:::^  合計額 [円]  ^  個数 [個]  ^  合計額[円]  ^  個数[個]  ^"
		for bought_item in user.get_item_list():
			print "|  " + str(cnt) + "|" + \
				bought_item.get_name() + "|  " + \
				str('{:,d}'.format(int(bought_item.get_bought_price() - bought_item.get_sold_price()))) + "|  " + \
				str('{:,d}'.format(int(bought_item.get_bought_price()))) + "|  " + \
				str('{:,d}'.format(int(bought_item.get_bought_num()))) + "|  " + \
				str('{:,d}'.format(int(bought_item.get_sold_price()))) + "|  " + \
				str('{:,d}'.format(int(bought_item.get_sold_num()))) + "|"
			cnt += 1
	print ""
