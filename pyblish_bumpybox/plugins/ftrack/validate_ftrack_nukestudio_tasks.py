import collections

import pyblish.api


class ValidateFtrackNukeStudioTasks(pyblish.api.ContextPlugin):
    """Validate tasks."""

    order = pyblish.api.ValidatorOrder
    label = "Ftrack Tasks"
    hosts = ["nukestudio"]

    def process(self, context):

        labels = []
        for instance in context:
            if instance.data["family"] != "trackItem.ftrackEntity.task":
                continue
            labels.append(instance.data["label"])

        duplicates = []
        for item, count in collections.Counter(labels).items():
            if count > 1:
                duplicates.append(item)

        assert not duplicates, "Duplicate tasks found: {0}".format(duplicates)
