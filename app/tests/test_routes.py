import pytest
from app.services.video_service import VideoService
from unittest.mock import MagicMock


def test_video_list(client, valid_auth_header, mock_minio):
    """Test retrieving a list of videos via the /api/v1/videos endpoint."""
    response = client.get('/api/v1/videos?page=1&per_page=5', headers=valid_auth_header)

    assert response.status_code == 200
    assert 'data' in response.json
    assert 'total' in response.json
    assert 'page' in response.json
    assert 'per_page' in response.json
    assert response.json['success'] is True

def test_video_upload(client, valid_auth_header, mock_minio):
    """Test uploading a video via the /api/v1/videos/upload endpoint."""
    with open('test_video.mp4', 'wb') as f:
        f.write(b"fake_video_content")

    # Upload at-least two videos as part of test, so that merge can be tested too.
    # IDs are sequential, video ids = [1,2]
    with open('test_video.mp4', 'rb') as video_file:
        data = {
            'video': video_file,
        }
        response = client.post('/api/v1/videos/upload', data=data, headers=valid_auth_header, content_type='multipart/form-data')

    assert response.status_code == 200
    assert response.json['success'] is True

    with open('test_video.mp4', 'rb') as video_file:
        data = {
            'video': video_file,
        }
        response = client.post('/api/v1/videos/upload', data=data, headers=valid_auth_header, content_type='multipart/form-data')

    assert response.status_code == 200
    assert response.json['success'] is True

def test_video_trim(client, valid_auth_header, mock_minio):
    """Test trimming a video."""
    data = {
        'start_time': 10,
        'end_time': 60
    }
    response = client.post('/api/v1/videos/1/trim', json=data, headers=valid_auth_header)

    assert response.status_code == 200
    assert response.json['success'] is True
    assert 'data' in response.json
    assert 'id' in response.json['data']

def test_video_merge(client, valid_auth_header, mock_minio):
    """Test merging multiple videos."""
    data = {
        'video_ids': ['1', '2'],
        'output_format': 'mp4'
    }
    response = client.post('/api/v1/videos/merge', json=data, headers=valid_auth_header)

    assert response.status_code == 200
    assert response.json['success'] is True
    assert 'data' in response.json
    assert 'filename' in response.json['data']


# Test share routes.

def test_create_share_link(client, valid_auth_header, mock_minio):
    """Test generating a share link for a video."""
    data = {
        'expires_in': 3600
    }
    response = client.post('/api/v1/videos/1/share', json=data, headers=valid_auth_header)

    assert response.status_code == 200
    assert response.json['success'] is True
    assert 'data' in response.json
    assert 'token' in response.json['data']
    return response.json['data']['token']

def test_get_shared_video(client,valid_auth_header,  mock_minio):
    """Test retrieving a shared video using a share token."""
    token = test_create_share_link(client, valid_auth_header, mock_minio)
    response = client.get('/api/v1/share/token', headers=valid_auth_header)

    assert response.status_code == 200
    assert response.json['success'] is True
    assert 'data' in response.json
    assert 'video_id' in response.json['data']
    assert 'url' in response.json['data']
