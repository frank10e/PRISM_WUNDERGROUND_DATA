import datetime
import pandas as pd

from wunderground_pws import WUndergroundAPI, units

wu = WUndergroundAPI(
    api_key='e1f10a1e78da46f5b10a1e78da96f525',
    default_station_id='KAZVAIL289',
    units=units.ENGLISH_UNITS,
)

station_ids=['KAZVAIL289','KAZGREEN15','KAZSAHUA108','KAZGREEN269','KAZSAHUA55']
station_names=['Vail','Florida Station','Rancho Sahuarita','Green Valley','Sahuarita']


start_date = datetime.date(2024, 1, 1)
end_date = datetime.date(2024, 9, 1)

for i in range(len(station_ids)):
    station_id=station_ids[i]
    station_name=station_names[i]
    print()
    print(station_name)
    print()

    all_imperial_data=[]
    current_date = start_date
    while current_date <= end_date:
        try:
            imperial_data = wu.history(date=current_date, granularity='daily')['observations'][0]['imperial']
            imperial_data['date']=current_date
            all_imperial_data.append(imperial_data)
        except Exception as e:
            print(f"Error fetching data for {current_date}: {e}")
        current_date += datetime.timedelta(days=1)

    df=pd.DataFrame(all_imperial_data)
    df.to_csv(f'{station_name}.csv',index=False)