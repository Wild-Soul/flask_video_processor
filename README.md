# About
Key features of this API layer:

1. Versioned API routes (v1)
2. Schema validation using marshmallow
3. RESTful resource organization
4. Swagger/OpenAPI documentation
5. Authentication middleware
6. Response formatting consistency
7. CORS support
8. Factory pattern for app creation

The API endpoints follow REST conventions:

```
GET    /api/v1/videos              - List all videos
POST   /api/v1/videos/upload       - Upload a new video
GET    /api/v1/videos/<id>         - Get video details
DELETE /api/v1/videos/<id>         - Delete a video
POST   /api/v1/videos/<id>/trim    - Trim a video
POST   /api/v1/videos/merge        - Merge multiple videos
POST   /api/v1/videos/<id>/share   - Create share link
GET    /api/v1/share/<token>       - Access shared video
```

- swagger ui:
  - ```http://localhost:<port[5000]>/swagger-ui```

# Setup
- Pre-requisites:
  - minio
    - a bucket named "videos" in minio
  - ffmpeg

## How to setup locally
- make a virutal python env ```python -m venv .venv``
- activate it ```source .venv/bin/activate```
- install requirements ```pip install -r requirements.txt```
- make sure ffmpeg is installed in your system
- start development server: ```python run.py```
- start production server: ```gunicorn wsgi:app --bind=0.0.0.0:5000```

## Runningn using docker
- requires docker
- docker compose
  - ```docker-compose up```
- create a new bucket **videos** after logging into minio at ```localhost:9000```

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

# Current architecture:
- a very simple overview:
```
client <-> server <-> minio
                  <-> sqlite
```
- currently video processing happens synchronously, which can take time.
  - for small videos (35 MB max) it might be fast/quick, but as the size grows this approach/setup won't work.
  - ideally we should be offloading video processing task to background worker through message queue.
  - this will decouple the API and worker and each can be individually scaled.
  - it'll also allow up to setup retry/DLQ.

# References:
- [Flask + marshmallow + swagger](https://medium.com/@adeesh999/marshmallow-flask-swagger-21764b432a55)
- [Flask + minio](https://medium.com/data-engineering-indonesia/how-to-upload-files-from-flask-to-minio-on-docker-14aade73596f)
- [Flask + SQLAlchemy](https://www.digitalocean.com/community/tutorials/how-to-use-flask-sqlalchemy-to-interact-with-databases-in-a-flask-application)
