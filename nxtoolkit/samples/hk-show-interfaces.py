#!/usr/bin/env python
################################################################################
#                                                                              #
# Copyright (c) 2015 Cisco Systems                                             #
# All Rights Reserved.                                                         #
#                                                                              #
#    Licensed under the Apache License, Version 2.0 (the "License"); you may   #
#    not use this file except in compliance with the License. You may obtain   #
#    a copy of the License at                                                  #
#                                                                              #
#         http://www.apache.org/licenses/LICENSE-2.0                           #
#                                                                              #
#    Unless required by applicable law or agreed to in writing, software       #
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT #
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the  #
#    License for the specific language governing permissions and limitations   #
#    under the License.                                                        #
#                                                                              #
################################################################################
"""
Simple application that logs on to the Switch and displays all
of the Interfaces.
"""
import sys
import nxtoolkit.nxtoolkit as NX


def main():
    """
    Main execution routine

    :return: None
    """
    # Take login credentials from the command line if provided
    # Otherwise, take them from your environment variables file ~/.profile
    description = '''Simple application that logs on to the Switch and 
                    displays all of the Interfaces.'''
    creds = NX.Credentials('switch', description)
    args = creds.get()

    # Login to Switch
    session = NX.Session(args.url, args.login, args.password)
    resp = session.login()
    if not resp.ok:
        print('%% Could not login to Switch')
        sys.exit(0)

    # Download all of the interfaces
    # and store the data as tuples in a list
    data = []
    interfaces = NX.Interface.get(session)
    for interface in interfaces:
        data.append((interface.attributes['if_name'],
                     interface.attributes['porttype'],
                     interface.attributes['adminstatus'],
                     interface.attributes['operSt'],
                     interface.attributes['speed'],
                     interface.attributes['mtu'],
                     interface.attributes['usage']))

    # Display the data downloaded
    template = "{0:17} {1:6} {2:^6} {3:^6} {4:7} {5:6} {6:9}"
   # print(template.format("INTERFACE", "TYPE", "ADMIN", "OPER",
     #                     "SPEED", "MTU", "USAGE"))
    #print(template.format("---------", "----", "------", "------",
    #                      "-----", "---", "---------"))
    #for rec in data:
    #    print(template.format(*rec))
    # For learning purpose, you can uncomment some of these.
    #print the contents of the data[]; since it is a list , we need to read one at a time
    #this will print the contents of the data list.  if  you want to print a particular value inside the tupple
    # you can reference it like this x[position in tuple]
    # if you want to know the  operation state, you need to look at 3
    #for x in data:
    #  print x
    #Hemant adds
    #print only the interfaces that are up
    #data is a list of tupples.  The 3 column has the  operations state of the interface
    data_up = [x for x in data if x[3] == "up"]
    for d in  data_up:
        print(template.format(*d))


if __name__ == '__main__':
    main()
