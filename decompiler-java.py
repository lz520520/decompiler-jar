# coding:utf-8

import os
import zipfile
import shutil
import sys
# !!!!!!! 需要修改成自己的路径
java_decompiler_path = r"fernflower.jar"
jdk_path = r"D:\environ\Java\jdk-11.0.12\bin\java.exe"
# program_params = r"-cp \"%s\" org.jetbrains.java.decompiler.main.decompiler.ConsoleDecompiler -dgs=true" % java_decompiler_path
program_params = "-jar \"%s\" -dgs=true" % java_decompiler_path


whitelist_name = "dec-whilelist.txt"

def get_jar_files(filepath):
    # 白名单过滤
    jarfiles = []
    files = os.listdir(filepath)  # 列出文件夹下所有的目录与文件
    for fi in files:
        fi_d = os.path.join(filepath, fi)
        if "java-decompiler.jar" in fi_d:
            continue
        if os.path.isdir(fi_d):
            if os.path.exists(os.path.join(fi_d, whitelist_name)):
                continue
            jarfiles += get_jar_files(fi_d)
        elif fi_d.endswith(".jar"):
            jarfiles.append(fi_d)
    return jarfiles



def get_all_jar_files(filepath):
    # 无白名单过滤
    jarfiles = []
    files = os.listdir(filepath)  # 列出文件夹下所有的目录与文件
    for fi in files:
        fi_d = os.path.join(filepath, fi)
        if "java-decompiler.jar" in fi_d:
            continue
        if os.path.isdir(fi_d):
            jarfiles += get_all_jar_files(fi_d)
        elif fi_d.endswith(".jar"):
            jarfiles.append(fi_d)
    return jarfiles

def get_class_files(filepath):
    # 白名单过滤
    jarfiles = []
    files = os.listdir(filepath)  # 列出文件夹下所有的目录与文件
    for fi in files:
        fi_d = os.path.join(filepath, fi)
        if os.path.isdir(fi_d):
            if os.path.exists(os.path.join(fi_d, whitelist_name)):
                continue
            jarfiles += get_class_files(fi_d)
        elif fi_d.endswith(".class"):
            jarfiles.append(fi_d)
    return jarfiles

def get_all_class_files(filepath):
    # 无把名单过滤
    jarfiles = []
    files = os.listdir(filepath)  # 列出文件夹下所有的目录与文件
    for fi in files:
        fi_d = os.path.join(filepath, fi)
        if os.path.isdir(fi_d):
            jarfiles += get_all_class_files(fi_d)
        elif fi_d.endswith(".class"):
            jarfiles.append(fi_d)
    return jarfiles

if __name__ == "__main__":
    # 只要修改project_path即可
    project_path = "webapps"
    jar_path = "decompiler\\jar1"
    zip_path = "decompiler\\zip"
    dst_path = "decompiler\\src\\main\\java"
    jar_files = get_jar_files(project_path)
    print(jar_files)




    # 删除目录
    if os.path.exists(zip_path):
        shutil.rmtree(zip_path)

    if os.path.exists(jar_path):
        shutil.rmtree(jar_path)

    if os.path.exists(dst_path):
        shutil.rmtree(dst_path)


    # 拷贝文件
    if not os.path.exists(jar_path):
        os.makedirs(jar_path, exist_ok=True)
    jar_allfiles = get_all_jar_files(project_path)
    for file in jar_allfiles:
        shutil.copy(file, jar_path)


    for file in jar_files:
        try:
            newdir = os.path.join(zip_path, os.path.splitext(file)[0])
            if not os.path.exists(newdir):
                os.makedirs(newdir, exist_ok=True)
            packname = os.path.join(newdir, os.path.basename(file))
            cmd = "%s %s \"%s\" \"%s\"" % \
                  (jdk_path, program_params, file, newdir)
            print(cmd)
            os.system(cmd)

            zip_file = zipfile.ZipFile(packname)
            # 这里提取到dst_path，而不是zip
            zip_file.extractall(dst_path)
            zip_file.close()
            # os.remove(packname)
        except Exception as e:
            ferr = open("error.log", "a+")
            ferr.write(file + "\r\n")
            ferr.write(str(e))
            ferr.close()
            print(e)


    print("[+] decompiler jar over.")
    class_files = get_class_files(project_path)


    class_allfiles = get_all_class_files(project_path)
    for file in class_allfiles:
        shutil.copy(file, jar_path)

    project_path_tmp = project_path
    if not jar_path.endswith("\\"):
        project_path_tmp = project_path + "\\"    


    for file in class_files:
        try:

            newdir = os.path.join(dst_path, os.path.dirname(file).split(project_path_tmp, 1)[1])
            if not os.path.exists(newdir):
                os.makedirs(newdir, exist_ok=True)
            cmd = "%s %s \"%s\" \"%s\"" % \
                  (jdk_path, program_params, file, newdir)
            os.system(cmd)
        except Exception as e:
            ferr = open("error.log", "a+")
            ferr.write("\r\n"+file + "\r\n")
            ferr.write(str(e))
            ferr.close()
            print(e)
    print("[+] decompiler class over.")

#