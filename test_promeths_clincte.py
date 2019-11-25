# Prometheus monitor server port.
# YangLin
# -*- coding:utf-8 -*-
import prometheus_client
from prometheus_client import Gauge,Counter
from prometheus_client.core import CollectorRegistry, REGISTRY
from flask import Response, Flask

app = Flask(__name__)
port_up = Gauge("Server_port", "monitor server port status.",["host","port"])
REGISTRY = CollectorRegistry(auto_describe=False)
muxStatus = Gauge("mux_api_21", "Api response stats is:", ["host", "port"], registry=REGISTRY)
manageStatus = Counter("manage_api_21", "Api response stats is:", ["host", "port"], registry=REGISTRY)


@app.route("/metrics")
def ApiResponse():
    # port_up.labels("192.168.1.22","2181").set(0)
    # port_up.labels("192.168.2.22", "2181").set(1)
    # print(type(port_up))
    a = [{"sertype": "zookeeper", "host": "192.168.1.22", "port": "2181", "status": 0},
         {"sertype": "zookeeper", "host": "192.168.1.23", "port": "2181", "status": 1}]
    for i in a:
        ip = "".join(i.get("host"))
        port = "".join(i.get("port"))
        status = i.get("status")
        muxStatus.labels(ip, port).set(status)
        manageStatus.labels(ip, port).inc()
    # manageStatus.labels("192.168.1.23","2181").inc()
    # return Response(prometheus_client.generate_latest(port_up),
    return Response(prometheus_client.generate_latest(REGISTRY),
                    mimetype="text/plain")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=31672, debug=True)
