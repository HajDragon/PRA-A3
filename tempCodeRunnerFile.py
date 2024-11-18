import wx
import csv

class MovieAnalyzerApp(wx.Frame):
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

        header = wx.StaticText(panel, label="🎬 Movie Analyzer 🎬")
        header.SetFont(header_font)
        header.SetForegroundColour(neon_purple)
        vbox.Add(header, flag=wx.ALIGN_CENTER | wx.TOP, border=20)

        dropdown_box = wx.BoxSizer(wx.HORIZONTAL)

        self.genre_choice = wx.Choice(panel, choices=["Any", "Thriller", "Drama", "Comedy", "Romantisch", "SciFi", "Rom-com", "Waargebeurd", "Actie", "Historisch"])
        self.genre_choice.SetSelection(0)
        self.availability_choice = wx.Choice(panel, choices=["Any", "Yes", "No"])
        self.availability_choice.SetSelection(0)
        self.reservation_choice = wx.Choice(panel, choices=["Any", "Yes", "No"])
        self.availability_choice.SetSelection(0)
        self.reservation_choice = wx.Choice(panel, choices=["Any", "Yes", "No"])
        self.reservation_choice.SetSelection(0)

        def create_label(text, color=neon_pink):
            label = wx.StaticText(panel, label=text, style=wx.ALIGN_CENTER_VERTICAL)
            label.SetFont(label_font)
            label.SetForegroundColour(color)
            return label

        dropdown_box.Add(create_label("Genre:"), flag=wx.RIGHT, border=5)
        dropdown_box.Add(self.genre_choice, flag=wx.RIGHT, border=20)
        dropdown_box.Add(create_label("Available:"), flag=wx.RIGHT, border=5)
        dropdown_box.Add(self.availability_choice, flag=wx.RIGHT, border=20)
        dropdown_box.Add(create_label("Reserved:"), flag=wx.RIGHT, border=5)
        dropdown_box.Add(self.reservation_choice)

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

        footer = wx.StaticText(panel, label="🎥 Powered by Arshia, Rares © 2077 🎥")
        footer.SetForegroundColour(neon_blue)
        footer.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_LIGHT))
        vbox.Add(footer, flag=wx.ALIGN_CENTER | wx.BOTTOM, border=10)

        panel.SetSizer(vbox)

    def on_search(self, event):
        genre = self.genre_choice.GetStringSelection()
        available = self.availability_choice.GetStringSelection()
        reserved = self.reservation_choice.GetStringSelection()

        try:
            with open('BF.csv', mode='r', encoding='latin-1') as file:
                reader = csv.DictReader(file, delimiter=';')

                total_count = 0
                available_count = 0
                reserved_count = 0

                results = []

                for row in reader:
                    if (
                        (genre == "Any" or row['genre'] == genre) and
                        (available == "Any" or (available == "Yes" and row['beschikbaar'] != "0") or (available == "No" and row['beschikbaar'] == "0")) and
                        (reserved == "Any" or (reserved == "Yes" and row['gereserveerd'] == "Ja") or (reserved == "No" and row['gereserveerd'] == "Nee"))
                    ):
                        total_count += 1
                        if row['beschikbaar'] != "0":
                            available_count += 1
                        if row['gereserveerd'] == "Ja":
                            reserved_count += 1
                        results.append(row['movieTitle'])

                output_str = (
                    f"Total movies found: {total_count}\n"
                    f"Movies available: {available_count}\n"
                    f"Movies reserved: {reserved_count}\n\n"
                    "Movie Titles:\n" + "\n".join(results)
                )

                self.output_text.SetValue(output_str)

        except FileNotFoundError:
            self.output_text.SetValue("Error: BF.csv file not found.")
        except Exception as e:
            self.output_text.SetValue(f"Error: {str(e)}")

if __name__ == "__main__":
    app = wx.App(False)
    frame = MovieAnalyzerApp(None, "Movie Analyzer")
    frame.Show()
    app.MainLoop()
