class PlaybackControlActions:
    def __init__(self):

        self.playback_control_commands = {
            "Play": self.play_control_action,
            "Pause": self.pause_control_action,
            "Skip backward": self.skip_backwards_control_action,
            "Skip forward": self.skip_forwards_control_action,
        }

    def play_control_action(self):
        pass

    def pause_control_action(self):
        pass

    def skip_backwards_control_action(self):
        pass

    def skip_forwards_control_action(self):
        pass
