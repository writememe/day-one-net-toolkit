#!/usr/bin/env python
# Author: Daniel Teycheney

# Import Modules
from nornir import InitNornir
from nornir.plugins.tasks.networking import napalm_get
from nornir.plugins.tasks.files import write_file
import json
import requests
import pathlib
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import datetime as dt

# Disable urllib3 warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


# Functions


def collect_getters(task, getter):
    """
    This function is used to collect all applicable getters for the applicable OS
    and then store these results under the respective facts/<hostname>/ directory.
    :param task: The name of the task to be run.
    :param getter: The name of the NAPALM getter.
    :return: An AggregatedResult of this task.
    """
    # Assign facts directory to variable
    fact_dir = "facts"
    # Assign hostname directory to a variable
    host_dir = task.host.name
    # Assign the destination directory to a variable. i.e facts/hostname/
    entry_dir = fact_dir + "/" + host_dir
    # Create facts directory and/or check that it exists
    pathlib.Path(fact_dir).mkdir(exist_ok=True)
    # Create entry directory and/or check that it exists
    pathlib.Path(entry_dir).mkdir(exist_ok=True)
    # Try/except block to catch exceptions, such as NotImplementedError
    try:
        # Gather facts using napalm_get and assign to a variable
        facts_result = task.run(task=napalm_get, getters=[getter])
        # Write the results to a JSON, using the convention <filter_name>.json
        task.run(
            task=write_file,
            content=json.dumps(facts_result[0].result[getter], indent=2),
            filename=f"" + str(entry_dir) + "/" + str(getter) + ".json",
        )
    # Handle NAPALM Not Implemented Error exceptions
    except NotImplementedError:
        return "Getter Not Implemented"
    except AttributeError:
        return "AttributeError: Driver has no attribute"


def collect_config(task, getter):
    """
    This function is used to collect applicable configs getters for the applicable OS
    and then store these results under the respective configs/<hostname>/ directory
    :param task: The name of the task to be run.
    :param getter: The name of the NAPALM config getter.
    :return: An AggregatedResult of this task.
    """
    # Assign configs directory to variable
    config_dir = "configs"
    # Assign hostname directory to a variable
    host_dir = task.host.name
    # Assign the destination directory to a variable. i.e configs/hostname/
    entry_dir = config_dir + "/" + host_dir
    # Create facts directory and/or check that it exists
    pathlib.Path(config_dir).mkdir(exist_ok=True)
    # Create entry directory and/or check that it exists
    pathlib.Path(entry_dir).mkdir(exist_ok=True)
    # Try/except block to catch exceptions, such as NotImplementedError
    try:
        # Gather config using napalm_get and assign to a variable
        config_result = task.run(task=napalm_get, getters=["config"])
        # Write the results to a JSON, using the convention <filter_name>.txt
        task.run(
            task=write_file,
            content=config_result.result["config"][getter],
            filename=f"" + str(entry_dir) + "/" + str(getter) + ".txt",
        )
    # Handle NAPALM Not Implemented Error exceptions
    except NotImplementedError:
        print("NAPALM get filter not implemented " + str(getter))


