__author__ = 'Zachary Hill'

import re
import os
from sys import argv
import pprint

# TODO Move this to a YAML or JSON file
# Define list of regular expression searches that are terrible or cause for concern.
########################################################################################################################
bad_configs = [
    r'Total output drops: \d+',  # Search for interface drops
    r'transport input telnet|transport input all',  # Search for telnet enabled devices
    r'^ip http server',  # Search for http enabled devices
    r'^ip http secure-server',  # Search for https enabled devices
    r'^.*password 7',  # Search for cisco encrypted passwords
    r'Half-duplex',  # Search for half-duplex interfaces
    r'ip ssh version 1',  # Search for ssh version less than 2
    r'permit ip any any',  # Search for bad access lists
    r'ip dhcp pool',  # Search for DHCP servers
]

# TODO grab user argv for special flags to run
# flags include whether the device is a router or switch


def assessment_parse(line, regex):
    """Checks whether or not line has a match, if it does returns all matches in the line."""
    for item in regex:
        if re.search(item, line) is None:
            pass
        else:
            return re.findall(item, line)


# TODO create regex to search each line for various bad things
# single uplinks
# old version
# bad routing
# statically set interfaces
# excessive ACLs
# database of EOL switches/routers

# TODO create function to list port configuration. Specifically find trunk ports to review access creep
# Should search through the lines, add the interface name to a list if it is trunked.

# TODO open the files in a directory and punt it over to the regex searches
def find_files(directory, filetype):
    """Searches a directory and sub-directories for all filenames with the specified filetype. Returns a list of
    filenames within those directories.
    """
    all_files_list = []
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in [f for f in filenames if f.endswith(filetype)]:
            all_files_list.append(os.path.join(dirpath, filename))
    return all_files_list


def file_open(file):
    """Takes input file, opens it, reads it line by line, then parses with regexes. Returns a list of any matches."""
    all_config_matches = []
    with open(file) as read_file:
        for line in read_file:
            all_config_matches.append(assessment_parse(line, bad_configs))
    cleaned_list = config_match_cleanup(all_config_matches)
    return cleaned_list


def config_match_cleanup(match_list):
    """Takes a list full of None's and actual data, returns a list without None entries."""
    cleaned_list = []
    for item in match_list:
        if item is not None:
            cleaned_list.append(item)
    return cleaned_list


# TODO output the searches to an output file


def main():
    """Takes command line arguments of <directory> <filetype> then searches for all files with that filetype. Returns
    a list of bad configurations.
    """
    list_of_files = find_files(argv[1], argv[2])
    for input_filename in list_of_files:
        pprint.pprint('Checking file: {0}'.format(input_filename))
        pprint.pprint(file_open(input_filename))


if __name__ == '__main__':
    main()

# Testing
########################################################################################################################
# print(file_open('2015-05-18-10.7.7.10-octobase-putty.log'))
