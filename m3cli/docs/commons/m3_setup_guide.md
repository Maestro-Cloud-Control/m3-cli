# Introduction

`Maestro CLI`, also known as `M3-CLI`, is a robust command-line interface (CLI) tool designed to provide a powerful alternative to user interfaces (UI). 
It allows you to perform cloud infrastructure management operations, as well as manage related assets, by sending respective calls to Maestro cloud management platform.
In this guide, you’ll find all the resources you need to install, update, uninstall, and effectively use the Maestro CLI.

## Table of Contents

- [Setup Guide](#m3-cli-setup-guide)
   - [Install](#installation)
   - [Update & Healthcheck](#update)
   - [Uninstall](#uninstallation)
- [Usage Guide](#usage-guide)
   - [Configuration](#configuration)
   - [Usage Examples](#usage-examples)
   - [Developers Guide](#developers-guide)
- [Support](#support)
   - [How to Report an Issue](#how-to-report-an-issue)
   - [How to Communicate with the Support Team](#how-to-communicate-with-the-support-team)

We're here to help you every step of the way. If you encounter any issues or have any questions, don't hesitate to reach out to our [support team](#support).

{{ pagebreak }}

# M3-CLI Setup Guide

## Installation

### Pre-requisites

Before you start with the installation of `M3-CLI`, ensure you have **Python 3.10** and **pip** installed on your system. If not, follow the guides provided below:

- [Python3 Installation Guide for Windows](https://www.python.org/downloads/windows/)

- [Python3 Installation Guide for Linux](https://docs.python-guide.org/starting/install3/linux/#installing-python-3-on-linux)

- [Python3 Installation Guide for Mac](https://docs.python-guide.org/starting/install3/osx/#installing-python-3-on-mac-os-x)

### Installation flow

> 💡 **Tip:** It's recommended to use a virtual environment to protect against dependency breakage. You can perform `m3cli` tool installation without this step, but if you want to install the tool to the created virtual environment, you will need to activate the virtual environment with installed M3CLI before using it.

#### Windows

🔗 [Guide for virtualenv installation](https://docs.python-guide.org/dev/virtualenvs/#lower-level-virtualenv)

Create:
```console
virtualenv -p python3 venv
```

Activate: 
```console
venv\Scripts\activate.bat
```

#### Linux/Mac

🔗 [Guide for virtualenv installation](https://docs.python-guide.org/dev/virtualenvs/#lower-level-virtualenv)

Create:
```console
virtualenv -p python3 .venv
```

Activate:
```console
source .venv/bin/activate
```

**To install `M3-CLI` tool use the command listed below installation command.**

```console
pip install m3-cli
```

## Update

### Pre-requisites

The updated version of `M3-CLI` assumes that you have **Python 3.10** and **venv** installed as a best practice, along with `M3-CLI` inside it.

### CLI Update Detection Flow

Once a day when any of the CLI commands is invoked, CLI performs a check for an available update.
It includes making a `m3 health-check` call to the server and using its response to refresh 
the data stored in the `default.cr` file about the latest CLI version and distribution links.

This data is used between the daily update checks to notify a user of a pending update 
while avoiding the need to communicate with the server on each request.

An update notification is printed to the user first before the actual response, and contains 
instructions of how to update the CLI client on a Linux, Windows or macOS machine.

If the `m3 health-check` call fails due to a server-side error while CLI performs a daily update check, 
a warning is printed informing the user of the error and that CLI is unable to automatically check for updates.

To force CLI to check for an update, invoke the `m3 health-check` command manually.

#### Windows

The updates require the following commands:
```console
pip list
pip install m3-cli==3.120.0
```

#### Examples:

```console
(venv) C:\Maestro3\m3-cli>pip list                
Package            Version
------------------ --------
attrs              23.2.0
...
m3-cli             3.101.10
...
(venv) C:\Maestro3\m3-cli>pip install m3-cli==3.120.0
...
Installing collected packages: m3-cli
  Attempting uninstall: m3-cli
    Found existing installation: m3-cli 3.101.10
    Uninstalling m3-cli-3.101.10:
      Successfully uninstalled m3-cli-3.101.10
Successfully installed m3-cli-3.120.0
```

Next step is to check if it works well by using the following commands:
```console
m3 --help
m3 health-check
```

If the `M3-CLI` version is outdated:

```console
(venv) C:\Maestro3\m3-cli>m3 health-check               
================================================================================
You are using an outdated version of m3-cli (3.101.10). Version 3.120.0 is now available. 
Please use the next link to download cli for Linux - https://mcc.cloud.epam.com/cli/3.101.10/m3-cli-x86_64.AppImage
To upgrade cli on macOS run the following command: pip install https://mcc.cloud.epam.com/cli/3.101.10/m3-cli-3.101.10.zip,
For windows run: pip install https://mcc.cloud.epam.com/cli/3.101.10/m3-cli-3.101.10.zip
================================================================================

Response:
+-------------------+---------+-------------+------------+---------------------+
| Server Available  | Mails   | Ownership   | Terraform  | Cli Latest Version  |
+===================+=========+=============+============+=====================+
| True              | True    | True        | True       | 3.120.0             |
+-------------------+---------+-------------+------------+---------------------+
```

Or if the `M3-CLI` version is the latest:

```console
$ m3 health-check
Response:
+-------------------+---------+-------------+------------+---------------------+
| Server Available  | Mails   | Ownership   | Terraform  | Cli Latest Version  |
+===================+=========+=============+============+=====================+
| True              | True    | True        | True       | 3.120.0             |
+-------------------+---------+-------------+------------+---------------------+
```

## Uninstallation

The uninstallation version of `M3-CLI` assumes that you have `Python 3.10` and `venv` installed as a best practice, along with `M3-CLI` inside it.

### Uninstallation Flow

#### Windows

The updates require the following command:
```console
pip uninstall m3-cli
```

#### Example:
```console
(venv) C:\Maestro3_tests\m3-cli-test-updating>pip uninstall m3-cli         
Found existing installation: m3-cli 3.120.0
Uninstalling m3-cli-3.120.0:
  Would remove:
    c:\maestro3_tests\m3-cli-test-updating\venv\lib\site-packages\m3_cli-3.120.0.dist-info\*
    c:\maestro3_tests\m3-cli-test-updating\venv\lib\site-packages\m3cli\*
    c:\maestro3_tests\m3-cli-test-updating\venv\m3cli\access_meta.json
    c:\maestro3_tests\m3-cli-test-updating\venv\m3cli\bash_m3cli_complete.sh
    c:\maestro3_tests\m3-cli-test-updating\venv\m3cli\commands_def.json
    c:\maestro3_tests\m3-cli-test-updating\venv\m3cli\m3cli_complete.py
    c:\maestro3_tests\m3-cli-test-updating\venv\m3cli\zsh_m3cli_complete.sh
    c:\maestro3_tests\m3-cli-test-updating\venv\scripts\m3.exe
Proceed (Y/n)? y
  Successfully uninstalled m3-cli-3.120.0
```

> 💡 **Tip:** Uninstalling `M3-CLI` does not delete all libraries that were installed with `M3-CLI`. The full uninstallation process includes removing `venv`

Go to [Table of Contents](#table-of-contents)

{{ pagebreak }}

# Usage Guide

## Configuration

Before using `M3-CLI` execute command `m3 access` to set up all needed settings.

In case you want to configure all needed settings manually, please set up the
following environmnet variables:

* `M3SDK_ACCESS_KEY`: Specifies an M3 access key associated with Maestro3 user;
* `M3SDK_SECRET_KEY`: Specifies the secret key associated with the access key.
  This is essentially the "password" for the access key.
* `M3SDK_ADDRESS`: Specifies the address of the Maestro3 environment.

Or you can set credentials non-interactively using `m3 access` command with
specified parameters:

```console
(venv) C:\Maestro3\m3-cli>m3 access --access_key <access_key> --secret_key <_secret_key> --api_address <api_address>
```

After this a `default.cr` file with the access parameters you provided will be 
created in a `.m3cli` folder inside your home directory.

### Obtaining Credentials

To get your credentials please `login` to the Maestro3 and follow the guide below:

1. Switch to My Account page:

![](https://raw.githubusercontent.com/Maestro-Cloud-Control/m3-cli/main/pics/generate_creds_0.png)

{{ pagebreak }}

*2*. Start the 'CLI/SDK Access' wizard:

![](https://raw.githubusercontent.com/Maestro-Cloud-Control/m3-cli/main/pics/generate_creds_1.png)

*3*. Specify the expiration time for the credentials:

![](https://raw.githubusercontent.com/Maestro-Cloud-Control/m3-cli/main/pics/generate_creds_2.png)

{{ pagebreak }}

*4*. Obtain your credentials and export access key to environment variable
M3SDK_ACCESS_KEY, and secret key to M3SDK_SECRET_KEY

![](https://raw.githubusercontent.com/Maestro-Cloud-Control/m3-cli/main/pics/generate_creds_3.png)

### Optional Configuration

The following environment variables could be used to override default values `M3-CLI` uses:

* `M3CLI_CONFIGURATION_FOLDER_PATH`: Specifies the path to the directory
  containing files with the actual commands and parameters
  definitions (``commands_def.json, commands_help.py``). The default value:
  internal application path.
* `M3SDK_VERSION`: In case you need to specify SDK version. The default version
  is "3.2.80".
* `M3CLI_DEBUG`: in case you need debug mode set to this env variable value
  True. The default value is "False".
* `LOG_PATH`: in case you need to store the `M3-CLI` log file by the custom path.

## Usage Examples

After you have installed the tool and set the credentials as environment
variables, the `M3-CLI` is ready to be used.

> 💡 **Tip:** The development of the Maestro3 CLI is still in progress. Examples below contain demo data. Will be updated.

To get information about the available commands/parameters just run the `m3` as
it is displayed below:

Root help contains data about all available commands:

![](https://raw.githubusercontent.com/Maestro-Cloud-Control/m3-cli/main/pics/usage_sample_0.png)

Command `--help` contains abbreviated data about parameters:<br>
![](https://raw.githubusercontent.com/Maestro-Cloud-Control/m3-cli/main/pics/usage_sample_1_1.png)

Use `--full-help` command for all available options:

![](https://raw.githubusercontent.com/Maestro-Cloud-Control/m3-cli/main/pics/usage_sample_1_2.png)

Command result in `--table` output mode (default output mode) :

![](https://raw.githubusercontent.com/Maestro-Cloud-Control/m3-cli/main/pics/usage_sample_2.png)

Command result in `--json` output mode (default output mode) :

![](https://raw.githubusercontent.com/Maestro-Cloud-Control/m3-cli/main/pics/usage_sample_3.png)

Command result in `--full` output mode (default output mode) :

![](https://raw.githubusercontent.com/Maestro-Cloud-Control/m3-cli/main/pics/usage_sample_4.png)

`--verbose` parameter writes command result to the terminal.

{{ pagebreak }}

## Developers Guide

The `M3-CLI` tool is designed to provide dynamic command line interface
based on commands configuration declared in `commands_def.json` file.

**The tool DOES NOT perform any business logic related to management of resources Maestro3 provides.**

The sequence diagram is displayed below.  
![](https://raw.githubusercontent.com/Maestro-Cloud-Control/m3-cli/main/pics/sequence_diagram.png)

### Commands Definition File:

The commands definition file (`commands_def.json`) is a file that defines a set
of commands, their groupings, and parameters of commands that can be executed via CLI. 
Here is a full example of attributes found in the definition file:

```json5
{
    "groups": [
        "A name of a group of related commands"
    ],
    "domain_parameters": {
        "domain-parameter-name-1": {
            "alias": "param_alias",
            "api_param_name": "The name of the parameter that the server accepts to form the response",
            "help": "Parameter description",
            "required": true,
            "validation": {
                "type": "string"
            }
        }
    },
    "commands": {
        "command-name-1": {
            "api-action": "REQUIRED. Mapping for M3API command",
            "help_file": true,                      // A Flag. If commands help 
                                                    // stored into the file
            "help": "Explanation of what command does",
            "alias": "Alias for the command name. Could be used instead of command-name-1",
            "integration_request": true,            // A Flag. Specify if the 
                                                    // request will be processed

            "integration_response": true,           // A Flag. Specify if the
                                                    // response will be processed

            "integration_suffix": "",               // if specified, m3cli should
                                                    // build the plugin name
                                                    // according to the 
                                                    // ${command_name}_
                                                    // ${integration_suffix}.py
                                                    // pattern
            "groups": [
                "group1",                           // A name of the group of
                                                    // commands to which this
                                                    // command relates

                "cli-<command-name>-help",          // Defines a unidirectional
                                                    // relation to the <command-
                                                    // name> command

                "email-<notification_type>-group",  // Defines a relation to the
                                                    // Maestro notifications of
                                                    // the type <notification_type>
            ],
            "parameters": {                         // Optional
                "inherited-param-from-domain": {
                    "parent": "Name of the domain parameter to inherit properties."
                },
                "param-name-1": {
                    "parent": "name",               // The name of the parent
                    "alias": "Alias for the parameter name. Could be used instead of param-name-1",
                    "api_param_name": "The name of the parameter that the server accepts to form the response",
                    "help": "REQUIRED. Explanation of what the parameter means",
                    "required": true,               // Set the parameter as a
                                                    // REQUIRED

                    "secure": true,                 // Hide the value of the
                                                    // parameter in logs. Allowed
                                                    // values: [true, false]

                    "validation": {                 // REQUIRED. Set of
                                                    // validation rules.

                        "type": "string/object",    // REQUIRED. The type of
                                                    // parameter. Allowed values:
                                                    // ['string', 'number',
                                                    // 'list', 'object', 'date',
                                                    // 'bool', 'file']

                        "allowed_values": [],       // A list of allowed values.
                                                    // Applicable to param of
                                                    // types 'string' and 'list'

                        "regex": "Regular Expression. Applicable to params of types: 'string', 'file'",
                        "regex_error": "A meesage to show if the regex check failed. Applicable to params of types: 'string', 'file'",
                        "properties": {},           // jsonschema validation
                                                    // rules. Applicable to param
                                                    // of type: 'object';

                        "min_value": 0,             // number validation rule.
                                                    // Applicable only to type:
                                                    // 'number',

                        "max_value": 7,             // number validation rule.
                                                    // Applicable only to type:
                                                    // 'number',

                        "max_size_bytes": 1024,     // file validation rule.
                                                    // Applicable only to type:
                                                    // 'file',

                        "file_extensions": ['.txt'] // file validation rule.
                                                    // Applicable only to type:
                                                    // 'file'

                    },
                    "case": "upper/lower"           // convert a value to upper
                                                    // case automatically
                }   
            },
            "output_configuration": {               // REQUIRED. Contains
                                                    // configuration for the
                                                    // output.

                "response_table_headers": [         // Required. Contains list
                  "header-1", "header-2"            // of attributes to display
                ],                                  // in output.
                "none": true,                       // Replace the response from
                                                    // server to "The command has
                                                    // been executed successfully"

                "nullable": true,                   // Set the flag 'nullable' in
                                                    // order to prevent hiding
                                                    // zeros and False values of
                                                    // number and boolean
                                                    // attributes.

                "multiple_table": true,             // A flag. If the response
                                                    // consists of several tables

                // The structure of the "response_table_headers" if the
                // "multiple_table" was specified
                "response_table_headers": [
                  {
                    // The display name of a table
                    "display_name": "Instance price model:",
                    // The name of the table that the server sends in the response
                    "name": "instancePriceModel",
                    // Contains list of attributes to display in output.
                    "headers": []
                  }
                ],
                // Optional. Used to alter appearance of data in columns.
                "headers_customization": {
                  // The header name
                  "the_name_of_header": {
                    // Custom name of the header
                    "header_display_name": "Custom name of the header",
                    // A flag. Disables automatic conversion of string-values to
                    // numbers.
                    "disable_numparse": true,
                    // A flag. Disables automatic alignment of list values to a
                    // column.
                    "prevent_list_formatting": true
                  }
                },
              "unmap_key": "Contains 'key' to extract response if needed."
            }
        }
    },
    "version": "major.minor"     // see the versioning rules below
}
```

> 💡 **Tip:** Commands help values can be stored into the file named `commands_help.py`. The format of the such storing type is Python native. Example:

```console
run-instance = """
Use this command to run instance.

Examples:
1. Describes all available instances for the certain tenant in the specified region
    m3 run-instance -tn <tenant-name> -r <region> -iname <instance-name> -shname <shape-name> -key <key-name> -count <number-of-instances>
"""
```

### Related Commands Section in "full-help" Contents

The related commands section is constructed automatically based on the `groups` attribute of each command.
The related commands look like this:
```console
Related commands:

1. Deletes a schedule from your tenants schedule library:
        m3 delete-schedule -r <region> -tn <tenant> -n <name>
```

There are two ways a command can be added to a list of related commands of the other command.

The first approach requires to declare a group of commands in the `group` attribute in the root of the `commands_def` file,
and then assign it to all commands that are in this group. All commands within the group share a bidirectional relation with each other.
Consider the next example:

```json5
{
  "groups": ["group_A"],
  "commands": {
    "first_command": {
      "groups": ["group_A"],
      // ...
    },
    "second_command": {
      "groups": ["group_A"],
      // ...
    }
  } 
}
```
With this configuration the `first_command` will be in the list of related commands of the `second_command` and vice versa.

The second approach allows us to define a unidirectional relation between commands (auxiliary commands). We make one command related to another 
by adding the name of the other command to the list of groups of this command with a special prefix and suffix (`cli-` and `-help`). 
Consider the next example:
```json5
{
  "commands": {
    "first_command": {
      "groups": ["cli-second-command-help"],
      // ...
    },
    "second_command": {
      // ...
    }
  } 
}
```
With this configuration we will see the `first_command` in the list of related commands of the `second_command`. 
At the same time the `second_command` will not be in the list of related commands of the `first_command`.

### Default Command Parameter Values

The default values for the command parameters can be stored 
in the `m3.properties` file.

```
...
tenant-name = SFTL-SLCTL
region = SFTL-OPENSTACK-SLCTL
...
```

You can create several `m3.properties` files in different directories with
different default values. To select the required parameters change the
current working directory to the directory with the appropriate
`m3.properties` file.

Other option is to store the default values for the command 
parameters in the `default.cr` file.

```json5
{
    ...
    "tenant-name": "SFTL-SLCTL",
    "region": "SFTL-OPENSTACK-SLCTL",
    ...
}
```

The default parameter values from the `m3.properties` file take precedence 
over the values from the `default.cr` file.

### Integration Request/Response

From version `2.1.0` there is possibility to process CLI input and Server output
manually using custom Python code. To use this feature you need to create plugin
with an appropriate properties:

0) Create the directory named `plugins` by the path that were specified as a
   value for the env variable `M3CLI_CONFIGURATION_FOLDER_PATH`;
1) Create simple python module (`filename.py`) and put it into the directory
   named `plugins` mentioned above;
2) To change the CLI input create a method inside your script with
   name `create_custom_request` that will receive one parameter `request`. For
   example:

```py
def create_custom_request(request):
    return request
```

3) To change the CLI output create a method inside your script with
   name `create_custom_response` that will receive `request` and `response` parameters. For
   example:

```py
def create_custom_response(request, response):
    return response
```

From the version `3.41.7` there is possibility not to hide the boolean fields if
the value is `False`. To use this feature you should follow the next step:

Add `nullable` field with the value `true` to the `output_configuration`
section of the `commands_def.json` file. For example:

```json5
"output_configuration": {
        "nullable": true,
        "response_table_headers": [
          "region",
          "nativeName",
          "cloud",
          "active",
          "hidden"
        ]
      }
```

In example above, if the value of field `active` will be `false`, the value in
the table column will not be hidden.

### Command Output Formatting

In case CLI receives a response with items which have an empty attribute, this attribute will be dropped
from the response (in table view only).

To add custom formatting to a response attribute, add the `headers_customization` parameter to `output_configuration`.

```json5
"output_configuration": {
    "response_table_headers": ["header-1", "header-2"],
    "headers_customization": {
      "header-1": {
        "disable_numparse": true,
        "prevent_list_formatting": true
      }
    }
}
```

The `disable_numparse` setting disables automatic conversion of string-values to numbers.
The `prevent_list_formatting` setting disables automatic alignment of list values to a column.

### Interactive Options

`Interactive options` is a feature that enables a command to fetch additional
parameters from the server and either prompt a user to interactively provide values for
these parameters or create a file with additional parameters (a `varfile`) for future use.

To enable a command to fetch additional parameters, add the following attribute to the command's definition:
```json5
"interactive_options": {
    // The name of parameters group
    "option_name": "params",
    // The name of server handler the returns the list of additional parameters
    "parameters_handler": "GET_SERVICE_VARIABLES_INFO",
    // The name of server handler the validates the list of additional parameters
    "validation_handler": "VALIDATE_SERVICE_VARIABLES",
}
```
If this feature is enabled, the command will get additional parameters via the `parameters_handler`,
ask the user to fill the values for these parameters or to provide a varfile, validate the additional parameters
and send them back to the server as a part of the original request.

To enable a command to create a varfile, add the following attribute to the command's definition: 
```json5
"interactive_options": {
    // The name of server handler the returns the list of additional parameters
    "parameters_handler": "GET_SERVICE_VARIABLES_INFO",
    // Marks the command as a generator of a file with additional parameters 
    // fetched with the "parameters_handler"
    "generate_varfile": true,
}
```
The `varfile` is a JSON file, and it contains all the additional parameters that the `parameter_handler` provides. 
The parameters are either filled with default values or have empty values.

### M3-CLI Autocomplete
By default, in `M3-CLI` tool  will be enabled autocomplete 
that supports only Unix-based platforms (bash&zsh interpreters).

To activate it do a few steps:

1. Create virtual environment
2. Install `M3-CLI`
3. Create SYMLINK to virtual environment `sudo ln -s your_path_to_venv/bin/m3 /usr/local/bin/m3`
4. Start new terminal session
5. Execute command `sudo m3 enable-autocomplete`
6. Restart terminal session

To deactivate 
1. Execute command `sudo m3 disable-autocomplete`
2. Restart terminal session

> 💡 **Tip:** The type of the return value in the functions described above should be the same as the received parameter (`request/response`)
3. After successful plugins creation add an appropriate attributes to the
   command description in the file `commands_def.json`:
   `"integration_request": true` or `"integration_response": true`

Go to [Table of Contents](#table-of-contents)

{{ pagebreak }}

# Support

## How to Report an Issue

When reporting an issue, please provide as much detail as possible. This includes:

- The version of Python you are using. The `M3-CLI` tool supports `Python 3.10`.
- A clear and concise description of the issue.
- Steps to reproduce the issue.
- Any error messages or logs that can help us understand the problem.

Please send your issue report to `Oleksii_Olchedai@epam.com`.

## How to Communicate with the Support Team

When communicating with the support team, please be respectful and patient. 
Our team is here to help you, and we will do our best to resolve your issue as quickly as possible.

Here are some tips for effective communication:

- Be clear and concise in your descriptions.
- Provide all the necessary information related to your issue.
- If you have any screenshots or logs, please include them.

You can reach out to the support team at `Oleksii_Olchedai@epam.com`. We aim to respond to all queries within 24 hours.

**Company**: `EPAM`

**Tool**: `M3-CLI`

**Supported Python Versions**: `3.10`

**Support**: `Oleksii_Olchedai@epam.com`

Go to [Table of Contents](#table-of-contents)
