import svgwrite

DIVISION_K1 = 0.28
DIVISION_K2 = 0.1
FONT_SIZE = 40.0
DIVISION_LINE_DISTANCE = 0.2


class TreeNode(object):
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.size = FONT_SIZE
        self.h_top = self.size
        self.h_bottom = 0.0
        self.width = self.size * 0.6

    def repr(self):
        pass

    def first_top_down_action(self):
        pass

    def second_top_down_action(self):
        pass

    def bottom_up_action(self):
        pass

    def first_traversal(self):
        pass

    def second_traversal(self):
        pass

    def svg(self, svg_doc, container):
        pass


class TernaryOpNode(TreeNode):
    def __init__(self, left, middle, right):
        super(TernaryOpNode, self).__init__()
        self.left = left
        self.middle = middle
        self.right = right

    def repr(self):
        return '{}{}{}{}{}[x: {}, y: {}, size: {}, h_top: {}, h_bottom: {}, width: {}]\n'.format(self.left.repr(), self.operator_1, self.middle.repr(), self.operator_2, self.right.repr(), self.x, self.y, self.size, self.h_top, self.h_bottom, self.width)

    def first_traversal(self):
        self.first_top_down_action()
        self.left.first_traversal()
        self.middle.first_traversal()
        self.right.first_traversal()
        self.bottom_up_action()

    def second_traversal(self):
        self.second_top_down_action()
        self.left.second_traversal()
        self.middle.second_traversal()
        self.right.second_traversal()

    def svg(self, svg_doc, container):
        self.left.svg(svg_doc, container)
        self.middle.svg(svg_doc, container)
        self.right.svg(svg_doc, container)


class BinaryOpNode(TreeNode):
    def __init__(self, left, right):
        super(BinaryOpNode, self).__init__()
        self.left = left
        self.right = right

    def repr(self):
        return '{}{}{}[x: {}, y: {}, size: {}, h_top: {}, h_bottom: {}, width: {}]\n'.format(self.left.repr(), self.operator, self.right.repr(), self.x, self.y, self.size, self.h_top, self.h_bottom, self.width)

    def first_traversal(self):
        self.first_top_down_action()
        self.left.first_traversal()
        self.right.first_traversal()
        self.bottom_up_action()

    def second_traversal(self):
        self.second_top_down_action()
        self.left.second_traversal()
        self.right.second_traversal()

    def svg(self, svg_doc, container):
        self.left.svg(svg_doc, container)
        self.right.svg(svg_doc, container)

class DivisionNode(BinaryOpNode):
    operator = '/'

    def first_top_down_action(self):
        self.left.size = self.size
        self.right.size = self.size

    def second_top_down_action(self):
        self.left.x = self.x + (self.width - self.left.width) / 2
        self.left.y = self.y - self.left.h_bottom - self.size * (DIVISION_K1 + 0.2)

        self.right.x = self.x + (self.width - self.right.width) / 2
        self.right.y = self.y + self.right.h_top

    def bottom_up_action(self):
        self.h_top = self.left.h_top + self.left.h_bottom + self.size * (DIVISION_K1 + 0.2)
        self.h_bottom = self.right.h_top + self.right.h_bottom
        self.width = max(self.left.width, self.right.width)

    def svg(self, svg_doc, container):
        super(DivisionNode, self).svg(svg_doc, container)
        x_min = min(self.left.x, self.right.x)
        line_y = self.left.y + self.left.h_bottom + self.size * 0.2
        container.add(svg_doc.line(start=(x_min, line_y), end=(x_min + self.width, line_y), stroke='black', stroke_width=str(0.05 * self.size)))

class ConcatenationNode(BinaryOpNode):
    operator = ''

    def first_top_down_action(self):
        self.left.size = self.size
        self.right.size = self.size

    def second_top_down_action(self):
        self.left.x = self.x
        self.left.y = self.y

        self.right.x = self.x + self.left.width
        self.right.y = self.y

    def bottom_up_action(self):
        self.h_top = max(self.left.h_top, self.right.h_top)
        self.h_bottom = max(self.left.h_bottom, self.right.h_bottom)
        self.width = self.left.width + self.right.width


class SuperindexNode(BinaryOpNode):
    operator = '^'

    def first_top_down_action(self):
        self.left.size = self.size
        self.right.size = self.size * 0.7

    def second_top_down_action(self):
        self.left.x = self.x
        self.left.y = self.y

        self.right.x = self.x + self.left.width
        self.right.y = self.y - self.left.h_top - 0.5 * self.right.h_bottom + 0.5 * self.right.size

    def bottom_up_action(self):
        self.h_top = self.left.h_top + self.right.h_top + 0.5 * self.right.h_bottom - self.right.size * 0.5
        self.h_bottom = self.left.h_bottom
        self.width = self.left.width + self.right.width


