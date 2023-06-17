class SingleJobData:
    def __init__(self):
        self.video_name = ""
        self.video_name_with_spaces = "  "
        self.video_name_after_elide = "..."
        self.video_name_displayed = ""
        self.video_name_absolute = ""

        self.subtitle_found = False
        self.subtitle_name = []
        self.subtitle_name_absolute = []
        self.subtitle_language = []
        self.subtitle_track_name = []
        self.subtitle_delay = []
        self.subtitle_set_default = []
        self.subtitle_set_forced = []
        self.subtitle_set_at_top = []

        self.audio_found = False
        self.audio_name = []
        self.audio_name_absolute = []
        self.audio_language = []
        self.audio_track_name = []
        self.audio_delay = []
        self.audio_set_default = []
        self.audio_set_forced = []
        self.audio_set_at_top = []

        self.chapter_found = False
        self.chapter_name = ""
        self.chapter_name_absolute = ""

        self.attachments_absolute_path = []
        self.discard_old_attachments = False
        self.allow_duplicates_attachments = False

        self.output_video_name = ""
        self.output_video_absolute_path = ""

        self.is_crc_calculating_required = False
        self.is_crc_removing_required = False
        self.progress_crc = 0
        self.progress = 0
        self.size_before_muxing = "0 MB"
        self.size_after_muxing = "0 MB"

        self.done = False
        self.error_occurred = False
        self.used_mkvpropedit = False
        self.muxing_message = ""
        self.new_crc = ""
