#-*- coding:utf-8 -*-
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from sklearn import linear_model
import re
import csv
import traceback
import time
import os
import numpy as np
import pandas as pd
import sklearn

def main():
	"""
	メイン処理
	クロール、CSV出力、CSV内容変更、分析を順に行う
	最終的なアウトプットは東京都の不動産価格の重回帰によるモデルと、
	調査対象のうち、上下に一番外れている物件の情報
	"""
	#url="http://www.fudousan.or.jp/system/?act=f&type=31&pref=13&stype=l"
	url="https://suumo.jp/chintai/tokyo/city/"
	crawl_and_csv_writer(url)
	print("station changer will begin")
	station_price_changer()
	print("regression will begin")
	regression()

def crawl_and_csv_writer(url):
	driver=webdriver.PhantomJS()
	driver.implicitly_wait(10)
	driver.get(url)

	#エリア検索　２３区
	#for line in range(1,24):
	#エリアを絞る
	#千代田、中央、港、新宿、文京、墨田、品川、目黒、世田谷、渋谷
	for line in (1,2,3,4,5,7,9,10,12,13):
		driver.find_element_by_xpath('//*[@id="la131' + str(line).zfill(2) + '"]').click()

	#金額(下限なし) default

	#金額
	#driver.find_element_by_xpath("//select[@name='ct']/option[@value='12.0']").click()
	driver.find_element_by_xpath("//select[@name='ct']/option[@value='15.0']").click()

	#最寄駅(15分以内)
	driver.find_element_by_xpath('//*[@id="et4"]').click()

	#間取り
	#driver.find_element_by_xpath('//*[@id="md1"]').click() #1K
	#driver.find_element_by_xpath('//*[@id="md2"]').click() #1DK
	#driver.find_element_by_xpath('//*[@id="md3"]').click() #1LDK
	driver.find_element_by_xpath('//*[@id="md4"]').click() #2K
	driver.find_element_by_xpath('//*[@id="md5"]').click() #2DK
	driver.find_element_by_xpath('//*[@id="md6"]').click() #2LDK
	driver.find_element_by_xpath('//*[@id="md7"]').click() #3K
	driver.find_element_by_xpath('//*[@id="md8"]').click() #3DK
	driver.find_element_by_xpath('//*[@id="md9"]').click() #3LDK
	driver.find_element_by_xpath('//*[@id="md10"]').click() #4K
	driver.find_element_by_xpath('//*[@id="md11"]').click() #4DK
	driver.find_element_by_xpath('//*[@id="md12"]').click() #4LDK
	driver.find_element_by_xpath('//*[@id="md13"]').click() #<5K

	#物件種別
	driver.find_element_by_xpath('//*[@id="ts0"]').click() #mansion
	driver.find_element_by_xpath('//*[@id="ts1"]').click() #apartment
	driver.find_element_by_xpath('//*[@id="ts2"]').click() #others

	#年数(15年未満)
	#driver.find_element_by_xpath('//*[@id="cn0"]').click() #new
	#driver.find_element_by_xpath('//*[@id="cn1"]').click() #less than 1 year
	#driver.find_element_by_xpath('//*[@id="cn2"]').click() #less than 3 years
	#driver.find_element_by_xpath('//*[@id="cn3"]').click() #less than 5 years
	#driver.find_element_by_xpath('//*[@id="cn4"]').click() #less than 7 years
	#driver.find_element_by_xpath('//*[@id="cn5"]').click() #less than 10 years
	driver.find_element_by_xpath('//*[@id="cn6"]').click() #less than 15 years
	#driver.find_element_by_xpath('//*[@id="cn7"]').click() #less than 20 years
	#driver.find_element_by_xpath('//*[@id="cn8"]').click() #less than 25years
	#driver.find_element_by_xpath('//*[@id="cn9"]').click() #less than 30years
	#driver.find_element_by_xpath('//*[@id="cn10"]').click() #not selected

	#面積
	driver.find_element_by_xpath("//select[@name='mb']/option[@value='50']").click()

	#バス・トイレ別
	driver.find_element_by_xpath('//*[@id="tc0"]').click()
	#部屋の位置(二階以上)
	driver.find_element_by_xpath('//*[@id="tc1"]').click()
	#宅配ボックス
	driver.find_element_by_xpath('//*[@id="tc96"]').click()
	#ゴミ置き場あり
	driver.find_element_by_xpath('//*[@id="tc97"]').click()

	#サブミット
	driver.find_element_by_xpath('//*[@id="js-searchpanel"]/div/div/a').click()

	#ページ件数変更(100件)
	#driver.find_element_by_xpath('//*[@id="cont"]/table[3]/tbody/tr[2]/td/table/tbody/tr[2]/td[1]/p/select/option[3]').click()

	#新着順に表示変更
	#driver.find_element_by_xpath('//*[@id="cont"]/table[3]/tbody/tr[2]/td/table/tbody/tr[3]/td/p/a[1]').click()

	#ページ読み込み
	time.sleep(5)
	bs = BeautifulSoup(driver.page_source, "lxml")

	#不動産件数
	#page = driver.find_element_by_class_name("paginate_set-hit")
	#page = bs.findAll(match_class("paginate_set-hit"))
	currentURL = driver.current_url
	print(currentURL)
	driver.get(currentURL)
	#page = driver.find_element_by_xpath('//div[5]/div[1]/div[2]/div[1]/div[1]/form[4]/div[2]/div[2]/div[1]')
	##page = driver.find_element_by_xpath('//*[@id="js-leftColumnForm"]/div[2]/div[2]/div[1]')
	#house_count = str(page.text)
	#house_count = house_count.replace(u'　', '')
	#house_count = house_count.replace(u' ', '')

	#regex = u'<span>.*'
	#house_count = re.sub(regex, "", house_count)
	#house_count = int(house_count)
	#print("house count ",house_count)

	#最終ページ数
	#maxPage = (house_count - (house_count % 100)) / 100 + 2
	maxPage = 1

	with open("./house_data.csv","w") as fp:
		header=["家賃","最寄駅","徒歩","管理費","共益費","広さ","築年数","階数","契約期間","敷金","礼金","更新料","URL"]
		writer=csv.writer(fp,lineterminator='\n')
		writer.writerow(header)

		try:
			for page in range(1,int(maxPage)):
				#最終ページのみ掲載数が少ないので、掲載数を変数にする
				if page == int(maxPage -1):
					listed_house_number = int(house_count % 100)
					listed_house_number = int(listed_house_number + 4)
				else:
					listed_house_number = 103

				for line in range(4,listed_house_number):
					csvArray=[]
					driver.find_element_by_xpath('//*[@id="js-bukkenList"]/ul/li[1]/div[1]/div[2]/table/tbody/tr[1]/td[8]/a').click()
					#WebDriverWait(driver,10).until(expected_conditions.text_to_be_present_in_element((By.XPATH,'//*[@id="cont"]/h4'),u'物件詳細'))
					time.sleep(1)

					#家賃(rent)
					rent = driver.find_element_by_xpath('//*[@id="cont"]/div[3]/span[1]')
					rent = str(rent.text)
					rent = rent.replace('賃料  ','')
					rent = price_format_changer(rent)
					csvArray.append(rent)

					bs=BeautifulSoup(driver.page_source, "lxml")
					data=[x for x in bs.findAll("td")]

					#最寄駅、徒歩(station, walk)
					location = data[2].p.text
					r1 = re.compile("徒歩(\w+)分")
					r2 = re.compile("「(.+?)」")
					walk = r1.search(location).group(1)
					station = r2.search(location).group(1)
					csvArray.append(station)
					csvArray.append(walk)

					#管理費、共益費(administrative expense, common service expense)
					monthly_fee = data[3].p.text
					if('なし' in monthly_fee):
						monthly_fee = monthly_fee.replace('なし','0')
					elif('-' in monthly_fee):
						monthly_fee = monthly_fee.replace('-', '0')
					monthly_fee = price_format_changer(monthly_fee)

					if('共益' in monthly_fee):
						cse = monthly_fee.split('共益費:')[1]
						ae = monthly_fee.split('共益費:')[0].replace('管理費:','')
					else:
						cse = '0'
						ae = monthly_fee.replace('管理費:','')
					csvArray.append(cse)
					csvArray.append(ae)

					#広さ
					csvArray.append(data[10].p.text.replace('㎡ ',''))

					#築月数(建設年月日から月単位で2017年4月から引いて計算)
					dat = data[11].p.text
					year = int(dat.split('年')[0])
					mon = int(dat.split('年')[1].replace('月',''))
					built = (2017 - year) * 12 + 4 - mon
					csvArray.append(built)

					#階数
					csvArray.append(re.sub(r'階.*','',data[13].p.text))

					#契約期間
					duration = data[21].p.text
					duration = span_format_changer(duration)
					csvArray.append(duration)

					#敷金、礼金(security deposit, key money)
					sd = data[4].p.text.split('・')[0]
					sd = exists_checker(sd, rent)
					if(sd == "else"):
						break
					csvArray.append(sd)

					km = data[4].p.text.split('・')[1]
					km = exists_checker(km, rent)
					if(km == "else"):
						break
					csvArray.append(km)

					#更新料
					rf = data[24].p.text
					if ('-' in rf):
						rf = '0'
					if('ヶ月' in rf):
						rf = rf.replace('ヶ月', '')
					csvArray.append(rf)

					#URL
					url = driver.current_url
					r3 = re.compile("pref=(.*)&s=n")
					param = r3.search(url).group(0)
					url = url.replace(param, '')
					csvArray.append(url)

					writer=csv.writer(fp,lineterminator='\n')
					writer.writerow(csvArray)

					driver.back()
					time.sleep(1)
				if (page < int(maxPage -1)):
					driver.find_element_by_xpath('//*[@id="cont"]/table[3]/tbody/tr[2]/td/table/tbody/tr[1]/td/p/a[' + str(page) + ']').click()
				time.sleep(1)
		except:
			print(traceback.format_exc())
			pass

