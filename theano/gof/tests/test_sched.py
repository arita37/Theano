from theano.gof.sched import (dependence, sort_apply_nodes, reverse_dict,
        _toposort, posort)

import theano
from theano import tensor
from theano.gof.graph import io_toposort

def test_dependence():
    x = tensor.matrix('x')
    y = tensor.dot(x*2, x+1)
    nodes = io_toposort([x], [y])

    for a, b in zip(nodes[:-1], nodes[1:]):
        assert dependence(a, b) <= 0

def test_sort_apply_nodes():
    x = tensor.matrix('x')
    y = tensor.dot(x*2, x+1)
    str_cmp = lambda a, b: cmp(str(a), str(b)) # lexicographical sort
    nodes = sort_apply_nodes([x], [y], cmps=[str_cmp])

    for a, b in zip(nodes[:-1], nodes[1:]):
        assert str(a) <= str(b)
def test_reverse_dict():
    d = {'a': (1, 2), 'b': (2, 3), 'c':()}
    assert reverse_dict(d) ==  {1: ('a',), 2: ('a', 'b'), 3: ('b',)}

def test__toposort():
    edges = {1: {4, 6, 7}, 2: {4, 6, 7}, 3: {5, 7}, 4: {6, 7}, 5: {7}}
    order = _toposort(edges)
    assert not any(a in edges.get(b, ()) for i, a in enumerate(order)
                                         for b    in order[i:])

def test_posort_easy():
    nodes = "asdfghjkl"
    cmp = lambda a,b: -1 if a<b else 1 if a>b else 0
    assert posort(nodes, cmp) == list("adfghjkls")

def test_posort():
    l = range(1,20)
    cmps = [lambda a,b: a%10 - b%10, lambda a, b: (a/10)%2 - (b/10)%2,
            lambda a,b: a-b]
    assert posort(l, *cmps) == \
            [10, 1, 11, 2, 12, 3, 13, 4, 14, 5, 15, 6, 16, 7, 17, 8, 18, 9, 19]
