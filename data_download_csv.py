import datetime
import pandas as pd
from wunderground_pws import WUndergroundAPI, units


wu = WUndergroundAPI(
    api_key='e1f10a1e78da46f5b10a1e78da96f525',  
    units=units.ENGLISH_UNITS,
)


station_ids = ['KAZSAHUA117']

station_names = [ 'KAZSAHUA117']


start_date = datetime.date(2024, 1, 1)
end_date = datetime.date(2024, 9, 1)

for i in range(len(station_ids)):
    station_id = station_ids[i]
    station_name = station_names[i]
    
    print(f"\nFetching data for {station_name} ({station_id})\n")
    
    all_imperial_data = []
    current_date = start_date
    

    while current_date <= end_date:
        try:
            response = wu.history(date=current_date, station_id=station_id, granularity='daily')
            
            
            if 'observations' in response and len(response['observations']) > 0:
                imperial_data = response['observations'][0]['imperial']
                imperial_data['date'] = current_date
                all_imperial_data.append(imperial_data)
            else:
                print(f"No data for {current_date}")
        
        except Exception as e:
            print(f"Error fetching data for {current_date} at {station_name}: {e}")
        
        
        current_date += datetime.timedelta(days=1)
    
    if all_imperial_data:
        df = pd.DataFrame(all_imperial_data)
        csv_filename = f"{station_name}.csv"
        df.to_csv(csv_filename, index=False)
        print(f"Data saved to {csv_filename}")
    else:
        print(f"No data available for {station_name}")
