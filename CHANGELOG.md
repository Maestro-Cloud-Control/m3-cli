# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.116.8] - 2024-07-19
* Implement error handling for `'NoneType' object has no attribute 'get'` issue
in `dstorquota` and `dinquota` commands. Update system to display user-friendly
message for enhanced user experience.

## [3.116.7] - 2024-06-17
* Refactor code and handle `Invalid JSON format`. This applies to the following
commands:
  * `apply-terraform-template`, `plan-terraform-template`
  * `upload-terraform-template`, `upload-terraform-template-from-git`

## [3.116.6] - 2024-05-31
* Add functionality to use JSON file with variables for commands
 Supported types for JSON file: STRING, LIST, MAP, NUMBER, BOOL
 Supported types for console: STRING, LIST, MAP
 This applies to the following commands:
  * `apply-terraform-template`, `plan-terraform-template`
  * `upload-terraform-template`, `upload-terraform-template-from-git`
* Add functionality to use parameter `--variables` for commands:
  * `upload-terraform-template`, `upload-terraform-template-from-git`
* Add `lock-terraform-template`, `prolong-terraform-template-lock`,
`unlock-terraform-template` commands to `group` with name `terraform-management`
* Improve code readability and add typing in `docs_generator.py`
* Fix typos in help
* Update help for all commands according to this rule: use `.` between sentences,
but do not use it at the end of the entire help message

## [3.116.1] - 2024-05-14
* Fix import for `m3 prolong-terraform-template-lock` command
* Remove `--description` as a parameter from the following commands and 
implement it as an auto-generated description:
  * `m3 lock-terraform-template`
  * `m3 prolong-terraform-template-lock`
  * `m3 unlock-terraform-template`

## [3.116.0] - 2024-05-09
* Add commands:
  * `m3 lock-terraform-template`
  * `m3 prolong-terraform-template-lock`
  * `m3 unlock-terraform-template`

## [3.112.4] - 2024-04-08
* Add `--tag` parameter alias `-tag` to `m3 run-instances` command

## [3.112.3] - 2024-04-05
* Improve readability of commands: 
  * m3 upload-script --help, m3 describe-script --help, m3 delete-scripts --help

## [3.112.2] - 2024-04-02
* Implement fixes related to commands `m3 delete-scripts` and `m3 upload-scripts`:
  * Change `"maestro-user-identifier"` from `SYSTEM` to `UNKNOWN`
  * Fix `"api_param_name"` for command `m3 delete-scripts`
  * Remove `.` from the list of allowed symbols for the `-scname` parameter in 
  `m3 upload-scripts` command
  * Enhance help documentation for `m3 upload-scripts` command

## [3.112.1] - 2024-04-01
* Add `--script` parameter alias `-scname` to `m3 run-instances` command

## [3.112.0] - 2024-03-19
* Update the `payload` to include `dtoList` and `serviceName` in
`get_interactivity_option` method for the action `VALIDATE_SERVICE_VARIABLES`
in the `m3 activate-platform-service` command

## [3.101.11] - 2024-03-15
* Add command `m3 billing-region-types`
* Improve the table view for the `m3 billing-region-types --table` command.

## [3.101.10] - 2024-02-14
* Update of the `m3 mreport` command: 
  * Add optional parameter `--include-billing-source`

## [3.101.8] - 2024-01-29
* Fixed typo in the command `disassociate-ip`

## [3.101.7] - 2024-01-17
* Fix and update `m3 plantlp` and `m3 applytpl` commands:
  * The `-var` field can take multiple values, examples are also given
  * The `-var` field works according to the help and examples provided

## [3.101.6] - 2023-12-14
* Remove the `resource-group` parameter from command `delete-storage`.
  * Command no longer requests or requires resource group information.

## [3.101.5] - 2023-12-07
* Update `README.md` to fix images not displaying on `PyPI`.

## [3.101.4] - 2023-12-06
* Update of the `m3 mreport` command: 
  * Now the `tenant-region` parameter is by default converted to upper case.

## [3.101.3] - 2023-12-04 
* Add:
  * Metadata 'description' and 'long_description' (sourced from README.md).
  * Specified 'long_description_content_type' as markdown.
  * Project 'url' field pointing to GitHub repository in metadata.

## [3.101.2] - 2023-12-01
* Update command `m3 mreport --help`:
  * Disable validation for the `region` parameter
  * Update help text for the `region` parameter

## [3.101.1] - 2023-11-28
* Fix deprecated `pkg_resources`

## [3.101.0] - 2023-11-22
* Add `--tenant-group` parameter to `multitenant-report`
* Add `ANNUAL` option to `--report-type` parameter to `multitenant-report`

## [3.97.8] - 2023-10-04
* Requests signature changed(maestro-user-identifier added to the signature)

## [3.97.7] - 2023-10-03
* Fixed m3 mreport command example in full-help

## [3.97.6] - 2023-09-29
* Fixed m3 mreport command. Updated the plugin for extending the request body 
with parameter ‘format: EMAIL’.

## [3.97.5] - 2023-09-27
* Fixed setuptools warning about unknown parameter `app`

## [3.97.4] - 2023-09-24
* Update libraries to support Python 3.10:
  * `certifi` from 2021.10.8 to 2023.7.22
  * `cffi` from 1.15.0 to 1.15.1
  * `chardet` from 3.0.4 to 4.0.0
  * `idna` from 2.7 to 3.4
  * `pyparsing` from 3.0.8 to 3.1.1
  * `urllib3` from 1.24.3 to 1.26.16
  * `cryptography` from 39.0.1 to 41.0.3
  * `packaging` from 21.0 to 21.3
  * `tabulate` from 0.8.9 to 0.9.0

## [3.97.3] - 2023-09-19
* Added possibility to show an original response from the server via flag `--raw`.

## [3.97.2] - 2023-09-12
* up `requests` version to `2.31.0`
* up `Pillow` version to `10.0.0`
* up `setuptools` version to `68.2.1`
* up `pyyaml` version to `6.0.1`
* Updated the required Python version to 3.10.11

## [3.97.1] - 2023-08-30
* up tabulate version to `0.9.0`

## [3.97.0] - 2023-08-16
* Add new commands [SFTGMSTR-7042]:
  * `allocate-ip`:
  * `release-ip`:
  * `describe-ip`:
  * `describe-vlans`:
  * `deactivate-vlan`:
  * `activate-vlan`:
  * `move-to-vlan`:
  * `associate-ip`:
  * `diassociate-ip`:


