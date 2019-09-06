### How to get this massive CSV in to a database so you can see it in grafana

0. Make sure your csv files are avilable in the volumes
1. Deploy the dockcer-compose.yml file using. Run from this folder
```
sudo docker-compose up -d
```

2. you should now have a grafana and mysql instance you can use.
3. connect to the mariadb datbase container by running
```
sudo docker exec -it datahack-db bash
```
Connect to the mysql console so you ran run commands. Namely (take password from the docker-compose.yml variable:

```
mysql -uroot -p

```
```
--> CREATE TABLE sessions (id INT, network_id INT, device_id VARCHAR(100), timestamp datetime, host VARCHAR(100), host_ip VARCHAR(100), port_dst INT, transport_protocol VARCHAR(10), service_device_id INT, packets_count INT, outbound_bytes_count INT, inbound_bytes_count INT, packet_loss FLOAT, retransmit_count INT, latency VARCHAR(100), session_count INT, outbound_packets_count INT, inbound_packets_count INT, outbound_bytes_max INT, outbound_bytes_min INT, outbound_bytes_mean FLOAT, outbound_bytes_median FLOAT, outbound_bytes_stddev FLOAT, inbound_bytes_max INT, inbound_bytes_min INT, inbound_bytes_mean FLOAT, inbound_bytes_median FLOAT, inbound_bytes_stddev FLOAT, outbound_packet_size_max FLOAT, outbound_packet_size_min FLOAT, outbound_packet_size_mean FLOAT, outbound_packet_size_median FLOAT, outbound_packet_size_stddev FLOAT, inbound_packet_size_max FLOAT, inbound_packet_size_min FLOAT, inbound_packet_size_mean FLOAT, inbound_packet_size_median FLOAT, inbound_packet_size_stddev FLOAT );


-->  CREATE TABLE devices ( id VARCHAR(100), network_id VARCHAR(100), device_id VARCHAR(100), type VARCHAR(100), model VARCHAR(100), manufacturer VARCHAR(100), operating_system VARCHAR(100), operating_system_version VARCHAR(100) );
  
--> LOAD DATA INFILE "/mnt/iso/dataset_datahack/all_devices.csv"
  INTO TABLE sessions
  FIELDS TERMINATED BY ','
  LINES TERMINATED BY '\n' ;
  
->> CREATE INDEX ix_timestamp ON armis.sessions(timestamp);
```

You can then enter grafana and use regular SQL calls
