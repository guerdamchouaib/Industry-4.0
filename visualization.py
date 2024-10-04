class DetectionHistory:
    def __init__(self):
        self.history = []

    def add_detection(self, detection_info):
        self.history.append(detection_info)

    def get_history(self):
        return self.history

class DefectCategoryChart:
    def __init__(self):
        self.categories = {"NG": 0, "OK": 0}

    def update_chart(self, category):
        if category in self.categories:
            self.categories[category] += 1

    def get_chart_data(self):
        return self.categories
