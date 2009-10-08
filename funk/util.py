def arguments_str(args, kwargs):
    args_str = map(str, args)
    args_str += ['%s=%s' % (key, kwargs[key]) for key in kwargs]
    return ', '.join(args_str)

def function_call_str(name, args, kwargs):
    return "%s(%s)" % (name, arguments_str(args, kwargs))

def method_call_str(object_name, method_name, args, kwargs):
    return "%s.%s" % (object_name, function_call_str(method_name, args, kwargs))
