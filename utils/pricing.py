from dataclasses import dataclass
import math

@dataclass
class PricingConfig:
    base_callout: int = 6500
    per_km: int = 180
    per_m3: int = 900
    stairs_fee_per_flight: int = 1000
    packing_flat: int = 5000
    piano_flat: int = 12000
    assembly_per_room: int = 2000
    weekend_multiplier: float = 1.10

def estimate_price(distance_km: float, volume_m3: float, stairs_from: int,
                   stairs_to: int, extras: dict, cfg: PricingConfig = PricingConfig()) -> int:
    price = cfg.base_callout
    price += int(distance_km * cfg.per_km)
    price += int(volume_m3 * cfg.per_m3)
    price += (stairs_from + stairs_to) * cfg.stairs_fee_per_flight
    if extras.get("packing"): price += cfg.packing_flat
    if extras.get("piano"): price += cfg.piano_flat
    if extras.get("assembly_rooms", 0): price += extras["assembly_rooms"] * cfg.assembly_per_room
    if extras.get("is_weekend"): price = int(price * cfg.weekend_multiplier)
    return int(math.ceil(price / 50.0) * 50)

def pretty(cents: int, currency="£"): return f"{currency}{cents/100:,.2f}"