## [3.93.0] - 2023-07-05
* Add additional message about update needed in case if user use outdated version and 
don`t have a credentials file yet [EPMEOOS-4943] 

## [3.85.1] - 2023-05-19
* MacOS build improvements: rename `m3cli.py` to `m3.py`, improve root dir path resolving

## [3.85.0] - 2023-04-20
* Rework encryption and decryption flow for interaction with M3 Server via RabbitMQ
* Raise "cryptography" library version up to 39.0.1

## [3.76.2] - 2022-12-23
* Fix typo in `decrypt-password` command response

## [3.76.1] - 2022-12-23
* Add ability to interact multiple users with tool via `--path` parameter in 
`m3 access` which  store credentials for different Maestro environment
* Fix an error associated with inability to view `decrypt-password` output 
in JSON format

## [3.76.0] - 2022-12-22
* Fixed an error associated with inability to decrypt encoded password in 
`decrypt-password` command

## [3.71.2] - 2022-10-28
* Refactor plugin for `describe-insights` command due to changes on BE side 

## [3.71.1] - 2022-09-30
* Added the processing of the `LOG_PATH` environment variable for storing 
  logs by the custom path. Changed the default path of the storing logs 
  on the Linux-based VMs to the 
  `/var/log/<app_name>/<user_name>/<app_name.log>`path. [SFTGMSTR-6234]

## [3.71.0] - 2022-09-12
* Add `--owner` parameter to `describe-instances` command which allows get 
instances by provided owner

## [3.63.2] - 2022-07-05
* Add validation for 'tag' parameter in `m3 describe-instances` command. 
Restrict describing instances by tag command to only one value [SFTGMSTR-6091]

## [3.63.1] - 2022-06-30
* Add new commands [SFTGMSTR-6059]:
  * `describe-insights`:
    * --cloud *
    * --region *
    * --tenant *
    * --instance-id *
    * --availability-zone
    * --resource-group
  * `describe-resources`:
    * --region *
    * --tenant *
    * --group
    * --tag

## [3.63.0] - 2022-06-23
* Fix autocomplete installation 
* Added two commands`enable-autocomplete` and `disable-autocomplete`
* Update command `describe-instances` by new parameters [SFTGMSTR-6059]:
  * insights
  * risk-factor
  * group
* Fix resource-tag parameter structure in output request [SFTGMSTR-6059]

## [3.60.9] - 2022-05-20
* Fixed the type of the `integration_suffix` value in the validation_service

## [3.60.8] - 2022-05-04
* Fix request structure for `publish-platform-service` command by taking out 
flag `allTenants` from `platformService` layer 

## [3.60.7] - 2022-05-03
* Make logs messages more detailed when processing request to make them more clear 
* Fix error associated with the 'list assignment index out of range' in case 
using the `disable_numparse` parameter and set empty value to the column in the 
`set-tags` command

## [3.60.6] - 2022-04-26
* Fixed display of `email` column in the `describe-keypair` command - it will be shown only when 
there are other users’ key-pairs in the response [SFTGMSTR-5770]
* Added the `status` field to response in the `describe-keypair` command [SFTGMSTR-5770]

## [3.60.5] - 2022-04-22
* Added the CI/CD documentation for m3cli
* Made parameters in the import- and create-keypair commands consistent [SFTGMSTR-5769]

## [3.60.4] - 2022-04-21
* Fixed incorrect typing in help messages
* Add command groups that link the commands with template-related notifications of Maestro: 
  * the group on stack destroying notification [SFTGMSTR-5826]
  * the group on platform service deleted notification [SFTGMSTR-5827]
* Fixed the groups on run template approved/rejected notifications [SFTGMSTR-5821]

## [3.60.3] - 2022-04-18
* Add command groups that link the commands with template-related notifications of Maestro: 
  * the group on template planned successfully notification [SFTGMSTR-5820]
  * the group on template applied successfully notification [SFTGMSTR-5819]
  * the group on template action failed notification [SFTGMSTR-5818]
  * the groups on run template approved/rejected notifications [SFTGMSTR-5821]
  
## [3.60.2] - 2022-04-13
* Add command groups that link the commands with template-related notifications of Maestro: 
  * the group on template publish notification [SFTGMSTR-5737]
  * the group on template diagnostics notifications [SFTGMSTR-5738]
  * the group on template validation successfully notification [SFTGMSTR-5739]

## [3.60.1] - 2022-04-04
* Add command groups that link the commands with template-related notifications of Maestro. [SFTGMSTR-5717]

## [3.60.0] - 2022-03-21
* Fixed output responses in the `describe-tags`, `set-tags` commands
* Fixed the `delete-tags` command due to the changes on BE side
* Unified the `api_action` parameters for tag related commands
* Renamed the `tag` parameter in the `delete-tags` command to `tag-key`, also
renamed the `tag` alias to `key`
* Updated command groups to display cli commands in 
upload/update/remove template notifications in the
`commands_def.json` file [SFTGMSTR-5717] 

## [3.55.14] - 2022-03-07
* Fix plugin name for command `describe-terraform-stacks`
* Fix error associated with the inability to execute commands in case 
of the absence of the `max_value` value when validating the value of  the parameters.
If the Max_value doesn't exist. This value up to 10 digits long by default.

## [3.55.13] - 2022-02-14
* Fix error associated with inability to install tool due to absent backward 
compatibility

## [3.55.12] - 2022-02-07
* Added tests for plugins:
  * test-delete-storage
  * tet-delete-tags
  * test-describe-events
  * test-describe-keys
  * test-describe-platform-services
* Update `command_schema` in `validation_service.py`

## [3.55.11] - 2022-02-04
* Fix plugin name for command `describe-terraform-templates`
* Renamed the all volume-related parameters from `-volume` to `-storage` in the following commands: [SFTGMSTR-5432]
  * `describe-storages`, `delete-storage`, `detach-storage`, `set-tags`: 
    * renamed the `volume-id` parameter to `storage-id`;
    * renamed the `vid` alias to `storid` of the `storage-id` parameter
* Renamed the following commands and parameters: [SFTGMSTR-5432]
  * the `delete-volume-quota` to `delete-storage-quota` and alias from `delvolquota` to `delstorquota` 
  * the `describe-volume-quota` to `describe-storage-quota` and alias from `getvolquota` to `dstorquota` 
  * the `create-volume-quota` to `create-storage-quota` and alias from `cvolquota` to `cstorquota` 
  * the `volume-amount` parameter of the `create-storage-quota` to `storage-amount`
  * the `volume-max-size` parameter of the `create-storage-quota` to `storage-max-size` and the `volsize` alias to `storsize`
* Fixed incorrect typing the volume words to storage words in help messages of the storage-related commands and parameters [SFTGMSTR-5432]

## [3.55.10] - 2022-01-28
* Changed the `--output_file_path` parameter in customizer.py to optional [SFTGMSTR-5407]
* Added tests for services:
  * `varfile_service.py`
  * `interactive_input_service.py`
  * `parameters_provider.py`
  * `remote_validation_service.py`
* Added tests for utils:
  * `interactivity_utils.py`
  * `cloud_utils.py`
* Added alias to `webhook` parameter in `upload-terraform-template-from-git` command

## [3.55.9] - 2022-01-25
* Integrate CLI test suite into GitLab CICD [SFTGMSTR-5260]
* Added tests for plugins:
  * `add-schedule-instances.py`
  * `apply-terraform-template.py`
  * `azure-management-console.py`
  * `activate-platform-service.py`
  * `add-service-section.py`
  * `aws-management-console.py`
* Added tests for services:
  * `aes_cipher_service.py`
  * `commands_service.py`
  * `environment_service.py`
  * `plugin_service.py`
  * `request_service.py`
  * `response_processor_service.py`
  * `response_utils.py`
  * `validation_service.py`
  * `create-schedule.py`
  * `deactivate-platform-service.py`
  * `delete-schedule-instances.py`
  * `delete-service-section.py`
* Implement script for configuring commands_def.json, more about [script](m3cli/customizer/README.md) [SFTGMSTR-5261]
* Added the `ALL` value to the validation of the `supported-cloud` parameter in the `publish-platform-service` command
* Added a parameter `--all-tenants`, `-AT` to the`publish-platform-service` command. Register service for all tenants of the customer [SFTGMSTR-5150]
* Made region names with prefix `GGL-` available for `decrypt-password` and `delete-storage` commands

## [3.55.8] - 2022-01-21
* Delete the obsolete `related_commands` attribute from the following commands in commands_def.json:
  * `describe-instances`
  * `create-schedule`
  * `delete-schedule`
* Added the `access-permission` group to the `groups` list in commands_def.json
* Included to `access-permission` group the following commands:
  * `health-check`
  * `describe-user-permissions`
* Added the following changes to README.md:
  * added the `integration_suffix` description to the `commands_def.json` schema
* Fixed an error associated with an inability to create custom response from empty fields in command `describe-storages`

## [3.55.7] - 2022-01-19
* Updated the `api_pram_name` for the following parameters of the `delete-service-section` command:
  * `--delete-all` from `allBlocks` to `deleteAllBlocks`
  * `--delete-empty` from `emptyTitle` to `deleteBlockWithoutTitle`
* The help functionality is now always available, regardless of availability of the server.
* Fixed resolving of related commands in the `full-help` messages. 
  Previously, some commands were added to a list of related commands by mistake.
* Rollback alias name pattern from `-ds*` to `-d*` for the following describe commands:
  * `describe-events` `-dev`
  * `describe-instances` `-din`
  * `describe-platform-service-stacks` `-dplstack`
  * `describe-platform-services` `-dplservice`
  * `describe-images` `-dim`
  * `describe-storages` `-dstor`
  * `describe-schedules` `-dsch`
  * `describe-script` `-dscript`
  * `describe-keys` `-dkey`
  * `describe-terraform-templates` `-dtpl`
  * `describe-terraform-stacks` `-dterstack`
  * `describe-tenants` `-dtn`
  * `describe-regions` `-dr`
  * `describe-shapes` `-dsh`
  * `describe-tags` `-dtag`
  * `describe-instance-quota` `-dinquota`
  * `describe-user-permissions` `-duserperm`
* Renamed the `volume-name` parameter to `name` and alias from `vname` to `n` in the `create-attach-storage` command
* Fix typos in the CHANGELOG file in [3.55.5] - 2022-01-18 
* The `display-name` parameter to `name` in the `add-schedule-instances` command, also renamed the alias from `dn` to `n`
* Renamed the `section-name` parameter to `section` and alias from `sename` to `sec` in the `add-service-section` command
* renamed the `s` alias to `sh` of the `shape` parameter in the `price` command
* renamed the `shname` alias to `sh` of the `shape` parameter in the `run-instances` command
* Renamed aliases of the `--description` parameters to `-d` in the following commands:
  * `update-platform-service` also renamed the alias of the `--summary-description` parameter from `-sdes` to `-sd`
  * `publish-platform-service` also renamed the alias of the `--summary-description` parameter from `-sdes` to `-sd`

## [3.55.6] - 2022-01-18
* The `describe-events` command has the following changes:
  * the `--region` parameter is required
  * the `--number-of-events` parameter is optional. Default value is 10. Added information about it to the command help
  * header displayed in the following sequences: Resource Id, Initiator, Group, Description, Date, Event Id
  * the `--resource-id` parameter is required in case RELATED search type is specified
  * renamed the `de` alias of the command to `dsev`

## [3.55.5] - 2022-01-18
* Renamed the `instance-ids` parameter to `instance-id` and alias from `iids` to `iid` in the `describe-instance` command
* Renamed all `tenant-name` parameters to `tenant`
* Renamed all `service-name` parameters to `service`  and aliases from `sname` to `sn`
* Renamed all `template-name` parameters to `template` and aliases from `tempname` to `tpl`
* Renamed all `script-name` parameters to `script` and aliases from `sname` to `scname`
* The `publish-service` command has the following changes:
  * renamed the `categories` parameter to `category`
* Renamed the `list-of-tenant-names` parameter to `tenant-list` and alias from `ltn` to `tnl` in the `describe-tenants` command
* The `update-platform-service` command has the following changes:
  * renamed the `categories` parameter to `category`
  * renamed the `ttype`  alias to `tpltype` of the `template-type` parameter
* Renamed the `temptype`  alias to `tpltype` of the `template-type` parameter in the `list-platform-service-definitions` command
* The `run-instance` command has the following changes:
  * renamed the `instance-name` parameter to `name`, also renamed the alias from `iname` to `n`
  * renamed the `image-name` parameter to `image`
  * renamed the `shape-name` parameter to `shape`
  * renamed the alias from `key` to `kname` in the `key-name` parameter
* Renamed the `volume-ids` parameter to `volume-id` and alias from `vids` to `vid` in the `describe-volumes` command
* Renamed the `resource-group-name` parameter to `resource-group` in the `delete-volume` command
* The `create-schedule` command has the following changes:
  * renamed the `list-instances` parameter to `instance-id` and alias from `inst` to `iid`
* The `set-tags` command has the following change:
  * renamed the `resource-group-name` parameter to `resource-group`
  * renamed the `volume-ids` parameter to `volume-id` and alias from `vids` to `vid`
  * renamed the alias `settag` to `stag`
* Renamed the `clouds-list` parameter to `cloud` and alias from `clist` to `c` in the `total-report` command
* Renamed the `product-name` parameter to `product` in the `cost-object-report` command
* The `upload-script` command has the following changes:
  * renamed the `file-path` parameter to `source-path` and alias from `fpath` to `spath`
* The `delete-script` and `describe-script` commands have the following changes:
  * renamed the `file-path` parameter to `source-path` and alias from `fpath` to `source`
  * renamed the `file-name` parameter to `script`
* Renamed the `image-name` parameter to `name` and alias from `imname` to `n` in the `create-image` command
* Renamed the `variables` parameter to `variable` in the `terraform-plan-template`, `apply-terraform-template` commands
* Renamed the `list-of-template-names` parameter to `template` and alias from `ltempnames` to `tpl`  in the `terraform-describe-template` command
* Renamed the `stack-ids` parameter to `stack-id` and alias from `stackids` to `stid` in `terraform-describe-stack`, `terraform-destroy-stack` commands
* The `create-keypair` command has the following changes:
  * renamed the `all` alias of the `all-tenants` parameter to `AT`
* The `publish-platform-service` command has the following changes:
  * the `clouds-list` parameter to `supported-cloud`, also renamed the alias from `clist` to `supcloud`
  * the `product-version` parameter to `service-version` in the `publish-platform-service`, `update-platform-service` commands, also renamed the alias from `productv` to `servicev`
* Renamed the following values:
  * the alias of the `section` parameter from `sname` to `sename` in the `add-service-section` command
  * the `file-name` parameter to `script` in the `describe-script` command, also renamed the alias from `sname` to `scname`
  * the `reviewers` parameter to `approver`, also renamed the `rev` alias to `apr` in the `upload-terraform-template-from-git`, `upload-terraform-template` commands
  * the `approval-rule` parameter to `approval-policy` in the `terraform-upload-template` and `terraform-upload-template-from-git` commands, also renamed the alias from `apvlrule` to `aprpolicy`
  * the `max-size` parameter to `volume-max-size` in the `create-volume-quota` command, also renamed the alias from `msize` to `volsize`
  * the `creation-interval-count` parameter to `volume-amount` in the `create-volume-quota` command, also renamed the alias from `count` to `amount`
  * the `cloud-list` parameter to `supported-cloud` in the `update-platform-service` command, also renamed the alias from `clist` to `supcloud`
  * the `expire-after` parameter to `destroy-after` in the `activate-platform-service` command, also renamed the alias from `exp` to `expire`
  * the `creation-interval-count` parameter to `instance-amount` in the `create-instance-quota` command, also renamed the alias from `count` to `amount`
  * the `tags` parameter to `tag` in the `delete-tags`, `set-tags` commands, also renamed the alias from `tags` to `tag`
  * the `display-name` parameter to `name` in the `delete-schedule-instances`, `create-schedule`, `delete-schedule` commands, also renamed the alias from `dn` to `n`
  * the `section-name` parameter to `section`, in the following commands:
    * `describe-service-section`
    * `delete-service-section`
  * the `keypair-name` parameter to `key-name`, also renamed the alias from `kpname` to `kname` in the following commands:
    * `import-keypair`
    * `update-keypair-region`
    * `describe-keypair`
    * `delete-keypair`
    * `create-keypair`
  * renamed the `dim` alias to `dsim` in the `describe-images` command
  * renamed the `dtn` alias to `dstn` in the `describe-tenants` command
  * renamed the `dr` alias to `dsr` in the `describe-regions` command
  * renamed the `dsh` alias to `dssh` in the `describe-shapes` command
  * renamed the `dscr` alias to `dsscript` in the `describe-scrip` command
  * renamed the `getinstq` alias to `dsinquota` in the `describe-instance-quota` command
  * renamed the `getvolq` alias to `getvolquota` in the `describe-volume-quota` command
  * renamed the `delinstq` alias to `delinquota` in the `delete-instance-quota` command
  * renamed the `delvolq` alias to `delvolquota` in the `delete-volume-quota` command
  * renamed the `cvolq` alias to `cvolquota` in the `create-volume-quota` command
  * renamed the `cinstq` alias to `cinquota` in the `create-instance-quota` command
  * renamed the `dpfs` alias to `dsservice` in the `describe-platform-service` command
* Renamed the following commands:
  * the `create-keypair` command to `create-key`
  * the `describe-keypair` command to `describe-keys` and alias from `dkey` to `dskey`
  * the `import-keypair` command to `import-key`
  * the `delete-keypair` command to `delete-key`
  * the `update-keypair-region` command to `manage-key` and alias from `ukey` to `mkey`
  * the `terraform-describe-template` command to `describe-terraform-templates` and alias from ` terdt` to `dstpl`
  * the `terraform-apply-template` command to `apply-terraform-templates` and alias from ` terapt` to `applytpl`
  * the `terraform-delete-template` command to `delete-terraform-template` and alias from `terdl` to `deltpl`
  * the `terraform-plan-template` command to `plan-terraform-template` and alias from `terpt` to `plantpl`
  * the `terraform-export-template` command to `export-terraform-template` and alias from `exptemp` to `exptpl`
  * the `terraform-upload-template` command to `upload-terraform-template` and alias from `uptemp` to `upltpl`
  * the `terraform-upload-template-from-git` command to `upload-terraform-template-from-git` and alias from `uptempgit` to `upltplgit`
  * the `terraform-describe-stack` command to `describe-terraform-stacks`  and alias from `terds` to `dsterstack`
  * the `terraform-destroy-stack` command to `destroy-terraform-stack` and alias from `terdes` to `dtrterstack`
  * the `publish-service` command to `publish-platform-service` and alias from `pubs` to `pubservice`
  * the `remove-service` command to `delete-platform-service` and alias from `dels` to `delservice`
  * the `set-tag` command to `set-tags`
  * the `describe-tag` command to `describe-tags` and alias from `dtag` to `dstag`
  * the `delete-tag` command to `delete-tags`
  * the `create-attach-volume` command to `create-attach-storage` and alias from `addattvol` to `addattstor`
  * the `detach-volume` command to `detach-storage` and alias from `detvol` to `detstor`
  * the `describe-volumes` command to `describe-storages` and alias from `dvol` to `dsstor`
  * the `delete-volume` command to `delete-storage` and alias from `delvol` to `delstor`
  * the `terminate-instance` command to `terminate-instances`
  * the `stop-instance` command to `stop-instances`
  * the `run-instance` command to `run-instances`
  * the `start-instance` command to `start-instances`
  * the `reboot-instance` command to `reboot-instances`
  * the `describe-instance` command to `describe-instances`  and alias from `din` to `dsin`
  * the `delete-script` command to `delete-scripts`
* Updated the "Commands definition file" paragraph in README.md
* Fixed output for `describe-volumes` command, now nullable values are visible
* Updated the help message in the `--cron` parameter of the `create-schedule` command
* Added the ability to change the name of the output headers in all commands
* The headers in the table format convert to Title Case automatically
* Fixed an incorrect ordering of commands in the "Related commands" section of full-helps

## [3.55.4] - 2022-01-17
* Added ability to remove all blocks in the `delete-service-section` command
* The `delete-service-section` command has the following changes:
  * added new parameter `--delete-all -A`. A flag. Deletes all blocks in a section
  * added new parameter `--delete-empty -E`. A flag. Deletes all text in section without titles
* The `block-title` parameter of the `delete-service-section` command is optional
* Set a flag for displaying extended help message (`--full-help`) for the `delete-tag`, `delete-service-section` commands
* Commands `describe-platform-service` and `list-platform-services` was merged to `describe-platform-service-stacks` with following parameters:
  * `--cloud`, `-c`, * The cloud
  * `--tenant`, `-tn`, * The tenant name
  * `--region`, `-r`, * The region name
  * `--service`, `-sname`, The service name
  * `--service-id`, `-sid`, Service ID
  * `--all`, `-A`, A flag. If specified, the services activated in all tenants of the current customer are displayed
* Commands `describe-platform-service-definition` and `list-platform-service-definitions` was merged to `describe-platform-services` with the following parameters:
  * `--cloud`, `-c`,
  * `--tenant`, `-tn` Displaying the list of the available platform services in the tenant
  * `--service`, `-sname` Displaying the list of the available platform services by service name
 Displaying current platform services by template type
  * `--template-type`, `-tpltype` [CLOUD_FORMATION, TERRAFORM]

## [3.55.3] - 2022-01-11
* Fixed empty rows in response of the `describe-tags` command.
* Added a new command `describe-user-permissions` that lists a set of permission groups available to a user
  for the given tenant and environment.

## [3.55.2] - 2022-01-10
* Fixed the error of a missing plugin for the `describe-platform-service-definition` command. 

## [3.55.1] - 2022-01-06
* Fixed an error that removed attributes with `False` and `0` values in the JSON-view when the `nullable`
  option was specified in the output configuration of the command (.e.g., `describe-instance` command).

## [3.55.0] - 2022-01-04
* Refactored the code for interactive mode.
* Changed the format of dates to ISO 8601 in output of the following commands:
  * activate-platform-service
  * cost-object-report
  * create-image
  * create-schedule
  * describe-events
  * describe-images
  * describe-platform-service
  * describe-schedules
  * describe-tenants
  * resource-report
  * subtotal-report
  * total-report
  * untagged-resource-report
* Changed the formatting of list attributes in output. Now, in table view list values are 
  aligned in column (one under another).

## [3.50.18] - 2021-12-15
* Extended the response of the `describe-instance` command for `json` and `full` view, added `memoryGb`, `storageGb` and `cpuCount` fields. 

## [3.50.17] - 2021-12-10
* Changed the format of dates in output of the `terraform-describe-stack` command to ISO 8601.

## [3.50.16] - 2021-12-09
* Shortened the description of `generate-platform-service-varfile` command.

## [3.50.15] - 2021-12-08
* Unified response for `set-tag`, `delete-tag` and `describe-tag` commands.
* The `describe-service-section` and `delete-service-section` commands were implemented.

## [3.50.14] - 2021-12-07
* Changes to the command `activate-platform-service`:
  * Added the `interactive-mode` optional parameter for explicit activation of interactive mode.
  * Interactive mode now activates on either of two conditions:
    * The `interactive-mode` flag is explicitly provided.
    * Default value is not configured for at least one of the service parameters.
  * Added the `variables-file` parameter that allows to provide service parameters in a form of a file.
* Added a new `generate-platform-service-varfile` command. It generates a template of a variables file to use with 
  the `activate-platform-service` command. Alternatively, it extends an existing variables file with missing variables.
* Reverted changes made to the `terraform-upload-template` command by mistake in the `3.50.13` version.

## [3.50.13] - 2021-12-06
* Merged commands related to public and private tags management into the next - `set-tag`, `delete-tag` and `describe-tag`.

## [3.50.12] - 2021-11-30
* Changes to `describe-schedules` command:
  * The `schedule-type` parameter is made optional.
  * The `region` is no longer shown in output if it is provided as input parameter.
* Datetime changes:
  * Made all CLI responses show datetime in UTC timezone.
* Simplify CLI commands:
  * Removed `need-review` param from `terraform-upload-template` and `terraform-upload-template-from-git` commands;
  * Removed `resource-group-name` and `availability-zone` params from `create-schedule` command;
  * Removed some particular output table headers from those commands where the same params are required to input.
    Mostly `region`, `cloud` and `tenantName` output attributes were removed;
  * Made `import-keypair` command show in output only importing status message instead of the attributes the server returns.
* Added the ability to process the parameters of the `list` type by the `case` value

## [3.50.11] - 2021-11-29
* Fixed validation for `resource-report` command

## [3.50.10] - 2021-11-25
* Fixed an error associated with an inability to display the empty response
* Added the processing of empty response in the `subtotal-report` command
* Added the displaying  of the `tenantGroup` value in the `describe-tenants` command
* Renamed the `inactive` alias of the `inactive` parameter in the `price` command to `N`
* Renamed the `all` alias of the `all-tenants` parameter in the `create-keypair` command to `AT`
* Renamed the `report-format` parameter in all commands to `report` also renamed alias from `rf` to `R`
* The `report-format` parameter has been converted to a flag in the following commands:
  * `cost-object-report`
  * `cost-usage-report`
  * `resource-report`
  * `subtotal-report`
  * `total-report`
  * `untagged-resource-report`
  * the processing of it also has been added in plugins
* The `cost-usage-report` command has the following changes:
  * command sends the report only by email
  * command sets the `AWS` value for the `cloud` parameter automatically

## [3.50.9] - 2021-11-24
* Improved resolving of a parent domain parameter. Now, a command parameter can inherit 
  a domain parameter under a different name and override a subset of its attributes.
* Added 2 response headers in `describe-instance` command 
  * `instanceStopDate`
  * `instanceTerminationDate`
* Added ability to set tags for several instances, now it is possible to specify several values for `instance-id` parameter.
* Added validation of the `region` parameter to the `multitenant-report` command
* Removed the `template-type` parameter from the `publish-service` command.
  Now, the type of template is determined automatically.

## [3.50.8] - 2021-11-22
* Improved `describe-tenants` command, added ability to show parent tenant for the linked tenant.
* Added validation for allowed values of `cloud-list` parameter for `publish-service` command.
* The `run-instance` command has the following changes:
  * The command is now working via the approval process. If instance-related quotas are depleted, 
    the instances will require a tenant-manager approval to be run. The approvals are based on notifications.
  * Added a new `additional-storage` parameter.
  * The output is changed. Now, it shows a status of the processed run-instance request and a details message.
* Replaced the `tenant-name` parameter with the `tenant-group` for `hourly-report`, `resource-report`, `subtotal-report` and `total-report` commands.

## [3.50.7] - 2021-11-17
* Implemented `terraform-upload-template-from-git` command.

## [3.50.6] - 2021-11-17
* The `multitenant-report` command has the following changes:
  * Renamed the `--target-name` parameter to `--region` in the `multitenant-report` command
  * The `--region` parameter may be specified for all values of the `report-type` parameters
* Added ability to set tags for several instances, now it is possible to specify several values for `instance-id` parameter.
* Added “required parameters missing” error message in case of command execution without any parameters

## [3.50.5] - 2021-11-12
* Added environment specific allowed values of the parameters for `hourly-report`,`total-report`,`resource-report` and `subtotal-report` commands.

## [3.50.4] - 2021-11-11
* The `publish-service` commands have the following changes:
  * made the `icon-path` parameter optional
  * improved descriptions for the `cloud` and `tenant-name` parameters
* Added to output the `templateType` value in the `list-platform-service-definitions` command

## [3.50.3] - 2021-11-08
* Fixed outdated cli distribution links in the prompt to update the m3-cli.

## [3.50.2] - 2021-10-28
* Added `_headers_customization_func` to `response_processor_service.py` with parameters:
  * `disable_numparse`
* Changed the `commands_def.json` :
  * deleted all `extra_headers` and moved them into headers
  * added optional parameter `headers_customization`

## [3.50.1] - 2021-10-15
* Added an optional property to the command definition object (listed in `commands_def.json`) named as `integration_suffix`.
  * In case the property is specified, m3cli should build the plugin name according to the following pattern:
${command_name}_${integration_suffix}.py

## [3.50.0] - 2021-10-13
* Added two optional parameters to `run-instance` command:
  * `stop_after`
  * `terminate_after`
  
## [3.45.43] - 2021-11-02
* Fixed `access` command for case when `api_address` parameter is not specified and api address for prod env should be set by default.

## [3.45.42] - 2021-10-26
* The `tenant-name` parameter has become optional in the` description-keypair` command
* The `publish-service` command had the following changes:
  * the `tenant-name` parameter is required
  * the `cloud` parameter is required

## [3.45.41] - 2021-10-21
* Updated the allowed values of the cloud providers in all commands  
* Added the `NUTANIX` cloud provider to allowed values
* Deleted the following cloud providers from `allowed values` as obsolete:
  * CSA
  * HPOO
  * EXOSCALE
* Changed the alias name in the following commands:
  * `describe-public-tag` from `dtag` to `dpvtag`
  * `describe-private-tags` from `dtag` to `dpubtag`

## [3.45.40] - 2021-10-19
* Added `nullable` flag to `price` command response parameters.
* The `update-keypair-region` command  had the following changes:
  * Added the `--all-regions` flag
  * Added the ability to send a list of regions
  * The `region` parameter isn't required if the `--all-regions` flag is specified
* Deleted the `owner` parameter from the following commands as obsolete:
  * `run-instance`
  * `create-image`

## [3.45.39] - 2021-10-12
* Added the `block-value-path` parameter to the `add-service-section` command. It provides an
  alternative way to specify a value of the block by using a file. 
* Changed the alias name of the `describe-public-tag` command to `dpubtag`
* Changed the alias name of the `describe-private-tag` command to `dprtag`

## [3.45.38] - 2021-10-11
* Added ability to follow order of headers according to 'commands_def.json'

## [3.45.37] - 2021-10-11
* Fixed typos and corrected terminology in commands' helps.

## [3.45.36] - 2021-10-07
* The `multiproject_report` command has the following changes:
  * Restored the `multiproject_report` command
  * Renamed  the `multiproject_report` command to `multitenant-report`
  * The following obsolete parameters were deleted from the `multitenant-report` command: 
    * `region`,
    * `cloud`,
    * `native-currency`,
    * `cloud-target`
  * Added the `target-name` parameter to the `multitenant-report` command
  * INACTIVE, UPSA_INACTIVE, ALL_PERSONAL, NOT_PMC, CUSTOMERS, UNITS, ADJUSTMENT types do not require additional parameters at all 
  * ACCOUNT type may accept the optional parameters – `account-id`
  * ACTIVE type may accept the optional parameters – `target-name`
* Updated the help field of the `terraform-version` parameter in the `terraform-upload-template` command

## [3.45.35] - 2021-10-07
* Added the `InstanceType` parameter to the `run-instance` command
* Added the ability to display `InstanceType` parameter in the `describe-instance` command

## [3.45.34] - 2021-10-05
* Added flag `inactive` for the `price` command to show price model for inactive resources.
* Made `from` and `to` parameters optional, added `shape` parameter to filter instance price model by shape name.

## [3.45.33] - 2021-10-01
* The `manage-termination-protection` command was implemented.
* There is the ability to enable or disable termination protection for AWS, Azure, and GCP instances.

## [3.45.32] - 2021-10-01
* Fixed validation for GCP cloud for `set-public-tag`, `describe-public-tag` and `delete-public-tag` commands.
* Made `errorMessage`, `instanceName` and `state` headers optional for `start-instance`, `stop-instance`, `reboot-instance` and `terminate-instance` commands.

## [3.45.31] - 2021-10-01
* The `update-platform-service` and `publish-service` commands have the following changes:
  * Renamed the alias name of the `template-name` parameter in the PaaS commands from `tname` to `tempname`;
  * Added the regex validation to the `provider-version` parameters

## [3.45.30] - 2021-09-30
* Changes to the `describe-schedules` command:
  * Removed the `instance-id` parameter as it was not in use;
  * Added the required `schedule-type` parameter;
  * Made the `region` parameter optional;
  * Removed the `cloud` and `tenant` attributes from output;
  * Added the `instances` and `tag` optional attributes to output.
* Added the `instance-ids` parameter to the `resource-report` command.
* Added the `summaryDescription` attribute to output of the `describe-platform-service-definition` command.
* Added the `clouds` and `categories` attributes to output of the `list-platform-service-definitions` command.

## [3.45.29] - 2021-09-28
* Added ability to show several tables in the command response.
* Use correct api action for the `price` command. Added validation about possible pricing types.

## [3.45.28] - 2021-09-28
* Added ability to show human-readable error in case of failed connection.

## [3.45.27] - 2021-09-23
* Fixed mistakes in request and response processing for commands with interactive options.

## [3.45.26] - 2021-09-23
* Changed parameters of report requests (`cost-object-report` and `untagged-resource-report`)
  to conform with Maestro API.

## [3.45.25] - 2021-09-22
* Added a file signature validation for images of PNG and JPEG types. 
  This change affects the `publish-service` and `update-platform-service` commands.

## [3.45.24] - 2021-09-21
* Renamed the output parameter `projectCode` to `tenantName` in the next commands: 
  * `cost-object-report`
  * `resource-report`
  * `untagged-resource-report`

## [3.45.23] - 2021-09-21
* Added ability to filter instances by their state

## [3.45.22] - 2021-09-20
* Provided ability to execute batch requests by adding the `batch_param` with value `true` to the certain command parameter.

## [3.45.21] - 2021-09-20
* Changed the request format for the `params` field in case of processing interactive mode from `key=value` to `key: value`
* The `run-instance` command has the following changes:
  * the `image-id` parameter renamed  to `image-name`
  * the alias `imid` of the parameter  renamed  to `imname`
* Fixed typos in the helps of commands and in command groups.
* Added command groups that link the commands with notifications of Maestro.

## [3.45.20] - 2021-09-14
* Added validation for case when `hidden` and `inactive` parameters specified in `describe-tenants` command.
* Made `tag-keys` parameter required for `delete-public-tag` command.

## [3.45.19] - 2021-09-09
* Improved generation of command help messages. Now, the commands are grouped by their scope.
  The "Related commands" section in help messages is dynamically generated based on the commands 
  that share the same group with the current command.
* Changed the maximum size of files for upload from 3 MB to 3.5 MB. 
  This affects the `upload-script` and `terraform-upload-template` commands.
* Removed the `content` column from the response of the `upload-script` command. 

## [3.45.18] - 2021-09-09
* Fixed the resolving m3-cli/m3cli/plugins/utils path 

## [3.45.17] - 2021-09-09
* The `decrypt-password` command was implemented, applicable for AWS and GCP
* Provided ability to pass the request parameters to the custom response in command plugin

## [3.45.16] - 2021-09-09
* The `update-platform-service` command has the following changes:
  * changed the alias name from `pver` to `providerv` in the `provider-version` parameter
  * changed the alias name from `pver` to `productv` in  the `product-version` parameter

## [3.45.15] - 2021-09-08
* Improved `describe-tenants` command, the `all` parameter was replaced with the `hidden`, 
  * it is possible to use `hidden` and `inactive` parameters separately and both

## [3.45.14] - 2021-09-08
* The `publish-service` command has the following changes:
  * the `operating-system` parameter was set as not `required`
  * the `delivery-method` parameter was set as not `required` and has the `Maestro` value by default
  * improved the descriptions for the following parameters:
    * `tenant-name`
    * `cloud`
* The function of encoding of the picture moved to the plugin_utilities.py file
* Added the Regex validation for `terraform-version` parameter in the terraform-upload-template command
* Added the ability to specify default values for required command parameters in the
  `m3.properties` file in the user's current working directory. Default values from the
  `m3.properties` file take precedence over default values from the `default.cr` file
  in the user's home directory.
* Removed the `path` parameter from the `access` command as obsolete.
* Removed the `M3CLI_PARAMETER_SET_NAME` environment variable as obsolete.
    
## [3.45.13] - 2021-09-07
* Fixed the interactive options if no default fields are available
* The `create-keypair` command has following changes:
  * the `access_key` and `secret_key` write to the local file to the `%HOME/.m3cli/keys/` path by default
  * added the ability to specify the `path` to save keys

## [3.45.12] - 2021-09-06
* Commands `describe-public-tag` and `delete-public-tag` was implemented, the `set-public-tag` command was improved:
 * by default command will add new tag instead of overwriting existing, added `overwrite` flag to make it possible overwrite existing tags

## [3.45.11] - 2021-09-06
* Added the following parameters to the `publish-service` command:
  * `tenant-name` - the tenant display name
  * `cloud` - the cloud provider
* Renamed the following alias in the `publish-service` command:
  * from `pver` to `providerv`;
  * from `pver` to `productv`

## [3.45.10] - 2021-09-03
* Improved the `create-keypair` command to make it possible use it with `all-tenants` flag which allows to create key pair for all tenants, 
  also made it possible to combine it with `cloud` or `tenant-name` name parameter

## [3.45.9] - 2021-09-03
* Change output in the `deactivate-platform-service` in case of the successful response
* Changed the output of error in case of not getting parameters in the interactive mode

## [3.45.8] - 2021-09-03
* Changed logic of `resource-report` command that does not allow to provide 
  `--region` and `--cloud-list` parameters together

## [3.45.7] - 2021-09-01
* Added a `script-name` parameter to `upload-script` command. Now, the name of the script is
  defined by this parameter, not by the name of the file in the `file-path` parameter.
* Changed a maximum allowed size of a file to 3 MB in the following commands:
  * `upload-script` - `file-path` parameter;
  * `terraform-upload-template` - `file-path` parameter;
  * `publish-service` - `icon-path` parameter;
  * `update-platform-service` - `icon-path` parameter.

## [3.45.6] - 2021-08-30
* Fixed to encode the icons in `publish-service`, `update-platform-service` commands

## [3.45.5] - 2021-08-26
* Added the `platformService` request wrapper for the next commands:
   * `publish-service`
   * `update-platform-service`
* Fixed the work of request wrapper in the `create-schedule` command

## [3.45.4] - 2021-08-23
* Added `--instance_id` parameter to `hourly-report` command
* Changed log path to: `$"HOME_PATH"/.m3cli/log/m3cli.log`

## [3.45.3] - 2021-08-20
* Added the new command: `update-platform-service`
* Implemented descriptions to the next commands:
  * `publish-service`
  * `remove-service`
  * `add-service-section`
  * `update-platform-service`
  * `cost-object-report`
  * `cost-usage-report`
  
## [3.45.2] - 2021-08-19
* Implemented `cost-object-report`
* Improved `resource-report` and `untagged-resource-report` commands:
  * Added `clouds-list` optional parameter to `resource-report` command
  * Pass `tagged` api param with `True` value for `resource-report` and `False` for `untagged-resource-report`

## [3.45.1] - 2021-08-12
* Implemented descriptions to the next commands:
  * `list-platform-service-definitions`
  * `list-platform-services`
  * `terraform-upload-template`
  * `terraform-export-template`
  * `terraform-describe-stack`
  * `terraform-plan-template`
  * `terraform-apply-template`
  * `terraform-destroy-stack`
* Deleted the `email` parameter from the next commands:
  * `terraform-plan-template`
  * `terraform-describe-stack`
  * `terraform-destroy-stack`
  * `update-keypair-region`
  * `upload-script`
* Added possibility to specify and add to the commands `interactive options`
  that will be used as a part of request to the server. More info can be found in the README.md
* Refactored command `activate-platform-service`. Now it uses `interactive options` for parameter `--params`
* Added new commands: `publish-service`, `remove-service`, `add-service-section`
* Added new required module `Pillow==8.3.1`
* Provided ability to store user credentials in the home directory
* Moved the logic of setup autocomplete to separate file not to do it during cli installation
* Made the `api_address` optional, use the default endpoint if not specified

## [3.45.0] - 2021-08-13
* Removed `user-email` parameter from `terraform-delete-template` command 
* Removed `task-initiator-email` parameter from `terraform-apply-template` command 

## [3.41.17] - 2021-08-10
* Improvements to validation of input parameters:
  * Introduced validation of files for uploads. Currently, there are three validation rules that check a file
    by its size, name, and extension.

## [3.41.16] - 2021-08-10
* Added new commands:
  * `list-platform-service-definitions` - shows all available platform services in the given location
  * `list-platform-services` - shows active platform services in the given location
  * `terraform-upload-template` - uploads the given Terraform template to Maestro with the specified parameters
  * `terraform-export-template` - prints a URL that can be used to access and download the requested Terraform template
  * `terraform-describe-stack` - shows details of stacks that were created in the given location
* Changes to the `terraform-destroy-template` command:
  * Renamed to `terraform-destroy-stack`
  * Added a new optional parameter `stack-id` to allow a destruction of a specific stack.
    If the parameter is omitted, the command behaves as before, destroying all stacks that were created 
    from the given template
* Changes to the `terraform-describe-stack` command:
  * Removed a `tenantName` from the command's output
  * Added `lastModificationDate` to the command's output

## [3.41.15] - 2021-08-10
* Corrected command's descriptions, in the case when using `--full-help`
* Fixed the bugs with the saving logs to the directory
* Implemented descriptions to the next commands:
  * volumes management:
    * `create-attach-volume`
    * `detach-volume`
    * `delete-volume`
  * console management:
    * `aws-management-console`
    * `azure-management-console`
    * `google-management-console`
  * report:
    * `untagged-resource-report`
    * `cost-usage-report`
* Fixed output for `describe-instance-quota` if response contains 0. It will display number, not an empty string

## [3.41.14] - 2021-08-09
* Moved `hidden` parameter from `describe-regions` to `describe-tenants` command
* Added `all` parameter to `describe-tenants` command to include hidden regions to response

## [3.41.13] - 2021-08-06
* Implemented the next commands for volumes management:
 * `create-attach-volume`
 * `detach-volume`
 * `delete-volume`
* Provided ability to use extra-columns in the table response

## [3.41.12] - 2021-08-04
* Fixed error related to missing help message in `describe-instance` command
* Renamed `run-instances` to `run-instance` command due to mismatching in naming convention
* Improved descriptions for commands in Maestro CLI.Improve descriptions for commands in Maestro CLI 

## [3.41.11] - 2021-08-03
* Removed `schedule-owner` from `create-schedule` command due to it unnecessary
* Renamed commands listed below due to mismatching in naming convention:
  * `describe-instances` -> `describe-instance`
  * `reboot-instances` -> `reboot-instance`
  * `start-instances` -> `start-instance`
  * `get-instance-quota` -> `describe-instance-quota`
  * `get-volume-quota` -> `describe-volume-quota`
  * `stop-instances` -> `stop-instance`

## [3.41.10] - 2021-08-03
* Removed `email` parameter because it is unnecessary from commands listed below:
  * `delete-keypair`
  * `describe-keypair`
  * `hourly-report`
  * `resource-report`
  * `delete-script`
  * `describe-script`
  * `subtotal-report`
  * `cost-usage-report`
  * `untagged-resource-report`
  * `import-keypair`
  * `create-keypair`
  * `total-report`
* Added range validation from 1 to 100 for `number-of-events` parameter in `describe-events` command
* Fixed error in report commands related to removing `from` and `to` parameters from request
* Hid the private part of the key in the command `create-keypair`

## [3.41.9] - 2021-08-02
* Reworked `managment-console` command for commands listed below for AWS, Azure, GCP:
  * `aws-management-console`
  * `azure-management-console`
  * `google-management-console`
* Fixed output for `describe-volumes` and `total-report` commands, now nullable values are visible
* Added cron validating for `create-schedule` command
* Added tag validation for `total-report`, `subtotal-report`, `resource-report`, `hourly-report` command
* Added `cost-usage-report` command which displays report for cost and usage optimization
* Added minimal value validation for `creation-interval-hours` and 
  `creation-interval-count` parameter in  `create-instance-quota` command
* The parameter `description` was made required in the command `create-image`
* Fixed typo in the `help` line in `stop-instance` command
* The parameters `cloud`, `tenant-name`, `region` were made required in the commands `create-keypair` and `import-keypair` 
* Fixed the problem with output the command `create-keypair`, in case, when use parameter `--json`
* In command `create-keypair` added to output fields tenant, region
* In command `import-keypair` added to output fields tenant, cloud, region
* Added `allowed_values` for parameter `cloud` in `create-keypair`, `descrive-keypair` commands
* Added checking for empty parameters in commands for `--help`
* Added mapping of allowed value for relationship `cloud`-`access-type` in `management-console` command
* Fixed minimal value validation for number type

## [3.41.8] - 2021-07-29
* Added `untagged-resource-report` that allows to monitor untagged resource report
* Parameter `number-of-instances` in `run-instances` command changed to non required with 
default value equal 1
* Fixed case sensitivity in parameters that contain the `allowed_values` list
* Added upper case to the parameter of:
  * `action` to the `create-schedule` command
  * `access-type` to the `management-console` command
  * `search-type` to the `describe-events` command
  * `cloud` to the `terraform-delete-template` command 
  * `state` to the `update-keypair-region` command
  * `region` to the `hourly-report` command
* The `--verbose` parameter writes the command logs to the terminal 
* The environment variable `M3CLI_DEBUG` writes logs to the `m3cli.log` file that is stored by the path of `$HOME` directory both for NT and POSIX systems 
* Changed output format for logs when using the environment variable `M3CLI_DEBUG`

## [3.41.7] - 2021-07-27
* Marked hidden parameter as false for non-hidden regions in response of `describe-regions` command. 
* Set the `nullable` flag with the value `true` in `output_configuration` section for command in `commands_def.json` so as not to hide the `False` value for boolean.
* Changed `scheduleName` to `displayName` flag in commands `add-schedule-instances`, `delete-schedule`, `delete-schedule-instances`
* Provided ability to show `displayName` instead of `scheduleName` in commands: `create-schedule`, `describe-schedules`

## [3.41.6] - 2021-07-26
* Fixed an error in `describe-events` command related to plugin missing
* Added convert to upper or lower case in the parameters where it was missing:
  * describe-platform-service: region -> upper
  * total-report: email -> lower, tenant-name -> upper
  * subtotal-report: email -> lower, tenant-name -> upper
  * resource-report: email -> lower, tenant-name -> upper, region -> upper
  * hourly-report: email -> lower, tenant-name -> upper, email -> lower
  * describe-keypair: cloud -> upper, email -> lower
  * import-keypair: tenant-name -> upper, cloud -> upper
  * describe-events: region -> upper
  * create-keypair: cloud -> upper
  * terraform-describe-template: cloud -> upper
  * terraform-plan-template: cloud -> upper
  * terraform-apply-template: cloud -> upper
  * terraform-destroy-template: cloud -> upper
  * set-public-tag: cloud -> upper
* Changed alias of `describe-events` from `dawsse` to `de`
* Modified error message when command failed

## [3.41.5] - 2021-07-23
* Renamed the parameter name from `templateName` to `template-name` in the `terraform-apply-template` command.
* Renamed the alias for `template-name` parameter in the command `terraform-apply-template`: `temname` instead of `tempname`. Such refactoring was performed in other commands with similar aliases.
* Changed the name of boolean alias in `describe-regions`, `describe-tenants`.
* Updated the structure of the `commands_def.json` in `README.md` file
* Fixed typo in parameter name of `describe-regions` command: changed from `include-hidded` to `include-hidden`

## [3.41.4] - 2021-07-20
* Renamed `describe-aws-stack-events` command to `describe-events`, because it can describe events for different clouds
* Changed parameter `--full_help` to `--full-help` for complete help message
* Fixed the picture (red square) in README.md
* Added .creds directory in .gitignore file
* Updated the pictures (usage_sample) in README.md file
* Added the `api_param_name` field in the command parameters in the file `commands_def.json`. Its replaced the original name of the parameters in `commands_service.py` with the server parameters `api_param_name` when sending a request to the server
* The names of the command's parameters reduced to one single form with m3admin's commands
* Sorting templates in `terraform-describe-template` command is no longer case-sensitive

## [3.41.3] - 2021-07-13
* Removed obsolete command `multiproject-report`

## [3.41.2] - 2021-07-05
* Updated cryptography module version due to unstable OS backward compatibility: 3.1.1 -> 3.4.7 

## [3.41.1] - 2021-07-02
* Renamed the following commands:
  * `update-tag` to `set-public-tag`
  * `set-tag` to `set-private-tag`
  * `delete-tag` to `delete-private-tag`
  * `describe-tags` to `describe-private-tags`
* If the response is more than 70 characters long, it will be split for better readability  
* Reworked `create-keypair` default command output to tabular
* Reworked `createdDate` param in `describe-images` command from time stamp to human-readable IS0-8601
* Reworked format the number of decimals to print out only two decimal places
* Command `management-console` allowed only for AWS, AZURE, GCP clouds
* Renamed the following parameters:
  * `memory` to `memoryGb` in `describe-shapes` command
  * `maxSize` to `maxSizeGb` in `get-volume-quota` command

## [3.37.11] - 2021-06-22
* Fixed `describe-schedules` command - now it describes all schedules, not just the first one in the list
* Renamed parameters of the `create-schedule` command:
  * `--tag_value` to `--tagValue`
  * `--tag_key` to `--tagKey`
* The `--tagValue` and `--tagKey` parameters are now required for schedule type "My instances with tag" 
  for `create-schedule` command

## [3.37.10] - 2021-06-16
* Fixed creating request for `mreport` command

## [3.37.9] - 2021-06-15
* Removed walrus operator

## [3.37.8] - 2021-06-14
* Reworked the boolean parameters from key-value pairs to flags: 
  * The presence of a flag parameter is regarded as a `true` value;
  * The absence of a flag parameter is regarded as a `false` value.
* Improved the output of the `add-schedule-instances` and `delete-schedule-instances` commands
* Hid the `tenantState` from the response of the `describe-tenants` command
* Changes to the `describe-aws-stack-events` command:
  * Fixed validation of the `eventId` and `resourceId` parameters;
  * Removed the `AUTHORIZATION` value from the `searchType` parameter;
  * Dropped the `customerName` parameter.

## [3.37.7] - 2021-06-10
* Update variables format for `terraform-apply-template` and `terraform-plan-template` commands:
  * `--variables key:value` for a string;
  * `--variables key:"value1, value2, value3"` for a list; 
  * `--variables key1:"key2=value2"` for an object.
* Remove parameter `variables` for `terraform-destroy-template`
* Interface of `update-keypair-region` updated: parameters `region` and `cloud` have become required
* Modified `import-keypair` command

## [3.37.6] - 2021-06-09
* Use correct help for `tenantName` parameter
* Remove obsolete commands: `activate-service`, `describe-platform-service-availability`

## [3.37.5] - 2021-06-03
* Fixed output for report commands
* `cloud` parameter in command `import-keypairs` has become required
* `email` parameter in command `management-console` has become optional
* `scheduleOwner` parameter in command `create-schedule` has become optional
* Fixed issue with command's help that stores in the file `commands_help.py`
* Added parameter `region` to the command `subtotal-report`

## [3.37.4] - 2021-06-04
* interface of `describe-aws-stack-events` updated: parameter `tenant` is replaced with `tenantName`
* integration request of `describe-aws-stack-events` has been removed
* commands_def version 2.7

## [3.37.3] - 2021-06-03
* The logic for checking the latest version has been changed. Now the latest version will come from the server side and not be determined by m3cli itself

## [3.37.2] - 2021-06-02
* Fixed commands `create-instance-quota` and `create-volume-quota` - added plugins and improved output
* Made the parameter `--cloud` for the command `describe-regions` required

## [3.37.1] - 2021-05-31
* Fixed integration request and modified command output in `management-console` command

## [3.37.0] - 2021-05-28
* Switched to unified versioning. Each m3cli version will be created according to the following rule - maestro_version.sprint_number.cli_version. Example, current version is 3.37.0
* Added `access` command to autocomplete
* Fixed file path error in `access` command
* Fixed file path error in `upload-script` command

## [2.6.0] - 2021-05-27
* Added new commands:
  * `reboot-instance`
  * `start-intance`
  * `terraform-delete-template`
  * `terraform-destroy-template`
  * `terraform-apply-template`
  * `terraform-plan-template`
  * `create-image`
  * `delete-image`
  * `describe-aws-stack-events`
  * `update-keypair-region`
  * `create-keypair`
  * `import-keypair`
  * `delete-keypair`
  * `describe-tenants`
  * `describe-regions`
  * `describe-shapes`
  * `add-schedule-instances`
  * `delete-schedule-instances`
  * `update-tag`
  * `describe-script`
  * `create-instance-quota`
  * `get-instance-quota`
  * `remove-instance-quota`
  * `create-volume-quota`
  * `get-volume-quota`
  * `remove-volume-quota`
* `aws-management-console` is now renamed to `management-console`
* The parameter `--templateNames` of the `terraform-describe-template` command now accepts any file name. 
  If this parameter is empty, the full list of templates will be displayed.
* Now commands required parameters in help message are marked with an asterisk (*) instead of the word "REQUIRED".

## [2.5.0] - 2021-05-05
* Changed field `instanceType` to `shape` in the command `describe-instances`
* Added the message if the user enters an invalid instance id as parameter value and requests the output in 
  json format. Previously, `[]` were displayed
* Added new parameter `--path` for the command `m3 access`. It specifies the path where to store the credentials file.
* Added help for the command `m3 access`
* Added warning message for `health-check` command if user provides incorrect URL
* Added `m3 access` command for all commands help
* Added ability to specify `object` type parameters in the following form: `key:value`
* Added m3cli autocomplete that supports only Unix-based platforms (bash&zsh interpreters) 

## [2.4.1] - 2021-04-23
* Fixed plugin `activate-platform-service`
* Fixed saving credential path for non-interactive `m3 access` 

## [2.4.0] - 2021-03-19
* Fixed date output for the command `describe-schedules`
* Sorted commands in help in ascending alphabetical order
* Clarified help for report commands (tags examples)
* Added check for duplicate keys
* Fixed cloud parameter in `create-schedule` command
* Parameter `sheduleName` in `create-schedule` command was removed, `sheduleName` consists of `displayName` and `region`  
* Added validation for defis in full(--) and alias(-) options
* Added possibility to specify a region in `total-report` command
* Added possibility to specify a report format in `resource-report` command
* Added parameter `--full_help` for complete help message and `--help` parameter for abbreviated description
* Added possibility to set credentials non-interactively using the following command:
    ```
    m3 access --access_key {your_access_key} --secret_key {your_secret_key} --api_address {api_address} 
    ```
* Added version checking
* Removed `params_set.ini`. The default values are now stored in the credentials file in format `parameter: value`
* Added health-check after setting credentials using `m3 access`
* Added possibility to specify secured parameters in `commands_def.json`
* Added `--verbose` parameter to write logs in m3cli.log file
* `--reportUnit` option was removed from report commands and generates automatically
* `--fileName` parameter in `remove-script` command accept list of file names
* Updated the required Python version to 3.8+

## [2.3.0] - 2021-03-04
* Added command `m3 access` to set up M3 CLI tool credentials 
* Added possibility to specify the case for parameters value in the `commands_def.json`
* Added human-readable message in case of bad credentials
* Added human-readable message in case of empty response from the M3 SDK server  
* Fixed a bug when user can use in the command's syntax some marker of the parameter and do not specify the value of that parameter   
* Fixed some commands that worked with issues

## [2.2.0] - 2021-02-18
* Fix resolving command plugin in case of execution via command alias
* Add `version` attribute to `commands_def.json` file to specify commands 
  definition version
* Update `README.md` file with commands definition versioning rules
* Add version option to m3 that displays the version of the m3 tool and the 
  version of commands definition
* Changed commands definition according to SDK parameters changes

## [2.1.4] - 2020-12-08
* Fix tag wrapping into an object in create-schedule command

## [2.1.3] - 2020-12-08
* Fix color highlights

## [2.1.2] - 2020-11-30
* Added new commands:
    GET_TOTAL_BILLING_REPORT,
    GET_SUBTOTAL_BILLING_REPORT,
    GET_HOURLY_BILLING_REPORT,
    GET_RESOURCE_BILLING_REPORT,
    GET_MULTIPROJECT_BILLING_REPORT
* Added new parameter type 'bool'    
    
## [2.1.1] - 2020-11-04
* Added new commands;
* Add showing request/response in debug mode (passwords are masked)

## [2.1.0] - 2020-10-30
* Added plugin mechanism;
* Removed old bugs, added new;
* Improved README.md;

## [2.0.3] - 2020-10-19
* Improved README.md;
* Fixed data converting to use it in requests to the server;
* Fixed trouble with os.get_terminal_size().columns method;
* Added packing `params_set.ini` and `commands_def.json` to the M3CLI distribution zip file.

## [2.0.2] - 2020-10-13
* Added commands: create schedule, delete schedule, delete tag;
* Added possibility to wrap the parameters in the request; 
* Small bug fixes and improvements.

## [2.0.1] - 2020-09-28
* Small bug fixes and improvements: 

### Added
* Domain parameters (inheritance for the parameters)
* Command help showing on the errors;
* Logs only by ``--debug`` flag;
* Storing commands help strings into ``commands_help.py``;
* Possibility to show detailed server response with ``--json`` flag.


## [2.0.0] - 2020-09-24
Adaptation to or2 cli has been made: 

### Added
* Regex validation for `string` type;
* The `date` data type for command parameters;
* The `alias` attribute for commands and parameters; 
Paths in commands def file: 
    * `commands.$command_name.alias`;
    * `commands.$command_name.parameters.$parameters_name.alias`.
* The `--table`(default), `--full`, `--json` modes for output;
* Filtering of `None`, `0`, `[]`, `{}`, `False` in `--table (default)` and `--json` mode;
* Configurable response attributes to show in `--table` and `--json` modes;
Path in commands def file: 
    * `commands.$command_name.output_configuration.response_table_headers`(list);
* Added ability to unmap response using configurable key;
Path in commands def file: 
    * `commands.$command_name.output_configuration.unmap_key`(string);
* Added validation of m3cli meta.

## [1.0.0] - 2020-09-1
Initial version. See README. 
