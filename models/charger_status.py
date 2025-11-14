from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from DTO.charger_stat_dto import ChargerStatDto


@dataclass
class Charger_status:
    busi_id: str
    station_id: str
    charger_id: str
    stat: int
    stat_upd_dt: Optional[datetime] = None
    last_tsdt: Optional[datetime] = None
    last_tedt: Optional[datetime] = None
    now_tsdt: Optional[datetime] = None
    reg_dt: Optional[datetime] = field(default_factory=datetime.now)
    upd_dt: Optional[datetime] = None


    @classmethod
    def from_dto(cls, dto: "ChargerStatDto") -> "Charger_status":
        def parse_time(value: Optional[str]) -> Optional[datetime]:
            if not value:
                return None
            try:
                return datetime.strptime(value, "%Y%m%d%H%M%S")
            except ValueError:
                return None

        return cls(
            busi_id=dto.busiId or "",
            station_id=dto.statId or "",
            charger_id=dto.chgerId or "",
            stat=int(dto.stat) if dto.stat and dto.stat.isdigit() else 0,
            stat_upd_dt=parse_time(dto.statUpdDt),
            last_tsdt=parse_time(dto.lastTsdt),
            last_tedt=parse_time(dto.lastTedt),
            now_tsdt=parse_time(dto.nowTsdt),
        )