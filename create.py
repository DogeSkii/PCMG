import numpy as np
import noise
import matplotlib.pyplot as plt
import svgwrite
from rich.progress import Progress, TextColumn, TimeRemainingColumn, BarColumn
from rich.console import Console
import random

console = Console()

def get_config():
    default_config = {
        'WIDTH': 1024,
        'HEIGHT': 1024,
        'SCALE': 150.0,
        'OCTAVES': 4,
        'PERSISTENCE': 0.5,
        'LACUNARITY': 2.0,
        'CONTOUR_LEVELS': 15,
        'LINE_THICKNESS': 2,
        'OUTPUT_FILENAME': "contour_map.svg"
    }
    use_default = console.input("[bold]Would you like to use the default configuration values? (y/n): [/bold]").strip().lower()
    if use_default.startswith('y'):
        return default_config
    else:
        try:
            WIDTH = int(console.input("[bold]Enter image width (default 1024): [/bold]") or 1024)
            HEIGHT = int(console.input("[bold]Enter image height (default 1024): [/bold]") or 1024)
            SCALE = float(console.input("[bold]Enter noise scale (default 150.0): [/bold]") or 150.0)
            OCTAVES = int(console.input("[bold]Enter noise octaves (default 4): [/bold]") or 4)
            PERSISTENCE = float(console.input("[bold]Enter noise persistence (default 0.5): [/bold]") or 0.5)
            LACUNARITY = float(console.input("[bold]Enter noise lacunarity (default 2.0): [/bold]") or 2.0)
            CONTOUR_LEVELS = int(console.input("[bold]Enter number of contour levels (default 15): [/bold]") or 15)
            LINE_THICKNESS = int(console.input("[bold]Enter line thickness (default 2): [/bold]") or 2)
            OUTPUT_FILENAME = console.input("[bold]Enter output SVG filename (default 'contour_map.svg'): [/bold]") or "contour_map.svg"
        except Exception as e:
            console.print(f"[bold red]Error in input, using default values. Error: {e}[/bold red]")
            return default_config

        return {
            'WIDTH': WIDTH,
            'HEIGHT': HEIGHT,
            'SCALE': SCALE,
            'OCTAVES': OCTAVES,
            'PERSISTENCE': PERSISTENCE,
            'LACUNARITY': LACUNARITY,
            'CONTOUR_LEVELS': CONTOUR_LEVELS,
            'LINE_THICKNESS': LINE_THICKNESS,
            'OUTPUT_FILENAME': OUTPUT_FILENAME
        }

# Retrieve configuration from user input
config = get_config()

# Update global configuration values
WIDTH = config['WIDTH']
HEIGHT = config['HEIGHT']
DEFAULT_SCALE = config['SCALE']
DEFAULT_OCTAVES = config['OCTAVES']
DEFAULT_PERSISTENCE = config['PERSISTENCE']
DEFAULT_LACUNARITY = config['LACUNARITY']

# === GENERATE HEIGHTMAP ===
def generate_heightmap(width, height, scale):
    height_map = np.zeros((width, height))
    offset_x = random.uniform(0, 10000)
    offset_y = random.uniform(0, 10000)
    
    with Progress(
        TextColumn("[bold]Generating Heightmap: [/bold]"),
        BarColumn(bar_width=20),
        TimeRemainingColumn(True, True),
    ) as progress:
        task = progress.add_task("[cyan]Processing", total=height)
        
        for y in range(height):
            for x in range(width):
                height_map[x, y] = noise.pnoise2(
                    (x + offset_x) / scale,
                    (y + offset_y) / scale,
                    octaves=DEFAULT_OCTAVES,
                    persistence=DEFAULT_PERSISTENCE,
                    lacunarity=DEFAULT_LACUNARITY
                )
            progress.update(task, advance=1)
    
    # Normalize the height map
    height_map = (height_map - np.min(height_map)) / (np.max(height_map) - np.min(height_map))
    return height_map

# === EXPORT TO SVG ===
def export_svg(height_map, filename, levels, line_thickness):
    dwg = svgwrite.Drawing(filename, size=(WIDTH, HEIGHT))
    contour_levels = np.linspace(0, 1, levels)
    fig, ax = plt.subplots()
    cs = ax.contour(height_map, levels=contour_levels)
    
    with Progress(
        TextColumn("[bold]Processing Contours: [/bold]"),
        BarColumn(bar_width=20),
        TimeRemainingColumn(True, True),
    ) as progress:
        task = progress.add_task("[magenta]Processing", total=len(contour_levels) - 1)
        
        for level in range(len(contour_levels) - 1):
            contour_segments = cs.allsegs[level]
            for contour in contour_segments:
                contour_array = np.array(contour)
                scaled_path = [
                    (x * (WIDTH / height_map.shape[1]), y * (HEIGHT / height_map.shape[0]))
                    for x, y in contour_array
                ]
                if len(scaled_path) > 1:
                    dwg.add(dwg.polyline(points=scaled_path, stroke="black", fill="none", stroke_width=line_thickness))
            progress.update(task, advance=1)
    
    dwg.save()
    plt.close(fig)
    console.print(f"[bold green]✅ SVG exported as {filename}[/bold green]")

# === PARAMETERS ===
# Add a slight random variation to the scale
scale = DEFAULT_SCALE + random.uniform(-10, 10)
contour_levels = config['CONTOUR_LEVELS']
line_thickness = config['LINE_THICKNESS']
output_filename = config['OUTPUT_FILENAME']

# === GENERATE AND EXPORT CONTOUR MAP ===
heightmap = generate_heightmap(WIDTH, HEIGHT, scale)
export_svg(heightmap, output_filename, contour_levels, line_thickness)
