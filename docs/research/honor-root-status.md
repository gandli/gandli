# Honor Root Status (2026)

> Reality check on rooting a post-2020 Honor phone — specifically an X80 Pro Max — with a survey of the open-source tools people reach for.

## TL;DR

**Don't bother rooting an Honor X80 Pro Max.**

- Post-2020 (after the Huawei split), Honor removed official Bootloader unlock. `fastboot flashing unlock` returns a fake state and does nothing.
- Community brute-force tools only work on old Kirin SoCs.
- X80 Pro Max is Snapdragon 6 Gen 1 — no public method exists.
- If you want to root *something*: buy a used Pixel 6a/7a for ~¥1000. Official unlock, first-class Magisk/KernelSU support.

## Honor's post-split reality

| Aspect | Status |
|---|---|
| Official BL unlock code | ❌ Never issued since 2020 |
| `fastboot flashing unlock` | ⚠️ Command accepted, returns success, does nothing |
| Brute-force old codes | ✅ Kirin 620/65x/95x/960 only |
| Testpoint / 9008 | 🔧 Requires disassembly + hardware; no public tutorial for X80 |
| MagicOS 8/9 root reports | 💀 None in the wild |

## Reference repos (2026)

### Landscape trackers — read these first

| Repo | ★ | Use |
|---|---:|---|
| [AdaUnlocked/2026-All-Brands-Bootloader-Unlock-Status](https://github.com/AdaUnlocked/2026-All-Brands-Bootloader-Unlock-Status) | 177 | Continuously updated status table across all brands, dedicated Honor CN section |
| [MlgmXyysd/android-bootloader-kernel-source](https://github.com/MlgmXyysd/android-bootloader-kernel-source) | 100 | Per-vendor BL unlock + kernel-source + warranty implications |
| [zenfyrdev/bootloader-unlock-wall-of-shame](https://github.com/zenfyrdev/bootloader-unlock-wall-of-shame) | 4875 | Vendors that lock BL — Honor is on the wall |

### Kirin unlockers (old models only)

| Repo | ★ | Fit |
|---|---:|---|
| [kitsuned/PotatoNV](https://github.com/kitsuned/PotatoNV) | 1621 | GUI unlock for Kirin 620/65x/95x/960 — the classic |
| [werasik2aa/Huawei-Unlock-Tool](https://github.com/werasik2aa/Huawei-Unlock-Tool) | 503 | General Huawei unlock + FRP |
| [vcka/huawei-honor-unlock-bootloader](https://github.com/vcka/huawei-honor-unlock-bootloader) | 113 | Bootloader-unlock management tool |
| [werasik2aa/UnlockedHuaweiBootloader](https://github.com/werasik2aa/UnlockedHuaweiBootloader) | 84 | Archive of already-unlocked boot images |

### 16-digit brute-force scripts

| Repo | ★ | Notes |
|---|---:|---|
| [programminghoch10/huawei-honor-bootloader-bruteforce](https://github.com/programminghoch10/huawei-honor-bootloader-bruteforce) | 92 | IMEI-based, needs 1–24 h to try |
| [rainxh11/HuaweiBootloader_Bruteforce](https://github.com/rainxh11/HuaweiBootloader_Bruteforce) | 91 | .NET version |
| [Kur01234/Huawei-Bootloader-Unlocker](https://github.com/Kur01234/Huawei-Bootloader-Unlocker) | 4 | Simple Python |

### Root frameworks (post-unlock)

| Repo | ★ | Notes |
|---|---:|---|
| [topjohnwu/Magisk](https://github.com/topjohnwu/Magisk) | 61.5k | Mainstream systemless root, Rust rewrite in progress (v30.5+) |
| [tiann/KernelSU](https://github.com/tiann/KernelSU) | 17k | Kernel-based root, needs GKI-compatible kernel |
| [bmax121/APatch](https://github.com/bmax121/APatch) | 7.6k | Kernel-patch root without recompilation |

## Only-viable-path checklist

Realistic route if you insist on trying with an X80 Pro Max:

1. Watch `AdaUnlocked/2026-All-Brands-Bootloader-Unlock-Status` Honor section for breakthroughs
2. Read [Uotan wiki](https://wiki.uotan.cn) — Chinese community for model-specific breakthroughs
3. **Only touch a backup phone.** Never a daily driver.

## What I actually did

Left the X80 Pro Max fully stock and stopped fighting it. See [honor-adb-automation](../ideas/honor-adb-automation.md) for a no-root way to still automate my home screen.
