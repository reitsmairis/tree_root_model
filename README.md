# Tree Root Model 

A model for estimating the necessary root volume for tree roots, now and in the future.


## About the Project
This project is an internship thesis for the Master Computational Science at the University of Amsterdam. It was created in the [3D Amsterdam](https://3d.amsterdam.nl/) team and the results are included in this 3D environment. 

The model needs at least some input about the tree, depending on which of the three methods a user wants to use (see Usage). The model also needs information about the BGT and AHN at the location of the input trees. If this is not known by the user, the model requests them via URL. Lastly, the model needs a mesh of Gemiddeld Hoogste Grondwaterstand (GHG, average highest groundwater level) measurements (see Usage). 

The main function in the model outputs NumPy arrays. With another script in the model, they can be converted to [CityJSON](https://www.cityjson.org/) files. For including the root volume cylinders in 3D Amsterdam, they had to be converted to binary format using the [Tile Bake Tool](https://github.com/Amsterdam/CityDataToBinaryModel) developed by the 3D Amsterdam team. 

### Built with
* [Pandas](https://pandas.pydata.org/docs/index.html)
* [NumPy](https://numpy.org/)
* [Math](https://docs.python.org/3/library/math.html#module-math)
* [Os](https://docs.python.org/3/library/os.html#module-os)
* [Json](https://docs.python.org/3/library/json.html#module-json)
* [Vedo](https://vedo.embl.es/)
* [Urllib](https://docs.python.org/3/library/urllib.html#module-urllib)
* [Copy](https://docs.python.org/3/library/copy.html)
* [Matplotlib](https://matplotlib.org/) 
* [Rijksdriehoek](https://pypi.org/project/rijksdriehoek/) 
* [PyShp](https://pypi.org/project/pyshp/)
* [BS4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

---
## Project Structure 
There are the following folders in the structure:
1) [`data`](./data): Contains files with the tree information that was used in the project, the root volume numbers from Boommonitor, and the growth equations from the Urban Tree Database. 
2) [`grondwater`](./grondwater): Contains the groundwater data CSVs from Waternet for the subregions used in this project (downloaded in March 2022), some NumPy and Dataframe files containing GHG values of the subregions (from January-May 2022), and the mesh of GHG values for Amsterdam (one with holes and one filled, created in May 2022). 
3) [`output`](./output): Contains the CityJSON files for the different subregions, methods and years, and the numpy files for the subregions and the whole city. 
4) [`output_bin`](./output_bin): Contains the binary and gltf tiles of subregion het Wallengebied. 
5) [`plots`](./plots): Contains the figures resulting from the validation and that are included in the report. 
6) [`validation`](./validation): Contains the code used for the validation. This is only functioning as example since most validation data is not publicly available, like the road damage reports and ground radar scans, so it is impossible to rerun most code for other users. 

These are the most important scripts for using the model:
1) [`main_code.py`](./main_code.py): For running the model, takes the input parameters and estimates the corresponding necessary root volume in NumPy arrays. 
2) [`data_to_cityjson.py`](./data_to_cityjson.py): For converting the NumPy arrays to CityJSON geometry.
3) [`GHG_calculator.py`](./GHG_calculator.py): For calculating the GHG values from the Waternet groundwater measurement CSVs. 
4) [`interpolation.py`](./interpolation.py): For interpolating the GHG values to a mesh. 

The other scripts and files are: 
1) [`ahn_reader.py`](./ahn_reader.py): For making URL requests for the AHN and RIVM data, which determine the tree height when unknown and the ground level height. 
2) [`bgt_reader.py`](./bgt_reader.py): For making URL requests to the BGT values. It also contains code for classifying the returned BGT value as a corresponding soil profile type. 
3) [`boommonitor_calc.py`](./boommonitor_calc.py`): Calculates the initial root volume numbers and growth per year numbers using the boommonitor info in the data folder. 
4) [`city_to_binary.py`](./city_to_binary.py): For converting the CityJSON files to binary. This needs the [Tile Bake Tool](https://github.com/Amsterdam/CityDataToBinaryModel) developed by the 3D Amsterdam team. 
5) [`cityjson_converter.py`](./cityjson_converter.py): Contains the functionality for converting the NumPy arrays to CityJSONs.
6) [`method_static.py`](./method_static.py), [`method_treedict.py`](./method_treedict.py), and [`method_treegrowth.py`](./method_treegrowth.py): Contain the code for respectively the static, tree dictionary and tree growth methods. 
7) [`rootvolume.py`](./rootvolume.py): For classifying height and crown sizes and determining the root volume. 
8) [`select_climate.py`](./select_climate.py): For selecting a climate region in the tree growth equation database in the data folder. The project used the Pacific Northwest. 
9) [`select_trees.py`](./select_trees.py): Used to select trees for the different subregions out of the total Amsterdam tree data. Can probably be done faster using for example [QGIS](https://qgis.org/nl/site/) if the user knows to use that. 
10) [`timedependency.py`](./timedependency.py): contains the allometric growth equations and functions that use them for predictions about the height and crown size of the trees. 
11) [`treedict.py`](./treedict.py): contains the tree dictionary used in the tree dictionary method, as well as a list of fast growing tree genera. 
12) [`root_config.json`](./root_config.json): Configuration file that was created for using the [Tile Bake Tool](https://github.com/Amsterdam/CityDataToBinaryModel).

---
## Installation 
1) Make sure to have Python version 3.5.8 installed on your machine. This project used [Anaconda](https://www.anaconda.com/), which comes with Python and a lot of nice libraries, as well as a nice terminal.

2) Clone this repository using the terminal:
    ```bash
    git clone https://github.com/reitsmairis/tree_root_model
    ```
3) Install the dependencies listed above (TODO requirements.txt ofzo)
---
## Usage
### Necessary input
* Static method: 
    * Height
    * Crown diameter  
    * Species (optional, assume regular growing tree if unknown)
* Tree dictionary method:
    *  Species
    *  Tree dictionary
*  Tree growth method:
    * Species
    * Growth equations from the Urban Tree Database
* For alle three methods:
    * Year of plantation
    * Groundwater (GHG) value
    * Tree type (optional, assume regular tree if unknown)
    * BGT value (optional, can be requested via URL if unknown)
    * AHN value (optional, can be requested via URL if unknown)

TODO example csv input

TODO Grondwater meer uitleggen

### TODO example how to run main

### TODO output numpy files uitleggen

### TODO uitleggen hoe naar cityjson / binary gaan

---

## How it Works
TODO pipeline images

TODO linkje naar thesis

---
## License
TODO 

---


## Contact

Iris Reitsma - reitsmairis@gmail.com 

LinkedIn: https://www.linkedin.com/in/iris-reitsma-269209139/ 

Project link: https://github.com/reitsmairis/tree_root_model 

---

## Acknowledgements 

#### Model input data: 
* The files in data/boommonitor_data contain root volume numbers from the calculation tool [Boommonitor](https://www.norminstituutbomen.nl/instrumenten/boommonitor/) from Norminstituut Bomen. These numbers can be accessed with a license. These guideline numbers are used to estimate the root volume for a tree with specific input parameters. 
* The file data/Cobra.data.csv contains the crown areas and diameters and other information about trees in three subregions of Amsterdam (Wallengebied, Sarphatipark, IJburg). This data is delivered by [Cobra Groeninzicht](https://www.cobra-groeninzicht.nl/). The data was used as input for the static method and to validate the crown predictions of the tree dictionary method. 
* The other tree data is from the city of Amsterdam and publicly available [here](https://maps.amsterdam.nl/open_geodata/). 
* The growth equation information in data/RDS-2016-0005 is from the [Urban Tree Database](https://www.fs.usda.gov/rds/archive/Catalog/RDS-2016-0005) and was made available by the [Forest Service U.S. Department of Agriculture](https://www.fs.usda.gov/treesearch/pubs/52933).
* The groundwater level measurements are done by Waternet and can be downloaded [here](https://maps.waternet.nl/kaarten/peilbuizen.html). 

#### Validation data: 
* [Terra Nostra](https://www.terranostra.nu/nl) delivered the ground radar data and the report of their investigation. 
* The department of municipal management ('afdeling stedelijk beheer') of the city of Amsterdam provided road inspection data ('inspectiegegevens') concerning root lifting. 
* The citizen reports about root lifting were made available by the [Signalen Informatievoorziening Amsterdam](https://openresearch.amsterdam/nl/page/39785/de-signalen-informatievoorziening-amsterdam-sia). 

#### Other: 
* The tool for converting the CityJSON files to binary format (Tile Bake Tool) is developed by the 3D Amsterdam team and available [here](https://github.com/Amsterdam/CityDataToBinaryModel). 
