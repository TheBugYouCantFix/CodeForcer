from typing import TypeVar, Callable, Hashable

T = TypeVar("T")


class DependenciesContainer:
    """
    Key-value storage with generic type support for accessing shared dependencies
    """

    __slots__ = ()

    providers: dict[type, Callable[[], T] | T] = {}

    def __setitem__(self, key: type[T] | Hashable, provider: Callable[[], T] | T):
        self.providers[key] = provider

    def __getitem__(self, key: type[T] | Hashable):
        if key not in self.providers:
            if isinstance(key, type):
                # try by classname
                key = key.__name__

                if key not in self.providers:
                    raise KeyError(f"Provider for {key} is not registered")

            elif isinstance(key, str):
                # try by classname
                for cls_key in self.providers.keys():
                    if cls_key.__name__ == key:
                        key = cls_key
                        break
                else:
                    raise KeyError(f"Provider for {key} is not registered")

        provider = self.providers[key]

        if callable(provider):
            return provider()
        else:
            return provider
