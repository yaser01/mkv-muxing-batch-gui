from PySide6.QtWidgets import QLabel


class CompletedJobsCounter(QLabel):
    def __init__(self):
        super().__init__()
        self.number_of_jobs = 0
        self.number_of_completed_jobs = 0
        self.update_text()

    def initiate_number_of_jobs(self, value):
        self.number_of_jobs = value
        self.number_of_completed_jobs = 0
        self.update_text()

    def set_number_of_jobs(self, value):
        self.number_of_jobs = value
        self.update_text()

    def increase_completed_jobs(self):
        self.number_of_completed_jobs += 1
        self.update_text()

    def set_number_of_completed_jobs(self, value):
        self.number_of_completed_jobs = value
        self.update_text()

    def update_text(self):
        self.setText("Completed : " + str(self.number_of_completed_jobs) + "/" + str(self.number_of_jobs))
