def arguments_str(args, kwargs, separator=", "):
    args_str = [str(arg) for arg in args] + \
        ['%s=%s' % (key, kwargs[key]) for key in kwargs]
    return separator.join(args_str)

def function_call_str(name, args, kwargs):
    return "%s(%s)" % (name, arguments_str(args, kwargs))

def method_call_str(object_name, method_name, args, kwargs):
    return "%s.%s" % (object_name, function_call_str(method_name, args, kwargs))

def function_call_str_multiple_lines(name, args, kwargs):
    return "%s(%s)" % (name, arguments_str(args, kwargs, ",\n" + " " * (len(name) + 1)))
    
