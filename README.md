# Fire simulation using Blender

This repository contains the code and resources for generating smoke and fire simulation on set of background images.

## Project Structure

The project structure is organized as follows:
- `config.py`: This file contains configeration for setting up fire and smoke at random position with random configerations in background image. 
- `generate_fire.py`: This file used for generating and rendering smoke and fire.
- `synthetic_fire_data/`: Directory to store generated images.
- `blender_fire.ipynb` : Notebook to run on colab.
- `background/`: This contains background images.
- `README.md`: This file, providing an overview of the project.

## Installation and Run
# Run on Colab
   ```shell
   git clone https://github.com/piyush4141/blender_fire_simulation.git
   upload blender_fire_simulation to google-drive 
   open and run blender_fire.ipynb
   ```
# Local run:
  1. Clone repo
  ```shell
  git clone https://github.com/piyush4141/blender_fire_simulation.git
  cd blender_fire_simulation
  conda create --name firepy3 python=3.10
  conda activate firepy3
  pip install -r requirements.txt
  ```
  2. Download blender from "https://download.blender.org/release/Blender3.6"
  3. export BLENDER="/PATH/TO/blender/blender"
  4. BLENDER -noaudio --background -P generate_fire.py -b

## Next Steps:
  1. Use Hdr images in background for more realistic effects.
     
