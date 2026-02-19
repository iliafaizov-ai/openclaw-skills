# Krea.ai Video Generation Models

Complete reference for video generation through Krea.ai API.

## Top Models (Recommended)

### Kling 2.6
- **Provider**: Kling
- **Features**: Native audio generation
- **Cost**: 387 CR (5s), 804 CR (10s)
- **Time**: ~84s (5s), ~125s (10s)
- **Endpoint**: `/generate/video/kling/kling-2.6`
- **Best for**: Videos with synchronized audio

### Veo 3.1
- **Provider**: Google
- **Features**: Frontier model with audio + reference images
- **Cost**: 758 CR (4s), 1098 CR (6s), 1505 CR (8s)
- **Time**: ~129s (4s), ~170s (6s), ~143s (8s)
- **Endpoint**: `/generate/video/veo/veo-3.1`
- **Best for**: High-quality cinematic videos

### Sora 2
- **Provider**: OpenAI
- **Features**: Rich detailed dynamic clips
- **Cost**: 311 CR (4s), 627 CR (8s), 922 CR (12s)
- **Time**: ~105s (4s), ~166s (8s), ~216s (12s)
- **Endpoint**: `/generate/video/sora/sora-2`
- **Best for**: Creative, artistic videos

### Runway Gen-4.5
- **Provider**: Runway
- **Features**: Latest frontier model, native text-to-video
- **Cost**: ~197-199 CR (5-10s)
- **Time**: ~47-52s
- **Endpoint**: `/generate/video/runway/runway-gen-4.5`
- **Best for**: Cinematic quality, consistent results

## Budget-Friendly Options

### Hailuo 2.3 Fast
- **Cost**: 256 CR (6s), 223 CR (10s)
- **Time**: ~135s (6s), ~108s (10s)
- **Endpoint**: `/generate/video/hailuo/hailuo-2.3-fast`
- **Best for**: Quick iterations, medium quality

### Seedance Pro Fast
- **Cost**: 39-208 CR (2-12s)
- **Time**: 35-93s
- **Endpoint**: `/generate/video/seedance/seedance-pro-fast`
- **Best for**: Cheap, fast generation (up to 12s)

## Request Format

All video endpoints accept similar parameters:

```json
{
  "prompt": "Your video description",
  "duration": 5,  // or 10, varies by model
  "aspectRatio": "16:9",  // or "9:16"
  "startImage": "https://...",  // optional, for image-to-video
  "endImage": "https://...",     // optional (some models)
  "generateAudio": true          // optional (audio-capable models)
}
```

## Complete Model List

| Model | Cost (5s) | Cost (10s) | Time | Audio | Max Duration |
|-------|-----------|------------|------|-------|--------------|
| Kling 2.6 | 387 CR | 804 CR | ~84s/~125s | ✅ | 10s |
| Veo 3.1 | 758 CR | 1505 CR | ~129s/~143s | ✅ | 8s |
| Veo 3.1 Fast | 307 CR | 617 CR | ~64s/~136s | ✅ | 8s |
| Sora 2 | 311 CR | 627 CR | ~105s/~166s | ❌ | 12s |
| Runway Gen-4.5 | 197 CR | 199 CR | ~47s/~52s | ❌ | 10s |
| Runway Gen-4 | 197 CR | 199 CR | ~47s/~52s | ❌ | 10s |
| Hailuo 2.3 Fast | 256 CR | 223 CR | ~135s/~108s | ❌ | 10s |
| Seedance Pro Fast | 97 CR | 192 CR | ~60s/~91s | ❌ | 12s |
| Kling 2.5 | 275 CR | 541 CR | ~94s/~136s | ❌ | 10s |
| Wan 2.5 | 589 CR | 1128 CR | ~132s/~240s | ❌ | 10s |

## Usage Examples

### Text-to-Video
```bash
curl -X POST \
  -H "Authorization: Bearer $KREA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A serene beach at sunset with waves gently rolling",
    "duration": 5,
    "aspectRatio": "16:9"
  }' \
  https://api.krea.ai/generate/video/kling/kling-2.6
```

### Image-to-Video
```bash
curl -X POST \
  -H "Authorization: Bearer $KREA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Camera slowly zooms in",
    "startImage": "https://your-image.png",
    "duration": 5,
    "aspectRatio": "16:9"
  }' \
  https://api.krea.ai/generate/video/kling/kling-2.6
```

### With Audio
```bash
curl -X POST \
  -H "Authorization: Bearer $KREA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "City street with traffic and pedestrians",
    "duration": 5,
    "generateAudio": true
  }' \
  https://api.krea.ai/generate/video/kling/kling-2.6
```

## Model Selection Guide

**For cinematic quality**: Veo 3.1, Runway Gen-4.5
**For audio**: Kling 2.6, Veo 3.1
**For speed**: Seedance Pro Fast, Hailuo 2.3 Fast
**For creativity**: Sora 2
**For budget**: Seedance Pro Fast (39-208 CR)
**For long videos**: Sora 2 (12s), Seedance Pro Fast (12s)

## Job Lifecycle

1. Submit via POST → get `job_id`
2. Poll `/jobs/{job_id}` every 5-10s
3. Status: queued → processing → completed
4. Download from `result.urls[0]`

Average completion times vary by model (see table above).

## Notes

- All endpoints return async jobs (no synchronous generation)
- Videos are returned as MP4/WebM URLs
- Audio models generate synchronized soundtracks
- Image-to-video requires publicly accessible image URLs
- Webhook support available via `X-Webhook-URL` header
