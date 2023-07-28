import gspread, requests
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)

client = gspread.authorize(creds)

sheet = client.open("Тест").sheet1

data = sheet.col_values(1)[1:]

def get_data(value, row):
    cells_data = []
    cells_data.append(f'https://www.wildberries.ru/catalog/{value}/detail.aspx')
    cells_data.append(requests.get(url=f'https://product-order-qnt.wildberries.ru/by-nm/?nm={value}').json()[0]['qnt'])

    url = f'https://card.wb.ru/cards/detail?appType=1&curr=rub&dest=-1205337&regions=80,38,83,4,64,33,68,70,30,40,86,69,22,1,31,66,48,114&spp=30&nm={value}'
    response = requests.get(url=url).json()['data']['products'][0]
    pages = int(response['pics'])
    photo_links = ''
    
    for i in range(100):
        if i < 10:
            i = '0' + str(i)
        try:
            if requests.get(f'https://basket-{i}.wb.ru/vol{value[:-5]}/part{value[:-3]}/{value}/info/price-history.json').status_code == 200:
                for page in range(pages):
                    text = f'https://basket-{i}.wb.ru/vol{value[:-5]}/part{value[:-3]}/{value}/images/big/{page}.jpg'
                    photo_links += f'{text}\n'
                break
        except:
            pass

    cells_data.append(str(photo_links))
    cells_data.append(str(response['sale']))
    cells_data.append(str(response['reviewRating']))
    cells_data.append(str(response['feedbacks']))

    for i, cell_data in enumerate(cells_data):
        sheet.update_cell(row, i + 2, cell_data)


for row, value in enumerate(data, start=2):
    get_data(value, row)
