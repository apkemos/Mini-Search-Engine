# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import scrapy
import os

class FrontSpider(scrapy.Spider):

	name = "reuters"
	counter = 0

	#reuters first page
	start_urls = [
	'http://www.reuters.com/',
	]
	def parse(self, response):
		#read links in sever points of the site

		links = []
		for category in response.css('div.story-content'):
			links.append(category.css("a::attr(href)").extract())
		links2 = []
		for category in response.css('h3.article-heading'):
			links2.append(category.css("a::attr(href)").extract())
		links3 = []
		for category in response.css('h3.story-title'):
			links2.append(category.css("a::attr(href)").extract())

		links4 = []
		for category in response.css('div.story-photo'):
			links4.append(category.css("a::attr(href)").extract())

		#concatenate links
		links = links + links2 + links3 + links4

		#write all links to file writing (http://www...) where missing
		with open(os.getcwd() + "\\all_links.txt", 'w+') as f:
			for i in range(len(links)):
				for item in links[i]:
					self.counter += 1
					if item[0] == "h":
						f.write("{0} {1}".format(str(self.counter) , item) )
					else:
						f.write("{0} {1}".format(str(self.counter) , 'http://www.reuters.com' + item + '\n') )
												


class ArticleSpider(scrapy.Spider):

	name = "reuters2"
	counter = 0

	def start_requests(self):

		#read datafrom all_links.txt created by FrontSpider spider

		with open(os.getcwd() + '\\' + "all_links.txt") as f:
			content = f.readlines()
			#get urls      
		content = [x.rstrip('\n').split(' ')[1] for x in content]

		#save links to variable urls
		urls = content

		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)



	def parse(self, response):


		bodies = []
		#text is found i p tags
		bodies.append(response.css("p::text").extract())

			#counter that counts the links that have been executed and defines the name of the file     
		self.counter +=1						 
		fileName = os.getcwd() + '\\collection\\' +  str(self.counter) + ".txt"
		mapName = os.getcwd() + '\\collection\\' + "mapping.txt"

		#Save final text bodies to file

		with open(mapName, 'a+') as tf :
			tf.write("%s %s\n" % (self.counter , str(response.url) ))

		with open(fileName, 'w+') as f: 
			for i in range(len(bodies)):
				for item in bodies[i]:
					if item == '':
						continue
					f.write("%s\n" % item)
			