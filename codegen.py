#!python3
import argparse
parser = argparse.ArgumentParser(description="Generate code")
parser.add_argument("--language", choices=[
                    "objc"], help="The language to generate", required=True)
parser.add_argument("-o", "--output", help="Output directory", default=".")
parser.add_argument("--url", help="URL for the schema", required=True)


class ObjCCodeGen:



    def __init__(self, schemas, args):
        self.schemas = schemas
        self.args = args

    def objcType(self,pythonType):
        print ('type',pythonType)
        typemap = {None:"void",str:"NSString*"}
        if pythonType in typemap:
            return typemap[pythonType]
        return pythonType.__name__

    def functionDefinition(self, name, annotation):
        print(name, annotation, "fd")
        definition = ""
        #so okay, first, we emit either + or -.  At some future point we should support -, but today we only support +.
        definition += "+ "
        #next, we figure out the return type
        definition += "(%s)" % self.objcType(annotation["return"])
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
            objcType = self.objcType(tipe)

            definition += selectorVersion + ":(%s)" % objcType + argname + " "

        return definition


    def emitSchema(self, name, schema):
        for name, annotation in schema.functions.items():
            print(self.functionDefinition(name, annotation))

    def generate(self):
        for name, schema in self.schemas.items():
            self.emitSchema(name, schema)


def codegen(args):
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
