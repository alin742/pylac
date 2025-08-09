from typing import Any, Self
from collections import ChainMap

CONTAINER_DEFAULTS = {
    'x': 0,
    'y': 0,
    'width': 0,
    'height': 0,
    'min_width': 0,
    'min_height': 0,
    'padding': [0, 0, 0, 0],
}
STACK_DEFAULTS = {
    'gap': 0,
}
GRID_DEFAULTS = {
    'gv': 0.0,
    'gh': 0.0,
    'row_first': True
}

class Container():
    id: str
    min_dim: list[float] # min_width, min_height
    dim: list[float] # x, y, width, height
    pad: list[float] # padding_left, padding_right, padding_top, padding_bottom
    children: list[Self]
    ratios: list[int]

    def __init__( self, id, **params ) -> Self:
        cm = ChainMap(params, CONTAINER_DEFAULTS)
        self.id = id
        self.min_dim = [
            cm['min_width'], cm['min_height']
        ]
        self.dim = [
            cm['x'],
            cm['y'],
            cm['width'],
            cm['height'],
        ]
        self.pad = cm['padding']
        self.children = []
        self.ratios = []

    def set_padding(self, p: float | list[float]):
        if isinstance(p, float):
            self.pad = [p, p, p, p]
        elif isinstance(p, list):
            if len(p) == 2:
                self.pad = [p[0], p[0], p[1], p[1]]
            elif len(p) == 4:
                self.pad = [p[0], p[1], p[2], p[3]]
            else:
                raise ValueError("Expects a float or a list of 2 floats or a list of 4 floats but got a list of %d floats"% len(p))
        else:
            raise ValueError("Expects a float or a list of floats, got a %s"% type(p))

    def set_x(self, x: float):
        self.dim[0] = x

    def set_y(self, y: float):
        self.dim[1] = y

    def set_pos(self, x: float, y: float):
        self.dim[0] = x
        self.dim[1] = y

    def set_width(self, w: float):
        self.dim[2] = w

    def set_height(self, h: float):
        self.dim[3] = h

    def set_dim(self, w: float, h: float):
        self.dim[2] = w
        self.dim[3] = h

    def get_layout(self) -> dict[str, Any]:
        if not self.children:
            return {"dim": self.dim}
        else:
            return {"dim": self.dim } | { child.id: child.get_layout() for child in self.children }

    def add(self, child: Self, ratio: int = 1):
        self.children.append(child)
        self.ratios.append(ratio)

    def update(self):
        map(lambda child: child.update(), self.children)
                

class VStack(Container):
    gap: float
    el_h: float
    el_w: float
    def __init__( self, id: str, **params ):
        cm = ChainMap(params, CONTAINER_DEFAULTS, STACK_DEFAULTS)
        super().__init__(id, **params)
        self.gap = cm['gap']
        self.el_h = 0.0
        self.el_w = 0.0

    def set_gap(self, g: float):
        if g > 0.0:
            self.gap = g

    def update(self):
        n = len(self.children)
        if n > 0:
            r_sum = sum(self.ratios)
            xs = self.dim[0] + self.pad[0] # x + pl
            xe = self.dim[0] + self.dim[2] - self.pad[1] # x + w - pr
            ys = self.dim[1] + self.pad[2] # y + pt
            ye = self.dim[1] + self.dim[3] - self.pad[3] # y + h - pb
            total_gaps = float(n-1) * self.gap
            self.el_h = (ye - ys - total_gaps)/float(n)
            self.el_w = xe - xs
            prev_y = ys
            for child, ratio in zip(self.children, self.ratios):
                ratio = float(ratio)/float(r_sum)
                child.set_pos(xs, prev_y)
                child.set_dim(self.el_w, n * self.el_h * ratio)
                child.update()
                prev_y = prev_y + (n * self.el_h * ratio) + self.gap



