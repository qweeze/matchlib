from matchlib import matches, Partial, Regex, Any


def test_simple():
    assert matches([], [])
    assert matches({}, {})
    assert matches(None, None)
    assert matches(False, False)
    assert matches(True, True)
    assert matches(42, 42)
    assert matches('abc', 'abc')

    assert matches([1, 2, 3], [1, 2, 3])
    assert matches({'a': 1, 'b': 2}, {'a': 1, 'b': 2})

    assert matches({'a': 1, 'b': 2}, {...: ...})
    assert matches({'a': 1, 'b': 2}, {'a': 1, 'b': ...})
    assert matches({'a': 1, 'b': 2}, {'a': 1, ...: ...})
    assert matches({'a': 1, 'b': 2, 'c': 3}, {'a': 1, ...: ...})
    assert matches({'a': 1, 'b': 2, 'c': 3}, {'a': 1, 'c': 3, ...: ...})
    assert matches({'a': 1, 'b': 2, 'c': 3}, {'a': ..., 'c': 3, ...: ...})

    assert matches([1, 2, 3], [..., 2, 3])
    assert matches([1, 2, 3], [1, 2, ...])
    assert matches([1, 2, 3], [1, ..., 3])

    assert matches([1, 2, 3], [Any, 2, 3])
    assert matches([1, 2, 3], [1, 2, Any])
    assert matches([1, 2, 3], [1, Any, 3])

    assert matches([1, 2, 3, 4, 5], [1, ..., 5])
    assert matches([1, 2, 3, 4, 5], [1, 2, ..., 4, 5])
    assert matches([1, 2, 3, 4, 5], [1, 2, 3, ..., 4, 5])


def test_simple_negative():
    assert not matches([], [42])
    assert not matches([42], [])
    assert not matches({'a': 1}, {})
    assert not matches({}, {'a': 1})
    assert not matches(None, 42)
    assert not matches(42, None)
    assert not matches(False, True)
    assert not matches(True, False)
    assert not matches(42, 43)
    assert not matches('abc', 'abcd')

    assert not matches([1, 2, 3], [1, 2, 3, 4])
    assert not matches([1, 2, 3, 4], [1, 2, 3])
    assert not matches({'a': 1, 'b': 2}, {'a': 1, 'b': 42})
    assert not matches({'a': 1, 'c': 2}, {'a': 1, 'b': 2})
    assert not matches({'a': 1, 'b': 42}, {'a': 1, 'b': 2})

    assert not matches({'a': 1, 'b': 2}, {'a': 1, 'c': ...})
    assert not matches({'a': 1, 'b': 2}, {'a': 2, ...: ...})
    assert not matches({'a': 2, 'b': 2}, {'a': 1, ...: ...})
    assert not matches({'a': 1, 'b': 2, 'c': 3}, {'a': 1, ...: ..., 'c': 4})
    assert not matches({'a': 1, 'b': 2, 'c': 4}, {'a': 1, 'c': 3, ...: ...})
    assert not matches({'a': 1, 'b': 2, 'c': 3}, {'a': ..., 'c': 4, ...: ...})

    assert not matches([1, 2, 3], [..., 2, 3, 4])
    assert not matches([1, 2, 3], [..., 2, 4, 3])
    assert not matches([1, 2, 3], [0, 1, 2, ...])
    assert not matches([1, 2, 3], [1, 3, 2, ...])
    assert not matches([1, 2, 3], [1, 2, ..., 4])
    assert not matches([1, 2, 3], [2, ..., 3])
    assert not matches([1, 2, 3], [1, ..., 4])
    assert not matches([1, 2, 3], [1, ..., 3, 4])
    assert not matches([1, 2, 3], [0, 1, ..., 3])
    assert not matches([1, 2, 4], [1, ..., 3])
    assert not matches([0, 2, 3], [1, ..., 3])

    assert not matches([1, 2, 3, 4, 5], [1, ..., 6])
    assert not matches([1, 2, 3, 4, 5], [1, ..., 5, 6])
    assert not matches([1, 2, 3, 4, 5], [1, 2, 4, ..., 4, 5])
    assert not matches([1, 2, 3, 4, 5], [1, 2, 4, ..., 5])
    assert not matches([1, 2, 3, 4, 5], [1, 2, 3, 4, ..., 4, 5])
    assert not matches([1, 2, 3, 4, 5], [1, 2, 3, ..., 4, 4, 5])


def test_multiple():
    assert matches([1, 3, 5], [..., ..., ..., 5])
    assert not matches([1, 3, 5], [..., ..., ..., 4])

    assert matches([1, 3, 5], [..., 3, ...])
    assert not matches([1, 3, 5], [..., 4, ...])

    assert matches([1, 2, 3, 4, 5], [..., 2, 3, 4, ...])
    assert not matches([1, 2, 3, 4, 5], [..., 2, 4, ...])

    assert matches([1, 3, 5], [..., ..., 3, ..., ...])
    assert not matches([1, 3, 5], [..., ..., 4, ..., ...])

    assert matches([1, 3, 5], [1, 3, ..., ...])
    assert not matches([1, 2, 5], [1, 3, ..., ...])

    assert matches([0, 1, 2, 4, 5, 6, 7, 8, 9], [0, 1, ..., 5, 6, 7, ..., 9])
    assert matches([0, 1, 2, 4, 5, 6, 7, 8, 9], [0, 1, ..., 5, 6, 7, ...])
    assert matches([0, 1, 2, 4, 5, 6, 7, 8, 9], [..., 5, 6, 7, ..., 9])
    assert not matches([0, 1, 2, 4, 5, 6, 7, 8, 9], [0, 1, ..., 5, 7, ..., 9])
    assert not matches([0, 1, 2, 4, 5, 6, 7, 8, 9], [0, 1, ..., 5, 7, ..., 8])


