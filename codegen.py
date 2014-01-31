#!python3
#This module generates code.
import argparse
parser = argparse.ArgumentParser(description="Generate code")
parser.add_argument("--language", choices=[
                    "objc"], help="The language to generate", required=True)
parser.add_argument("-o", "--output", help="Output directory", default=".")
parser.add_argument("--url", help="URL for the schema", required=True)


class ObjCCodeGen:
"""A code generator for the ObjC language."""


    def __init__(self, schemas, args):
        self.schemas = schemas
        self.args = args

    def objc_type(self,pythonType):
        """Look up the type of the pythonType to get an equivalent ObjC type"""
        print ('type',pythonType)
        typemap = {None:"void",str:"NSString*"}
        if pythonType in typemap:
            return typemap[pythonType]
        return pythonType.__name__

    def function_definition(self, name, annotation):
        """Figure out the function definition for the given name and annotation"""
        print(name, annotation, "fd")
        definition = ""
        #so okay, first, we emit either + or -.  At some future point we should support -, but today we only support +.
        definition += "+ "
        #next, we figure out the return type
        definition += "(%s)" % self.objc_type(annotation["return"])
        #and the method name
        definition += name

        if len(annotation)==1:
            return definition

        #append With
        definition += "With"
        wantsCap = True

        for argname in sorted(annotation.keys()):
            if argname=="return": continue
            if wantsCap:
                selectorVersion = argname[0].upper() + argname[1:]
                wantsCap = False
            else:
                selectorVersion = argname

            tipe = annotation[argname]
            objcType = self.objc_type(tipe)

            definition += selectorVersion + ":(%s)" % objcType + argname + " "

        return definition


    def emit_schema(self, name, schema):
        """Emit code for the entire schema"""
        for name, annotation in schema.functions.items():
            print(self.function_definition(name, annotation))

    def generate(self):
        """Run the generator and emit all code"""
        for name, schema in self.schemas.items():
            self.emit_schema(name, schema)


def codegen(args):
    """main function"""
    import worker
    client = worker.RPCClient(url=args.url)
    schemas = client.CaffeineService.directory()
    codegen = None
    if args.language == "objc":
        codegen = ObjCCodeGen(schemas, args)
    else:
        raise NotImplementedError("Language not implemented")

    codegen.generate()

if __name__ == "__main__":
    args = parser.parse_args()
    codegen(args)
