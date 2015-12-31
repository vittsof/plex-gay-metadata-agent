import re
import urllib
# Log Title
PLUGIN_LOG_TITLE='Helix Studios'

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

ENCLOSING_DIRECTORY_LIST=["HelixStudios", "Helix Studios"]

def Start():
	HTTP.CacheTime = CACHE_1DAY
	# HTTP.SetHeader('User-agent', 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.2; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0)')

class AgentTemplateAgent(Agent.Movies):
	name = 'Helix Studios'
	languages = [Locale.Language.NoLanguage, Locale.Language.English]
	primary_provider = False
	contributes_to = ['com.plexapp.agents.cockporn']

	def search(self, results, media, lang, manual):
		Log('\033[33m' + PLUGIN_LOG_TITLE + ' - SEARCH CALLED\033[0m')
		Log('\033[33m' + PLUGIN_LOG_TITLE + ' - SEARCH - media.title - \033[0m %s', media.title)
		Log('\033[33m' + PLUGIN_LOG_TITLE + ' - SEARCH - media.items[0].parts[0].file - \033[0m %s', media.items[0].parts[0].file)
		Log('\033[33m' + PLUGIN_LOG_TITLE + ' - SEARCH - media.primary_metadata.title - \033[0m %s', media.primary_metadata.title)
		Log('\033[33m' + PLUGIN_LOG_TITLE + ' - SEARCH - media.items - \033[0m %s', media.items)
		Log('\033[33m' + PLUGIN_LOG_TITLE + ' - SEARCH - media.filename - \033[0m %s', media.filename)
		Log('\033[33m' + PLUGIN_LOG_TITLE + ' - SEARCH - lang - \033[0m %s', lang)
		Log('\033[33m' + PLUGIN_LOG_TITLE + ' - SEARCH - manual - \033[0m %s', manual)

		if media.items[0].parts[0].file is not None:
			file_path = media.items[0].parts[0].file
			Log('\033[33m' + PLUGIN_LOG_TITLE + '- SEARCH - File Path\033[0m: %s' % file_path)
			enclosing_directory = file_path.split('/')[-2]
			Log('\033[33m' + PLUGIN_LOG_TITLE + '- SEARCH - Enclosing Directory\033[0m: %s' % enclosing_directory)
			# Check if enclosing directory matches an element in the directory list.
			if enclosing_directory in ENCLOSING_DIRECTORY_LIST:
				file_name=file_path.split('/')[-1].split('.')[0]
				Log('\033[33m' + PLUGIN_LOG_TITLE + '- SEARCH - File Name\033[0m: %s' % file_name)
				Log('\033[33m' + PLUGIN_LOG_TITLE + '- SEARCH - Split File Name\033[0m: %s' % file_name.split(' '))
				search_query_raw = list()
				# Process the split filename to remove words with special characters. This is to attempt to find a match with the limited search function(doesn't process any non-alphanumeric characters correctly)
				for piece in file_name.split(' '):
					if re.search('^[0-9A-Za-z]*$', piece.replace('!', '')) is not None:
						search_query_raw.append(piece)
				search_query="+".join(search_query_raw)
				Log('\033[33m' + PLUGIN_LOG_TITLE + '- SEARCH - Search Query\033[0m: %s' % search_query)
				html=HTML.ElementFromURL(BASE_SEARCH_URL % search_query)
				search_results=html.xpath('//*[@class="video-gallery"]/li/a')
				score=10
				# Enumerate the search results looking for an exact match. The hope is that by eliminating special character words from the title and searching the remainder that we will get the expected video in the results.
				for result in search_results:
					video_url=result.get('href')
					Log('\033[33m' + PLUGIN_LOG_TITLE + '- SEARCH - video url\033[0m: %s' % video_url)
					image_url=result.findall("img")[0].get("src")
					Log('\033[33m' + PLUGIN_LOG_TITLE + '- SEARCH - image url\033[0m: %s' % image_url)
					video_title=result.findall("img")[0].get("alt")
					Log('\033[33m' + PLUGIN_LOG_TITLE + '- SEARCH - video title\033[0m: %s' % video_title)
					# Check the alt tag which includes the full title with special characters against the video title. If we match we nominate the result as the proper metadata. If we don't match we reply with a low score.
					if video_title is file_name:
						Log('\033[33m' + PLUGIN_LOG_TITLE + '- SEARCH - Exact Match\033[0m' + file_name + '== %s' % video_title)
						results.Append(MetadataSearchResult(id = video_url, name = video_title, score = 100, lang = lang))
					else:
						score=score-1
						results.Append(MetadataSearchResult(id = video_url, name = video_title, score = score, lang = lang))

	def update(self, metadata, media, lang):
		Log('\033[33m' + PLUGIN_LOG_TITLE + ' - UPDATE CALLED\033[0m')

		if media.items[0].parts[0].file is not None:
			file_path = media.items[0].parts[0].file
			Log('\033[33m' + PLUGIN_LOG_TITLE + ' - UPDATE - File Path\033[0m: %s' % file_path)
			Log('\033[33m' + PLUGIN_LOG_TITLE + ' - UPDATE - metadata.id\033[0m: %s' % metadata.id)
			video_url = BASE_URL % metadata.id

			html = HTML.ElementFromURL(video_url)

			video_title = html.xpath('//div[@class="scene-title"]/text()')[0]
			Log('\033[33m' + PLUGIN_LOG_TITLE + ' - UPDATE - video_title\033[0m: "%s"' % video_title)
			video_release_date = html.xpath('//*[@id="main"]/div[1]/div[1]/div[2]/table/tr[1]/td[1]/text()')[1]
			Log('\033[33m' + PLUGIN_LOG_TITLE + ' - UPDATE - video_release_date\033[0m: "%s"' % video_release_date)
			video_description = html.xpath('//*[@id="main"]/div[1]/div[1]/div[2]/table/tr/td/p/text()')
			Log('\033[33m' + PLUGIN_LOG_TITLE + ' - UPDATE - video_description\033[0m: "%s"' % video_description)
			video_cast = html.xpath('//*[@id="main"]/div[1]/div[1]/div[2]/table/tr[3]/td/a/text()')
			Log('\033[33m' + PLUGIN_LOG_TITLE + ' - UPDATE - video_cast\033[0m: "%s"' % video_cast)
			# External 	https://cdn.helixstudios.com/img/300h/media/stills/hx109_scene52_001.jpg
			# Member 	https://cdn.helixstudios.com/img/250w/media/stills/hx109_scene52_001.jpg
			valid_image_names = list()
			i = 0
			video_image_list = html.xpath('//*[@id="scene-just-gallery"]/a/img')
			# Log('\033[33m' + PLUGIN_LOG_TITLE + ' - UPDATE - video_image_list\033[0m: "%s"' % video_image_list)
			try:
				for image in video_image_list:
					thumb_url = image.get('src')
					Log('\033[33m' + PLUGIN_LOG_TITLE + ' - UPDATE - thumb_url\033[0m: "%s"' % thumb_url)
					poster_url = thumb_url.replace('300h', '1920w')
					Log('\033[33m' + PLUGIN_LOG_TITLE + ' - UPDATE - poster_url\033[0m: "%s"' % poster_url)
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
				Log('\033[33m' + PLUGIN_LOG_TITLE + ' - UPDATE - About Text - RAW\033[0m %s', raw_about_text)
				about_text=' '.join(str(x.text_content().strip()) for x in raw_about_text)
				metadata.summary=about_text
			except: pass

			# Try to get release date
			try:
				release_date=html.xpath('//*[@id="main"]/div[1]/div[1]/div[2]/table/tr[1]/td[1]/text()')[1].strip()
				Log('\033[33m' + PLUGIN_LOG_TITLE + ' - UPDATE - Release Date - New:\033[0m %s' % release_date)
				metadata.originally_available_at = Datetime.ParseDate(release_date).date()
				metadata.year = metadata.originally_available_at.year
			except: pass

			# Try to get and process the video cast
			try:
				metadata.roles.clear()
				htmlcast = html.xpath('//*[@id="main"]/div[1]/div[1]/div[2]/table/tr[3]/td/a')
				for cast in htmlcast:
					cname = cast.text_content().strip()
					Log('\033[33m' + PLUGIN_LOG_TITLE + ' - UPDATE - Cast:\033[0m %s' % cname)
					if (len(cname) > 0):
						role = metadata.roles.new()
						role.actor = cname
			except: pass
			
			html.xpath('//*[@id="main"]/div[1]/div[1]/div[2]/table/tbody/tr/td/p/text()')

			metadata.posters.validate_keys(valid_image_names)
			metadata.title = video_title
			metadata.studio = "Helix Studios"


