import streamlit as st
import pandas as pd
import layout
# from services.get_charge_price import scrapping_charge_price # 이 페이지에서는 스크래핑이 필요 없어 임포트 제거

# 기본 레이아웃 적용
layout.base_layout()

# ----------------------------------------------------
# 1. 가상의 데이터프레임 생성 (제공해주신 DB 스키마 기반)
# ----------------------------------------------------

# (1) 지역 코드 데이터 (area_code_master 기반)
# 서울, 부산, 경기 데이터 일부만 사용
area_data = [
    ('11', '11110', '서울특별시', '종로구'), ('11', '11140', '서울특별시', '중구'),
    ('11', '11680', '서울특별시', '강남구'), ('11', '11740', '서울특별시', '강동구'),
    ('26', '26110', '부산광역시', '중구'), ('26', '26350', '부산광역시', '해운대구'),
    ('41', '41110', '경기도', '수원시'), ('41', '41130', '경기도', '성남시'),
    ('41', '41830', '경기도', '양평군')
]
area_code_master = pd.DataFrame(area_data, columns=['zcode', 'zscode', 'region', 'sub_region'])

# (2) 가상의 운영기관-요금 정보 (charge_price 및 operator_info 기반)
# 실제 DB에서는 여러 테이블을 조인해서 가져오는 데이터입니다.
price_data = [
    # 운영기관, 충전기 타입, 회원가, 비회원가, 지역 (zcode, zscode)
    ('에버차지', 'DC콤보', 290.00, 310.00, '11', '11110'), 
    ('에버차지', 'AC완속', 190.00, 210.00, '11', '11680'), 
    ('파워EV', 'DC차데모', 310.00, 330.00, '41', '41130'), 
    ('파워EV', 'DC콤보', 280.00, 300.00, '41', '41830'),  
    ('마린EV', 'DC콤보', 270.00, 290.00, '26', '26350'),  
    ('모두의EV', 'DC콤보', 250.00, 270.00, '11', '11680'), 
    ('모두의EV', 'AC완속', 150.00, 170.00, '41', '41110'), 
    ('테스트EV', 'DC콤보', 300.00, 320.00, '41', '41110'), 
]
df_charge_price = pd.DataFrame(price_data, columns=[
    'operator_name', 'charger_type', 'member_price', 'guest_price', 'zcode', 'zscode'
])

# 지역 코드와 요금 정보 테이블을 병합하여 시/도, 시/군/구 정보를 추가
df_charge_price = pd.merge(
    df_charge_price, 
    area_code_master, 
    on=['zcode', 'zscode'], 
    how='left'
)

# ----------------------------------------------------
# 2. 요금 비교 페이지 UI 구성
# ----------------------------------------------------

st.title('💰 지역별 충전 요금 비교')
st.markdown("전기차 충전 요금을 지역별, 운영기관별로 비교해보세요.")
st.markdown("---")


# --- 지역 선택 UI ---
st.header("지역 선택")

# 1. '시/도' 선택
# 데이터에 없는 지역이 선택되는 것을 방지하기 위해 데이터에 있는 지역만 목록으로 구성
regions = ['선택하세요'] + df_charge_price['region'].dropna().unique().tolist()
selected_region = st.selectbox("1. 시/도 선택", regions)

selected_sub_region = '전체' # 기본값 설정

# 컬럼 분할 (UI 정렬)
col1, col2 = st.columns([1, 1])

if selected_region != '선택하세요':
    # 해당 시/도에 해당하는 시/군/구 목록 필터링
    sub_regions_filter = df_charge_price[df_charge_price['region'] == selected_region]
    sub_regions = ['전체'] + sub_regions_filter['sub_region'].dropna().unique().tolist()
    
    # 2. '시/군/구' 선택
    selected_sub_region = col1.selectbox("2. 시/군/구 선택", sub_regions)
    
    # --- 요금표 표시 로직 ---
    st.markdown(f"### 📍 **{selected_region}** {selected_sub_region} 지역 요금표")

    # 데이터 필터링 시작
    filtered_data = df_charge_price[df_charge_price['region'] == selected_region].copy()
    
    # '전체'가 아닌 경우 시/군/구로 한 번 더 필터링
    if selected_sub_region != '전체':
        filtered_data = filtered_data[filtered_data['sub_region'] == selected_sub_region].copy()
    
    
    if filtered_data.empty:
        st.warning(f"선택하신 지역에 해당하는 요금 정보가 없습니다. (시/군/구 데이터 매칭 오류 가능성)")
    else:
        # 출력용 데이터프레임 정리
        display_df = filtered_data.drop(columns=['zcode', 'zscode', 'region', 'sub_region'])
        
        display_df = display_df.rename(columns={
            'operator_name': '운영기관',
            'charger_type': '충전기 타입',
            'member_price': '회원가 (원/kWh)',
            'guest_price': '비회원가 (원/kWh)'
        })
        
        # 운영기관별로 그룹화하여 표시
        for operator in display_df['운영기관'].unique():
            st.markdown(f"#### 🏢 {operator}")
            # 운영기관 이름을 제외하고 출력
            operator_df = display_df[display_df['운영기관'] == operator].drop(columns=['운영기관'])
            
            # 가격은 소수점 둘째 자리까지 표시하도록 포매팅
            st.dataframe(
                operator_df.style.format({
                    '회원가 (원/kWh)': "{:,.2f}",
                    '비회원가 (원/kWh)': "{:,.2f}"
                }), 
                use_container_width=True, 
                hide_index=True
            )
        st.caption("※ 이 정보는 제공해주신 스키마 기반의 가상 데이터입니다.")

