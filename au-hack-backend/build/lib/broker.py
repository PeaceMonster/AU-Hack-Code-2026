import csv
from datetime import datetime

import pandas as pd

from .model import FlowInfo, InfoBundle, Region

DATA = "data"


# def get_spot_prices(region: Region):
#     with open(f"{DATA}/spot-price/{region}-spot-price.csv") as f:
#         data = list(csv.DictReader(f))
#     return data


def get_info(region: Region) -> InfoBundle:

    return InfoBundle(
        region=region,
        price=spot_price(region),
        load=total_load(region),
        total_flow_in=flow_in(region),
        total_flow_out=flow_out(region),
        ingoing_flows=flows_in(region),
    )


def get_info_timestamp(region: Region, timestamp: datetime) -> InfoBundle:

    return InfoBundle(
        region=region,
        price=spot_price(region, timestamp),
        load=total_load(region, timestamp),
        total_flow_in=flow_in(region, timestamp),
        total_flow_out=flow_out(region, timestamp),
        ingoing_flows=flows_in(region, timestamp),
    )


def _load_dataframe(
    region: str, folder: str, dataset: str, timestamp: datetime | None = None
) -> pd.DataFrame:

    # Read dataframe and convert date-time
    df = pd.read_csv(f"{DATA}/{folder}/{region}-{dataset}.csv")
    df["time"] = pd.to_datetime(df["time"], format="ISO8601", utc=True)

    # Sort data according to timestamp
    df = df.sort_values("time", ascending=False)

    if timestamp is not None:
        df = df[df["time"] <= timestamp]

    return df


def spot_price(region: Region, timestamp: datetime | None = None) -> float:

    # Retrieve most closest row entry
    df = _load_dataframe(region, "spot-price", "spot-price", timestamp)
    return df["value (EUR/MWh)"].iloc[0]


def total_load(region: Region, timestamp: datetime | None = None) -> float:

    # Retrieve most recent row entry
    df = _load_dataframe(region, "total-load", "total-load", timestamp)
    return df["value (MW)"].iloc[0]


def flows_in(region: Region, timestamp: datetime | None = None) -> list[FlowInfo]:

    # Get overview over all flows in
    df = _load_dataframe(region, "flows", "physical-flows-in", timestamp)
    df = df.groupby("zone")

    # Compute all flow infos
    infos: list[FlowInfo] = list()

    # TODO: Make sure that fetched data-points
    # are from the same time-slot
    for zone, group in df:
        for row in group.head(1).itertuples(index=False):
            reg_from, reg_to = zone.split("->")
            infos.append(
                FlowInfo(
                    region_from=reg_from,
                    region_to=reg_to,
                    amount=row[2],
                )
            )

    # Return collected infos
    return infos


def flow_in(region: Region, timestamp: datetime | None = None) -> float:

    # Retrieve most recent row entry
    df = _load_dataframe(region, "flows", "physical-flows-in", timestamp)
    df = df.groupby("zone").head(1)
    total_flow: float = df["value (MW)"].sum()

    return total_flow


def flow_out(region: Region, timestamp: datetime | None = None) -> float:
    # TODO
    return -1.0