class HStack(Container):
    gap: float
    el_h: float
    el_w: float

    def __init__( self, id: str, **params ):
        cm = ChainMap(params, CONTAINER_DEFAULTS, STACK_DEFAULTS)
        super().__init__(id, **params)
        self.gap = cm['gap']
        self.el_h = 0.0
        self.el_w = 0.0

    def set_gap(self, g: float):
        if g > 0.0:
            self.gap = g

    def update(self):
        n = len(self.children)
        if n > 0:
            r_sum = sum(self.ratios)
            xs = self.dim[0] + self.pad[0] # x + pl
            xe = self.dim[0] + self.dim[2] - self.pad[1] # x + w - pr
            ys = self.dim[1] + self.pad[2] # y + pt
            ye = self.dim[1] + self.dim[3] - self.pad[3] # y + h - pb
            total_gaps = float(n-1) * self.gap
            self.el_h = ye - ys
            self.el_w = (xe - xs - total_gaps)/float(n)
            prev_x = xs
            for child, ratio in zip(self.children, self.ratios):
                ratio = float(ratio)/float(r_sum)
                child.set_pos(prev_x, ys)
                child.set_dim(n * self.el_w * ratio, self.el_h)
                child.update()
                prev_x = prev_x + (n * self.el_w * ratio) + self.gap


class Grid(Container):
    gap_v: float
    gap_h: float
    r: int
    c: int
    el_h: float
    el_w: float
    row_first: bool

    def __init__( self, id: str, r: int, c: int, **params ):
        cm = ChainMap(params, CONTAINER_DEFAULTS, STACK_DEFAULTS, GRID_DEFAULTS)
        super().__init__(id, **params)
        self.r = r
        self.c = c
        if 'gap' in params and params['gap'] != 0.0:
            self.gap_h = cm['gap']
            self.gap_v = cm['gap']
        else: 
            self.gap_h = cm['gh']
            self.gap_v = cm['gv']
        self.row_first = cm['row_first']
        self.el_h = 0.0
        self.el_w = 0.0
        self.cap = r*c

    def set_gap(self, g):
        if g > 0.0:
            self.gap_h = g
            self.gap_v = g

    def set_gaps(self, gh: float, gv: float):
        if gh > 0.0:
            self.gap_h = gh
        if gv > 0.0:
            self.gap_v = gv

    def add(self, child: Self):
        if len(self.children) < self.cap:
            self.children.append(child)

    def fill_row_first(self, row_first: bool):
        self.row_first = row_first

    def update(self):
        n = len(self.children)
        if n > 0:
            xs = self.dim[0] + self.pad[0] # x + pl
            xe = self.dim[0] + self.dim[2] - self.pad[1] # x + w - pr
            ys = self.dim[1] + self.pad[2] # y + pt
            ye = self.dim[1] + self.dim[3] - self.pad[3] # y + h - pb
            total_gaps_v = float(self.r-1) * self.gap_v
            total_gaps_h = float(self.c-1) * self.gap_h
            self.el_h = (ye - ys - total_gaps_v)/float(self.r)
            self.el_w = (xe - xs - total_gaps_h)/float(self.c)
            counter = 0
            if self.row_first:
                prev_x = xs
                for i in range(self.c):
                    prev_y = ys
                    for j in range(self.r):
                        if counter < len(self.children):
                            child = self.children[counter]
                            counter += 1
                            child.set_pos(prev_x, prev_y)
                            child.set_dim(self.el_w, self.el_h)
                            child.update()
                            prev_y = prev_y + self.el_h + self.gap_v
                    prev_x = prev_x + self.el_w + self.gap_h
            else:
                prev_y = ys
                for i in range(self.r):
                    prev_x = xs
                    for j in range(self.c):
                        if counter < len(self.children):
                            child = self.children[counter]
                            counter += 1
                            child.set_pos(prev_x, prev_y)
                            child.set_dim(self.el_w, self.el_h)
                            child.update()
                            prev_x = prev_x + self.el_w + self.gap_h
                    prev_y = prev_y + self.el_h + self.gap_v


