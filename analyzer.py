import wx
import csv
import random


def generate_csv():
    roles = ["Developer", "Designer", "Manager", "Analyst"]
    countries = ["USA", "Canada", "Germany", "netherlands"]
    seniority = ["Junior", "Senior"]
    salary_types = ["Hourly", "Yearly"]

    with open('employee_data.csv', mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["Serial", "Salary", "SalaryType", "JobRole", "Country", "Seniority"])
        writer.writeheader()

        for i in range(1, 501):
            salary_type = random.choice(salary_types)
            salary = random.randint(15, 150) if salary_type == "Hourly" else random.randint(30000, 150000)
            writer.writerow({
                "Serial": i,
                "Salary": salary,
                "SalaryType": salary_type,
                "JobRole": random.choice(roles),
                "Country": random.choice(countries),
                "Seniority": random.choice(seniority),
            })


class SalaryAnalyzerApp(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(900, 650))

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        bg_color = "#0a0f29"
        neon_blue = "#00ffff"
        neon_pink = "#ff007f"
        neon_purple = "#bf5fff"

        panel.SetBackgroundColour(bg_color)

        header_font = wx.Font(22, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        label_font = wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        output_font = wx.Font(11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)

        header = wx.StaticText(panel, label="⚡ Salary Analyzer ⚡")
        header.SetFont(header_font)
        header.SetForegroundColour(neon_purple)
        vbox.Add(header, flag=wx.ALIGN_CENTER | wx.TOP, border=20)

        dropdown_box = wx.BoxSizer(wx.HORIZONTAL)

        self.salary_type_choice = wx.Choice(panel, choices=["Any", "Hourly", "Yearly"])
        self.salary_type_choice.SetSelection(0)
        self.role_choice = wx.Choice(panel, choices=["Any", "Developer", "Designer", "Manager", "Analyst"])
        self.role_choice.SetSelection(0)
        self.country_choice = wx.Choice(panel, choices=["Any", "USA", "Canada", "Germany", "netherlands"])
        self.country_choice.SetSelection(0)
        self.level_choice = wx.Choice(panel, choices=["Any", "Junior", "Senior"])
        self.level_choice.SetSelection(0)

        def create_label(text, color=neon_pink):
            label = wx.StaticText(panel, label=text, style=wx.ALIGN_CENTER_VERTICAL)
            label.SetFont(label_font)
            label.SetForegroundColour(color)
            return label

        dropdown_box.Add(create_label("Salary Type:"), flag=wx.RIGHT, border=5)
        dropdown_box.Add(self.salary_type_choice, flag=wx.RIGHT, border=20)
        dropdown_box.Add(create_label("Job Role:"), flag=wx.RIGHT, border=5)
        dropdown_box.Add(self.role_choice, flag=wx.RIGHT, border=20)
        dropdown_box.Add(create_label("Country:"), flag=wx.RIGHT, border=5)
        dropdown_box.Add(self.country_choice, flag=wx.RIGHT, border=20)
        dropdown_box.Add(create_label("Seniority:"), flag=wx.RIGHT, border=5)
        dropdown_box.Add(self.level_choice)

        for child in dropdown_box.GetChildren():
            dropdown = child.GetWindow()
            if dropdown:
                dropdown.SetBackgroundColour("#1a1f3b")
                dropdown.SetForegroundColour(neon_blue)
                dropdown.SetFont(label_font)

        vbox.Add(dropdown_box, flag=wx.EXPAND | wx.ALL, border=20)

        search_button = wx.Button(panel, label="🔍 Search", size=(150, 50))
        search_button.SetFont(wx.Font(14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        search_button.SetBackgroundColour(neon_pink)
        search_button.SetForegroundColour("black")
        search_button.Bind(wx.EVT_BUTTON, self.on_search)
        vbox.Add(search_button, flag=wx.ALIGN_CENTER | wx.ALL, border=10)

        self.output_text = wx.TextCtrl(
        panel, 
        style=wx.TE_MULTILINE | wx.TE_READONLY,
        size=(800, 300)
        )
        self.output_text.SetBackgroundColour("#1a1f3b")
        self.output_text.SetForegroundColour("white")
        self.output_text.SetFont(output_font)

        vbox.Add(self.output_text, proportion=1, flag=wx.EXPAND | wx.ALL, border=20)

        footer = wx.StaticText(panel, label="⚡ Powered by Arshia, Rares  © 2077 ⚡")
        footer.SetForegroundColour(neon_blue)
        footer.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_LIGHT))
        vbox.Add(footer, flag=wx.ALIGN_CENTER | wx.BOTTOM, border=10)

        panel.SetSizer(vbox)

    def on_search(self, event):
        salary_type = self.salary_type_choice.GetStringSelection()
        role = self.role_choice.GetStringSelection()
        country = self.country_choice.GetStringSelection()
        level = self.level_choice.GetStringSelection()

        results = []

        with open('employee_data.csv', mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if (
                    (salary_type == "Any" or row['SalaryType'] == salary_type) and
                    (role == "Any" or row['JobRole'] == role) and
                    (country == "Any" or row['Country'] == country) and
                    (level == "Any" or row['Seniority'] == level)
                ):
                    serial = row['Serial']
                    salary = float(row['Salary'])
                    salary_type = row['SalaryType']

                    if salary_type == "Hourly":
                        yearly_salary = salary * 40 * 52
                        results.append(
                            f"Serial Number: {serial}, Salary per hour is {salary}, "
                            f"which translates to approximately {yearly_salary:.2f} per year."
                        )
                    elif salary_type == "Yearly":
                        hourly_salary = salary / (40 * 52)
                        results.append(
                            f"Serial Number: {serial}, Salary per year is {salary}, "
                            f"which translates to approximately {hourly_salary:.2f} per hour."
                        )

        if results:
            self.output_text.SetValue("\n".join(results))
        else:
            self.output_text.SetValue("No matching data found.")


if __name__ == "__main__":
    generate_csv()

    app = wx.App(False)
    frame = SalaryAnalyzerApp(None, "Salary Analyzer")
    frame.Show()
    app.MainLoop()