def price_format_changer(fee):
	"""
	家賃、管理費共益費のフォーマットを変更する
	"""
	if ('万円' in fee ):
		fee = fee.replace('万円','0000')
	else:
		fee = fee.replace(',','')
		fee = fee.replace('万','')
		fee = fee.replace('円','')
	return fee

def exists_checker(fee, rent):
	"""
	敷金礼金の有無、金額のフォーマットを変更する
	"""
	regex = re.compile("([\d\.]+)ヶ月(.*)")
	if('敷金なし' in fee):
		fee = fee.replace('敷金なし', '0')
	elif('礼金なし' in fee):
		fee = fee.replace('礼金なし', '0')
	elif('-' in fee):
		fee = '0'
	elif(re.match(regex, fee)):
		fee = regex.search(fee).group(1)
	elif('万円' in fee):
		fee = fee.replace('万円','')
	else:
		fee = "else"
	return fee

def span_format_changer(span):
	regex_year = re.compile("(\d+)年")
	regex_month = re.compile("(\d+)ヶ月")
	year = 0
	month = 0
	if('期間' in span):
		span = span.replace('期間:','')
	if('-' in span):
		span = span.replace('-', '0')
	elif('年' in span):
		year = regex_year.search(span).group(1)
		year = int(year)
		if('ヶ月' in span):
			month = regex_month.search(span).group(1)
			month = round(int(month)/12, 1)
		span = year + month
	elif('ヶ月' in span):
		month = regex_month.search(span).group(1)
		month = round(int(month)/12, 1)
		span = year + month
	return span

