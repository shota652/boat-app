import requests
from bs4 import BeautifulSoup
import streamlit as st

st.title("ボートレース出走表スクレイピング")

date = st.text_input("日付 (例: 20250508)", value="20250508")
jcd = "07"  # 蒲郡

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
}

def get_race_data(date, jcd):
    race_data = []
    for rno in range(1, 13):
        url = f"https://www.boatrace.jp/owpc/pc/race/raceindex?jcd={jcd}&hd={date}&rno={rno}"
        res = requests.get(url, headers=headers)
        if res.status_code != 200:
            continue
        soup = BeautifulSoup(res.content, "html.parser")

        # 選手名リンクの抽出
        name_links = soup.select("a[href*='/owpc/pc/data/racersearch/profile']")
        names = [link.get_text(strip=True) for link in name_links]

        if len(names) == 6:
            race_data.append((rno, names))
    return race_data

if st.button("出走表を取得"):
    results = get_race_data(date, jcd)
    if not results:
        st.warning("出走表が取得できませんでした。日付かレース場を確認してください。")
    else:
        for rno, racers in results:
            st.subheader(f"{rno}R")
            for i, name in enumerate(racers, start=1):
                st.text_input(f"{rno}R {i}号艇", value=name, key=f"{rno}_{i}_{name}")


