# Day One Network Discovery Toolkit #

![day-one-net-toolkit](https://github.com/writememe/day-one-net-toolkit/workflows/day-one-net-toolkit/badge.svg)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/)
[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)


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

-  Python 3.6 or higher
-  Git
- A network inventory of your devices including hostname, IP address, OS type, username and password

In addition to these pre-requisites, the following items are recommended:

- Create a virtual environment for this project. There are some guides on how to do this in 
 [Pycharm](https://www.jetbrains.com/help/pycharm/creating-virtual-environment.html), on a 
 [Mac](https://gist.github.com/pandafulmanda/730a9355e088a9970b18275cb9eadef3) or follow the
 [Official Documentation](https://virtualenv.pypa.io/en/stable/userguide/)
- Basic understanding of Python  
- Basic understanding of YAML

## Installation ##

To install the toolkit and the associated modules, please perform the following from within your virtual environment:  

1) Clone the repository to your local machine:  
`git clone https://github.com/writememe/day-one-net-toolkit.git`
2) Change to the repo directory:  
`cd day-one-net-toolkit`
3) Install the required modules:  
`pip install -r requirements.txt`

## Setup ##

You need to populate some YAML files with your particular network inventory. Below is the procedure to 
populate your minimum variables in order to get yourself up and running. 
This toolkit takes advantages of Nornir's inheritance model so we are as efficient as possible.

Throughout the setup, we are going to use the example device inventory below:

| Hostname  |  IP Address | FQDN | Platform| Username| Password|
| ---------- |----------------|---------------|---------|---------|-------------|
| lab-iosv-01| 10.0.0.12 | lab-iosv-01.lab.dfjt.local | ios | username1 | 2password |
| lab-arista-01| 10.0.0.11 | lab-arista-01.lab.dfjt.local | eos | username1| 2password |
| lab-nxos-01| 10.0.0.14 | lab-nxos-01.lab.dfjt.local | nxos | username1 | 2password |


### Step 1 - inventory/hosts.yaml file

The first step is to populate the hosts.yaml file with the pertinent information about your hosts.

Below is an example of the hosts.yaml structure for one entry:

```
<fqdn>
    hostname: <fqdn> or <ip address>
    groups:
        - <platform>
```

An extension of this using our example inventory is below, using a mixture of FQDN or IP addresses for the hosts.yaml file:

```
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

### Step 2 - inventory/groups.yaml file

The second step is to populate the groups.yaml file with information regarding each group setup in Step 1. Below is an example of what we
use in our groups.yaml file:

```
<group_name>:
    platform: <platform>
    username: <username>
    password: <password>

```

An extension of this using our example inventory is below, using the groups which were setup in Step 1:

```
ios:
    platform: ios
    username: username1
    password: 2password

eos:
    platform: eos
    username: username1
    password: 2password

nxos:
    platform: nxos
    username: username1
    password: 2password
    
junos:
    platform: junos
    username: username1
    password: 2password
    
iosxr:
    platform: iosxr
    username: username1
    password: 2password

```

NOTE: You will notice some additional groups in here named `junos` and `iosxr` in here as well.
These were intentionally added to show how you would consistently implement this on other platforms.

**WARNING: Obviously performing this practice means that you have your password(s) for your network access in clear text
in these files. If you are uncomfortable with this, check out some options in the
[Nornir documentation](https://nornir.readthedocs.io/en/latest/howto/transforming_inventory_data.html?highlight=transform#Setting-a-default-password).**

You are now setup and ready to use the toolkit!

## day-one-toolkit.py - Detailed discovery and config collection

This script uses the Nornir inventory used in the setup and performs two operations:

- Collect the running and startup/candidate configurations for each hosts and
store them using the following directory convention:

```
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
 
```
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


## Known Issues

At the time of writing, there are two known issues with workarounds for this toolkit.

### NAPALM - nxos - get_interfaces_ip

At the time of writing, napalm=2.4.0 did not correctly process the get_interfaces_ip function for nxos device. Below is a link to the issue raised, which seems to be resolved in the develop branch of this version:

https://github.com/napalm-automation/napalm/issues/964

It's anticipated that this will be resolved in the next release. There is a workaround in the above link.

### NAPALM - junos - get_users

In the `collection-toolkit.py` toolkit, the standard way of placing all `<os>_users` into a list and
iterating over that list doesn't work for junos: 

```

    # Take all the those results and add them to a list so we can iterate over the result
    os_users = [
        ios_users,
        # TODO: Need to work out this junos_users filter not working.
        # junos_users,
        eos_users,
        nxos_users,
        iosxr_users,
    ]
    
 ```
 
 Therefore, I've had to create a JUNOS platform block just for `junos_users`:  
 
 ```
   # JUNOS Platform Block
    """
    I am not sure how this is working given that the task results
    are failing, but it is....
    """
    for host, task_results in junos_users.items():
```

This block of code results in getting results for junos devices.

## Contributing ##

If you are interested in contributing or adding new features, please go to this [page](https://github.com/writememe/day-one-net-toolkit/blob/master/CONTRIBUTING.md)
on how to contribute.
