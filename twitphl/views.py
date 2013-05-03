from django.template import Context, loader, RequestContext
from django.http import HttpResponse
from twitphl.models import BeerLocs, Neighborhoods
from django.db.models import Count
import urllib
import simplejson
import json
import datetime
from django.contrib.gis.geos import GEOSGeometry


untapdFp = ''

def index(request):
	path = 'http://api.untappd.com/v4/thepub/local?client_id=AC2D813E208EF5CFD6290233622DA30260C9F66E&client_secret=D0A0C43B4CE252C0A21BECB2F3A6FB84A4366FA7&lng=-75.1642&lat=39.9522&radius=10&limit=50'
	search = urllib.urlopen(path)
	results = simplejson.loads(search.read())
	checkins = results['response']['checkins']['items']
	for i in range(len(checkins)):
		uid = results['response']['checkins']['items'][i]['checkin_id']
		created_at = results['response']['checkins']['items'][i]['created_at'].split()
		dt = ' '.join([created_at[3], created_at[2], created_at[1], created_at[4]])
		dt = datetime.datetime.strptime(dt, "%Y %b %d %H:%M:%S") - datetime.timedelta(hours=5)
		lng = results['response']['checkins']['items'][i]['venue']['location']['lng']
		lat = results['response']['checkins']['items'][i]['venue']['location']['lat']
		v = results['response']['checkins']['items'][i]['venue']['venue_name']
		loc =  GEOSGeometry('POINT(' + str(lng) + ' ' + str(lat) + ')')
		bp = BeerLocs(id=uid, lng=lng, lat=lat, bar=v, time=dt, locs=loc)
		bp.save()

	bars = BeerLocs.objects.values('bar').annotate(barcount=Count('bar')).order_by('-barcount')[:5]

	a = Neighborhoods.objects.raw('select n.id, name, count(*) from twitphl_neighborhoods n,  twitphl_beerlocs where ST_Contains(geom, locs) group by n.id')
	allnabes = Neighborhoods.objects.values('id')
	nabsum = {}
	tday = datetime.datetime.today() + datetime.timedelta(hours=1)
	for i in a:
		nabsum[int(i.id)] = int(i.count)
	for nabe in allnabes:
	    if nabsum.get(nabe['id']) == None:
             nabsum[int(nabe['id'])] = -1
	t = loader.get_template('twitphl/index.html')
	c = RequestContext(request, {'bars': bars, 'nabe_count_json' : nabsum, 'tday': tday})

	return HttpResponse(t.render(c))

