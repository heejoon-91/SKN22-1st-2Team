from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from DTO.charger_info_dto import ChargerInfoDTo


@dataclass
class Charger_station:
    station_id: str
    station_name: str
    addr: str
    addr_detail: str
    location: str
    lat: float
    lng: float
    use_time: str
    parking_free: str
    note: str
    limit_yn: str
    limit_detail: str
    del_yn: str
    del_detail: str
    kind: str
    kind_detail: str
    zcode: str
    zscode: str
    traffic_yn: str
    year: str
    floor_num: str
    floor_type: str
    operator_id: str
    update_dt: Optional[datetime] = None

    # ✅ DTO → 엔티티 변환 클래스 메서드
    
    @classmethod
    def from_dto(cls, dto: ChargerInfoDTo) -> Charger_station:
        def parse_datetime(value: Optional[str]) -> Optional[datetime]:
            """문자열(YYYYMMDDHHMMSS) → datetime 변환"""
            if not value:
                return None
            try:
                return datetime.strptime(value, "%Y%m%d%H%M%S")
            except ValueError:
                return None

        def parse_float(value: Optional[str]) -> float:
            """문자열 → float 변환 (None, 'null' 안전처리)"""
            try:
                return float(value) if value not in (None, "", "null") else 0.0
            except ValueError:
                return 0.0

        return cls(
            station_id=dto.statId or "",
            station_name=dto.statNm or "",
            addr=dto.addr or "",
            addr_detail=dto.addrDetail or "",
            location=dto.location or "",
            lat=parse_float(dto.lat),
            lng=parse_float(dto.lng),
            use_time=dto.useTime or "",
            parking_free=dto.parkingFree or "",
            note=dto.note or "",
            limit_yn=dto.limitYn or "",
            limit_detail=dto.limitDetail or "",
            del_yn=dto.delYn or "",
            del_detail=dto.delDetail or "",
            kind=dto.kind or "",
            kind_detail=dto.kindDetail or "",
            zcode=dto.zcode or "",
            zscode=dto.zscode or "",
            traffic_yn=dto.trafficYn or "",
            year=dto.year or "",
            floor_num=dto.floorNum or "",
            floor_type=dto.floorType or "",
            operator_id=dto.busiId or "",
            update_dt=parse_datetime(dto.statUpdDt),
        )
