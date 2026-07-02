# eSIM Tooling Landscape (2026)

> A survey of open-source eSIM / eUICC / LPA projects — sorted by *what you actually need it for*, not by star count.

## TL;DR routing

| Goal | Use this |
|---|---|
| Install my Giffgaff eSIM on a modern phone | System settings → manual entry (SM-DP+ + activation code). No tool needed. |
| Get a QR code from my activation string | Local script that emits `LPA:1$SM-DP+$activation` |
| Convert a physical SIM to eSIM (Giffgaff / Simyo) | [Silentely/eSIM-Tools](https://github.com/Silentely/eSIM-Tools) |
| Manage a physical eUICC card (5ber / eSIM.me) | [`lpac`](https://github.com/estkme-group/lpac) on Mac/Linux |
| Rooted Android without native eSIM support | [OpenEUICC_for_Magisk](https://github.com/hzy132/OpenEUICC_for_Magisk) |
| Xiaomi HyperOS eSIM unlock | [XiaomiEsimLPA](https://github.com/tehcneko/XiaomiEsimLPA) |
| Research the SM-DP+ protocol | [vfoschi/esim-rsp-ts](https://github.com/vfoschi/esim-rsp-ts) |

## 1. Giffgaff / Simyo — carrier-specific

| Project | ★ | Purpose | Fit |
|---|---:|---|---|
| [Silentely/eSIM-Tools](https://github.com/Silentely/eSIM-Tools) | 1760+ | Giffgaff / Simyo eSIM conversion, device swap, QR generation | **most relevant** |
| [Tuluobo/GGEsim](https://github.com/Tuluobo/GGEsim) | 62 | iOS Swift app: Giffgaff → eSIM QR | if you carry Xcode |
| [LSOIVNE/Giffgaff-Hook](https://github.com/LSOIVNE/Giffgaff-Hook) | 53 | LSPosed module: spoof device to force eSIM path, scrape activation | LSPosed only |
| [MiniMoss/giffgaff_esim_postman](https://github.com/MiniMoss/giffgaff_esim_postman) | 22 | Postman collection for Giffgaff eSIM API | technical dive |
| [MaxThinking/giffgaff-is-easy](https://github.com/MaxThinking/giffgaff-is-easy) | 3 | Walkthrough | reference reading |

## 2. General eUICC / LPA managers

| Project | ★ | Platform | Notes |
|---|---:|---|---|
| [estkme-group/openeuicc](https://github.com/estkme-group/openeuicc) | 917 | Android | The reference open-source LPA |
| [EsimMoe/MiniLPA](https://github.com/EsimMoe/MiniLPA) | 706 | Android | Polished LPA UI |
| [estkme-group/lpac](https://github.com/estkme-group/lpac) | 647 | C (Linux/macOS/Win) | CLI eUICC manager, pairs with a card reader |
| [iebb/NekokoLPA](https://github.com/iebb/NekokoLPA) | 525 | Android / iOS | Cross-platform LPA |
| [Laiteux/openeuicc-bridge](https://github.com/Laiteux/openeuicc-bridge) | 5 | Android via ADB | Drive OpenEUICC from a computer |

## 3. Magisk / OEM system integration

| Project | ★ | Purpose |
|---|---:|---|
| [hzy132/OpenEUICC_for_Magisk](https://github.com/hzy132/OpenEUICC_for_Magisk) | 290 | OpenEUICC as a Magisk module |
| [tehcneko/XiaomiEsimLPA](https://github.com/tehcneko/XiaomiEsimLPA) | 187 | Native eSIM management for MIUI / HyperOS |

## 4. Research / protocol

| Project | Purpose |
|---|---|
| [truebest/esim_loader](https://github.com/truebest/esim_loader) | Download consumer eSIM profiles via a smartcard reader |
| [vfoschi/esim-rsp-ts](https://github.com/vfoschi/esim-rsp-ts) | TypeScript / NestJS SM-DP+ server — study reference |
| [dani-mg-05/smdpplus-server-client](https://github.com/dani-mg-05/smdpplus-server-client) | Minimal SM-DP+ pair for lab work |

## For most people

If you *have* the activation info in hand:

```
System Settings → Cellular → Add eSIM → Enter Details Manually
  SM-DP+ address: cel.prod.ondemandconnectivity.com
  Activation code: <your long code>
```

That's it. Skip the tools unless you're converting, transferring, or researching.

## For me

I already activated Giffgaff via the system UI. I'm keeping [`lpac`](https://github.com/estkme-group/lpac) on the Mac in case I later grab a 5ber eUICC. Everything else is bookmark-only.
