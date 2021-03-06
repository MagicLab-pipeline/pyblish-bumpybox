import pyblish.api


class ValidateNukeStudioTrackItem(pyblish.api.InstancePlugin):
    """Validate the track item to the sequence.

    Exact matching to optimize processing.
    """

    order = pyblish.api.ValidatorOrder
    families = ["trackItem"]
    match = pyblish.api.Exact
    label = "Track Item"
    hosts = ["nukestudio"]
    optional = True

    def process(self, instance):

        item = instance.data["item"]
        media_source = item.source().mediaSource()
        msg = (
            'A setting does not match between track item "{0}" and sequence '
            '"{1}".'.format(item.name(), item.sequence().name()) +
            '\n\nSetting: "{0}".''\n\nTrack item: "{1}".\n\nSequence: "{2}".'
        )

        # Validate format settings.
        fmt = item.sequence().format()
        assert fmt.width() == media_source.width(), msg.format(
            "width", fmt.width(), media_source.width()
        )
        assert fmt.height() == media_source.height(), msg.format(
            "height", fmt.height(), media_source.height()
        )
        assert fmt.pixelAspect() == media_source.pixelAspect(), msg.format(
            "pixelAspect", fmt.pixelAspect(), media_source.pixelAspect()
        )

        # Validate framerate setting.
        sequence = item.sequence()
        source_framerate = media_source.metadata()["foundry.source.framerate"]
        assert sequence.framerate() == source_framerate, msg.format(
            "framerate", sequence.framerate(), source_framerate
        )


class ValidateNukeStudioTrackItemFtrack(ValidateNukeStudioTrackItem):
    """Validate the track item to the sequence.

    Because we are matching the families exactly, we need this plugin to
    accommodate for the ftrack family addition.
    """
    families = ["trackItem", "ftrack"]
