from packages.Startup.DefaultOptions import Default_Subtitle_Language


class SingleJobData:
    def __init__(self):
        self.video_name = ""
        self.video_name_with_spaces = "  "
        self.video_name_after_elide = "..."
        self.video_name_displayed = ""
        self.video_name_absolute = ""

        self.subtitle_found = False
        self.subtitle_name = ""
        self.subtitle_name_absolute = ""
        self.subtitle_language = Default_Subtitle_Language
        self.subtitle_track_name = ""
        self.subtitle_delay = 0.0
        self.subtitle_set_default = False
        self.subtitle_set_forced = False

        self.chapter_found = False
        self.chapter_name = ""
        self.chapter_name_absolute = ""

        self.progress = 0
        self.size_before_muxing = "0 MB"
        self.size_after_muxing = "0 MB"

        self.done = False
        self.error_occurred = False
        self.used_mkvpropedit = False
        self.muxing_message = ""
