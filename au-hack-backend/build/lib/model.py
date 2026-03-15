from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum


class Region(StrEnum):
    AT = "AT"
    BE = "BE"
    CH = "CH"
    CZ = "CZ"
    DE = "DE"
    DK1 = "DK1"
    DK2 = "DK2"
    FR = "FR"
    NL = "NL"
    NO2 = "NO2"
    PL = "PL"
    SE4 = "SE4"


@dataclass
class FlowInfo:
    """Flow information unit"""

    region_from: Region
    region_to: Region
    amount: float


@dataclass
class InfoBundle:
    """Information-Bundle containing information related to a single region"""

    region: Region
    price: float
    load: float
    total_flow_in: float
    total_flow_out: float
    ingoing_flows: list[FlowInfo]
