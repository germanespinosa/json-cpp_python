import unittest
from json_cpp2 import *


class Parse(unittest.TestCase):

    def test_supported_types(self):
        self.assertTrue(JsonParser.is_supported_type(None))
        self.assertTrue(JsonParser.is_supported_type(bool))
        self.assertTrue(JsonParser.is_supported_type(int))
        self.assertTrue(JsonParser.is_supported_type(float))
        self.assertTrue(JsonParser.is_supported_type(str))
        self.assertTrue(JsonParser.is_supported_type(list))
        self.assertTrue(JsonParser.is_supported_type(tuple))
        self.assertTrue(JsonParser.is_supported_type(dict))
        self.assertTrue(JsonParser.is_supported_type(JsonList))
        self.assertTrue(JsonParser.is_supported_type(JsonObject))

        self.assertTrue(JsonParser.is_supported_type(True))
        self.assertTrue(JsonParser.is_supported_type(1))
        self.assertTrue(JsonParser.is_supported_type(1.5))
        self.assertTrue(JsonParser.is_supported_type([1, 2, 3]))
        self.assertTrue(JsonParser.is_supported_type((1, 2, )))
        self.assertTrue(JsonParser.is_supported_type({'x': 10, 'y': 20}))


    def test_base_types(self):
        self.assertIsNone(JsonParser.parse("null"), "failed to parse 'null'")
        self.assertTrue(JsonParser.parse("true"), "failed to parse 'true'")
        self.assertFalse(JsonParser.parse("false"), "failed to parse 'false'")
        self.assertEqual(JsonParser.parse("1"), 1, "failed to parse 'int'")
        self.assertEqual(JsonParser.parse("-1"), -1, "failed to parse negative 'int'")
        self.assertAlmostEqual(JsonParser.parse("1.8"), 1.8, 2, "failed to parse 'float'")
        self.assertAlmostEqual(JsonParser.parse("-1.8"), -1.8, 2, "failed to parse negative 'float'")
        self.assertEqual(JsonParser.parse("\"hello\""), "hello", "failed to parse 'str'")

    def test_variant_object(self):
        self.assertIsNone(JsonParser.parse("{\"x\":null}").x, "failed to parse 'null'")
        self.assertTrue(JsonParser.parse("{\"x\":true}").x, "failed to parse 'true'")
        self.assertFalse(JsonParser.parse("{\"x\":false}").x, "failed to parse 'false'")
        self.assertEqual(JsonParser.parse("{\"x\":1}").x, 1, "failed to parse 'int'")
        self.assertEqual(JsonParser.parse("{\"x\":-1}").x, -1, "failed to parse negative 'int'")
        self.assertAlmostEqual(JsonParser.parse("{\"x\":1.8}").x, 1.8, 2, "failed to parse 'float'")
        self.assertAlmostEqual(JsonParser.parse("{\"x\":-1.8}").x, -1.8, 2, "failed to parse negative 'float'")
        self.assertEqual(JsonParser.parse("{\"x\":\"hello\"}").x, "hello", "failed to parse 'str'")
        o = JsonParser.parse("{\"a\":false,\"b\":15,\"c\":55.4,\"d\":\"ok\",\"e\":{\"f\":55,\"g\":\"ok\"},\"h\":null,\"i\":[1,2,3]}")
        self.assertEqual(o.a, False)
        self.assertEqual(o.b, 15)
        self.assertAlmostEqual(o.c, 55.4, 2)
        self.assertEqual(o.d, "ok")
        self.assertEqual(o.e.f, 55)
        self.assertEqual(o.e.g, "ok")
        self.assertIsNone(o.h)
        self.assertListEqual(o.i, [1, 2, 3])

    def test_dictionary(self):
        self.assertTrue(JsonParser.is_supported_type(dict))
        self.assertEqual(JsonParser.to_json({"a": 10, "b": 20}), "{\"a\":10,\"b\":20}")

    def test_variant_list(self):
        self.assertIsNone(JsonParser.parse("[null]")[0], "failed to parse 'null'")
        self.assertTrue(JsonParser.parse("[true]")[0], "failed to parse 'true'")
        self.assertFalse(JsonParser.parse("[false]")[0], "failed to parse 'false'")
        self.assertEqual(JsonParser.parse("[1]")[0], 1, "failed to parse 'int'")
        self.assertEqual(JsonParser.parse("[-1]")[0], -1, "failed to parse negative 'int'")
        self.assertAlmostEqual(JsonParser.parse("[1.8]")[0], 1.8, 2, "failed to parse 'float'")
        self.assertAlmostEqual(JsonParser.parse("[-1.8]")[0], -1.8, 2, "failed to parse negative 'float'")
        self.assertEqual(JsonParser.parse("[\"hello\"]")[0], "hello", "failed to parse 'str'")
        l = JsonParser.parse("[null, true, false, 1, -1, 10.5, -20.5, \"ok\"]")
        self.assertIsNone(l[0])
        self.assertTrue(l[1])
        self.assertFalse(l[2])
        self.assertEqual(l[3], 1)
        self.assertEqual(l[4], -1)
        self.assertAlmostEqual(l[5], 10.5, 2)
        self.assertAlmostEqual(l[6], -20.5, 2)
        self.assertEqual(l[7], "ok")

    def test_object(self):
        o = JsonObject(a=None, b=True, c=False)
        self.assertIsNone(o.a)
        self.assertTrue(o.b)
        self.assertFalse(o.c)
        self.assertEqual(str(o), "{\"a\":null,\"b\":true,\"c\":false}")
        c = JsonObject.create_class("test_class", a=None, b=True, c=False, d=float, f=str)
        o = c()
        self.assertIsNone(o.a)
        self.assertTrue(o.b)
        self.assertFalse(o.c)
        self.assertIs(type(o.d), float)
        self.assertIs(type(o.f), str)
        o.a = 5
        o.f = "ok"
        self.assertEqual(str(o), "{\"a\":5,\"b\":true,\"c\":false,\"d\":0,\"f\":\"ok\"}")
        self.assertTrue(o == JsonParser.parse("{\"a\":5,\"b\":true,\"c\":false,\"d\":0,\"f\":\"ok\"}"))
        c = JsonObject.create_class("test_class", a=int, b=bool, c=bool, d=float, f=str)
        o = c()
        o.load("{\"a\":15,\"b\":false,\"c\":true,\"d\":0,\"f\":\"ok\"}")
        self.assertEqual(str(o), "{\"a\":15,\"b\":false,\"c\":true,\"d\":0,\"f\":\"ok\"}")
        c = JsonObject.create_class("test_class", a=int, b=bool, c=bool, d=float, f=str, g=list, h=tuple)
        o = c()

    def test_json_object_mandatory_members(self):
        Coordinates = JsonObject.create_class("Coordinates", x=int, y=int)
        c = Coordinates.parse("{\"x\":10}")
        self.assertEqual(c.x, 10)
        self.assertEqual(c.y, int())
        c = Coordinates.parse("{\"x\":-10}")
        self.assertEqual(c.x, -10)
        self.assertEqual(c.y, int())
        Coordinates = JsonObject.create_class("Coordinates", x=int, y=int, _mandatory_members=["x", "y"])
        c = Coordinates.parse("{\"x\":10, \"y\":10}")
        self.assertEqual(c.x, 10)
        self.assertEqual(c.y, 10)
        c = Coordinates.parse("{\"x\":-10, \"y\":-10}")
        self.assertEqual(c.x, -10)
        self.assertEqual(c.y, -10)
        self.assertRaises(RuntimeError, Coordinates.parse, "{\"x\":-10}")

    def test_json_object_additional_members(self):
        Coordinates = JsonObject.create_class("Coordinates", x=int, y=int, _mandatory_members=["x", "y"])
        c = Coordinates.parse("{\"x\":-10, \"y\":-10}")
        self.assertEqual(c.x, -10)
        self.assertEqual(c.y, -10)
        c = Coordinates.parse("{\"x\":10, \"y\":15, \"z\": 20}")
        self.assertEqual(c.x, 10)
        self.assertEqual(c.y, 15)
        self.assertEqual(c.z, 20)
        Coordinates = JsonObject.create_class("Coordinates", x=int, y=int, _allow_undefined_members=False)
        c = Coordinates.parse("{\"x\":-10, \"y\":-10}")
        self.assertEqual(c.x, -10)
        self.assertEqual(c.y, -10)
        self.assertRaises(RuntimeError, Coordinates.parse, "{\"x\":10,\"y\":15,\"z\":20}")

    def test_typed_list(self):
        self.assertEqual(str(JsonList(int, [1, 2, 3])), "[1,2,3]")
        self.assertEqual(str(JsonList(int, (1, 2, 3))), "[1,2,3]")
        self.assertEqual(str(JsonList(bool, [True, True, False])), "[true,true,false]")
        self.assertEqual(str(JsonList(float, [10.3, .2, 23.1])), "[10.3,0.2,23.1]")
        self.assertEqual(str(JsonList(str, ["ok", "yes", "no"])), "[\"ok\",\"yes\",\"no\"]")
        self.assertEqual(str(JsonList(int, [1, 2, 3])), "[1,2,3]")
        self.assertEqual(str(JsonList(int, (1, 2, 3))), "[1,2,3]")
        self.assertEqual(str(JsonList(int, [1, 2, None])), "[1,2,null]")

    def test_allow_null_values(self):
        self.assertRaises(RuntimeError, JsonList, int, [1, 2, None], allow_null_values=False)
        self.assertEqual(JsonList(int, [1, 2, 3]), [1, 2, 3])
        self.assertRaises(RuntimeError, JsonList(int, [1, 2, 3], allow_null_values=False).load, "[1,2,3,null]")

    def test_list_class(self):
        c = JsonList.create_class("IntList", int, allow_null_values=False)
        self.assertEqual(c.parse("[1,2,3]"), [1, 2, 3])
        self.assertRaises(RuntimeError, c.parse, "[1,2,3,null]")

    def test_object_member_access(self):
        c = JsonObject.create_class(a=10, b=2.5)
        o = c()
        self.assertEqual(o["a"], 10)
        self.assertEqual(o["b"], 2.5)
        self.assertEqual([member for member in o], ["a", "b"])

    def test_from_file(self):
        Coordinates = JsonObject.create_class("Coordinates", x=int, y=int, _mandatory_members=["x", "y"])
        c = Coordinates.parse("{\"x\":-10, \"y\":-10}")
        c.to_file("coordinates.json")

    def test_to_json(self):
        self.assertEqual(JsonParser.to_json(None), "null")
        self.assertEqual(JsonParser.to_json(1), "1")
        self.assertEqual(JsonParser.to_json(True), "true")
        self.assertEqual(JsonParser.to_json(15.5), "15.5")
        self.assertEqual(JsonParser.to_json("ok"), "\"ok\"")
        self.assertEqual(JsonParser.to_json([1, 2, 3]), "[1,2,3]")
        self.assertEqual(JsonParser.to_json((1, 2, 3)), "[1,2,3]")


if __name__ == '__main__':
    unittest.main()
