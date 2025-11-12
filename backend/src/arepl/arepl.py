from arepl_dump import dump  # type: ignore  # noqa: F401

import pathlib

path = pathlib.Path("/home/user/to/some/folder/toto.out")
qwe = path.suffix
asd = str(path.parent / (path.stem + "other_file" + path.suffix))