def getter_collector():
    """
    This function is the main function of the toolkit.

    It performs two roles:

    1) Collects configurations for all devices in the inventory,
    based on NAPALM support.

    These configurations are saved in the configs/ directory using the following convention:
    <hostname>/<filter_name>.txt

    2) Performs a collection of supported getters based on
    the official NAPALM supported filter list:
    https://napalm.readthedocs.io/en/latest/support/

    It has been written in a way whereby one simply updates the appropriate <os>_getters
    list to add or remove supported getters. All getters are stored in the facts/
    directory using the following convention:
    <hostname>/<filter_name>.json

    """
    """
    The following block of code is used to generate a log file in a directory.
    These log files will indicate the success/failure of filter collector
    for retrospective analysis.
    """
    # Capture time
    cur_time = dt.datetime.now()
    # Cleanup time, so that the format is clean for the output file 2019-07-01-13-04-59
    fmt_time = cur_time.strftime("%Y-%m-%d-%H-%M-%S")
    # Set log directory variable
    log_dir = "logs"
    # Create log directory if it doesn't exist.
    pathlib.Path(log_dir).mkdir(exist_ok=True)
    # Create log file name, with timestamp in the name
    filename = str("DISCOVERY-LOG") + "-" + fmt_time + ".txt"
    # Join the log file name and log directory together into a variable
    log_file_path = log_dir + "/" + filename
    # Create the log file
    log_file = open(log_file_path, "w")
    # Start of logging output
    print("STARTING DISCOVERY: " + str(fmt_time))
    log_file.write("STARTING DISCOVERY: " + str(fmt_time) + "\n\n")
    """
    Initialise two counters, so that success and failure can be counted
    and incremented as the getters are collected.
    """
    # Success Counter
    success_count = 0
    # Fail Counter
    fail_count = 0
    # Initialize Nornir and define the inventory variables.
    nr = InitNornir(
        inventory={
            "options": {
                "host_file": "inventory/hosts.yaml",
                "group_file": "inventory/groups.yaml",
                "defaults_file": "inventory/defaults.yaml",
            }
        }
    )
    """
    The following block of lists are the supported getters per OS based
    on the website https://napalm.readthedocs.io/en/latest/support/
    """
    # IOS supported getters
    ios_getters = [
        "arp_table",
        "bgp_neighbors",
        "bgp_neighbors_detail",
        "environment",
        "facts",
        "interfaces",
        "interfaces_counters",
        "interfaces_ip",
        "ipv6_neighbors_table",
        "lldp_neighbors",
        "lldp_neighbors_detail",
        "mac_address_table",
        "network_instances",
        "ntp_peers",
        "ntp_servers",
        "ntp_stats",
        "optics",
        "snmp_information",
        "users",
    ]
    # JUNOS supported getters
    junos_getters = [
        "arp_table",
        "bgp_config",
        "bgp_neighbors",
        "bgp_neighbors_detail",
        "environment",
        "facts",
        "interfaces",
        "interfaces_counters",
        "interfaces_ip",
        "ipv6_neighbors_table",
        "lldp_neighbors",
        "lldp_neighbors_detail",
        "mac_address_table",
        "network_instances",
        "ntp_peers",
        "ntp_servers",
        "ntp_stats",
        "optics",
        "snmp_information",
        "users",
    ]
    # EOS supported getters
    eos_getters = [
        "arp_table",
        "bgp_config",
        "bgp_neighbors",
        "bgp_neighbors_detail",
        "environment",
        "facts",
        "interfaces",
        "interfaces_counters",
        "interfaces_ip",
        "lldp_neighbors",
        "lldp_neighbors_detail",
        "mac_address_table",
        "network_instances",
        "ntp_servers",
        "ntp_stats",
        "optics",
        "snmp_information",
        "users",
    ]
    # NXOS supported getters
    nxos_getters = [
        "arp_table",
        "bgp_neighbors",
        "facts",
        "interfaces",
        "interfaces_ip",
        "lldp_neighbors",
        "lldp_neighbors_detail",
        "mac_address_table",
        "ntp_peers",
        "ntp_servers",
        "ntp_stats",
        "snmp_information",
        "users",
    ]
    # IOSXR supported getters
    iosxr_getters = [
        "arp_table",
        "bgp_config",
        "bgp_neighbors",
        "bgp_neighbors_detail",
        "environment",
        "facts",
        "interfaces",
        "interfaces_counters",
        "interfaces_ip",
        "lldp_neighbors",
        "lldp_neighbors_detail",
        "mac_address_table",
        "ntp_peers",
        "ntp_servers",
        "ntp_stats",
        "snmp_information",
        "users",
    ]
    """
    The following block of code assigns a filter based on platform to a variable.
    This variable is used later on to apply logic in for loops
    """
    ios_devices = nr.filter(platform="ios")
    junos_devices = nr.filter(platform="junos")
    eos_devices = nr.filter(platform="eos")
    nxos_devices = nr.filter(platform="nxos")
    iosxr_devices = nr.filter(platform="iosxr")
    """
    The following block of code is a list of config getters which will be
    iterated over to collect the different config types per OS
    """
    ios_config_getters = ["running", "startup"]
    junos_config_getters = ["running", "candidate"]
    eos_config_getters = ["running", "startup"]
    nxos_config_getters = ["running", "startup"]
    iosxr_config_getters = ["running", "startup"]
    """
    The following block is the main component of the program. Each OS collects
    the running config, all supported getters and the startup/candidate config
    based on the OS. Each OS block is as uniform as possible.
    """
    # IOS Platform Block
    for host in ios_devices.inventory.hosts.items():
        # Assign the hostname to a variable from the host tuple
        hostname = host[0]
        # Starting processing of a host
        print("** Start Processing Host: " + str(hostname))
        log_file.write("** Start Processing Host: " + str(hostname) + "\n")
        for config in ios_config_getters:
            # Start collecting the config getters
            print("Processing " + str(config) + " config ... ")
            log_file.write("Processing " + str(config) + " config ... " + "\n")
            # Execute the collect_config function
            configs = nr.run(
                task=collect_config, getter=config, on_failed=True, num_workers=20
            )
            """
            Access the specific 'napalm_get' result out of the collect_getters function
            and store whether the failed boolean is True (failure) or False (success)
            """
            configs_results = configs[hostname][1].failed
            # Conditional block to record success/fail count of the 'napalm_get' result
            if configs_results is True:
                print("FAILURE : " + str(hostname) + " - " + str(config) + " config")
                log_file.write(
                    "FAILURE : "
                    + str(hostname)
                    + " - "
                    + str(config)
                    + " config"
                    + "\n"
                )
                fail_count += 1
            else:
                print("SUCCESS : " + str(hostname) + " - " + str(config) + " config")
                log_file.write(
                    "SUCCESS : "
                    + str(hostname)
                    + " - "
                    + str(config)
                    + " config"
                    + "\n"
                )
                success_count += 1
        # For block to collect all supported getters
        for entry in ios_getters:
            # Start processing getters
            print("Processing Getter: " + str(entry))
            log_file.write("Processing Getter: " + str(entry) + "\n")
            # Execute collect_getters function
            getters = nr.run(
                task=collect_getters, getter=entry, on_failed=True, num_workers=20
            )
            """
            Access the specific 'napalm_get' result out of the collect_getters function
            and store whether the failed boolean is True (failure) or False (success)
            """
            getters_results = getters[hostname][1].failed
            # Conditional block to record success/fail count of the 'napalm_get' result
            if getters_results is True:
                log_file.write("FAILURE : " + str(hostname) + " - " + str(entry) + "\n")
                print("FAILURE : " + str(hostname) + " - " + str(entry))
                fail_count += 1
            else:
                log_file.write("SUCCESS : " + str(hostname) + " - " + str(entry) + "\n")
                print("SUCCESS : " + str(hostname) + " - " + str(entry))
                success_count += 1
        # Ending processing of host
        print("** End Processing Host: " + str(hostname))
        log_file.write("** End Processing Host: " + str(hostname) + "\n\n")
    # EOS Platform Block
    for host in eos_devices.inventory.hosts.items():
        # Assign the hostname to a variable from the host tuple
        hostname = host[0]
        # Starting processing of a host
        print("** Start Processing Host: " + str(hostname))
        log_file.write("** Start Processing Host: " + str(hostname) + "\n")
        for config in eos_config_getters:
            # Start collecting the config getters
            print("Processing " + str(config) + " config ... ")
            log_file.write("Processing " + str(config) + " config ... " + "\n")
            # Execute the collect_config function
            configs = nr.run(
                task=collect_config, getter=config, on_failed=True, num_workers=20
            )
            """
            Access the specific 'napalm_get' result out of the collect_getters function
            and store whether the failed boolean is True (failure) or False (success)
            """
            configs_results = configs[hostname][1].failed
            # Conditional block to record success/fail count of the 'napalm_get' result
            if configs_results is True:
                print("FAILURE : " + str(hostname) + " - " + str(config) + " config")
                log_file.write(
                    "FAILURE : "
                    + str(hostname)
                    + " - "
                    + str(config)
                    + " config"
                    + "\n"
                )
                fail_count += 1
            else:
                print("SUCCESS : " + str(hostname) + " - " + str(config) + " config")
                log_file.write(
                    "SUCCESS : "
                    + str(hostname)
                    + " - "
                    + str(config)
                    + " config"
                    + "\n"
                )
                success_count += 1
        # For block to collect all supported getters
        for entry in eos_getters:
            # Start processing getters
            print("Processing Getter: " + str(entry))
            log_file.write("Processing Getter: " + str(entry) + "\n")
            # Execute collect_getters function
            getters = nr.run(
                task=collect_getters, getter=entry, on_failed=True, num_workers=20
            )
            """
            Access the specific 'napalm_get' result out of the collect_getters function
            and store whether the failed boolean is True (failure) or False (success)
            """
            getters_results = getters[hostname][1].failed
            # Conditional block to record success/fail count of the 'napalm_get' result
            if getters_results is True:
                log_file.write("FAILURE : " + str(hostname) + " - " + str(entry) + "\n")
                print("FAILURE : " + str(hostname) + " - " + str(entry))
                fail_count += 1
            else:
                log_file.write("SUCCESS : " + str(hostname) + " - " + str(entry) + "\n")
                print("SUCCESS : " + str(hostname) + " - " + str(entry))
                success_count += 1
        # Ending processing of host
        print("** End Processing Host: " + str(hostname))
        log_file.write("** End Processing Host: " + str(hostname) + "\n\n")
    # NX-OS Platform Block
    for host in nxos_devices.inventory.hosts.items():
        # Assign the hostname to a variable from the host tuple
        hostname = host[0]
        # Starting processing of a host
        print("** Start Processing Host: " + str(hostname))
        log_file.write("** Start Processing Host: " + str(hostname) + "\n")
        for config in nxos_config_getters:
            # Start collecting the config getters
            print("Processing " + str(config) + " config ... ")
            log_file.write("Processing " + str(config) + " config ... " + "\n")
            # Execute the collect_config function
            configs = nr.run(
                task=collect_config, getter=config, on_failed=True, num_workers=20
            )
            """
            Access the specific 'napalm_get' result out of the collect_getters function
            and store whether the failed boolean is True (failure) or False (success)
            """
            configs_results = configs[hostname][1].failed
            # Conditional block to record success/fail count of the 'napalm_get' result
            if configs_results is True:
                print("FAILURE : " + str(hostname) + " - " + str(config) + " config")
                log_file.write(
                    "FAILURE : "
                    + str(hostname)
                    + " - "
                    + str(config)
                    + " config"
                    + "\n"
                )
                fail_count += 1
            else:
                print("SUCCESS : " + str(hostname) + " - " + str(config) + " config")
                log_file.write(
                    "SUCCESS : "
                    + str(hostname)
                    + " - "
                    + str(config)
                    + " config"
                    + "\n"
                )
                success_count += 1
        # For block to collect all supported getters
        for entry in nxos_getters:
            # Start processing getters
            print("Processing Getter: " + str(entry))
            log_file.write("Processing Getter: " + str(entry) + "\n")
            # Execute collect_getters function
            getters = nr.run(
                task=collect_getters, getter=entry, on_failed=True, num_workers=20
            )
            """
            Access the specific 'napalm_get' result out of the collect_getters function
            and store whether the failed boolean is True (failure) or False (success)
            """
            getters_results = getters[hostname][1].failed
            # Conditional block to record success/fail count of the 'napalm_get' result
            if getters_results is True:
                log_file.write("FAILURE : " + str(hostname) + " - " + str(entry) + "\n")
                print("FAILURE : " + str(hostname) + " - " + str(entry))
                fail_count += 1
            else:
                log_file.write("SUCCESS : " + str(hostname) + " - " + str(entry) + "\n")
                print("SUCCESS : " + str(hostname) + " - " + str(entry))
                success_count += 1
        # Ending processing of host
        print("** End Processing Host: " + str(hostname) + "\n")
        log_file.write("** End Processing Host: " + str(hostname) + "\n\n")
    # JUNOS Platform Block
    for host in junos_devices.inventory.hosts.items():
        # Assign the hostname to a variable from the host tuple
        hostname = host[0]
        # Starting processing of a host
        print("** Start Processing Host: " + str(hostname))
        log_file.write("** Start Processing Host: " + str(hostname) + "\n")
        for config in junos_config_getters:
            # Start collecting the config getters
            print("Processing " + str(config) + " config ... ")
            log_file.write("Processing " + str(config) + " config ... " + "\n")
            # Execute the collect_config function
            configs = nr.run(
                task=collect_config, getter=config, on_failed=True, num_workers=20
            )
            """
            Access the specific 'napalm_get' result out of the collect_getters function
            and store whether the failed boolean is True (failure) or False (success)
            """
            configs_results = configs[hostname][1].failed
            # Conditional block to record success/fail count of the 'napalm_get' result
            if configs_results is True:
                print("FAILURE : " + str(hostname) + " - " + str(config) + " config")
                log_file.write(
                    "FAILURE : "
                    + str(hostname)
                    + " - "
                    + str(config)
                    + " config"
                    + "\n"
                )
                fail_count += 1
            else:
                print("SUCCESS : " + str(hostname) + " - " + str(config) + " config")
                log_file.write(
                    "SUCCESS : "
                    + str(hostname)
                    + " - "
                    + str(config)
                    + " config"
                    + "\n"
                )
                success_count += 1
        for entry in junos_getters:
            # Start processing getters
            print("Processing Getter: " + str(entry))
            log_file.write("Processing Getter: " + str(entry) + "\n")
            # Execute collect_getters function
            getters = nr.run(
                task=collect_getters, getter=entry, on_failed=True, num_workers=20
            )
            """
            Access the specific 'napalm_get' result out of the collect_getters function
            and store whether the failed boolean is True (failure) or False (success)
            """
            getters_results = getters[hostname][1].failed
            # Conditional block to record success/fail count of the 'napalm_get' result
            if getters_results is True:
                log_file.write("FAILURE : " + str(hostname) + " - " + str(entry) + "\n")
                print("FAILURE : " + str(hostname) + " - " + str(entry))
                fail_count += 1
            else:
                log_file.write("SUCCESS : " + str(hostname) + " - " + str(entry) + "\n")
                print("SUCCESS : " + str(hostname) + " - " + str(entry))
                success_count += 1
        # Ending processing of host
        print("** End Processing Host: " + str(hostname) + "\n")
        log_file.write("** End Processing Host: " + str(hostname) + "\n\n")
    # IOS-XR Platform Block
    for host in iosxr_devices.inventory.hosts.items():
        # Assign the hostname to a variable from the host tuple
        hostname = host[0]
        # Starting processing of a host
        print("** Start Processing Host: " + str(hostname))
        log_file.write("** Start Processing Host: " + str(hostname) + "\n")
        for config in iosxr_config_getters:
            # Start collecting the config getters
            print("Processing " + str(config) + " config ... ")
            log_file.write("Processing " + str(config) + " config ... " + "\n")
            # Execute the collect_config function
            configs = nr.run(
                task=collect_config, getter=config, on_failed=True, num_workers=20
            )
            """
            Access the specific 'napalm_get' result out of the collect_getters function
            and store whether the failed boolean is True (failure) or False (success)
            """
            configs_results = configs[hostname][1].failed
            # Conditional block to record success/fail count of the 'napalm_get' result
            if configs_results is True:
                print("FAILURE : " + str(hostname) + " - " + str(config) + " config")
                log_file.write(
                    "FAILURE : "
                    + str(hostname)
                    + " - "
                    + str(config)
                    + " config"
                    + "\n"
                )
                fail_count += 1
            else:
                print("SUCCESS : " + str(hostname) + " - " + str(config) + " config")
                log_file.write(
                    "SUCCESS : "
                    + str(hostname)
                    + " - "
                    + str(config)
                    + " config"
                    + "\n"
                )
                success_count += 1
        # For block to collect all supported getters
        for entry in iosxr_getters:
            # Start processing getters
            print("Processing Getter: " + str(entry))
            log_file.write("Processing Getter: " + str(entry) + "\n")
            # Execute collect_getters function
            getters = nr.run(
                task=collect_getters, getter=entry, on_failed=True, num_workers=20
            )
            """
            Access the specific 'napalm_get' result out of the collect_getters function
            and store whether the failed boolean is True (failure) or False (success)
            """
            getters_results = getters[hostname][1].failed
            # Conditional block to record success/fail count of the 'napalm_get' result
            if getters_results is True:
                log_file.write("FAILURE : " + str(hostname) + " - " + str(entry) + "\n")
                print("FAILURE : " + str(hostname) + " - " + str(entry))
                fail_count += 1
            else:
                log_file.write("SUCCESS : " + str(hostname) + " - " + str(entry) + "\n")
                print("SUCCESS : " + str(hostname) + " - " + str(entry))
                success_count += 1
        # Ending processing of host
        print("** End Processing Host: " + str(hostname))
        log_file.write("** End Processing Host: " + str(hostname) + "\n\n")
    # Add the two variables together to get a total count into a variable
    total_count = success_count + fail_count
    # Provide a summary of the main function and add to log file
    print("SUMMARY" + "\n")
    log_file.write("SUMMARY" + "\n\n")
    print("SUCCESS COUNT : " + str(success_count))
    log_file.write("SUCCESS COUNT : " + str(success_count) + "\n")
    print("FAILURE COUNT : " + str(fail_count))
    log_file.write("FAILURE COUNT : " + str(fail_count) + "\n")
    print("TOTAL COUNT : " + str(total_count))
    log_file.write("TOTAL COUNT : " + str(total_count) + "\n")
    # Close the log file
    log_file.close()


# Execute main program
getter_collector()
