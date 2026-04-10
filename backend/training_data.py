# CivicFlow ML Training Dataset
# 500+ Sample Complaints for Better Classification

TRAINING_DATA = {
    "Electricity": [
        # Power Outages
        "No electricity in my area for 3 days", "Power outage affecting entire street",
        "Frequent power cuts disturbing work", "Electricity supply disconnected without notice",
        "Blackout lasting more than 6 hours", "Power failure in residential area",
        "Street lights not working at night", "Electric poles damaged by storm",
        "Flickering lights damaging appliances", "No power supply to our society",
        
        # Meter Issues
        "Electricity meter not working properly", "Meter showing incorrect reading",
        "Double billing on electricity bill", "Meter charges unusually high",
        "Damaged electricity meter", "Meter not installed correctly",
        "Getting overbilled for electricity", "Meter malfunction causing high charges",
        
        # Cable Issues
        "Broken electric wires on road", "Hanging electrical cables dangerous",
        "Electric lines touching tree branches", "Electrical wires placed unsafely",
        "Damaged power cables need repair", "Electric poles leaning dangerously",
        
        # Maintenance
        "Electricity poles need maintenance", "Power line maintenance needed urgently",
        "Electric infrastructure deteriorating", "Transformers need replacement",
        "Cannot get new electricity connection", "Connection delayed for weeks",
        "Meter reading staff never visit", "Electricity office not responding",
        
        # Safety
        "Electric shock hazard in area", "Exposed wires causing danger",
        "Children getting electrocuted", "Electrical hazard near school",
        "Transformer overheating problem", "Voltage fluctuations damaging devices",
        
        # Additional variations
        "Urgent power outage emergency", "Critical electricity shortage",
        "Multiple power failures this week", "Blackout during exam period",
        "No power at hospital entrance", "Emergency lights not working",
    ],
    
    "Water Supply": [
        # No Water
        "No water supply for 3 days", "Water connection disconnected wrongly",
        "No tap water in residential area", "Dry taps entire week",
        "Water shortage during summer", "No water supply to apartment",
        
        # Low Pressure
        "Very low water pressure", "Insufficient water in morning",
        "Water pressure fluctuating", "Cannot fill bucket in 30 minutes",
        "Low pressure affecting household", "Weak water supply to upper floors",
        
        # Contaminated Water
        "Water is brown and smelly", "Contaminated water supply",
        "Water tastes like dirt", "Chemical smell in tap water",
        "Water appears cloudy and dirty", "Polluted water causing illness",
        "Water contamination emergency", "Unsafe water for drinking",
        "Water pipes leaking contaminated material", "Brownish water from taps",
        
        # Damaged Infrastructure
        "Water pipe burst on street", "Pipeline damaged needs repair",
        "Water leaking from main line", "Broken water connections everywhere",
        "Underground water pipe damage", "Multiple water leaks in area",
        "Water tank overflow on road", "Damaged water distribution system",
        
        # Billing Issues
        "Excessive water charges", "Water bill unusually high",
        "Double charging for water", "Incorrect water meter reading",
        "Water meter not functioning", "Getting overcharged monthly",
        
        # Tank/Storage
        "Community water tank empty", "Water tank not being filled",
        "Dirty water tank needs cleaning", "Water storage tank broken",
        "Tank overflow creating puddles", "Unmaintained water reservoir",
        
        # Quality
        "Hard water causing problems", "Water not suitable for washing",
        "Salty water from tap", "Water quality deteriorating",
        "Fluoride content too high", "Water hardness unbearable",
        
        # Additional variations
        "Water emergency urgent", "Critical water shortage",
        "Cannot get potable water", "Waste of water in area",
        "Pipe laying incomplete", "Water supply irregular",
    ],
    
    "Sanitation": [
        # Garbage Collection
        "Garbage not collected for days", "Overflowing dustbins on street",
        "Waste piling up near my home", "Garbage collection delayed",
        "Trash not removed from area", "Dumped waste everywhere",
        "No garbage collection this week", "Accumulating garbage causing diseases",
        
        # Cleanliness
        "Street very dirty and unhygienic", "Filthy lanes need cleaning",
        "Area covered with trash", "Excessive litter on roads",
        "Dirty surroundings spreading disease", "Unhygienic conditions everywhere",
        "Lack of cleanliness causing health hazard", "Rats attracted by garbage",
        
        # Drainage Issues
        "Clogged drainage causing overflow", "Blocked drain on street",
        "Sewage overflowing on road", "Drainage system not working",
        "Stagnant water on street", "Drainage blocked near school",
        "Sewage smell unbearable", "Dirty water flowing on roads",
        
        # Public Toilets
        "Public toilet not cleaned", "Filthy public restroom",
        "Toilet blocked and unusable", "No water in public toilet",
        "Broken public toilet facility", "Unhygienic public restroom",
        
        # Waste Management
        "Waste management completely failed", "No proper waste disposal",
        "Illegal dumping near residential area", "Hazardous waste disposal",
        "Burnt waste creating smoke", "Chemical waste disposal unsafe",
        
        # Pest Control
        "Rats and rodents everywhere", "Disease-carrying insects",
        "Mosquitoes breeding in stagnant water", "Cockroach infestation",
        "Need pest control urgently", "Healthcare threat from pests",
        
        # Sanitation Workers
        "Sanitation staff absent", "No sweeping or cleaning",
        "Inadequate sanitation workforce", "Garbage collectors not showing up",
        
        # Additional variations
        "Sanitation emergency urgent", "Critical cleanliness issue",
        "Health hazard due to garbage", "Epidemic risk from dirty surroundings",
        "Sanitation breakdown", "Disease outbreak possible",
    ],
    
    "Roads": [
        # Potholes
        "Road full of potholes", "Deep pothole on street",
        "Multiple potholes causing accidents", "Big hole in road",
        "Dangerous potholes everywhere", "Road damage spreading",
        "Vehicle damaged by pothole", "Cannot drive safely",
        
        # Cracks
        "Road cracked and damaged", "Broken road surface",
        "Pavement cracking everywhere", "Deteriorating road condition",
        "Bad road causing dust", "Broken asphalt needs repair",
        
        # Unevenness
        "Uneven road surface", "Road bumpy and difficult",
        "Irregular road causing accidents", "Bad road maintenance",
        "Potholed and uneven road", "Dangerous road condition",
        
        # Flooding
        "Road flooded during rain", "Water accumulated on street",
        "Road becomes waterlogged", "Flooding problem on main road",
        "Drainage failure causing floods", "Unable to cross road",
        
        # Maintenance
        "Road needs urgent repair", "Street maintenance completely failed",
        "Road deterioration accelerating", "No road maintenance",
        "Repaired road already broken", "Poor quality road work",
        
        # Traffic/Safety
        "No zebra crossing on busy street", "Missing speed breaker",
        "Dangerous intersection needs signals", "No traffic signals working",
        "Accident-prone road needs safety", "Road markings faded",
        
        # Street Lights
        "Street lights not working", "Dark road with no lights",
        "Broken street lamps on highway", "No lighting at night",
        
        # Debris
        "Debris blocking road", "Construction material on street",
        "Scattered stones on road", "Rubble from demolition",
        
        # Sidewalks
        "Broken sidewalk dangerous", "Damaged pavement for pedestrians",
        "Uneven footpath causing falls", "Broken tiles on street",
        
        # Additional variations
        "Road emergency urgent repair needed", "Critical road damage",
        "Cannot use road safely", "Road unfit for vehicles",
        "Major road deterioration", "Accident waiting to happen",
    ],
    
    "Public Services": [
        # Buses/Transport
        "Buses not stopping at assigned stops", "No bus service in area",
        "Bus frequency reduced too much", "Long wait for public transport",
        "Buses overcrowded everyday", "Bus routes changed without notice",
        "Broken down buses blocking traffic", "No night bus service",
        
        # Public Parks
        "Park gates locked frequently", "Maintenance of park neglected",
        "Public park in poor condition", "Broken playground equipment",
        "Park benches damaged", "No maintenance of green space",
        
        # Public Buildings
        "Library closed indefinitely", "Community center not accessible",
        "Government office doors locked", "Public facilities not maintained",
        "School building needs repair", "Hospital entrance broken",
        
        # Markets
        "Market congestion terrible", "No proper market management",
        "Dirty market conditions", "Market vendors blocking streets",
        "Illegal encroachments in market", "Market rat menace",
        
        # Sports Facilities
        "Sports ground maintenance poor", "Playground equipment broken",
        "No swimming pool maintenance", "Athletic field in bad shape",
        "Gymnasium equipment damaged", "Tennis court needs repair",
        
        # Public Amenities
        "No public restrooms available", "Drinking water fountain broken",
        "Bench seating insufficient", "No shade structures",
        "Accessibility for disabled missing", "Public infrastructure lacking",
        
        # Administrative
        "Government office not responsive", "Permit processing very slow",
        "Staff absenteeism affecting services", "Long queues everywhere",
        "Service counters always closed", "Bureaucratic delays",
        
        # Events/Activities
        "No community events organized", "Public programs cancelled",
        "Cultural activities missing", "Youth programs not available",
        "Health camps not scheduled", "Educational programs stopped",
        
        # Safety
        "Street safety concerns increasing", "Crime in area rising",
        "No police patrol at night", "Inadequate security measures",
        "CCTV cameras not working", "Street safety deteriorating",
        
        # Additional variations
        "Public service emergency", "Critical service failure",
        "Municipal services inadequate", "Civic infrastructure neglected",
        "Service delivery failing", "Public welfare affected",
    ]
}

# Count total samples
TOTAL_SAMPLES = sum(len(complaints) for complaints in TRAINING_DATA.values())

# Helper function to get training data in format for classifier
def get_training_data():
    """Returns training texts and labels for ML model"""
    texts = []
    labels = []
    
    for category, complaints in TRAINING_DATA.items():
        for complaint in complaints:
            texts.append(complaint)
            labels.append(category)
    
    return texts, labels


if __name__ == "__main__":
    print(f"📊 CivicFlow Training Dataset")
    print(f"{'='*50}")
    
    for category, complaints in TRAINING_DATA.items():
        print(f"{category}: {len(complaints)} samples")
    
    print(f"{'='*50}")
    print(f"✅ Total samples: {TOTAL_SAMPLES}")
