Ansible Role InfluxDB
=====================

Fully configurable [InfluxDB](https://influxdata.com/time-series-platform/influxdb/) installation for Linux Debian.  
You can manage your users and databases with `influxdb_users` and `influxdb_databases` variables.

Requirements
------------

Tested with ansible 2.1.0  
Should work for ansible >= 1.9 (usage of `become` and `become_user`)

Role Variables
--------------

Please see all the available variables [here](defaults/main.yml).

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

BSD, MIT

Author Information
------------------

None for now.
