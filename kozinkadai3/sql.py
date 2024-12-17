import sqlite3

# SQLite DB初期化
def init_db():
    conn = sqlite3.connect("weather_forecast.db")
    cursor = conn.cursor()

    # エリア情報テーブル作成
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS area_info (
        area_code TEXT PRIMARY KEY,
        area_name TEXT NOT NULL,
        office_name TEXT,
        parent_region TEXT
    )
    ''')

    # 天気情報テーブル作成
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS weather_info (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        area_code TEXT,
        report_datetime TEXT,
        forecast_date TEXT,
        weather TEXT,
        wind TEXT,
        wave TEXT,
        temp TEXT,
        pop INTEGER,
        temp_max TEXT,
        temp_min TEXT,
        reliability TEXT,
        FOREIGN KEY (area_code) REFERENCES area_info(area_code)
    )
    ''')

    conn.commit()
    conn.close()




def save_weather_to_db(area_code, weather_data):
    conn = sqlite3.connect("weather_forecast.db")
    cursor = conn.cursor()

    # データを挿入する
    for weather_entry in weather_data:
        report_datetime = weather_entry["reportDatetime"]  # 発表日時
        time_series = weather_entry["timeSeries"]

        for ts in time_series:
            time_defines = ts["timeDefines"]
            areas = ts["areas"]

            for area in areas:
                for idx, time_define in enumerate(time_defines):
                    cursor.execute('''
                        INSERT INTO weather_info (
                            area_code, report_datetime, forecast_date, weather,
                            wind, wave, temp, pop, temp_max, temp_min, reliability
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        area_code,
                        report_datetime,
                        time_define,
                        area.get("weathers", ["情報なし"])[idx] if idx < len(area.get("weathers", [])) else None,
                        area.get("winds", ["情報なし"])[idx] if idx < len(area.get("winds", [])) else None,
                        area.get("waves", ["情報なし"])[idx] if idx < len(area.get("waves", [])) else None,
                        area.get("temps", ["情報なし"])[idx] if idx < len(area.get("temps", [])) else None,
                        area.get("pops", ["情報なし"])[idx] if idx < len(area.get("pops", [])) else None,
                        area.get("tempsMax", ["情報なし"])[idx] if idx < len(area.get("tempsMax", [])) else None,
                        area.get("tempsMin", ["情報なし"])[idx] if idx < len(area.get("tempsMin", [])) else None,
                        area.get("reliabilities", ["情報なし"])[idx] if idx < len(area.get("reliabilities", [])) else None,
                    ))

    conn.commit()
    conn.close()



def fetch_weather_from_db(area_code):
    conn = sqlite3.connect("weather_forecast.db")
    cursor = conn.cursor()

    cursor.execute('''
        SELECT report_datetime, forecast_date, weather, wind, wave, temp, pop
        FROM weather_info
        WHERE area_code = ?
        ORDER BY forecast_date
    ''', (area_code,))

    rows = cursor.fetchall()
    conn.close()

    # データを表示用に整形
    forecast_text = "天気予報:\n"
    for row in rows:
        report_datetime, forecast_date, weather, wind, wave, temp, pop = row
        forecast_text += f"\n発表日時: {report_datetime}\n"
        forecast_text += f"日時: {forecast_date}\n天気: {weather}\n風: {wind}\n波: {wave}\n気温: {temp}℃\n降水確率: {pop}%\n"

    return forecast_text
