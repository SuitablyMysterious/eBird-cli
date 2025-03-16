import argparse
import requests

# Function to fetch the top bird species within a radius
def get_top_birds(api_key, latitude, longitude, radius, top_n):
    url = f"https://api.ebird.org/v2/data/obs/geo/recent"
    
    # Set up the request headers with the API key
    headers = {
        "X-eBirdApiToken": api_key
    }

    # Parameters for the API call
    params = {
        "lat": latitude,
        "lng": longitude,
        "maxDistance": radius,  # radius in miles
        "numResults": top_n,    # top N birds
    }

    # Send GET request to eBird API
    response = requests.get(url, headers=headers, params=params)

    # Check if the response was successful
    if response.status_code == 200:
        data = response.json()
        
        # Create a dictionary to store bird species and their counts
        bird_counts = {}
        
        for sighting in data:
            species = sighting['speciesCode']
            bird_counts[species] = bird_counts.get(species, 0) + 1

        # Sort by the count in descending order and take the top N
        sorted_birds = sorted(bird_counts.items(), key=lambda x: x[1], reverse=True)[:top_n]
        
        # Format the list for BirdNET Analyzer
        bird_list = [species for species, _ in sorted_birds]
        return bird_list
    else:
        print(f"Error: {response.status_code}")
        return []

# Main function to handle command-line arguments
def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Get top bird species from eBird API within a specified radius.")
    parser.add_argument("api_key", help="Your eBird API key.")
    parser.add_argument("latitude", type=float, help="Latitude of the location (e.g., 40.7128).")
    parser.add_argument("longitude", type=float, help="Longitude of the location (e.g., -74.0060).")
    parser.add_argument("radius", type=int, help="Radius to search within (in miles).")
    parser.add_argument("top_n", type=int, help="Number of top bird species to fetch.")
    
    args = parser.parse_args()

    # Call the function with the arguments from the command line
    top_birds = get_top_birds(args.api_key, args.latitude, args.longitude, args.radius, args.top_n)
    
    # Output the results
    print("Top Birds for BirdNET Analyzer:")
    for bird in top_birds:
        print(bird)

if __name__ == "__main__":
    main()
