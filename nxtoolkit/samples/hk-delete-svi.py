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

    # Create ConfigureInterfaces to do multiple SVI configuration at a time   
    config = NX.ConfigInterfaces()
    
    # Create SVI objects providing vlans
    svi1 = NX.SVI('vlan301')
    
    # Add svis to the config
    config.add_svis(svi1)
    
    # Push entire configuration to the switch
    # Note: Using svi1.get_url() and svi1.get_json() only one svi
    # configuration can be pushed to the switch

    for id in [svi1]:
        resp = session.delete(svi1.get_delete_url(id))
        if not resp.ok:
            print ('%% Could not login to Switch')
            print resp.text
            sys.exit(0)



if __name__ == '__main__':
    main()
