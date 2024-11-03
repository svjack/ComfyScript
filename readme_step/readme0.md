# ComfyScript

ComfyScript is a tool that allows you to write and execute workflows for ComfyUI using a Python-based scripting interface. This README provides instructions on how to install and use ComfyScript.

## Installation

1. **Install Comfy CLI**:
   ```bash
   pip install comfy-cli
   ```

2. **Install ComfyScript**:
   ```bash
   comfy --here install
   cd ComfyUI/custom_nodes
   git clone https://github.com/Chaoses-Ib/ComfyScript.git
   cd ComfyScript
   python -m pip install -e ".[default]"
   ```

3. **Optional: Install CLI support**:
   ```bash
   pip install -e ".[default,cli]"
   ```

4. **Update aiohttp**:
   ```bash
   pip uninstall aiohttp
   pip install -U aiohttp
   ```

5. **Optional: Install SOCKS support for httpx**:
   ```bash
   pip install "httpx[socks]"
   ```

## Usage

### Start the Server

To start the server, use the following Python code:

```python
from comfy_script.runtime import *
load()
```

### Download a Model

Download a model checkpoint and place it in the appropriate directory:

```bash
wget https://cdn-lfs.hf.co/repos/66/6f/666f465fa70158515404e8de2c6bc6fe2f90c46f9296293aa14daededeb32c52/cc6cb27103417325ff94f52b7a5d2dde45a7515b25c255d8e396c90014281516\?response-content-disposition\=attachment%3B+filename\*%3DUTF-8%27%27v1-5-pruned-emaonly.ckpt%3B+filename%3D%22v1-5-pruned-emaonly.ckpt%22%3B\&Expires\=1730878768\&Policy\=eyJTdGF0ZW1lbnQiOlt7IkNvbmRpdGlvbiI6eyJEYXRlTGVzc1RoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTczMDg3ODc2OH19LCJSZXNvdXJjZSI6Imh0dHBzOi8vY2RuLWxmcy5oZi5jby9yZXBvcy82Ni82Zi82NjZmNDY1ZmE3MDE1ODUxNTQwNGU4ZGUyYzZiYzZmZTJmOTBjNDZmOTI5NjI5M2FhMTRkYWVkZWRlYjMyYzUyL2NjNmNiMjcxMDM0MTczMjVmZjk0ZjUyYjdhNWQyZGRlNDVhNzUxNWIyNWMyNTVkOGUzOTZjOTAwMTQyODE1MTY%7EcmVzcG9uc2UtY29udGVudC1kaXNwb3NpdGlvbj0qIn1dfQ__\&Signature\=Fnc-RGdxuxNpFVZDbmwC-4nXS4imWcQ8MMPJu20CMHVLcvvcM5t4G7SK6zVDaMLbzGYs7oFQ4o4%7E7sep7djMUrwdTDloocyvGU9lfB%7EqZpW797plvVTzqFBJoYy7kTzvtTgB-1aerE6svJDhxiXpACDeAgKJKdAhWNndZuqSCtgGu1HSLmflaVmKpXkufD7ZCVxwsnawRhwSam63smYl7BOySLiHbAYKWr8UjzfaaIM6FLqx0JPMJZL2wAkLCNbNPvg74hZ0I8Bxn7%7EKio63VXxnIYQpLVW7bZcQXjwXQ3XXbKekjTyILTtXUvG2tQ40CDoiH9T%7E3Df6pylYLzJJWQ__\&Key-Pair-Id\=K3RPWS32NSSJCE -O v1-5-pruned-emaonly.ckpt
   cp v1-5-pruned-emaonly.ckpt ComfyUI/models/checkpoints
   ```

### Example Workflow

Here is an example workflow written in ComfyScript:

