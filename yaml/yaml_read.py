import yaml

with open('test.yaml', 'r') as yml:
    ap = yaml.safe_load(yml)
    print(ap)
    category = ap['category']
    print(category)
