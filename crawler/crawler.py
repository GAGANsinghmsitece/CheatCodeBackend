import requests
import time
import re
import json
from bs4 import BeautifulSoup
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import 	Options

def GetProblemsList(opt):
	# finding total number of pages
	browser=Firefox(options=opt)
	current_page = 1
	total_page = 1
	browser.get("https://leetcode.com/problemset/all/?page={}".format(current_page))
	time.sleep(5)
	soup= BeautifulSoup(browser.page_source,'html.parser')
	result = soup.select('button.text-label-2.text-sm.flex.items-center.justify-center.w-8.h-8.rounded.select-none.text-sm.bg-fill-3.text-label-2.items-center.justify-center.w-8.h-8.rounded.select-none.text-sm.bg-fill-3.text-label-2')
	for content in result:
		if content.text != "":
			total_page = int(content.text)
	problem_links=[]
	for x in range(1,total_page):
		browser.get("https://leetcode.com/problemset/all/?page={}".format(x))
		time.sleep(5)
		soup = BeautifulSoup(browser.page_source,'html.parser')
		problems = soup.select('a.h-5')
		premium = soup.select("a.opacity-60")
		for problem in problems:
			if problem in premium:
				problems.remove(problem)
		for problem in problems:
			problem_links.append('https://leetcode.com{}'.format(problem['href']))
	browser.quit()
	return problem_links

def ConvertToJSON(data,tag):
	problems=[]
	tags=[]
	for p in data:
		problems.append(p)
	for t in tag:
		tags.append(t)
	res={
		"problems":problems,
		"tags":tags
	}
	return res

def SaveToFile(data,filename):
	with open(filename,'w') as f:
		json.dump(data,f,ensure_ascii=False,indent=4)

def GetProblemDetails(problem_link,browser):
	browser.implicitly_wait(5)
	browser.get(problem_link)
	time.sleep(4)
	soup = BeautifulSoup(browser.page_source,'html.parser')

	headingContainer = soup.find('div',class_='css-v3d350')
	descriptionContainer = soup.find('div',class_='question-content__JfgR')
	difficultyContainer = soup.find('div',class_='css-10o4wqw')
	likeContainer = soup.find_all('button',class_='css-1rdgofi')
	tags_container = soup.find_all('span',class_='tag__24Rd')


	if headingContainer is not None and descriptionContainer is not None and difficultyContainer is not None and likeContainer is not None and tags_container is not None:
		heading = headingContainer.text
		description = str(descriptionContainer.findChildren())
		difficulty = difficultyContainer.findChildren()[0].text
		like = likeContainer[0].text
		unlike = likeContainer[1].text
		tags=[]

		for tag in tags_container:
			tags.append({'name':tag.text})
		data={
			'heading':heading,
			'description':description,
			'difficulty':difficulty,
			'like':like,
			'unlike':unlike,
			'tags':tags,
			'link':problem_link
		}
		return data
	


def init():
	opt=Options()
	opt.headless=True
	browser=Firefox(options=opt)
	problem_links=GetProblemsList(opt)
	data={}
	for x in range(len(problem_links)):
		data[str(x)]=problem_links[x]
	SaveToFile(data,'problems.json')
	f=open('problems.json')
	problem_data = json.load(f)
	tags=[]
	problems=[]
	for key in problem_data:
		data=GetProblemDetails(problem_data[key],browser)
		if data is None:
			continue
		print(data['heading'])
		for tag in data['tags']:
			tags.append(tag)
		problems.append(data)
	final_response=ConvertToJSON(problems,tags)
	SaveToFile(final_response,'data.json')
	browser.quit()
	
init()