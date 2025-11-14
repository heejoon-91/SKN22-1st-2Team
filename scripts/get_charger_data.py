# scripts/update_data.py
import os
import traceback
from typing import Dict, List, Optional, Union
import requests
from dotenv import load_dotenv

from DTO.charger_info_dto import ChargerInfoDTo
from DTO.charger_stat_dto import ChargerStatDto


class EVChargerAPI:
    """공공데이터 전기차 충전소 API 핸들러"""

    def __init__(self) -> None:
        load_dotenv()
        self.base_url: str = os.getenv("API_BASE_URL", "")
        self.api_key: str = os.getenv("API_KEY", "")

    def _get(self, endpoint: str, params: dict):
        """
        공통 GET 요청 처리
            
        Args:
            endpoint (str): API 엔드포인트
            params (dict): 요청 파라미터

        Returns:
            Optional[List[Dict[str, Any]]]: API 응답 데이터의 item 리스트 또는 None

        """
        params["serviceKey"] = self.api_key
        try:
            response = requests.get(f"{self.base_url}/{endpoint}", params=params)
            response.raise_for_status()
            data = response.json()
            return data.get("items", {}).get("item", None)
        except Exception as e:
            print(e)
            print(traceback.format_exception)

    def get_charger_info(self, sta_id: str = "", chger_id: str = ""):
        """
        충전기 정보 조회

        Args:
            sta_id (str): 충전소 ID
            chger_id (str): 충전기 ID

        Returns:
            Optional[List[ChargerInfoDTo]]: 충전기 정보 DTO 리스트
        """

        params : Dict[str, Union[str, int]] = {
            "pageNo": 1,
            "numOfRows": 10,
            "dataType": "JSON",
        }
        if sta_id:
            params["staId"] = sta_id
        if chger_id:
            params["chgerId"] = chger_id

        result = self._get("getChargerInfo", params)
        if result:
            # JSON의 "null" 문자열을 실제 None으로 변환
            def clean_null(v): return None if v == "null" else v
            cleaned = [{k: clean_null(v) for k, v in item.items()} for item in result]
            return [ChargerInfoDTo(**item) for item in cleaned]
        return None

    def get_charger_status(self, sta_id: str = "", chger_id: str = "") -> Optional[List[ChargerStatDto]]:
        """
        충전기 상태 조회

        Args:
            sta_id (str): 충전소 ID
            chger_id (str): 충전기 ID

        Returns:
            Optional[List[ChargerStatDto]]: 충전기 상태 DTO 리스트
        """
        params: Dict[str, Union[str, int]] = {
            "pageNo": 1,
            "numOfRows": 10,
            "dataType": "JSON",
        }
        if sta_id:
            params["staId"] = sta_id
        if chger_id:
            params["chgerId"] = chger_id

        result = self._get("getChargerStatus", params)
        if result:
            return [ChargerStatDto(**item) for item in result]
        return None

if __name__ == "__main__":
    api = EVChargerAPI()

    # 테스트용
    # sta_id = "28260005"
    # chger_id = "O2"
    sta_id = ""
    chger_id = ""

    info = api.get_charger_info(sta_id, chger_id)
    status = api.get_charger_status(sta_id, chger_id)

    print("=== 충전기 정보 ===")
    print(info)

    print("\n=== 충전기 상태 ===")
    print(status)
