import jsonschema
from rest_framework.exceptions import ParseError
from rest_framework.parsers import JSONParser


class JSONSchemaParser(JSONParser):
    def parse(self, stream, media_type=None, parser_context=None):
        data = super(JSONSchemaParser, self).parse(stream, media_type,
                                                   parser_context)
        try:
            view = parser_context["view"]
            jsonschema.validate(data, view.schema)
        except Exception as error:
            raise ParseError(error.message)
        else:
            return data