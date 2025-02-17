
# Procedural Contour Map Generator

This project generates a procedural contour map based on Perlin noise and exports the result as an SVG file. The map can be customized with different noise scales, contour levels, and line thicknesses.

## Features
- Generate a heightmap using Perlin noise.
- Create contour lines based on the heightmap.
- Export the contour map as an SVG file.
- Use a simple progress bar to track the process.

## Installation

To get started, you'll need to install the required Python dependencies. You can do this by creating a `virtualenv` and installing the packages from the `requirements.txt` file.

1. Clone this repository:
   ```bash
   git clone <repository_url>
   cd <repository_name>
   ```

2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Once the dependencies are installed, you can generate the contour map by running the Python script.

```bash
python contour_map_generator.py
```

This will generate a heightmap using Perlin noise and create contour lines at different levels. The contour map will be exported as an SVG file.

### Script Configuration
You can modify the following variables to customize the output:
- **`WIDTH`** and **`HEIGHT`**: Set the dimensions of the generated map (default: `1024x1024`).
- **`DEFAULT_SCALE`**: Controls the zoom level of the Perlin noise (default: `150.0`).
- **`DEFAULT_OCTAVES`**: Controls the detail of the noise (default: `4`).
- **`DEFAULT_CONTOUR_LEVELS`**: Number of contour levels to generate (default: `15`).
- **`DEFAULT_LINE_THICKNESS`**: Thickness of the contour lines (default: `2`).
- **`output_filename`**: The name of the output SVG file (default: `contour_map.svg`).

## Example Output

After running the script, an SVG file (`contour_map.svg`) will be generated, containing contour lines that represent the heightmap.

## License


