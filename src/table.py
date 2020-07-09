# @Time    : 2020-06-08 10:46
# @Author  : wangjunjie.09
# @File    : table.py
# @User    : wangjunjie

import sys

sys.path.append(".")

from matplotlib import pyplot as plt


def is_number(s):
    s = str(s).replace("%", "")
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


class Table():
    """
    绘图数据表格用，保存到本地，返回文件名，文件名可自定义
    """

    def __init__(self, data=None,
                 columns=None,
                 header_column=False,
                 need_column=True,
                 save_file_path=None,
                 font=None,
                 watermark_text=None,
                 line_split_style=True,
                 last_line_color_style=True,
                 col_color_style="#FFD700",
                 col_text_color_style="black",
                 row_color_style="#FFFFD0",
                 fill_row_color_index_list=None,
                 widths_list=None,
                 height=0.55,
                 width=1.5,
                 inner_line_show=True,
                 debug_mode=False
                 ):
        """
        :param data: 绘图的数据源
        :param columns: 手动指定的表头
        :param header_column: 是否取第一行数据作为表头
        :param need_column: 是否需要表头
        :param save_file_path: 保存的路径
        :param font: 采用的字体
        :param watermark_text: 水印文本
        :param line_split_style: 是否每行分割
        :param last_line_color_style：最后一行是否填充颜色
        :param col_color_style: 表头行的颜色
        :param col_text_color_style：表头行的字体颜色
        :param row_color_style: 实际行的颜色ne
        :param fill_row_color_index_list：需要手动填充行的index，List
        :param widths_list：手动指定宽度，List格式
        :param height:高度
        :param width:宽度
        :param inner_line_show：展示内部的分割线
        :param debug_mode：True时直接show，False保存到本地
        """

        assert isinstance(data, list) or isinstance(data, tuple), "data必须为list格式"
        assert not columns or isinstance(columns, list), "columns必须为list格式"
        assert len(data) >= 1, "data的长度至少大于1"
        assert fill_row_color_index_list is None or isinstance(fill_row_color_index_list,
                                                               list), "row_color_index 必须为 List"

        if columns:
            self.columns = columns
        elif header_column:
            self.columns = data.pop(0)  # 提取第一行作为列

        self.data = data
        self.save_file_path = save_file_path
        self.need_column = need_column
        self.watermark_text = watermark_text
        self.line_split_sytle = line_split_style
        self.last_line_color_style = last_line_color_style
        self.col_color_style = col_color_style
        self.col_text_color_style = col_text_color_style
        self.row_color_style = row_color_style
        self.fill_row_color_index_list = fill_row_color_index_list
        self.widths_list = widths_list
        self.height = height
        self.width = width
        self.inner_line_show = inner_line_show
        self.debug_mode = debug_mode

        if not font:
            # plt.rcParams['font.sans-serif'] = ['SimHei']
            plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
        else:
            plt.rcParams['font.sans-serif'] = [font]

    def draw(self):

        if not self.widths_list:  # 是否要自动获取宽度
            widths = self.__cal_columns_widths()  # 获取宽度
        else:
            widths = self.widths_list

        cell_colours, col_colours = self.__add_style()  # 获取样式的颜色

        fig = plt.figure(figsize=(self.width * len(self.data[0]), self.height * len(self.data)))  # 初始化画布

        ax = fig.add_subplot(111, frameon=True, xticks=[], yticks=[])  # 边框透明化
        for side in ("top", "right", "bottom", "left"):
            ax.spines[side].set_visible(False)

        bbox = [-0.1, 0, 1.2, 1]

        the_table = plt.table(cellText=self.data, colLabels=self.columns,
                              colWidths=widths, loc='center', cellLoc='center',
                              cellColours=cell_colours, colColours=col_colours, bbox=bbox)
        the_table.set_fontsize(16)
        the_table.scale(3.2, 3.2)

        self.__cell_handle(the_table)  # 单元格进行处理

        if self.watermark_text:
            self.__add_water_mark(fig, self.watermark_text)

        if self.debug_mode:
            plt.show()
        else:
            plt.savefig(self.save_file_path, bbox_inches='tight')
        plt.close()
        return self.save_file_path

    def __cal_columns_widths(self):
        """
        自适应计算宽的长度
        """
        columns = self.columns
        data = self.data
        max_width = []

        columns_width = [len(str(i)) for i in columns]
        for i in range(len(data[0])):  # 竖着取

            store = []
            for j in range(len(data)):
                store.append(len(str(data[j][i])))  # data[j][i] 表示竖着，为了取max的宽度

            max_width.append(max(store + [columns_width[i]]) + 1)  # 取出这一列中最大的宽度

        return max_width

    def __add_style(self):
        """
        增加样式
        """

        col_length = len(self.data[0])
        row_length = len(self.data)

        cell_colours = [
            ["w" for i in range(col_length)] for j in range(row_length)
        ]

        row_color_cell_colour = [self.row_color_style for i in range(col_length)]

        if self.line_split_sytle:  # 隔行分割上色
            for i in range(1, len(self.data), 2):
                cell_colours[i] = row_color_cell_colour


        if self.fill_row_color_index_list:  # 特定行填充颜色
            for i in self.fill_row_color_index_list:
                cell_colours[i] = row_color_cell_colour

        if self.last_line_color_style:  # 最后一行填充颜色
            cell_colours[-1] = row_color_cell_colour

        col_colours = [self.col_color_style] * col_length

        return cell_colours, col_colours

    def __add_water_mark(self, fig, water_mark):
        """
        增加水印，野鸡写法，可以自己重写
        """
        for x in (0.4, 0.7):
            for y in (0.4, 0.7):
                fig.text(x, y, water_mark, rotation=1,
                         fontsize=20, color='gray',
                         ha='right', va='bottom', alpha=0.1)
        return fig

    def __cell_handle(self, the_table):
        """
        单元格的处理，改颜色啥的
        """
        table_cells = the_table.properties()['children']  # 这一段为了把<0的数标红
        for cell in table_cells:
            if is_number(cell._text._text) and cell._text._text[0] == "-":
                cell._text.set_color('r')

        col_cell_index = -1 * len(self.data[0])  # 列头开始的索引
        for cell in table_cells[col_cell_index:]:  # 最后一行增加颜色，最后一行多半是总和，特殊标记出来
            cell._text.set_color(self.col_text_color_style)

        if not self.inner_line_show:  # 中间间隔是否要透明化
            for key, cell in the_table.get_celld().items():
                cell.set_linewidth(0)


if __name__ == '__main__':

    data = [
        [1.0, 2.0, 3, 4, 5],
        [1, 3, 4, 5, 6],
        [1.0, 2.0, 3, 4, 5],
        [1, 3, 4, 5, 6],
        [1.0, 2.0, 3, 4, 5],
        [1, 3, 4, 5, 6]
    ]
    columns = ["a", "b", "c", "d", "e"]

    for i in range(1):
        Table(data=data,
              columns=columns,
              save_file_path="test{}.png".format(i),
              line_split_style=False,
              last_line_color_style=False,
              fill_row_color_index_list=[1,3,5],
              debug_mode=False).draw()
