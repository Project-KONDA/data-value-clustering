# Data Value Clustering

This tool is a proof of concept for a bottom-up approach to detecting quality problems in data
models that manifest in heterogeneous data values.

The approach is described in detail in the research paper "[Detecting Quality Problems in Data Models by
Clustering Heterogeneous Data Values](################)".
[//]: # (doi), published in the [proceedings](doi) of the conference "[MODELS2021](https://conf.researchr.org/home/models-2021)".


![Component Diagram](readme_images/components_small.png)


This diagram gives an overview of the components and their interfaces.
The core of the approach is the Clustering-based Analyser. It realises the workflow presented at the paper and controlls the data flows between the different components. In this proof-of-concept implementation, this is realized via the Main-class (DataValueClustering\gui_center\main.py).

The Extraction component is used to extract a list of data values from the database.

Multiple GUI components are required to enable the configuration and present the output of the approach.

The Data Value Clustering component performs the 3-step calculations to generate the clustering.
It beginns with the calculation of the abstraction, where irrelevant syntactic details are removed from the data values as previously configured.
Then the likeliness between the values are calculated via distance calculation.
Based on this the data values are clustered via the chosen cluster algorithm.

The Export component allows to save the parameters and the resulting clustering of the current iteration as json file.
Further it creates an Excel representation of the result clustering.


## Built With

* [PyCharm 2021.1](https://www.jetbrains.com/pycharm/download/)
* [Python 3.8](https://www.python.org/downloads/release/python-380/)

This project was implemented using the PyCharm IDE. However it is possible to execute the implementation via any Python interpreter.


## Installation

Required Python Packages (can be installed via PyCharm):

* [Python 3.8](https://www.python.org/downloads/release/python-380/)
* [numba](http://numba.pydata.org)
* [scipy](https://www.scipy.org)
* [scikit-learn](https://scikit-learn.org)
* [scikit-learn-extra](https://scikit-learn-extra.readthedocs.io/en/stable/install.html)
* [json](https://docs.python.org/3/library/json.html)
* [xlsxwriter](https://xlsxwriter.readthedocs.io)
* [tkinter](https://docs.python.org/3/library/tkinter.html)


## Examples

Fully configured and directly executable example executions are presented in DataValueClustering\experiments\evaluation. These examples also were used for the evaluation of the approach in the associated research paper.


## Usage

For manual configuration via GUI the class Main has to be executed. It can be found in DataValueClustering\gui_center\main.py.


## Authors
 
* Viola Wenz - [viola.wenz@uni-marburg.de](mailto:viola.wenz@uni-marburg.de?subject=[GitHub]%20Data%20Value%20Clustering)  
* Arno Kesper - [arno.kesper@uni-marburg.de](mailto:arno.kesper@uni-marburg.de?subject=[GitHub]%20Data%20Value%20Clustering)  
* Gabriele Taentzer - [taentzer@uni-marburg.de](mailto:taentzer@uni-marburg.de?subject=[GitHub]%20Data%20Value%20Clustering)  

This work emerged from the research project "[KONDA](https://zenodo.org/communities/konda-project)". 
![KONDA](readme_images/konda_logo.jpg)


## License

GNU Lesser General Public License v3.0
