import pandas as pd
import os

class DataLoader:
    def __init__(self, data_path="data/"):
        self.data_path = data_path

    def load_it_solutions_data(self):
        """Load IT solutions data"""
        try:
            return pd.read_csv(os.path.join(self.data_path, "it_solutions.csv"))
        except FileNotFoundError:
            print("File not found. Please check the file path and try again.")

    def load_hr_staffing_data(self):
        """Load HR staffing data"""
        try:
            return pd.read_csv(os.path.join(self.data_path, "hr_staffing.csv"))
        except FileNotFoundError:
            print("File not found. Please check the file path and try again.")

    def load_consulting_data(self):
        """Load business consulting data"""
        try:
            return pd.read_csv(os.path.join(self.data_path, "business_consulting.csv"))
        except FileNotFoundError:
            print("File not found. Please check the file path and try again.")

    def load_ai_services_data(self):
        """Load AI services data"""
        try:
            return pd.read_csv(os.path.join(self.data_path, "data_ai_services.csv"))
        except FileNotFoundError:
            print("File not found. Please check the file path and try again.")