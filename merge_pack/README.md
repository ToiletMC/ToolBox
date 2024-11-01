# 简单资源包合并

### 简介

主要是将两个压缩包合并，但提供额外功能：

- 合并 assets\minecraft\models\item 中的 json，按照 overrides 中的谓词从小到大排序合并。
- 合并 assets\minecraft\atlases 中的 json。

### 使用方法：

1. 将需要合并的资源包放入 original 目录。
2. 将其他额外文件放入 extra 目录，会最后添加到资源包中。
3. Python，启动！

### TO-DO

- [ ] 未来可能需要合并 assets\minecraft\sounds.json，因为粘液科技现在增加了一个空的声音文件。