def test_nested():

    obj = {
        'id': 42,
        'name': 'John Doe',
        'email': 'john@gmail.com',
        'posts': [
            {
                'id': 1,
                'text': 'some text',
            },
            {
                'id': 13,
                'text': 'Lorem Ipsum...',
                'likes': [42, 142, 242],
            }
        ]

    }

    assert matches(
        obj,
        {
            'name': 'John Doe',
            'posts': [...],
            ...: ...
        },
    )

    assert obj == Partial({
        'name': 'John Doe',
        'posts': [...],
        ...: ...
    })

    assert obj == Partial({
        'name': 'John Doe',
        'posts': [
            ...,
            {
                ...: ...,
                'likes': [..., 142, ...]
            },
            ...
        ],
        ...: ...
    })

    assert obj == Partial({
        'id': ...,
        'name': 'John Doe',
        'email': Regex(r'\w+@gmail.com'),
        'posts': [...],
    })

    assert obj == Partial({
        'id': ...,
        'name': 'John Doe',
        'email': Regex(r'\w+@gmail.com'),
        'posts': [
            {
                'id': ...,
                'text': 'some text',
            },
            ...
        ],
    })

    assert obj == Partial({
        'id': 42,
        ...: ...,
        'posts': [
            {
                'id': 1,
                ...: ...
            },
            {
                'text': Regex(r'Lorem \w+'),
                ...: ...
            }
        ],
    })

    assert [obj] == Partial([{
        'name': 'John Doe',
        'posts': [...],
        ...: ...
    }])

    assert [obj, {}] == Partial([
        {
            'name': 'John Doe',
            'posts': [...],
            ...: ...
        },
        ...
    ])


def test_nested_negative():

    obj = {
        'id': 42,
        'name': 'John Doe',
        'email': 'john@gmail.com',
        'posts': [
            {
                'id': 1,
                'text': 'some text',
            },
            {
                'id': 13,
                'text': 'Lorem Ipsum...',
                'likes': [42, 142, 242],
            }
        ]

    }

    assert obj != Partial({
        'id': ...,
        'name': 'John Doe',
        'email': Regex(r'\w+@gmail.com'),
        'posts': [
            {
                'id': ...,
                'text': 'some text',
            },
        ],
    })

    assert obj != Partial({
        'email': Regex(r'\w+@gmail.com'),
        'posts': {...: ...},
    })

    assert obj != Partial({
        'email': Regex(r'mail.org'),
        ...: ...
    })

    assert obj != Partial({
        'name': 'John Doe',
        'posts': [
            {
                ...: ...,
                'likes': [..., 142, ...]
            },
        ],
        ...: ...
    })

    assert obj != Partial({
        'name': 'John Doe',
        'posts': [
            ...,
            {
                ...: ...,
                'likes': [..., 142, ...]
            },
            ...
        ],
    })

    assert obj != Partial({
        'name': 'John Doe',
        'posts': [
            ...,
            {
                ...: ...,
                'likes': [142, ...]
            },
            ...
        ],
        ...: ...
    })

    assert [obj, {}] != Partial([{
        'name': 'John Doe',
        'posts': [...],
        ...: ...
    }])

    assert [obj] != Partial([
        {
            'name': 'John Doe',
            'posts': [...],
            ...: ...
        },
        {}
    ])


def test_sets():
    assert matches(set(), set())
    assert matches({1, 2, 3}, {1, ..., 3})
    assert matches({1, 2, 3}, {1, ...})
    assert matches({1, 2, 3}, {...})

    assert not matches({1, 2, 3}, set())
    assert not matches({1, 2, 3}, {0, 1, 2, ...})


def test_dict_values():
    obj = {
        'id': 42,
        'name': 'John Doe',
        'email': 'john@gmail.com',
    }

    assert obj == Partial({
        ...: 42,
        'name': 'John Doe',
        'email': 'john@gmail.com',
    })

    assert obj == Partial({
        'id': 42,
        'name': 'John Doe',
        ...: 'john@gmail.com',
    })

    assert obj != Partial({
        'id': 42,
        ...: 'john@gmail.com',
    })

    assert obj != Partial({
        'id': 42,
        'name': 'John Doe',
        'posts': [1, 2, 3],
        ...: 'john@gmail.com',
    })

    assert obj == Partial({
        'id': 42,
        'name': ...,
        ...: 'john@gmail.com',
    })

    assert obj == Partial({
        'id': ...,
        'name': ...,
        'email': 'john@gmail.com',
    })
