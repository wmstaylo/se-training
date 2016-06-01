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
Simple application that logs on to the Switch and configure ipv4 on the 
Interfaces.
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
                configure ipv4 on the Interfaces.'''
    creds = NX.Credentials('switch', description)
    args = creds.get()

    # Login to Switch
    session = NX.Session(args.url, args.login, args.password)
    resp = session.login()
    if not resp.ok:
        print('%% Could not login to Switch')
        sys.exit(0)

    #Ensure that  port as layer 3 mode
    int1 = NX.Interface('eth1/2')
    int2 = NX.Interface('eth1/3')
    
    # ConfigInterfacs object is used to configure multiple 
    # interfaces at a time (No need of multiple REST calls)
    # Note: Using Interface object also an interface can be configured
    config = NX.ConfigInterfaces()
    
    # Adding interfaces to be configured
    config.add_interface(int1)
    config.add_interface(int2)
    
    # Setting interface attributes 
    # Note: if attributes are not set, then default values will be used
    int1.set_admin_status('up')
    int1.set_layer('Layer3')


    # Push entire configuration to the switch
    # Note:To configure only one interface use int1.get_url() & int1.get_json()
    resp = session.push_to_switch(config.get_url(), config.get_json())
    if not resp.ok:
        print ('%% Could not push to Switch')
        print resp.text
        sys.exit(0)

    

    # Creating interface objects
    # Note: interfaces should be L3 interface
    int1 = NX.Interface('eth1/2')
    config = NX.ConfigInterfaces()
    

    
    # Create IPv4 instance
    ipv4 = NX.IP()
    
    # Enable ip directed broadcast on the interface
    ipv4.enable_directed_broadcast(int1)
    
    # Add interfaces
    ipv4.add_interface_address(int1, '192.168.60.1/24')
    
  #  print ipv4.get_url()
  #  print ipv4.get_json()
    resp = session.push_to_switch(ipv4.get_url(), ipv4.get_json())
    if not resp.ok:
        print ('%% Could not push to Switch.')
        print resp.text
        sys.exit(0)

    # Uncomment below to delete the resources
    '''
    # Delete IP route
    resp = session.delete(r1.get_delete_url())
    if not resp.ok:
        print ('%% Could not delete from Switch')
        print resp.text
        sys.exit(0)
   
    # Delete from interface
    resp = session.delete(ipv4.get_delete_url('eth1/2'))
    if not resp.ok:
        print ('%% Could not delete from Switch')
        print resp.text
        sys.exit(0)

    resp = session.delete(ipv4.get_url())
    if not resp.ok:
        print ('%% Could not delete from Switch')
        print resp.text
        sys.exit(0)
    '''


if __name__ == '__main__':
    main()