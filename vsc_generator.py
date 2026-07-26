import os
import sys
import platform
from pathlib import Path
import re
import json
import yaml

# pip install pyyaml

toolchain={
    "windows": {
        "gdb":"D:/Program/mingw64/bin/gdb.exe",
        "python":"python",
        "STM32_Programmer_CLI":"D:/program/stm32cubeprg_v2_10_0/bin/STM32_Programmer_CLI.exe",
        
        "workspace_path":"D:/studio/workspace/c_cpp_workspace2",
        "ThirdParty_path":"D:/studio/workspace/c_cpp_workspace2/ThirdParty",
        "tool_path":"D:/studio/workspace/c_cpp_workspace2/tools",

        "rtt_env":"D:/Program/env-windows-1.5.2/tools/bin/env-init.bat",
        "PKGS_ROOT":"D:/studio/workspace/c_cpp_workspace2/ThirdParty/source/rtt-packages",
        "RTT_ROOT4":"D:/studio/workspace/c_cpp_workspace2/ThirdParty/source/rtt-kernel-v4.1.0",
        "SDK_ROOT4":"D:/studio/workspace/c_cpp_workspace2/ThirdParty/source/rtt-sdk-v4.1.0/stm32",
        "RTT_ROOT":"D:/studio/workspace/c_cpp_workspace2/ThirdParty/source/rtt-kernel",
        "SDK_ROOT":"D:/studio/workspace/c_cpp_workspace2/ThirdParty/source/rtt-sdk/stm32",

        # "idf":"D:/program/esp-idf/esp-idf_v5.4.1/export.ps1",
        "idf":"C:/Espressif/tools/Microsoft.v5.5.4.PowerShell_profile.ps1",
    },
    "linux": {
        "gdb":"/usr/bin/gdb",
        "python":"python3",
        "STM32_Programmer_CLI":"/home/sean/program/stm32cubeprg/bin/STM32_Programmer_CLI",

        "workspace_path":"/home/sean/studio/c_cpp_workspace",
        "ThirdParty_path":"/home/sean/studio/c_cpp_workspace/ThirdParty",
        "tool_path":"/home/sean/studio/c_cpp_workspace/tools",

        "rtt_env":"~/.env/env.sh",
        "PKGS_ROOT":"/home/sean/studio/c_cpp_workspace/ThirdParty/source/rtt-packages",
        "RTT_ROOT4":"/home/sean/studio/c_cpp_workspace/ThirdParty/source/rtt-kernel-v4.1.0",
        "SDK_ROOT4":"/home/sean/studio/c_cpp_workspace/ThirdParty/source/rtt-sdk-v4.1.0/stm32",
        "RTT_ROOT":"/home/sean/studio/c_cpp_workspace/ThirdParty/source/rtt-kernel",
        "SDK_ROOT":"/home/sean/studio/c_cpp_workspace/ThirdParty/source/rtt-sdk/stm32",
        
        # "idf":"~/esp/esp-idf/export.sh",
        "idf":"/home/sean/.espressif/tools/activate_idf_v5.5.5.sh",
    }
}


#嵌套字典
task_json = {
    "windows": {
        "make_type_build": {
            "type": "shell",
            "label": "build",
            "command":"mingw32-make",
            "args": [],
            "options": {},
            "problemMatcher": [],
            "group": "build", 
        },
        "cmake_config": {
            "type": "shell",
            "label": "cmake_config",
            "command":"cmake",
            "args": [
                "-S",".",
                "-B","build",
                "-G", "MinGW Makefiles",
                "-DCMAKE_EXPORT_COMPILE_COMMANDS=ON",
            ],
            "options": {},
            "problemMatcher": [],
        },
        "cmake_build": {
            "type": "shell",
            "label": "cmake_build",
            "command":"cmake",
            "args": [
                "--build", "build"
            ],
            "options": {},
            "problemMatcher": [],
        },
        "cmake_type_build": {
            "type": "shell",
            "label": "build",
            "dependsOn":[
                "cmake_config",
                "cmake_build",
            ],
            "dependsOrder": "sequence",
            "options": {},
            "problemMatcher": [],
            "group": "build", 
        }
    },
    "linux": {
        "make_type_build": {
            "type": "shell",
            "label": "build",
            "command": "bear",
            "args": [
                "--",
                "make"
            ],
            "options": {},
            "problemMatcher": [],
            "group": "build", 
        },
        "cmake_config": {
            "type": "shell",
            "label": "cmake_config",
            "command":"cmake",
            "args": [
                "-S",".",
                "-B","build",
                "-DCMAKE_EXPORT_COMPILE_COMMANDS=ON",
            ],
            "options": {},
            "problemMatcher": [],
        },
        "cmake_build": {
            "type": "shell",
            "label": "cmake_build",
            "command":"cmake",
            "args": [
                "--build", "build"
            ],
            "options": {},
            "problemMatcher": [],
        },
        "cmake_type_build": {
            "type": "shell",
            "label": "build",
            "dependsOn":[
                "cmake_config",
                "cmake_build",
            ],
            "dependsOrder": "sequence",
            "options": {},
            "problemMatcher": [],
            "group": "build", 
        }
    }
}


