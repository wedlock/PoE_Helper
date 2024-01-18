from dataclasses import dataclass
from numpy import uint8

@dataclass
class Entity:
    name = str
    pattern = uint8
    corner = [int,int]
    offset = [int,int]
