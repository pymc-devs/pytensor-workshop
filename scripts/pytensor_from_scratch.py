#!/usr/bin/env python
# coding: utf-8

# <a href="https://colab.research.google.com/github/pymc-devs/pytensor-workshop/blob/main/notebooks/walkthrough/pytensor_from_scratch.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

# ## Basic PyTensor objects

# In[1]:


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


# ## Writing our first tensor graph

# In[2]:


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


# In[3]:


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


# In[4]:


import pytensor
# Make our Variable a class of the PyTensor Variable
pytensor.graph.basic.Variable.register(Variable)

pytensor.dprint(sum_x_add_y)


# ## Evaluating a graph

# In[5]:


def add_perform(self, inputs):
    a, b = inputs
    return [a + b]

Add.perform = add_perform

def sum_perform(self, inputs):
    [a] = inputs
    return [a.sum()]

Sum.perform = sum_perform


# In[6]:


def eval(var, given):
    if var in given:
        return given[var]

    if var.owner is None:
        raise ValueError("Root variable must be given values")

    evaled_inputs = [eval(input, given) for input in var.owner.inputs]
    evaled_outputs = var.owner.op.perform(evaled_inputs)
    for output, evaled_output in zip(var.owner.outputs, evaled_outputs):
        given[output] = evaled_output
    return given[var]

import numpy as np
eval(sum_x_add_y, {x: np.arange(10), y: np.arange(10)})


# In[7]:


eval(sum_x_add_y, {x_add_y: np.arange(10)})


# ## Constants

# In[8]:


class Constant(Variable):
    def __init__(self, data, *, type: Type):
        self.data = data
        super().__init__(type=type)

    def __repr__(self):
        return str(self.data)

def eval(var, given):
    if var in given:
        return given[var]

    if isinstance(var, Constant):
        return var.data

    if var.owner is None:
        raise ValueError("Root variable must be given values")

    evaled_inputs = [eval(input, given) for input in var.owner.inputs]
    evaled_outputs = var.owner.op.perform(evaled_inputs)
    for output, evaled_output in zip(var.owner.outputs, evaled_outputs):
        given[output] = evaled_output
    return given[var]


# In[9]:


two = Constant(np.full((10,), 10), type=dvector)
two


# In[10]:


x_add_2 = add.make_node(x, two).outputs[0]
eval(x_add_2, {x: np.arange(10)})


# ## Making it easier to work with

# In[11]:


def type_call(self, name: str | None = None):
    """Create a variable with self type when calling the type."""
    return Variable(name=name, type=self)

Type.__call__ = type_call


# In[12]:


def op_call(self, *args, name: str | None = None):
    """Create a node with self operation and return the output when calling the operation."""
    node = self.make_node(*args)
    if len(node.outputs) == 1:
        out = node.outputs[0]
        out.name = name
        return out
    else:
        return node.outputs

Op.__call__ = op_call


# In[13]:


Variable.eval = eval
Variable.dprint = pytensor.dprint


# In[14]:


class Sum(Op):
    def __init__(self, axis: tuple[int]):
        self.axis = axis

    def make_node(self, a):
        if not(isinstance(a.type, TensorType)):
            raise TypeError("Input must be a tensor")
        output_shape = tuple(
            dim
            for i, dim in enumerate(a.type.shape)
            if i not in self.axis
        )
        out_var = TensorType(shape=output_shape, dtype=a.type.dtype)()
        return Apply(self, [a], [out_var])

    def perform(self, inputs):
        [a] = inputs
        return [a.sum(axis=self.axis)]

    def __str__(self):
        return f"Sum(axis={self.axis})"


# In[15]:


dmatrix = TensorType(shape=(3, 5), dtype="float64")
x = dmatrix(name="x")
out = Sum(axis=(1,))(add(x, x))


# In[16]:


out.type


# In[17]:


pytensor.dprint(out)


# In[18]:


out.eval({x: np.arange(15).reshape((3, 5))})


# ## Rewrites the clumsy way

# In[19]:


class Mul(Op):
    def make_node(self, a, b):
        if not(isinstance(a.type, TensorType) and isinstance(b.type, TensorType)):
            raise TypeError("Inputs must be tensors")
        if a.type.dtype != b.type.dtype:
            raise TypeError("Multiplication only supported for inputs of the same dtype")
        output_shape = np.broadcast_shapes(a.type.shape, b.type.shape)
        output = TensorType(shape=output_shape, dtype=a.type.dtype)()
        return Apply(self, [a, b], [output])

    def perform(self, inputs):
        [a, b] = inputs
        return [a * b]

