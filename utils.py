#encoding: utf-8
import torch
from termcolor import cprint, colored as c


def num_flat_features(x):
    size = x.size()[1:]  # all dimensions except the batch dimension
    num_features = 1
    for s in size:
        num_features *= s
    return num_features

# might be uselesss -------------------------

def forward_tracer(self, input, output):
    cprint(c("--> " + self.__class__.__name__, 'red') + " ===forward==> ")
    # print('')
    # print('input: ', type(input))
    # print('input[0]: ', type(input[0]))
    # print('output: ', type(output))
    # print('')
    # print('input size:', input[0].size())
    # print('output size:', output.data.size())
    # print('output norm:', output.data.norm())


def backward_tracer(self, input, output):
    cprint(c("--> " + self.__class__.__name__, 'red') + " ===backward==> ")


CHARS = "\x00 ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz01234567890.,;:?\"'\n\r\t~!@#$%^&*()-/–—=_+<>{}[]|\\`~\xa0ëµ£"
CHAR_DICT = {ch: i for i, ch in enumerate(CHARS)}


class Char2Vec():
    def __init__(self, size=None, chars=None, add_unknown=False):
        if chars is None:
            self.chars = CHARS
        else:
            self.chars = chars
        # create dictionary of characters using the index 
        self.char_dict = {ch: i for i, ch in enumerate(self.chars)}
        if size:
            self.size = size
        else:
            self.size = len(self.chars)
        if add_unknown:
            self.allow_unknown = True
            self.size += 1
            self.char_dict['<unk>'] = self.size - 1
        else:
            self.allow_unknown = False

    def get_ind(self, char):
        try:
            return self.char_dict[char]
        except KeyError:
            if self.allow_unknown is False:
                raise KeyError('character is not in dictionary: ' + str([char]))
            return self.char_dict['<unk>']

    def one_hot(self, source):
        y = torch.LongTensor([[self.get_ind(char)] for char in source])

        y_onehot = torch.zeros(len(source), self.size)
        y_onehot.scatter_(1, y, 1)

        return y_onehot

    def one_hot_batch(self, sources):
        """
        source: (seq_length * batch_n)
        output: (seq_length * batch_n * input_width)
        """
        source_shape = [len(sources), len(sources[0])]
        y = torch.LongTensor([[[self.get_ind(char)] for char in src] for src in sources])
        y_onehot = torch.zeros(len(sources), len(sources[0]), self.size)
        y_onehot.scatter_(2, y, 1)

        return y_onehot

    def char_code(self, source):
        return torch.LongTensor([self.char_dict[char] for char in source])

    def char_code_batch(self, batch):
        return torch.LongTensor([[self.char_dict[char] for char in seq] for seq in batch])

    def vec2list(self, vec):
        chars = [self.chars[ind] for ind in vec.cpu().data.numpy()]
        return chars

    def vec2list_batch(self, vec):
        chars = [[self.chars[ind] for ind in row] for row in vec.cpu().data.numpy()]
        return chars


def flatten(l):
    return [item for sublist in l for item in sublist]