class SubindexNode(BinaryOpNode):
    operator = '_'

    def first_top_down_action(self):
        self.left.size = self.size
        self.right.size = self.size * 0.7

    def second_top_down_action(self):
        self.left.x = self.x
        self.left.y = self.y

        self.right.x = self.x + self.left.width
        self.right.y = self.y + 0.5 * self.right.h_top

    def bottom_up_action(self):
        self.h_top = self.left.h_top
        self.h_bottom = self.left.h_bottom + self.right.h_bottom + self.right.h_top * 0.5
        self.width = self.left.width + self.right.width


class SuperSubindexNode(TernaryOpNode):
    operator_1 = '^'
    operator_2 = '_'

    def first_top_down_action(self):
        self.left.size = self.size
        self.middle.size = self.size * 0.7
        self.right.size = self.size * 0.7

    def second_top_down_action(self):
        self.left.x = self.x
        self.left.y = self.y

        self.middle.x = self.x + self.left.width
        self.middle.y = self.y - self.left.h_top - 0.5 * self.middle.h_bottom + 0.5 * self.middle.size

        self.right.x = self.x + self.left.width
        self.right.y = self.y + 0.5 * self.right.h_top

    def bottom_up_action(self):
        self.h_top = self.left.h_top + self.middle.h_top + 0.5 * self.middle.h_bottom - self.middle.size * 0.5
        self.h_bottom = self.left.h_bottom + self.right.h_bottom + self.right.h_top * 0.5
        self.width = self.left.width + max(self.middle.width, self.right.width)


class SubSuperindexNode(TernaryOpNode):
    operator_1 = '_'
    operator_2 = '^'

    def first_top_down_action(self):
        self.left.size = self.size
        self.middle.size = self.size * 0.7
        self.right.size = self.size * 0.7

    def second_top_down_action(self):
        self.left.x = self.x
        self.left.y = self.y

        self.middle.x = self.x + self.left.width
        self.middle.y = self.y + 0.5 * self.middle.h_top

        self.right.x = self.x + self.left.width
        self.right.y = self.y - self.left.h_top - 0.5 * self.right.h_bottom + 0.5 * self.right.size

    def bottom_up_action(self):
        self.h_top = self.left.h_top + self.right.h_top + 0.5 * self.right.h_bottom - self.right.size * 0.5
        self.h_bottom = self.left.h_bottom + self.middle.h_bottom + self.middle.h_top * 0.5
        self.width = self.left.width + max(self.middle.width, self.right.width)


class ParenthesesNode(TreeNode):
    def __init__(self, child):
        super(ParenthesesNode, self).__init__()
        self.child = child

    def repr(self):
        return '({})[x: {}, y: {}, size: {}, h_top: {}, h_bottom: {}, width: {}]\n'.format(self.child.repr(), self.x, self.y, self.size, self.h_top, self.h_bottom, self.width)

    def first_top_down_action(self):
        self.child.size = self.size

    def second_top_down_action(self):
        self.child.x = self.x + 0.6 * self.size
        self.child.y = self.y

    def bottom_up_action(self):
        self.h_top = self.child.h_top
        self.h_bottom = self.child.h_bottom
        self.width = self.child.width + 2 * self.size * 0.6

    def first_traversal(self):
        self.first_top_down_action()
        self.child.first_traversal()
        self.bottom_up_action()

    def second_traversal(self):
        self.second_top_down_action()
        self.child.second_traversal()

    def svg(self, svg_doc, container):
        height = self.h_bottom + self.h_top
        var = self.y*0.3 if self.y > 0 else 0
        container.add(svg_doc.text('(',
            insert=(0, 0),
            font_size=str(self.size),
            transform='translate({},{}) scale(1,{})'.format(self.x, self.y +  0.5 * self.h_bottom, (height * 1.3) / FONT_SIZE)))
        container.add(svg_doc.text(')',
            insert=(0, 0),
            font_size=str(self.size),
            transform='translate({},{}) scale(1,{})'.format(self.x + self.width - self.size * 0.6, self.y + 0.5 * self.h_bottom, (height * 1.3) / FONT_SIZE)))
        self.child.svg(svg_doc, container)

class OperandNode(TreeNode):
    def __init__(self, value):
        super(OperandNode, self).__init__()
        self.value = value

    def repr(self):
        return '{}[x: {}, y: {}, size: {}, h_top: {}, h_bottom: {}, width: {}]\n'.format(self.value, self.x, self.y, self.size, self.h_top, self.h_bottom, self.width)

    def bottom_up_action(self):
        self.h_top = self.size
        self.h_bottom = 0
        self.width = 0.6 * self.size

    def first_traversal(self):
        self.bottom_up_action()

    def svg(self, svg_doc, container):
        container.add(svg_doc.text(self.value,
            insert=(self.x, self.y),
            font_size=str(self.size)))

