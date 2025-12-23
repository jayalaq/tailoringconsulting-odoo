from odoo import fields
from odoo.tests import common

@common.tagged('post_install', '-at_install')
class TestAccountMoveValidation(common.TransactionCase):
    def setUp(self):
        super().setUp()

        self.valid_numbers_data = {
            'word': '12345',
            'length': 5,
            'validation_type': 'equal',
            'field_name': 'TestFieldEqual',
            'expected_result': ''
        }

        self.invalid_numbers_data = {
            'word': '123456',
            'length': 5,
            'validation_type': 'equal',
            'field_name': 'TestFieldEqual',
            'expected_result': "- La cantidad de caracteres para el campo 'TestFieldEqual' debe ser: 5 \n"
        }

        self.max_letters_data = {
            'word': 'ABCDE',
            'length': 5,
            'validation_type': 'max',
            'field_name': 'TestFieldMax',
            'expected_result': "- La cantidad de caracteres para el campo 'TestFieldMax' debe ser como máximo: 5 \n"
        }
        self.valid_numbers_data_2 = {
            'word': '12345',
            'validation_type': 'numbers',
            'field_name': 'TestFieldNumbers',
            'expected_result': ''
        }

        self.invalid_numbers_data_2 = {
            'word': 'abc123',
            'validation_type': 'numbers',
            'field_name': 'TestFieldNumbers',
            'expected_result': "- El campo 'TestFieldNumbers' solo debe contener números.\n"
        }

        self.zero_numbers_data = {
            'word': '0000',
            'validation_type': 'numbers',
            'field_name': 'TestFieldNumbers',
            'expected_result': "- El campo 'TestFieldNumbers' no puede contener solo ceros.\n"
        }

        self.special_characters_data = {
            'word': 'abc@123',
            'validation_type': 'letters',
            'field_name': 'TestFieldSpecial',
            'expected_result': "- El campo 'TestFieldSpecial' contiene caracteres no permitidos:  @ \n"
        }

    def test_validate_long_equal_numbers_valid(self):
       
        result = self._validate_long(**self.valid_numbers_data)
        self.assertEqual(result, self.valid_numbers_data['expected_result'],
                         "La validación debería pasar sin errores")

    def test_validate_long_equal_numbers_invalid(self):
      
        result = self._validate_long(**self.invalid_numbers_data)
        self.assertEqual(result, self.invalid_numbers_data['expected_result'],
                         "La validación debería fallar con el mensaje esperado")

    def test_validate_long_max_letters(self):
      
        result = self._validate_long(**self.max_letters_data)
        self.assertEqual(result, self.max_letters_data['expected_result'],
                         "La validación debería fallar con el mensaje esperado")
  
    def test_validate_word_structure_numbers_valid(self):
        
        result = self._validate_word_structure(**self.valid_numbers_data_2)
        self.assertEqual(result, self.valid_numbers_data_2['expected_result'],
                         "La validación debería pasar sin errores")

    def test_validate_word_structure_numbers_invalid(self):
       
        result = self._validate_word_structure(**self.invalid_numbers_data_2)
        self.assertEqual(result, self.invalid_numbers_data_2['expected_result'],
                         "La validación debería fallar con el mensaje esperado")

    def test_validate_word_structure_numbers_zeros(self):
        
        result = self._validate_word_structure(**self.zero_numbers_data)
        self.assertEqual(result, self.zero_numbers_data['expected_result'],
                         "La validación debería fallar con el mensaje esperado")

    def test_validate_word_structure_special_characters(self):
        
        result = self._validate_word_structure(**self.special_characters_data)
        self.assertEqual(result, self.special_characters_data['expected_result'],
                         "La validación debería fallar con el mensaje esperado")


    def _validate_long(self, word, length, validation_type, field_name, expected_result):
        if word and validation_type:
            if validation_type == 'equal':
                if len(word) != length:
                    return "- La cantidad de caracteres para el campo '%s' debe ser: %d \n" % (field_name, length)
            elif validation_type == 'max':
                if len(word) > length:
                    return "- La cantidad de caracteres para el campo '%s' debe ser como máximo: %d \n" % (field_name, length)
        return ''

    def _validate_word_structure(self, word, validation_type, field_name, expected_result):
        special_characters = '-°%&=~\\+?*^$()[]{}|@%#"/¡¿!:.,;'
        if word:
            if validation_type == 'numbers':
                if not word.isdigit():
                    return "- El campo '%s' solo debe contener números.\n" % field_name
                else:
                    total = 0
                    for d in str(word):
                        total += int(d)
                    if total == 0:
                        return "- El campo '%s' no puede contener solo ceros.\n" % field_name
            special = ''
            for letter in word:
                if letter in special_characters:
                    special += letter
            if special != '':
                return "- El campo '%s' contiene caracteres no permitidos:  %s \n" % (field_name, special)
        return ''