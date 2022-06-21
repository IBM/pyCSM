class createNewCopyset:
    """
        The createCopyset class can be used to create copysets to be used in
        the add_copysets method in the copysets.py file.
    """

    def __init__(self, copyset):
        """
        Creates a single copyset that can be added to with add_to_copyset
        and used in the add_copysets method in the copysets.py file.

        Args:
            copyset(list): list of host and target volume for a copyset.
            ex. ["DS8000:2107.GXZ91:VOL:D000", "DS8000:2107.GXZ91:VOL:D001"]
        """
        self.copyset = [copyset]

    def get_new_addcopyset(self):
        """
        Gets the list of copysets in the createNewCopyset object.

        Return:
            returns the list of copysets that is self.copyset.
        """
        return self.copyset

    def get_new_removecopyset(self):
        """
        Gets the list of H1 volumes in the copyset object.

        Return:
            returns the list of copysets that is self.copyset.
        """
        result =[]
        for i in self.copyset:
            result.append(i[0])

        return result

    def add_to_new_copyset(self, copyset):
        """
        This method will package all log files on the server into a .jar file

        Args:
            copyset(list): list of host and target volume for a copyset.
            ex.["DS8000:2107.GXZ91:VOL:D000", "DS8000:2107.GXZ91:VOL:D001"]
        """
        temp = copyset
        self.copyset.append(temp)
        return self.copyset
