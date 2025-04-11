# 7セグメント表示パターン
SEGMENTS = {
    '0': [1, 1, 1, 1, 1, 1, 0],
    '1': [0, 1, 1, 0, 0, 0, 0],
    '2': [1, 1, 0, 1, 1, 0, 1],
    '3': [1, 1, 1, 1, 0, 0, 1],
    '4': [0, 1, 1, 0, 0, 1, 1],
    '5': [1, 0, 1, 1, 0, 1, 1],
    '6': [1, 0, 1, 1, 1, 1, 1],
    '7': [1, 1, 1, 0, 0, 0, 0],
    '8': [1, 1, 1, 1, 1, 1, 1],
    '9': [1, 1, 1, 1, 0, 1, 1],
    ':': [0, 0, 0, 0, 0, 0, 0]
}

# セグメントの描画座標（7本）
SEG_POS = [
    ((10, 13), (60, 13)),    # 上 0
    ((60, 10), (60, 60)),    # 右上 1
    ((60, 60), (60, 110)),   # 右下 2
    ((10, 107), (60, 107)),  # 下 3
    ((10, 60), (10, 110)),   # 左下 4
    ((10, 10), (10, 60)),    # 左上 5
    ((10, 60), (60, 60)),    # 中央 6
]

class SevenSegmentDigit:
    def __init__(self, canvas,x):
        self.canvas = canvas
        self.segments = [
        ]
        self.x_offset = 8
        self.figure_offset = x
        self.create_segments()

    def create_segments(self):
        for i in range(7):
            (x1, y1), (x2, y2) = SEG_POS[i] 
            x1 = (x1 + self.figure_offset) 
            x2 = (x2 +  self.figure_offset) 
            y1 = y1
            y2 = y2
            if i == 6:
                points = [
                    (x1, y1),
                    (x1 + self.x_offset, y1 + self.x_offset),
                    (x2 - self.x_offset, y1 + self.x_offset),
                    (x2, y2),
                    (x2 - self.x_offset, y1 - self.x_offset),
                    (x1 + self.x_offset, y1 - self.x_offset),
                ]
            elif i == 1 or i == 2:
                points = [
                    (x1 + 4, y1),
                    (x1 + self.x_offset, y1 + self.x_offset),
                    (x1 + self.x_offset, y2 - self.x_offset),
                    (x2 + 4, y2),
                    (x1 - self.x_offset, y2 - self.x_offset-4),
                    (x1 - self.x_offset, y1 + self.x_offset+4),
                ]
            elif i == 4 or i == 5:
                points = [
                    (x1 - 4 , y1),
                    (x1 + self.x_offset, y1 + self.x_offset+4),
                    (x1 + self.x_offset, y2 - self.x_offset-4),
                    (x2 - 4 , y2),
                    (x1 - self.x_offset, y2 - self.x_offset),
                    (x1 - self.x_offset, y1 + self.x_offset),
                ]
            elif i == 0:  # 縦線（左右上下）
                points = [
                    (x1, y1 - 4),
                    (x1 + self.x_offset+4, y1 + self.x_offset),
                    (x2 - self.x_offset-4, y1 + self.x_offset),
                    (x2, y2 -4),
                    (x2 - self.x_offset, y1 - self.x_offset),
                    (x1 + self.x_offset, y1 - self.x_offset),
                ]
            elif i == 3:
                points = [
                    (x1, y1 + 4),
                    (x1 + self.x_offset, y1 + self.x_offset),
                    (x2 - self.x_offset, y1 + self.x_offset),
                    (x2, y2 +4),
                    (x2 - self.x_offset -4, y1 - self.x_offset),
                    (x1 + self.x_offset+ 4, y1 - self.x_offset),
                ]

            # 各点にシアー変換を適用
            sheared_points = []
            for px, py in points:
                sx =px + int(-0.00 * py)
                sheared_points.extend([sx, py])
                
            seg = self.canvas.create_polygon(sheared_points)
            self.segments.append(seg)

    def draw(self, digit):
        pattern = SEGMENTS.get(digit, [0]*7)
        for i, val in enumerate(pattern):
            self.canvas.itemconfig(self.segments[i], fill='red' if val else 'gray14')
