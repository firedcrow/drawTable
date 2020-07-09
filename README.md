# 用途
脱离Excel，实现纯代码绘制表格，提供较多参数用于自定义图标格式  

# 使用例
```python
data = [
    [1.0, 2.0, 3, 4, 5],
    [1, 3, 4, 5, 6],
    [1.0, 2.0, 3, 4, 5],
    [1, 3, 4, 5, 6],
    [1.0, 2.0, 3, 4, 5],
    [1, 3, 4, 5, 6]
]
columns = ["a", "b", "c", "d", "e"]


Table(data=data,
        columns=columns,
        save_file_path="test{}.png".format(i),
        line_split_style=False,
        last_line_color_style=False,
        fill_row_color_index_list=[1, 3, 4, 5]).draw()
```

# 安装字体
**仅提供Linux环境下的字体安装**  
若缺少字体文件，在图表中含有中文时会渲染不出来  
运行如下代码即可安装字体  
```bash
bash fonts/install_chinese_fonts.sh
```