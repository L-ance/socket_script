## 研发常用测试脚本




*  ### 服务端的代码, 运行直接 





    1.  打开 cmd 窗口  找到文件的路径 
 




        `python socket_recy.py 'your host' 'your port'`
        
            * your host:你的主机ip
            * your port:你的端口


    2.  详细参数会在代码里写到, 本代码主要用于测试,支持并发接受数据,并做了Ctrl+C的处理,将这个快捷操作做成简单的数据清除







*  ### 客户端的代码





    1.  打开一个新的 cmd 窗口,找到文件的路径


        `python socket_send.py 'your host' 'your port' 'times' 'large'`
        
            *times:要发送的此时
            *large:每次发送的大小
            
            
    2.  在客户端建立大量的套接字,需要大量占用计算机的端口,计算机在短时间内无法快速回收
    
        [解决方法](https://blog.csdn.net/stillfantasy1988/article/details/43196627)
#### 版本 python 2.7`
