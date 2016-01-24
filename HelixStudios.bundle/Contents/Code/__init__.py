#HelixStudios
import re, os, urllib
PLUGIN_LOG_TITLE='Helix Studios'	# Log Title

VERSION_NO = '2016.01.24.1'

REQUEST_DELAY = 0					# Delay used when requesting HTML, may be good to have to prevent being banned from the site

# URLS
BASE_URL='https://www.helixstudios.net%s'

# Example Video Details URL
# https://www.helixstudios.net/video/3437/hosing-him-down.html
BASE_VIDEO_DETAILS_URL='https://www.helixstudios.net/video/%s'

# Example Search URL: 
# https://www.helixstudios.net/videos/?q=Hosing+Him+Down
BASE_SEARCH_URL='https://www.helixstudios.net/videos/?q=%s'

# Example File Name:
# https://media.helixstudios.com/scenes/hx111_scene2/hx111_scene2_member_1080p.mp4
# FILENAME_PATTERN = re.compile("")
# TITLE_PATTERN = re.compile("")

ENCLOSING_DIRECTORY_LIST=["Helix"]

def Start():
	HTTP.CacheTime = CACHE_1WEEK
	HTTP.Headers['User-agent'] = 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.2; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0)'

class HelixStudios(Agent.Movies):
	name = 'Helix Studios'
	languages = [Locale.Language.NoLanguage, Locale.Language.English]
	primary_provider = False
	contributes_to = ['com.plexapp.agents.cockporn']

	def Log(self, message, *args):
		if Prefs['debug']:
			Log(message, *args)

	def search(self, results, media, lang, manual):
		self.Log('-----------------------------------------------------------------------')
		self.Log(PLUGIN_LOG_TITLE + ' - SEARCH CALLED v.%s', VERSION_NO)
		self.Log(PLUGIN_LOG_TITLE + ' - SEARCH - media.title -  %s', media.title)
		self.Log(PLUGIN_LOG_TITLE + ' - SEARCH - media.items[0].parts[0].file -  %s', media.items[0].parts[0].file)
		self.Log(PLUGIN_LOG_TITLE + ' - SEARCH - media.primary_metadata.title -  %s', media.primary_metadata.title)
		self.Log(PLUGIN_LOG_TITLE + ' - SEARCH - media.items -  %s', media.items)
		self.Log(PLUGIN_LOG_TITLE + ' - SEARCH - media.filename -  %s', media.filename)
		self.Log(PLUGIN_LOG_TITLE + ' - SEARCH - lang -  %s', lang)
		self.Log(PLUGIN_LOG_TITLE + ' - SEARCH - manual -  %s', manual)

		if media.items[0].parts[0].file is not None:
			path_and_file = media.items[0].parts[0].file
			self.Log(PLUGIN_LOG_TITLE + ' - SEARCH - File Path: %s' % path_and_file)
			path_and_file = os.path.splitext(path_and_file)[0]
			enclosing_directory, file_name = os.path.split(path_and_file)
			enclosing_directory, enclosing_folder = os.path.split(enclosing_directory)
			self.Log(PLUGIN_LOG_TITLE + ' - SEARCH - Enclosing Folder: %s' % enclosing_folder[:5])
			# Check if enclosing directory matches an element in the directory list.
			if enclosing_folder[:5] in ENCLOSING_DIRECTORY_LIST:
				self.Log(PLUGIN_LOG_TITLE + ' - SEARCH - File Name: %s' % file_name)
				self.Log(PLUGIN_LOG_TITLE + ' - SEARCH - Split File Name: %s' % file_name.split(' '))

				remove_words = file_name.lower()
				remove_words = remove_words.replace('helix studios', '')
				remove_words = remove_words.replace('helixstudios', '')
				remove_words = re.sub('\(([^\)]+)\)', '', remove_words)
				remove_words = remove_words.lstrip(' ')
				remove_words = remove_words.rstrip(' ')
				search_query_raw = list()
				# Process the split filename to remove words with special characters. This is to attempt to find a match with the limited search function(doesn't process any non-alphanumeric characters correctly)
				for piece in remove_words.split(' '):
					if re.search('^[0-9A-Za-z]*$', piece.replace('!', '')) is not None:
						search_query_raw.append(piece)
				search_query="+".join(search_query_raw)
				self.Log(PLUGIN_LOG_TITLE + ' - SEARCH - Search Query: %s' % search_query)
				html=HTML.ElementFromURL(BASE_SEARCH_URL % search_query, sleep=REQUEST_DELAY)
				search_results=html.xpath('//*[@class="video-gallery"]/li')
				score=10
				# Enumerate the search results looking for an exact match. The hope is that by eliminating special character words from the title and searching the remainder that we will get the expected video in the results.
				if search_results:
					for result in search_results:
						video_title=result.find('a').find("img").get("alt")
						self.Log(PLUGIN_LOG_TITLE + ' - SEARCH - video title: %s' % video_title)
						video_url=result.find('a').get('href')
						self.Log(PLUGIN_LOG_TITLE + ' - SEARCH - video url: %s' % video_url)
						# Check the alt tag which includes the full title with special characters against the video title. If we match we nominate the result as the proper metadata. If we don't match we reply with a low score.
						video_title = re.sub("[\:\?\|\#]", '', video_title)
						video_title = re.sub("\s{2,4}", ' ', video_title)
						if video_title.lower() == file_name.lower():
							self.Log(PLUGIN_LOG_TITLE + ' - SEARCH - Exact Match: \'' + file_name.lower() + '\' == \'%s\'' % video_title.lower())
							results.Append(MetadataSearchResult(id = video_url, name = video_title, score = 100, lang = lang))
							return
						else:
							score=score-1
							results.Append(MetadataSearchResult(id = video_url, name = video_title, score = score, lang = lang))
				else:
					search_query="+".join(search_query_raw[-2:])
					self.Log(PLUGIN_LOG_TITLE + ' - SEARCH - Search Query: %s' % search_query)
					html=HTML.ElementFromURL(BASE_SEARCH_URL % search_query, sleep=REQUEST_DELAY)
					search_results=html.xpath('//*[@class="video-gallery"]/li')
					if search_results:
						for result in search_results:
							video_title=result.find('a').find("img").get("alt")
							self.Log(PLUGIN_LOG_TITLE + ' - SEARCH - video title: %s' % video_title)
							video_url=result.find('a').get('href')
							self.Log(PLUGIN_LOG_TITLE + ' - SEARCH - video url: %s' % video_url)
							video_title = re.sub("[\:\?\|\#]", '', video_title)
							if video_title.lower() == file_name.lower():
								self.Log(PLUGIN_LOG_TITLE + ' - SEARCH - Exact Match: \'' + file_name.lower() + '\' == \'%s\'' % video_title.lower())
								results.Append(MetadataSearchResult(id = video_url, name = video_title, score = 100, lang = lang))
								return
							else:
								score=score-1
								results.Append(MetadataSearchResult(id = video_url, name = video_title, score = score, lang = lang))
					else:
						search_query="+".join(search_query_raw[:2])
						self.Log(PLUGIN_LOG_TITLE + ' - SEARCH - Search Query: %s' % search_query)
						html=HTML.ElementFromURL(BASE_SEARCH_URL % search_query, sleep=REQUEST_DELAY)
						search_results=html.xpath('//*[@class="video-gallery"]/li')
						if search_results:
							for result in search_results:
								video_title=result.find('a').find("img").get("alt")
								self.Log(PLUGIN_LOG_TITLE + ' - SEARCH - video title: %s' % video_title)
								video_url=result.find('a').get('href')
								self.Log(PLUGIN_LOG_TITLE + ' - SEARCH - video url: %s' % video_url)
								video_title = re.sub("[\:\?\|\#]", '', video_title)
								if video_title.lower() == file_name.lower():
									self.Log(PLUGIN_LOG_TITLE + ' - SEARCH - Exact Match: \'' + file_name.lower() + '\' == \'%s\'' % video_title.lower())
									results.Append(MetadataSearchResult(id = video_url, name = video_title, score = 100, lang = lang))
									return
								else:
									score=1
									self.Log(PLUGIN_LOG_TITLE + ' - SEARCH - Title not found')
									results.Append(MetadataSearchResult(id = video_url, name = video_title, score = score, lang = lang))
						else:
							score=1
							self.Log(PLUGIN_LOG_TITLE + ' - SEARCH - Title not found')
							results.Append(MetadataSearchResult(id = video_url, name = video_title, score = score, lang = lang))

	def update(self, metadata, media, lang, force=False):
		self.Log(PLUGIN_LOG_TITLE + ' - UPDATE CALLED')

		if media.items[0].parts[0].file is not None:
			file_path = media.items[0].parts[0].file
			self.Log(PLUGIN_LOG_TITLE + ' - UPDATE - File Path: %s' % file_path)
			self.Log(PLUGIN_LOG_TITLE + ' - UPDATE - metadata.id: %s' % metadata.id)
			url = BASE_URL % metadata.id

			# Fetch HTML
			html = HTML.ElementFromURL(url, sleep=REQUEST_DELAY)	

			# Set tagline to URL
			metadata.tagline = url
			
			video_title = html.xpath('//div[@class="scene-title"]/span/text()')[0]
			self.Log(PLUGIN_LOG_TITLE + ' - UPDATE - video_title: "%s"' % video_title)
			#video_release_date = html.xpath('//*[@id="main"]/div[1]/div[1]/div[2]/table/tr[1]/td[1]/text()')[1]
			#self.Log(PLUGIN_LOG_TITLE + ' - UPDATE - video_release_date: "%s"' % video_release_date)
			#video_description = html.xpath('//*[@id="main"]/div[1]/div[1]/div[2]/table/tr/td/p/text()')
			#self.Log(PLUGIN_LOG_TITLE + ' - UPDATE - video_description: "%s"' % video_description)
			
			# External 	https://cdn.helixstudios.com/img/300h/media/stills/hx109_scene52_001.jpg
			# Member 	https://cdn.helixstudios.com/img/250w/media/stills/hx109_scene52_001.jpg
			valid_image_names = list()
			i = 0
			video_image_list = html.xpath('//*[@id="scene-just-gallery"]/a/img')
			# self.Log(PLUGIN_LOG_TITLE + ' - UPDATE - video_image_list: "%s"' % video_image_list)
			try:
				for image in video_image_list:
					thumb_url = image.get('src')
					# self.Log(PLUGIN_LOG_TITLE + ' - UPDATE - thumb_url: "%s"' % thumb_url)
					poster_url = thumb_url.replace('300h', '1920w')
					# self.Log(PLUGIN_LOG_TITLE + ' - UPDATE - poster_url: "%s"' % poster_url)
					valid_image_names.append(poster_url)
					if poster_url not in metadata.posters:
						try:
							i += 1
							metadata.posters[poster_url]=Proxy.Preview(HTTP.Request(thumb_url), sort_order = i)
						except: pass
			except: pass

			# Try to get description text
			try:
				raw_about_text=html.xpath('//*[@id="main"]/div[1]/div[1]/div[2]/table/tr/td/p')
				self.Log(PLUGIN_LOG_TITLE + ' - UPDATE - About Text - RAW %s', raw_about_text)
				about_text=' '.join(str(x.text_content().strip()) for x in raw_about_text)
				metadata.summary=about_text
			except: pass

			# Try to get release date
			try:
				release_date=html.xpath('//*[@id="main"]/div[1]/div[1]/div[2]/table/tr[1]/td[1]/text()')[1].strip()
				self.Log(PLUGIN_LOG_TITLE + ' - UPDATE - Release Date - New: %s' % release_date)
				metadata.originally_available_at = Datetime.ParseDate(release_date).date()
				metadata.year = metadata.originally_available_at.year
			except: pass

			# Try to get and process the video cast
			try:
				metadata.roles.clear()
				htmlcast = html.xpath('//*[@id="main"]/div[1]/div[1]/div[2]/table/tr[3]/td/a/text()')
				self.Log(PLUGIN_LOG_TITLE + ' - UPDATE - cast: "%s"' % htmlcast)
				for cast in htmlcast:
					cname = cast.strip()
					if (len(cname) > 0):
						role = metadata.roles.new()
						role.actor = cname
			except: pass
			
			# Try to get and process the video genres
			try:
				metadata.genres.clear()
				genres = html.xpath('//*[@id="main"]/div[1]/div[1]/div[2]/table/tr[4]/td/a/text()')
				self.Log(PLUGIN_LOG_TITLE + ' - UPDATE - video_genres: "%s"' % genres)
				for genre in genres:
					genre = genre.strip()
					if (len(genre) > 0):
						metadata.genres.add(genre)
			except: pass
			
			html.xpath('//*[@id="main"]/div[1]/div[1]/div[2]/table/tbody/tr/td/p/text()')

			metadata.posters.validate_keys(valid_image_names)
			metadata.title = video_title
			metadata.studio = "Helix Studios"