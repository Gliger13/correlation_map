class UserActions:
    def __init__(self):
        self.progress = 0
        self.image1_path = None
        # Select region of image1
        self.x1 = None
        self.y1 = None
        self.x2 = None
        self.y2 = None

        self.image2_path = None
        # Type of correlation
        self.correlation = None
        # Image process
        self.flag_autorotate = False
        self.flag_select = False
        self.flag_find = False
        # Images to show
        self.show_src = False
        self.show_src_sel = False
        self.show_new = False
        self.show_new_rot = False
        self.show_new_find = False
        self.show_new_sel = False
        self.show_detected = False
        self.show_correlation_map = False

    def reset_choices(self):
        self.correlation = None
        # Image process
        self.flag_autorotate = False
        self.flag_select = False
        self.flag_find = False
        # Images to show
        self.show_src = False
        self.show_src_sel = False
        self.show_new = False
        self.show_new_rot = False
        self.show_new_find = False
        self.show_new_sel = False
        self.show_detected = False
        self.show_correlation_map = False