```python
from comfy_script.runtime.nodes import *

with Workflow():
    model, clip, vae = CheckpointLoaderSimple('v1-5-pruned-emaonly.ckpt')
    conditioning = CLIPTextEncode('beautiful scenery nature glass bottle landscape, , purple galaxy bottle,', clip)
    conditioning2 = CLIPTextEncode('text, watermark', clip)
    latent = EmptyLatentImage(512, 512, 1)
    latent = KSampler(model, 156680208700286, 20, 8, 'euler', 'normal', conditioning, conditioning2, latent, 1)
    image = VAEDecode(latent, vae)
    SaveImage(image, 'ComfyUI')

from PIL import Image
Image.open("ComfyUI/output/ComfyUI_00001_.png")
```

### CLI Translation

You can translate workflows using the CLI:

```bash
python -m comfy_script.transpile "D:\workflow.json"
python -m comfy_script.transpile niji-动漫二次元_3.0.safetensors-keqing-lora-workflow.json
```

### Advanced Workflow Example

Here is an advanced example that includes LoraLoader:

```python
model, clip, vae = CheckpointLoaderSimple('niji-动漫二次元_3.0.safetensors')
model, clip = LoraLoader(model, clip, 'keqing_lion_optimizer_dim64_loraModel_5e-3noise_token1_4-3-2023.safetensors', 1, 1)
conditioning = CLIPTextEncode('(Realistic painting style:0.9), masterpiece, best quality,  absurdres, looking at viewer, solo, keqing (lantern rite) (genshin impact), official alternate costume, 1girl, keqing (genshin impact), phone, purple hair, solo, skirt, scarf, twintails, hair bun, cellphone, plaid scarf, sweater, purple sweater, long hair, hair ornament, white skirt, looking at viewer, holding phone, holding, cone hair bun, bag, plaid, blush, smartphone, long sleeves, bare shoulders, purple eyes, braid, bow, flower, shoulder bag, hair flower, breasts, frills, bangs, casual, double bun, handbag, hair bow, very long hair, closed mouth, outdoors, cable knit', clip)
conditioning2 = CLIPTextEncode('(worst quality, low quality, extra digits, loli, child, male:1.4)), bad_prompt,', clip)
latent = EmptyLatentImage(512, 512, 1)
latent = KSampler(model, 1123713238173417, 20, 8, 'euler', 'normal', conditioning, conditioning2, latent, 1)
image = VAEDecode(latent, vae)
SaveImage(image, 'ComfyUI')
```

#### 这个功能只能对安装完之后的进行翻译


### CLI 翻译工作流

