#include "catch.h"
#include "../include/json_descriptor.h"
#include <iostream>
#include <cstring>

using namespace json_cpp;
using namespace std;

TEST_CASE("Json_bool_descriptor"){
    Json_bool_descriptor v;
    CHECK(v.to_json() == "false");
    v.value = true;
    CHECK(v.to_json() == "true");
    v.from_json("false");
    CHECK(v.to_json() == "false");
    v.from_json("true");
    CHECK(v.to_json() == "true");
}

TEST_CASE("Json_int_descriptor"){
    Json_int_descriptor v;
    CHECK(v.to_json() == "0");
    v.value = 100;
    CHECK(v.to_json() == "100");
    v.from_json("20");
    CHECK(v.to_json() == "20");
    v.from_json("30");
    CHECK(v.to_json() == "30");
}

TEST_CASE("Json_float_descriptor"){
    Json_float_descriptor v;
    CHECK(v.to_json() == "0");
    v.value = 100.5;
    CHECK(v.to_json() == "100.5");
    v.from_json("20.5");
    CHECK(v.to_json() == "20.5");
    v.from_json("30.5");
    CHECK(v.to_json() == "30.5");
}

TEST_CASE("Json_string_descriptor"){
    Json_string_descriptor v;
    CHECK(v.to_json() == "\"\"");
    v.value = "100";
    CHECK(v.to_json() == "\"100\"");
    v.from_json("\"hello\"");
    CHECK(v.to_json() == "\"hello\"");
    v.from_json("\"bye\"");
    CHECK(v.to_json() == "\"bye\"");
}

TEST_CASE("Json_object_descriptor"){
    Json_int_descriptor v;
    CHECK(v.to_json() == "0");
    v.value = 100;
    CHECK(v.to_json() == "100");
    Json_object_descriptor o;
    CHECK(o.to_json() == "{}");
    o.add_member("m1", v, true);
    CHECK(o.to_json() == "{\"m1\":100}");

    Json_object_descriptor oo;
    Json_bool_descriptor b;
    oo.add_member("m2", b, true);
    o.add_member("m3",oo, true);
    CHECK(o.to_json() == "{\"m1\":100,\"m3\":{\"m2\":false}}");
    o.from_json("{\"m1\":50,\"m3\":{\"m2\":true}}");
    CHECK(o.to_json() == "{\"m1\":50,\"m3\":{\"m2\":true}}");
    o.set("m1",200);
    CHECK(o.to_json() == "{\"m1\":200,\"m3\":{\"m2\":true}}");
}

TEST_CASE("Json_list_descriptor"){
    Json_bool_descriptor jb;
    jb.value = true;
    Json_int_descriptor ji;
    ji.value = 155;
    Json_float_descriptor jf;
    jf.value = 15.5;
    Json_string_descriptor js;
    js.value = "hello";
    Json_object_descriptor jo;
    jo.add_member("m0", jb, true);
    jo.add_member("m1", ji, true);
    jo.add_member("m2", jf, true);
    jo.add_member("m3", js, true);
    cout << jo << endl;
    Json_list_descriptor jl;
//    jl.set_item_descriptor(jo);
//    jl.from_json("[{\"m0\":true,\"m1\":155,\"m2\":15.5,\"m3\":\"hello\"},{\"m0\":false,\"m1\":35,\"m2\":5.5,\"m3\":\"bye\"}]");
//    cout << jl << endl;
}

TEST_CASE("Json_variant_descriptor"){
    Json_variant_descriptor jv;
    jv.from_json("1");
    cout << jv << endl;
    jv.from_json("10.5");
    cout << jv << endl;
    jv.from_json("true");
    cout << jv << endl;
    jv.from_json("false");
    cout << jv << endl;
    jv.from_json("\"false\"");
    cout << jv << endl;
    jv.from_json("null");
    cout << jv << endl;
    jv.from_json("[1,2,3]");
    cout << jv << endl;
    jv.from_json("{\"n\":{\"m0\":true,\"m1\":155,\"m2\":15.5,\"m3\":\"hello\"}}");
    cout << jv << endl;
    jv.from_json("[[[{\"n\":[{\"m0\":true,\"m1\":155,\"m2\":15.5,\"m3\":\"hello\",\"m4\":{\"a\":1,\"b\":true,\"c\":null}},{\"m0\":false,\"m1\":35,\"m2\":5.5,\"m3\":\"bye\"}]}]]]");
    cout << jv << endl;
}


TEST_CASE("Python_test") {
    Json_object_descriptor jod;
    Json_bool_descriptor jbd(true);
    jod.add_member("a",jbd, true);
    Json_int_descriptor jbi(10);
    jod.add_member("b",jbi, true);
    Json_float_descriptor jbf(15.5);
    jod.add_member("c",jbf, true);
    Json_string_descriptor jbs("other");
    jod.add_member("d",jbs, true);
    Json_list_descriptor jbl;
    jbl.set_item_descriptor(jbi);
    jbl.value.values.emplace_back(jbi.new_item());
    jbl.value.values.emplace_back(jbi.new_item());
    jbl.value.values.emplace_back(jbi.new_item());
    jod.add_member("e",jbl, true);
    cout << jod << endl;
    jod.from_json("{\"a\":false,\"b\":66,\"c\":5.22,\"d\":\"value\",\"e\":[4.5,5,6,7]}");
    cout << jod << endl;
}

//TEST_CASE("Json_value_bool"){
//    Python_value v(json_cpp::Python_type::Bool);
//    CHECK(v.get_python_type() == "bool");
//    CHECK(v.bool_value == false);
//}
//
//TEST_CASE("Json_value_int"){
//    Python_value v(json_cpp::Python_type::Int);
//    CHECK(v.get_python_type() == "int");
//    CHECK(v.int_value == 0);
//}
//
//TEST_CASE("Json_value_float"){
//    Python_value v(json_cpp::Python_type::Float);
//    CHECK(v.get_python_type() == "float");
//    CHECK(v.float_value == 0);
//}
//
//TEST_CASE("Json_value_string"){
//    Python_value v(json_cpp::Python_type::String);
//    CHECK(v.get_python_type() == "str");
//    CHECK(v.string_value == "");
//}