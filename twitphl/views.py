from django.template import Context, loader, RequestContext
from django.http import HttpResponse
from twitphl.models import BeerLocs
import urllib
import simplejson
from django.contrib.gis.geos import GEOSGeometry


untapdFp = ''

def index(request):
	path = 'http://api.untappd.com/v4/thepub/local?client_id=AC2D813E208EF5CFD6290233622DA30260C9F66E&client_secret=D0A0C43B4CE252C0A21BECB2F3A6FB84A4366FA7&lng=-75.1642&lat=39.9522&radius=10&limit=50'
	search = urllib.urlopen(path)
	results = simplejson.loads(search.read())
	checkins = results['response']['checkins']['items']
	for i in range(len(checkins)):
		uid = results['response']['checkins']['items'][i]['user']['uid']
		lng = results['response']['checkins']['items'][i]['venue']['location']['lng']
		lat = results['response']['checkins']['items'][i]['venue']['location']['lat']
		v = results['response']['checkins']['items'][i]['venue']['venue_name']
		loc =  GEOSGeometry('POINT(' + str(lng) + ' ' + str(lat) + ')')
		bp = BeerLocs(id=uid, lng=lng, lat=lat, bar=v, locs=loc)
		bp.save()
	t = loader.get_template('twitphl/index.html')
	c = RequestContext(request)

	#select name, count(*) from nabes ,  twitphl_beerlocs where  ST_Contains(geom, locs) group by name ;

	return HttpResponse(t.render(c))

