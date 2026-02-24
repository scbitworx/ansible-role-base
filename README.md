# Base Role

Layer 1 Ansible role applied to **all hosts**. Handles core system
configuration that every machine needs.

## What It Does

- Installs essential packages (distro-aware: `base-devel` on Arch,
  `build-essential` on Debian/Ubuntu)
- Creates the primary admin user account
- Sets timezone and locale
- Deploys a hardened `/etc/ssh/sshd_config`
- Sets up XDG shell skeleton (`~/.config/bash/`) with `conf.d/` sourcing
  loop and symlinks (`~/.bashrc`, `~/.profile`, `~/.inputrc`)

## Supported Platforms

- Arch Linux
- Ubuntu 24.04
- Debian 12

## Role Variables

| Variable | Default | Description |
|---|---|---|
| `base_extra_packages` | `[]` | Additional packages beyond the base set |
| `base_user` | `bwright` | Primary admin username |
| `base_user_groups` | `[]` | Additional groups (e.g., wheel, sudo) |
| `base_user_shell` | `/bin/bash` | Login shell |
| `base_user_create_home` | `true` | Create home directory |
| `base_timezone` | `America/New_York` | System timezone |
| `base_locale` | `en_US.UTF-8` | System locale |
| `base_sshd_port` | `22` | SSH port |
| `base_sshd_permit_root_login` | `no` | Root SSH login |
| `base_sshd_password_authentication` | `no` | Password auth |
| `base_sshd_pubkey_authentication` | `yes` | Pubkey auth |
| `base_sshd_x11_forwarding` | `no` | X11 forwarding |
| `base_editor` | `vim` | Default EDITOR/VISUAL |
| `base_histsize` | `10000` | Bash HISTSIZE |

## Shell Skeleton

The role deploys an XDG-compliant bash configuration:

```
~/.config/bash/
  bashrc       # conf.d/ sourcing loop, XDG exports, EDITOR, HISTSIZE
  profile      # sources bashrc, adds ~/.local/bin to PATH
  inputrc      # readline settings
  conf.d/      # drop-in directory for other roles
```

Symlinks are created for compatibility:
- `~/.bashrc` -> `.config/bash/bashrc`
- `~/.profile` -> `.config/bash/profile`
- `~/.inputrc` -> `.config/bash/inputrc`

## Testing

### Prerequisites

- Python 3 + pip
- Docker (running)
- Install the toolchain:

```bash
pip install ansible-core ansible-lint yamllint molecule molecule-plugins[docker]
ansible-galaxy collection install community.general
```

### Lint (fast — run before every commit)

```bash
yamllint .
ansible-lint
```

### Molecule (full integration test)

```bash
# Run full test suite (lint + converge + verify + destroy)
molecule test

# Converge and keep containers running for debugging
molecule converge
molecule login -h archlinux
molecule verify
molecule destroy
```

## License

MIT
