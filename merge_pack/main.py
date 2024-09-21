import json
import os
from pathlib import Path
import tempfile
import zipfile


def main():
    # 获取资源包文件名
    pack_names = list((Path(__file__).parent / "original").iterdir())
    print("要处理的资源包", pack_names)
    if input("输入y继续").lower() != "y":
        return
    # 解压缩资源包到临时目录
    with tempfile.TemporaryDirectory() as tmp_dir:
        packs: list[Path] = []
        for pack_name in pack_names:
            pack_path = Path(tmp_dir) / pack_name.name
            zipfile.ZipFile(pack_name).extractall(pack_path)
            print(f"解压缩 {pack_name} 到 {pack_path}")
            packs.append(pack_path)
        # 把两个目录的文件合并到一起，不要打包zip！
        merged_pack_path = Path(tmp_dir) / "merged"
        merged_pack_path.mkdir()
        # walk两个目录，把所有文件都复制到merged目录，注意有多层目录要递归
        for pack_path in packs:
            for root, dirs, files in os.walk(pack_path, topdown=True):
                for file in files:
                    src_path = Path(root) / file
                    dst_path = merged_pack_path / src_path.relative_to(pack_path)
                    dst_path.parent.mkdir(parents=True, exist_ok=True)
                    # 如果目标文件在merged/assets/minecraft/models/item下
                    if (
                        dst_path.parent.parts[-3:]
                        == (
                            "minecraft",
                            "models",
                            "item",
                        )
                        and dst_path.exists()
                    ):
                        # 要合并json中的overrides数组，并按照custom_model_data排序
                        src_json = json.loads(src_path.read_text())
                        dst_json = json.loads(dst_path.read_text())
                        dst_json["overrides"].extend(src_json["overrides"])
                        dst_json["overrides"].sort(
                            key=lambda x: (
                                x["predicate"]["custom_model_data"]
                                if "predicate" in x
                                and "custom_model_data" in x["predicate"]
                                else 0
                            )
                        )
                        dst_path.write_text(json.dumps(dst_json, ensure_ascii=False))
                        print(f"合并 {src_path} 到 {dst_path}")
                        continue
                    # 如果目标文件在merged/assets/minecraft/atlases下
                    if (
                        dst_path.parent.parts[-2:]
                        == (
                            "minecraft",
                            "atlases",
                        )
                        and dst_path.exists()
                    ):
                        # 合并json中的sources数组，不用排序
                        src_json = json.loads(src_path.read_text())
                        dst_json = json.loads(dst_path.read_text())
                        dst_json["sources"].extend(src_json["sources"])
                        dst_path.write_text(json.dumps(dst_json, ensure_ascii=False))
                        print(f"合并 {src_path} 到 {dst_path}")
                        continue
                    src_path.replace(dst_path)
                    print(f"移动 {src_path} 到 {dst_path}")
        # 写入额外的文件（把extra目录下的文件复制到merged目录）
        extra_path = Path(__file__).parent / "extra"
        for root, dirs, files in os.walk(extra_path, topdown=True):
            for file in files:
                src_path = Path(root) / file
                dst_path = merged_pack_path / src_path.relative_to(extra_path)
                dst_path.parent.mkdir(parents=True, exist_ok=True)
                # tmp和源文件有可能在不同的挂载点，不能用replace，只能读取然后写入
                data = src_path.read_bytes()
                dst_path.write_bytes(data)
                print(f"extra: 复制 {src_path} 到 {dst_path}")
        print("合并完成，正在打包")
        # 打包merged目录为zip文件
        merged_pack_name = Path(__file__).parent / "merged.zip"
        # 使用极限压缩，压缩率最高但压缩时间最长
        with zipfile.ZipFile(
            merged_pack_name, "w", zipfile.ZIP_DEFLATED, compresslevel=9
        ) as f:
            for root, dirs, files in os.walk(merged_pack_path, topdown=True):
                for file in files:
                    path = Path(root) / file
                    f.write(path, path.relative_to(merged_pack_path))
                    print(f"打包 {path} 到 {merged_pack_name}")
        print(f"打包完成，输出文件 {merged_pack_name}")


if __name__ == "__main__":
    main()
