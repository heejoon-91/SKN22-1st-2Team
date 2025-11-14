from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from DTO.charger_info_dto import ChargerInfoDTo
from DTO.charger_stat_dto import ChargerStatDto


@dataclass
class Charger_detail:
    charger_id: str
    station_id: str
    charger_type: str
    output_kw: float
    method: str
    del_yn: str
    del_detail: str
    stat: int
    stat_upd_dt: Optional[datetime] = None
    last_tsdt: Optional[datetime] = None
    last_tedt: Optional[datetime] = None
    now_tsdt: Optional[datetime] = None

    @classmethod
    def from_dtos(
        cls, info_dto: ChargerInfoDTo, stat_dto: ChargerStatDto
    ) -> Charger_detail:
        """
        ChargerInfoDTo + ChargerStatDto → Charger_detail 변환
        """

        def parse_datetime(value: Optional[str]) -> Optional[datetime]:
            if not value:
                return None
            try:
                return datetime.strptime(value, "%Y%m%d%H%M%S")
            except ValueError:
                return None

        def parse_float(value: Optional[str]) -> float:
            try:
                return float(value) if value not in (None, "", "null") else 0.0
            except ValueError:
                return 0.0

        return cls(
            charger_id=stat_dto.chgerId or info_dto.chgerId or "",
            station_id=stat_dto.statId or info_dto.statId or "",
            charger_type=info_dto.chgerType or "",
            output_kw=parse_float(info_dto.output),
            method=info_dto.method or "",
            del_yn=info_dto.delYn or "",
            del_detail=info_dto.delDetail or "",
            stat=int(stat_dto.stat) if stat_dto.stat and stat_dto.stat.isdigit() else 0,
            stat_upd_dt=parse_datetime(stat_dto.statUpdDt),
            last_tsdt=parse_datetime(stat_dto.lastTsdt),
            last_tedt=parse_datetime(stat_dto.lastTedt),
            now_tsdt=parse_datetime(stat_dto.nowTsdt),
        )
