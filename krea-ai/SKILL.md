---
name: krea-ai
description: Generate high-quality images using Krea.ai API with professional models (Flux 1.1 Pro Ultra, Imagen 4 Ultra, Seedream 4, ChatGPT Image, Nano Banana Pro). Use when you need architectural visualizations, photorealistic renders, or high-quality image generation beyond standard DALL-E/GPT capabilities. Supports job-based polling, credit tracking, and multiple models with different quality/speed/cost tradeoffs.
---

# Krea.ai Image Generation

Generate professional-quality images using Krea.ai's advanced models.

## Prerequisites

- **API Key**: Set `KREA_API_KEY` environment variable
- **Documentation**: https://docs.krea.ai

## Quick Start

```bash
export KREA_API_KEY="your-key-here"

python3 scripts/generate.py \
  --prompt "Your detailed prompt" \
  --model bfl/flux-1.1-pro-ultra \
  --width 1536 \
  --height 1024 \
  --output-dir ./output
```

## Models

See [references/models.md](references/models.md) for complete model comparison.

**Quick reference:**
- **Development**: `seedream-4` (24 credits, ~20s)
- **Production**: `bfl/flux-1.1-pro-ultra` (47 credits, ~18s)
- **Complex prompts**: `gpt-image` (184 credits, ~60s)
- **4K output**: `nano-banana-pro` (119 credits, ~30s)

## Usage Patterns

### Architectural Visualization

```bash
python3 scripts/generate.py \
  --prompt "$(cat detailed-prompt.txt)" \
  --model bfl/flux-1.1-pro-ultra \
  --width 1536 \
  --height 1024 \
  --output-dir ./renders
```

**Tip**: Use `raw=true` (default for Flux) for better prompt adherence.

### Quick Iteration

```bash
python3 scripts/generate.py \
  --prompt "Concept sketch..." \
  --model seedream-4 \
  --batch-size 4 \
  --output-dir ./concepts
```

### High-Resolution Output

```bash
python3 scripts/generate.py \
  --prompt "Ultra-detailed scene..." \
  --model nano-banana-pro \
  --width 4096 \
  --height 4096 \
  --output-dir ./high-res
```

## Script Parameters

- `--prompt`: Image generation prompt (required)
- `--model`: Model name (default: `bfl/flux-1.1-pro-ultra`)
- `--width`: Image width in pixels (default: 1536)
- `--height`: Image height in pixels (default: 1024)
- `--batch-size`: Number of images to generate (default: 1)
- `--seed`: Random seed for reproducibility (optional)
- `--no-raw`: Disable raw mode for Flux models
- `--output-dir`: Output directory (default: `./output`)
- `--poll-interval`: Polling interval in seconds (default: 5)
- `--max-wait`: Maximum wait time in seconds (default: 300)

## Output

The script:
1. Submits job and prints job ID
2. Polls job status every 5 seconds
3. Downloads images when complete
4. Prints JSON metadata with file paths and credits used

**Example output:**
```json
{
  "job_id": "abc123",
  "model": "bfl/flux-1.1-pro-ultra",
  "prompt": "...",
  "images": [
    "/path/to/output/abc123_00.png"
  ],
  "credits_used": 47
}
```

## Cost Tracking

All models return `credits_used` in the job response. Track costs by:
- Logging credits from script output
- Reviewing model costs in [references/models.md](references/models.md)
- Using cheaper models (`seedream-4`) for development

## Best Practices

1. **Start cheap**: Use `seedream-4` for quick iterations
2. **Detailed prompts**: Write 300-500 word prompts for architectural work
3. **Batch wisely**: Use `--batch-size` for variations, but watch credit costs
4. **Save prompts**: Store successful prompts in text files for reuse
5. **Track costs**: Log `credits_used` from each generation

## Troubleshooting

### API Key Issues
```bash
export KREA_API_KEY="your-key-here"
echo $KREA_API_KEY  # Verify it's set
```

### Timeout Errors
Increase `--max-wait`:
```bash
--max-wait 600  # 10 minutes
```

### Model Not Found
Check model name spelling:
- `bfl/flux-1.1-pro-ultra`
- `google/imagen-4-ultra`
- `seedream-4`
- `gpt-image`
- `nano-banana-pro`

## Integration Example

```python
import subprocess
import json

result = subprocess.run([
    "python3", "scripts/generate.py",
    "--prompt", "Your prompt here",
    "--model", "bfl/flux-1.1-pro-ultra",
    "--width", "1536",
    "--height", "1024",
    "--output-dir", "./output"
], capture_output=True, text=True)

metadata = json.loads(result.stdout)
print(f"Generated: {metadata['images']}")
print(f"Cost: {metadata['credits_used']} credits")
```
