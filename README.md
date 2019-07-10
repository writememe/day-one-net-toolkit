# Day One Network Discovery Toolkit #

## Background ##

This toolkit has been created to enable those who are relatively new with [Nornir](https://nornir.readthedocs.io/en/latest/index.html) or [NAPALM](https://napalm.readthedocs.io/en/latest/) with the 
benefits of these two great open source projects.

At a high level, the intent is to lower the barrier to entry into exploring these
projects and provide new users with a real-life example of automating discovery tasks
when first interacting with a new network.

I have open sourced this repository in an attempt to contribute back to the wider community and hopefully kickstart others
in sparking their interest in network automation.

By using this toolkit, you will be able to answer and provide information on questions like:

- What model(s) of Cisco devices do we have?
- What OS version(s) do we have for the same model across the inventory?
- Has someone configured IPv6 on any devices?
- What local usernames are configured on all platforms?
- What devices have the longest uptime?
- What are all our serial numbers which we need for maintainance renewals?

## Pre-requisties ##

The following pre-requisites are required to use this toolkit:

-  Python 3.6 or higher
-  Git
- A network inventory of your devices including hostname, IP address, OS type, username and password

In addition to these pre-requisites, the following items are recommended:

- Use a virtual environment. An example of this can be done in [Pycharm](https://www.jetbrains.com/help/pycharm/creating-virtual-environment.html)
- Basic understanding of Python  
- Basic understanding of YAML

## Installation ##

To install the toolkit and the associated modules, please perform the following:  

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

The first step is to populate the hosts.yaml file with the pertinent information about your network devices.

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

## collection-toolkit.py - Summarised discovery

The purpose of this repository to provide network operators with a day one toolkit to collect information about a new network.

The idea is at the end of day one, you should have the following:

- All running and startup/candidate configs
- All applicable NAPALM getters

This toolkit uses Nornir as the DSL. Being pure python, we can use all the existing Python modules on offer.
