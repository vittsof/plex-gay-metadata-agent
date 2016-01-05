#Staxus
import re, os, urllib
PLUGIN_LOG_TITLE='Staxus'	# Log Title

VERSION_NO = '2016.01.04.1'

REQUEST_DELAY = 0					# Delay used when requesting HTML, may be good to have to prevent being banned from the site

# URLS
BASE_URL='http://staxus.com%s'

# Example Video Details URL
# http://staxus.com/trial/gallery.php?id=4044
BASE_VIDEO_DETAILS_URL='http://staxus.com/trial/%s'

# Example Search URL: 
# http://staxus.com/trial/search.php?query=Staxus+Classic%3A+BB+Skate+Rave+-+Scene+1+-+Remastered+in+HD
BASE_SEARCH_URL='http://staxus.com/trial/search.php?query=%s'

ENCLOSING_DIRECTORY_LIST=["Staxus"]

def Start():
	HTTP.CacheTime = CACHE_1WEEK
	HTTP.Headers['User-agent'] = 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.2; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0)'

class Staxus(Agent.Movies):
	name = 'Staxus'
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
			self.Log(PLUGIN_LOG_TITLE + ' - SEARCH - Enclosing Folder: %s' % enclosing_folder)
			# Check if enclosing directory matches an element in the directory list.
			if enclosing_folder in ENCLOSING_DIRECTORY_LIST:
				self.Log(PLUGIN_LOG_TITLE + ' - SEARCH - File Name: %s' % file_name)
				self.Log(PLUGIN_LOG_TITLE + ' - SEARCH - Split File Name: %s' % file_name.split(' '))

				remove_words = file_name.lower()
				remove_words = remove_words.replace('Staxus', '')
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
				search_results=html.xpath('//*[@class="reset collection-listing Marea"]/li/div/a')
				score=10
				# Enumerate the search results looking for an exact match. The hope is that by eliminating special character words from the title and searching the remainder that we will get the expected video in the results.
				for result in search_results:
					video_url=result.get('href')
					self.Log(PLUGIN_LOG_TITLE + ' - SEARCH - video url: %s' % video_url)
					image_url=result.findall("img")[0].get("src")
					self.Log(PLUGIN_LOG_TITLE + ' - SEARCH - image url: %s' % image_url)
					video_title=result.findall("img")[0].get("alt")
					self.Log(PLUGIN_LOG_TITLE + ' - SEARCH - video title: %s' % video_title)
					# Check the alt tag which includes the full title with special characters against the video title. If we match we nominate the result as the proper metadata. If we don't match we reply with a low score.
					if video_title is file_name:
						self.Log(PLUGIN_LOG_TITLE + ' - SEARCH - Exact Match' + file_name + '== %s' % video_title)
						results.Append(MetadataSearchResult(id = video_url, name = video_title, score = 100, lang = lang, sleep = REQUEST_DELAY))
					else:
						score=score-1
						results.Append(MetadataSearchResult(id = video_url, name = video_title, score = score, lang = lang))

	def update(self, metadata, media, lang, force=False):
		self.Log(PLUGIN_LOG_TITLE + ' - UPDATE CALLED')

		if media.items[0].parts[0].file is not None:
			file_path = media.items[0].parts[0].file
			self.Log(PLUGIN_LOG_TITLE + ' - UPDATE - File Path: %s' % file_path)
			self.Log(PLUGIN_LOG_TITLE + ' - UPDATE - metadata.id: %s' % metadata.id)
			url = BASE_VIDEO_DETAILS_URL % metadata.id

			# Fetch HTML
			html = HTML.ElementFromURL(url, sleep=REQUEST_DELAY)	

			# Set tagline to URL
			metadata.tagline = url
			
			video_title = html.xpath('//div[@class="sidebar right sidebar-models"]/h2/text()')[0]
			self.Log(PLUGIN_LOG_TITLE + ' - UPDATE - video_title: "%s"' % video_title)
			video_release_date = html.xpath('//div[@class="sidebar right sidebar-models"]/p[1]/span/text()')[0]
			self.Log(PLUGIN_LOG_TITLE + ' - UPDATE - video_release_date: "%s"' % video_release_date)
			video_description = html.xpath('//div[@class="col-main"]/p/text()')
			self.Log(PLUGIN_LOG_TITLE + ' - UPDATE - video_description: "%s"' % video_description)

			valid_image_names = list()
			i = 0
			video_image_list = html.xpath('//*[@class="reset collection-images"]/li/a/img')
			try:
				for image in video_image_list:
					thumb_url = image.get('src')
					self.Log(PLUGIN_LOG_TITLE + ' - UPDATE - thumb_url: "%s"' % thumb_url)
					poster_url = thumb_url.replace('300h', '1920w')
					self.Log(PLUGIN_LOG_TITLE + ' - UPDATE - poster_url: "%s"' % poster_url)
					valid_image_names.append(poster_url)
					if poster_url not in metadata.posters:
						try:
							i += 1
							metadata.posters[poster_url]=Proxy.Preview(HTTP.Request(thumb_url), sort_order = i)
						except: pass
			except: pass

			# Try to get description text
			try:
				raw_about_text=html.xpath('//div[@class="col-main"]/p')
				self.Log(PLUGIN_LOG_TITLE + ' - UPDATE - About Text - RAW %s', raw_about_text)
				about_text=' '.join(str(x.text_content().strip()) for x in raw_about_text)
				metadata.summary=about_text
			except: pass

			# Try to get release date
			try:
				release_date=html.xpath('//div[@class="sidebar right sidebar-models"]/p[1]/span/text()').strip()
				self.Log(PLUGIN_LOG_TITLE + ' - UPDATE - Release Date - New: %s' % release_date)
				metadata.originally_available_at = Datetime.ParseDate(release_date).date()
				metadata.year = metadata.originally_available_at.year
			except: pass

			# Try to get and process the video cast
			try:
				metadata.roles.clear()
				htmlcast = html.xpath('//div[@class="sidebar right sidebar-models"]/p[5]/text()')[0].split(', ')
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
				genres = html.xpath('//div[@class="sidebar right sidebar-models"]/p[3]/span/a/text()')
				self.Log(PLUGIN_LOG_TITLE + ' - UPDATE - video_genres: "%s"' % genres)
				for genre in genres:
					genre = genre.strip()
					if (len(genre) > 0):
						metadata.genres.add(genre)
			except: pass
			
			try:
				rating = html.xpath('//div[@class="col-md-4 col-xs-12 stats-single"]/b/text()')[0].strip()
				rating_count = html.xpath('//div[@class="col-md-4 col-xs-12 stats-single"]//strong/text()')[0]
				rating_count = rating_count.replace('(Total votes: ', '')
				rating_count = rating_count.replace(')', '')
				self.Log(PLUGIN_LOG_TITLE + ' - UPDATE - video_rating: "%s"', rating)
				self.Log(PLUGIN_LOG_TITLE + ' - UPDATE - video_rating_count: "%s"', rating_count)
				metadata.audience_rating = rating
				metadata.rating_count = rating_count
			except: pass

			metadata.posters.validate_keys(valid_image_names)
			metadata.title = video_title
			metadata.studio = "Staxus"