def check_toolchain(tc):
    """
    Check if all values in the toolchain dict are non-empty.
    Returns True if all valid, False if any empty value found.
    """
    all_valid = True
    for platform_name, tools in tc.items():
        for tool_name, tool_path in tools.items():
            if tool_path is None or str(tool_path).strip() == "":
                print(f"[ERROR] {platform_name}.{tool_name} is empty!")
                all_valid = False
            # else:
            #     print(f"{platform_name}.{tool_name} = {tool_path}")
    return all_valid

def generate_task_tip(build_system,tip_type):

    return {
        "label": "tip",
        "type": "shell",
        "command": toolchain[build_system]["python"],
        "args": [
            toolchain[build_system]["tool_path"] + "/tool_tips.py",
            tip_type,
        ],
        "options": {},
        "problemMatcher": [],
        "group": "build"
    }

def generate_task_clean(build_system,clean_type):

    if clean_type in ["make_all","cmake_all", "idf_all","rtt4_all","rtt_all"]: 
        task_label = "clean_all"
    else :  
        task_label = "clean"

    return {
        "label": task_label,
        "type": "shell",
        "command": toolchain[build_system]["python"],
        "args": [
            toolchain[build_system]["tool_path"] + "/tool_clean.py",
            clean_type,
        ],
        "options": {},
        "problemMatcher": [],
        "group": "build"
    }

def generate_task_findCOM(build_system):

    if(build_system == "windows"):
        task={
            "type": "shell",
            "label": "findCOM",
            "command": toolchain[build_system]["python"],
            "args": [toolchain[build_system]["tool_path"] + "/tool_findCOM.py"],
            "options": {},
            "problemMatcher": [],
            "group": "build"
        }
    else:
        task={
            "type": "process",
            "label": "findCOM",
            "command": "bash",
            "args": [
                "-c",
                f'{toolchain[build_system]["python"]} {toolchain[build_system]["tool_path"]}/tool_findCOM.py && exec bash',
            ],
            "options": {},
            "problemMatcher": [],
            "group": "build"
        }
    return task

def generate_task_openocd(build_system,target,cmd):

    task_label =f"openocd_{target}"
    
    if(build_system == "windows"):
        task={
            "type": "process",
            "label": task_label,
            "command": "powershell",
            "args": [
                "-Command",
                cmd
            ],
            "options": {},
            "problemMatcher": [],
            "group": "build"
        }
    else:
        task={
            "type": "process",
            "label": task_label,
            "command": "bash",
            "args": [
                "-c",
                cmd
            ],
            "options": {},
            "problemMatcher": [],
            "group": "build"
        }
    return task

def generate_task_stlink(build_system,target,cmd):

    build_system="linux"

    task_label =f"stlink_{target}"
    
    tool_path = toolchain[build_system]["STM32_Programmer_CLI"]

    # print(tool_path)

    cmd=cmd.replace("STM32_Programmer_CLI", tool_path)

    # print(cmd)

    if(build_system == "windows"):
        task={
            "type": "process",
            "label": task_label,
            "command": "powershell",
            "args": [
                "-Command",
                cmd
            ],
            "options": {},
            "problemMatcher": [],
            "group": "build"
        }
    else:
        task={
            "type": "process",
            "label": task_label,
            "command": "bash",
            "args": [
                "-c",
                cmd
            ],
            "options": {},
            "problemMatcher": [],
            "group": "build"
        }
    return task

