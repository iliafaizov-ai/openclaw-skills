# Krea.ai Models Reference

## Available Models

### Flux 1.1 Pro Ultra (`bfl/flux-1.1-pro-ultra`)
- **Cost**: 47 credits
- **Generation time**: ~18 seconds
- **Quality**: Excellent architectural and scene accuracy
- **Best for**: Professional visualizations, architectural renders, detailed scenes
- **Supports raw mode**: Yes (recommended for better prompt adherence)
- **Max dimensions**: 1536x1536

### Imagen 4 Ultra (`google/imagen-4-ultra`)
- **Cost**: 47 credits
- **Generation time**: ~30 seconds
- **Quality**: High-quality photorealistic images
- **Best for**: Photorealistic scenes, complex compositions
- **Max dimensions**: 1536x1536

### Seedream 4 (`seedream-4`)
- **Cost**: 24 credits
- **Generation time**: ~20 seconds
- **Quality**: Good quality, faster generation
- **Best for**: Quick iterations, concept exploration
- **Max dimensions**: 1536x1536

### ChatGPT Image (`gpt-image`)
- **Cost**: 184 credits
- **Generation time**: ~60 seconds
- **Quality**: Best prompt adherence
- **Best for**: Complex prompts requiring precise interpretation
- **Max dimensions**: 1536x1536

### Nano Banana Pro (`nano-banana-pro`)
- **Cost**: 119 credits
- **Generation time**: ~30 seconds
- **Quality**: Native 4K support
- **Best for**: Ultra-high resolution output
- **Max dimensions**: 4096x4096

## Cost Optimization

- **Development**: Use `seedream-4` (24 credits) for quick iterations
- **Production**: Use `bfl/flux-1.1-pro-ultra` (47 credits) for final renders
- **Complex prompts**: Use `gpt-image` (184 credits) when prompt accuracy is critical
- **4K output**: Use `nano-banana-pro` (119 credits) for maximum resolution

## Model Selection Guide

1. **Architectural visualization**: `bfl/flux-1.1-pro-ultra` with `raw=true`
2. **Quick prototypes**: `seedream-4`
3. **Photorealistic scenes**: `google/imagen-4-ultra`
4. **Complex prompts**: `gpt-image`
5. **Ultra-high res**: `nano-banana-pro`

## API Workflow

1. **Submit job** via POST to model-specific endpoint
2. **Poll job status** via GET `/jobs/{job_id}` every 5 seconds
3. **Download images** from URLs in completed job response
4. **Track credits** from `credits_used` field in response
