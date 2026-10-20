# Security Policy

## Scope

`sts2-trainer` is an offline, single-player **Slay the Spire 2 trainer**. It
reads and writes process memory of the local game client to enable cheat
features (infinite energy, gold multiplier, card duplication, etc.).

This is not a security product. It is a cheat tool for a single-player game.
That said, we still take the following seriously:

- **No persistence outside the game process.** The trainer must not write
  registry keys, scheduled tasks, or startup entries.
- **No network exfiltration.** The only outbound traffic is the optional
  update check against `api.github.com`.
- **No bundled binaries.** All hooks are pure Python via `pymem` + `ctypes`.
  If a PR adds a `.dll` or `.exe`, it will be rejected.

## Reporting a vulnerability

If you find a bug that could damage a user's save file (e.g. an offset that
writes into the save region instead of the target stat), open a private
advisory via GitHub Security Advisories or email the maintainer listed in
`pyproject.toml`.

Please include:
- Game build ID (bottom-right of the main menu)
- Trainer version (`python -m sts2_trainer.cli --version`)
- The feature that triggered the issue

## Supported versions

Only the latest tagged release is supported. Older offsets rot fast.