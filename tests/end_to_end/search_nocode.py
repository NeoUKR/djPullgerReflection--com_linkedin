from rest_framework.test import APITestCase
from . import nocode
from django.test import tag


class Test000NoCode(APITestCase):
    @tag('NoCode')
    def test_no_code(self):
        executing_code = nocode.ExecutingCode()
        next_command = None
        status = ""
        status_executed = ""

        end = False
        while end is False:
            if next_command is None:
                print(f"{status}" +
                      f"{'' if status_executed == '' else ' > '}" +
                      f"{status_executed}" +
                      f"{'' if status == '' else ' >> ' }" +
                      f"COMMAND:", end="")
                command = input()
            else:
                command = next_command
                next_command = None
            # -------------------------------------------------------------
            if command == "ac":
                print("New code", end=":")
                executing_code.append_code(input())
            elif command == "al":
                print("APPEND LIBRARY: FROM", end=">>")
                from_path = input()
                if from_path.strip() != "" and from_path is not None:
                    print("APPEND LIBRARY: ", end=">>")
                    element_name = input()
                    if element_name.strip() != "" and element_name is not None:
                        executing_code.append_library(from_path=from_path, element_name=element_name)
            elif command == "n":
                result_operation, description = executing_code.next_line()
                if result_operation is True:
                    status = executing_code.get_code_string()
                    status_executed = 'NOT EXECUTED'
                else:
                    print("Error: ", description)
            elif command == "gcs":
                print(executing_code.get_code_string())
            elif command == 'e' or command == 'en':
                try:
                    exec(executing_code.get_code_string())
                except BaseException as e:
                    print(f"Error: {e}")
                    status_executed = 'ERROR'
                else:
                    executing_code.set_executed()
                    status_executed = 'EXECUTED'
                    if command == 'en':
                        next_command = 'n'
            elif command == "exit":
                print("Finalising.")
                end = True
            elif command == "l":
                executing_code.load_json()
            elif command == "s":
                executing_code.save_json()

