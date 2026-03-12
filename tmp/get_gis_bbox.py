import json
import os

def get_bbox(geojson_path):
    min_x, min_y = float('inf'), float('inf')
    max_x, max_y = float('-inf'), float('-inf')
    
    if not os.path.exists(geojson_path):
        print(f"Warning: {geojson_path} not found.")
        return None

    with open(geojson_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    for feature in data.get('features', []):
        geometry = feature.get('geometry')
        if not geometry:
            continue
            
        coords = geometry.get('coordinates')
        
        # Flatten coordinates regardless of geometry type (Point, LineString, MultiLineString, etc.)
        def extract_coords(c):
            nonlocal min_x, min_y, max_x, max_y
            if isinstance(c[0], (int, float)):
                x, y = c[0], c[1]
                min_x = min(min_x, x)
                max_x = max(max_x, x)
                min_y = min(min_y, y)
                max_y = max(max_y, y)
            else:
                for sub in c:
                    extract_coords(sub)
        
        if coords:
            extract_coords(coords)
            
    return (min_x, min_y, max_x, max_y)

def main():
    base_path = r'c:\Desarrollo\Aquatica\LouroApp\frontend_pwa\public\data'
    files = ['principales.geojson', 'secundarios.geojson']
    
    global_min_x, global_min_y = float('inf'), float('inf')
    global_max_x, global_max_y = float('-inf'), float('-inf')
    
    for f in files:
        path = os.path.join(base_path, f)
        bbox = get_bbox(path)
        if bbox:
            global_min_x = min(global_min_x, bbox[0])
            global_min_y = min(global_min_y, bbox[1])
            global_max_x = max(global_max_x, bbox[2])
            global_max_y = max(global_max_y, bbox[3])
            
    if global_min_x == float('inf'):
        print("No coordinates found.")
        return

    print("--- UTM BBox (EPSG:25829) ---")
    print(f"Min X: {global_min_x}")
    print(f"Min Y: {global_min_y}")
    print(f"Max X: {global_max_x}")
    print(f"Max Y: {global_max_y}")
    
    # Simple conversion to WGS84 (Lat/Lon) using Proj4 logic if available or just output UTM for the user to convert
    # Since I don't know if pyproj is installed, I will provide the UTM values and the Overpass query template.
    
    print("\nPara usar en Overpass Turbo, necesitas convertir estos límites a Lat/Long.")
    print("Puedes usar https://epsg.io/transform#s_srs=25829&t_srs=4326")
    print(f"Punto 1 (MinX, MinY): {global_min_x}, {global_min_y}")
    print(f"Punto 2 (MaxX, MaxY): {global_max_x}, {global_max_y}")

if __name__ == "__main__":
    main()
