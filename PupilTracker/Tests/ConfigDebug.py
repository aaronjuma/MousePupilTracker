import yaml

with open("config.yaml", "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

mouseNumber = str(config["Mouse"])
print(config["Mice"]["Mouse"+mouseNumber]["MEAN"]+config["Mice"]["Mouse"+mouseNumber]["STD"])