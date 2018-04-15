The code of this repository was used for the following publication. If
you find this code useful please cite our paper:

```
@article{Gallego2017,
title = "Grammatical inference of directed acyclic graph languages with polynomial time complexity",
author = "Antonio-Javier Gallego and Damián López and Jorge Calera-Rubio",
journal = "Journal of Computer and System Sciences",
year = "2017",
issn = "0022-0000",
doi = "https://doi.org/10.1016/j.jcss.2017.12.002",
url = "http://www.sciencedirect.com/science/article/pii/S0022000017302866"
}
```

Below we include instructions to reproduce the experiments.



## Requirements

First you have to install version 1.11 of the Python NetworkX library. For this you can run the following command:

```
pip install networkx==1.11
```


## Usage

The `grammin.py` script runs the grammatical inference algorithm. The parameters of this script are the following:


| Parameter    | Default | Description                      |
| ------------ | ------- | -------------------------------- |
| `-path`      |         | Path to the dataset              |
| `-ftype`     |  grf    | Input file type: grf, gxl        |
| `-nlabel`    |         | Tag used for node labels (only for gxl files) |
|              |         | Mutagenicity: chem, GREC: type, RNA and NIST do not have |
| `-db`        |  -1     | Dataset name: grec, mutagen, rna, nist        |
| `-c`         |  -1     | Class to validate. -1 to validate all         |
| `-values`    |  2,3,4  | Comma-separated list of k values to test      |
| `-limit`     |         | Limit number of samples per class             |
| `-step`      |  100    | Step size between tests. Use -1 to test only at the end  |
| `--remove`   |         | Remove graphs with more than one initial node |


The only mandatory parameter is `-path`, the rest are optional. The `-nlabel` parameter allows to specify the attribute that contains the node's label (only used for the `gxl` files). The labels of the samples are specified in the name of the file, whose name pattern can change depending on the dataset, for this reason it is necessary to indicate the name of the dataset that will be loaded with the `-db` option. The `-c` parameter allows to validate the inclusion of all classes (value -1) or of the indicated class. The `-values` option indicates the list of k values that will be evaluated.

For example, to classify all the classes in the Mutagenicity dataset, you have to run the following command:

```
python grammin.py -c -1 -ftype gxl -path datasets/Mutagenicity -nlabel chem
```




## Datasets


The `datasets` folder includes the _Hairpin loops_ dataset and the graphs extracted from the NIST dataset (Neighbor, Grid, and Skeleton graphs). The rest can be downloaded from the following address:


IAM Graph Database Repository 

http://www.fki.inf.unibe.ch/databases/iam-graph-database

