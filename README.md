# ImageWebshell

将一句话木马隐藏到像素颜色中，生成抗裁剪的PNG图片马

除了生成一句话木马之外还支持生成带有任意文本的PNG图片

## 安装

`pip install -r requirements.txt`

## 使用

`python -m image_webshell`，然后将`output.png`传到目标上，后缀改为PHP即可

命令行选项：

`text`: 指定webshell文本，注意不要使用会被deflate过度压缩的文本（即不要带有重复字符或者连续的小写字母等）
`width`: 指定图像的宽度，不宜太宽
`height`: 指定图像的高度
`output`: 图像保存地址
