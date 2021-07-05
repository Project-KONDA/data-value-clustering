# Data Value Clustering

This tool is a proof-of-concept implementation of a bottom-up approach to detecting quality problems in data
models that manifest in heterogeneous data values.
It supports an explorative analysis of the existing data and can be configured by domain experts according to their domain knowledge.
All values of a selected data field are clustered by syntactic similarity.
Thereby an overview of the data values' diversity in syntax is provided.
It shall help domain experts to understand how the data model is used in practice and to derive potential quality problems of the data model.

<!---
The approach is described in detail in the research paper "[Detecting Quality Problems in Data Models by
Clustering Heterogeneous Data Values](################)".
[//]: # (doi), published in the [proceedings](doi) of the conference "[MODELS2021](https://conf.researchr.org/home/models-2021)".
-->

![Component Diagram](readme_images/components_small.png)


This diagram gives an overview of the components and their interfaces.
The core of the tool is the Clustering-based Analyser.
It realises the workflow and controlls the data flows between the other components.
It is realized via the class ```Main``` (```DataValueClustering\gui_center\main.py```).

The Extraction component is extracts a list of data values from the database.
It is not yet implemented.

Multiple GUI components are provided to enable the configuration of the data value clustering based on domain knowledge and present the clustering results.
The GUI is still under development.

The Data Value Clustering component allows performing 3-step data value clustering via an API.
It starts with the abstraction of the original data values. Thereby irrelevant syntactical features that, according to the configuration by domain experts, are irrelevant for clustering are removed.
Next, pairwise distances (i.e. dissimilarities) between the abstracted data values are calculated based on the configuration of the distance function.
Finally, the abstracted data values are clustered via the chosen and configured clustering algorithm.

The Export component allows saving the parameters and the resulting clustering in a JSON file.
Further it creates a representation of the clustering as an Excel file.


## Built With

* [PyCharm 2021.1](https://www.jetbrains.com/pycharm/download/)
* [Python 3.8](https://www.python.org/downloads/release/python-380/)

<!---
This project was implemented using the PyCharm IDE. However it is possible to execute the implementation via any Python interpreter.
-->

## Installation

Required Python packages:

* [Python 3.8](https://www.python.org/downloads/release/python-380/)
* [numba](http://numba.pydata.org)
* [scipy](https://www.scipy.org)
* [scikit-learn](https://scikit-learn.org)
* [scikit-learn-extra](https://scikit-learn-extra.readthedocs.io/en/stable/install.html)
* [json](https://docs.python.org/3/library/json.html)
* [xlsxwriter](https://xlsxwriter.readthedocs.io)
* [tkinter](https://docs.python.org/3/library/tkinter.html)


## Examples

Four executable example configurations for data on cultural heritage objects, such as paintings and buildings, can be found in ```DataValueClustering\experiments\evaluation```.
The configurations were created for the following data fields:
artist name and dating from the data model [MIDAS](https://archiv.ub.uni-heidelberg.de/artdok/3770/) as well as measurement unit and attribution qualifier from the data model [LIDO](http://www.lido-schema.org/schema/v1.0/lido-v1.0.xsd/).
The data values that the configurations are applied to can be found at ```DataValueClustering\data```.
The clustering results can be found in ```DataValueClustering\experiments\exports\study```.

<!---
These examples also were used for the evaluation of the approach in the associated research paper.
-->


## Usage

For running the GUI, ```main.py``` has to be executed. It can be found in ```DataValueClustering\gui_center```.


## Authors
 
* Viola Wenz - [viola.wenz@uni-marburg.de](mailto:viola.wenz@uni-marburg.de?subject=[GitHub]%20Data%20Value%20Clustering)  
* Arno Kesper - [arno.kesper@uni-marburg.de](mailto:arno.kesper@uni-marburg.de?subject=[GitHub]%20Data%20Value%20Clustering)  
* Gabriele Taentzer - [taentzer@uni-marburg.de](mailto:taentzer@uni-marburg.de?subject=[GitHub]%20Data%20Value%20Clustering)  

This work emerged from the research project "[KONDA](https://zenodo.org/communities/konda-project)". 
![KONDA](readme_images/konda_logo.jpg)


## License

GNU Lesser General Public License v3.0
