##provides a link to an image of a galaxy. 
##input: galaxy number as its order in Selected Spiral spreadsheet (for first galaxy, input 1, etc.)

from baseconv import BaseConverter
import urllib2
from bs4 import BeautifulSoup

def imageFinder(num):

	def giveID(galaxynumber):

		inFilePipe = open("SelectedSpirals.csv", "r")

		contents = inFilePipe.read()
		lines = contents.split("\r")
		
		inFilePipe.close()
		
		info = (lines[galaxynumber+1])
		objID = info[0:18] ##objID is a string
		return objID
	
	def search_url(objID):

		#objID fed as string
	
		IDnum = int(objID)
		base16 = BaseConverter('0123456789abcdef')
		base16id = base16.encode(IDnum)
		url = "http://skyserver.sdss.org/dr7/en/tools/explore/summary.asp?id=0x" + base16id + "&spec=0x01c2cac422c00000"

		return url
		
	def coordinates(url):

		html = urllib2.urlopen(url).read()

		soup = BeautifulSoup(html, "lxml")

		data = str(soup.find_all('h3'))

		a = data.split("=")

		ra = a[1].split(",")[0]
		dec = a[2].split(",")[0]

		return (ra, dec)
		
	def imageGrab(coordinates):

		ra = coordinates[0]
		dec = coordinates[1]
		
		
		##modify scale // allow to change scaling?
				
		link = "http://skyservice.pha.jhu.edu/DR7/ImgCutout/getjpeg.aspx?ra=" + ra + "&dec=" + dec + "&scale=0.1&width=1000&height=1000&opt=&query="
		
		return link
		
	return imageGrab(coordinates(search_url(giveID(num))))

print imageFinder(1149)
