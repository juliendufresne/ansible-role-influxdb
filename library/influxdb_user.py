#!/usr/bin/python

DOCUMENTATION = '''
---
module: influxdb_user
short_description: Manage influxdb users
description: []
version_added: "2.1"
author: "Julien Dufresne, @juliendufresne"
notes:
  - It does not delete non managed users. Please ensure to use state: absent to remove users
requirements: []
options:
  name:
    description:
      - Name of the user to add, remove or modify.
    required: true
  password:
    description:
      - set the user's password.
    required: true
  admin:
    description:
      - Whether the user is considered as an admin (i.e has all privileges) or not.
    required: false
    choices: [ "yes", "no" ]
    default: "no"
  grants:
    description:
      - "InfluxDB privileges string in the format: C(db:grants_type)"
      - "C(grants_type) should be one of ALL, WRITE, READ or NO"
    required: false
    default: null
  append_grants:
    description:
      - Append the privileges defined by grants to the existing ones instead of overwriting existing ones.
    required: false
    choices: [ "yes", "no" ]
    default: "no"
  state:
    description:
      - Whether the user should exist.  When C(absent), removes
        the user
    required: false
    choices: [ "present", "absent" ]
    default: "present"
'''
import re
from subprocess import check_output, check_call


VALID_PRIVS = frozenset(('NO', 'READ', 'WRITE', 'ALL'))

class InvalidPrivsError(Exception):
    pass

def user_exists(name):
    output = subprocess.check_output(["influx", "-execute", "SHOW USERS"]).split('\n')
    del output[0]
    for line in output:
        if re.match(r'^%s'%name, line):
            return True
    return False

def user_add(name, password, admin):
    command = "CREATE USER %s WITH PASSWORD '%s'" % (name, password)
    if admin:
        command += " WITH ALL PRIVILEGES"
    return subprocess.check_call(["influx", "-execute", command])

def user_delete(name):
    command = "DROP USER %s" % (name)
    return subprocess.check_call(["influx", "-execute", command])

# We have no way to check if the password has changed or not
def set_password(name, password):
    command = "SET PASSWORD FOR %s = '%s'" % (name, password)

def grants_unpack(grants):
    """ Take a grants string, typically passed as a parameter, and unserialize
    it into a dictionary, the same format as privileges_get() above. We have this
    custom format to avoid using YAML/JSON strings inside YAML playbooks. Example
    of a privileges string:
     mydb:WRITE,anotherdb:READ,yetanother:ALL
    """

    unpacked_grants = {}
    for item in grants.split(','):
        pieces           = item.split(':')
        current_database = pieces[0]
        current_grant    = pieces[1].upper()

        if current_database in unpacked_grants:
            if unpacked_grants[current_database] == current_grant:
                continue
            # NO is not compatible with any other rights
            if current_grant == 'NO' or unpacked_grants[current_database] == 'NO':
                other_grant = current_grant
                if current_grant == 'NO':
                    other_grant = unpacked_grants[current_database]
                raise InvalidPrivsError('Invalid privileges specified. You cannot define both grants NO and %s for database %s' % (other_grant, current_database))
            # In any cases, it should results in ALL. Here are the possible cases:
            # | output[pieces[0]] | pieces[1].upper() | results      |
            # | ----------------- | ----------------- | ------------ |
            # | ALL               | ALL               | not possible |
            # | ALL               | WRITE             | ALL          |
            # | ALL               | READ              | ALL          |
            # | WRITE             | ALL               | ALL          |
            # | WRITE             | WRITE             | not possible |
            # | WRITE             | READ              | ALL          |
            # | READ              | ALL               | ALL          |
            # | READ              | WRITE             | ALL          |
            # | READ              | READ              | not possible |
            current_grant = 'ALL'

        unpacked_grants[current_database] = current_grant
        if not unpacked_grants[current_database] in VALID_PRIVS:
            raise InvalidPrivsError('Invalid privileges specified: %s. Expects one of %s' % (unpacked_grants[pieces[0]], VALID_PRIVS))

    return unpacked_grants

def set_grant(username, database, grants):
    command = "GRANT %s ON %s TO %s" % (grants, database, username)
    if grants == 'NO':
        command = "REVOKE ALL ON %s FROM %s" % (database, username)

    return subprocess.check_call(["influx", "-execute", command])

def manage_grants(username, grants, append_grants, admin):
    databases = subprocess.check_output(["influx", "-execute", "SHOW DATABASES"]).split('\n')
    del databases[0]
    del databases[0]
    del databases[0]

    command = "SHOW GRANTS FOR %s" % (username)
    show_grants_output = subprocess.check_output(["influx", "-execute", command]).split('\n')
    del show_grants_output[0]

    existing_grants = {}
    search_str = "^((?:(?!\\t)\w)+)\\t.*(NO|READ|WRITE|ALL)"
    for item in show_grants_output:
        pieces = re.match(search_str.decode('utf-8'), item.decode('utf-8'), re.U)
        if pieces:
            existing_grants[pieces.group(1)] = pieces.group(2)

    changed = False
    for db in databases:
        if db == '':
            continue

        current_grant = 'NO'
        if db in existing_grants:
            current_grant = existing_grants[db]

        new_grant = 'NO'
        if db in grants:
            new_grant = grants[db]

            if append_grants:
                if current_grant == 'ALL':
                    new_grant = 'ALL'
                elif new_grant != 'ALL' and current_grant != 'NO' and current_grant != new_grant:
                    if new_grant == 'NO':
                        new_grant = current_grant
                    else:
                        new_grant = 'ALL'

        if current_grant != new_grant:
            set_grant(username, db, new_grant)
            changed = True

    return changed



from ansible.module_utils.basic import *

def main():
    module = AnsibleModule(
        argument_spec     = dict(
            name          = dict(required=True, type='str'),
            password      = dict(required=True, type='str'),
            state         = dict(default="present", choices=["absent", "present"]),
            admin         = dict(default=False, type='bool'),
            grants        = dict(default=None),
            append_grants = dict(default=False, type='bool'),
        ),
        supports_check_mode=True
    )
    name          = module.params["name"]
    password      = module.params["password"]
    state         = module.params["state"]
    admin         = module.boolean(module.params["admin"])
    grants        = module.params["grants"]
    append_grants = module.boolean(module.params["append_grants"])

    if grants is not None and grants != "":
        try:
            grants = grants_unpack(grants)
        except Exception:
            e = get_exception()
            module.fail_json(msg="invalid grants string: %s" % str(e))

    changed = False
    if state == "present":
        if not user_exists(name):
            user_add(name, password, admin)
            changed = True
        # We have no way to check if the password has changed or not
        # So we always update it
        set_password(name, password)
        if manage_grants(name, grants, append_grants, admin):
            changed = True

    elif state == "absent":
        if user_exists(name):
            user_delete(name)
            changed = True

    module.exit_json(changed=changed)


if __name__ == '__main__':
    main()
