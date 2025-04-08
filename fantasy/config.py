# Define the CSV file name
CSV_FILE = "players.csv"
# Define the CSV file for teams
TEAM_CSV_FILE = "city_teams.csv"
PLAYER_TEAM_CSV_FILE = "player_teams.csv"
# Define the CSV files for schedules
CITY_SCHEDULE = "city_schedule.csv"
PLAYER_SCHEDULE = "player_schedule.csv"

POSITIONS = ["QB", "WR", "RB", "TE", "K"]
# Name pools categorized by species, with heroic, villainous, and WWE-style names
NAME_POOLS = {
    "Bear": {
        "heroic": ["Bear", "Sun Seeker", "Major", "Big Beaver", "Mule"],
        "villainous": ["Trout Terror", "Dozer", "Eclipse", "Tracker", "Titan", "Monster Mauller"],
        "wwe": ["Sleepy", "Mother", "Scottish", "Sun", "Creature of Claw", "Hairy", "Panda Bear",
               "Ursa", "Russian", "Kodiak", "Brother", "Moscow"],
        "first": ["Yogi", "Baloo", "Smokey", "Ursa", "Artic", "Brown", "Black", "Artic", "Polar", "Moon", "Winnie"],
        "last": ["Honey", "Cub", "Bear", "Moon", "The Poo", "Brook"]
    },
    "Sea Creature": {
        "heroic": ["Skipper", "Ray", "Angelfish", "Light Keeper", "Lake Legend"],
        "villainous": ["Bottom Dewler", "Eel", "Wave Crusher", "Kraken", "of the Deep", "Gator"],
        "wwe": ["Octo", "Angler", "Clown", "Tidal", "Righteous", "Captain", "Rainbow", "Manta"],
        "first": ["Bubbles", "ReefStalker", "Gilbert", "Skyler", "Shelly", "Puffer", "Alantic", "Artic", "Fin", "Alfonso", "Nessie"],
        "last": ["ReefStalker", "Waves", "Tentacles", "Meowerson", "Clawson", "Nemo"]
    },
    "Cat": {
        "heroic": ["Floof", "Lioness", "of the Jungle", "Chadwick", "the Meak"],
        "villainous": ["Mousey", "Panther", "Puma", "Quill", "Yellow Eyes"],
        "wwe": ["Huntress", "Floofy", "Abyssal", "Quick Claws", "Dark"],
        "first": ["Floof", "Iroh", "Maisha", "Chester", "Chesire", "Nibbles", "Creature"],
        "last": ["Flooferson", "SoftPaws", "Quickfoot", "Meowerson", "Clawson", "Bleepy"]
    },
    "Goose": {
        "heroic": ["Captain Honkman", "Defender", "Brave Waddles", "Gallant", "Hawkbeak"],
        "villainous": ["Honkerson", "Waddle", "Beakman", "Quill", "Darkwing"],
        "wwe": ["Winged Wrecker", "Honk Crusher", "Flapstorm", "Beak of Doom", "Feather Fury"],
        "first": ["Gustav", "Honk", "Flap", "Feather", "Quill", "Waddles"],
        "last": ["Pondstrider", "Beakman", "Gosling", "Featherstone", "Wingate", "Honkerson"]
    },
    "Wolf": {
        "heroic": ["Blaze", "Shadow", "Silverfang", "Ironclaw", "Valorhowl"],
        "villainous": ["Rogue Nightstalker", "Vile Fang", "Bloodmoon Howler", "Darkstrike", "Wolfbane"],
        "wwe": ["Howling Storm", "Fury Fang", "Unleashed", "Nightmare", "Iron Fang"],
        "first": ["Fang", "Lupin", "Howler", "Shadow", "Rogue", "Blizzard"],
        "last": ["Moonfang", "Stormpaw", "Snowfur", "Blackfang", "Greyhide", "Howlington"]
    },
    "Penguin": {
        "heroic": ["Waddlefoot", "Ice Glider", "Pebbles", "Feet", "Torpedo"],
        "villainous": ["Night Diver", "Seal Killer", "Ice Veins", "GenTooth", "Wild Style", "Stormbreaker"],
        "wwe": ["Sliding", "Happy", "Chilled", "Sleak", "Iron Beak", "Emporer"],
        "first": ["Pebbles", "Fin", "Tuxedo", "Macaroni", "Clumsey", "Blizzard"],
        "last": ["Waddlefoot", "Feet", "Snowfur", "Chinstrap", "Flippers", "Eggs"]
    },
    "Raccoon": {
        "heroic": ["Quickpaw", "Shadowmask", "Stealthy", "Bandit", "Scraps"],
        "villainous": ["King Trashpaw", "Nighthowler", "Grim Bandit", "Darkmask Sly", "The Wrecking"],
        "wwe": ["Danger", "Masked Marauder", "Scrap King", "Trash Titan", "Night Rook"],
        "first": ["Bandit", "Sly", "Tinker", "Scraps", "Zorro", "Rusty"],
        "last": ["Nightwhisker", "Trashpaw", "Maskwell", "Shadowtail", "Gutteridge", "Quickpaws"]
    },
    "Otter": {
        "heroic": ["Swiftcurrent", "Brave Paddler", "Splash Knight", "Stormtide", "Waterstrike"],
        "villainous": ["Mudwhisker", "Frostbite", "Corrupt Otter", "Wavestrike", "Shadowswimmer"],
        "wwe": ["Otter King", "Paddlebreaker", "Tidal Wave", "River Destroyer", "Wild Otter"],
        "first": ["River", "Splash", "Bubbles", "Nimble", "Marsh", "Scamper"],
        "last": ["Wavecrest", "Paddlemore", "Brooktail", "Finsley", "Oceansong", "Mudwhisker"]
    },
    "Fox": {
        "heroic": ["Blaze", "Sly", "Fireswift", "Emberstrike", "Quicktail"],
        "villainous": ["Vixenshadow", "Darkflame", "Sinister", "Scarredfang", "Nightfire"],
        "wwe": ["Fury", "Red Vixen", "Slyfire", "Beastly", "Wild"],
        "first": ["Vixen", "Rust", "Sly", "Blaze", "Amber", "Dash"],
        "last": ["Swiftpaw", "Redtail", "Cinderfang", "Sharpclaw", "Firewhisker", "Foxley"]
    },
    "Lynx": {
        "heroic": ["Silentstrike", "Icefang", "Stormclaw", "BlizzeRidge", "Snowhunter"],
        "villainous": ["Nightclaw", "Coldshadow", "Icewhisper", "Cinderstrike"],
        "wwe": ["Prowler", "Clawmaster", "Frostfang Fury", "Silent Strike", "Lynx King"],
        "first": ["Brindle", "Silent", "Ghost", "Rime", "Claw", "Tundra"],
        "last": ["Icefang", "Sharpclaw", "Snowstalker", "Whisperpaw", "Stonehide", "Nightroar"]
    },
    "Badger": {
        "heroic": ["Brutal Burrow", "Ironclaw", "Mighty Root", "Shadowfang", "Boulderback"],
        "villainous": ["Gravelstone", "Doomclaw", "Scalebreaker", "Darkfang", "Deepwood Menace"],
        "wwe": ["Brawler", "Grizzle", "Stonecrusher", "Diggs", "Rampager"],
        "first": ["Burrow", "Grizzle", "Diggs", "Root", "Brutus", "Tusk"],
        "last": ["Ironhide", "Deepclaw", "Hollowfang", "Dirtpaw", "Strongback", "Clawmaster"]
    },
    "Hawk": {
        "heroic": ["Stormwing", "Skystrike", "Falconeye", "Thunderbeak", "Aero Blaze"],
        "villainous": ["Viperwing", "Darkstorm", "Cindersky", "Vengeful Talon", "Hawkshade"],
        "wwe": ["Sky's Fury", "Talon", "Flying Beast", "Hawkstorm", "Sky Crusher"],
        "first": ["Talon", "Sky", "Wind", "Gale", "Aero", "Storm"],
        "last": ["Stormwing", "Windtalon", "Featherstrike", "Sharpbeak", "Cloudpiercer", "Sunwing"]
    },
    "Rabbit": {
        "heroic": ["Thumper", "Fleetfoot", "Swiftwhisker", "Hopper", "Velvetdash"],
        "villainous": ["Scarletfang", "Warren Fury", "Nibbles of Doom", "Shadowthump", "Grimhopper"],
        "wwe": ["Ravager", "Hops of Fury", "Thumper 'The Crusher'", "Quickfoot", "Velvet"],
        "first": ["Thumper", "Hopper", "Dash", "Clover", "Nibbles", "Velvet"],
        "last": ["Quickfoot", "Softpaw", "Meadowtail", "Fleetwhisker", "Warren", "Dandelion"]
    },
    "Turtle": {
        "heroic": ["Shellshock", "Tidewalker", "Braveshell", "Stonestride", "Slow Tide"],
        "villainous": ["Coralbreaker", "Venomspike", "Shellbane", "Deep Sea Tyrant", "Terror"],
        "wwe": ["Shellstorm", "Titan of the Deep", "The Wrath", "Sea Serpant", "Tidal"],
        "first": ["Shelly", "Tank", "Moss", "Tide", "Snap", "Drift"],
        "last": ["Stoneback", "Slowstream", "Lagoon", "Shellington", "Pebblepath", "Reefwalker"]
    },
    "Monster": {
        "heroic": ["Gryphon", "Dragon", "Devil Slayer", "Elemental", "Knight", "Druid"],
        "villainous": ["Sea Serpant", "Necromancer", "Summoner", "Terror"],
        "wwe": ["4-Eyed", "Winged", "Draconic", "Sea Serpant", "Fanatic", "Wooly", "Rage"],
        "first": ["Cyclops", "Mystical", "Invisible", "Royal", "Swamp", "Forsaken", "Flame"],
        "last": ["Centaur", "Chimera", "Devil", "Fairy", "Man", "Goliath", "Gorgon"]
    },
    "Human": {
        "heroic": ["Lil Guy", "Stepdad", "Friend of the Forest", "Lady of the Lake", "King of Man"],
        "villainous": ["Smelly", "Grumpz", "Skinny", "Slapstick", "Kyle", "Queen of Hearts", "Sanders", "Bossman"],
        "wwe": ["Trashman", "The Gov'na", "Southern Witch", "Smelly", "Clumsey", "Dr.", "Patron Saint", "The Horrible", "Forsaken",
                "Forgotten", "The Silent", "Drunk", "Colonial", "CEO", "Local", "Dude"],
        "first": ["Chris", "Martha", "Jim", "John", "David", "Keanu", "Sandra", "Ricky", "Brandon", "Maria", "Joey", "Mohammed",
                 "Jose", "Ahmed", "Ali", "Ashley", "Jarrett", "Ying", "Mikey", "Juan", "Robert", "Luis", "Lil'", "Drew", "Ryan", "Gavin", "Marcus",
                 "Izzy", "Em", "Heather", "Nick", "Cassidy", "April", "Swole"],
        "last": ["Reeves", "Smith", "Hill", "Rodriguez", "Miller", "Garcia", "Wang", "Johnson", "Williams", "Brown", "Torosian", "Tranel",
                 "of Rhodes", "King", "From Way Back"]
    },
    "Horror": {
        "heroic": ["Strider", "Fallen Angel", "Cthulu"],
        "villainous": ["Nightmare", "Soul Sucker", "Karen", "Terror"],
        "wwe": ["Soul Collector", "Winged", "Dead", "Nightmare", "Fanatic", "Eldritch"],
        "first": ["Cyclops", "Crawling", "Invisible", "Razertooth", "Forsaken"],
        "last": ["Clown", "Horror", "Devil", "Skin Stealer", "Killer", "Stalker"]
    },
}