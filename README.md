# Prometheus monitor port
# 使用文档

依赖: \
   python3.* \
   pyyaml==5.1.2 \
   prometheus_client==0.7.1 \
   flask==1.1.1
   
安装依赖: \
   1、安装python3.* \
   2、pip3 install -r requirements.txt
   
安装路径: \
   可安装至任意路径 \
   将 export_moniotr_port.py 、 host_port_conf.yaml 放在同级路径

配置文件: \
   host_port_conf.yaml \
   示例:
```
elasticsearch:
  host:
    - "192.168.7.41"
    - "192.168.7.42"
    - "192.168.7.43"
  port:
    - 9200
    - 9300
zookeeper:
  host:
    - "192.168.7.51"
    - "192.168.7.52"
    - "192.168.7.53"
  port:
    - 2181
```

   说明:
```
最外层key为服务名称，自定义服务名称
  host:为固定key，不可以变
    - "服务器ip"
  port:
    - 端口
注意:
  新增或者删除某项端口监控,不需要重启端口监控服务
```
          

启动方式: \
   nohup python3 export_moniotr_port.py &

修改端口: \
   app.run(host="0.0.0.0", port=31672, debug=True) 中修改 31672 端口为自己要用的端口 \

prometheus数据抓取配置:
```
    scrape_configs:
    - job_name: 'monitor-port'
      scrape_interval: 10s
      static_configs:
      - targets:
        - "ip:port"
```

prometheus监控报警配置:
```
    - alert: Zookeeper 端口未探测到
      expr: server_port_up{sertype=="zookeeper"} != 1
      for: 3m
      labels:
        severity: "非常严重"
      annotations:
        summary: "{{$labels.host}}:{{$labels.port}} 端口未探测到"
        description: "请到服务器查看"
```
