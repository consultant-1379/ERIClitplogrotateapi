##############################################################################
# COPYRIGHT Ericsson AB 2013
#
# The copyright to the computer program(s) herein is the property of
# Ericsson AB. The programs may be used and/or copied only with written
# permission from Ericsson AB. or in accordance with the terms and
# conditions stipulated in the agreement/contract under which the
# program(s) have been supplied.
##############################################################################


import unittest
from logrotate_extension.logrotate_extension import LogrotateExtension
from logrotate_extension.logrotate_extension import MailFirstAndMailLastValidator
from litp.core.validators import ValidationError


class TestsysparamspluginExtension(unittest.TestCase):

    def setUp(self):
        self.ext = LogrotateExtension()

    def test_property_types_registered(self):
        # Assert that only extension's property types
        # are defined.
        prop_types_expected = ['logrotate_basic_size',
                               'logrotate_any_string',
                               'logrotate_date_format',
                               'logrotate_email', 'logrotate_time_period',
                               'comma_separated_file_names']
        prop_types = [pt.property_type_id for pt in
                      self.ext.define_property_types()]
        self.assertEquals(prop_types_expected, prop_types)

    def test_item_types_registered(self):
        # Assert that only extension's item types
        # are defined.
        item_types_expected = ['logrotate-rule', 'logrotate-rule-config', ]
        item_types = [it.item_type_id for it in
                      self.ext.define_item_types()]
        diff = [x for x in item_types_expected if x not in item_types]
        self.assertEquals(len(diff), 0)

    def test_path_regex(self):
        prop = self.ext.define_property_types()[-1]
        self.assertEquals(None, prop.validators[-1].validate("/var/log/messages,/tmp/test.log,/var/another/*"))
        self.assertEquals(None, prop.validators[-1].validate("/var/log/my\\ log,/tmp/test.log,/var/another/*"))
        self.assertEquals("Value \"/var/log/cobber/*.log /var/log/libvirtd/*.log\" is not a valid path.",
            prop.validators[-1].validate("/var/log/cobber/*.log /var/log/libvirtd/*.log").error_message)

        self.assertEquals('Value "/var/log/   messages, /tmp/temp.log /var/another/*" is not a valid path.',
            prop.validators[-1].validate("/var/log/   messages, /tmp/temp.log /var/another/*").error_message)

        self.assertEquals(None, prop.validators[-1].validate("/var/log/messages,/tmp/test.log,/var/another/*"))

        self.assertEquals('Value "/var/log/messages /, /tmp/test.log /var/another/*" is not a valid path.',
                          prop.validators[-1].validate("/var/log/messages /, /tmp/test.log /var/another/*").error_message)

        self.assertEquals(None, prop.validators[-1].validate("/home/my\ documents/,/tmp/test.log,/var/another/*"))
        
    def test_mailfirst_and_maillast(self):
        validator = MailFirstAndMailLastValidator()
        expected = ValidationError(error_message='The properties "mailfirst"'
                        ' and "maillast" can not both be set to true')
        result = validator.validate({'mailfirst': 'true', 'maillast': 'true'})
        self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()