def generate_task_cmd(build_system,target,cmd):

    if(build_system == "windows"):
        task={
            "type": "process",
            "label": target,
            "command": "powershell",
            "args": [
                "-Command",
                cmd
            ],
            "options": {},
            "problemMatcher": [],
            "group": "build"
        }
    else:
        task={
            "type": "process",
            "label": target,
            "command": "bash",
            "args": [
                "-c",
                cmd
            ],
            "options": {},
            "problemMatcher": [],
            "group": "build"
        }
    return task

def generate_tasks_json(build_system,vscode_dir,build_type,builtin_dict,openocd_cmds_dict,stlink_cmds_dict):

    tasks_json = {
        # // See https://go.microsoft.com/fwlink/?LinkId=733558
        # // for the documentation about the tasks.json format
        "version": "2.0.0",
        "tasks": []
    }

    # tasks_json["tasks"].append(task_json["windows"]["gcc_clean_build"])


    artpi_firmware_path=toolchain[build_system]["tool_path"] +"/download/firmware/art_pi"
    artpi_sdk_path=toolchain[build_system]["ThirdParty_path"]+"/source/sdk-bsp-stm32h750-realthread-artpi"

    openocd_onchip_demo =" ".join([
        "openocd -f interface/stlink.cfg -f target/stm32h7x.cfg",
        "-c init",
        "-c 'reset halt'",
        "-c 'flash write_image erase " + artpi_firmware_path + "/onchip_demo.bin 0x08000000'",
        "-c reset",
        "-c shutdown"
    ])

    openocd_onchip_read =" ".join([
        "openocd -f interface/stlink.cfg -f target/stm32h7x.cfg",
        "-c init",
        "-c 'reset halt'",
        "-c 'flash read_bank 0 read_OnChip.bin ' ",
        "-c reset",
        "-c shutdown"
    ])

    stlink_tool=toolchain[build_system]["STM32_Programmer_CLI"]
    stlink_connect = " -c port=SWD mode=NORMAL"

    artpi_cmds_dict={
        "openocd_onchip_demo"    :openocd_onchip_demo,
        "openocd_onchip_read"    :openocd_onchip_read,

        "stlink_onchip_demo"     : stlink_tool + stlink_connect + " -d " + artpi_firmware_path+"/onchip_demo.bin"+" 0x08000000 "+" -hardRst -s ",

        "stlink_onchip_boot_mdk" : stlink_tool + stlink_connect + " -d " + artpi_firmware_path+"/onchip_boot_mdk.bin"+" 0x08000000 "+" -hardRst -s ",
        "stlink_onchip_boot_rtt" : stlink_tool + stlink_connect + " -d " + artpi_firmware_path+"/onchip_boot_rtt.bin"+" 0x08000000 "+" -hardRst -s ",

        "stlink_Resource_16MB"   : stlink_tool + stlink_connect + " --extload " +artpi_sdk_path+"/debug/stldr/ART-Pi_W25Q128JV.stldr" + " -d " + artpi_sdk_path+"/tools/firmware/Resource_16MB.bin"+" 0x70000000 "+" -hardRst -s ",

        "stlink_flash_mdk_241212": stlink_tool + stlink_connect + " --extload " +artpi_sdk_path+"/debug/stldr/ART-Pi_W25Q64.stldr" + " -d " + artpi_firmware_path+"/flash_mdk_241212.bin"+" 0x90000000 "+" -hardRst -s ",
        "stlink_flash_rtt_led"   : stlink_tool + stlink_connect + " --extload " +artpi_sdk_path+"/debug/stldr/ART-Pi_W25Q64.stldr" + " -d " + artpi_firmware_path+"/flash_rtt_led.bin"+" 0x90000000 "+" -hardRst -s ",
        "stlink_flash_rtt_factory": stlink_tool + stlink_connect + " --extload " +artpi_sdk_path+"/debug/stldr/ART-Pi_W25Q64.stldr" + " -d " + artpi_firmware_path+"/flash_rtt_factory.bin"+" 0x90000000 "+" -hardRst -s ",
        
    }

    # for target, cmd in artpi_cmds_dict.items():
    #     print(f"        {target}:{cmd}")

    art_pi_enabled = builtin_dict.get("art_pi", False)                              #builtin_download
    if art_pi_enabled:
        for target, cmd in artpi_cmds_dict.items():                                
            task=generate_task_cmd(build_system,target,cmd)
            tasks_json["tasks"].append(task)

    if build_type == "make":                                                        #tip
        task=generate_task_tip(build_system,"make")
        tasks_json["tasks"].append(task)
    elif build_type == "cmake":                                                       
        task=generate_task_tip(build_system,"cmake")
        tasks_json["tasks"].append(task)
    elif build_type == "rtt4":                                                      
        task=generate_task_tip(build_system,"rtt4")
        tasks_json["tasks"].append(task)
    elif build_type == "rtt":  
        task=generate_task_tip(build_system,"rtt")
        tasks_json["tasks"].append(task)
    elif build_type == "idf":  
        task=generate_task_tip(build_system,"idf")
        tasks_json["tasks"].append(task)

    if build_type == "make":                                                       #build
        tasks_json["tasks"].append(task_json[build_system]["make_type_build"])
    elif build_type == "cmake":                                                      
        tasks_json["tasks"].append(task_json[build_system]["cmake_config"])
        tasks_json["tasks"].append(task_json[build_system]["cmake_build"])
        tasks_json["tasks"].append(task_json[build_system]["cmake_type_build"])

    # if build_type == "rtt4" :                                                       #env
    #     task=generate_task_env(build_system,build_type)
    #     tasks_json["tasks"].append(task)
    # elif build_type == "rtt" :
    #     task=generate_task_env(build_system,build_type)
    #     tasks_json["tasks"].append(task)

    if build_type != "undefined":                                                   #clean
        clean_type=build_type
        clean_all_type=build_type+"_all"
        # print(clean_type)
        # print(clean_all_type)
        task=generate_task_clean(build_system,clean_type)
        tasks_json["tasks"].append(task)
        task=generate_task_clean(build_system,clean_all_type)
        tasks_json["tasks"].append(task)

    download_cmd_len=len(openocd_cmds_dict)+len(stlink_cmds_dict)
    download_flg=download_cmd_len>0 or art_pi_enabled
    if download_flg or build_type == "idf":                                         #find COM
        task=generate_task_findCOM(build_system)
        tasks_json["tasks"].append(task)

    if(len(openocd_cmds_dict)>0):
        for target, cmd in openocd_cmds_dict.items():                               #openocd
            task=generate_task_openocd(build_system,target,cmd)
            tasks_json["tasks"].append(task)
    if(len(stlink_cmds_dict)>0):
        for target, cmd in stlink_cmds_dict.items():                                #stlink
            task=generate_task_stlink(build_system,target,cmd)
            tasks_json["tasks"].append(task)


    task_path = vscode_dir /"tasks.json"

    with open(task_path, "w") as f:
        json.dump(tasks_json, f, indent=4)

    print("[OK] tasks.json created.")

