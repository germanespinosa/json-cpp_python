#include "../include/json_descriptor.h"
#include <pybind11/pybind11.h>
#include <map>

using namespace json_cpp;
using namespace std;


PYBIND11_MODULE(json_cpp2_core, m) {
    pybind11::class_<Json_descriptor>(m, "JsonDescriptor");

    pybind11::class_<Json_variant_descriptor, Json_descriptor>(m, "JsonVariantDescriptor")
            .def(pybind11::init<>())
            .def("get_value", [](Json_variant_descriptor &d){
                return d.value.get()->new_item();
            })
            .def("get_type", &Json_variant_descriptor::get_type)
            .def("load", &Json_variant_descriptor::load)
            .def("save", &Json_variant_descriptor::save)
            .def("__str__", &Json_variant_descriptor::to_json)
            .def("__repr__", &Json_variant_descriptor::to_json)
            .def("to_json", &Json_variant_descriptor::to_json)
            .def("from_json", &Json_variant_descriptor::from_json)
            ;

    pybind11::class_<Json_null_descriptor, Json_descriptor>(m, "JsonNullDescriptor")
            .def(pybind11::init<>())
            .def("load", &Json_null_descriptor::load)
            .def("save", &Json_null_descriptor::save)
            .def("__str__", &Json_null_descriptor::to_json)
            .def("__repr__", &Json_null_descriptor::to_json)
            .def("to_json", &Json_null_descriptor::to_json)
            .def("from_json", &Json_null_descriptor::from_json)
            ;

    pybind11::class_<Json_bool_descriptor, Json_descriptor>(m, "JsonBoolDescriptor")
            .def(pybind11::init<>())
            .def_readwrite("value", &Json_bool_descriptor::value)
            .def("load", &Json_bool_descriptor::load)
            .def("save", &Json_bool_descriptor::save)
            .def("__str__", &Json_bool_descriptor::to_json)
            .def("__repr__", &Json_bool_descriptor::to_json)
            .def("to_json", &Json_bool_descriptor::to_json)
            .def("from_json", &Json_bool_descriptor::from_json)
    ;

    pybind11::class_<Json_int_descriptor, Json_descriptor>(m, "JsonIntDescriptor")
            .def(pybind11::init<>())
            .def_readwrite("value", &Json_int_descriptor::value)
            .def("load", &Json_int_descriptor::load)
            .def("save", &Json_int_descriptor::save)
            .def("__str__", &Json_int_descriptor::to_json)
            .def("__repr__", &Json_int_descriptor::to_json)
            .def("to_json", &Json_int_descriptor::to_json)
            .def("from_json", &Json_int_descriptor::from_json)
    ;

    pybind11::class_<Json_float_descriptor, Json_descriptor>(m, "JsonFloatDescriptor")
            .def(pybind11::init<>())
            .def_readwrite("value", &Json_float_descriptor::value)
            .def("load", &Json_float_descriptor::load)
            .def("save", &Json_float_descriptor::save)
            .def("__str__", &Json_float_descriptor::to_json)
            .def("__repr__", &Json_float_descriptor::to_json)
            .def("to_json", &Json_float_descriptor::to_json)
            .def("from_json", &Json_float_descriptor::from_json)
    ;

    pybind11::class_<Json_string_descriptor, Json_descriptor>(m, "JsonStringDescriptor")
            .def(pybind11::init<>())
            .def_readwrite("value", &Json_string_descriptor::value)
            .def("load", &Json_string_descriptor::load)
            .def("save", &Json_string_descriptor::save)
            .def("__str__", &Json_string_descriptor::to_json)
            .def("__repr__", &Json_string_descriptor::to_json)
            .def("to_json", &Json_string_descriptor::to_json)
            .def("from_json", &Json_string_descriptor::from_json)
    ;

    pybind11::class_<std::map<std::string, Json_descriptor*>>(m, "JsonObjectMembers")
            .def("__iter__", [](std::map<std::string, Json_descriptor*> &m) {
                return pybind11::make_iterator(m.begin(), m.end());
            }, pybind11::keep_alive<0, 1>() /* Essential: keep object alive while iterator exists */)
    ;

    pybind11::class_<Json_object_descriptor, Json_descriptor>(m, "JsonObjectDescriptor")
            .def(pybind11::init<>())
            .def_readwrite("allow_undefined_members", &Json_object_descriptor::allow_undefined_members)
            .def("add_member",+[](Json_object_descriptor &o, const string &n, Json_descriptor *d){
                o.add_member(n, *d, false);
            })
            .def("add_member",+[](Json_object_descriptor &o, const string &n, Json_descriptor *d, bool mandatory){
                o.add_member(n, *d, mandatory);
            })
            .def("get_member",+[](Json_object_descriptor &o, const string &n){
                return &(o.get(n));
            })
            .def("get_members",[](Json_object_descriptor &o){
                std::map<std::string, Json_descriptor*> members;
                for (size_t i=0;i<o.members_name.size();i++)
                    members[o.members_name[i]] = o.members_descriptor.values[i].get();
                return members;
            })
            .def("set_members",[](Json_object_descriptor &o, std::map<std::string, Json_descriptor *> &members){
                for (auto &member:members)
                    o.add_member(member.first, *member.second, true);
            })
            .def("load", &Json_object_descriptor::load)
            .def("save", &Json_object_descriptor::save)
            .def("__str__", &Json_object_descriptor::to_json)
            .def("__repr__", &Json_object_descriptor::to_json)
            .def("to_json", &Json_object_descriptor::to_json)
            .def("from_json", &Json_object_descriptor::from_json)
    ;

    m.def("get_descriptor",[](bool b){
        return Json_bool_descriptor(b);
    });
    m.def("get_descriptor",[](int i){
        return Json_int_descriptor(i);
    });
    m.def("get_descriptor",[](float f){
        return Json_float_descriptor(f);
    });
    m.def("get_descriptor",[](string &s){
        return Json_string_descriptor(s);
    });

    pybind11::class_<Json_list_descriptor, Json_descriptor>(m, "JsonListDescriptor")
            .def(pybind11::init<>())
            .def("set_item_descriptor",+[](Json_list_descriptor &o, Json_descriptor *d){
                o.set_item_descriptor(*d);
            })
            .def_readwrite("allow_null_values", &Json_list_descriptor::allow_null_values)
            .def("load", &Json_list_descriptor::load)
            .def("save", &Json_list_descriptor::save)
            .def("__str__", &Json_list_descriptor::to_json)
            .def("__repr__", &Json_list_descriptor::to_json)
            .def("to_json", &Json_list_descriptor::to_json)
            .def("from_json", &Json_list_descriptor::from_json)
            .def("__getitem__", +[](Json_list_descriptor & m, const int c){
                return m.value.values[c]->new_item();
            })
            .def("__setitem__", +[](Json_list_descriptor & m, const int c, Json_descriptor &id){
                m.value.replace(c, id);
            })
            .def("__iadd__", +[](Json_list_descriptor & m, Json_descriptor *id){
                m.value.values.push_back(id->new_item());
            })
            .def("__len__", [](const Json_list_descriptor &m){
                return m.value.values.size();
            })
            ;
}
