#!python3
# This module generates code.
import argparse
parser = argparse.ArgumentParser(description="Generate code")
parser.add_argument("--language", choices=[
                    "objc"], help="The language to generate", required=True)
parser.add_argument("-o", "--output", help="Output directory", default=".")
parser.add_argument("--url", help="URL for the schema", required=True)


class OutException:
        pass


class ObjCCodeGen:

    """A code generator for the ObjC language."""

    def __init__(self, schemas, args):
        self.schemas = schemas
        self.args = args

    def underscore_case_to_camel_case(self, underscore_case):
        camelCase = ""
        next_capital = False
        for char in underscore_case:
            if char == "_":
                next_capital = True
                continue
            camelCase += char if not next_capital else char.upper()
            next_capital = False
        return camelCase

    def objc_type(self, pythonType):
        """Look up the type of the pythonType to get an equivalent ObjC type"""
        print('type', pythonType)
        typemap = {None: "void", str: "NSString*", OutException: "NSError**"}
        if pythonType in typemap:
            return typemap[pythonType]
        return pythonType.__name__

    def function_prototype(self, name, annotation):
        """Figure out the function prototype for the given name and annotation"""
        print(name, annotation, "fd")
        definition = ""
        # so okay, first, we emit either + or -.  At some future point we
        # should support -, but today we only support +.
        definition += "+ "
        # next, we figure out the return type
        definition += "(%s)" % self.objc_type(annotation["return"])
        # and the method name
        definition += self.underscore_case_to_camel_case(name)

        # append With
        definition += "With"
        wantsCap = True
        args = sorted(annotation.keys()) + ["error"]
        annotation = dict(annotation)  # copy
        annotation["error"] = OutException

        for argname in args:
            if argname == "return":
                continue
            if wantsCap:
                selectorVersion = argname[0].upper() + argname[1:]
                wantsCap = False
            else:
                selectorVersion = argname

            tipe = annotation[argname]
            objcType = self.objc_type(tipe)

            definition += selectorVersion + ":(%s)" % objcType + argname + " "
        return definition

    def function_implementation(self, name, annotation):
        """Emit a function implementation"""
        template = """{PROTOTYPE} {{
            CaffeineClient *currentClient = [CaffeineClient clientOnThread:[NSThread currentThread] forURL:clientURL];
    NSString *result = [currentClient RPCClassMethod:@"{METHOD_NAME}" inClass:NSStringFromClass([self class]) withArguments:nil];
    if ([result isKindOfClass:[NSError class]]) {{
        *error = (NSError*)result;
        return {RETURNTYPE};
    }}
    return {RETURNTYPE};
}}""".format(PROTOTYPE=self.function_prototype(name, annotation), METHOD_NAME=name,
             #Must be empty string in the void case
             RETURNTYPE="" if annotation["return"] is None else "result",
             )
        return template

    def emit_header(self, name, schema):
        header = """
//
//  {CLASS}.h
//
//  Created by caffeine-codegen
//  This file is automatically generated by caffeine.  You **MUST NOT** modify it.  
//  This code is provided under the terms of the caffeine license for Python.  To use this software you must agree to its terms.
#import <Foundation/Foundation.h>
#import <caffeine-ios/caffeine_ios.h>
@interface {CLASS} : CaffeineRemoteObject

""".format(CLASS=name)

        for name, annotation in schema.functions.items():
            header += self.function_prototype(name, annotation) + ";" + "\n"
        header += "\n@end"
        return header

    def emit_implementation(self, name, schema):
        implementation = """
//
//  {CLASS}.m
//
//  Created by caffeine-codegen
//  This file is automatically generated by caffeine.  You **MUST NOT** modify it.  
//  This code is provided under the terms of the caffeine license for Python.  To use this software you must agree to its terms.

#import "{CLASS}.h"
#import <caffeine-ios/caffeine_ios.h>
@implementation {CLASS}
static NSURL *clientURL;

+ (void)load {{
    clientURL = [NSURL URLWithString:@"{URL}"];
}}

""".format(CLASS=name, URL=self.args.url)

        # define the URL

        for name, annotation in schema.functions.items():
            implementation += self.function_implementation(
                name, annotation) + ";" + "\n"

        implementation += "\n@end"
        return implementation

    def emit_schema(self, name, schema, dir):
        """Emit code for the entire schema"""
        with open(dir + "/%s.h" % name, "w") as header:
            header.write(self.emit_header(name, schema))

        with open(dir + "/%s.m" % name, "w") as implementation:
            implementation.write(self.emit_implementation(name, schema))

    def generate(self):
        """Run the generator and emit all code"""
        for name, schema in self.schemas.items():
            self.emit_schema(name, schema, dir=self.args.output)


def codegen(args):
    """main function"""
    import caffeine.worker as worker
    client = worker.RPCClient(url=args.url)
    schemas = client.CaffeineService.directory()
    codegen = None
    if args.language == "objc":
        codegen = ObjCCodeGen(schemas, args)
    else:
        raise NotImplementedError("Language not implemented")

    codegen.generate()

def main():
    args = parser.parse_args()
    codegen(args)
if __name__ == "__main__":
    main()
