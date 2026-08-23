#!/usr/bin/env python3
"""
Tiny AutoEncoder for Stable Diffusion
(DNN for encoding / decoding SD's latent space)
"""
import torch
import torch.nn as nn

def conv(n_in, n_out, **kwargs):
    return nn.Conv2d(n_in, n_out, 3, padding=1, **kwargs)

class Clamp(nn.Module):
    def forward(self, x):
        return torch.tanh(x / 3) * 3

class Block(nn.Module):
    def __init__(self, n_in, n_out, use_midblock_gn=False):
        super().__init__()
        self.conv = nn.Sequential(conv(n_in, n_out), nn.ReLU(), conv(n_out, n_out), nn.ReLU(), conv(n_out, n_out))
        self.skip = nn.Conv2d(n_in, n_out, 1, bias=False) if n_in != n_out else nn.Identity()
        self.fuse = nn.ReLU()
        self.use_midblock_gn = use_midblock_gn
        if use_midblock_gn:
            self.gn = nn.GroupNorm(8, n_out)
    def forward(self, x):
        y = self.conv(x) + self.skip(x)
        if self.use_midblock_gn:
            y = self.gn(y)
        return self.fuse(y)

def Encoder(latent_channels=4, use_midblock_gn=False):
    return nn.Sequential(
        conv(3, 64), Block(64, 64, use_midblock_gn),
        conv(64, 64, stride=2, bias=False), Block(64, 64, use_midblock_gn), Block(64, 64, use_midblock_gn), Block(64, 64, use_midblock_gn),
        conv(64, 64, stride=2, bias=False), Block(64, 64, use_midblock_gn), Block(64, 64, use_midblock_gn), Block(64, 64, use_midblock_gn),
        conv(64, 64, stride=2, bias=False), Block(64, 64, use_midblock_gn), Block(64, 64, use_midblock_gn), Block(64, 64, use_midblock_gn),
        conv(64, latent_channels),
    )

def Decoder(latent_channels=4, use_midblock_gn=False):
    return nn.Sequential(
        Clamp(), conv(latent_channels, 64), nn.ReLU(),
        Block(64, 64, use_midblock_gn), Block(64, 64, use_midblock_gn), Block(64, 64, use_midblock_gn), nn.Upsample(scale_factor=2), conv(64, 64, bias=False),
        Block(64, 64, use_midblock_gn), Block(64, 64, use_midblock_gn), Block(64, 64, use_midblock_gn), nn.Upsample(scale_factor=2), conv(64, 64, bias=False),
        Block(64, 64, use_midblock_gn), Block(64, 64, use_midblock_gn), Block(64, 64, use_midblock_gn), nn.Upsample(scale_factor=2), conv(64, 64, bias=False),
        Block(64, 64, use_midblock_gn), conv(64, 3),
    )

class TAESD(nn.Module):
    latent_magnitude = 3
    latent_shift = 0.5
    def __init__(self, encoder_path="taesd_encoder.pth", decoder_path="taesd_decoder.pth", latent_channels=None, arch_variant=None):
        super().__init__()
        if latent_channels is None:
            latent_channels, arch_variant = self.guess_latent_channels_and_arch(str(encoder_path))
        self.encoder = Encoder(latent_channels, use_midblock_gn=(arch_variant in ["flux_2"]))
        self.decoder = Decoder(latent_channels, use_midblock_gn=(arch_variant in ["flux_2"]))
        if encoder_path is not None:
            self.encoder.load_state_dict(torch.load(encoder_path, map_location="cpu", weights_only=True))
        if decoder_path is not None:
            self.decoder.load_state_dict(torch.load(decoder_path, map_location="cpu", weights_only=True))
    def guess_latent_channels_and_arch(self, encoder_path):
        if "taef1" in encoder_path:
            return 16, None
        if "taef2" in encoder_path:
            return 32, "flux_2"
        if "taesd3" in encoder_path:
            return 16, None
        if "taesana" in encoder_path:
            return 32, "f32"
        return 4, None
    @staticmethod
    def scale_latents(x):
        return x.div(2 * TAESD.latent_magnitude).add(TAESD.latent_shift).clamp(0, 1)
    @staticmethod
    def unscale_latents(x):
        return x.sub(TAESD.latent_shift).mul(2 * TAESD.latent_magnitude)
