### How to spin up just minio
Run the below command from root of the project. This will spin up the minio container in detached and tty session mode [ref](https://min.io/docs/minio/container/index.html)
```
docker run \
    -p 9000:9000 -p 9090:9090 \
    -v $(pwd)/local/minio/data:/mnt/data \
    -v $(pwd)/minio.config.env:/etc/config.env \
    -e "MINIO_CONFIG_ENV_FILE=/etc/config.env" \
    --name "minio" \
    quay.io/minio/minio:RELEASE.2024-11-07T00-52-20Z-cpuv1 server /mnt/data --console-address ":9090"
```