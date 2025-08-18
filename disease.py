"""
Defines disease characteristics and types.
"""

class Disease:
    def __init__(self, name, infectivity, severity, lethality, transmission_land, transmission_air, transmission_sea):
        self.name = name
        self.infectivity = infectivity  # How easily it spreads (0-1)
        self.severity = severity      # How severe the symptoms are (0-1)
        self.lethality = lethality    # Mortality rate (0-1)
        self.transmission_land = transmission_land # Spread modifier for land
        self.transmission_air = transmission_air   # Spread modifier for air travel
        self.transmission_sea = transmission_sea   # Spread modifier for sea travel

class Influenza(Disease):
    def __init__(self):
        super().__init__(
            name="Influenza",
            infectivity=0.6,
            severity=0.3,
            lethality=0.01,
            transmission_land=0.7,
            transmission_air=0.8,
            transmission_sea=0.6
        )

class COVID19(Disease):
    def __init__(self):
        super().__init__(
            name="COVID-19",
            infectivity=0.7,
            severity=0.5,
            lethality=0.02,
            transmission_land=0.8,
            transmission_air=0.9,
            transmission_sea=0.7
        )

class Measles(Disease):
    def __init__(self):
        super().__init__(
            name="Measles",
            infectivity=0.9,
            severity=0.6,
            lethality=0.002,
            transmission_land=0.9,
            transmission_air=0.7,
            transmission_sea=0.5
        )