def generate_c_cpp_properties_json(build_system,vscode_dir,build_type):

    if build_type=="make":
        if build_system=="linux":
            # Define c_cpp_properties.json content
            config = {
                "configurations": [
                    {
                        "name": "Linux",
                        "compileCommands": "${workspaceFolder}/compile_commands.json",
                        "intelliSenseMode": "gcc-x64",
                        "cStandard": "c11",
                        "cppStandard": "c++17"
                    }
                ],
                "version": 4
            }
            create_flag=True
        else:
            create_flag=False
    elif build_type=="cmake":
        config = {
            "configurations": [
                {
                    "name": "CMake",
                    "cStandard": "c11",
                    "cppStandard": "c++17",
                    "compileCommands": "${workspaceFolder}/build/compile_commands.json"
                }
            ],
            "version": 4
        }
        create_flag=True
    elif build_type=="idf":
        # Define c_cpp_properties.json content
        config = {
            "configurations": [
                {
                    "name": "ESP-IDF",
                    "cStandard": "c11",
                    "cppStandard": "c++17",
                    "compileCommands": "${workspaceFolder}/build/compile_commands.json"
                }
            ],
            "version": 4
        }
        create_flag=True
    else:
        create_flag=False

    if create_flag:
        # Write to c_cpp_properties.json
        cpp_path = vscode_dir /"c_cpp_properties.json"
        with open(cpp_path, "w") as f:
            json.dump(config, f, indent=4)

        print("[OK] c_cpp_properties.json created.")

