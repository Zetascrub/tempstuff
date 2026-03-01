import os

input_file = "code.txt"
output_file = "config.manifest"

# Load the binary data
with open(input_file, "rb") as f:
    raw = f.read()

# Hex encode (lowercase, 2-digit)
hexdata = ''.join(format(b, '02x') for b in raw)

# Split into multiple <entry> values
chunks = [hexdata[i:i+64] for i in range(0, len(hexdata), 64)]
key_prefixes = ["theme", "layout", "hint", "render", "guid", "font"]

entries = ""
for idx, chunk in enumerate(chunks):
    key = f"{key_prefixes[idx % len(key_prefixes)]}_{100+idx}"
    entries += f'        <entry key="{key}" value="{chunk}"/>\n'

# Template with harmless XML structure
manifest = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
  <trustInfo xmlns="urn:schemas-microsoft-com:asm.v3">
    <security>
      <requestedPrivileges>
        <requestedExecutionLevel level="asInvoker" uiAccess="false"/>
      </requestedPrivileges>
      <config>
{entries}      </config>
    </security>
  </trustInfo>
</assembly>
'''

# Write to output
with open(output_file, "w", encoding="utf-8") as f:
    f.write(manifest)

print(f"[+] Stealth manifest written to: {output_file}")
