

import os
import shutil
from pathlib import Path
import sys


clean_targets = {
    "make": [
        "build",
        "output",
        "compile_commands.json",
    ],
    "cmake": [
        "build",
        "output",
    ],
    "idf": [
        "build",
        "managed_components",
        "dependencies.lock",
        "sdkconfig",
        "sdkconfig.old",
    ],
    "rtt4": [
        "build",
        "packages",
        "rtthread.bin",
        "rtthread.elf",
        "rtthread.map",
        "vscode.code-workspace",
    ],
    "rtt": [
        "build",
        "packages",
        "rtthread.bin",
        "rtthread.elf",
        "rtthread.map",
        "vscode.code-workspace",
    ],
}

clean_all_targets={
    "public":[
        "__pycache__",
        ".vscode/tasks.json",
        ".vscode/launch.json",
        ".vscode/c_cpp_properties.json",
        ".vscode/settings.json",
    ],
    "make": [
        "build",
        "output",
        "compile_commands.json",
    ],
    "cmake": [
        "build",
        "output",
    ],
    "idf": [
        "build",
        "managed_components",
        "dependencies.lock",
        "sdkconfig",
        "sdkconfig.old",
    ],
    "rtt4": [
        "rtconfig.pyc",
        ".sconsign.dblite",
    ],
    "rtt": [
        "rtconfig.pyc",
        ".sconsign.dblite",
    ],
}

def remove_path(path):

    if os.path.exists(path):
        # print(path)

        if os.path.isdir(path):
            basename = os.path.basename(path)
            if basename in ("build", "output"):
                # Only delete contents of 'build' directory
                for item in os.listdir(path):
                    item_path = os.path.join(path, item)
                    if os.path.isdir(item_path):
                        shutil.rmtree(item_path)
                    else:
                        os.remove(item_path)
                print(f"[OK] Removed directory: {path}")
            else:
                shutil.rmtree(path)
                print(f"[OK] Removed directory: {path}")
        elif os.path.isfile(path):
            os.remove(path)
            print(f"[OK] Removed file: {path}")


def main():

    if len(sys.argv) > 1:
        param1 = sys.argv[1]  # 第一个参数，字符串类型
    else:
        sys.exit(1)


    if param1 in ["make_all","cmake_all", "idf_all","rtt4_all","rtt_all"]: 
        build_type = param1.rsplit('_', 1)[0]
        clean_all_flag=True
    else :  
        build_type=param1
        clean_all_flag=False

    if build_type not in ("make", "cmake", "idf","rtt4","rtt"):
        print(f"[ERROR] Not Supported: {build_type}")
        sys.exit(1)

    # print(build_type)
    # print(clean_all_flag)

    targets=clean_targets[build_type]

    # print(targets)

    if clean_all_flag:

        targets_all=targets+clean_all_targets["public"]+clean_all_targets[build_type]
        # targets.append("__pycache__")
        # targets.append(".vscode/tasks.json")
        # targets.append(".vscode/launch.json")
        # targets.append(".vscode/c_cpp_properties.json")
        # targets.append(".vscode/settings.json")
    else:
        targets_all=targets
    # print(targets_all)

    if targets:
        
        build_path=Path.cwd() 
        print(f"Cleaning project in: {build_path}")

        for item in targets_all:
            full_path = build_path /  item
            remove_path(full_path)

        print("Clean completed.")

if __name__ == "__main__":
    main()