def generate_settings_json(build_system,vscode_dir,build_type):

    if build_type=="cmake":
        if build_system=="windows":
            config ={
                "terminal.integrated.env.windows": {
                    "PATH": f'{toolchain["windows"]["ThirdParty_path"]}/install/x86_64-w64-mingw32-release/bin;${{env:PATH}}'
                }
            }
            create_flag=True
        else:
            create_flag=False
    elif build_type=="rtt4":
        if build_system=="linux":
            config = {
                "terminal.integrated.profiles.linux": {
                    "ENV-4.1.0": {
                        "path": "/bin/bash",
                        "args": [
                            "--rcfile",
                            toolchain["linux"]["rtt_env"],
                            "-i"
                        ],
                        "env": {
                            "PKGS_ROOT":toolchain["linux"]["PKGS_ROOT"],
                            "RTT_ROOT": toolchain["linux"]["RTT_ROOT4"],
                            "SDK_ROOT": toolchain["linux"]["SDK_ROOT4"],
                        }
                    }
                },
                # // "terminal.integrated.defaultProfile.linux": "ENV-4.1.0"
            }
            create_flag=True
        else:
            config ={
                "terminal.integrated.profiles.windows": {
                    "ENV-4.1.0": {
                        "path": "cmd.exe",
                        "args": [
                            "/k",
                            toolchain["windows"]["rtt_env"]
                        ],
                        "env": {
                            "PKGS_ROOT":toolchain["windows"]["PKGS_ROOT"],
                            "RTT_ROOT": toolchain["windows"]["RTT_ROOT4"],
                            "SDK_ROOT": toolchain["windows"]["SDK_ROOT4"]
                        }
                    }
                },
                # // "terminal.integrated.defaultProfile.windows": "ENV-4.1.0"
            }
            create_flag=True
    elif build_type=="rtt":
        if build_system=="linux":
            config = {
                "terminal.integrated.profiles.linux": {
                    "ENV-5.1.0": {
                        "path": "/bin/bash",
                        "args": [
                            "--rcfile",
                            toolchain["linux"]["rtt_env"],
                            "-i"
                        ],
                        "env": {
                            "PKGS_ROOT":toolchain["linux"]["PKGS_ROOT"],
                            "RTT_ROOT": toolchain["linux"]["RTT_ROOT"],
                            "SDK_ROOT": toolchain["linux"]["SDK_ROOT"],
                        }
                    }
                },
                # // "terminal.integrated.defaultProfile.linux": "ENV-5.1.0"
            }
            create_flag=True
        else:
            config ={
                "terminal.integrated.profiles.windows": {
                    "ENV-5.1.0": {
                        "path": "cmd.exe",
                        "args": [
                            "/k",
                            toolchain["windows"]["rtt_env"]
                        ],
                        "env": {
                            "PKGS_ROOT":toolchain["windows"]["PKGS_ROOT"],
                            "RTT_ROOT": toolchain["windows"]["RTT_ROOT"],
                            "SDK_ROOT": toolchain["windows"]["SDK_ROOT"]
                        }
                    }
                },
                # // "terminal.integrated.defaultProfile.windows": "ENV-5.1.0"
            }
            create_flag=True
    elif build_type=="idf":
        if build_system=="linux":
            config = {
                "terminal.integrated.profiles.linux": {
                    "ESP-IDF": {
                        "path": "/bin/bash",
                        "args": [
                            "--rcfile",
                            toolchain["linux"]["idf"],
                            "-i"
                        ]
                    }
                },

                # // "terminal.integrated.defaultProfile.linux": "ESP-IDF"
            }
            create_flag=True
        else:
            create_flag=False
    else:
        create_flag=False

    if create_flag:
        cpp_path = vscode_dir /"settings.json"
        with open(cpp_path, "w") as f:
            json.dump(config, f, indent=4)

        print("[OK] settings.json created.")

