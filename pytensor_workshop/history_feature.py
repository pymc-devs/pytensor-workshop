from pytensor import config
from pytensor.graph.features import Feature, LambdaExtract

class FullHistory(Feature):
    """Keeps track of all changes in FunctionGraph and allows arbitrary back and forth through intermediate states"""

    def __init__(self):
        self.fw = []
        self.bw = []
        self.pointer = -1
        self.fg = None

    def on_attach(self, fgraph):
        if self.fg is not None:
            raise ValueError("Full History already attached to another fgraph")
        self.fg = fgraph

    def on_change_input(self, fgraph, node, i, r, new_r, reason=None):
        self.bw.append(LambdaExtract(fgraph, node, i, r, reason))
        self.fw.append(LambdaExtract(fgraph, node, i, new_r, reason))
        self.pointer += 1

    def goto(self, checkpoint):
        """
        Reverts the graph to whatever it was at the provided
        checkpoint (undoes all replacements). A checkpoint at any
        given time can be obtained using self.checkpoint().

        """
        history_len = len(self.bw)
        pointer = self.pointer
        assert 0 <= checkpoint <= history_len
        verbose = config.optimizer_verbose

        # Go backwards
        while pointer > checkpoint - 1:
            reverse_fn = self.bw[pointer]
            if verbose:
                print(reverse_fn.reason)
            reverse_fn()
            pointer -= 1

        # Go forward
        while pointer < checkpoint - 1:
            pointer += 1
            forward_fn = self.fw[pointer]
            if verbose:
                print(forward_fn.reason)
            forward_fn()

        # Remove history changes caused by the foward/backward!
        self.bw = self.bw[:history_len]
        self.fw = self.fw[:history_len]
        self.pointer = pointer
        return self.fg

    def start(self):
        return self.goto(0)

    def end(self):
        return self.goto(len(self.bw))

    def prev(self):
        if self.pointer < 0:
            return self.fg
        else:
            return self.goto(self.pointer)

    def next(self):
        if self.pointer >= len(self.bw) - 1:
            return self.fg
        else:
            return self.goto(self.pointer + 2)