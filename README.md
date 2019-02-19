## matchlib

[![PyPI version](https://badge.fury.io/py/matchlib.svg)](https://badge.fury.io/py/matchlib)

This package provides a handy way to partially compare python data structures 
(typically nested lists/dictionaries).

### Installation
```bash
pip install matchlib
```
### Usage
```python
from matchlib import matches

user = {
    'id': 42,
    'name': 'John Doe',
    'email': 'johndoe@gmail.com',
    'posts': [
        {
            'id': 1,
            'text': 'some text'
        },
        {
            'id': 2,
            'text': 'lorem ipsum',
            'comments': [42, 142, 242]
        }
    ]
}

assert matches(
    user,
    {
        'id': ...,
        'name': 'John Doe',
        'email': 'johndoe@gmail.com',
        ...: ...
    }
)
```
Same can be achieved using standard `==` operator with `matchlib.Partial` object:
```python
from matchlib import Partial

assert user == Partial({
    'id': 42,
    'email': 'johndoe@gmail.com',
    ...: ...
})
```
The `...` "wildcard" could be placed at any nested level. 
Let's say we only need to check that comment `142` is present in specific post: 
```python 
assert user == Partial({
    'posts': [
        ...,
        {
            'id': 2,
            'comments': [..., 142, ...],
            ...: ...
        }
    ],
    ...: ...
})
``` 
Matching rules are simple:
 - In __lists__ and __tuples__ `...` matches zero or more elements and order is preserved:
    ```python
    Partial([1, 2, ...]) == [1, 2, 3, 4]
    Partial([1, 2, ...]) == [1, 2]
    
    Partial([1, 2, ...]) != [0, 1, 2]
    Partial([1, 2, ...]) != [2, 1]
    ```
 - Same for the __sets__ except they are unordered:
    ```python
    Partial({1, 2, ...}) == {1, 2}
    Partial({1, 2, ...}) == {0, 1, 2, 3}
 
    Partial({1, 2, ...}) != {0, 1, 3}
    ```
 - As __dict value__ `...` matches any object:
    ```python
    Partial({'a': 1, 'b': ...}) == {'a': 1, 'b': 2}
    ```
 - As __dict key__ `...` matches any key if assosiated values match:
    ```python
    Partial({'a': 1, ...: 2}) == {'a': 2, 'b': 2}
    ``` 
 - When passed as __both key and value__ matches zero or more arbitrary key-value pairs:
    ```python
    Partial({'a': 1, ...: ...}) == {'a': 1, 'b': 2, 'c': 3}
    ```

### Some more hacks
`mathchlib` provides a `Regex` object that allows to match an arbitrary string element 
(except if it is a dict key) against a regular expression.
Also `pytest.approx` is supported for floating-point numbers comparison:
```python
from pytest import approx
from matchlib import Regex, Partial

account = {
    'id': 1,
    'balance': 1007.62,
    'owner': {
        'email': 'user42@domain.com',
    }
}

assert account == Partial({
    'id': ...,
    'balance': approx(1000, 0.1),
    'owner': {
        'email': Regex(r'\w+@domain\.com')
    }
})
```
If for any reason you dislike Ellipsis literal (`...`) 
a `matchlib.Any` object can be used interchangeably.