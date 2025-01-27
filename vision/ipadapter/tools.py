import replicate
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def set_image_url(image_url, prompt):
  return {
  "3": {
    "inputs": {
      "seed": 479086916121443,
      "steps": 35,
      "cfg": 8,
      "sampler_name": "dpmpp_2m",
      "scheduler": "karras",
      "denoise": 1,
      "model": [
        "4",
        0
      ],
      "positive": [
        "6",
        0
      ],
      "negative": [
        "7",
        0
      ],
      "latent_image": [
        "5",
        0
      ]
    },
    "class_type": "KSampler",
    "_meta": {
      "title": "KSampler"
    }
  },
  "4": {
    "inputs": {
      "ckpt_name": "realismEngineSDXL_v30VAE.safetensors"
    },
    "class_type": "CheckpointLoaderSimple",
    "_meta": {
      "title": "Load Checkpoint"
    }
  },
  "5": {
    "inputs": {
      "width": 1024,
      "height": 1024,
      "batch_size": 1
    },
    "class_type": "EmptyLatentImage",
    "_meta": {
      "title": "Empty Latent Image"
    }
  },
  "6": {
    "inputs": {
      "text": "hyperdetailed photography, soft light, head potrait, (white background: 1.3), skin details, sharp and in focus, \ngirl indian student,\nshort wavey black hair.\nbig eyes,\nnarrow nose,\nslim,\ncute,\nbeautiful",
      "clip": [
        "4",
        1
      ]
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "CLIP Text Encode (Prompt)"
    }
  },
  "7": {
    "inputs": {
      "text": "(worst quality, low quality, normal quality, lowres, low details, oversaturated, undersaturated, overexposed, underexposed, grayscale, bw, bad photo, bad photography, bad art:1.4), (watermark, signature, text font, username, error, logo, words, letters, digits, autograph, trademark, name:1.2), (blur, blurry, grainy), morbid, ugly, asymmetrical, mutated malformed, multilated, poorly lit, bad shadow, draft, cropped, out of frame, cut off, censored, jpeg artifacts, out of focus, glitch, duplicate, (airbrushed, cartoon, anime, semi-realistic, cgi, render, blender, digital art, manga, amateur:1.3), (3D, 3D game, 3d Game scene, 3D character:1.1), acne",
      "clip": [
        "4",
        1
      ]
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "CLIP Text Encode (Prompt)"
    }
  },
  "8": {
    "inputs": {
      "samples": [
        "3",
        0
      ],
      "vae": [
        "4",
        2
      ]
    },
    "class_type": "VAEDecode",
    "_meta": {
      "title": "VAE Decode"
    }
  },
  "11": {
    "inputs": {
      "resolution": 1024,
      "image": [
        "8",
        0
      ]
    },
    "class_type": "OneFormer-COCO-SemSegPreprocessor",
    "_meta": {
      "title": "OneFormer COCO Segmentor"
    }
  },
  "12": {
    "inputs": {
      "images": [
        "11",
        0
      ]
    },
    "class_type": "PreviewImage",
    "_meta": {
      "title": "Preview Image"
    }
  },
  "14": {
    "inputs": {
      "channel": "red",
      "image": [
        "11",
        0
      ]
    },
    "class_type": "ImageToMask",
    "_meta": {
      "title": "Convert Image to Mask"
    }
  },
  "16": {
    "inputs": {
      "weight": 0.5,
      "weight_faceidv2": 1.5,
      "weight_type": "linear",
      "combine_embeds": "concat",
      "start_at": 0,
      "end_at": 1,
      "embeds_scaling": "V only",
      "model": [
        "4",
        0
      ],
      "ipadapter": [
        "33",
        0
      ],
      "image": [
        "8",
        0
      ],
      "attn_mask": [
        "14",
        0
      ],
      "clip_vision": [
        "18",
        0
      ],
      "insightface": [
        "19",
        0
      ]
    },
    "class_type": "IPAdapterFaceID",
    "_meta": {
      "title": "IPAdapter FaceID"
    }
  },
  "18": {
    "inputs": {
      "clip_name": "CLIP-ViT-H-14-laion2B-s32B-b79K.safetensors"
    },
    "class_type": "CLIPVisionLoader",
    "_meta": {
      "title": "Load CLIP Vision"
    }
  },
  "19": {
    "inputs": {
      "provider": "CPU",
      "model_name": "buffalo_l"
    },
    "class_type": "IPAdapterInsightFaceLoader",
    "_meta": {
      "title": "IPAdapter InsightFace Loader"
    }
  },
  "22": {
    "inputs": {
      "text": f"{prompt}",
      "clip": [
        "4",
        1
      ]
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "CLIP Text Encode (Prompt)"
    }
  },
  "23": {
    "inputs": {
      "text": "  (worst quality, low quality, normal quality, lowres, low details, oversaturated, undersaturated, overexposed, underexposed, grayscale, bw, bad photo, bad photography, bad art:1.4), (watermark, signature, text font, username, error, logo, words, letters, digits, autograph, trademark, name:1.2), (blur, blurry, grainy), morbid, ugly, asymmetrical, mutated malformed, multilated, poorly lit, bad shadow, draft, cropped, out of frame, cut off, censored, jpeg artifacts, out of focus, glitch, duplicate, (airbrushed, cartoon, anime, semi-realistic, cgi, render, blender, digital art, manga, amateur:1.3), (3D, 3D game, 3d Game scene, 3D character:1.1), acne",
      "clip": [
        "4",
        1
      ]
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "CLIP Text Encode (Prompt)"
    }
  },
  "24": {
    "inputs": {
      "seed": 1095694457262049,
      "steps": 35,
      "cfg": 8,
      "sampler_name": "dpmpp_2m",
      "scheduler": "karras",
      "denoise": 1,
      "model": [
        "40",
        0
      ],
      "positive": [
        "22",
        0
      ],
      "negative": [
        "23",
        0
      ],
      "latent_image": [
        "25",
        0
      ]
    },
    "class_type": "KSampler",
    "_meta": {
      "title": "KSampler"
    }
  },
  "25": {
    "inputs": {
      "width": 1024,
      "height": 1024,
      "batch_size": 1
    },
    "class_type": "EmptyLatentImage",
    "_meta": {
      "title": "Empty Latent Image"
    }
  },
  "26": {
    "inputs": {
      "samples": [
        "24",
        0
      ],
      "vae": [
        "4",
        2
      ]
    },
    "class_type": "VAEDecode",
    "_meta": {
      "title": "VAE Decode"
    }
  },
  "28": {
    "inputs": {
      "images": [
        "8",
        0
      ]
    },
    "class_type": "PreviewImage",
    "_meta": {
      "title": "Preview Image"
    }
  },
  "29": {
    "inputs": {
      "image": f"{image_url}",
      "upload": "image"
    },
    "class_type": "LoadImage",
    "_meta": {
      "title": "Load Image"
    }
  },
  "32": {
    "inputs": {
      "ipadapter_file": "ip-adapter-plus-face_sdxl_vit-h.safetensors"
    },
    "class_type": "IPAdapterModelLoader",
    "_meta": {
      "title": "IPAdapter Model Loader"
    }
  },
  "33": {
    "inputs": {
      "ipadapter_file": "ip-adapter-faceid-plusv2_sdxl.bin"
    },
    "class_type": "IPAdapterModelLoader",
    "_meta": {
      "title": "IPAdapter Model Loader"
    }
  },
  "36": {
    "inputs": {
      "weight": 0.3,
      "weight_type": "linear",
      "combine_embeds": "concat",
      "start_at": 0,
      "end_at": 1,
      "embeds_scaling": "V only",
      "model": [
        "16",
        0
      ],
      "ipadapter": [
        "32",
        0
      ],
      "image": [
        "8",
        0
      ],
      "attn_mask": [
        "14",
        0
      ],
      "clip_vision": [
        "18",
        0
      ]
    },
    "class_type": "IPAdapterAdvanced",
    "_meta": {
      "title": "IPAdapter Advanced"
    }
  },
  "37": {
    "inputs": {
      "resolution": 1024,
      "image": [
        "29",
        0
      ]
    },
    "class_type": "UniFormer-SemSegPreprocessor",
    "_meta": {
      "title": "UniFormer Segmentor"
    }
  },
  "38": {
    "inputs": {
      "channel": "red",
      "image": [
        "37",
        0
      ]
    },
    "class_type": "ImageToMask",
    "_meta": {
      "title": "Convert Image to Mask"
    }
  },
  "39": {
    "inputs": {
      "ipadapter_file": "ip-adapter-plus_sdxl_vit-h.safetensors"
    },
    "class_type": "IPAdapterModelLoader",
    "_meta": {
      "title": "IPAdapter Model Loader"
    }
  },
  "40": {
    "inputs": {
      "weight": 0.5,
      "weight_type": "linear",
      "combine_embeds": "concat",
      "start_at": 0,
      "end_at": 1,
      "embeds_scaling": "V only",
      "model": [
        "36",
        0
      ],
      "ipadapter": [
        "39",
        0
      ],
      "image": [
        "29",
        0
      ],
      "attn_mask": [
        "38",
        0
      ],
      "clip_vision": [
        "18",
        0
      ]
    },
    "class_type": "IPAdapterAdvanced",
    "_meta": {
      "title": "IPAdapter Advanced"
    }
  },
  "41": {
    "inputs": {
      "images": [
        "37",
        0
      ]
    },
    "class_type": "PreviewImage",
    "_meta": {
      "title": "Preview Image"
    }
  },
  "42": {
    "inputs": {
      "filename_prefix": "genrated_image",
      "images": [
        "26",
        0
      ]
    },
    "class_type": "SaveImage",
    "_meta": {
      "title": "Save Image"
    }
  }
}

