import requests
import json
import urllib.parse
import os
import pdfkit
import shutil
import random

from multiprocessing import Process
from time import sleep
from urllib.request import urlopen
from bs4 import BeautifulSoup

'''
EXAMPLE
match_str = ['테스트', '테스트2']
'''
match_str = ['#match_str']

def urlencode(str):
	return urllib.parse.quote(str)


def search_subject_content(result):
	title = ''
	body = ''

	search_str = result.findAll("span", {"class":"title_subject"})
	for title in search_str:
		title = title.get_text()

	search_str = result.findAll("div", {"class":"gallview_contents"})
	for body in search_str:
		body = body.get_text()

	return (title+body)


def save_to_pdf(URL, pagenum):
	config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')
	options = {
		'custom-header': [
			('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36')
			]
	}
	try:
		pdfkit.from_url(URL, './'+str(pagenum)+'.pdf', configuration=config, options=options)
	except:
		return


def dcinside_search(target_URL, pagenum):
	URL = target_URL+str(pagenum)

	title = ''
	body = ''

	try:
		req = urllib.request.Request(URL, data=None, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
		response = urllib.request.urlopen(req)
	except:
		print("------ Error at #"+str(pagenum)+" ------")
		return

	result = BeautifulSoup(response,'html.parser')
	text = search_subject_content(result)

	for i, target_str in enumerate(match_str):
		check_found = text.find(target_str)
		if check_found != -1:
			print('------ Found : ' + URL + '------')
			archive = requests.get('https://web.archive.org/save/'+URL)
			sleep(0.5)
			try:
				check_archive = requests.get('http://archive.org/wayback/available?url='+urlencode(URL))
			except:
				return
			check_archive = check_archive.json()
			
			if 'closest' in check_archive['archived_snapshots']:
				if check_archive['archived_snapshots']['closest']['status'] == '200':
					f = open("./"+str(pagenum)+'.txt','w')
					f.write(check_archive['archived_snapshots']['closest']['url'])
					f.close()

			save_to_pdf(URL, pagenum)


def indexer(start_page, end_page):
	tmp = (end_page - start_page) // 4
	return tmp, [start_page, end_page-(tmp*3), end_page-(tmp*2), end_page-tmp]


def start_searching(target_URL, pagenum, size):
	for i in range(pagenum, pagenum+size):
		dcinside_search(target_URL, i)
		sleep(random.random())


def main():
	'''
	EXAMPLE
	target_URL = 'https://gall.dcinside.com/board/view/?id=iu_new&no='
	'''
	target_URL = '#target_URL'
	start_page = 1
	end_page = 100

	size, page_num = indexer(start_page, end_page)
	procs = []

	for index, num in enumerate(page_num):
		proc = Process(target=start_searching, args=(target_URL, num, size, ), daemon=True)
		procs.append(proc)
		proc.start()

	for proc in procs:
		proc.join()


if __name__ == "__main__":
	main()