def generate_launch_json(build_system,vscode_dir,build_type,):

    if build_type=="cmake":
        if build_system=="windows":
            program="${workspaceFolder}/output/main.exe"
            environment_name ="PATH"
            environment_value  =toolchain["windows"]["ThirdParty_path"]+"/install/x86_64-w64-mingw32-release/bin;${env:PATH}"
            config = {
                "version": "0.2.0",
                "configurations": [
                    {
                        "name": "C/C++: debug",
                        "type": "cppdbg",
                        "request": "launch",
                        "program": program,                                     #//调试的可执行文件
                        "args": [],
                        "stopAtEntry": False,
                        "cwd": "${workspaceFolder}",                            #//调试时的工作目录                        
                        "environment": [
                            {
                                "name": environment_name,
                                "value": environment_value
                            }
                        ],
                        "externalConsole": False,
                        "MIMode": "gdb",
                        "miDebuggerPath": toolchain[build_system]["gdb"],
                        "setupCommands": [
                            {
                                "description": "Enable neat printing for gdb",
                                "text": "-enable-pretty-printing",
                                "ignoreFailures": True  
                            }
                        ],
                        # "preLaunchTask": "rebuild"                            #//调试前自动编译    
                    }
                ]
            }
        else:
            program="${workspaceFolder}/output/main"
            config = {
                "version": "0.2.0",
                "configurations": [
                    {
                        "name": "C/C++: debug",
                        "type": "cppdbg",
                        "request": "launch",
                        "program": program,                                     #//调试的可执行文件
                        "args": [],
                        "stopAtEntry": False,
                        "cwd": "${workspaceFolder}",                            #//调试时的工作目录                        
                        "environment": [],
                        "externalConsole": False,
                        "MIMode": "gdb",
                        "miDebuggerPath": toolchain[build_system]["gdb"],
                        "setupCommands": [
                            {
                                "description": "Enable neat printing for gdb",
                                "text": "-enable-pretty-printing",
                                "ignoreFailures": True  
                            }
                        ],
                        # "preLaunchTask": "rebuild"                            #//调试前自动编译    
                    }
                ]
            }

        create_flag=True
    else:
        create_flag=False

    if create_flag:
        # Write to c_cpp_properties.json
        cpp_path = os.path.join(vscode_dir, "launch.json")
        with open(cpp_path, "w") as f:
            json.dump(config, f, indent=4)

        print("[OK] launch.json created.")

def main():

    if check_toolchain(toolchain):                                                              #toolchain检查
        print("[OK] All tool paths are valid.")
    else:
        print("[ERROR]  Some values are empty. Please check your configuration.")
        sys.exit(1)

    system_type = platform.system()                                                             #build_system
    if system_type not in ("Windows", "Linux", "Darwin"):
        print(f"[ERROR] Not Supported: {system_type}")
        sys.exit(1)

    if system_type == "Windows":
        build_system="windows"
    elif system_type in ["Linux", "Darwin"]:  # Darwin  macOS
        build_system="linux"

    print(f"[OK] build_system: {build_system}")

    build_path = Path.cwd()                                                                     #build_path
    print(f"[OK] build_path: {build_path}")

    config_path = build_path / ".vscode" / "vsc_generator_config.yaml"                          #build_type

    if not os.path.isfile(config_path):
        print(f"[ERROR] Config file not found: {config_path}")
        sys.exit(1)

    print(f"[OK] Config file: {config_path}")
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config_data = yaml.safe_load(f)
    
    # print(config_data)

    project_type = config_data.get('project_type')
    if project_type in ["make","cmake", "idf","rtt4","rtt"]: 
        build_type=project_type
    else :  
        build_type="undefined"
    
    builtin_config = config_data.get('download', {}).get('builtin', {})
    
    # openocd_cmds = config_data['download']['openocd']   
    # stlink_cmds = config_data['download']['stlink']     

    openocd_cmds = config_data.get('download', {}).get('openocd') or {}
    stlink_cmds = config_data.get('download', {}).get('stlink') or {}

    print(f"    build_type: {build_type}")

    if(len(builtin_config)>0):
        print(f"    builtin_config")
        for board, enabled  in builtin_config.items():
            print(f"        {board}:{enabled}")
    if(len(openocd_cmds)>0):
        print(f"    openocd")
        for target, cmd in openocd_cmds.items():
            print(f"        {target}:{cmd}")
    if(len(stlink_cmds)>0):
        print(f"    stlink")
        for target, cmd in stlink_cmds.items():
            print(f"        {target}:{cmd}")

    vscode_dir = build_path / ".vscode"
    os.makedirs(vscode_dir, exist_ok=True)

    generate_tasks_json(build_system,vscode_dir,build_type,builtin_config,openocd_cmds,stlink_cmds)

    generate_c_cpp_properties_json(build_system,vscode_dir,build_type)

    generate_settings_json(build_system,vscode_dir,build_type)

    generate_launch_json(build_system,vscode_dir,build_type)


