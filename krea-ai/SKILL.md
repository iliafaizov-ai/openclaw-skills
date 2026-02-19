---
name: krea-ai
description: Generate high-quality images and videos using Krea.ai API. Currently supports Flux 1.1 Pro Ultra (text-to-image) and Nano Banana Pro (text-to-image, image-to-image, up to 4K). Use when you need professional image generation, architectural visualization, or creative editing beyond standard DALL-E capabilities. Also supports video generation (Kling, Veo, Sora, Runway) and image enhancement (Bloom, Topaz).
---

# Krea.ai Image & Video Generation

Professional AI generation using Krea.ai's advanced models.

## Prerequisites

- **API Key**: Set `KREA_API_KEY` environment variable
- **Format**: `{client_id}:{secret}` (not Bearer token)
- **Documentation**: https://docs.krea.ai

## Available Models

### ✅ Text-to-Image (Verified Working)

**Flux 1.1 Pro Ultra** (`bfl/flux-1.1-pro-ultra`)
- Cost: 47 credits
- Time: ~10-18 seconds
- Best for: General purpose, architectural visualization
- Max resolution: 1536x1536
- Example:
```bash
python3 scripts/generate.py \
  --prompt "Your prompt" \
  --model bfl/flux-1.1-pro-ultra \
  --width 1536 --height 1024
```

**Nano Banana Pro** (`google/nano-banana-pro`)
- Cost: 119 credits
- Time: ~30-40 seconds
- Best for: 4K generation, image editing, highest quality
- Resolutions: 1K, 2K, 4K (native 4K support!)
- Supports image-to-image with reference URLs
- Example:
```bash
python3 scripts/generate.py \
  --prompt "Your prompt" \
  --model google/nano-banana-pro \
  --aspect-ratio 16:9 \
  --resolution 2K
```

### 🎥 Video Generation (Available)

See [references/video-models.md](references/video-models.md) for complete list.

**Top choices:**
- **Kling 2.6**: Newest with native audio (387-804 CR, 5-10s)
- **Veo 3.1**: Google frontier with audio (758-1505 CR, 4-8s)
- **Sora 2**: OpenAI model (311-922 CR, 4-12s)
- **Runway Gen-4.5**: Cinematic quality (197-199 CR, 5-10s)

Endpoints: `/generate/video/{provider}/{model}`

### 🔧 Image Enhancement (Available)

- **Bloom**: Creative upscale to 8x (~256 CR, ~132s)
- **Topaz**: Up to 22K resolution (~51 CR, ~19s)
- **Topaz Generative**: Slower, higher quality (~137 CR, ~96s)

## Quick Start

```bash
export KREA_API_KEY="your-client-id:your-secret"

# Flux (fast, general purpose)
python3 scripts/generate.py \
  --prompt "Architectural visualization..." \
  --model bfl/flux-1.1-pro-ultra \
  --width 1536 --height 1024

# Nano Banana Pro (4K, best quality)
python3 scripts/generate.py \
  --prompt "Epic scene..." \
  --model google/nano-banana-pro \
  --aspect-ratio 16:9 \
  --resolution 4K

# Image-to-image with Nano Banana Pro
python3 scripts/generate.py \
  --prompt "Transform this into..." \
  --model google/nano-banana-pro \
  --image-url https://your-image-url.png \
  --resolution 2K
```

## Script Parameters

### Common
- `--prompt`: Image generation prompt (required)
- `--model`: Model name (default: `bfl/flux-1.1-pro-ultra`)
- `--batch-size`: Number of images (default: 1, max: 4)
- `--output-dir`: Output directory (default: `./output`)

### Flux-specific
- `--width`: Image width (default: 1536)
- `--height`: Image height (default: 1024)
- `--seed`: Random seed for reproducibility
- `--no-raw`: Disable raw mode (raw=true recommended for better results)

### Nano Banana Pro-specific
- `--aspect-ratio`: Aspect ratio (21:9, 1:1, 4:3, 3:2, 2:3, 5:4, 4:5, 3:4, 16:9, 9:16)
- `--resolution`: Resolution (1K, 2K, 4K)
- `--image-url`: Reference image URL (for image-to-image, can specify multiple)

