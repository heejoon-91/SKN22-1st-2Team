
import traceback
from models.charger_station import Charger_station
from models.charger_detail import Charger_detail
from models.charger_status import Charger_status
from models.charge_price import ChargePrice 
from repository.db import get_connection


# save - 충전소 기본 정보(charger_station)

def save_station(station:Charger_station):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            sql = """
            insert into 
                        charger_station 
            VALUES (
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s
            )
            ON DUPLICATE KEY UPDATE
                use_time     = %s,
                limit_yn     = %s,
                limit_detail = %s,
                del_yn       = %s,
                del_detail   = %s,
                update_dt    = NOW()
            """
            params = (*station.as_tuple(), station.use_time, station.limit_yn, station.limit_detail, station.del_yn, station.del_detail)
            try:
                cursor.execute(sql, params)
                conn.commit()
            except Exception as e:
                conn.rollback()
                print(e)
                print(traceback.format_exc())

# save - 충전소 상세 정보(charger_station)

def save_charger_detail(charger_detail: Charger_detail):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            sql = """
            insert into 
                        charger_detail 
            values (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                    charger_type = %s,
                    output_kw    = %s,
                    method       = %s,
                    del_yn       = %s,
                    del_detail   = %s,
                    stat         = %s,
                    stat_upd_dt  = %s,
                    last_tsdt    = %s,
                    last_tedt    = %s,
                    now_tsdt     = %s
            """
            params = (*charger_detail.as_tuple(), 
                        charger_detail.charger_type,
                        charger_detail.output_kw,
                        charger_detail.method,
                        charger_detail.del_yn,
                        charger_detail.del_detail,
                        charger_detail.stat,
                        charger_detail.stat_upd_dt,
                        charger_detail.last_tsdt,
                        charger_detail.last_tedt,
                        charger_detail.now_tsdt
                        )
            try:
                cursor.execute(sql, params)
                conn.commit()
            except Exception as e:
                conn.rollback()
                print(e)
                print(traceback.format_exc())




# save - 충전기 상태 정보 (charger_status)

def save_charger_status(charger_status: Charger_status):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            sql = """
            insert into 
                        charger_station 
            values (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                    stat        = %s,
                    stat_upd_dt = %s,
                    last_tsdt   = %s,
                    last_tedt   = %s,
                    now_tsdt    = %s,
                    reg_dt      = %s,
                    upd_dt      = NOW()
            """

            params = (*charger_status.as_tuple, 
                    charger_status.stat,
                    charger_status.stat_upd_dt,
                    charger_status.last_tsdt,
                    charger_status.last_tedt,
                    charger_status.now_tsdt,
                    charger_status.reg_dt
                      )
            try:
                cursor.execute(sql, params)
                conn.commit()
            except Exception as e:
                conn.rollback()
                print(e)
                print(traceback.format_exc())
                

# save - charge_price(요금정보)

def save_charger_price(charge_price: ChargePrice):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            sql = """
            insert into 
                        charge_price 
            values (
                %s, %s, %s, %s, %s, %s, %s,%s)
            ON DUPLICATE KEY UPDATE
                    guest_price=%s,
                    update_dt=now()
            """
            params =(*charge_price.as_tuple(),charge_price.guest_price)
            try:
                cursor.execute(sql, params)
                conn.commit()
            except Exception as e:
                conn.rollback()
                print(e)
                print(traceback.format_exc())