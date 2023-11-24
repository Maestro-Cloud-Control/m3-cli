## Script `customizer`

The script is written to customize `commands_def.json` file content.
**PLEASE NOTE:** script can be executed only if m3cli tool installed

### Required parameters for script execution:

* `--commands_def_file_path` - Path to root `commands_def.json` file
* `--mutation_file_path` - Path to file with predefined mutation rules
* `--output_file_path <path/file_name.json>` - Optional. Path to file where 
processed `commands_def.json` file will be saved. By default save to root 
`commands_def.json` file path 

#### Script execution path:
1. Script iterates through mutations provided in `--mutation_file_path` parameter 
and depends on mutation action, overrides, inherits or exclude command configuration 
2. Inherit mutation adds configuration to existed command structure or updates it 
depends on provided user-defined key-values. <br>
There are three levels of configuration available for inheritance:
    * Top level configuration (allows configuring command settings such as 
   `api_action`, `integration_request`, `help_file`, etc.)
    * Parameter level configuration (allows configuring options such as 
   `api_param_name`, `validation`, `case`, etc.)
    * Output configuration level (allows configuring options such as 
   `response_table_headers`, `headers_customization`, `sizeLabel`, etc.)
3. Override mutation fully overwrites command structure with user-defined.
4. Commands provided in list of exclusions will be deleted from result meta


#### Mutation file structure:

```json5
{
  "mutations": {
    "command_name_to_be_mutated": { 
      "action": "inherit/override", // the type of mutation which will be applied to command  
      "mutation_key": "mutation_value", // top level configuration 
      "parameters": {
        "mutation_parameter_key": "mutation_parameter_value" // parameter level configuration
      },
      "output_configuration": {
        "mutation_output_key": "mutation_output_value" // output configuration level
      }
    }
  },
  "exclusions": [
    "command_name_to_be_excluded" // the name of command which will be deleted
  ]
}
```

#### Example of inherit mutation:
![customizer_inherit](pics/customizer_inherit.png)
As mentioned above, in case of inherit mutation existed options can be updated
with user defined or extended if mutation options are not exists in command.

#### Example of override mutation:
![customizer_override](pics/customizer_override.png)
In case of override mutation existed options overwrites with user-defined in 
mutation file