# function for generate img
def generate_image(original_cloth_img_url: str, prompt: str) -> str:
    print("original_cloth_img_url", original_cloth_img_url)
    print("prompt", prompt)

    worflow = set_image_url(original_cloth_img_url, prompt)
    input = {
        "workflow_json": json.dumps(worflow),
        "randomise_seeds": True,
        "return_temp_files": False,
    }

    output = replicate.run(
        "fofr/any-comfyui-workflow:d485be22dbcdb7e1e80b8905d965a20266a326575aeda2cdb35eee45624f9aab",
        input=input,
    )

    print("generated image output", output[0].url)

    return {
       "original_cloth_img_url": original_cloth_img_url,
        "prompt": prompt,
        "ai_generated_img": output[0].url
    }

# function for review img

def review_image(original_cloth_img_url: str, ai_generated_img_url: str, text_prompt: str) -> str:
    client = OpenAI()
    response = client.chat.completions.create(
       model="gpt-4o",
       messages=[
          {
             "role": "user",
             "content": [
                {
                   "type": "text",
                   "text": f"""
original text prompt: {text_prompt}
--------------------------------------------------------------
You are the world class fashion designer, and your task is to review the human model wearing your designed cloth.
1st image is the image of the cloth you have designed, 2nd image is an AI generated image of human model wearing this cloth;
Please compare and clarify if the cloth in the 2nd image is highly similar, around 98% match with 1st image;
Please be very particular about the cloth texture, color, pattern, and design;
If more than 98% match, just return "98% match";
if less than 98% match, list out the discrepancies,
and iterate the original text prompt for the image generation model to fill the gap of the discrepancies.
(just add/tweak details to the original text prompt, do not do major structure changes);

Return in specific format:
MATCH SCORE: xxx,
CRITIQUE: xxx,
ITERATED PROMPT: xxx
            """
                },
                {
                   "type": "image_url",
                   "image_url": {
                        "url": original_cloth_img_url
                   }
                },
                {
                   "type": "image_url",
                   "image_url": {
                        "url": ai_generated_img_url
                   }
                }
             ]
          }
       ],
       max_tokens=300,
    )
    return response.choices[0].message.content