mul = Mul()


# In[20]:


pytensor.dprint(out)


# In[21]:


scalar = TensorType(shape=(), dtype="float64")
two_x = mul(x, Constant(np.array(2.0), type=scalar))


# In[22]:


# Just change the input that goes into the Sum!
out.owner.inputs[0] = two_x


# In[23]:


out.dprint()


# In[24]:


out.eval({x: np.arange(15).reshape((3, 5))})


# ## Rewrites the proper way

# In[25]:


out = Sum(axis=(1,))(add(x, x))


# In[26]:


def clone_graph(var, clone_dict=None):
    if clone_dict is None:
        clone_dict = {}
    if var in clone_dict:
        return var
    if var.owner is None:
        # Reuse root variables and constants
        return var

    new_inputs = [clone_graph(input, clone_dict) for input in var.owner.inputs]
    new_outputs = [out.type() for out in var.owner.outputs]
    new_apply = Apply(var.owner.op, new_inputs, new_outputs)
    for new_output, old_output in zip(new_outputs, var.owner.outputs):
        clone_dict[old_output] = new_output
    return new_outputs[var.owner.outputs.index(var)]

new_out = clone_graph(out)


# In[27]:


new_out = clone_graph(out)
new_out.dprint()
new_out is out, new_out.owner.inputs[0] is out.owner.inputs[0]


# In[28]:


def compute_clients(var):
    clients = {var: []}
    queue = [var.owner]
    while queue:
        apply = queue.pop(0)
        if apply is None:
            continue
        queue.extend([inp.owner for inp in apply.inputs])

        for idx, input in enumerate(apply.inputs):
            if input not in clients:
                clients[input] = {(idx, apply)}
            else:
                clients[input].add((idx, apply))
    return clients


# In[29]:


out.name = "Sum(x + x)"
out.owner.inputs[0].name = "x + x"
compute_clients(out)


# In[30]:


def local_add_to_mul(apply: Apply) -> list[Variable] | None:
    """x + x -> x * 2"""
    if not isinstance(apply.op, Add):
        return None

    x, y = apply.inputs
    if x is y:
        return [mul(x, Constant(np.array(2.0), type=scalar))]

def local_factor_sum_mul(apply: Apply) -> list[Variable] | None:
    """sum(x * a) -> sum(x) * a, when a is a scalar."""
    if not isinstance(apply.op, Sum):
        return None

    sum_input = apply.inputs[0]

    if not (sum_input.owner is not None and isinstance(sum_input.owner.op, Mul)):
        return None

    mul_input, mul_factor = sum_input.owner.inputs

    # Check the second input is a scalar
    if mul_factor.type.shape != ():
        return None

    new_sum = apply.op(mul_input)
    new_mul = mul(new_sum, mul_factor)
    return [new_mul]


def graph_rewrite(node_rewrites, var):
    clients = compute_clients(var)
    queue = [var.owner]
    while queue:
        apply = queue.pop(0)
        if apply is None:
            continue

        queue.extend([inp.owner for inp in apply.inputs])

        for node_rewrite in node_rewrites:
            replacements = node_rewrite(apply)
            if replacements is None:
                continue
            else:
                for old_out, new_out in zip(apply.outputs, replacements):
                    if old_out is var:
                        # The output variable was itself replaced, reference new one from now on
                        var = new_out
                    else:
                        # Update any references to the old variable by the replacement
                        for inp_idx, client in clients[old_out]:
                            client.inputs[inp_idx] = new_out
                # Try to apply rewrites in new var
                return graph_rewrite(node_rewrites, var)
    return var


# In[31]:


new_out = clone_graph(out)
new_out.dprint()


# In[32]:


new_out = graph_rewrite([local_add_to_mul], new_out)


# In[33]:


new_out.dprint()


# In[34]:


new_out = clone_graph(out)
new_out = graph_rewrite([local_add_to_mul, local_factor_sum_mul], new_out)
new_out.dprint()


# In[35]:


# Confirm math holds up
new_out.eval({x: np.arange(15).reshape((3, 5))})


# In[35]:




