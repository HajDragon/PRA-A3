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
        self.reservation_choice.SetSelection(0)
        self.yrear_choice = wx.Choice(panel, choices=["Any", "2023", "2022", "2021", "2020", "2019", "2018", "2017", "2016", "2015", "2014", "2013", "2012", "2011", "2010", "2009", "2008", "2007", "2006", "2005", "2004", "2003", "2002", "2001", "2000", "1999", "1998", "1997", "1996", "1995", "1994", "1993", "1992", "1991", "1990", "1989", "1988", "1987", "1986", "1985", "1984"])
        self.yrear_choice.SetSelection(0)

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
        dropdown_box.Add(create_label("Year:"), flag=wx.RIGHT, border=5)
        dropdown_box.Add(self.yrear_choice)

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
        year = self.yrear_choice.GetStringSelection()  # Get selected year

        try:
            with open('BF.csv', mode='r', encoding='latin-1') as file:
                reader = csv.DictReader(file, delimiter=';')

                total_count = 0
                available_count = 0
                reserved_count = 0
                long_movies_count = 0
                thriller_count = 0
                movie_rent_count = {}
                results = []
                available_movies = []
                year_count = 0  # Variable to track the count of movies for the selected year

                for row in reader:
                    # Get release year as string (if it’s a number, it will be treated as a string)
                    movie_year = row['release']
                    if year != "Any" and movie_year != year:  # If a specific year is selected, filter accordingly
                        continue

                    if (
                        (genre == "Any" or row['genre'] == genre) and
                        (available == "Any" or (available == "Yes" and row['beschikbaar'] != "0") or (available == "No" and row['beschikbaar'] == "0")) and
                        (reserved == "Any" or (reserved == "Yes" and row['gereserveerd'] == "Ja") or (reserved == "No" and row['gereserveerd'] == "Nee"))
                    ):
                        total_count += 1
                        movie_title = row['movieTitle']

                        # Count availability
                        if row['beschikbaar'] != "0":
                            available_count += 1
                            available_movies.append(movie_title)
                        if row['gereserveerd'] == "Ja":
                            reserved_count += 1

                        # Track rent count (for 2020)
                        uitgeleend_2020 = int(row['uitgeleend_2020']) if row['uitgeleend_2020'].isdigit() else 0
                        if movie_title not in movie_rent_count:
                            movie_rent_count[movie_title] = uitgeleend_2020
                        else:
                            movie_rent_count[movie_title] += uitgeleend_2020

                        # Count long movies (longer than 180 mins)
                        if int(row['duration (mins)']) > 180:
                            long_movies_count += 1

                        # Count thrillers
                        if row['genre'] == "Thriller":
                            thriller_count += 1

                        # Count movies for the selected year
                        if year != "Any" and movie_year == year:
                            year_count += 1

                        results.append(row['movieTitle'])

                # Calculate average rental for a genre
                genre_rentals = [uitgeleend_2020 for title, uitgeleend_2020 in movie_rent_count.items() if genre == "Any" or title.startswith(genre)]
                avg_rentals = sum(genre_rentals) / len(genre_rentals) if genre_rentals else 0

                # Top 10 most rented movies
                top_rented_movies = sorted(movie_rent_count.items(), key=lambda x: x[1], reverse=True)[:10]

                output_str = (
                    f"🔎 **Search Results:** 🔎\n\n"
                    f"📊 **Total movies found:** {total_count}\n"
                    f"🎬 **Movies available:** {available_count}\n"
                    f"📚 **Movies reserved:** {reserved_count}\n"
                    f"⏳ **Movies longer than 3 hours:** {long_movies_count}\n"
                    f"🎥 **Thriller movies:** {thriller_count}\n"
                    f"📈 **Average rentals for {genre} genre:** {avg_rentals:.2f}\n\n"
                    f"🎬 **Top 10 rented movies:**\n"
                    f"{', '.join([f'{movie[0]} ({movie[1]} rentals)' for movie in top_rented_movies])}\n\n"
                    f"📅 **Movies from {year}:** {year_count}\n\n"
                    f"📀 **Available movie list:**\n"
                    f"{', '.join(available_movies)}"
                )

                self.output_text.SetValue(output_str)

        except Exception as e:
            self.output_text.SetValue(f"Error: {str(e)}")


if __name__ == "__main__":
    app = wx.App(False)
    frame = MovieAnalyzerApp(None, title="Movie Analyzer")
    frame.Show()
    app.MainLoop()
