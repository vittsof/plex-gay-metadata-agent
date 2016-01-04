# Gay Scenes
# Description: Updated for the changes to the new site.
PLUGIN_LOG_TITLE='Cock Porn'	# Log Title

version = '2016.01.04.1'

def Start():
	pass

class CockPornAgent(Agent.Movies):
	name = 'Gay Adult'
	languages = [Locale.Language.NoLanguage, Locale.Language.English]
	primary_provider = True
	accepts_from=['com.plexapp.agents.localmedia', 'com.plexapp.agents.themoviedb']

	def Log(self, message, *args):
		if Prefs['debug']:
			Log(message, *args)

	def search(self, results, media, lang):
		self.Log('-----------------------------------------------------------------------')
		self.Log(PLUGIN_LOG_TITLE + ' - SEARCH CALLED v.%s', version)
		self.Log(PLUGIN_LOG_TITLE + ' - SEARCH - media.filename - %s', media.filename.split('%2F')[-1])
		filename=media.filename.split('%2F')[-1].replace('%20', ' ').replace('%2Emp4', '')
		self.Log(PLUGIN_LOG_TITLE + ' - SEARCH - results - %s', results)
		self.Log(PLUGIN_LOG_TITLE + ' - SEARCH - media.title - %s', media.title)
		results.Append(MetadataSearchResult(id=media.id, name=filename, score = 86, lang = lang))
		self.Log(PLUGIN_LOG_TITLE + ' - SEARCH - %s', results)
		

	def update(self, metadata, media, lang):
		self.Log(PLUGIN_LOG_TITLE + ' - UPDATE CALLED\033[0m')

		# Clear out the title to ensure stale data doesn't clobber other agents' contributions.
		# metadata.title = None
		# part = media.items[0].parts[0]
		# path = os.path.dirname(part.file)

		# # Look for local media.
		# try: localmedia.findAssets(metadata, media.title, [path], 'movie', media.items[0].parts)
		# except Exception, e: 
		# 	Log('Error finding media for movie %s: %s' % (media.title, str(e)))

		# # Look for subtitles
		# for item in media.items:
		# 	for part in item.parts:
		# 		localmedia.findSubtitles(part)

		# # If there is an appropriate VideoHelper, use it.
		# video_helper = videohelpers.VideoHelpers(part.file)
		# if video_helper:
		# 	video_helper.process_metadata(metadata)
