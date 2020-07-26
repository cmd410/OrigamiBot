class Listener:
    """A helper base class for bots event listeners
    """

    def on_message(self, message):
        """Called upon recieving a message before anything else
        """
        pass

    def on_edited_message(self, message):
        """Called when someone edits a message
        """
        pass

    def on_channel_post(self, message):
        """Called upon recieving a channel post before anything else
        """

    def on_edited_channel_post(self, message):
        """Called when someone edits a channel post"""
        pass

    def on_plain_message(self, message):
        """Called upon recieving a message without commands
        before anything else
        """
        pass

    def on_command_failure(self, message, exception=None):
        """Called when bot fails to execute a command

        Takes message and optional exception
        If no exception provided, bot failed to bind command arguments.
        """
        pass

    def on_left_chat_member(self, message):
        """Called upon recieving a message with
        left_chat_member
        """
        pass

    def on_new_chat_members(self, message):
        """Called upon recieving a message with
        new_chat_members
        """
        pass

    def on_new_chat_title(self, message):
        """Called upon recieving a message with
        new_chat_title
        """
        pass

    def on_group_chat_created(self, message):
        """Called upon recieving a message with
        group_chat_created
        """
        pass

    def on_poll_error(self, exc):
        """Called when get_updates results in connection related
        error
        """
        pass
