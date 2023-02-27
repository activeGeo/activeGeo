In this directory, we use RDNS hostname to infer the locations of some IPs. The output will be put in the directory `pickle_bin`. We have put the results of our run which is compressed.

There are some files should be put in the directory `src`. Considering the file size, we only put some small demo files. Here are the specific requirements:

1. `itdk_data`
This directory contains the `midar-iff.nodes.bz2` file, which is published by CAIDA. 
Here is the example: https://publicdata.caida.org/datasets/topology/ark/ipv4/itdk/2021-03/ .
We split this file into a number of smaller files named in the format `data-{i}.txt` where `i` is a number.

2. `rdns_data`
This directory contains the RDNS hostname file. We get it from Rapid7 RDNS. 
We also split this file into a number of smaller files named in the format `data-{i}.txt` where `i` is a number.

3. `georule_by_caida.json`
This file is published by CAIDA. This link is the source: https://publicdata.caida.org/datasets/topology/ark/ipv4/itdk/2021-03/202103-midar-iff.geo-re.jsonl. It is the work of the paper 'Luckie M, Huffaker B, Marder A, et al. Learning to extract geographic information from internet router hostnames[C]//Proceedings of the 17th International Conference on emerging Networking EXperiments and Technologies. 2021: 440-453'.


