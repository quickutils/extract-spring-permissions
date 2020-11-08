
# {::nomarkdown}<p style="text-align: center;" align="center"><img src="https://github.com/quickutils/quickutils.github.io/blob/master/images/esp-512.png?raw=true" alt="extract-spring-permissions" style="width:180px;height:160px;" width="180" height="160" /><br />extract-spring-permissions</p>{:/}

Extract all permissions and roles declared with the any of the annotations `@PreAuthorized`, `//@PreAuthorize`, `@PreAuthorizePermission` and `//@PreAuthorizePermission`. You can also specified format in which each value should be exported in each line and also replace part of the value, useful for direct export to json or other format without need to copy the roles and permission values.

The script does not use proper parsing techniques it a quick script so it prone to error, crash or inaccurate result. At time of finishing this script it able to extract over 500 permissions completely from a very large multi-tenant system.

___

## Table of content
- [Installation](#installation)
- [Examples](#examples)
- [How it works](#how-it-works)
- [Contributing](#contributing)
- [License](#license)

## Installation

Downlaod and install python from https://www.python.org/downloads/. Clone the repo and run the `esp.py` script in the folder

```bash
git clone https://github.com/quickutils/extract-spring-permissions.git
cd extract-spring-permissions
python esp.py -h
```

## Examples

Using the controller file with the content

```java
//HomeController.java
package io.github.thecarisma;

import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.stereotype.Controller;

@Controller
@RequestMapping("/")
@PreAuthorize("hasAnyRole('ROLE_USER,ROLE_SUPER_USER,ROLE_ADMIN')")
public class AbstractProviderController {
    	
    @ResponseBody
    @RequestMapping(method = RequestMethod.GET)
    @PreAuthorize("hasRole('ROLE_VIEW_ABSTRACT_PROVIDER')")
    public String index(){
		return "<html>Hello World</html>"
	}

}

```

### Basic

```
python esp.py HomeController.java

ROLE_USER
ROLE_SUPER_USER
ROLE_ADMIN
ROLE_VIEW_ABSTRACT_PROVIDER
```

### With --format argument

```
python esp.py HomeController.java --outformat "Permission is #{value}"

Permission is ROLE_USER
Permission is ROLE_SUPER_USER
Permission is ROLE_ADMIN
Permission is ROLE_VIEW_ABSTRACT_PROVIDER
```

### With --replace argument

```
python esp.py HomeController.java --replace "ROLE,PERMISSION"
PERMISSION_USER
PERMISSION_SUPER_USER
PERMISSION_ADMIN
PERMISSION_VIEW_ABSTRACT_PROVIDER


python esp.py HomeController.java --replace "ROLE_,"
USER
SUPER_USER
ADMIN
VIEW_ABSTRACT_PROVIDER
```

### With --format argument and --replace

```
python esp.py HomeController.java --outformat "\"value\": \"#{value}\"," --replace "ROLE_,"

"value": "USER",
"value": "SUPER_USER",
"value": "ADMIN",
"value": "VIEW_ABSTRACT_PROVIDER",
```

## How it works

If the specified path if a folder it uses the python function `os.walk` to iterate the sub folders to find any java file then go ahead and process each detected java file, if the path is a file it go straign to extracting the permissions from that file. 

For each line of the java file the leading and trailing spaces are removed then if that line starts with any of `@PreAuthorized`, `//@PreAuthorize`, `@PreAuthorizePermission` and `//@PreAuthorizePermission`, the argument for that annotation will be extracted, e.g. `@PreAuthorize("hasRole('ROLE_VIEW_ABSTRACT_PROVIDER')")` will result to `"hasRole('ROLE_VIEW_ABSTRACT_PROVIDER')"` which is further processes to extract the argument or value within to `'ROLE_VIEW_ABSTRACT_PROVIDER'`, then the leading and trailing quotes `'` or `"` are removed to get `ROLE_VIEW_ABSTRACT_PROVIDER`. For annotation with multiple value the value is splited by comma to get the values.

For the formating aspect it simply replaces `#{value}` in your outformat string with the permission before printing in each line. E.g. for permission ROLE_SUPER_USER `--outformat "Permission is #{value}"` result to printing `Permission is ROLE_SUPER_USER`, combining with the --replace argument allow more custom output. The `--replace` is used to replace part of each permission with another value before printing to command line E.g. for permission ROLE_SUPER_USER `--replace "ROLE,PERMISSION"` result to printing `PERMISSION_SUPER_USER`. Combining the --outformat with --replace give more custome output. 

`--outformat "Permission is #{value}" --replace "ROLE,PERMISSION"` result to 

```bash
Permission is PERMISSION_SUPER_USER
```

`--outformat "Permission is #{value}" --replace "ROLE_,"` result to 

```bash
Permission is SUPER_USER
```

## Contributing

You can open issue or file a request that only address problems in this implementation on this repo. All Pull Requests are welcomed.

## License

MIT License Copyright © 2020 [Adewale Azeez](https://twitter.com/iamthecarisma) - quickutils
