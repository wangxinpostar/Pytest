import operator

class BuildParseTree:


    def __init__(self, fpexp):
        self.fplist = fpexp.split()

    def buildParseTree(self):
        """
        构建解析树
        使用栈来保存父节点
        """
        pStack = Stack()
        eTree = BinaryTree('')
        pStack.push(eTree)
        curentTree = eTree
        for i in self.fplist:
            # 如果标记是 (， 为当前节点创建一个子节点， 并下沉至该节点
            if i == "(":

                curentTree.insertLeft("")
                pStack.push(curentTree)
                curentTree = curentTree.getLeftChild()
            # 如果当前标记在列表["+", "-", "/", "*"], 将当前节点的值设置为当前标记对应的运算符；为当前节点穿件一个右节点并下沉至该节点
            elif i not in "=-*/":
                curentTree.setRootVal(eval(i))
                parent = pStack.pop()
                curentTree = parent
            # 如果当前值是是数值， 就将当前节点的数值设置为该数值并返回至父节点
            elif i in "=-*/":
                curentTree.setRootVal(eval(i))
                curentTree.insertRight("")
                pStack.push(curentTree)
                curentTree.getRightChild()
            # 如果标记是), 则跳到当前节点的父节点
            elif i == ")":
                parent = pStack.pop()
                curentTree = parent
            else:
                raise ValueError("Error: %s" % i)
        return eTree

    def evaluate(self, parseTree):
        """
        计算解析树
        """

        # 构建运算操作字典
        opers = {
            "+": operator.add,
            "-": operator.sub,
            "*": operator.mul,
            "/": operator.truediv
        }

        leftC = parseTree.getLeftChild()
        rightC = parseTree.getRightChild()
        if leftC and rightC:
            fn = opers[parseTree.getRootVal()]
            return fn(self.evaluate(leftC), self.evaluate(rightC))
        else:
            return parseTree.getRootVal()

if __name__ == "__main__":
    formulas = "((7+3)*(8-6))"
    fTree = BuildParseTree(formulas)
    eTree = fTree.buildParseTree()
    value = fTree.evaluate(eTree)
    print("%s = " % formulas, value)

class BinaryTree:
    """
    利用节点与引用创建二叉树
    """
    
    def __init__(self, rootObj):
        self.key = rootObj
        self.leftChild = None
        self.rightChild = None


    def insertLeft(self, newNode):
        """
        插入左节点
        """
        if self.leftChild is None:
            self.leftChild = BinaryTree(newNode)
        else:
            t = BinaryTree(newNode)
            t.leftChild = self.leftChild
            self.leftChild = t
    
    def insertRight(self, newNode):
        """
        插入右节点
        """
        if self.rightChild is None:
            self.rightChild = BinaryTree(newNode)
        else:
            t = BinaryTree(newNode)
            t.rightChild = self.rightChild
            self.rightChild = t

    def getRightChild(self):
        """
        返回当前节点的右节点和对应的二叉树
        """
        return self.rightChild

    def getLeftChild(self):
        """
        返回当前节点的左节点和对应的二叉树
        """
        return self.leftChild

    def getRootVal(self):
        """
        获取当前节点的数值
        """
        return self.key

    def setRootVal(self, obj):
        """
        存储当前节点的数值
        """
        self.key = obj
class Stack():

    def __init__(self):
        self.items = list()

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[-1]

    def size(self):
        return len(self.items)


if __name__ == "__main__":
    stack = Stack()
    stack.push(1)
    stack.push(2)
    stack.push(3)
    stack.push(4)
    print(stack.items)
    print(stack.peek())
    print(stack.isEmpty())
