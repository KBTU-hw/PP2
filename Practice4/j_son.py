import json

n=int(input())
with open(r"c:\Users\Home\OneDrive\Desktop\PP2\Practice4\sample-data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print("Interface Status")
print("=" * 80)
print(f'{"DN":<50} {"Description":<20} {"Speed":<6} {"MTU":<6}')
print(f'{"-"*50} {"-"*20}  {"-"*6}  {"-"*6}')

for item in data["imdata"][:n]:
    attrs = item["l1PhysIf"]["attributes"]

    dn = attrs.get("dn", "")
    descr = attrs.get("descr", "")
    speed = attrs.get("speed", "")
    mtu = attrs.get("mtu", "")

    print(f"{dn:<50} {descr:<20}  {speed:<6}  {mtu:<6}")