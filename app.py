# 스트림릿
from dataclasses import asdict
import streamlit as st
import layout

# 지도, 그래프
import pandas as pd
from streamlit_folium import st_folium
import folium
import json

# 현위치
from streamlit_js_eval import get_geolocation

# 스케줄러
import threading
import time
import schedule
from services.charger_detail import select_charger_detail
from services.charger_station.select_charger_station import (
    select_charger_station,
    select_charger_station_location,
)
from services.scheduler import job

layout.base_layout()

# 현 위치 가져오기
loc = get_geolocation()

MY_LAT = 0
MY_LNG = 0

if loc:
    # 지도 변수/상수
    MY_LAT = float(loc["coords"]["latitude"])
    MY_LNG = float(loc["coords"]["longitude"])

if loc:

    # Folium 지도 객체 생성
    m = folium.Map(location=[MY_LAT, MY_LNG], zoom_start=13)

    # 내 위치 마커
    folium.Marker(
        [MY_LAT, MY_LNG],
        # popup="📍 내 위치",
        # tooltip="현재 위치",
        icon=folium.Icon(color="red", icon="user"),
    ).add_to(m)

    datas = select_charger_station_location(MY_LAT, MY_LNG)
    charger_data = [asdict(d) for d in datas or []]

    # 충전소 마커 표시
    for c in charger_data:
        
        folium.Marker(
            [c["lat"], c["lng"]],
            popup=c["station_id"],
            tooltip=f"🔋 {c['station_name']}",
            icon=folium.Icon(color="blue", icon="bolt"),
        ).add_to(m)

    # ---- Folium 지도 렌더링 ----
    st_data = st_folium(m, width=800, height=500)

    # ---- 클릭 이벤트 ----
    if st_data and st_data["last_object_clicked"]:
        lat = st_data["last_object_clicked"]["lat"]
        lon = st_data["last_object_clicked"]["lng"]
        
        station_id = st_data["last_object_clicked_popup"]
        one_data_list = [asdict(d) for d in select_charger_station(station_id) or []]
        data = one_data_list[0]
        st.success(
f"""{data["station_name"]}, {data["use_time"]} \n
{data["addr"]} {data["location"]} \n
{data["limit_detail"]}     
"""
        )
        # 예: DB나 API를 이용한 충전소 상세조회
        st.write(
            "👉 이 좌표 인근의 충전소 정보를 불러오는 로직을 여기에 추가할 수 있습니다."
        )
else:
    st.warning("📍 위치 정보를 불러오는 중이거나, 권한이 거부되었습니다.")

# 스케줄 등록
schedule.every(30).minutes.do(job)


def background_thread():
    while True:
        schedule.run_pending()
        time.sleep(1)


if "scheduler_started" not in st.session_state:
    threading.Thread(target=background_thread, daemon=True).start()
    st.session_state["scheduler_started"] = True
    st.success("백그라운드 스케줄러 시작됨")

st.title("EV 충전소 모니터링")
st.write("스케줄러가 30분마다 자동 실행 중입니다.")
if st.button("수동 실행"):
    job()
    st.info("수동으로 job() 실행 완료!")
