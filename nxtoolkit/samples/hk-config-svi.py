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
Simple application that logs on to the Switch and configure SVI.
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
    description = '''Simple application that logs on to the Switch
                    and configure SVI.'''
    creds = NX.Credentials('switch', description)
    args = creds.get()

    # Login to Switch
    session = NX.Session(args.url, args.login, args.password)
    resp = session.login()
    if not resp.ok:
        print('%% Could not login to Switch')
        sys.exit(0)

    # Enable inteface-vlan feature
        #Create Feature Base object
    feature = NX.Feature(session)

    feature.enable('interface-vlan')
    feature.enable('lacp')
    
    # Push entire configuration to switch
    resp = session.push_to_switch(feature.get_url(), feature.get_json())
    if not resp.ok:
        print('%% Error: Could not push configuration to Switch')
        print(resp.text)

    # Create ConfigureInterfaces to do multiple SVI configuration at a time   
    config = NX.ConfigInterfaces()
    
    # Create SVI objects providing vlans
    svi1 = NX.SVI('vlan300','up','configured from nxtoolkit')
    svi2 = NX.SVI('vlan301')
    
    # Add svis to the config
    config.add_svis(svi1)
    config.add_svis(svi2)
    
    # Push entire configuration to the switch
    # Note: Using svi1.get_url() and svi1.get_json() only one svi
    # configuration can be pushed to the switch
    resp = session.push_to_switch(config.get_url(), config.get_json())
    if not resp.ok:
        print ('%% Could not login to Switch')
        print resp.text
        sys.exit(0)

    #displaying data

    data = []
    svis = NX.SVI.get(session)
    for svi in svis:
        data.append((svi.id, svi.admin_st, svi.bw, svi.mtu,
                     svi.descr))

    # Display the data downloaded (Uncomment below 
    # lines to get the configured SVI)
    template = "{0:15} {1:15} {2:15} {3:15} {4:40}"
    print(template.format("  ID     " , " ADMIN ", " BANDWIDTH ",
                          " MTU   ", "  DESCR."))
    print(template.format("---------",  "-------", "-----------",
                          "------ ", "--------"))
    for rec in data:
        print(template.format(*rec))
    
    
    # Uncomment below lines to delete the created svi
    '''
    for id in [svi1]:
        resp = session.delete(svi1.get_delete_url(id))
        if not resp.ok:
            print ('%% Could not login to Switch')
            print resp.text
            sys.exit(0)
    '''


if __name__ == '__main__':
    main()
