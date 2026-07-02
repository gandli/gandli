# honor-adb-automation

> Fully automated home-screen organization on a Honor X80 Pro Max, driven from my Mac mini over ADB. 4×6 grid, every installed app placed exactly once. No manual dragging.

**Status:** 💭 Concept — waiting for a spare weekend

## The itch

Every new phone I spend 45 minutes dragging icons into folders and end up with a layout I hate a week later. If it's a script, I can re-run it after every install/uninstall.

## Constraints

- 🖥️ Driven from Mac mini via `adb` — phone doesn't run anything itself
- 🚫 **No root** — X80 Pro Max Bootloader is [locked](../research/honor-root-status.md), so purely user-space
- 📐 4×6 layout, all apps on home screen (no app drawer), one page ideally
- ♻️ Idempotent — re-runnable after any install/uninstall

## Approach comparison

| Approach | Root? | MagicOS compatible? | Reliability |
|---|:---:|:---:|:---:|
| `adb shell settings put` on the launcher DB | ✅ needed | ❌ MagicOS launcher DB is locked | 💀 |
| `adb shell input tap/swipe` — pure UI automation | ❌ | ✅ | 🙂 slow but stable |
| Launcher swap → Nova / KISS + import layout XML | ❌ | ✅ default launcher setting | ✅✅ |
| ADB → launcher `am start-activity` with layout intent | ❌ | ❌ Honor Launcher has no such intent | 💀 |

## Recommended path

1. **Install Nova Launcher** via `adb install`
2. Set it as default with `adb shell cmd package set-home-activity`
3. Query installed packages: `adb shell pm list packages -3` (user apps only)
4. Generate Nova backup XML (grid + positions) → import via Nova Backup restore
5. Verify layout via `uiautomator dump`

## Layout policy

- Cell size: 4 columns × 6 rows on home
- Sort key: category (from Play Store metadata scraped locally) → app name pinyin
- Reserved cells: dock (bottom row 4 slots) = 电话 / 短信 / 相机 / 浏览器
- Never place: system settings clones, OEM bloat (auto-detect via package prefix `com.hihonor.*.deprecated`)

## Open questions

- [ ] Nova can't hide apps from home — do we uninstall bloat via `adb shell pm uninstall --user 0`?
- [ ] How to detect newly installed apps? Poll `pm list packages` on schedule, or listen to `am broadcast --user 0 android.intent.action.PACKAGE_ADDED`?
- [ ] Wallpaper is locked by MagicOS theme — can we skip and let user pick?
- [ ] Multi-user profiles (工作空间)?

## Related research

- [honor-root-status](../research/honor-root-status.md) — why we're not rooting this thing
