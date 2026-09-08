"""Interpret a finite, pure Python subset; candidate code is never exec'd/imported."""
import ast
from pathlib import Path


class PolicyError(ValueError):
    pass


HISTORY_NAMES = {'own_history', 'opponent_history'}
ALLOWED = (ast.Module, ast.FunctionDef, ast.arguments, ast.arg, ast.If, ast.Return,
           ast.Expr, ast.Constant, ast.Name, ast.Load, ast.Subscript, ast.Slice,
           ast.UnaryOp, ast.Not, ast.USub, ast.BinOp, ast.Add, ast.Sub, ast.Mod,
           ast.Compare, ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
           ast.BoolOp, ast.And, ast.Or, ast.IfExp, ast.Call, ast.Attribute)


def load_policy(path):
    return parse_policy(Path(path).read_text(encoding='utf-8'))


def parse_policy(source):
    if len(source.encode()) > 16000:
        raise PolicyError('Source exceeds 16000 bytes')
    try:
        tree = ast.parse(source)
    except (SyntaxError, RecursionError) as exc:
        raise PolicyError(str(exc)) from exc
    nodes = list(ast.walk(tree))
    if len(nodes) > 400 or any(not isinstance(n, ALLOWED) for n in nodes):
        raise PolicyError('Unsupported syntax or more than 400 AST nodes')
    body = tree.body[:]
    if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant) and isinstance(body[0].value.value, str):
        body.pop(0)
    if len(body) != 1 or not isinstance(body[0], ast.FunctionDef):
        raise PolicyError('Provide exactly one function')
    fn = body[0]
    if (fn.name != 'policy' or [a.arg for a in fn.args.args] != ['own_history', 'opponent_history']
            or fn.args.posonlyargs or fn.args.kwonlyargs or fn.args.defaults or fn.args.kw_defaults
            or fn.args.vararg or fn.args.kwarg or fn.decorator_list or fn.returns
            or any(a.annotation for a in fn.args.args)):
        raise PolicyError('Required signature: policy(own_history, opponent_history)')
    for n in nodes:
        if isinstance(n, ast.FunctionDef) and n is not fn:
            raise PolicyError('Nested functions forbidden')
        if isinstance(n, ast.Name) and n.id not in HISTORY_NAMES | {'len', 'sum', 'min', 'max'}:
            raise PolicyError('Unknown name: ' + n.id)
        if isinstance(n, ast.Constant) and not (type(n.value) in (int, bool) and abs(n.value) <= 10000 or isinstance(n.value, str)):
            raise PolicyError('Unsupported constant')
        if isinstance(n, ast.Attribute) and n.attr != 'count':
            raise PolicyError('Only history.count is supported')
        if isinstance(n, ast.Call) and (n.keywords or len(n.args) != 1):
            raise PolicyError('Calls take exactly one positional argument')

    def expression(n, env):
        if isinstance(n, ast.Constant):
            if type(n.value) not in (int, bool):
                raise PolicyError('Strings allowed only in docstrings')
            return n.value
        if isinstance(n, ast.Name):
            if n.id not in env:
                raise PolicyError('Function names may only be called')
            return env[n.id]
        if isinstance(n, ast.Subscript):
            value = expression(n.value, env)
            if not isinstance(value, tuple):
                raise PolicyError('Only histories can be indexed')
            if isinstance(n.slice, ast.Slice):
                index = slice(*(expression(x, env) if x else None for x in (n.slice.lower, n.slice.upper, n.slice.step)))
            else:
                index = expression(n.slice, env)
            return value[index]
        if isinstance(n, ast.UnaryOp):
            value = expression(n.operand, env)
            if isinstance(n.op, ast.Not):
                return not value
            if type(value) is not int:
                raise PolicyError('Unary minus requires integer')
            return -value
        if isinstance(n, ast.BinOp):
            a, b = expression(n.left, env), expression(n.right, env)
            if type(a) is not int or type(b) is not int:
                raise PolicyError('Arithmetic requires integers')
            if isinstance(n.op, ast.Add):
                return a + b
            if isinstance(n.op, ast.Sub):
                return a - b
            return a % b
        if isinstance(n, ast.BoolOp):
            value = expression(n.values[0], env)
            for item in n.values[1:]:
                if isinstance(n.op, ast.And) and not value or isinstance(n.op, ast.Or) and value:
                    break
                value = expression(item, env)
            return value
        if isinstance(n, ast.Compare):
            left = expression(n.left, env)
            for op, item in zip(n.ops, n.comparators):
                right = expression(item, env)
                if isinstance(op, ast.Eq): result = left == right
                elif isinstance(op, ast.NotEq): result = left != right
                elif isinstance(op, ast.Lt): result = left < right
                elif isinstance(op, ast.LtE): result = left <= right
                elif isinstance(op, ast.Gt): result = left > right
                else: result = left >= right
                if not result:
                    return False
                left = right
            return True
        if isinstance(n, ast.IfExp):
            return expression(n.body if expression(n.test, env) else n.orelse, env)
        if isinstance(n, ast.Call):
            arg = expression(n.args[0], env)
            if isinstance(n.func, ast.Name) and n.func.id in {'len', 'sum', 'min', 'max'}:
                if not isinstance(arg, tuple):
                    raise PolicyError('Builtins take a history or slice')
                return {'len': len, 'sum': sum, 'min': min, 'max': max}[n.func.id](arg)
            if isinstance(n.func, ast.Attribute) and n.func.attr == 'count':
                sequence = expression(n.func.value, env)
                if not isinstance(sequence, tuple) or type(arg) is not int or arg not in (0, 1):
                    raise PolicyError('count expects a history and 0 or 1')
                return sequence.count(arg)
            raise PolicyError('Unsupported call')
        raise PolicyError('Unsupported expression')

    def statements(block, env):
        for n in block:
            if isinstance(n, ast.Return):
                return True, expression(n.value, env)
            if isinstance(n, ast.If):
                done, value = statements(n.body if expression(n.test, env) else n.orelse, env)
                if done:
                    return True, value
            elif isinstance(n, ast.Expr) and isinstance(n.value, ast.Constant) and isinstance(n.value.value, str):
                continue
            else:
                raise PolicyError('Only if and return statements are supported')
        return False, None

    def candidate(own_history, opponent_history):
        try:
            done, action = statements(fn.body, {'own_history': tuple(own_history), 'opponent_history': tuple(opponent_history)})
            if not done or type(action) is not int or action not in (0, 1):
                raise PolicyError('Action must be integer 0 or 1 (not bool)')
            return action
        except (IndexError, TypeError, ZeroDivisionError, ValueError, RecursionError) as exc:
            raise PolicyError(str(exc)) from exc
    candidate.source = source
    return candidate
