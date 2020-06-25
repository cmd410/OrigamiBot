from inspect import signature, BoundArguments
from typing import Optional


def check_args(method, args) -> Optional[BoundArguments]:
    """Checks if arguments are suitable for given method.

    Returns BoundArguments, or None on failure.
    """
    try:
        bound_args = signature(method).bind(*args)
        bound_args.apply_defaults()
        for name, param in bound_args.signature.parameters.items():
            p_type = param.annotation
            if p_type == param.empty:   # No conversion needed
                continue

            arg = bound_args.arguments[name]
            if type(arg) == p_type:   # No conversion needed
                continue

            # read boolean
            if issubclass(p_type, bool):
                if arg in {'True', 'true', '1'}:
                    bound_args.arguments[name] = p_type(True)
                    continue
                elif arg in {'Fasle', 'false', '0'}:
                    bound_args.arguments[name] = p_type(False)
                    continue
                else:
                    return None

            # Generic param conversion attempt
            bound_args.arguments[name] = p_type(bound_args.arguments[name])
        return bound_args
    except (TypeError, ValueError):
        return None
