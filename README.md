一般修改project_path即可

流程是先把project_path里的jar包和class拷贝到jar1目录，当然如果目录下设置了dec-whilelist.txt就会跳过。

然后调用java-decompiler.jar反编译，生成结果在zip目录下。

最后将zip下的文件解压到src/java/main目录