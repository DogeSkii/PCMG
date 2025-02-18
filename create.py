import numpy as np
import noise
import matplotlib.pyplot as plt
import svgwrite
from tqdm import tqdm  # Importing tqdm for progress bar
import random  # Import random for generating offsets

# === CONFIGURATION ===
WIDTH = 1024  # Image width
HEIGHT = 1024  # Image height
DEFAULT_SCALE = 150.0  # Controls zoom level of noise
DEFAULT_OCTAVES = 4  # Controls terrain detail
DEFAULT_PERSISTENCE = 0.5
DEFAULT_LACUNARITY = 2.0
DEFAULT_CONTOUR_LEVELS = 15  # Number of contour lines
DEFAULT_LINE_THICKNESS = 2  # Slightly thicker line thickness for contours


# === GENERATE HEIGHTMAP ===
def generate_heightmap(width, height, scale):
    height_map = np.zeros((width, height))
    
    # Introduce random offsets for x and y to ensure different maps each run
    offset_x = random.uniform(0, 10000)
    offset_y = random.uniform(0, 10000)
    
    for y in tqdm(range(height), desc="Generating heightmap", unit="row"):  # Add progress bar for heightmap generation
        for x in range(width):
            height_map[x, y] = noise.pnoise2((x + offset_x) / scale, (y + offset_y) / scale,
                                             octaves=DEFAULT_OCTAVES,
                                             persistence=DEFAULT_PERSISTENCE,
                                             lacunarity=DEFAULT_LACUNARITY)
    
    # Normalize to 0-1 range
    height_map = (height_map - np.min(height_map)) / (np.max(height_map) - np.min(height_map))
    return height_map


# === EXPORT TO SVG ===
def export_svg(height_map, filename, levels, line_thickness):
    """Exports contour lines from heightmap to an SVG file"""
    dwg = svgwrite.Drawing(filename, size=(WIDTH, HEIGHT))
    contour_levels = np.linspace(0, 1, levels)

    # Create a figure and axes
    fig, ax = plt.subplots()

    # Generate contours using matplotlib
    cs = ax.contour(height_map, levels=contour_levels)

    # Extract the contour paths using allsegs with progress bar
    for level in tqdm(range(len(contour_levels) - 1), desc="Processing contours", unit="level"):
        contour_segments = cs.allsegs[level]
        for contour in contour_segments:
            # Convert contour to a numpy array
            contour_array = np.array(contour)

            # Scale coordinates to fit SVG size
            scaled_path = [(x * (WIDTH / height_map.shape[1]), y * (HEIGHT / height_map.shape[0])) for x, y in contour_array]

            # Only add the path if it contains more than one point
            if len(scaled_path) > 1:
                dwg.add(dwg.polyline(points=scaled_path, stroke="black", fill="none", stroke_width=line_thickness))

    dwg.save()
    plt.close(fig)  # Close the matplotlib figure
    print(f"✅ SVG exported as {filename}")


# === PARAMETERS ===
scale = DEFAULT_SCALE + random.uniform(-10, 10)  # Introduce slight variation in scale
contour_levels = 15  # Number of contour levels
line_thickness = 2  # Slightly thicker line thickness for contours
output_filename = "contour_map.svg"  # Output file name

# === GENERATE AND EXPORT CONTOUR MAP ===
heightmap = generate_heightmap(WIDTH, HEIGHT, scale)
export_svg(heightmap, output_filename, contour_levels, line_thickness)
