# Gay Scenes
import os, platform

# Description: Updated for the changes to the new site.
PLUGIN_LOG_TITLE='Cock Porn'	# Log Title

version = '2017.07.26.1'

def Start():
	pass

class CockPornAgent(Agent.Movies):
	name = 'Gay Adult'
	languages = [Locale.Language.NoLanguage, Locale.Language.English]
	primary_provider = True
	accepts_from=['com.plexapp.agents.localmedia']

	def Log(self, message, *args):
		if Prefs['debug']:
			Log(PLUGIN_LOG_TITLE + ' - ' + message, *args)

	def search(self, results, media, lang):
		self.Log('-----------------------------------------------------------------------')
		self.Log('SEARCH CALLED v.%s', version)
		self.Log('SEARCH - media.filename - %s', media.filename.split('%2F')[-1])
		self.Log('SEARCH - Platform: %s %s', platform.system(), platform.release())

		path_and_file = media.items[0].parts[0].file.lower()
		self.Log('SEARCH - File Path: %s', path_and_file)

		(file_dir, basename) = os.path.split(os.path.splitext(path_and_file)[0])
		self.Log('SEARCH - File Name: %s' % basename)

		self.Log('SEARCH - results - %s', results)
		self.Log('SEARCH - media.title - %s', media.title)
		results.Append(MetadataSearchResult(id=media.id, name=basename, score = 86, lang = lang))
		self.Log('SEARCH - %s', results)


	def update(self, metadata, media, lang):
		self.Log('UPDATE CALLED')

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