else:
    # 초기 상태 메시지
    st.info("지역을 선택하면 해당 지역의 충전 요금 정보를 확인할 수 있습니다.")


#==============================================================================================================================
# 실제 운영기관 데이터 entity 적용시

import pandas as pd
# 실제 DB 커넥션 라이브러리 임포트 (예시: SQLAlchemy)
# from sqlalchemy import create_engine 

# DB 연결 정보를 환경 변수 등에서 가져오는 것이 좋습니다.
# DATABASE_URL = "postgresql://user:password@host:port/dbname"
# engine = create_engine(DATABASE_URL)

def get_db_connection():
    """
    실제 DB 연결 객체를 반환합니다. 
    로컬 테스트를 위해 잠시 Pandas를 이용한 가상 DB를 반환합니다.
    """
    # TODO: 실제 운영 환경에서는 SQLAlchemy 엔진이나 Psycopg2 커넥션을 반환하도록 변경하세요.
    
    # --- [START] 실제 DB 연결 코드로 대체할 부분 ---
    # 현재는 가상 데이터를 이용해 DB에서 데이터를 조회하는 흉내를 냅니다.
    
    # (1) area_code_master 데이터
    area_data = [
        ('11', '11110', '서울특별시', '종로구'), ('11', '11140', '서울특별시', '중구'),
        ('11', '11680', '서울특별시', '강남구'), ('11', '11740', '서울특별시', '강동구'),
        ('26', '26110', '부산광역시', '중구'), ('26', '26350', '부산광역시', '해운대구'),
        ('41', '41110', '경기도', '수원시'), ('41', '41130', '경기도', '성남시'),
        ('41', '41830', '경기도', '양평군')
    ]
    area_code_master = pd.DataFrame(area_data, columns=['zcode', 'zscode', 'region', 'sub_region'])

    # (2) charge_price, operator_info, charger_station 조인 가상 데이터
    price_data = [
        ('에버차지', 'DC콤보', 290.00, 310.00, '11', '11110'), 
        ('에버차지', 'AC완속', 190.00, 210.00, '11', '11680'), 
        ('파워EV', 'DC차데모', 310.00, 330.00, '41', '41130'), 
        ('모두의EV', 'DC콤보', 250.00, 270.00, '11', '11680'), 
    ]
    df_charge_price_raw = pd.DataFrame(price_data, columns=[
        'operator_name', 'charger_type', 'member_price', 'guest_price', 'zcode', 'zscode'
    ])
    
    df_charge_price = pd.merge(
        df_charge_price_raw, 
        area_code_master, 
        on=['zcode', 'zscode'], 
        how='left'
    )
    
    return df_charge_price 
    # --- [END] 실제 DB 연결 코드로 대체할 부분 ---


def fetch_charge_price_data() -> pd.DataFrame:
    """
    DB에서 필요한 모든 충전 요금 정보를 조인하여 가져오는 함수입니다.
    
    실제 SQL 쿼리 예시 (여러 테이블 조인):
    SELECT 
        T1.operator_name, T4.description AS charger_type, T2.member_price, T2.guest_price,
        T3.region, T3.sub_region, T1.zcode, T1.zscode
    FROM charger_station T1
    JOIN charge_price T2 ON T1.operator_id = T2.operator_code
    JOIN area_code_master T3 ON T1.zscode = T3.zscode
    JOIN charger_meta T4 ON T1.charger_type = T4.charger_type
    WHERE T2.price_type_name = '기본요금' -- 필요시 필터 추가
    """
    try:
        # get_db_connection()을 사용하여 DB에서 데이터를 가져옵니다.
        # 실제 DB 연결 시: return pd.read_sql(sql_query, engine)
        
        # 현재는 가상 데이터를 반환합니다.
        return get_db_connection()
    except Exception as e:
        print(f"DB 데이터 조회 중 오류 발생: {e}")
        return pd.DataFrame() # 오류 발생 시 빈 데이터프레임 반환