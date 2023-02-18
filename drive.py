
from Google import Create_Service


def get_values_from_files(files):
	indexs 				= ('#',)
	video_names  		= ('Title',)
	video_links 		= ('Google Drive Link',)
	video_embed_codes 	= ('Embed Code',) 
	for index, file in enumerate(files):
		video_id 	= file.get('id')
		name 		= file.get('name')
		link 		= f"https://drive.google.com/file/d/{video_id}/view"
		embed_code 	= f"<iframe src='https://drive.google.com/file/d/{video_id}/preview' width='640' height='480' allow='autoplay'></iframe>"

		indexs    		= indexs + (index, )
		video_names		= video_names + (name,) 
		video_links 	= video_links + (link,)
		video_embed_codes= video_embed_codes + (embed_code,)

	print(video_names)
	print(video_links)
	print(video_embed_codes)
	return indexs, video_names, video_links, video_embed_codes


def google_drive():
	CLIENT_SECRET_FILE 	= 'credentials.json'
	API_NAME 			= 'drive'
	API_VERSION 		= 'v3'
	SCOPES 				= ['https://www.googleapis.com/auth/drive']
	drive_service 		= Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
	
	folder_id 	= '1fGZpA7FzlQj6yy5LlJlw2PMpTuFCq2KV'
	query 		= f"parents = '{folder_id}'"
	response 	= drive_service.files().list(q = query).execute()
	
	files 			= response.get('files')
	next_page_token = response.get('nextPageToken')

	while next_page_token:
	 	response = drive_service.files().list(q = query).execute()
	 	files.extend(response.get('files'))
	 	next_page_token = response.get('nextPageToken')

	return files


def google_sheet(files):
	indexs, video_names, video_links, video_embed_codes = get_values_from_files(files)


	CLIENT_SECRET_FILE 	= 'credentials.json'
	API_NAME 			= 'sheets'
	API_VERSION 		= 'v4'
	SCOPES 				= ['https://www.googleapis.com/auth/spreadsheets']
	
	sheet_service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

	sheet_body = {
		'properties': {
  			"title": "Sample Sheet for Video and Embed Code",
  			"locale": 'en_US',
  			"autoRecalc": 'HOUR',
  			"timeZone": 'America/Los_Angeles'
			}
	}
	sheet = sheet_service.spreadsheets().create(body=sheet_body).execute()
	spreadsheet_id = sheet.get('spreadsheetId')

	worksheet_name = 'sheet1'

	values = (
		indexs,
		video_names,
		video_links,
		video_embed_codes
		)
	value_range_body  = {
		'majorDimension': 'COLUMNS',
		'values' 		: values
	}


	final_result = sheet_service.spreadsheets().values().update(
			spreadsheetId=spreadsheet_id,
			valueInputOption='USER_ENTERED',
			range= worksheet_name,
			body= value_range_body
		).execute()


	print('DONE... All data saved in spreadsheet. URL: {}'.format(sheet.get('spreadsheetUrl')))

files = google_drive()
google_sheet(files)


