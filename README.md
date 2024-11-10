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

For this project we'll need to create "videos" bucket manually for now, but it can be automated to certain extent.

### Curl requests for different routes

- GET /api/v1/videos
```
curl -X GET http://localhost:5000/api/v1/videos \
  -H "Authorization: Bearer test-token"
```

- POST /api/v1/videos/upload
```
curl --location 'http://localhost:5000/api/v1/videos/upload' \
  --header 'Authorization: Bearer test-token' \
  --form 'video=@"/absolure/path/to/video.mp4"'
```

- GET /api/v1/videos/<video_id>
```
curl -X GET http://localhost:5000/api/v1/videos/<video_id> \
  -H "Authorization: Bearer test-token"
```

- POST /api/v1/videos/<video_id>/trim
```
curl -X POST http://localhost:5000/api/v1/videos/<video_id>/trim \
  -H "Authorization: Bearer test-token" \
  -H "Content-Type: application/json" \
  -d '{"start_time": "00:01:00", "end_time": "00:05:00"}'
```

- POST /api/v1/videos/merge
```
curl --location 'http://localhost:5000/api/v1/videos/merge' \
  --header 'Content-Type: application/json' \
  --header 'Authorization: Bearer test-token' \
  --data '{
      "video_ids": ["video1", "video2", "video3"]
  }'
```

- POST /api/v1/videos/<video_id>/share
```
curl -X POST http://localhost:5000/api/v1/videos/<video_id>/share \
  -H "Authorization: Bearer test-token"
```

- GET /share/<token>
```
curl -X GET http://localhost:5000/share/<token> \
  -H "Authorization: Bearer test-token"
```