## Output

The script:
1. Submits job and prints job ID
2. Polls job status every 5 seconds
3. Downloads images when complete
4. Prints JSON metadata:

```json
{
  "job_id": "abc123",
  "model": "google/nano-banana-pro",
  "prompt": "...",
  "images": ["/path/to/output/abc123_00.png"],
  "credits_used": "unknown"
}
```

## Usage Patterns

### Architectural Visualization (Tested)

**EXPO Russia 2025 Example:**
```bash
python3 scripts/generate.py \
  --prompt "Circular dome pavilion, 360° LED environment, five nevalyashka dolls 7m tall with cosmic projections, black mirror floor, suspended spheres..." \
  --model google/nano-banana-pro \
  --aspect-ratio 16:9 \
  --resolution 2K
```

Result: Photorealistic 2K render in ~42 seconds.

### Portrait Enhancement

```bash
python3 scripts/generate.py \
  --prompt "Epic beach scene, muscular athletic man, palm trees, white sand..." \
  --model google/nano-banana-pro \
  --image-url https://your-reference-photo.jpg \
  --aspect-ratio 9:16 \
  --resolution 2K
```

### Quick Iterations

Use Flux for fast iterations:
```bash
python3 scripts/generate.py \
  --prompt "Concept sketch..." \
  --model bfl/flux-1.1-pro-ultra \
  --batch-size 4
```

## Important Notes

### API Quirks Discovered

1. **User-Agent Required**: Must include `User-Agent` header to bypass Cloudflare protection
2. **Response Format**: Uses `result.urls` not `images` array
3. **Endpoint Naming**: Nano Banana Pro uses `/google/` prefix despite being in-house model
4. **Prompt Length**: Keep prompts under ~1000 chars for Nano Banana Pro to avoid errors

### Model Availability

**Currently NOT available via API** (as of 2026-02-19):
- Seedream-4 (404 endpoint not found)
- Imagen 4 Ultra (500 internal error)
- ChatGPT Image (404)
- Most other text-to-image models listed in docs

**Confirmed working:**
- Flux 1.1 Pro Ultra ✅
- Nano Banana Pro ✅
- Video models (endpoints exist, not tested)
- Enhance models (endpoints exist, not tested)

## Cost Optimization

- **Development**: Flux 1.1 Pro Ultra (47 CR, ~10s)
- **Production/Final**: Nano Banana Pro 2K (119 CR, ~40s)
- **Ultra-high res**: Nano Banana Pro 4K (119 CR, ~40s)
- **Batch processing**: Use batch-size for variations

## Troubleshooting

### "Internal Error"
- Prompt too long (>1000 chars)
- Invalid aspect ratio or resolution
- Solution: Shorten prompt, check parameters

### "Endpoint not found"
- Model not available via API
- Solution: Use Flux or Nano Banana Pro

### Timeout
Increase max wait:
```bash
--max-wait 600  # 10 minutes
```

## Advanced: Video Generation

Video generation is available but requires different endpoints. Example:

```bash
curl -X POST \
  -H "Authorization: Bearer $KREA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Your video prompt",
    "duration": 5,
    "aspectRatio": "16:9"
  }' \
  https://api.krea.ai/generate/video/kling/kling-2.6
```

See full video model list: https://docs.krea.ai/llms.txt

## Integration Example

```python
import subprocess, json

result = subprocess.run([
    "python3", "scripts/generate.py",
    "--prompt", "Photorealistic architectural render",
    "--model", "google/nano-banana-pro",
    "--resolution", "2K",
    "--aspect-ratio", "16:9",
    "--output-dir", "./renders"
], capture_output=True, text=True)

metadata = json.loads(result.stdout)
print(f"Generated: {metadata['images']}")
```

## References

- [Video Models](references/video-models.md) - Complete video generation guide
- [Image Models](references/models.md) - All image models comparison
- [API Documentation](https://docs.krea.ai) - Official Krea.ai docs
