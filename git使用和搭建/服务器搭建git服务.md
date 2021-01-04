# 在CentOS7下搭建Git服务器

**环境**：

服务器：CentOS7+git

客户端：windows10+git

## 1.安装git

Linux作为服务端系统，Windows作为客户端系统，分别安装git

服务端：

```
yum install -y git
```

客户端：

下载 Git for Windows，地址：https://git-for-windows.github.io/

安装完之后，可以使用 Git Bash 作为命令行客户端

## 2.服务器端创建git用户

```
useradd -m 用户名    #添加用户
passwd 用户名     #为该用户设置密码
```

## 3.服务器端创建Git仓库

```
mkdir -p data/git/gittest.git #创建git仓库文件夹
git init --bare home/git/gittest.git #初始化git仓库
cd data/git
chrown -R git:用户名 gittest.git #将Git仓库的owner设为该用户
```

## 4.创建证书登录

**客户端创建ssh公钥和私钥**：

```
ssh-keygen -t rsa -C "邮箱"
```

此时 C:\Users\用户名\.ssh 下会多出两个文件 id_rsa 和 id_rsa.pub

id_rsa 是私钥

id_rsa.pub 是公钥

**服务器端Git打开RSA认证：**

进入/etc/ssh目录，编辑sshd-config，打开三个配置的注释：

```
RSAAuthentication yes
PubkeyAuthentication yes
AuthorizedKeysFile .ssh/authorized_keys
```

注：在 CentOS7.4 的配置文件中没有 RSAAuthentication 这一行，CentOS7.4相对于之前版本，做了一些与sshd相关的安全更新来加强sshd的安全性。其中之一就是弃用RSAAuthentication支持。

在用户的主目录里新建.ssh文件夹，然后在文件夹里新建文件authorized_keys,将客户端的id_rsa.pub公钥写进文件authorized_keys，一行一个。

## 5.客户端clone远程仓库

```
git clone 用户名@服务器IP地址:服务器上git仓库地址
如git clone ghy@192.168.100.23:/home/git/gittest.git
如果公网连接需在前面加上ssh:
git clone ssh://ghy@223.93.139.180:48080/home/git/gittest.git
```

# CentOS7安装部署Gitlab服务器

**环境**：

服务器：CentOS7

## 1.安装相关依赖

```
yum -y install policycoreutils openssh-server openssh-clients postfix
```

## 2.安装postfix，并设置开机自启动

```
systemctl enable postfix && systemctl start postfix
```

## 3.下载并安装Gitlab

添加gitlab镜像：

```
wget https://mirrors.tuna.tsinghua.edu.cn/gitlab-ce/yum/el7/gitlab-ce-10.0.0-ce.0.el7.x86_64.rpm
```

安装gitlab:

```
rpm -i gitlab-ce-10.0.0-ce.0.el7.x86_64.rpm
```

安装成功后：

![](img\安装成功.png)

## 4.配置gitlab的IP和端口

在文件gitlab.rb中设置gitlab的IP和端口：vim  /etc/gitlab/gitlab.rb

```
external_url 'http://192.168.100.23:8077'
```

## 5. 重新配置并启动Gitlab

```
配置:gitlab-ctl reconfigure
启动:gitlab-ctl restart
```

## 6. 配置防火墙

```
# 开启防火墙
systemctl start firewalld
systemctl enable firewalld
# 开发所需服务
firewall-cmd --permanent --add-service ssh
firewall-cmd --permanent --add-service http
firewall-cmd --permanent --add-service https
firewall-cmd --reload
```

## 7.访问

通过192.168.100.23:8077连接，登录界面

![登录页面](\img\登录页面.png)**遇到过的问题:**

1. 登录报错：

   ![502错误](img\502错误.png)

   **可能原因：**

   **1.运行内存不足**：gitlab的运行内存要大于4G

   **2.端口被占用:**

   查看GitLab状态：

   ```
   gitlab-ctl status
   ```

   ![promentheus端口启动失败](img\promentheus端口启动失败.png)

   网上找的修复命令：

   ```
   sudo -u gitlab-prometheus python -c "import leveldb; leveldb.RepairDB('/var/opt/gitlab/prometheus/data/archived_fingerprint_to_metric')"
   ```

   修改以后还是不行，后来发现prometheus端口默认是9090，所以和现在设置的端口冲突，所以讲gitlab端口改为了8077。

   修改后还是不能登录，继续查看GitLab状态，发现unicorn的pid一直在变大。因为设置了unicorn的端口为8077，又冲突了，所以修改文件**/etc/gitlab/gitlab.rb** ：

   ```
   unicorn['port'] = 8055
   ```

   注意：还要修改文件**/var/opt/gitlab/gitlab-rails/etc/unicorn.rb**的端口

   端口修改后重新载入配置文件并开启：

   ```
   配置:gitlab-ctl reconfigure
   启动:gitlab-ctl restart
   ```

   **3.权限问题**

   ```
   chmod -R 755    /var/log/gitlab
   ```

2. pull时报错”remote: error: insufficient permission for adding an object to repository database ./objects“`

   原因：该账号没有该仓库的权限；

   解决方法：把上面的文件夹权限改为777

   ```git
   chmod -R 777 仓库文件夹名
   ```

   或者给账号开通权限：

   ```git
   usermod -a -G groupA use
   ```

   

