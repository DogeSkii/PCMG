import numpy as np
import noise
import matplotlib.pyplot as plt
import svgwrite
from rich.progress import Progress, TextColumn, TimeRemainingColumn, BarColumn
from rich.console import Console
import random

console = Console()

# This line was added so i can test the new action, thanks


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
    offset_x = random.uniform(0, 10000)
    offset_y = random.uniform(0, 10000)
    
    with Progress(
        TextColumn("[bold]Generating Heightmap: "),
        BarColumn(bar_width=20),
        TimeRemainingColumn(True,True),
    ) as progress:
        task = progress.add_task("[cyan]Processing", total=height)
        
        for y in range(height):
            for x in range(width):
                height_map[x, y] = noise.pnoise2((x + offset_x) / scale, (y + offset_y) / scale,
                                                 octaves=DEFAULT_OCTAVES,
                                                 persistence=DEFAULT_PERSISTENCE,
                                                 lacunarity=DEFAULT_LACUNARITY)
            progress.update(task, advance=1)
    
    height_map = (height_map - np.min(height_map)) / (np.max(height_map) - np.min(height_map))
    return height_map

# === EXPORT TO SVG ===
def export_svg(height_map, filename, levels, line_thickness):
    dwg = svgwrite.Drawing(filename, size=(WIDTH, HEIGHT))
    contour_levels = np.linspace(0, 1, levels)
    fig, ax = plt.subplots()
    cs = ax.contour(height_map, levels=contour_levels)
    
    with Progress(
        TextColumn("[bold]Processing Contours: "),
        BarColumn(bar_width=20),
        TimeRemainingColumn(True,True),
    ) as progress:
        task = progress.add_task("[magenta]Processing", total=len(contour_levels) - 1)
        
        for level in range(len(contour_levels) - 1):
            contour_segments = cs.allsegs[level]
            for contour in contour_segments:
                contour_array = np.array(contour)
                scaled_path = [(x * (WIDTH / height_map.shape[1]), y * (HEIGHT / height_map.shape[0])) for x, y in contour_array]
                if len(scaled_path) > 1:
                    dwg.add(dwg.polyline(points=scaled_path, stroke="black", fill="none", stroke_width=line_thickness))
            progress.update(task, advance=1)
    
    dwg.save()
    plt.close(fig)
    console.print(f"✅ [bold green]SVG exported as {filename}")

# === PARAMETERS ===
scale = DEFAULT_SCALE + random.uniform(-10, 10)
contour_levels = 15
line_thickness = 2
output_filename = "contour_map.svg"

# === GENERATE AND EXPORT CONTOUR MAP ===
heightmap = generate_heightmap(WIDTH, HEIGHT, scale)
export_svg(heightmap, output_filename, contour_levels, line_thickness)
