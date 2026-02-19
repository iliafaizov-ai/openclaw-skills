# Krea.ai Image Models Reference

## ✅ Verified Working Models (API Access)

### Flux 1.1 Pro Ultra (`bfl/flux-1.1-pro-ultra`)
- **Cost**: 47 credits
- **Generation time**: ~10-18 seconds
- **Quality**: Excellent for general purpose
- **Best for**: Architectural visualization, fast iterations, general scenes
- **Max dimensions**: 1536x1536
- **Special features**: Raw mode for better prompt adherence
- **Endpoint**: `/generate/image/bfl/flux-1.1-pro-ultra`

**Parameters:**
```json
{
  "prompt": "string",
  "width": 1536,
  "height": 1024,
  "batchSize": 1,
  "seed": 12345,  // optional
  "raw": true     // recommended
}
```

### Nano Banana Pro (`google/nano-banana-pro`)
- **Cost**: 119 credits
- **Generation time**: ~30-40 seconds  
- **Quality**: Highest quality, native 4K support
- **Best for**: Final production, 4K output, image editing, portraits
- **Resolutions**: 1K, 2K, 4K
- **Special features**: Image-to-image, style references, aspect ratio presets
- **Endpoint**: `/generate/image/google/nano-banana-pro`

**Parameters:**
```json
{
  "prompt": "string",
  "aspectRatio": "16:9",  // or 1:1, 4:3, 9:16, etc.
  "resolution": "2K",     // 1K, 2K, or 4K
  "batchSize": 1,
  "imageUrls": ["https://..."],  // optional, for image-to-image
  "styleImages": [               // optional, for style reference
    {"url": "https://...", "strength": 0.8}
  ]
}
```

## ❌ NOT Available via API

The following models appear in documentation but return errors:

- **Seedream-4**: 404 Endpoint not found
- **Imagen 4 Ultra**: 500 Internal Server Error  
- **ChatGPT Image**: 404 Endpoint not found
- **All other text-to-image models**: Not accessible

## Model Comparison

| Model | Cost | Time | Resolution | Best Use Case |
|-------|------|------|------------|---------------|
| **Flux 1.1 Pro Ultra** | 47 CR | ~15s | Up to 1536² | Fast iterations, architectural viz |
| **Nano Banana Pro 1K** | 119 CR | ~35s | ~1024² | Quick high-quality |
| **Nano Banana Pro 2K** | 119 CR | ~40s | ~2048² | Production quality |
| **Nano Banana Pro 4K** | 119 CR | ~45s | ~4096² | Ultra-high resolution |

## Cost Optimization

**Development workflow:**
1. Use **Flux 1.1 Pro Ultra** for rapid prototyping (47 CR, ~15s)
2. Switch to **Nano Banana Pro 2K** for final renders (119 CR, ~40s)
3. Use **4K** only when absolutely needed

**Batch generation:**
- Both models support `batchSize` up to 4
- Cost scales linearly (4 images = 4x credits)

## Aspect Ratios (Nano Banana Pro)

Supported ratios:
- `21:9` - Ultra-wide cinematic
- `16:9` - Standard wide (recommended for architecture)
- `9:16` - Vertical/portrait  
- `4:3` - Classic photography
- `3:2` - DSLR standard
- `2:3` - Portrait DSLR
- `5:4` - Large format
- `4:5` - Instagram portrait
- `3:4` - Vertical classic
- `1:1` - Square

## Image-to-Image Workflow

Nano Banana Pro supports image reference:

1. **Upload reference image** to Krea.ai assets:
```bash
curl -X POST \
  -H "Authorization: Bearer $KREA_API_KEY" \
  -F "file=@input.jpg" \
  https://api.krea.ai/assets
```

2. **Use returned URL** in generation:
```json
{
  "prompt": "Transform into epic beach scene...",
  "imageUrls": ["https://app-uploads.krea.ai/..."],
  "resolution": "2K"
}
```

## Tested Use Cases

### ✅ Architectural Visualization
- **Model**: Nano Banana Pro 2K
- **Prompt length**: Up to ~500-800 words works well
- **Aspect ratio**: 16:9
- **Result**: Photorealistic renders in ~42s

### ✅ Portrait Enhancement  
- **Model**: Nano Banana Pro 2K
- **Method**: Image-to-image with reference photo
- **Aspect ratio**: 9:16 for full-body
- **Result**: Natural transformation with face preservation

### ✅ Concept Art
- **Model**: Flux 1.1 Pro Ultra
- **Batch size**: 4 for variations
- **Time**: ~15s for 4 images
- **Result**: Fast iteration for creative exploration

## API Quirks & Gotchas

1. **User-Agent Required**: Must include browser User-Agent header to bypass Cloudflare
2. **Response Format**: Returns `result.urls` array, not `images`
3. **Prompt Length**: Keep under ~1000 chars for Nano Banana Pro to avoid errors
4. **Download Protection**: Image URLs also require User-Agent header
5. **Resolution Parameter**: Only works with Nano Banana Pro, ignored by Flux

## Error Handling

**"Internal Error"**
- Cause: Prompt too long or invalid parameters
- Solution: Shorten prompt to <1000 chars, verify aspect ratio

**"Endpoint not found"**  
- Cause: Model not available via API
- Solution: Use Flux or Nano Banana Pro only

**403 Forbidden**
- Cause: Missing User-Agent header
- Solution: Add browser User-Agent to all requests

## Future Enhancements Available

### Image Enhancement
- **Bloom**: Creative upscale to 8x (~256 CR)
- **Topaz**: Fast upscale to 22K (~51 CR)
- **Topaz Generative**: Slow high-quality (~137 CR)

Endpoints exist but not yet integrated into script.

### Video Generation
See [video-models.md](video-models.md) for complete video generation guide.

## Best Practices

1. **Start with Flux** for concept validation
2. **Use Nano Banana Pro** for production
3. **Batch when possible** for variations
4. **Keep prompts focused** - quality over quantity
5. **Test aspect ratios** before high-res generation
6. **Save successful prompts** for reuse
7. **Track credits** to optimize workflow

## Example Workflows

### Quick Iteration Loop
```bash
# 1. Fast concepts (47 CR, 15s)
python3 generate.py --model bfl/flux-1.1-pro-ultra --batch-size 4

# 2. Select best concept, refine in 2K (119 CR, 40s)
python3 generate.py --model google/nano-banana-pro --resolution 2K

# 3. Final 4K if needed (119 CR, 45s)
python3 generate.py --model google/nano-banana-pro --resolution 4K
```

### Image-to-Image Transform
```bash
# Upload asset first, get URL, then:
python3 generate.py \
  --model google/nano-banana-pro \
  --prompt "Epic transformation..." \
  --image-url https://app-uploads.krea.ai/... \
  --resolution 2K
```
