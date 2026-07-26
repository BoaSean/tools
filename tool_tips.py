import platform
import os
import sys

from vsc_generator import toolchain


def show_tips():

    commands_dict = {
        "make": [
            ("windows", "mingw32-make"),
            ("linux",   "bear -- make"),
        ],
        "cmake": [
            ("windows", r"Remove-Item -Path .\* -Recurse -Force"),
            ("linux",   "rm -rf ./*"),
            ("windows", r'cmake .. -G "MinGW Makefiles" -DCMAKE_EXPORT_COMPILE_COMMANDS=ON'),
            ("windows", "cmake --build ."),
            ("windows", "mingw32-make.exe"),
            ("linux",   "cmake .."),
            ("linux",   "make"),
            ("all",     ""),
            ("windows", r'Remove-Item -Path build\\*, output\\* -Recurse -Force'),
            ("linux", r'rm -rf build/* output/*'),
            ("windows", r'cmake -S . -B build -G "MinGW Makefiles" -DCMAKE_EXPORT_COMPILE_COMMANDS=ON'),
            ("linux", r'cmake -S . -B build -DCMAKE_EXPORT_COMPILE_COMMANDS=ON'),
            ("all", "cmake --build build"),
            ("all",     ""),
            ("windows", f'$env:PATH = "{toolchain["windows"]["ThirdParty_path"]}/install/x86_64-w64-mingw32-release/bin;$env:PATH"'),
            ("linux",   ""),
            ("linux",   "   sudo apt install glibc-source"),
            ("linux",   "   cd /usr/src/glibc/"),
            ("linux",   "   sudo tar -xvf glibc-2.35.tar.xz"),
            ("linux",   "   [lanch cwd] ->  /usr/src/glibc/glibc-2.35"),
        ],
        "idf": [
            ("linux",   "sudo apt install unrar "),
            ("linux",   "sudo apt install rar "),
            ("linux",   "unrar x yourfile.rar"),
            ("linux",   "rar a -r esp_esp32s3_szp.rar esp_esp32s3_szp/"),
            ("linux",   "cp -r esp_hello_world my_project"),
            ("all",     ""),
            ("windows", toolchain["windows"]["idf"]),
            ("linux", "source "+toolchain["linux"]["idf"]),
            ("all",     ""),
            ("all",     "   idf.py create-project test"),
            ("all",     ""),
            ("all",     "   idf.py set-target esp32c6   idf.py set-target esp32s3"),
            ("all",     ""),
            ("all",     "   idf.py menuconfig"),
            ("all",     "   idf.py save-defconfig                        ->sdkconfig.defaults  默认构建"),
            ("all",     ""),
            ("all",     "   idf.py create-manifest                       ->idf_component.yml   组件管理"),
            ("all",     "   idf.py update-dependencies                   ->dependencies.lock"),
            ("all",     ""),
            ("all",     "   idf.py fullclean"),
            ("all",     "   idf.py build"),
            ("all",     ""),
            ("linux",   "   sudo chmod 777 /dev/ttyACM0"),
            ("all",     ""),
            ("all",     "   idf.py -p COM7 flash"),
            ("all",     "   idf.py -p COM7 monitor"),
            ("windows", "   idf.py -p COM10 flash monitor"),
            ("linux",   "   idf.py -p /dev/ttyACM0 flash monitor"),
            ("all",     "   idf.py -p COM9 app-flash monitor"),
            ("all",     "   CTRL + ]"),
        ],
        "rtt4": [
            ("windows", "cmd /k "+toolchain["windows"]["rtt_env"]),
            ("windows", "set PKGS_ROOT="+toolchain["windows"]["PKGS_ROOT"]),
            ("windows", "set RTT_ROOT="+toolchain["windows"]["RTT_ROOT4"]),
            ("windows", "set SDK_ROOT="+toolchain["windows"]["SDK_ROOT4"]),
            ("linux",   f'source {toolchain["linux"]["rtt_env"]}'),
            ("linux",   f'export PKGS_ROOT="{toolchain["linux"]["PKGS_ROOT"]}"'),
            ("linux",   f'export RTT_ROOT="{toolchain["linux"]["RTT_ROOT4"]}"'),
            ("linux",   f'export SDK_ROOT="{toolchain["linux"]["SDK_ROOT4"]}"'),
            ("all",     ""),
        ],
        "rtt": [
            ("windows", "cmd /k "+toolchain["windows"]["rtt_env"]),
            ("windows", "set PKGS_ROOT="+toolchain["windows"]["PKGS_ROOT"]),
            ("windows", "set RTT_ROOT="+toolchain["windows"]["RTT_ROOT"]),
            ("windows", "set SDK_ROOT="+toolchain["windows"]["SDK_ROOT"]),
            ("linux",   f'source {toolchain["linux"]["rtt_env"]}'),
            ("linux",   f'export PKGS_ROOT="{toolchain["linux"]["PKGS_ROOT"]}"'),
            ("linux",   f'export RTT_ROOT="{toolchain["linux"]["RTT_ROOT"]}"'),
            ("linux",   f'export SDK_ROOT="{toolchain["linux"]["SDK_ROOT"]}"'),
            ("all",     ""),
        ],
    }

    if len(sys.argv) > 1:
        param1 = sys.argv[1]  # 第一个参数，字符串类型
    else:
        sys.exit(1)

    if param1 not in ("make", "cmake", "idf","rtt4","rtt"):
        print(f"[ERROR] Not Supported: {param1}")
        sys.exit(1)

    commands=commands_dict[param1]

    if commands:
        system = platform.system().lower()  # 'windows', 'linux', 'darwin'等
        
        # system ="windows"        
        # system ="linux"

        print("Common commands:")
        for plat, cmd in commands:
            if plat == "all" or (plat == "windows" and system == "windows") or (plat == "linux" and system == "linux"):
                print(f"  {cmd}")

if __name__ == "__main__":
    show_tips()