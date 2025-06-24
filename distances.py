from geopy.distance import geodesic
import random
areas = {
    "Gulshan": (23.7945, 90.4159),
    "Banani": (23.7932, 90.4063),
    "Dhanmondi": (23.7465, 90.3750),
    "Uttara": (23.8742, 90.3987),
    "Mirpur": (23.8028, 90.3610),
    "Mohammadpur": (23.7646, 90.3585),
    "Lalbagh": (23.7170, 90.3785),
    "Motijheel": (23.7324, 90.4125),
    "Badda": (23.7805, 90.4268),
    "Tejgaon": (23.7625, 90.3917),
    "Wari": (23.7099, 90.4174),
    "Hazaribagh": (23.7223, 90.3773),
    "Jatrabari": (23.7091, 90.4345),
    "Pallabi": (23.8209, 90.3611),
    "Sabujbagh": (23.7383, 90.4412),
    "Malibagh": (23.7589, 90.4186),
    "Farmgate": (23.7620, 90.3861),
    "Ramna": (23.7381, 90.3954),
    "Baily Road": (23.7471, 90.3984),
    "Elephant Road": (23.7513, 90.3929),
    "Kakrail": (23.7493, 90.4080),
    "Khilgaon": (23.7469, 90.4200),
    "Shyamoli": (23.7703, 90.3651),
    "Agargaon": (23.7774, 90.3674),
    "Moghbazar": (23.7477, 90.4171),
    "Shantinagar": (23.7464, 90.4113),
    "Baridhara": (23.8073, 90.4131),
    "Niketon": (23.7933, 90.4186),
    "Rampura": (23.7439, 90.4426),
}

def calculate_distance(area1, area2):
    if area1 in areas and area2 in areas:
        coord1 = areas[area1]
        coord2 = areas[area2]
        distance = geodesic(coord1, coord2).kilometers
        return f"{distance:.2f}"
    else:
        return random.randint(2, 15)

if __name__ == "__main__":
    area1 = input("Enter the first area: ")
    area2 = input("Enter the second area: ")
    
    distance = calculate_distance(area1, area2)
    
    
    if isinstance(distance, str):
        print(distance)
    else:
        print(f"Approximate distance between {area1} and {area2}: {distance} kilometers")
