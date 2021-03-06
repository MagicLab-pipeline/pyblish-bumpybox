import os

import nuke

import pyblish.api


class RepairNukeWriteGeoNodeAction(pyblish.api.Action):

    label = "Repair"
    icon = "wrench"
    on = "failed"

    def process(self, context, plugin):

        # Get the errored instances
        failed = []
        for result in context.data["results"]:
            if (result["error"] is not None and result["instance"] is not None
               and result["instance"] not in failed):
                failed.append(result["instance"])

        # Apply pyblish.logic to get the instances for the plug-in
        instances = pyblish.api.instances_by_plugin(failed, plugin)

        for instance in instances:

            cls_instance = ValidateNukeWriteGeoNode()
            value = cls_instance.get_expected_value(instance)
            instance[0]["file"].setValue(value)

            ext = os.path.splitext(value)[1]
            instance[0]["file_type"].setValue(ext[1:])


class ValidateNukeWriteGeoNode(pyblish.api.InstancePlugin):
    """ Validates file output. """

    order = pyblish.api.ValidatorOrder
    optional = True
    families = ["writegeo"]
    label = "WriteGeo Node"
    actions = [RepairNukeWriteGeoNodeAction]
    hosts = ["nuke"]
    targets = ["default", "process"]

    def process(self, instance):

        # Validate output path
        current = instance[0]["file"].getValue()
        expected = self.get_expected_value(instance)

        msg = "Output path for \"{0}\"."
        msg += " Current: \"{1}\". Expected: \"{2}\""
        assert current == expected, msg.format(
            instance[0].name(), current, expected
        )

        # Validate file type
        msg = "Wrong file type \"{0}\" selected for extension \"{1}\""
        ext = os.path.splitext(current)[1][1:]
        file_type = instance[0]["file_type"].enumName(
            int(instance[0]["file_type"].getValue())
        )
        assert file_type == ext, msg.format(file_type, ext)

    def get_current_value(self, instance):

        current = ""
        if nuke.filename(instance[0]):
            current = nuke.filename(instance[0])

        return current

    def get_expected_value(self, instance):

        expected = (
            "[python {nuke.script_directory()}]/workspace/[python "
            "{os.path.splitext(os.path.basename(nuke.scriptName()))[0]}]_"
            "[python {nuke.thisNode().name()}]"
        )

        # Extension, defaulting to exr files.
        current = self.get_current_value(instance)
        ext = os.path.splitext(os.path.basename(current))[1]
        if not ext:
            ext = ".abc"
        expected += ext

        return expected
