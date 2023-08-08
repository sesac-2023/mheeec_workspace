import pandas as pd
import requests
import json
import requests
import pandas as pd
import pandas as pd
from bs4 import BeautifulSoup

###데이터 수집하기

#1. driver's information/ lap_result

cars_info = []
lap_result = []

for page_num in range(2):
    url = f'https://motorsportstats.com/api/result-statistics?sessionSlug=formula-one_2023_belgian-grand-prix_race&sessionFact=LapChart&page={page_num}&size=25'


    # URL에서 데이터 가져오기
    response = requests.get(url, format(2))
    data = json.loads(response.text)
    


    for car in data['cars']:
        
        for driver in car['drivers']:
            driver['name']
            driver['code']

        cars_info.append({
            '차번호':  car['carNumber'],
            '드라이버':  driver['name'],
            '대문자이름' : driver['code'],
    })

    for l in data['content']:
        lap_result.append({
            'lap' : l['lap'],
            'cars' : l['cars']
        })

car_info_df = pd.DataFrame(cars_info)[:20]
lap_result_df = pd.DataFrame(lap_result)

#2. race_result - pit stop
url = "https://www.formula1.com/en/results.html/2023/races/1216/belgium/pit-stop-summary.html"

response = requests.get(url)

stops_data = pd.read_html(response.text)[0][['Stops','No','Driver']]

#3. race_result - time
url = "https://www.formula1.com/en/results.html/2023/races/1216/belgium/race-result.html"

response = requests.get(url)

time_result = pd.read_html(response.text)[0][["Pos", "No", "Driver", 'Car','Laps','Time/Retired', "PTS"]]

###그래프에 넣을 수 있게 데이터 전처리
result = []

for i  in lap_result_df['cars']:
    result.append(i)

race_result = []

for lap in result:
    result_dict = {string : i+1 for i,string in enumerate(lap)}
    race_result.append(result_dict)

race_lap_result = pd.DataFrame(race_result)

race_lap_result = race_lap_result.fillna(0)

race_lap_result=race_lap_result.astype('int64')

car_dict = car_info_df.set_index('차번호')['대문자이름'].to_dict()

race_lap_result.rename(columns = car_dict, inplace=True)

###html 불러오기
with open('./test2.html', encoding='utf-8') as f:
    html = f.read()

###html left 데이터 추가하기
html_template = """
              <tr>
                <td>{}</td>
                <td>{}</td>
                <td>{}</td>
              </tr>
"""

content = ""

html_file_path = './test2.html'


for n, driver in zip(range(0,21), race_lap_result[0:0]):
    row_html = html_template.format(n+1, driver, '이미지')  # 이미지 문자열 변경
    content += row_html


final_html = html.replace('</tbody>', content + '</tbody>')

with open(html_file_path, 'w') as f:
    f.write(final_html)



html_f = """
              <tr>
                <td>{}</td>
                <td>{}</td>
                <td>{}</td>
                <td>{}</td>
              </tr>
"""

html_content = ""


for n,(r,time,stop) in enumerate(zip(time_result['Driver'],time_result['Time/Retired'],stops_data['Stops'])):
    row_html = html_f.format(n+1, r, time, stop)
    html_content += row_html
    

soup = BeautifulSoup(html, 'html.parser')
tbody2 = soup.select('tbody')[1]
tbody2.append(BeautifulSoup(html_content, 'html.parser'))

with open(html_file_path, 'w') as f:
    f.write(str(soup))