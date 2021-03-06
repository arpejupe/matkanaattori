# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: location.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='location.proto',
  package='matkanaattori',
  serialized_pb=_b('\n\x0elocation.proto\x12\rmatkanaattori\"\xe6\x01\n\x08Response\x12\x32\n\x06status\x18\x01 \x02(\x0e\x32\".matkanaattori.Response.StatusCode\x12\x19\n\x11requestedLocation\x18\x02 \x01(\t\x12\x32\n\x08location\x18\x03 \x03(\x0b\x32 .matkanaattori.Response.Location\x1a$\n\x08Location\x12\x0b\n\x03lat\x18\x01 \x02(\x01\x12\x0b\n\x03lng\x18\x02 \x02(\x01\"1\n\nStatusCode\x12\t\n\x05\x46OUND\x10\x00\x12\r\n\tNOT_FOUND\x10\x01\x12\t\n\x05\x45RROR\x10\x02')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)



_RESPONSE_STATUSCODE = _descriptor.EnumDescriptor(
  name='StatusCode',
  full_name='matkanaattori.Response.StatusCode',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='FOUND', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='NOT_FOUND', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERROR', index=2, number=2,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=215,
  serialized_end=264,
)
_sym_db.RegisterEnumDescriptor(_RESPONSE_STATUSCODE)


_RESPONSE_LOCATION = _descriptor.Descriptor(
  name='Location',
  full_name='matkanaattori.Response.Location',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='lat', full_name='matkanaattori.Response.Location.lat', index=0,
      number=1, type=1, cpp_type=5, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='lng', full_name='matkanaattori.Response.Location.lng', index=1,
      number=2, type=1, cpp_type=5, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=177,
  serialized_end=213,
)

_RESPONSE = _descriptor.Descriptor(
  name='Response',
  full_name='matkanaattori.Response',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='status', full_name='matkanaattori.Response.status', index=0,
      number=1, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='requestedLocation', full_name='matkanaattori.Response.requestedLocation', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='location', full_name='matkanaattori.Response.location', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_RESPONSE_LOCATION, ],
  enum_types=[
    _RESPONSE_STATUSCODE,
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=34,
  serialized_end=264,
)

_RESPONSE_LOCATION.containing_type = _RESPONSE
_RESPONSE.fields_by_name['status'].enum_type = _RESPONSE_STATUSCODE
_RESPONSE.fields_by_name['location'].message_type = _RESPONSE_LOCATION
_RESPONSE_STATUSCODE.containing_type = _RESPONSE
DESCRIPTOR.message_types_by_name['Response'] = _RESPONSE

Response = _reflection.GeneratedProtocolMessageType('Response', (_message.Message,), dict(

  Location = _reflection.GeneratedProtocolMessageType('Location', (_message.Message,), dict(
    DESCRIPTOR = _RESPONSE_LOCATION,
    __module__ = 'location_pb2'
    # @@protoc_insertion_point(class_scope:matkanaattori.Response.Location)
    ))
  ,
  DESCRIPTOR = _RESPONSE,
  __module__ = 'location_pb2'
  # @@protoc_insertion_point(class_scope:matkanaattori.Response)
  ))
_sym_db.RegisterMessage(Response)
_sym_db.RegisterMessage(Response.Location)


# @@protoc_insertion_point(module_scope)
