class Meta(type):
    @classmethod
    def __prepare__(metaclass, name, parents, **kwargs):
        """
        Gets kwargs in class(object, **kwargs) & returns dict for __new__
        """
        print("__prepare__(")
        print("        metaclass={},".format(metaclass))
        print("        name={},".format(name))
        print("        parents={},".format(parents))
        print("        **kwargs={},".format(kwargs))
        print(")")
        # if kwargs.get("prepare") is None:
        #     print("__prepare__: kwargs.get('foo') was None!")
        #     print("__prepare__: kwargs['foo'] = 'prepare'")
        #     kwargs['foo'] = 'prepare'
        # else:
        #     print("__prepare__: kwargs['foo'] = ", kwargs['foo'])
        return dict(kwargs)

    def __new__(metaclass, name, parents, namespace_dict, **kwargs):
        """
        Allows editing before Class is constructed.

        Items in namespace_dict become attributes/methods of created Class
        """
        print("__new__(")
        print("        metaclass={},".format(metaclass))
        print("        name={},".format(name))
        print("        parents={},".format(parents))
        print("        namespace_dict={},".format(namespace_dict))
        print("        **kwargs={},".format(kwargs))
        print(")")
        # if namespace_dict.get("foo") is None:
        #     print("__new__: namespace_dict.get('foo') was None!")
        #     print("__new__: namespace_dict['foo'] = 'new'")
        #     namespace_dict['foo'] = 'new'
        # else:
        #     print("__new__: namespace_dict.get('foo') = ", namespace_dict['foo'])
        return super().__new__(metaclass, name, parents, namespace_dict)

    def __init__(cls, name, parents, namespace_dict, **kwargs):
        """
        Allows editing after Class is constructed.

        Does not run for subclasses of constructed Class.
        """
        print("__init__(")
        print("        cls={},".format(cls))
        print("        name={},".format(name))
        print("        parents={},".format(parents))
        print("        namespace_dict={},".format(namespace_dict))
        print("        **kwargs={},".format(kwargs))
        print(")")
        # if hasattr(cls, "foo") is False:
        #     print("__init__: hasattr(cls, 'foo') is False!")
        #     print("__init__: cls.foo = 'init'")
        #     cls.foo = "init"
        # else:
        #     print("__init__: getattr(cls, 'foo') = ", cls.foo)
        super().__init__(name, parents, namespace_dict)

    def __call__(cls, *args, **kwargs):
        """
        Constructs instance of Cls
        """
        print("__call__(")
        print("        cls={},".format(cls))
        print("        *args={},".format(args))
        print("        **kwargs={},".format(kwargs))
        print(")")
        return super().__call__(*args, **kwargs)

if __name__ == "__main__":
    print()
    print("class X(object, metaclass=Meta):")
    print("    pass")
    print("----------------------------------------------------")
    class X(object, metaclass=Meta):
        pass
    print("hasattr(X, 'foo') = ", hasattr(X, 'foo'))
    print()
    print()

    print("class Y(object, metaclass=Meta, foo='bar'):")
    print("    pass")
    print("----------------------------------------------------")
    class Y(object, metaclass=Meta, foo="bar"):
        pass
    print("Y.foo = ", Y.foo)
    print()
    print()

    print("class Z(object, metaclass=Meta):")
    print("    foo = 'baz'")
    print("----------------------------------------------------")
    class Z(object, metaclass=Meta):
        foo = "baz"
    print("Z.foo = ", Z.foo)
    print()
    print()

    print("class A(object, metaclass=Meta, foo='bet'):")
    print("    foo = 'bay'")
    print("----------------------------------------------------")
    class A(object, metaclass=Meta, foo="bet"):
        foo = 'bay'
    print("A.foo = ", A.foo)
    print()
    print()

    print("class B(object, metaclass=Meta, foo='blo'):")
    print("    foo = 'bru")
    print("----------------------------------------------------")
    class A(object, metaclass=Meta, foo="blo"):
        foo = 'bru'
        def __init__(self, foo):
            self.foo = foo
    print("A.foo = ", A.foo)
    print("a = A('bux')")
    a = A(foo='bux')
    print("a.foo = ", a.foo)
    print()
   
