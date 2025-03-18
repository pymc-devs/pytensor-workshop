"""
This script is an export of pytensor_from_scratch.ipynb.
It was created to generate the UML and call charts in data/.
"""


class Type:
    "Baseclass for PyTensor types"

class Op:
    "Baseclass for PyTensor operations."

    def __str__(self):
        return self.__class__.__name__

class Node:
    "Baseclass for PyTensor nodes."


class Variable(Node):
    def __init__(self, name=None, *, type: Type):
        self.name = name
        self.type = type
        self.owner = None

    def __repr__(self):
        if self.name:
            return self.name
        return f"Variable(type={self.type})"

class Apply(Node):
    def __init__(self, op:Op, inputs, outputs):
        self.op = op
        self.inputs = inputs
        self.outputs = outputs
        for out in outputs:
            if out.owner is not None:
                raise ValueError("This variable already belongs to another Apply Node")
            out.owner = self

    def __repr__(self):
        return f"Apply(op={self.op.__class__.__name__}, inputs={self.inputs}, outputs={self.outputs})"


class TensorType(Type):
    def __init__(self, shape: tuple[float | None, ...], dtype: str):
        self.shape = shape
        self.dtype = dtype

    def __eq__(self, other):
        return (
            type(self) is type(other)
            and self.shape == other.shape
            and self.dtype == other.dtype
        )

    def __repr__(self):
        return f"TensorType(shape={self.shape}, dtype={self.dtype})"

class Add(Op):
    def make_node(self, a, b):
        if not(isinstance(a.type, TensorType) and isinstance(b.type, TensorType)):
            raise TypeError("Inputs must be tensors")
        if a.type != b.type:
            raise TypeError("Addition only supported for inputs of the same type")

        output_type = TensorType(shape=a.type.shape, dtype=a.type.dtype)
        output = Variable(type=output_type)
        return Apply(self, [a, b], [output])


add = Add()

dvector = TensorType(shape=(10,), dtype="float64")

x = Variable("x", type=dvector)
y = Variable("y", type=dvector)
[x_add_y] = add.make_node(x, y).outputs
x_add_y.name = "x + y"
x_add_y.owner

class Sum(Op):

    def make_node(self, a):
        if not(isinstance(a.type, TensorType)):
            raise TypeError("Input must be a tensor")
        output_type = TensorType(shape=(), dtype=a.type.dtype)
        output = Variable(type=output_type)
        return Apply(self, [a], [output])

sum = Sum()

[sum_x_add_y] = sum.make_node(x_add_y).outputs
sum_x_add_y.name = "sum(x + y)"
sum_x_add_y.owner





