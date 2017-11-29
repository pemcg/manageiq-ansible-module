#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) 2017, Alex Braverman <abraverm@redhat.com>
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
#

ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'supported_by': 'community',
    'status': ['preview']
}

DOCUMENTATION = '''
---
module: manageiq_key
version_added: "2.4"
description: |
    Create and import encryption key using the appliance_console_cli on
    ManageIQ.
short_description: Create and import ManageIQ encryption key.
author: "Alex Braverman Masis (@abraverm)"
requirements:
    - appliance_console_cli
options:
    fetch_key:
        description: |
            Should the encryption key be fetched from a remote ManageIQ
            appliance.
        default: False
    hostname:
        description: |
            remote ManageIQ appliance FQDN or IP to fetch the encryptyion
            key from.
    force_key:
        description: Forcefully create (overwrite) encryption key.
        default: False
    sshlogin:
        description: |
            SSH user name to login with when fetching from remote ManageIQ
            appliance.
        default: root
    sshpassword:
        description: |
            SSH password to login with when fetching from remote ManageIQ
            appliance.
        default: smartvm
'''

EXAMPLES = '''
- name: Fetch key from main ManageIQ server
  manageiq_key:
      fetch_key: true
      hostname: main.manageiq.redhat.com
      sshlogin: root
      sshpassword: smartvm
'''

RETURN = ''' # '''

from ansible.module_utils.basic import AnsibleModule
from os import path

CMD_NAME = '/usr/bin/appliance_console_cli'
VMDB = '/var/www/miq/vmdb'


def main():
    module = AnsibleModule(
        argument_spec=dict(
            fetch_key=dict(default=False, type='bool'),
            force_key=dict(default=False, type='bool'),
            hostname=dict(type='str'),
            sshlogin=dict(type='str'),
            sshpassword=dict(type='str', no_log=True),
        ),
        required_if=[
            ['fetch_key', True, ['hostname', 'sshlogin', 'sshpassword']]
        ]
    )

    cmd = CMD_NAME
    if module.params['fetch_key']:
        cmd += " --fetch-key=%s" % module.params['hostname']
        cmd += " --sshlogin={} --sshpassword={}".format(
            module.params['sshlogin'], module.params['sshpassword'])
    else:
        cmd += ' --key'

    if path.isfile(path.join(VMDB, 'certs', 'v2_key')):
        if module.params['force_key']:
            cmd += ' --force-key'
        else:
            module.exit_json(changed=False, stdoug='Key exists')

    result, env, err = module.run_command('/usr/bin/env')
    result, out, err = module.run_command(cmd)
    if err != '':
        if 'No such file or directory' in out:
            module.fail_json("Encryption key doesn't exists on host")
        module.fail_json(
            msg="Command'%s' Failed on '%s' with evironment '%s'" % (
                cmd, err, env))
    changed = True

    module.exit_json(changed=changed, cmd=cmd, stdout=out, stderr=err)


if __name__ == "__main__":
    main()
