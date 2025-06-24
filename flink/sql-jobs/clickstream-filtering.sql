-- Configure Flink Settings for Streaming and State Management
SET 'state.backend' = 'rocksdb';
SET 'state.backend.incremental' = 'true';
SET 'execution.checkpointing.mode' = 'EXACTLY_ONCE';
SET 'execution.checkpointing.interval' = '10s';
SET 'execution.checkpointing.min-pause' = '10s';
SET 'sql-client.execution.result-mode' = 'TABLEAU';
SET 'parallelism.default' = '1';

-- Load Required Jars
ADD JAR '/opt/flink/lib/flink-sql-connector-kafka-3.1.0-1.18.jar';
ADD JAR '/opt/flink/lib/flink-json-1.18.1.jar';
ADD JAR '/opt/flink/lib/iceberg-flink-runtime-1.18-1.5.0.jar';
ADD JAR '/opt/flink/lib/hadoop-common-2.8.3.jar';
ADD JAR '/opt/flink/lib/hadoop-hdfs-2.8.3.jar';
ADD JAR '/opt/flink/lib/hadoop-client-2.8.3.jar';
ADD JAR '/opt/flink/lib/flink-shaded-hadoop-2-uber-2.8.3-10.0.jar';
ADD JAR '/opt/flink/lib/bundle-2.20.18.jar';

-- Confirm Jars are Loaded
SHOW JARS;

DROP CATALOG IF EXISTS iceberg;
CREATE CATALOG iceberg WITH (
    'type' = 'iceberg',
    'catalog-impl' = 'org.apache.iceberg.rest.RESTCatalog',  -- Use REST catalog
    'uri' = 'http://iceberg-rest:8181',                     -- REST catalog server URL
    'warehouse' = 's3://warehouse/',                        -- Warehouse location
    'io-impl' = 'org.apache.iceberg.aws.s3.S3FileIO',       -- S3 file IO
    's3.endpoint' = 'http://minio:9000',                    -- MinIO endpoint
    's3.path-style-access' = 'true',                        -- Enable path-style access
    'client.region' = 'us-east-1',                          -- S3 region
    's3.access-key-id' = 'admin',                           -- MinIO access key
    's3.secret-access-key' = 'password'                     -- MinIO secret key
);

-- Define Kafka Source Table
DROP TABLE IF EXISTS order_source;
CREATE TABLE IF NOT EXISTS order_source (
    order_id STRING,
    user_id STRING,
    order_time TIMESTAMP_LTZ(3),
    items ARRAY<ROW<
        item_id STRING,
        product_name STRING,
        quantity INT,
        price DOUBLE
    >>,
    total_amount DOUBLE,
    payment_method STRING,
    shipping_address STRING,
    order_status STRING
) WITH (
    'connector' = 'kafka',
    'topic' = 'orders',
    'properties.bootstrap.servers' = 'broker:29092',
    'scan.startup.mode' = 'earliest-offset',
    'format' = 'json',
    'json.ignore-parse-errors' = 'true',
    'json.timestamp-format.standard' = 'ISO-8601'
);

-- Define Iceberg Sink Table
CREATE DATABASE IF NOT EXISTS iceberg.db;
DROP TABLE IF EXISTS iceberg.db.order_sink;
CREATE TABLE IF NOT EXISTS iceberg.db.order_sink (
    order_id STRING,
    user_id STRING,
    order_time TIMESTAMP_LTZ(3),
    total_amount DOUBLE,
    payment_method STRING,
    shipping_address STRING,
    order_status STRING
) WITH (
    'catalog-name' = 'iceberg',
    'format' = 'parquet'
);

-- Insert filtered orders (e.g., only delivered orders)
INSERT INTO iceberg.db.order_sink
SELECT
    order_id,
    user_id,
    order_time,
    total_amount,
    payment_method,
    shipping_address,
    order_status
FROM order_source
WHERE order_status = 'delivered';

