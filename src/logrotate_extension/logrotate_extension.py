##############################################################################
# COPYRIGHT Ericsson AB 2013
#
# The copyright to the computer program(s) herein is the property of
# Ericsson AB. The programs may be used and/or copied only with written
# permission from Ericsson AB. or in accordance with the terms and
# conditions stipulated in the agreement/contract under which the
# program(s) have been supplied.
##############################################################################
import re

from litp.core.model_type import ItemType
from litp.core.model_type import Collection
from litp.core.model_type import Property
from litp.core.model_type import PropertyType
from litp.core.extension import ModelExtension
from litp.core.validators import PropertyValidator
from litp.core.validators import ValidationError
from litp.core.validators import NotEmptyStringValidator
from litp.core.validators import ItemValidator


class LogrotateExtension(ModelExtension):
    """
    Logrotate model extension. This model extension defines property and item \
types that enable the user to create logrotate configuration files in the \
/etc/logrotate.d directory.
    """

    def define_property_types(self):
        return [PropertyType("logrotate_basic_size", regex=r"^\d+[kMG]?$"),
                PropertyType("logrotate_any_string", regex=r"^.+$",
                            validators=[NotEmptyStringValidator()]),
                PropertyType("logrotate_date_format",
                             regex="^([-]?[%]+[Y|m|d|s])*$"),
                PropertyType("logrotate_email", regex=r"[^@]+@[^@]+\.[^@]+"),
                PropertyType("logrotate_time_period", regex=r"^((day)|(week)|"
                "(month)|(year))$"),
                PropertyType("comma_separated_file_names",
                             regex=r"([^,])+(,([^,])+)*",
                             validators=[PathListValidator()])]

    def define_item_types(self):
        return [
            ItemType("logrotate-rule-config",
                extend_item="node-config",
                item_description="A collection of logrotate-rule items.",
                rules=Collection("logrotate-rule", min_count=1)
            ),
            ItemType("logrotate-rule",
                item_description="A rule to be configured "
                     "on a node.",
                     validators=[MailFirstAndMailLastValidator()],
               name=Property("basic_string",
                    prop_description="The name of the rule. "
                                      "The value of this property must be "
                                      "unique for each peer server in your "
                                      "deployment. Ensure that you select a "
                                      "name that is not already in use by any "
                                      "pre-existing files in "
                                      "the /etc/logrotate.d directory",
                    required=True,
                    updatable_plugin=False,
                    updatable_rest=False),

                path=Property("comma_separated_file_names",
                    prop_description=(
                        "The path of the log file(s) to be "
                        "rotated. For multiple files, this is a space-"
                        "separated string; for "
                        "example: var/log/exampleservice/*.log "
                        "/var/log/libvirtd/*.log. If there are "
                        "duplicate paths in any of the files in "
                        "the /etc/logrotate.d directory (including "
                        "those files not managed by LITP), "
                        "logrotate applies the rule that is found "
                        "first (rule files are sorted alphabetically)"
                    ),
                    required=True
                ),
                compress=Property("basic_boolean",
                    prop_description=(
                        "The rotated log "
                        "files are compressed"
                    )
                ),
                compresscmd=Property("logrotate_any_string",
                    prop_description=(
                        "The command that is executed to "
                        "compress the rotated log files"
                        ),
                ),
                compressext=Property("basic_string",
                    prop_description=(
                        "The extension applied to the "
                        "rotated log files after they have been "
                        "compressed"
                    )
                ),
                compressoptions=Property("basic_string",
                    prop_description=(
                        "The options passed to the compression program "
                        "specified in compresscmd"
                    )
                ),
                copy=Property("basic_boolean",
                    prop_description=(
                        "A copy of the log file is made without changing "
                        "the original"
                    )
                ),
                copytruncate=Property("basic_boolean",
                    prop_description=(
                        "Truncates the original log file after "
                        "making a copy of it"
                    )
                ),
                create=Property("basic_boolean",
                    prop_description=(
                        "Creates a new log file immediately after "
                        "rotation"
                    )
                ),
                create_mode=Property("file_mode",
                    prop_description=(
                        "The octal mode that "
                        "applies to the newly-created log file if "
                        "create => true (optional). You must "
                        "define a value for the create property if "
                        "you include the create_mode property in "
                        "your rule"
                        )
                ),
                create_owner=Property("basic_string",
                    prop_description=(
                        "The username of the owner of "
                        "the newly-created log file if create => "
                        "true. You must define a value for "
                        "the create_mode property if you include "
                        "the create_owner property in your rule"
                    )
                ),
                create_group=Property("basic_string",
                    prop_description=(
                         "The group name that "
                         "applies to the newly-created log file if "
                         "create => true (optional). You must "
                         "define a value for the create_owner "
                         "property if you include the "
                         "create_group property in your rule"
                    )
                ),
                dateext=Property("basic_boolean",
                    prop_description=(
                        "Rotated log files "
                        "are archived with the date in the log "
                        "filename rather than just a number"
                    )
                ),
                dateformat=Property("logrotate_date_format",
                    prop_description=(
                        "The date format used for the "
                        "value of the dateext property. Valid "
                        "specifiers are %Y, %m, %d and %s"
                    )
                ),
                delaycompress=Property("basic_boolean",
                    prop_description=(
                        "Compression of "
                        "the rotated log file is delayed until the "
                        "next logrotate run"
                    )
                ),
                extension=Property("basic_string",
                    prop_description=(
                        "The log filename extension that "
                        "you want to be maintained even after "
                        "rotation"
                    )
                ),
                ifempty=Property("basic_boolean",
                    prop_description=(
                        "The log file is "
                        "rotated if it is empty"
                    )
                ),
                mail=Property("logrotate_email",
                    prop_description=(
                         "The email address to which logs, "
                         "that are about to be rotated out "
                         "of existence, are emailed to"
                    )
                ),
                mailfirst=Property("basic_boolean",
                    prop_description=(
                        "When used with "
                        "the mail property, the file "
                        "that has just been rotated is emailed "
                        "instead of the file that is about to expire. "
                        "The mailfirst and mailast properties are "
                        "mutually exclusive"
                    )
                ),
                maillast=Property("basic_boolean",
                    prop_description=(
                        "When used with "
                        "the mail property, the file "
                        "that is about to expire is emailed instead "
                        "of the file that has just been rotated. "
                        "The mailfirst and mailast properties are "
                        "mutually exclusive"
                    )
                ),
                maxage=Property("integer",
                    prop_description=(
                        "The number of days for which a "
                        "rotated log file can remain on the "
                        "system"
                    )
                ),
                minsize=Property("logrotate_basic_size",
                    prop_description=(
                        "The minimum size, measured in "
                        "bytes, which a log file must reach before "
                        "it is rotated (note that it will not be "
                        "rotated before the scheduled rotation "
                        "time). Append k,M or G for kilobytes, "
                        "megabytes and gigabytes, respectively"
                    )
                ),
                missingok=Property("basic_boolean",
                    prop_description=(
                        "Ignores missing log files. If this value is "
                        "set to false, an error is issued if "
                        "log files are missing"
                    )
                ),
                olddir=Property("path_string",
                    prop_description=(
                        "The path to the directory to which "
                        "old versions of log files are moved"
                    )
                ),
                postrotate=Property("logrotate_any_string",
                    prop_description=(
                        "The command that is executed "
                        "by /bin/sh after the log file is rotated"
                    )
                ),
                prerotate=Property("logrotate_any_string",
                    prop_description=(
                        "The command that is executed "
                        "by /bin/sh before the log file is rotated "
                        "(and only if the log file is actually going "
                        "to be rotated)"
                    )
                ),
                firstaction=Property("logrotate_any_string",
                    prop_description=(
                        "The command string that should be "
                        "executed by /bin/sh "
                        "once before all log files that match the wildcard "
                        "pattern are rotated (optional)"
                    )
                ),
                lastaction=Property("logrotate_any_string",
                    prop_description=(
                        "The command executed once "
                        "by /bin/sh after all the log files that match "
                        "the wildcard pattern are rotated"
                    )
                ),
                rotate=Property("integer",
                    prop_description=(
                        "The number of rotated log files to "
                        "keep on disk"
                    )
                ),
                rotate_every=Property("logrotate_time_period",
                    prop_description=(
                        "How often the log files should be rotated as "
                        "a String. Valid values are \'day\', \'week\', "
                        "\'month\' and \'year\' (optional)"
                    )
                ),
                sharedscripts=Property("basic_boolean",
                    prop_description=(
                        "Runs the postrotate and prerotate scripts for "
                        "each matching file. If this value is set "
                        "to false, these scripts are run only once"
                    )
                ),
                shred=Property("basic_boolean",
                    prop_description=(
                        "Logs are deleted "
                        "using the shred utility. If this value is set "
                        "to false, logs are deleted using the unlink "
                        "utility"
                    )
                ),
                shredcycles=Property("integer",
                    prop_description=(
                        "The number of times that the "
                        "shred utility overwrites log files before "
                        "unlinking them"
                    )
                ),
                size=Property("logrotate_basic_size",
                    prop_description=(
                        "The minimum size, measured in "
                        "bytes, which a log file must reach before "
                        "it is rotated (regardless of the scheduled "
                        "rotation time). Append k, M or G for "
                        "kilobytes, megabytes and gigabytes, "
                        "respectively"
                    )
                ),
                start=Property("integer",
                    prop_description=(
                        "The number used as the base for "
                        "the extensions appended to the rotated "
                        "log files"
                    )
                ),
                uncompresscmd=Property("logrotate_any_string",
                    prop_description=(
                        "The command used to "
                        "uncompress log files"
                    )
                )
            )
        ]


