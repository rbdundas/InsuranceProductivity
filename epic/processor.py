import os
import sys
import importlib.util
from django.core.exceptions import ObjectDoesNotExist
from amsforms.models import AMSObjectType, FormToAMSValueMapping, AMSObjectValueDefault
from epic_sdk_scripts_rbdundas.epic_sdk import EpicSDK
from core.models import EpicSDKConfiguration, Account


def get_epic_sdk(account: Account) -> EpicSDK:
    sdk_settings = EpicSDKConfiguration.objects.filter(Account=account).first()
    sdk = None
    if sdk_settings:
        sdk = EpicSDK(
            endpoint_url=sdk_settings.EndpointURL,
            database=sdk_settings.Database,
            user_code=sdk_settings.UserCode,
            password=sdk_settings.Token,
            host=sdk_settings.Host
        )
    return sdk


def convert_form_to_dict(dict_to_process: dict, parent_dict: dict = None) -> dict:
    converted_dict = {}
    for _key, _value in dict_to_process.items():
        try:
            if _key.startswith('q'):
                new_key = _key.split('_')[1].lower()
            else:
                new_key = _key.lower()
            if isinstance(_value, str):
                converted_dict[new_key] = _value
            elif isinstance(_value, dict):
                converted_dict[new_key] = convert_form_to_dict(_value, converted_dict)
        except AttributeError:
            print(f'AttributeError: {_key}, {_value}')
        except KeyError:
            print(f'KeyError: {_key}, {_value}')
        except ObjectDoesNotExist:
            print(f'Does Not Exist: {_key}, {_value}')
        except Exception as e:
            print(f'{e}: {_key}, {_value}')
    return converted_dict


def get_value_from_nested_dict(d, _key):
    for key, value in d.items():
        if key == _key:
            yield value
        elif isinstance(value, dict):
            yield from get_value_from_nested_dict(value, _key)


def convert_form_and_post_to_ams(raw_request: dict, ams_object_type: AMSObjectType):

    def set_defaults(ams_object, ams_object_type):
        ams_value_defaults = AMSObjectValueDefault.objects.filter(AMSObjectType=ams_object_type).all()
        for default in ams_value_defaults:
            setattr(ams_object, default.AMSObjectValue.AMSField, default.DefaultValue)
        return ams_object

    def set_values_in_ams_object(ams_object, ams_object_type):
        mappings = FormToAMSValueMapping.objects.filter(AMSObjectType=ams_object_type).all()
        try:
            for each in ams_object.__dir__():
                try:
                    if each.startswith('__') and each.endswith('__'):
                        pass
                    elif isinstance(getattr(ams_object, each), str):
                        mapping = mappings.filter(AMSObjectValue__AMSField=each).first()
                        if mapping is not None:
                            field = next(get_value_from_nested_dict(converted, mapping.FormField))
                            setattr(ams_object, mapping.AMSObjectValue.AMSField, field)
                    elif isinstance(getattr(ams_object, each), list):
                        pass
                    else:
                        _child = getattr(ams_object, each)
                        _child = set_values_in_ams_object(_child, ams_object_type)
                        setattr(ams_object, each, _child)
                except KeyError:
                    print(each)
                except Exception as e:
                    print(f'{e}: {each}')
        except TypeError:
            try:
                for each in ams_object.__dict__.keys():
                    try:
                        if each.startswith('__') and each.endswith('__'):
                            pass
                        elif isinstance(getattr(ams_object, each), str):
                            mapping = mappings.filter(AMSObjectValue__AMSField=each).first()
                            if mapping is not None:
                                field = next(get_value_from_nested_dict(converted, mapping.FormField))
                                setattr(ams_object, mapping.AMSObjectValue.AMSField, field)
                        elif isinstance(getattr(ams_object, each), list):
                            pass
                        else:
                            _child = getattr(ams_object, each)
                            _child = set_values_in_ams_object(_child, ams_object_type)
                            setattr(ams_object, each, _child)
                    except KeyError:
                        print(each)
                    except AttributeError as ae:
                        print(f'{ae}: {each}')
                    except Exception as e:
                        print(f'{e}: {each}')
            except Exception as e:
                print(f'{e}: {ams_object}')
        return ams_object

    converted = convert_form_to_dict(raw_request)
    ams_object = classes[ams_object_type.AMSObjectType]
    ams_object = set_defaults(ams_object, ams_object_type)
    ams_object = set_values_in_ams_object(ams_object, ams_object_type)
    sdk = get_epic_sdk(account=ams_object_type.AMSType.Account)

    processor_str = f'{ams_object_type.AMSObjectType.lower()}_processor'
    spec = importlib.util.spec_from_file_location(processor_str, f'{os.getcwd()}/epic/{processor_str}.py')
    module = importlib.util.module_from_spec(spec)
    sys.modules[processor_str] = module
    spec.loader.exec_module(module)
    processor_module = importlib.import_module(module.__name__)
    ams_object = processor_module.create_ams_object(ams_object, converted, ams_object_type)

    results = sdk.insert_object(ams_object_type.AMSObjectType, ams_object)
    return results
