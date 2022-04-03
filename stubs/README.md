TODO

1. Consider relying on pybind's implicit conversion and loosen the parameter types
    1. What about return type?
    2. i.e. use `ArrayLike` as parameter type and then pybind will convert it to `ndarry`
2. Consider specifying 1d ndarray type instead of NDArray which has `Any` for shape
3. Check `int` values to see if they are `np` types