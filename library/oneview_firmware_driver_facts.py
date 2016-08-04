#!/usr/bin/python

###
# Copyright (2016) Hewlett Packard Enterprise Development LP
#
# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
###

from ansible.module_utils.basic import *
from hpOneView.oneview_client import OneViewClient

DOCUMENTATION = '''
---
module: oneview_firmware_driver_facts
short_description: Retrieve facts about one or more of the OneView Firmware Drivers.
description:
    - Retrieve facts about one or more of the Firmware Drivers from OneView.
requirements:
    - "python >= 2.7.9"
    - "hpOneView"
author: "Bruno Souza (@bsouza)"
options:
    config:
      description:
        - Path to a .json configuration file containing the OneView client configuration.
      required: true
    name:
      description:
        - Firmware driver name.
      required: false
notes:
    - "A sample configuration file for the config parameter can be found at:
       https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/oneview_config-rename.json"
'''

EXAMPLES = '''
- name: Gather facts about all Firmware Drivers
  oneview_firmware_driver_facts:
    config: "{{ config_file_path }}"

- debug: var=oneview_firmware_drivers

- name: Gather facts about a Firmware Driver by name
  oneview_firmware_driver_facts:
    config: "{{ config_file_path }}"
    name: "Service Pack for ProLiant.iso"

- debug: var=oneview_firmware_drivers
'''

RETURN = '''
oneview_firmware_drivers:
    description: Has all the OneView facts about the Firmware Drivers.
    returned: always, but can be null
    type: complex
'''


class FirmwareDriverFactsModule(object):

    argument_spec = dict(
        config=dict(required=True, type='str'),
        name=dict(required=False, type='str')
    )

    def __init__(self):
        self.module = AnsibleModule(
            argument_spec=self.argument_spec,
            supports_check_mode=False
        )
        oneview_client = OneViewClient.from_json_file(self.module.params['config'])
        self.resource_client = oneview_client.firmware_drivers

    def run(self):
        name = self.module.params["name"]

        try:
            if name:
                result = self.resource_client.get_by('name', name)
            else:
                result = self.resource_client.get_all()

            self.module.exit_json(
                changed=False,
                ansible_facts=dict(oneview_firmware_drivers=result)
            )
        except Exception as exception:
            self.module.fail_json(msg=exception.message)


def main():
    FirmwareDriverFactsModule().run()


if __name__ == '__main__':
    main()
