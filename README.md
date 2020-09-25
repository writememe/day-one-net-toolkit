# Day One Network Discovery Toolkit #

![day-one-net-toolkit](https://github.com/writememe/day-one-net-toolkit/workflows/day-one-net-toolkit/badge.svg)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/)
[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)
[![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/writememe/day-one-net-toolkit)

## Table of Contents

- [Background](#background)
- [Pre-requisites](#pre-requisites)
- [Installation](#installation)
  - [Inventory Setup](#inventory-setup)
    - [hosts.yaml file](#step-1---inventoryhostsyaml-file)
    - [groups.yaml file](#step-2---inventorygroupsyaml-file)
- [Operating Instructions](#operating-instructions)
  - [day-one-toolkit.py - Detailed discovery and config collection](#day-one-toolkitpy---detailed-discovery-and-config-collection)
  - [collection-toolkit.py - Summarised discovery](#collection-toolkitpy---summarised-discovery)
- [Supporting Information](#supporting-information)
- [Contributing](#contributing)

## Background ##

This toolkit has been created to enable those who are relatively new with [Nornir](https://nornir.readthedocs.io/en/latest/index.html) or [NAPALM](https://napalm.readthedocs.io/en/latest/) with the 
benefits of these two great open source projects.

At a high level, the intent is to lower the barrier to entry into exploring these
projects and provide new users with a real-life example of automating discovery tasks
when first interacting with a new network.

I have open sourced this project in an attempt to contribute back to the wider community and hopefully kickstart others
in sparking their interest in network automation.

By using this toolkit, you will be able to answer and provide information on questions like:

_- What model(s) of Cisco/Juniper/Arista devices do we have?_  
_- What OS version(s) do we have for the same model across the inventory?_  
_- Has someone configured IPv6 on any devices?_  
_- What local usernames are configured on all platforms?_  
_- What devices have the longest uptime?_  
_- What are all our serial numbers which we need for maintenance renewals?_  

## Pre-requisites ##

The following pre-requisites are required to use this toolkit:

- Python 3.6 or higher
- Git
- A network inventory of your devices including hostname, IP address, OS type, username and password

In addition to these pre-requisites, the following items are recommended:

- Basic understanding of Python  
- Basic understanding of YAML
- Basic understanding of JSON

## Installation ##

To install the toolkit and the associated modules, please perform the following from within your virtual environment:  

1) Clone the repository to the machine on which you will run the application from:

```git
git clone https://github.com/writememe/day-one-net-toolkit.git
cd day-one-net-toolkit
```

2) Populate your Nornir inventory files:

    - [defaults.yaml](inventory/defaults.yaml)
    - [groups.yaml](inventory/groups.yaml)
    - [hosts.yaml](inventory/hosts.yaml)

See the [Inventory Setup](#inventory-setup) below for more detailed instructions

3) Create the virtual environment to run the application in:

```console
virtualenv --python=`which python3` venv
source venv/bin/activate
```
4) Install the requirements:

```python
pip install -r requirements.txt
```

5) Set two environmental variables, which are used by the application as the default credentials to login to devices:

```bash
export NORNIR_DEFAULT_USERNAME=<someusername>
export NORNIR_DEFAULT_PASSWORD=<somepassword>
```
6) Validate these environmental variables by entering the following command:

```bash
env | grep NORNIR
```
You should see the two environment variables set.

### Inventory Setup ##

You need to populate some YAML files with your particular network inventory. Below is the procedure to 
populate your minimum variables in order to get yourself up and running. 
This toolkit takes advantages of Nornir's inheritance model so we are as efficient as possible.

Throughout the setup, we are going to use the example device inventory below:

| Hostname  |  IP Address | FQDN | Platform|
| ---------- |----------------|---------------|---------|
| lab-iosv-01| 10.0.0.12 | lab-iosv-01.lab.dfjt.local | ios |
| lab-arista-01| 10.0.0.11 | lab-arista-01.lab.dfjt.local | eos |
| lab-nxos-01| 10.0.0.14 | lab-nxos-01.lab.dfjt.local | nxos |

#### Step 1 - inventory/hosts.yaml file

The first step is to populate the hosts.yaml file with the pertinent information about your hosts.

Below is an example of the hosts.yaml structure for one entry:

```yaml
<fqdn>
    hostname: <fqdn> or <ip address>
    groups:
        - <platform>
```

An extension of this using our example inventory is below, using a mixture of FQDN or IP addresses for the hosts.yaml file:

```yaml
lab-iosv-01.lab.dfjt.local
    hostname: 10.0.0.12
    groups:
        - ios
        
lab-arista-01.lab.dfjt.local
    hostname: 10.0.0.11
    groups:
        - eos
        
lab-nxos-01.lab.dfjt.local
    hostname: lab-nxos-01.lab.dfjt.local
    groups:
        - nxos
```

NOTE: We are only putting in the absolute minimum data to get the toolkit up and running. You will notice that other Nornir inventories
can look markedly different to this and have been enriched with more metadata. This will not be explored in this toolkit.

#### Step 2 - inventory/groups.yaml file

The second step is to populate the groups.yaml file with information regarding each group setup in Step 1. Below is an example of what we
use in our groups.yaml file:

```yaml
<group_name>:
    platform: <platform>

```

An extension of this using our example inventory is below, using the groups which were setup in Step 1:

```yaml
ios:
    platform: ios

eos:
    platform: eos

nxos:
    platform: nxos
    
junos:
    platform: junos
    
iosxr:
    platform: iosxr

```

NOTE: You will notice some additional groups in here named `junos` and `iosxr` in here as well.
These were intentionally added to show how you would consistently implement this on other platforms.

You are now setup and ready to use the toolkit!

## Operating Instructions

To run the scripts, please run the following from the command line.

For `day-one-toolkit.py` please run the following:

```python
python day-one-toolkit.py
```

For `collection-toolkit.py` please run the following:

```python
python collection-toolkit.py
```

## day-one-toolkit.py - Detailed discovery and config collection

This script uses the Nornir inventory used in the setup and performs two operations:

- Collect the running and startup/candidate configurations for each hosts and
store them using the following directory convention:

```bash
.
|
├── configs
    ├── lab-arista-01.lab.dfjt.local
    │   ├── running.txt
    │   └── startup.txt
    ├── lab-iosv-01.lab.dfjt.local
    │   ├── running.txt
    │   └── startup.txt
    └── lab-nxos-01.lab.dfjt.local
        ├── running.txt
        └── startup.txt


```

NOTE: The directory structure is dynamically allocated and the appropriate configs are retrieved based on platform.

- Based on the supported list of [NAPALM getters](https://napalm.readthedocs.io/en/latest/support/index.html#getters-support-matrix),
 attempt to retrieve all the getters which are supported on each platform and store them using the following directory convention:  
 
```bash
facts
├── lab-arista-01.lab.dfjt.local
    ├── arp_table.json
    ├── bgp_neighbors.json
    ├── bgp_neighbors_detail.json
    ├── environment.json
    ├── facts.json
    ├── interfaces.json
    ├── interfaces_counters.json
    └── interfaces_ip.json

```

There is a log file which is dynamically created in the `logs/` directory which maintains the success and failure of each task on each host
and provides a summary of what failed and succeeded. This file follows the naming convention:

_DISCOVERY-LOG-YYYY-MM-DD-HH-MM-SS.txt_  

A collection run on July the 10th, 2019 at 19:19:54 would have the log file name of:  

DISCOVERY-LOG-2019-07-10-19-19-54.txt

From here, you could SCP these files to a central location, or commit them to a central repository for version control and tracking.

## collection-toolkit.py - Summarised discovery

This script uses the Nornir inventory used in the setup collects key information about all devices using NAPALM getters
and saves them to an Excel workbook. The information collected is:  

- Facts
- Interfaces
- Interfaces IP
- LLDP neighbor
- Users

Some of the information has been omitted from the spreadsheet as this is meant to provide a key summary of the environment.

Once the script has run, it will create an Excel workbook using the following convention:  

_Collection-<customer_name>-YYYY-MM-DD-HH-MM-SS.xlsx_

In the toolkit, you can change the customer name variable in the code under the `create_workbook` function towards the end of the code:  

```
# Assign customer name to Excel file
customer_name = "Customer"
```

There is a log file which is dynamically created in the `logs/` directory which maintains the success and failure of each task on each host
and provides a summary of what failed and succeeded. This file follows the naming convention:

_COLLECTION-LOG-YYYY-MM-DD-HH-MM-SS.txt_  

A collection run on July the 10th, 2019 at 19:19:54 would have the log file name of:  

COLLECTION-LOG-2019-07-10-19-19-54.txt

### Why an Excel workbook?!?

I chose Excel for a few reasons:  

1) Virtually everyone knows how to use Excel so this report can be passed around to non-programmer teams like Procurement, Service Desk or Change Management.

2) It's easy to format and query, or apply additional fields to as needed.

3) This provides information in a format which is easy to understand for management.

4) It demonstrates the advantages of using Nornir as we can access many mature Python modules
 such as [Openpyxl](https://openpyxl.readthedocs.io/en/stable/index.html), as Nornir is pure Python.

## Supporting Information

In addition to what is documented in this repo, I've written some more long form descriptions of Nornir and solutions presented here over at my blog:

[Exploring Nornir - Part One](https://blog.danielteycheney.com/posts/exploring-nornir-part-one/)

[Exploring Nornir - Part Two](https://blog.danielteycheney.com/posts/exploring-nornir-part-two/)

## Contributing ##

If you are interested in contributing or adding new features, please go to this [page](https://github.com/writememe/day-one-net-toolkit/blob/master/CONTRIBUTING.md)
on how to contribute.
