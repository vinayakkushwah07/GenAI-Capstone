from enum import Enum

class AccesRole(str, Enum):
    # Literal["user","admin","ce","junior","senior"]
    user = "user"
    admin="admin"
    ce= "ce"
    junior= "junior"
    senior = "senior"