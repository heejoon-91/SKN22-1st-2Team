import streamlit as st
import pandas as pd

# ----------------------------------------------------
# 1. 가상의 데이터 생성 (제공해주신 스키마 기반)
# ----------------------------------------------------

# (1) 지역 코드 데이터 (area_code_master 기반)
# 제공해주신 INSERT INTO 구문을 기반으로 데이터프레임 생성
area_data = [
    ('11', '11110', '서울특별시', '종로구'), ('11', '11140', '서울특별시', '중구'),
    ('11', '11680', '서울특별시', '강남구'), ('11', '11740', '서울특별시', '강동구'),
    ('26', '26110', '부산광역시', '중구'), ('26', '26350', '부산광역시', '해운대구'),
    ('41', '41110', '경기도', '수원시'), ('41', '41130', '경기도', '성남시'),
    ('41', '41830', '경기도', '양평군')
]
area_code_master = pd.DataFrame(area_data, columns=['zcode', 'zscode', 'region', 'sub_region'])


# (2) 가상의 운영기관-요금 정보 (charge_price 및 operator_info 기반)
# 실제 운영기관 및 요금 정보를 가상으로 생성합니다.
price_data = [
    # 서울특별시/경기도 권역 요금
    ('Seoul_Company', '에버차지', '11', '11110', '서울특별시', '종로구', 'DC콤보', 290.00, 310.00),
    ('Seoul_Company', '에버차지', '11', '11680', '서울특별시', '강남구', 'AC완속', 190.00, 210.00),
    ('Gyeonggi_Operator', '파워EV', '41', '41130', '경기도', '성남시', 'DC차데모', 310.00, 330.00),
    ('Gyeonggi_Operator', '파워EV', '41', '41830', '경기도', '양평군', 'DC콤보', 280.00, 300.00),
    # 부산광역시 권역 요금
    ('Busan_EV', '마린EV', '26', '26350', '부산광역시', '해운대구', 'DC콤보', 270.00, 290.00),
    ('Busan_EV', '마린EV', '26', '26350', '부산광역시', '해운대구', 'AC완속', 170.00, 190.00),
    # 전국 공통 요금 (전국구 운영사)
    ('National_EV', '모두의EV', '11', '11110', '서울특별시', '종로구', 'DC콤보', 250.00, 270.00),
    ('National_EV', '모두의EV', '41', '41130', '경기도', '성남시', 'DC콤보', 250.00, 270.00),
    ('National_EV', '모두의EV', '26', '26350', '부산광역시', '해운대구', 'DC콤보', 250.00, 270.00),
]
# 이 데이터프레임은 실제 DB의 charger_station, charge_price, operator_info, charger_meta를 조인한 형태를 가정합니다.
# 'operator_code'는 charge_price, 'operator_name'은 operator_info의 필드명을 따랐습니다.
df_charge_price = pd.DataFrame(price_data, columns=[
    'operator_code', 'operator_name', 'zcode', 'zscode', 'region', 'sub_region', 
    'charger_type', 'member_price', 'guest_price'
])

# ----------------------------------------------------
# 2. Streamlit 앱 구성
# ----------------------------------------------------

def run_app():
    st.set_page_config(
        page_title="지역별 충전 요금 정보",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.title("⚡ 지역별 전기차 충전 요금 안내")
    st.markdown("---")
    
    # ------------------
    # 지역 선택 사이드바
    # ------------------
    with st.sidebar:
        st.header("지역 선택")

        # 1. '시/도' 선택 박스 (region)
        regions = area_code_master['region'].unique().tolist()
        selected_region = st.selectbox("1. 시/도 선택", regions)
        
        # 필터링: 선택된 시/도에 해당하는 시/군/구만 추출
        sub_regions_filter = area_code_master[area_code_master['region'] == selected_region]

        # 2. '시/군/구' 선택 박스 (sub_region)
        sub_regions = sub_regions_filter['sub_region'].unique().tolist()
        # '전체' 옵션을 추가하여 해당 시/도의 모든 데이터를 볼 수 있게 함
        sub_regions.insert(0, '전체')
        
        selected_sub_region = st.selectbox("2. 시/군/구 선택", sub_regions)


    # ------------------
    # 메인 페이지 콘텐츠
    # ------------------

    # 1. 데이터 필터링 로직
    # 선택된 시/도로 필터링
    filtered_data = df_charge_price[df_charge_price['region'] == selected_region].copy()
    
    # '전체'를 선택하지 않았다면 시/군/구로 한 번 더 필터링
    if selected_sub_region != '전체':
        filtered_data = filtered_data[filtered_data['sub_region'] == selected_sub_region].copy()
    
    
    # 2. 결과 출력
    st.subheader(f"📍 **{selected_region}** {selected_sub_region if selected_sub_region != '전체' else ''} 지역 요금 정보")

    if filtered_data.empty:
        st.warning("선택하신 지역에 해당하는 요금 정보가 없습니다.")
    else:
        # 출력용 데이터프레임 정리 (불필요한 컬럼 제거 및 컬럼명 변경)
        display_df = filtered_data.drop(columns=['zcode', 'zscode', 'region', 'sub_region', 'operator_code'])
        
        display_df = display_df.rename(columns={
            'operator_name': '운영기관',
            'charger_type': '충전기 타입',
            'member_price': '회원가 (원/kWh)',
            'guest_price': '비회원가 (원/kWh)'
        })
        
        # 운영기관별로 요금표를 보기 쉽게 그룹화하여 표시
        for operator in display_df['운영기관'].unique():
            st.markdown(f"#### 🏢 {operator} 요금")
            operator_df = display_df[display_df['운영기관'] == operator].drop(columns=['운영기관'])
            # 테이블 출력
            st.dataframe(operator_df, use_container_width=True, hide_index=True)
            st.markdown("---")

# 앱 실행
if __name__ == "__main__":
    run_app()