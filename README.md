Ansible Role InfluxDB
=====================

[![Build Status](https://travis-ci.org/juliendufresne/ansible-role-influxdb.svg?branch=master)](https://travis-ci.org/juliendufresne/ansible-role-influxdb)

Fully configurable [InfluxDB](https://influxdata.com/time-series-platform/influxdb/) installation and management.  
You can manage your users and databases with `influxdb_users` and `influxdb_databases` variables.

Supported platforms
-------------------

| Distribution           | Last check date     | From scratch    | Idempotency |
| ---------------------- | ------------------- | --------------- | ----------- |
| CentOS 7.2.1511 (Core) | 2016-08-06 18:40:07 | ![OK](https://img.shields.io/badge/status-pass-brightgreen.svg) | ![OK](https://img.shields.io/badge/status-pass-brightgreen.svg)  |
| Debian 7.10 (wheezy)   | 2016-08-06 18:41:39 | ![OK](https://img.shields.io/badge/status-pass-brightgreen.svg) | ![OK](https://img.shields.io/badge/status-pass-brightgreen.svg)  |
| Debian 8.4 (jessie)    | 2016-08-06 18:43:44 | ![OK](https://img.shields.io/badge/status-pass-brightgreen.svg) | ![OK](https://img.shields.io/badge/status-pass-brightgreen.svg)  |
| Ubuntu 12.04 (precise) | 2016-08-06 18:45:21 | ![OK](https://img.shields.io/badge/status-pass-brightgreen.svg) | ![OK](https://img.shields.io/badge/status-pass-brightgreen.svg)  |
| Ubuntu 14.04 (trusty)  | 2016-08-06 18:47:32 | ![OK](https://img.shields.io/badge/status-pass-brightgreen.svg) | ![OK](https://img.shields.io/badge/status-pass-brightgreen.svg)  |
| Ubuntu 15.04 (vivid)   | 2016-08-06 18:49:37 | ![OK](https://img.shields.io/badge/status-pass-brightgreen.svg) | ![OK](https://img.shields.io/badge/status-pass-brightgreen.svg)  |
| Ubuntu 15.10 (wily)    | 2016-08-06 18:51:39 | ![OK](https://img.shields.io/badge/status-pass-brightgreen.svg) | ![OK](https://img.shields.io/badge/status-pass-brightgreen.svg)  |
| Ubuntu 16.04 (xenial)  | 2016-08-06 18:53:35 | ![OK](https://img.shields.io/badge/status-pass-brightgreen.svg) | ![OK](https://img.shields.io/badge/status-pass-brightgreen.svg)  |

> _Table generated with [test-ansible-roles](https://github.com/juliendufresne/test-ansible-roles)_

Requirements
------------

This role requires ansible 2.1.0+ (apt_repository use filename)  

Module influxdb_user
--------------------

This role contains a module to manage your influxdb users.
It can:
- Ensure a user is present or absent
- create an admin user or a classic user
- manage user's database grants access (NO, READ, WRITE or ALL privileges)
- append your specified grants to the existing ones

For more information about this module, please see its [dedicated documentation](docs/module_influxdb_user.md)

> *Note:* You can use this module independently or via the variable `influxdb_users`

Role Variables
--------------

Every variables have default value. This role can be run with default configuration.

### global options

| Name                      | Description                           | Default         |
| ------------------------- |:------------------------------------- | --------------- |
| **influxdb_install_user** | Which user will be used to install.   | "root"          |
| **influxdb_user**         | InfluxDB user                         | "influxdb"      |
| **influxdb_group**        | InfluxDB group                        | "influxdb"      |
| **influxdb_config_dir**   | Where is located configuration files  | "/etc/influxdb" |
| **influxdb_config_file**  | Name of the configuration file        | "influxdb.conf" |
| **influxdb_users**        | Allow to manage users (see below)     | []              |
| **influxdb_databases**    | Allow to manage databases (see below) | ["_internal"]   |

**Managing users**

The `influxdb_users` variables gives the ability to manage users creation and rights management.
For each entry, the script will:
- create the user if it does not exists
- update the user password if it has changed
- give the admin role if the `type` is set to `admin`
- revoke any previously defined database rights
- gives the right specified to each database.

Example:
```yml
influxdb_users:
  - name: admin
    admin: yes
    password: admin
  - name: grafana
    password: grafana
    grants: "measurement:READ" # Gives READ access to the measurement table for user grafana
  - type: user
    name: telegraf
    password: telegraf
    grants: "measurement:WRITE" # Gives WRITE access to the measurement table for user telegraf
  - name: john
    password: john
    grants: "measurement:ALL" # Gives READ and WRITE access to the measurement table for user telegraf
```
_For safety reasons, it does not remove any databases._

**Managing databases**

Ensure databases listed in `influxdb_databases` are created.

Example:
```yml
influxdb_databases:
  - "_internal"
  - "grafana"
```
_For safety reasons, it does not remove any databases._

### Configuration file options

Each parameter in the configuration file may be specified.  
Variable format: `influxdb__<block-name>__<parameter_in_snake_case>`

To see all available parameters, see the [defaults variables](defaults/main.yml#L13) or the [influxdb.conf template](templates/influxdb.conf.j2)

Dependencies
------------

None.

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: servers
      roles:
         - { role: juliendufresne.influxdb }

License
-------

MIT / BSD

Author Information
------------------

This role was created in 2016 by [Julien Dufresne](http://www.juliendufresne.fr).
