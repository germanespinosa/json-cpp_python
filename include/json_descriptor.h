#include "json_cpp/json_base.h"
#include <unordered_map>
#include <memory>
#include <utility>

//#define Json_descriptor_ptr Json_descriptor*

#define Json_descriptor_ptr std::unique_ptr<Json_descriptor>

namespace json_cpp {

    struct Json_descriptor : Json_base {
        Json_descriptor() = default;
        enum class Json_descriptor_type {
            Null,
            Bool,
            Int,
            Float,
            String,
            Object,
            List
        };
        virtual Json_descriptor_ptr new_item() const {
            return std::make_unique<Json_descriptor>();
        };
        virtual Json_descriptor_type get_type() { return Json_descriptor_type::Null; };
        void json_parse(std::istream &) override;
        void json_write(std::ostream &) const override;
        virtual ~Json_descriptor() = default;
    };

    struct Json_null_descriptor : Json_descriptor {
    };

    struct Json_descriptor_container {
        Json_descriptor_container(const Json_descriptor_container &);
        Json_descriptor_container() = default;
        void replace(size_t, const Json_descriptor &);
        Json_descriptor_container &operator = (const Json_descriptor_container &);
        std::vector<Json_descriptor_ptr> values;
    };

    struct Json_bool_descriptor :Json_descriptor {
        Json_bool_descriptor() = default;
        explicit Json_bool_descriptor(bool value) : value(value) {};
        [[nodiscard]] Json_descriptor_ptr new_item() const override {
            return std::make_unique<Json_bool_descriptor>(value);
        };
        Json_descriptor_type get_type() override {return Json_descriptor_type::Bool;}
        bool value{};
        void json_parse(std::istream &) override;
        void json_write(std::ostream &) const override;
        ~Json_bool_descriptor() override = default;
    };

    struct Json_int_descriptor :Json_descriptor {
        Json_int_descriptor() = default;
        explicit Json_int_descriptor(int value) : value(value) {};
        [[nodiscard]] Json_descriptor_ptr new_item() const override {
            return std::make_unique<Json_int_descriptor>(value);
        };
        Json_descriptor_type get_type() override {return Json_descriptor_type::Int;}
        int value{};
        void json_parse(std::istream &) override;
        void json_write(std::ostream &) const override;
        ~Json_int_descriptor() override = default;
    };

    struct Json_float_descriptor :Json_descriptor {
        Json_float_descriptor() = default;
        explicit Json_float_descriptor(float value) : value(value) {};
        [[nodiscard]] Json_descriptor_ptr new_item() const override {
            return std::make_unique<Json_float_descriptor>(value);
        };
        Json_descriptor_type get_type() override {return Json_descriptor_type::Float;}
        float value{};
        void json_parse(std::istream &) override;
        void json_write(std::ostream &) const override;
        ~Json_float_descriptor() override = default;
    };

    struct Json_string_descriptor :Json_descriptor {
        Json_string_descriptor() = default;
        explicit Json_string_descriptor(std::string value) : value(std::move(value)) {};
        [[nodiscard]] Json_descriptor_ptr new_item() const override {
            return std::make_unique<Json_string_descriptor>(value);
        };
        Json_descriptor_type get_type() override {return Json_descriptor_type::String;}
        std::string value{};
        void json_parse(std::istream &) override;
        void json_write(std::ostream &) const override;
        ~Json_string_descriptor() override = default;
    };

    struct Json_list_descriptor : Json_descriptor {
        Json_list_descriptor() = default;
        explicit Json_list_descriptor(const Json_descriptor_container& value, bool allow_nulls) :
                allow_null_values(allow_nulls),
                value(value) {};
        [[nodiscard]] Json_descriptor_ptr new_item() const override {
            return std::make_unique<Json_list_descriptor>(value, allow_null_values);
        };
        Json_descriptor_type get_type() override {return Json_descriptor_type::List;}
        bool allow_null_values = true;
        Json_descriptor_container value{};
        Json_descriptor_ptr item_descriptor;
        void set_item_descriptor(const Json_descriptor &item_descriptor);
        void json_parse(std::istream &) override;
        void json_write(std::ostream &) const override;
    };

    struct Json_variant_descriptor :Json_descriptor {
        Json_variant_descriptor() = default;
        explicit Json_variant_descriptor(const Json_descriptor_ptr &value) :
            value(value->new_item()) {};

        [[nodiscard]] Json_descriptor_ptr new_item() const override {
            if (value)
                return std::make_unique<Json_variant_descriptor>(value);
            else
                return std::make_unique<Json_variant_descriptor>();
        };
        Json_descriptor_ptr value{};
        Json_descriptor_type get_type() override {
            if (value) return value->get_type();
            return Json_descriptor_type::Null;
        }
        void clear();
        ~Json_variant_descriptor() override;
        Json_variant_descriptor &operator =(const Json_variant_descriptor &);
        Json_variant_descriptor &operator =(const Json_descriptor &);
        void json_parse(std::istream &) override;
        void json_write(std::ostream &) const override;
    };

    struct Json_object_descriptor :Json_descriptor {
        [[nodiscard]] Json_descriptor_ptr new_item() const override {
            return std::make_unique<Json_object_descriptor>(*this);
        };
        Json_descriptor_type get_type() override {return Json_descriptor_type::Object;}
        void add_member(const std::string &, Json_descriptor &, bool member_mandatory);
        Json_descriptor_container members_descriptor;
        std::vector<std::string> members_name;
        std::vector<bool> members_mandatory;
        bool allow_undefined_members{true};
        void set(const std::string &, Json_descriptor &);
        void set(const std::string &, bool);
        void set(const std::string &, int);
        void set(const std::string &, float);
        void set(const std::string &, std::string);
        Json_descriptor &get(const std::string);
        int find(const std::string &);
        bool contains(const std::string &);
        void json_parse(std::istream &) override;
        void json_write(std::ostream &) const override;
        ~Json_object_descriptor() override = default;
    };

}