# Tree Root Model 

A model for estimating the necessary root volume of tree roots, now and in the future.


## About the Project
This project is an internship thesis for the Master Computational Science at the University of Amsterdam. It was created in the 3D Amsterdam team and the results are included in this 3D environment. 

The model needs at least some input about the tree, depending on which of the three methods a user wants to use (see Usage). The model also needs information about the BGT and AHN at the location of the input trees. If this is not known by the user, the model requests them via URL. Lastly, the model needs a mesh of Gemiddeld Hoogste Grondwaterstand (GHG, average highest groundwater level) measurements (see Usage). 

The main function in the model outputs NumPy arrays. With another script in the model, they can be converted to CityJSON files (TODO iets over cityjson). (TODO ook naar binary met de tilebaketool, deze tool denkik uit mn map halen).  

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
6) Validation TODO link: Contains the code used for the validation. This is only functioning as example since most validation data is not publicly available, like the road damage reports and ground radar scans, so it is impossible to rerun most code for other users. 

These are the most important scripts:

These are descriptions of the other scripts: 

---
## Installation 

---
## Usage

---

## How it Works

---
## License

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
* The tool for converting the CityJSON files to binary format is developed by the 3D Amsterdam team and available [here](https://github.com/Amsterdam/CityDataToBinaryModel). 
