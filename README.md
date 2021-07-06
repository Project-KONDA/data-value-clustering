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


## GUI

The goal of the GUI is to provide an interface with which the nomerous parameters can be configured intuitively and easily by domain experts based on their domain knowledge.
Therefore the ultimate goal of the interface is to require as little technical understanding of the process.
For this we want to hide the complexity by reducing the parameter amount and determine parameters based on questions adressing specific circumstances within the domain.

Currently the GUI is build from multiple windows, that open successively.
In the future we will reimplement the center window, to be the real center of configuration.
It shall be able to start the data value clustering process and present the results.
Further it shall provide the reentry point for new iterations.


### Abstraction Configuration

![Abstraction Configuration](readme_images/config_abstraction.png)

For configuring the abstraction step we developed an interactive view based on a binary response questionnaire.
Each option is accompanied by a ToolTip showing additional information including an explanation and an example.
Meanwhile the abstraction of the first 100 original values are dynamically visualized on the right-hand side.
For this each abstracted value is listed with all associated original values.


### Distance Configuration

For the clustering the similarity between values must be measured.
To do this we chose the weighted Levenshtein distance, which is a highly configurable edit distance function for string values.
For  the configuration each edit operation is assigned a weight.
As the measured distance is the accumulated sum of the weights for each performed edit operation during the transformation of one string to another.
Therefore each operation needs an associated weight, which can be dependent on the in- and outputs.


#### Matrix View

The most flexible and most complex configuration of the distance function gives the Matrix View.
Here groups of symbols can be manually configured.
Every insertion, deletion and substitution can be assigned a weight based on domain knowledge and personal intentions.

![Matrix View](readme_images/config_matrixview.png)

For this the Matrix view offers a tabular interface.
Each cell is assigned a substitution operation between groups of symbols, where the user can input a custom weight.
The table should be read in such a way that the substitutions are from left to top. 
Additions and deletions are interpreted as substitutions from or to empty strings. 
To represent this, the first column and first row is always reserved for empty strings.

The distance function needs to be symmetrical to fulfill the symmetry axiom for metrics.
Therefore the matrix must be symmetrical to the diagonal.
To guarantee this, all input values are copied into the symmetrically corresponding field.


#### Blob View

![Blob View](readme_images/config_blobview.png)

As a more simple and playful approach on configuring the numerous weights for the configuration of the distance function we developed the Blob View.
The view enables the configuration of the weight matrix via moving and scaling graphical objects.

Groups of characters are presented as graphical objects, called blobs. 
They correspond to the columns and rows of the matrix.
To configure additions and deletions we use an additional blob, the small blue blob labelled with an X.
For configuring the weights, the user can move the blobs on the 2D canvas using drag and drop.
The weight for substitutions within a group is represented by the size of the corresponding blob. 
The user can modify the size using the mouse wheel while hovering over the blob.


#### Slider View (prevision)

The Slider view is the easiest way of configuring the distance function.
However it is not implemented yet.
The idea of this view is, to only configure relative importance of different groups of symbols.
For this each group will have one slider.
From the relative importances a valid weight matrix is calculated.


### Cluster Choice

We support multiple clustering algorithms.
For the selection of a fitting algorithm, we implemented a short binary questionnaire with fitting ToolTips.


### Cluster Configuration

All the clustering algorithms come with many parameters.
We implemented a modularized view to configure these parameters contains a checkbox, a slider or an enumeration with radio buttons, respectively.
The sliders for numerical parameters are provided with appropriate minimum and maximum values.
For enumerations, tooltips are provided for each option.

![Hierarchical Configuration 2](readme_images/config_clustering_hierarchical2.png)

The modules also mimic the dependencies between parameters.
For example in hierarchical clustering, there is an alternating dependency between n_clusters and distance_threshold: 
only one of the parameters is required.
The parameter depth is enabled only if the option “inconsistent” is chosen for the parameter criterion.


### Result

![Excel Excerpt](readme_images/excel_excerpt2.png)

Currently there is no real result view implemented.
Instead the resulting clusters are provided via a generated Excel file.
In the future, we plan to also present this cluster representation directly in the interface.
This shall also include a questionnaire on which features of the clustering do not fulfill the expectations of the user.
They will then be used to provide suggestions for the next iteration on how to change the configuration.



## Authors
 
* Viola Wenz - [viola.wenz@uni-marburg.de](mailto:viola.wenz@uni-marburg.de?subject=[GitHub]%20Data%20Value%20Clustering)  
* Arno Kesper - [arno.kesper@uni-marburg.de](mailto:arno.kesper@uni-marburg.de?subject=[GitHub]%20Data%20Value%20Clustering)  
* Gabriele Taentzer - [taentzer@uni-marburg.de](mailto:taentzer@uni-marburg.de?subject=[GitHub]%20Data%20Value%20Clustering)  

This work emerged from the research project "[KONDA](https://zenodo.org/communities/konda-project)". 
![KONDA](readme_images/konda_logo.jpg)


## License

GNU Lesser General Public License v3.0