def station_price_changer():
	"""
	最寄り駅の情報から坪単価の情報に編集
	"""
	header=["rent","station_price","walk","cse","ae","area","built_month","floor","contract_period","sd","km","renewal_fee"]
	with open('station_price.csv', 'r') as infile:
		reader = csv.reader(infile)
		with open('station_price_dict.csv', 'w') as outfile:
			for row in reader:
				station_price = {row[0]:row[1] for row in reader}

		with open('house_data.csv', 'r') as fp:
			crawler_result = csv.reader(fp)
			next(reader, None)
			with open('house_data_with_price.csv', 'w') as fw:
				writer = csv.writer(fw)
				writer.writerow(header)
				for row in crawler_result:
					if row[1] in station_price.keys():
						row[1] = station_price[row[1]]
						writer.writerow(row[0:12])
	os.remove('station_price_dict.csv')

def regression():
	"""
	家賃を除く変数を説明変数として重回帰分析実施
	得られた式と、最もパフォーマンスの良い物件と悪い物件を出力
	"""
	house = pd.read_csv("house_data_with_price.csv", sep=",")
	columns = house["rent"].count()

	clf = linear_model.LinearRegression()

	# 説明変数に "家賃を除く全て" を利用
	house_param = house.drop("rent", axis=1)

	X = house_param.as_matrix()

	# 目的変数に "家賃" を利用
	Y = house['rent'].as_matrix()

	# 予測モデルを作成
	clf.fit(X, Y)

	# 偏回帰係数
	df = pd.DataFrame({"Name":house_param.columns, "Coefficients":clf.coef_})
	print(df)
	coef_list = df["Coefficients"].tolist()
	name_list = df["Name"].tolist()
	coef_list.append(clf.intercept_)
	name_list.append("intercept")
	coef_list_round = []
	out = "y = "
	i = 0
	for value in coef_list:
		coef_list_round.append(round(value,8))
		out += "(" + str(round(value,8)) + ") * (" + str(name_list[i]) + ") + "
		i += 1

	out = out[0:-2]
	coef_list_round.pop()
	calc_x = np.asarray(coef_list_round)

	high = 0
	low = float("inf")

	for x in range(columns):
		calc_y_list = []
		for i in ("station_price","walk","cse","ae","area","built_month","floor","contract_period","sd","km","renewal_fee"):
			calc_y_list.append(house[i][x])
		calc_y = np.asarray(calc_y_list)
		total = np.dot(calc_x, calc_y)

		if total > high:
			high = total
			high_list = calc_y_list
			high_list.insert(0, house["rent"][x])
		if total < low:
			low = total
			low_list = calc_y_list
			low_list.insert(0, house["rent"][x])

	with open('house_data.csv', 'r') as infile:
		reader = csv.reader(infile)
		header = next(reader)
		outfile = open('output.csv', 'w')
		writer = csv.writer(outfile)
		writer.writerow([out])
		writer.writerow("")
		writer.writerow("best")
		writer.writerow(header)
		for row in reader:
			if int(row[0]) == int(low_list[0]):
				if int(row[2]) == int(low_list[2]):
					if float(row[5]) == float(low_list[5]):
						writer.writerow(row)
		writer.writerow("")
		writer.writerow("worst")
		for row in reader:
			if int(row[0]) == int(high_list[0]):
				if int(row[2]) == int(high_list[2]):
					if float(row[5]) == float(high_list[5]):
						writer.writerow(row)
		outfile.close()


if __name__ == '__main__':
	main()
