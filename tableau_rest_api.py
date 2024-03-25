import requests
import os
import csv

class TableauAPI:
    def __init__(self, server_url, username, password):
        self.server_url = server_url
        self.username = username
        self.password = password
        self.token = None

    def login(self):
        login_url = f"{self.server_url}/api/3.5/auth/signin"
        payload = {
            "credentials": {
                "name": self.username,
                "password": self.password,
                "site": {
                    "contentUrl": ""
                }
            }
        }
        response = requests.post(login_url, json=payload)
        if response.status_code == 200:
            self.token = response.json()["credentials"]["token"]
            print("Login successful.")
        else:
            print("Login failed.")

    def logout(self):
        logout_url = f"{self.server_url}/api/3.5/auth/signout"
        headers = {"X-Tableau-Auth": self.token}
        response = requests.post(logout_url, headers=headers)
        if response.status_code == 204:
            print("Logout successful.")
            self.token = None
        else:
            print("Logout failed.")

    def set_project(self, project_name):
        projects_url = f"{self.server_url}/api/3.5/sites/{self.username}/projects"
        headers = {"X-Tableau-Auth": self.token, "Content-Type": "application/json"}
        response = requests.get(projects_url, headers=headers)
        projects = response.json()["projects"]["project"]
        project_id = None
        for project in projects:
            if project["name"] == project_name:
                project_id = project["id"]
                break
        if project_id:
            print(f"Project '{project_name}' found.")
            return project_id
        else:
            print(f"Project '{project_name}' not found.")

    def get_workbooks(self):
        workbooks_url = f"{self.server_url}/api/3.5/sites/{self.username}/workbooks"
        headers = {"X-Tableau-Auth": self.token}
        response = requests.get(workbooks_url, headers=headers)
        workbooks = response.json()["workbooks"]["workbook"]
        workbook_names = [workbook["name"] for workbook in workbooks]
        return workbook_names

    def get_views(self, workbook_id):
        views_url = f"{self.server_url}/api/3.5/sites/{self.username}/workbooks/{workbook_id}/views"
        headers = {"X-Tableau-Auth": self.token}
        response = requests.get(views_url, headers=headers)
        views = response.json()["views"]["view"]
        view_names = [view["name"] for view in views]
        return view_names

    def download_view_image(self, view_id, file_name):
        image_url = f"{self.server_url}/api/3.5/sites/{self.username}/views/{view_id}/image"
        headers = {"X-Tableau-Auth": self.token}
        response = requests.get(image_url, headers=headers)
        if response.status_code == 200:
            with open(f"{file_name}.png", "wb") as f:
                f.write(response.content)
            print(f"View image downloaded as '{file_name}.png'.")
        else:
            print("Failed to download view image.")

    def download_view_dataset_csv(self, view_id, file_name):
        csv_url = f"{self.server_url}/api/3.5/sites/{self.username}/views/{view_id}/data"
        headers = {"X-Tableau-Auth": self.token}
        response = requests.get(csv_url, headers=headers)
        if response.status_code == 200:
            with open(f"{file_name}.csv", "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerows(response.json()["data"])
            print(f"View dataset downloaded as '{file_name}.csv'.")
        else:
            print("Failed to download view dataset CSV.")

# Example usage
if __name__ == "__main__":
    tableau = TableauAPI("https://your-tableau-server.com", "username", "password")
    tableau.login()
    project_id = tableau.set_project("Sample Project")
    if project_id:
        print("Workbooks in Sample Project:")
        print(tableau.get_workbooks())
        # Assume you choose the first workbook for further operations
        workbook_id = "workbook_id"  # You need to replace this with the actual workbook id
        print(f"Views in Workbook '{workbook_id}':")
        print(tableau.get_views(workbook_id))
        # Assume you choose the first view for further operations
        view_id = "view_id"  # You need to replace this with the actual view id
        tableau.download_view_image(view_id, "view_image")
        tableau.download_view_dataset_csv(view_id, "view_dataset")
    tableau.logout()
