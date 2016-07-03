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
  - type: admin
    name: admin
    password: admin
  - type: user
    name: grafana
    password: grafana
    rights:
      - "measurement:READ" # Gives READ access to the measurement table for user grafana
  - type: user
    name: telegraf
    password: telegraf
    rights:
      - "measurement:WRITE" # Gives WRITE access to the measurement table for user telegraf
  - type: user
    name: john
    password: john
    rights:
      - "measurement:ALL" # Gives READ and WRITE access to the measurement table for user telegraf
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

| Name                                                          | Description | Default                        |
| ------------------------------------------------------------- |:----------- | ------------------------------ |
| **influxdb_config__meta__dir**                                |             | "/var/lib/influxdb/meta"       |
| **influxdb_config__meta__retention_autocreate**               |             | "true"                         |
| **influxdb_config__meta__logging_enabled**                    |             | "true"                         |
| **influxdb_config__meta__pprof_enabled**                      |             | "false"                        |
| **influxdb_config__meta__lease_duration**                     |             | "1m0s"                         |
| **influxdb_config__data__enabled**                            |             | "true"                         |
| **influxdb_config__data__dir**                                |             | "/var/lib/influxdb/data"       |
| **influxdb_config__data__wal_dir**                            |             | "/var/lib/influxdb/wal"        |
| **influxdb_config__data__wal_logging_enabled**                |             | "true"                         |
| **influxdb_config__data__data_logging_enabled**               |             | "true"                         |
| **influxdb_config__data__query_log_enabled**                  |             | "true"                         |
| **influxdb_config__data__cache_max_memory_size**              |             | 524288000                      |
| **influxdb_config__data__cache_snapshot_memory_size**         |             | 26214400                       |
| **influxdb_config__data__cache_snapshot_write_cold_duration** |             | "1h"                           |
| **influxdb_config__data__compact_min_file_count**             |             | 3                              |
| **influxdb_config__data__compact_full_write_cold_duration**   |             | "24h"                          |
| **influxdb_config__data__max_points_per_block**               |             | 1000                           |
| **influxdb_config__cluster__shard_writer_timeout**            |             | "5s"                           |
| **influxdb_config__cluster__write_timeout**                   |             | "10s"                          |
| **influxdb_config__cluster__max_concurrent_queries**          |             | 0                              |
| **influxdb_config__cluster__query_timeout**                   |             | "0s"                           |
| **influxdb_config__cluster__max_select_point**                |             | 0                              |
| **influxdb_config__cluster__max_select_series**               |             | 0                              |
| **influxdb_config__cluster__max_select_buckets**              |             | 0                              |
| **influxdb_config__retention__enabled**                       |             | "true"                         |
| **influxdb_config__retention__check_interval**                |             | "30s"                          |
| **influxdb_config__shard_precreation__enabled**               |             | "true"                         |
| **influxdb_config__shard_precreation__check_interval**        |             | "10m"                          |
| **influxdb_config__shard_precreation__advance_period**        |             | "30m"                          |
| **influxdb_config__monitor__store_enabled**                   |             | "true"                         |
| **influxdb_config__monitor__store_database**                  |             | "_internal"                    |
| **influxdb_config__monitor__store_interval**                  |             | "10s"                          |
| **influxdb_config__admin__enabled**                           |             | "true"                         |
| **influxdb_config__admin__bind_address**                      |             | ":8083"                        |
| **influxdb_config__admin__https_enabled**                     |             | "false"                        |
| **influxdb_config__admin__https_certificate**                 |             | "/etc/ssl/influxdb.pem"        |
| **influxdb_config__http__enabled**                            |             | "true"                         |
| **influxdb_config__http__bind_address**                       |             | ":8086"                        |
| **influxdb_config__http__auth_enabled**                       |             | "false"                        |
| **influxdb_config__http__log_enabled**                        |             | "true"                         |
| **influxdb_config__http__write_tracing**                      |             | "false"                        |
| **influxdb_config__http__pprof_enabled**                      |             | "false"                        |
| **influxdb_config__http__https_enabled**                      |             | "false"                        |
| **influxdb_config__http__https_certificate**                  |             | "/etc/ssl/influxdb.pem"        |
| **influxdb_config__http__max_row_limit**                      |             | 10000                          |
| **influxdb_config__graphite__enabled**                        |             | "false"                        |
| **influxdb_config__graphite__bind_address**                   |             | ":2003"                        |
| **influxdb_config__graphite__database**                       |             | "graphite"                     |
| **influxdb_config__graphite__protocol**                       |             | "tcp"                          |
| **influxdb_config__graphite__batch_size**                     |             | 5000                           |
| **influxdb_config__graphite__batch_pending**                  |             | 10                             |
| **influxdb_config__graphite__batch_timeout**                  |             | "1s"                           |
| **influxdb_config__graphite__consistency_level**              |             | "one"                          |
| **influxdb_config__graphite__separator**                      |             | "."                            |
| **influxdb_config__graphite__udp_read_buffer**                |             | 0                              |
| **influxdb_config__graphite__tags**                           |             | []                             |
| **influxdb_config__graphite__templates**                      |             | []                             |
| **influxdb_config__collectd__enabled**                        |             | "false"                        |
| **influxdb_config__collectd__bind_address**                   |             | ":25826"                       |
| **influxdb_config__collectd__database**                       |             | "collectd"                     |
| **influxdb_config__collectd__batch_size**                     |             | 5000                           |
| **influxdb_config__collectd__batch_pending**                  |             | 10                             |
| **influxdb_config__collectd__batch_timeout**                  |             | "10s"                          |
| **influxdb_config__collectd__read_buffer**                    |             | 0                              |
| **influxdb_config__collectd__typesdb**                        |             | "/usr/share/collectd/types.db" |
| **influxdb_config__opentsdb__enabled**                        |             | "false"                        |
| **influxdb_config__opentsdb__bind_address**                   |             | ":4242"                        |
| **influxdb_config__opentsdb__database**                       |             | "opentsdb"                     |
| **influxdb_config__opentsdb__retention_policy**               |             | ""                             |
| **influxdb_config__opentsdb__consistency_level**              |             | "one"                          |
| **influxdb_config__opentsdb__tls_enabled**                    |             | "false"                        |
| **influxdb_config__opentsdb__certificate**                    |             | "/etc/ssl/influxdb.pem"        |
| **influxdb_config__opentsdb__batch_size**                     |             | 1000                           |
| **influxdb_config__opentsdb__batch_pending**                  |             | 5                              |
| **influxdb_config__opentsdb__batch_timeout**                  |             | "1s"                           |
| **influxdb_config__opentsdb__log_point_errors**               |             | "true"                         |
| **influxdb_config__udp__enabled**                             |             | "false"                        |
| **influxdb_config__udp__bind_address**                        |             | ":8089"                        |
| **influxdb_config__udp__database**                            |             | "udp"                          |
| **influxdb_config__udp__retention_policy**                    |             | ""                             |
| **influxdb_config__udp__batch_size**                          |             | 5000                           |
| **influxdb_config__udp__batch_pending**                       |             | 10                             |
| **influxdb_config__udp__batch_timeout**                       |             | "1s"                           |
| **influxdb_config__udp__read_buffer**                         |             | 0                              |
| **influxdb_config__udp__udp_payload_size**                    |             | 65536                          |
| **influxdb_config__continuous_queries__log_enabled**          |             | "true"                         |
| **influxdb_config__continuous_queries__enabled**              |             | "true"                         |
| **influxdb_config__continuous_queries__run_interval**         |             | "1s"                           |


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
