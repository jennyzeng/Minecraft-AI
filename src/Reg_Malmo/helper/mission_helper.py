import os

class MissionHelper:

    @staticmethod
    def get_parent_path(cur_path):
        return os.path.abspath(os.path.join(cur_path, os.pardir))

    @staticmethod
    def get_grand_parent_path(cur_path):
        parent_path= MissionHelper.get_parent_path(cur_path)
        grand_parent_path = MissionHelper.get_parent_path(parent_path)
        return grand_parent_path
