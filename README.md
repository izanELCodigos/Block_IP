# Windows Firewall IP Blocker

A lightweight GUI utility built with Python and CustomTkinter to automate inbound IP blocking rules in Windows Firewall via PowerShell.

## Features

- **Automated validation:** Validates IPv4 syntax and prevents blocking critical networking ranges (Loopback `127.0.0.0/8`, Multicast `224.0.0.0/4`, Public DNS...).
- **Dynamic rule management:** Automatically checks if a `Block_IP` rule exists. It creates a new rule or appends the target IP to the existing array without overwriting previous blocks.
- **UAC privilege escalation:** Leverages Windows `ShellExecuteW` (`runas`) to request elevated permissions cleanly for PowerShell operations.
- **Custom UI controls:** Implements auto-focus and input filtering across octet entry fields.

## Tech stack

- **Python 3.x** (CustomTkinter, `subprocess`, `ctypes`)
- **PowerShell** (`NetSecurity` module)

## Dependencies
Installing Python's CustomTinker module for execution is needed. Run this code below on your terminal:
```powershell
pip install customtkinter
```

## How it works

1. **Input filtering:** The GUI restricts inputs to numeric values and handles keyboard navigation between octet boxes.
2. **Validation:** Checks octet bounds ($0-255$) and verifies against restricted IP lists.
3. **Execution:** Executes an elevated PowerShell process to update or inject firewall rules:
   ```powershell
   # Dynamic array update logic used in backend
   $current = @(Get-NetFirewallRule -Name 'Block_IP' | Get-NetFirewallAddressFilter | Select-Object -ExpandProperty RemoteAddress)
   Set-NetFirewallRule -Name 'Block_IP' -RemoteAddress ($current + 'TARGET_IP')

> [!WARNING]
> This tool DOES NOT cover all not dangerous IP adresses from being blocked. Check twice before applying changes.