# function for fix hands

# function for upscale img
def upscale_image(latest_ai_generated_img_url: str, prompt: str) -> str:
    input = {
        "cfg": 8,
        "image": latest_ai_generated_img_url,
        "steps": 20,
        "denoise": 0.1,
        "upscaler": "4x-UltraSharp",
        "mask_blur": 8,
        "mode_type": "Linear",
        "scheduler": "normal",
        "tile_width": 512,
        "upscale_by": 2,
        "tile_height": 512,
        "sampler_name": "euler",
        "tile_padding": 32,
        "seam_fix_mode": "None",
        "seam_fix_width": 64,
        "positive_prompt": prompt,
        "seam_fix_denoise": 1,
        "seam_fix_padding": 16,
        "seam_fix_mask_blur": 8,
        "controlnet_strength": 1,
        "force_uniform_tiles": True,
        "use_controlnet_tile": True,
        "negative_prompt": "(worst quality, low quality, normal quality, lowres, low details, oversaturated, undersaturated, overexposed, underexposed, grayscale, bw, bad photo, bad photography, bad art:1.4), (watermark, signature, text font, username, error, logo, words, letters, digits, autograph, trademark, name:1.2), (blur, blurry, grainy), morbid, ugly, asymmetrical, mutated malformed, multilated, poorly lit, bad shadow, draft, cropped, out of frame, cut off, censored, jpeg artifacts, out of focus, glitch, duplicate, (airbrushed, cartoon, anime, semi-realistic, cgi, render, blender, digital art, manga, amateur:1.3), (3D, 3D game, 3d Game scene, 3D character:1.1), acne"
    }

    output = replicate.run(
        "juergengunz/ultimate-portrait-upscale:f7fdace4ec7adab7fa02688a160eee8057f070ead7fbb84e0904864fd2324be5",
        input=input
    )

    print("upscaled image output", output)

    return {
        "upscaled_img": output
    }



      