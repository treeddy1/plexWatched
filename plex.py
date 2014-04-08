import urllib
import urllib2
import base64
from xml.dom import minidom



class Plex(object):
	def __init__(self, host, username="", password=""):
		self.host = host
		self.showKey = 0
		self.movieKey = 0
		self.token = ""
		self.username = username
		self.password = password
		if username:
			self.authRequired = True
		else:
			self.authRequired = False

	def _get_plex_token(self):
		url = "https://my.plexapp.com/users/sign_in.xml"
		try:
			req = urllib2.Request(url, data="")
			base64string = base64.encodestring('%s:%s' % (self.username, self.password))[:-1]
			authheader = "Basic %s" % base64string
			req.add_header("Authorization", authheader)
			req.add_header("X-Plex-Client-Identifier","myapp")    

			response = urllib2.urlopen(req)
			result = minidom.parse(response)
			response.close()
			self.token =  result.getElementsByTagName('authentication-token')[0].childNodes[0].data
			return True


		except (urllib2.URLError, IOError), e:
			print "Warning: Couldn't contact Plex at: " + url 
			print e

	def _send_to_plex(self, command):
		url = "http://%s%s" % (self.host, command)
		try:
			req = urllib2.Request(url)
			if self.authRequired:
				if self.token == "":
					self._get_plex_token()
					
				#logger.log(u"Contacting Plex (with auth header) via url: " + url)     
				req.add_header("X-Plex-Token", self.token)
			response = urllib2.urlopen(req)
			if response.headers['content-length'] != "0":
				#print response.headers['content-length']
				result = minidom.parse(response)
			else:
				result = ""
			response.close()
			return result

		except (urllib2.URLError, IOError), e:
			print "Warning: Couldn't contact Plex at: " + url 


	def get_sections(self):
		sections = self._send_to_plex('/library/sections/').getElementsByTagName('Directory')
		for section in sections:
			if section.getAttribute('type') == "show":
				self.showKey = section.getAttribute('key')
			elif section.getAttribute('type') == "movie":
				self.movieKey = section.getAttribute('key')



	def get_shows(self):
		showList = []
		mycommand = "/library/sections/%s/all" % (self.showKey)
		shows = self._send_to_plex(mycommand).getElementsByTagName('Directory')
		for show in shows:
			showName = show.getAttribute('title')
			showKey = show.getAttribute('key')
			newShow = Show(showName, showKey)
			newShow.seasons = self.get_show_seasons(show.getAttribute('key'))

			for season in newShow.seasons:
				#print season.getAttribute('title')
				newShow.episodes = self.get_episode_list(season)

			showList.append(newShow)

		return showList

	def get_show_seasons(self, showKey):
		#mycommand = show.getAttribute('key')
		seasons = self._send_to_plex(showKey).getElementsByTagName('Directory')
		return seasons
		

	def get_episode_list(self, season):
		seasonPath = season.getAttribute('key')
		episodeList = []
		episodes = self._send_to_plex(seasonPath).getElementsByTagName('Video')

		for episode in episodes:
			#create new Episode Instance
			episodeNew = Episode()

			#set the new Episode Attributes
			episodeNew.name = episode.getAttribute('title')
			episodeNew.description = episode.getAttribute('summary')
			episodeNew.key = episode.getAttribute('key')
			episodeNew.season = season.getAttribute('index')
			episodeNew.episodeNumber = episode.getAttribute('index')
			episodeNew.filePath = episode.childNodes[1].childNodes[1].getAttribute('file')

			if episode.getAttribute('viewCount'):
				episodeNew.watched = True

			episodeList.append(episodeNew)
		return episodeList


	def get_movies(self):
		movieList = []
		mycommand = "/library/sections/%s/all" % (self.movieKey)
		movies = self._send_to_plex(mycommand).getElementsByTagName('Video')
		for movie in movies:
			newMovie = Movie()
			newMovie.name = movie.getAttribute('title')
			newMovie.description = movie.getAttribute('summary')
			newMovie.key = movie.getAttribute('key')
			newMovie.filePath = movie.childNodes[1].childNodes[1].getAttribute('file')
			if movie.getAttribute('viewCount'):
				newMovie.watched = True


			movieList.append(newMovie)

		return movieList

	def refesh_library(self):
		mycommand = "/library/sections/%s/refresh" % (self.showKey)
		self._send_to_plex(mycommand)




class Show(object):
	def __init__(self, name, showKey):
		self.name = name
		self.showKey = showKey
		self.seasons = []
		self.episodes = []

class Episode(object):
	def __init__(self):
		self.name = ""
		self.description = ""
		self.key = ""
		self.season = 0
		self.episodeNumber = 0
		self.filePath = ""
		self.watched = False

class Movie(object):
	def __init__(self):
		self.name = ""
		self.description = ""
		self.key = ""
		self.filePath = ""
		self.watched = False

host = "192.168.1.173:32400"
username = "treeddy1"
password = "iluvibm7"
myplex = Plex(host, username, password)
myplex.get_sections()
myplex.refesh_library()
shows = myplex.get_shows()

for show in shows:
	for episode in show.episodes:
		if episode.watched:
			print "rm " + "\"" + episode.filePath + "\""


movies = myplex.get_movies()

for movie in movies:
	if movie.watched:
		print "rm " +"\"" + movie.filePath + "\""






