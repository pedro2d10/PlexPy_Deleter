import json
import requests
import calendar
from datetime import datetime as DTime, date, time
import datetime
from terminaltables import AsciiTable
import humanfriendly

api_token = 'XXXXX'
api_url_base = 'http://localhost:8181/plexpy/api/v2/?apikey={0}&cmd='.format(api_token)

PLEXPY_APIKEY = 'XXXXX'  # Your PlexPy API key
PLEXPY_URL = 'http://localhost:8181/plexpy'  # Your PlexPy URL


headers = {'Content-Type': 'application/json'}


def get_server_identity():

	api_command = '{0}get_server_identity'.format(api_url_base)

	response = requests.get(api_command, headers=headers)

	if response.status_code == 200:
		return json.loads(response.content.decode('utf-8'))
	else:
		return None


def return_basic_command(command):
	api_command = '{0}{1}'.format(api_url_base,command)
	print(api_command)
	response = requests.get(api_command, headers=headers)

	if response.status_code == 200:
		return json.loads(response.content.decode('utf-8'))
	else:
		return None

def get_library_media_info(id_library):

	payload = {'apikey': PLEXPY_APIKEY,
				'section_id': '1',
				'cmd': 'get_library_media_info',
				'length': 10000}

	response = requests.get(PLEXPY_URL.rstrip('/') + '/api/v2', params=payload)

	if response.status_code == 200:
		return json.loads(response.content.decode('utf-8'))
	else:
		return None

def add_months(sourcedate,months):
	month = sourcedate.month - 1 + months
	year = sourcedate.year + month // 12
	month = month % 12 + 1
	day = min(sourcedate.day,calendar.monthrange(year,month)[1])
	return datetime.date(year,month,day)


#
# server_identity = get_server_identity()
# if server_identity is not None:
# 	print("Here's your server info: ")
# 	for k, v in server_identity['response']['data'].items():
# 		print('{0}:{1}'.format(k, v))
# else:
# 	print('[!] Request Failed')

server_library = return_basic_command('get_libraries')
for item in server_library['response']['data']:
		print ('{0} , {1} , {2}'.format(item.get('section_name'),item.get('section_id'),item.get('rating_key')))


server_library = return_basic_command('get_libraries_table')
# print (server_library['response'].get('data'))
for item in server_library['response']['data']['data']:

	print ('{0} , {1}'.format(item.get('rating_key'), item.get('section_id')))

# for item in server_library['response']['data']:
# 		print ('{0} , {1} , {2}'.format(item.get('section_name'),item.get('section_id'),item.get('rating_key')))


today = datetime.date.today()
print (today)
DateToDelete  = add_months(today,-9)

server_library = get_library_media_info('1')
row_format ="{:>15}" * (len(server_library['response']['data']['data']) + 1)
data = []
data.append (['Titre', 'Last Played', 'Date Added', 'Year', 'Size'])
nb_data = 0
total_size = 0
# print (server_library)
if server_library is not None:
	for item in server_library['response']['data']['data']:
		if item.get('last_played') == None:
			dateAded = DTime.fromtimestamp(float(item.get('added_at')))
			DateToDelete = DTime.combine(DateToDelete, time())
			if dateAded < DateToDelete and int(item.get('year')) < 2017 :
				#print (row_format.format(server_library['response']['data']['data']))
				total_size += int(item.get('file_size'))
				file_size = humanfriendly.parse_size(item.get('file_size'))
				data.append([item.get('title'), item.get('last_played'), DTime.fromtimestamp(float(item.get('added_at'))), item.get('year'), humanfriendly.format_size(file_size)])
				nb_data += 1
				#print ('{0}\t{1}\t{2}'.format( item.get('title'), item.get('last_played'),  DTime.fromtimestamp(float(item.get('added_at')))))
	#table = AsciiTable(server_library['response']['data']['data'])

	data.append(['Total to delete : ' + str(nb_data) , '','', '', humanfriendly.format_size(total_size)])
	table = AsciiTable(data)
	table.inner_footing_row_border = True
	print (table.table)
else:
	print('[!] Request Failed')
