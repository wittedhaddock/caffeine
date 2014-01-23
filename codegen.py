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

    def functionDefinition(self, name, annotation):
        print(name, annotation, "fd")

    def emitSchema(self, name, schema):
        for name, annotation in schema.functions.items():
            print(self.functionDefinition(name, annotation))

    def generate(self):
        for name, schema in self.schemas.items():
            self.emitSchema(name, schema)


def codegen(args):
    import worker
    client = worker.RPCClient(URL=args.url)
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
