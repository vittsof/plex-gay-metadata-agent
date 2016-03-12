<h1>plex-gay-metadata-agent</h1>
A Plex agent for fetching gay adult video metadata. https://forums.plex.tv/discussion/32922/adult-agents-for-gay-titles


<h1>INSTALLATION</h1>
1. Copy the Cockporn.bundle and any required site specific agents into the Plex Server plug-ins directory<br />
	<b>Mac:</b> ~/Library/Application Support/Plex Media Server/Plug-ins/<br />
	<b>QNAP:</b> /root/Library/Plex\ Media\ Server/Plug-ins/<br />
	<b>Windows:</b> %LOCALAPPDATA%\Plex Media Server\Plug-ins\ <br />
	<b>Raspberry Pi:</b> /var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Plug-ins<br />
2. Login to the web interface and open settings.
3. In Settings > Server > Agents select "Gay Adult" and check all required agents.
4. In Settings > Server > Agents move The Movie Database to second to last and Local Media Assets (Movies) to last.
5. In Settings > Server > Agents > The Movie Database > check "Include adult content"
6. Create a new library or change the agent of an existing library to the "Gay Adult" agent.

<h1>Wiki</h1>
More documentation can be found in the <a href="https://github.com/iklier/plex-gay-metadata-agent/wiki">wiki</a>.<br />
https://github.com/iklier/plex-gay-metadata-agent/wiki

NONE OF THE FILENAMES FOR THE ADGENTS BELOW ARE CASE SENSITIVE.

<h1>AEBN.bundle</h1>
	NAMING CONVENTION:
		Enclosing directory: Any
		Video Naming: Text of the title as displayed on AEBN website. You can even have scenes for movies.

		If multiple titles from different studios follow exact format below must have ().
			(Studio name) - title.extention
		Else you can just use.
			tite.extention

		If it is a scene include the word scene in the filename.
			title scene 1
	KNOWN ISSUES
	- Autoupdate may cause issues as it may cause a full metadata refresh when a new file is added.

<h1>HelixStudios.bundle</h1>
	NAMING CONVENTION:
		Enclosing directory: Any folder that starts with "Helix"
		Video Naming: Text title as displayed on Helix Studios website.

	KNOWN ISSUES
	- Limited ability to match titles with special characters in the name.
	- Unable to get metadata for bonus material from other sites.
	- Autoupdate may cause issues as it may cause a full metadata refresh when a new file is added.

<h1>Staxus.bundle</h1>
	NAMING CONVENTION:
		Enclosing directory: "Staxus"
		Video Naming: Partial title or text of the title as displayed on Staxus website.

	KNOWN ISSUES
	- Unable to get metadata for bonus material from other sites.
	- Autoupdate may cause issues as it may cause a full metadata refresh when a new file is added.

<h1>NOTES</h1>
All metadata is downloaded by the end users personal Plex Media Server instance and no metadata is embedded in the agent bundle itself.
