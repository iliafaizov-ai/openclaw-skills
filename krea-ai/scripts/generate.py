#!/usr/bin/env python3
"""
Krea.ai Image Generation Script
Generates high-quality images using Krea.ai API with job-based polling.
"""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Dict, Any, Optional


def make_request(
    url: str,
    api_key: str,
    method: str = "GET",
    data: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Make HTTP request to Krea.ai API."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    
    body = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, method=method, headers=headers, data=body)
    
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        payload = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Krea.ai API failed ({e.code}): {payload}") from e


def generate_image(
    api_key: str,
    prompt: str,
    model: str = "bfl/flux-1.1-pro-ultra",
    width: int = 1536,
    height: int = 1024,
    batch_size: int = 1,
    seed: Optional[int] = None,
    raw: bool = True,
) -> str:
    """
    Submit image generation job to Krea.ai.
    Returns job_id for polling.
    """
    endpoint_map = {
        "bfl/flux-1.1-pro-ultra": "generate/image/bfl/flux-1.1-pro-ultra",
        "google/imagen-4-ultra": "generate/image/google/imagen-4-ultra",
        "seedream-4": "generate/image/seedream-4",
        "gpt-image": "generate/image/gpt-image",
        "nano-banana-pro": "generate/image/nano-banana-pro",
    }
    
    endpoint = endpoint_map.get(model)
    if not endpoint:
        raise ValueError(f"Unknown model: {model}. Supported: {list(endpoint_map.keys())}")
    
    url = f"https://api.krea.ai/{endpoint}"
    
    payload = {
        "prompt": prompt,
        "width": width,
        "height": height,
        "batchSize": batch_size,
    }
    
    if seed is not None:
        payload["seed"] = seed
    
    if model == "bfl/flux-1.1-pro-ultra" and raw:
        payload["raw"] = True
    
    print(f"[SUBMIT] Model: {model}, Size: {width}x{height}, Batch: {batch_size}", file=sys.stderr)
    response = make_request(url, api_key, method="POST", data=payload)
    
    job_id = response.get("job_id")
    if not job_id:
        raise RuntimeError(f"No job_id in response: {response}")
    
    print(f"[JOB] ID: {job_id}", file=sys.stderr)
    return job_id


def poll_job(api_key: str, job_id: str, poll_interval: int = 5, max_wait: int = 300) -> Dict[str, Any]:
    """
    Poll job status until completion or timeout.
    Returns final job response with image URLs.
    """
    url = f"https://api.krea.ai/jobs/{job_id}"
    elapsed = 0
    
    while elapsed < max_wait:
        response = make_request(url, api_key, method="GET")
        status = response.get("status", "unknown")
        
        if status == "completed":
            print(f"[COMPLETE] Job finished in {elapsed}s", file=sys.stderr)
            return response
        elif status in ["failed", "cancelled"]:
            raise RuntimeError(f"Job {status}: {response}")
        
        print(f"[POLL] Status: {status}, elapsed: {elapsed}s", file=sys.stderr)
        time.sleep(poll_interval)
        elapsed += poll_interval
    
    raise TimeoutError(f"Job did not complete within {max_wait}s")


def download_image(url: str, output_path: Path) -> None:
    """Download image from URL to local file."""
    print(f"[DOWNLOAD] {url} -> {output_path}", file=sys.stderr)
    
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=60) as resp:
        output_path.write_bytes(resp.read())
    
    print(f"[SAVED] {output_path}", file=sys.stderr)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate images via Krea.ai API")
    parser.add_argument("--prompt", required=True, help="Image generation prompt")
    parser.add_argument("--model", default="bfl/flux-1.1-pro-ultra", help="Model name")
    parser.add_argument("--width", type=int, default=1536, help="Image width")
    parser.add_argument("--height", type=int, default=1024, help="Image height")
    parser.add_argument("--batch-size", type=int, default=1, help="Number of images")
    parser.add_argument("--seed", type=int, help="Random seed (optional)")
    parser.add_argument("--no-raw", action="store_true", help="Disable raw mode for Flux")
    parser.add_argument("--output-dir", default="./output", help="Output directory")
    parser.add_argument("--poll-interval", type=int, default=5, help="Poll interval (seconds)")
    parser.add_argument("--max-wait", type=int, default=300, help="Max wait time (seconds)")
    
    args = parser.parse_args()
    
    api_key = os.environ.get("KREA_API_KEY", "").strip()
    if not api_key:
        print("Error: KREA_API_KEY environment variable not set", file=sys.stderr)
        return 2
    
    # Submit job
    job_id = generate_image(
        api_key=api_key,
        prompt=args.prompt,
        model=args.model,
        width=args.width,
        height=args.height,
        batch_size=args.batch_size,
        seed=args.seed,
        raw=not args.no_raw,
    )
    
    # Poll until complete
    result = poll_job(
        api_key=api_key,
        job_id=job_id,
        poll_interval=args.poll_interval,
        max_wait=args.max_wait,
    )
    
    # Download images
    output_dir = Path(args.output_dir).expanduser()
    output_dir.mkdir(parents=True, exist_ok=True)
    
    images = result.get("images", [])
    if not images:
        print(f"Warning: No images in response: {result}", file=sys.stderr)
        return 1
    
    for idx, img_url in enumerate(images):
        filename = f"{job_id}_{idx:02d}.png"
        output_path = output_dir / filename
        download_image(img_url, output_path)
    
    # Print metadata
    metadata = {
        "job_id": job_id,
        "model": args.model,
        "prompt": args.prompt,
        "images": [str(output_dir / f"{job_id}_{i:02d}.png") for i in range(len(images))],
        "credits_used": result.get("credits_used", "unknown"),
    }
    
    print(json.dumps(metadata, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
