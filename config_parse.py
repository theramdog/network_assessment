__author__ = 'Zachary Hill'

import re
import os
from sys import argv

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
    for item in regex:
        if re.search(item, line) is None:
            pass
        else:
            print(re.findall(item, line))


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
    all_files_list = []
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in [f for f in filenames if f.endswith(filetype)]:
            all_files_list.append(os.path.join(dirpath, filename))
    return all_files_list


def file_open(file):
    with open(file) as read_file:
        for line in read_file:
            assessment_parse(line, bad_configs)


# TODO output the searches to an output file


def main():
    list_of_files = find_files(argv[1], argv[2])
    for input_filename in list_of_files:
        print('Checking file: {0}'.format(input_filename))
        file_open(input_filename)


#if __name__ == '__main__':
#    main()

# Testing
########################################################################################################################
file_open('2015-05-18-10.7.7.10-octobase-putty.log')
