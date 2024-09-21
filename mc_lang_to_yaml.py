import json
import yaml


def main():
    with open("mc_lang.json", "r", encoding="utf-8") as f:
        json_data: dict[str, str] = json.load(f)
    with open("mc_lang.yml", "r", encoding="utf-8") as f:
        yaml_data: dict[str, str] = yaml.load(f, Loader=yaml.FullLoader)

    result: dict[str, str] = {}
    for key, value in yaml_data.items():
        # 处理一些有问题的名称
        if key.endswith(
            tuple(
                i.replace(" ", "_").upper()
                for i in (
                    "White",
                    "Light gray",
                    "Gray",
                    "Black",
                    "Brown",
                    "Red",
                    "Orange",
                    "Yellow",
                    "Lime",
                    "Green",
                    "Cyan",
                    "Light blue",
                    "Blue",
                    "Purple",
                    "Magenta",
                    "Pink",
                )
            )
        ):
            key = key.split("_")[-1] + "_DYE"
        if key == "ZOMBIE_PIGMAN_SPAWN_EGG":
            result[key] = "僵尸猪人刷怪蛋"
            print(f"{key} {value} -> {result[key]}")
            continue
        if key.endswith("_BANNER"):
            # [COLOR]_BANNER -> item.minecraft.xxx_banner
            # [COLOR]_WALL_BANNER -> block.minecraft.xxx_wall_banner
            json_keys = [
                (
                    "block.minecraft."
                    + key.replace("_WALL_BANNER", "").replace("_BANNER", "").lower()
                    + "_banner"
                ),
            ]
            # 检查是否存在对应json键
            for json_key in json_keys:
                if json_key in json_data:
                    result[key] = json_data[json_key]
                    print(f"{key} {value} -> {json_key} {json_data[json_key]} (banner)")
                    break
            else:
                print(f"error: {key} {value} {json_keys} not found in json (banner)")
                break
            continue
        json_keys = [
            "item.minecraft." + key.lower(),
            "block.minecraft." + key.lower(),
            "block.minecraft." + "oak_" + key.lower(),
        ]
        # 检查是否存在对应json键
        for json_key in json_keys:
            if json_key in json_data:
                result[key] = json_data[json_key]
                print(f"{key} {value} -> {json_key} {json_data[json_key]}")
                break
        else:
            print(f"error: {key} {value} {json_keys} not found in json")
            break
    print("done, writing to mc_lang.out.yml")
    with open("mc_lang.out.yml", "w", encoding="utf-8") as f:
        yaml.dump(result, f, allow_unicode=True, sort_keys=True)


if __name__ == "__main__":
    main()
