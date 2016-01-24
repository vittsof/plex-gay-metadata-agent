# Gay Scenes
# Description: Updated for the changes to the new site.
PLUGIN_LOG_TITLE='Cock Porn'	# Log Title

version = '2016.01.24.1'

def Start():
	pass

class CockPornAgent(Agent.Movies):
	name = 'Gay Adult'
	languages = [Locale.Language.NoLanguage, Locale.Language.English]
	primary_provider = True
	accepts_from=['com.plexapp.agents.localmedia', 'com.plexapp.agents.themoviedb']
