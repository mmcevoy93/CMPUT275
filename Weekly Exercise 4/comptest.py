import sys
import traceback

"""
Interactive and doctest program for the expression compiler.

Run the interactive version with
    python3 comptest.py
and the doctests with
    python3 comptest.py --test
"""

from exprparser import ExprParser
from compiler import Compiler

# Debugging and comprehension settings
debug = False

def main():

    comp = Compiler()

    comp.debug = True

    # Ask for an expression until get EOF or blank line.
    # Note use of next, instead for s in sys.stdin:

    # These store the global and local context 
    # under which we test our compiled code.
    globals = {}
    locals = {}

    while True:
        print("?", end='', flush=True)
        # return empty string on EOF
        s = next(sys.stdin, "")
        s = s.strip()
        if s == "": 
            # Quit on blank line or EOF
            break

        result = None
        compiled_code = []

        # Compilation should not raise any exceptions normally.
        error = comp.compile(s, compiled_code)
        if error:
            print("Compilation Error: {}".format(error))
            continue

        if len(compiled_code) == 0:
            print("No code generated!")
            continue

        if debug:
            print("Compiled code:", compiled_code)

        # We need to modify the code to print the value of the expression
        # which is in _result
        # expression
        compiled_code.append("print(_result)")

        program = "\n".join(compiled_code)
        print()
        print(program)

        print("\nRunning program ...")

        # locals preserves the previous computed values of variables,
        # so our programs are effectively chained together.
        print("locals before", sorted(locals.items()))

        # We can test the program by running it under Python.   
        # During the compile phase we can get SyntaxError exceptions, 
        # and so indicate the line of the program it occurs at.
        # During execution, we can get almost anything,
        # so capture the exception and provide a traceback.
        try:
            exec(program, globals, locals)

        except SyntaxError as e:
            print("Exec compile-time error: {}".format(e))
            lnum = e.lineno
            if lnum is not None:
                # line numbers are 1 greater than code indexes
                lnum -= 1
                print("at code pos {}, '{}'".
                    format(lnum, compiled_code[lnum]))
            
        except Exception as e:
            print("Exec run-time error: {}".format(e))
            error_class = e.__class__.__name__
            detail = e.args[0]
            print(detail)
            cl, exc, tb = sys.exc_info()

            lnum = traceback.extract_tb(tb)[-1][1]
            if lnum is not None:
                # line numbers are 1 greater than code indexes
                lnum -= 1
                print("at code pos {}, '{}'".
                    format(lnum, compiled_code[lnum]))

        print("locals after", sorted(locals.items()))
        print()

        # Back for more

    print("Done")

def tests():
    """
    Doctests - not even remotely complete.
    
    >>> comp = Compiler()
    >>> code = []
    >>> s = "1"
    >>> error = comp.compile(s, code)
    >>> (error, code)
    (None, ['# code for:', '# 1', '_result = 1'])

    >>> code = []
    >>> s = "-1"
    >>> error = comp.compile(s, code)
    >>> (error, code)
    (None, ['# code for:', '# -1', '_result = (-1)'])

    >>> code = []
    >>> s = "sqr(2)"
    >>> error = comp.compile(s, code)
    >>> (error, code)
    (None, ['# code for:', '# sqr(2)', '_result = (2 ** 2)'])

    >>> code = []
    >>> s = "1 / 0"
    >>> error = comp.compile(s, code)
    >>> (error, code)
    (None, ['# code for:', '# 1 / 0', '_result = (1 / 0)'])

    >>> code = []
    >>> s = "(x = 1) + (x = x + 2) + (x = x + 42)"
    >>> error = comp.compile(s, code)
    >>> (error, code)
    (None, ['# code for:', '# (x = 1) + (x = x + 2) + (x = x + 42)', '_x_1 = 1', '_x_2 = (_x_1 + 2)', '_x_3 = (_x_2 + 42)', '_result = ((_x_1 + _x_2) + _x_3)', '# Update and cleanup x', 'x = _x_3', 'del(_x_1)', 'del(_x_2)', 'del(_x_3)'])

    >>> code = []
    >>> s = "x + - + 1"
    >>> error = comp.compile(s, code)
    >>> (error, code)
    ("Parsing generated errors:\\nSyntax error at '+'", [])

        Examples:
            1 + 2
            y = x + 1
            (x = 2) + 1
            (x = 1) + (y = x + 1)
            x=1 + (y=2) + (z=x)
            (x=1) + (y=2) + (z=x)
            (x=1) + (y=2) + (x=y+3)
            ((x0 + y0) + x1)
            y + y = 1
            (x = (x = ( x = (x = 42))))

    """
    pass

def _test():
    import doctest
    global debug
    debug = False
    doctest.testmod()

if __name__ == "__main__":
    """
    Run doctests if the --test argument is in command line arguments
    when run as a main program. Otherwise, run as a normal program.
    """

    import sys
    if "--test" in sys.argv:
        print("Running doctests")
        _test()
        exit()

    # Start the compiler
    main()

