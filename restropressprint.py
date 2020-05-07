import pyzmail
import urllib3
import pprint
import requests
from imapclient import IMAPClient
import re
from bs4 import BeautifulSoup
from escpos.printer import Network


#imgkit options
options = {
	'width': '300'
}

##defind kitchen printer settings
kitchen = Network("192.168.16.80") #Printer IP Address

##define Mail Login
HOST = ''
USERNAME = ''
PASSWORD = ''

#Define wp login details
wp_login = ''
username = ''
password = ''


#Functiontime Baby

def getmail():
	server = IMAPClient(HOST, use_uid=True, ssl=True)
	server.login(USERNAME, PASSWORD)
	select_info = server.select_folder('INBOX')
	unseenMessages = server.search(['UNSEEN'])
	 
	rawMessage = server.fetch(unseenMessages, ['BODY[]', 'FLAGS']) 

	returnmail = []
	for msgNum in unseenMessages:
	    message = pyzmail.PyzMessage.factory(rawMessage[msgNum][b'BODY[]'])
	    text = message.html_part.get_payload().decode(message.html_part.charset)
	    returnmail.append(text)
	return returnmail

def getorderurl(url_dictionary):
	linkstoreturn = []
	for x in url_dictionary:
		#print(x)
		#x.replace("\r", "").replace("\t", "")
		#print(x)
		soup = BeautifulSoup(x,features="lxml")
		for a in soup.find_all("a", text=re.compile('browser')):
	   		link = a['href']
	   		linkstoreturn.append(link)
	return linkstoreturn

def getorderlist(url_list):
	orderlist = []
	paymentinfo = []
	for n in url_list:
		text = login(n)	
		soup = BeautifulSoup(text,features="lxml")
		food_list = soup.find(id="rpress_purchase_receipt_products")
		orderlist.append(food_list)
		payment_list = soup.find(id="rpress_purchase_receipt")
		paymentinfo.append(payment_list)

	return paymentinfo, orderlist

def login(input_link):
	with requests.Session() as s:
		linknew = input_link
		headers1 = { 'Cookie':'wordpress_test_cookie=WP Cookie check' }
		datas={'log':username, 'pwd':password, 'wp-submit':'Log In','redirect_to':linknew, 'testcookie':'1'}
		s.post(wp_login, headers=headers1, data=datas)
		resp = s.get(linknew)	
		return resp.text

def kitchenorderprint(order):
	soup = BeautifulSoup(str(order),features="lxml")
	kitchen.text('\n')
	for a in soup.find_all('div', class_="rpress_purchase_receipt_product_name"):
		#print(a)
		plainorder = a.get_text()
		finaltext = re.sub(r'\(.*?\)', '', plainorder)
		finaltext = re.sub(r'	', '', finaltext)
		finaltext = re.sub(r'  ', '--', finaltext)
		kitchen.text(finaltext)

		#print(finaltext)
		#kitchen.text(finaltext)
	kitchen.text('\n \n \n \n \n')
	kitchen.cut()

def paymentinfoprint(payment_info):
	soup = BeautifulSoup(str(payment_info),features="lxml")
	#kitchen.text('\n')
	#print(a)
	plainorder = soup.get_text()
	finaltext = re.sub(r'\(.*?\)', '', plainorder)
	finaltext = re.sub(r'	', '', finaltext)
	finaltext = re.sub(r'  ', '--', finaltext)
	finaltext = re.sub(r'\n\n', '', finaltext)
	finaltext = re.sub(r'\n\n\n', '', finaltext)
	finaltext = re.sub(r'\n\n\n\n', '', finaltext)
	finaltext = re.sub(r'\n\n\n\n\n', '', finaltext)
	print(finaltext)
	kitchen.text(finaltext)

def printfunctions(paymentinfo,orderlist):
	x = 0
	for x in range(len(paymentinfo)):
		paymentinfoprint(paymentinfo[x])
		kitchenorderprint(orderlist[x])



while True:
	output = getmail()
	if len(output) != 0:
		links = getorderurl(output)
		paymentinfo, orderlist = getorderlist(links)
		#paymentinfoprint(paymentinfo)
		#kitchenorderprint(orderlist)
		printfunctions(paymentinfo,orderlist)
	time.sleep(5)





