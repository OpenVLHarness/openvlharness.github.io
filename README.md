# openvlharness.github.io

Project page for **OpenVLHarness: Real World Visual Agentic Tool-Use with Multimodal Memory**.

Plain static site (no build step): `index.html`, `static/css/style.css`, `static/js/{data,main}.js`, images in `static/images/`.

```bash
python3 -m http.server 8765   # then open http://localhost:8765
```

## Paper

[arXiv:2610.26860](https://arxiv.org/abs/2610.26860) · [PDF](https://arxiv.org/pdf/2610.26860)

The publication links, citation metadata, and BibTeX are in `index.html`.

Launch video (top of the page): `static/video/openvlharness_launch.mp4` is the launch film (v12, dark, 1080p60, from the private tool-vision/video repo) and `static/video/launch_poster.jpg` its frame at 6.5 s. To swap in a new cut, replace both files and bump their `?v=` in `index.html`.

Examples gallery: `static/js/examples.js` + `static/examples/` are generated from the `paper_examples` bundles in mini-vlm-toolkit (branch `bryan/sandbox`). Unzip the bundles into one folder and run `python scripts/build_examples.py <folder>` to regenerate.

All chart numbers live in `static/js/data.js` (transcribed from the paper's tables; the effort chart is generated from the
full-split GPT-6 Luna effort sweep by `luna_full/update_site_effort.py` in OpenVLHarness-release-check).
After editing CSS/JS, bump the `?v=` query in `index.html` so browsers pick up the change.

Live demo: `static/js/demo.js` is the client; its backend lives in [`demo_server/`](demo_server/README.md) (Gradio app on the released `openvlharness` package, GPU tool budget, launch scripts). Append `?demo_server=http://127.0.0.1:7860` to the page URL to test against a local backend (only localhost URLs are accepted).

Hugging Face Space: `python scripts/build_space.py <tunnel-url> <out-dir>` builds the Space page from this page's demo section (same markup, `demo.js`, styles and samples) and records the demo server URL that both pages read; upload `<out-dir>` to the Space after each tunnel restart.
