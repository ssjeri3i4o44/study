### pycharm使用git

https://www.cnblogs.com/csmashang/p/12659045.html

1.pycharm配置git环境：

File-->Sittings-->Version Control-->Git,然后在 Path to Git executable中选择本地的git.exe路径：

一般地址为默认的C:\Program Files\Git\cmd\git.exe；

2.从版本库克隆项目：

VCS-->Get from Version Control-->Git--Repository URL:

URL:GitLab版本库地址

Directory:项目工作路径

3.向Git仓库添加文件：

- 在pycharm中任意新建一个文件，默认是红色的，但是会弹出一个对话框（你想要将以下文件添加到Git吗），点击Add后，文件变成绿色，表示进入暂存区。
- 点击pycharm右上角的绿色小勾，pycharm左侧会显示Default Changelist,填写commit之后提交。

4.分支与合并

创建分支：VSC-->Git-->Branches-->New Branch

分支合并到Master：首先VCS-Git-Branches-master -->checkout,切换到 master 分支上，然后VCS-Git-Merge Changes，从Branches to merge 选项框里面选择需要合并的分支，前面不带 remotes/的是本地分支，带remotes/是远程分支。填写commit Message后就可以点击merge,此时代码已经合并到本地的 master 分支上了(此时只是本地仓库的合并，并没有合并到远程仓库)。接下来push下就可以推送到远程仓库了。

文件名颜色代表不同的文件状态：

红色， 表示在工作区

绿色， 表示在暂存区

蓝色， 表示文件有修改，位于暂存区

无颜色：表示位于本地仓库区域或者已经提交到远程仓库区。

