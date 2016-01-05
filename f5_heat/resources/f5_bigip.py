# Copyright 2016 F5 Networks Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from f5.bigip.bigip import BigIP
from heat.common.i18n import _
from heat.engine import properties
from heat.engine import resource


class F5BigIP(resource.Resource):
    '''Holds BigIP server, username, and password.'''

    PROPERTIES = (
        IP,
        USERNAME,
        PASSWORD
    ) = (
        'ip',
        'username',
        'password'
    )

    properties_schema = {
        IP: properties.Schema(
            properties.Schema.STRING,
            _('IP address of BigIP device.'),
            required=True
        ),
        USERNAME: properties.Schema(
            properties.Schema.STRING,
            _('Username for logging into the BigIP.'),
            required=True
        ),
        PASSWORD: properties.Schema(
            properties.Schema.STRING,
            _('Password for logging into the BigIP.'),
            required=True
        )
    }

    def __init__(self, name, definition, stack):
        super(F5BigIP, self).__init__(name, definition, stack)
        try:
            self.bigip = BigIP(
                self.properties['ip'],
                self.properties['username'],
                self.properties['password']
            )
        except Exception as ex:
            raise Exception('Failed to initialize BigIP object: {}'.format(ex))

    def get_bigip(self):
        return self.bigip

    def handle_create(self):
        '''Create the BigIP resource.'''
        self.resource_id_set(self.physical_resource_name())

    def handle_delete(self):
        '''Delete BigIP resource.'''
        pass


def resource_mapping():
    return {'F5::BigIP': F5BigIP}