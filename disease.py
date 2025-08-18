"""
Defines disease characteristics and types.
"""

class Disease:
    def __init__(self, name, infectivity, severity, lethality, incubation_period, infection_duration, transmission_land, transmission_air, transmission_sea):
        self.name = name
        self.infectivity = infectivity  # How easily it spreads (per second)
        self.severity = severity      # How severe the symptoms are (0-1)
        self.lethality = lethality    # Mortality rate (0-1)
        self.incubation_period = incubation_period # Days from exposure to infectiousness
        self.infection_duration = infection_duration # Days an individual is infectious
        self.transmission_land = transmission_land # Spread modifier for land
        self.transmission_air = transmission_air   # Spread modifier for air travel
        self.transmission_sea = transmission_sea   # Spread modifier for sea travel

class Influenza(Disease):
    def __init__(self):
        super().__init__(
            name="Influenza",
            infectivity=4.3e-6, # R0 ~1.3
            severity=0.1,
            lethality=0.001, # 0.1%
            incubation_period=2, # Days
            infection_duration=6, # Days
            transmission_land=0.7,
            transmission_air=0.8,
            transmission_sea=0.6
        )

class COVID19(Disease):
    def __init__(self):
        super().__init__(
            name="COVID-19",
            infectivity=5.6e-6, # R0 ~2.8
            severity=0.3,
            lethality=0.01, # 1%
            incubation_period=5, # Days
            infection_duration=10, # Days
            transmission_land=0.8,
            transmission_air=0.9,
            transmission_sea=0.7
        )

class Measles(Disease):
    def __init__(self):
        super().__init__(
            name="Measles",
            infectivity=3.75e-5, # R0 ~15
            severity=0.5,
            lethality=0.0015, # 0.15%
            incubation_period=12, # Days
            infection_duration=8, # Days
            transmission_land=0.9,
            transmission_air=0.7,
            transmission_sea=0.5
        )

class Ebola(Disease):
    def __init__(self):
        super().__init__(
            name="Ebola",
            infectivity=5.5e-6, # R0 ~1.95
            severity=0.9,
            lethality=0.5, # 50%
            incubation_period=9, # Days
            infection_duration=7, # Days
            transmission_land=0.3, # Primarily through direct contact
            transmission_air=0.1,
            transmission_sea=0.05
        )

class Smallpox(Disease):
    def __init__(self):
        super().__init__(
            name="Smallpox",
            infectivity=3.7e-6, # R0 ~4.5
            severity=0.8,
            lethality=0.3, # 30%
            incubation_period=12, # Days
            infection_duration=24, # Days
            transmission_land=0.8,
            transmission_air=0.6,
            transmission_sea=0.4
        )

class CommonCold(Disease):
    def __init__(self):
        super().__init__(
            name="Common Cold (Rhinovirus)",
            infectivity=1.0e-5, # R0 ~2.5
            severity=0.05,
            lethality=0.0, # Effectively 0
            incubation_period=2, # Days
            infection_duration=5, # Days
            transmission_land=0.9,
            transmission_air=0.8,
            transmission_sea=0.7
        )
