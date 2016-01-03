# Gay Scenes
# Update: 12 July 2015
# Description: Updated for the changes to the new site.

def Start():
	pass

class CockPornAgent(Agent.Movies):
	name = 'Gay Adult'
	languages = [Locale.Language.NoLanguage, Locale.Language.English]
	primary_provider = True
	accepts_from=['com.plexapp.agents.localmedia']

	def search(self, results, media, lang):
		Log('\033[1mCock Porn - SEARCH CALLED - %s\033[0m', media.filename.split('%2F')[-1])
		filename=media.filename.split('%2F')[-1].replace('%20', ' ').replace('%2Emp4', '')
		Log('\033[1mCock Porn - SEARCH - results - \033[0m %s', results)
		Log('\033[1mCock Porn - SEARCH - media.title - \033[0m %s', media.title)
		results.Append(MetadataSearchResult(id=media.id, name=filename, score = 86, lang = lang))
		Log('\033[1mCock Porn - SEARCH - \033[0m %s', results)
		

	def update(self, metadata, media, lang):
		Log('\033[1mCock Porn - UPDATE CALLED\033[0m')

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