参考文档: [CLI 翻译工作流](https://github.com/Chaoses-Ib/ComfyScript/blob/main/docs/Transpiler.md#cli)

```bash
python -m comfy_script.transpile "D:\workflow.json"
```

```bash
python -m comfy_script.transpile niji-动漫二次元_3.0.safetensors-keqing-lora-workflow.json
```

### 工作流示例

```python
with Workflow():
    model, clip, vae = CheckpointLoaderSimple('niji-动漫二次元_3.0.safetensors')
    model, clip = LoraLoader(model, clip, 'keqing_lion_optimizer_dim64_loraModel_5e-3noise_token1_4-3-2023.safetensors', 1, 1)
    conditioning = CLIPTextEncode('(Realistic painting style:0.9), masterpiece, best quality,  absurdres, looking at viewer, solo, keqing (lantern rite) (genshin impact), official alternate costume, 1girl, keqing (genshin impact), phone, purple hair, solo, skirt, scarf, twintails, hair bun, cellphone, plaid scarf, sweater, purple sweater, long hair, hair ornament, white skirt, looking at viewer, holding phone, holding, cone hair bun, bag, plaid, blush, smartphone, long sleeves, bare shoulders, purple eyes, braid, bow, flower, shoulder bag, hair flower, breasts, frills, bangs, casual, double bun, handbag, hair bow, very long hair, closed mouth, outdoors, cable knit', clip)
    conditioning2 = CLIPTextEncode('(worst quality, low quality, extra digits, loli, child, male:1.4)), bad_prompt,', clip)
    latent = EmptyLatentImage(512, 512, 1)
    latent = KSampler(model, 1123713238173417, 20, 8, 'euler', 'normal', conditioning, conditioning2, latent, 1)
    image = VAEDecode(latent, vae)
    SaveImage(image, 'ComfyUI')
```

```python
Image.open("ComfyUI/output/ComfyUI_00006_.png")
```

### 尝试安装新的自定义节点并运行工作流

参考文档: [ComfyUI 自定义节点生命周期](https://docs.comfy.org/essentials/custom_node_lifecycle)

```bash
git clone https://github.com/ArtVentureX/comfyui-animatediff
cd comfyui-animatediff
sudo apt-get install git-lfs
git clone https://huggingface.co/guoyww/animatediff
```


### 安装自定义节点

```bash
comfy node show installed
ls ComfyUI/custom_nodes/comfyui-animatediff/models
cp -r animatediff/* ComfyUI/custom_nodes/comfyui-animatediff/models
```

#### 安装后是否需要重启？

```bash
ls ComfyUI/custom_nodes/comfyui-animatediff/models
```

```plaintext
README.md       mm_sd_v15_v2.ckpt      v2_lora_PanRight.ckpt              v2_lora_TiltDown.ckpt  v2_lora_ZoomOut.ckpt  v3_sd15_sparsectrl_rgb.ckpt
mm_sd_v14.ckpt  mm_sdxl_v10_beta.ckpt  v2_lora_RollingAnticlockwise.ckpt  v2_lora_TiltUp.ckpt    v3_sd15_adapter.ckpt  v3_sd15_sparsectrl_scribble.ckpt
mm_sd_v15.ckpt  v2_lora_PanLeft.ckpt   v2_lora_RollingClockwise.ckpt      v2_lora_ZoomIn.ckpt    v3_sd15_mm.ckpt
```


### 下载模型

```bash
git clone https://huggingface.co/manshoety/AD_Stabilized_Motion
git clone https://huggingface.co/stb/animelike2d
git clone https://huggingface.co/hakurei/waifu-diffusion-v1-4
```


### 工作流示例

```bash
mv simple.json animatediff-simple.json
python -m comfy_script.transpile animatediff-simple.json
```

```python
with Workflow():
    motion_module = AnimateDiffModuleLoader('mm-Stabilized_mid.pth', None)
    model, clip, _ = CheckpointLoaderSimple('AnimeLike25D_v11.safetensors')
    conditioning = CLIPTextEncode('masterpiece, best quality, 1girl, solo, cherry blossoms, hanami, pink flower, white flower, spring season, wisteria, petals, flower, plum blossoms, outdoors, falling petals, white hair, black eyes', clip)
    conditioning2 = CLIPTextEncode('embedding:easynegative, embedding:badhandv4, ', clip)
    latent = EmptyLatentImage(512, 512, 1)
    latent = AnimateDiffSampler(motion_module, 'default', 16, model, 345029849956677, 20, 8, 'euler', 'normal', conditioning, conditioning2, latent, 0.8, None)
    vae = VAELoader('klF8Anime2.ckpt')
    image = VAEDecode(latent, vae)
    AnimateDiffCombine(image, 8, 0, 'Enabled', 'AnimateDiff', None, None)
```


### 复制模型文件

```bash
ls AD_Stabilized_Motion/mm-Stabilized_mid.pth
cp AD_Stabilized_Motion/mm-Stabilized_mid.pth ComfyUI/custom_nodes/comfyui-animatediff/models
ls animelike2d/animelike25D_animelike25DV11Pruned.safetensors
cp animelike2d/animelike25D_animelike25DV11Pruned.safetensors ComfyUI/models/checkpoints
ls waifu-diffusion-v1-4/vae/kl-f8-anime.ckpt
cp waifu-diffusion-v1-4/vae/kl-f8-anime.ckpt ComfyUI/models/vae
cp waifu-diffusion-v1-4/vae/kl-f8-anime2.ckpt ComfyUI/models/vae
```

---

### 最终工作流

```python
with Workflow():
    motion_module = AnimateDiffModuleLoader('mm-Stabilized_mid.pth', None)
    model, clip, _ = CheckpointLoaderSimple('animelike25D_animelike25DV11Pruned.safetensors')
    conditioning = CLIPTextEncode('masterpiece, best quality, 1girl, solo, cherry blossoms, hanami, pink flower, white flower, spring season, wisteria, petals, flower, plum blossoms, outdoors, falling petals, white hair, black eyes', clip)
    conditioning2 = CLIPTextEncode('embedding:easynegative, embedding:badhandv4, ', clip)
    latent = EmptyLatentImage(512, 512, 1)
    latent = AnimateDiffSampler(motion_module, 'default', 16, model, 345029849956677, 20, 8, 'euler', 'normal', conditioning, conditioning2, latent, 0.8, None)
    vae = VAELoader('kl-f8-anime2.ckpt')
    image = VAEDecode(latent, vae)
    AnimateDiffCombine(image, 8, 0, 'Enabled', 'AnimateDiff', None, None)
```

```python
from IPython import display
display.Image("ComfyUI/output/AnimateDiff_00001_.gif")
```

---

### 成功示例

```python
with Workflow():
    motion_module = AnimateDiffModuleLoader('mm-Stabilized_mid.pth', None)
    model, clip, _ = CheckpointLoaderSimple('animelike25D_animelike25DV11Pruned.safetensors')
    conditioning = CLIPTextEncode('masterpiece, best quality, 1cat, solo, cherry blossoms, hanami, green grass, yellow flower, fall season, wisteria, petals, flower, plum blossoms, outdoors, falling petals, white hair, black eyes', clip)
    conditioning2 = CLIPTextEncode('embedding:easynegative, embedding:badhandv4, ', clip)
    latent = EmptyLatentImage(512, 512, 1)
    latent = AnimateDiffSampler(motion_module, 'default', 16, model, 345029849956677, 20, 8, 'euler', 'normal', conditioning, conditioning2, latent, 0.8, None)
    vae = VAELoader('kl-f8-anime2.ckpt')
    image = VAEDecode(latent, vae)
    AnimateDiffCombine(image, 8, 0, 'Enabled', 'AnimateDiff', None, None)
```

```python
from IPython import display
display.Image("ComfyUI/output/AnimateDiff_00002_.gif")
```

```python
with Workflow():
    motion_module = AnimateDiffModuleLoader('mm-Stabilized_mid.pth', None)
    model, clip, _ = CheckpointLoaderSimple('animelike25D_animelike25DV11Pruned.safetensors')
    conditioning = CLIPTextEncode('masterpiece, best quality, 1girl, solo, hanami, green grass, yellow flower, fall season', clip)
    conditioning2 = CLIPTextEncode('embedding:easynegative, embedding:badhandv4, ', clip)
    latent = EmptyLatentImage(512, 512, 1)
    latent = AnimateDiffSampler(motion_module, 'default', 16, model, 345029849956677, 20, 8, 'euler', 'normal', conditioning, conditioning2, latent, 0.8, None)
    vae = VAELoader('kl-f8-anime2.ckpt')
    image = VAEDecode(latent, vae)
    AnimateDiffCombine(image, 8, 0, 'Enabled', 'AnimateDiff', None, None)
```

```python
from IPython import display
display.Image("ComfyUI/output/AnimateDiff_00005_.gif")
```


## Documentation

For more details on the CLI translation, refer to the [Transpiler documentation](https://github.com/Chaoses-Ib/ComfyScript/blob/main/docs/Transpiler.md#cli).


Feel free to explore and modify the workflows to suit your needs!