if __name__ == "__main__":
    main()


# def generate_task_env(build_system,build_type):

#     # build_system="windows"
#     # build_type="rtt"

#     windows_cmd_rtt4=[
#         f'set RTT_ROOT={toolchain["windows"]["RTT_ROOT4"]}',
#         f'set SDK_ROOT={toolchain["windows"]["SDK_ROOT4"]}',
#         toolchain["windows"]["rtt_env"]
#     ]

#     windows_cmd_rtt=[
#         f'set RTT_ROOT={toolchain["windows"]["RTT_ROOT"]}',
#         f'set SDK_ROOT={toolchain["windows"]["SDK_ROOT"]}',
#         toolchain["windows"]["rtt_env"]
#     ]

#     linux_cmd_rtt4 = [
#         f'source {toolchain["linux"]["rtt_env"]}',
#         f'export RTT_ROOT="{toolchain["linux"]["RTT_ROOT4"]}"',
#         f'export SDK_ROOT="{toolchain["linux"]["SDK_ROOT4"]}"',
#         'echo "RTT 4.1.0 environment variables loaded successfully!"',
#         'exec bash'                                             # 打开一个新 bash 会话，让变量生效
#     ]
    
#     linux_cmd_rtt = [
#         f'source {toolchain["linux"]["rtt_env"]}',
#         f'export RTT_ROOT="{toolchain["linux"]["RTT_ROOT"]}"',
#         f'export SDK_ROOT="{toolchain["linux"]["SDK_ROOT"]}"',
#         'echo "RTT 5.1.0 environment variables loaded successfully!"',
#         'exec bash'                                             # 打开一个新 bash 会话，让变量生效
#     ]
    
#     cmd_dict = {
#         "windows": {
#             "rtt4":windows_cmd_rtt4,
#             "rtt":windows_cmd_rtt,
#         },
#         "linux": {
#             "rtt4":linux_cmd_rtt4,
#             "rtt":linux_cmd_rtt,
#         }
#     }
#     # print('&&'.join(cmd_dict["windows"]["rtt4"]))
#     # print('&&'.join(cmd_dict["windows"]["rtt"]))
#     # print('&&'.join(cmd_dict["linux"]["rtt4"]))
#     # print('&&'.join(cmd_dict["linux"]["rtt"]))

#     full_cmd='&&'.join(cmd_dict[build_system][build_type])

#     if build_type =="rtt4":
#         task_label="env4.1.0"
#     elif build_type =="rtt":
#         task_label="env5.1.0"

#     if(build_system == "windows"):
#         task={
#             "type": "process",
#             "label": task_label,
#             "command": "cmd",
#             "args": [
#                 "/k",
#                 full_cmd,
#             ],
#             "options": {},
#             "problemMatcher": [],
#             "group": "build"
#         }
#     else:
#         task={
#             "type": "process",
#             "label": task_label,
#             "command": "bash",
#             "args": [
#                 "-c",
#                 full_cmd,
#             ],
#             "options": {},
#             "problemMatcher": [],
#             "group": "build"
#         }
#     return task