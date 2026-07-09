from pathlib import Path

# --------------------------------------------------
# Map origin-destination pairs to SUMO route IDs
# --------------------------------------------------

ROUTE_MAP = {
    ("north", "south"): "northSouth",
    ("north", "east"): "northEast",
    ("north", "west"): "northWest",

    ("south", "north"): "southNorth",
    ("south", "east"): "southEast",
    ("south", "west"): "southWest",

    ("east", "west"): "eastWest",
    ("east", "north"): "eastNorth",
    ("east", "south"): "eastSouth",

    ("west", "east"): "westEast",
    ("west", "north"): "westNorth",
    ("west", "south"): "westSouth",
}

# --------------------------------------------------
# Traffic profile
# --------------------------------------------------

traffic_profile = [

    {
        "name": "night",
        "time": (0, 100),

        "demand": {

            ("north", "south"): 0.10,
            ("north", "east"): 0.03,
            ("north", "west"): 0.02,

            ("south", "north"): 0.08,
            ("south", "east"): 0.02,
            ("south", "west"): 0.02,

            ("east", "west"): 0.10,
            ("east", "north"): 0.03,
            ("east", "south"): 0.02,

            ("west", "east"): 0.08,
            ("west", "north"): 0.02,
            ("west", "south"): 0.02,
        },
    },

    {
        "name": "morning",
        "time": (100, 200),

        "demand": {

            ("north", "south"): 0.40,
            ("north", "east"): 0.15,
            ("north", "west"): 0.05,

            ("south", "north"): 0.12,
            ("south", "east"): 0.04,
            ("south", "west"): 0.04,

            ("east", "west"): 0.12,
            ("east", "north"): 0.05,
            ("east", "south"): 0.03,

            ("west", "east"): 0.10,
            ("west", "north"): 0.04,
            ("west", "south"): 0.03,
        },
    },

    {
        "name": "rush",
        "time": (200, 350),

        "demand": {

            ("north", "south"): 0.70,
            ("north", "east"): 0.20,
            ("north", "west"): 0.10,

            ("south", "north"): 0.25,
            ("south", "east"): 0.08,
            ("south", "west"): 0.07,

            ("east", "west"): 0.20,
            ("east", "north"): 0.08,
            ("east", "south"): 0.07,

            ("west", "east"): 0.18,
            ("west", "north"): 0.06,
            ("west", "south"): 0.06,
        },
    },

    {
        "name": "evening",
        "time": (350, 450),

        "demand": {

            ("north", "south"): 0.20,
            ("north", "east"): 0.05,
            ("north", "west"): 0.05,

            ("south", "north"): 0.20,
            ("south", "east"): 0.05,
            ("south", "west"): 0.05,

            ("east", "west"): 0.50,
            ("east", "north"): 0.10,
            ("east", "south"): 0.10,

            ("west", "east"): 0.60,
            ("west", "north"): 0.10,
            ("west", "south"): 0.10,
        },
    },

    {
        "name": "night2",
        "time": (450, 500),

        "demand": {

            ("north", "south"): 0.10,
            ("north", "east"): 0.03,
            ("north", "west"): 0.02,

            ("south", "north"): 0.08,
            ("south", "east"): 0.02,
            ("south", "west"): 0.02,

            ("east", "west"): 0.10,
            ("east", "north"): 0.03,
            ("east", "south"): 0.02,

            ("west", "east"): 0.08,
            ("west", "north"): 0.02,
            ("west", "south"): 0.02,
        },
    },

]

# --------------------------------------------------
# Read template
# --------------------------------------------------

template = Path("routes_template.rou.xml").read_text()

flow_text = ""

# --------------------------------------------------
# Generate flow XML
# --------------------------------------------------

for period in traffic_profile:

    begin, end = period["time"]

    for (origin, destination), probability in period["demand"].items():

        route = ROUTE_MAP[(origin, destination)]

        flow_text += f"""
    <flow
        id="{period['name']}_{route}"
        type="car"
        route="{route}"
        begin="{begin}"
        end="{end}"
        probability="{probability}"/>
"""

# --------------------------------------------------
# Insert flows into template
# --------------------------------------------------

output = template.replace(
    "</routes>",
    flow_text + "\n</routes>"
)

# --------------------------------------------------
# Save generated file
# --------------------------------------------------

Path("routes.rou.xml").write_text(output)

print("Successfully generated routes.rou.xml")