class PathListValidator(PropertyValidator):
    """
    Validates that a property value doesn't have quotes \"\
characters in it.
    """

    def __init__(self,):
        """
        """
        super(PathListValidator, self).__init__()

    def validate(self, property_value,):
        escaped_spaces = property_value.replace(r'\ ', '!')
        if len(escaped_spaces.split(" ")) > 1:
            return ValidationError(
                error_message=("Value \"%s\" is not a valid path." %
                               (property_value,))
            )
        for p in property_value.split(","):
            if len(p) < 1 or p.startswith(" ") or p.endswith(" "):
                return ValidationError(
                    error_message=("Value \"" + p + "\" is not a valid path."))
            if not re.match(r"([A-Za-z0-9\-\.\*\s\\_\/#:]+)?", p):
                return ValidationError(
                    error_message=("Value \"" + p + "\" is not a valid path."))


class MailFirstAndMailLastValidator(ItemValidator):
    """
    Validates that the properties "mailfirst"' and "maillast" '
    'can not both be set to true'.
    """

    def __init__(self,):
        """
        """
        super(MailFirstAndMailLastValidator, self).__init__()

    def validate(self, properties):
        errors = []
        mailfirst = 'mailfirst'
        maillast = 'maillast'
        mailfirst_prop = properties.get(mailfirst, '')
        maillast_prop = properties.get(maillast, '')
        if mailfirst_prop == 'true' and maillast_prop == 'true':
            errors = ValidationError(error_message='The properties "mailfirst"'
                        ' and "maillast" can not both be set to true')
        return errors
