# node 服务部署流程
1、进入 node 项目路径
    /home/picoroot/node_proj
2、修改 Dockerfile 内容
    参考文件为 node_proj.dockerfile
3、根据项目需求修改依赖
    vim package.json
4、重新构建容器并启动
    docker build -t node_server .
    docker run -d -p 2229:2229 container ID
