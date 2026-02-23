import wx
import wx.adv
import csv
from datetime import datetime

CSV_PATH = "sample.csv" 

# Load bus data
def load_buses(path):
    buses = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                buses.append(row)
    except FileNotFoundError:
        print(f"Error: {path} not found.")
    return buses

def parse_time(t):
    try:
        return datetime.strptime(t.strip(), "%I:%M %p").time()
    except:
        return datetime.strptime("12:00 AM", "%I:%M %p").time()

def parse_duration(d):
    try:
        parts = d.strip().split()
        h = int(parts[0].replace("h", ""))
        m = int(parts[1].replace("m", ""))
        return h * 60 + m
    except:
        return 10**6

class WayfareApp(wx.Frame):
    def __init__(self):
        # Updated Title to "Wayfare"
        super().__init__(None, title="Wayfare | Karnataka Transit Explorer", size=(1180, 780))

        panel = wx.Panel(self)
        panel.SetBackgroundColour(wx.Colour(255, 255, 255)) 

        self.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))

        self.buses = load_buses(CSV_PATH)
        self.sources = sorted({b.get("Departure", "") for b in self.buses})
        self.destinations = sorted({b.get("Destination", "") for b in self.buses})
        ops = sorted({b.get("Bus Name", "") for b in self.buses if b.get("Bus Name")})
        self.operators = ["All Operators"] + ops

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # BRANDING HEADER
        header_sizer = wx.BoxSizer(wx.HORIZONTAL)
        brand_label = wx.StaticText(panel, label="WAYFARE")
        brand_label.SetForegroundColour(wx.Colour(0, 102, 204)) # A nice professional blue
        brand_label.SetFont(wx.Font(14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        
        header_sizer.Add(brand_label, flag=wx.LEFT | wx.TOP, border=20)
        main_sizer.Add(header_sizer, flag=wx.EXPAND)

        # ---------------------------
        # ROUTE FILTER SECTION
        # ---------------------------
        route_label = wx.StaticText(panel, label="ROUTE FILTERS")
        route_label.SetFont(wx.Font(11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        main_sizer.Add(route_label, flag=wx.LEFT | wx.TOP, border=10)

        main_sizer.Add(self.separator(panel), flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=20)

        route_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.src_combo = self.labeled_dropdown(panel, route_sizer, "Source", self.sources)
        self.dst_combo = self.labeled_dropdown(panel, route_sizer, "Destination", self.destinations)
        self.date_picker = self.labeled_date(panel, route_sizer, "Date")

        main_sizer.Add(route_sizer, flag=wx.LEFT | wx.TOP, border=20)

        # ... [Rest of your existing logic remains the same] ...
        # (I've kept the rest of your UI logic below for completeness)

        options_label = wx.StaticText(panel, label="BUS OPTIONS")
        options_label.SetFont(wx.Font(11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        main_sizer.Add(options_label, flag=wx.LEFT | wx.TOP, border=20)
        main_sizer.Add(self.separator(panel), flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=20)

        opt_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.ac_check = wx.CheckBox(panel, label="AC Only")
        self.sleeper_check = wx.CheckBox(panel, label="Sleeper Only")
        opt_sizer.Add(self.ac_check, flag=wx.LEFT | wx.TOP, border=20)
        opt_sizer.Add(self.sleeper_check, flag=wx.LEFT | wx.TOP, border=20)

        self.min_rating = self.labeled_text(panel, opt_sizer, "Min Rating", width=60)
        self.max_fare = self.labeled_text(panel, opt_sizer, "Max Fare", width=80)
        self.sort_choice = self.labeled_dropdown(panel, opt_sizer, "Sort By", [
            "Fare (Low → High)", "Timing (Earliest First)", "Rating (High → Low)", "Duration (Shortest First)"
        ])
        main_sizer.Add(opt_sizer, flag=wx.LEFT | wx.TOP, border=20)

        actions_label = wx.StaticText(panel, label="ACTIONS")
        actions_label.SetFont(wx.Font(11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        main_sizer.Add(actions_label, flag=wx.LEFT | wx.TOP, border=20)
        main_sizer.Add(self.separator(panel), flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=20)

        action_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.search_btn = self.flat_button(panel, "Search", self.on_search)
        self.swap_btn = self.flat_button(panel, "Swap", self.on_swap)
        self.cheapest_btn = self.flat_button(panel, "Cheapest", self.on_cheapest)
        self.fastest_btn = self.flat_button(panel, "Fastest", self.on_fastest)

        action_sizer.Add(self.search_btn, flag=wx.LEFT | wx.TOP, border=20)
        action_sizer.Add(self.swap_btn, flag=wx.LEFT | wx.TOP, border=10)
        action_sizer.Add(self.cheapest_btn, flag=wx.LEFT | wx.TOP, border=10)
        action_sizer.Add(self.fastest_btn, flag=wx.LEFT | wx.TOP, border=10)
        main_sizer.Add(action_sizer)

        self.table = wx.ListCtrl(panel, style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        cols = ["Bus Number", "Operator", "Timing", "Fare (INR)", "Ratings", "Duration", "AC", "Sleeper", "Seats", "From", "To"]
        for i, c in enumerate(cols):
            self.table.InsertColumn(i, c, width=110)

        main_sizer.Add(self.table, proportion=1, flag=wx.EXPAND | wx.ALL, border=20)
        self.table.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.on_item_activated)

        panel.SetSizer(main_sizer)
        self.Center()
        self.Show()

    # --- UI HELPERS & SEARCH LOGIC (Same as your original code) ---
    def separator(self, parent):
        line = wx.StaticLine(parent, style=wx.LI_HORIZONTAL)
        line.SetBackgroundColour(wx.Colour(220, 220, 220))
        return line

    def flat_button(self, parent, label, handler):
        btn = wx.Button(parent, label=label, style=wx.BORDER_NONE)
        btn.SetBackgroundColour(wx.Colour(245, 245, 245))
        btn.Bind(wx.EVT_BUTTON, handler)
        return btn

    def labeled_dropdown(self, parent, sizer, label, choices):
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(wx.StaticText(parent, label=label))
        dd = wx.ComboBox(parent, choices=choices, style=wx.CB_READONLY, size=(200, -1))
        box.Add(dd, flag=wx.TOP, border=5)
        sizer.Add(box, flag=wx.LEFT, border=20)
        return dd

    def labeled_date(self, parent, sizer, label):
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(wx.StaticText(parent, label=label))
        dp = wx.adv.DatePickerCtrl(parent)
        box.Add(dp, flag=wx.TOP, border=5)
        sizer.Add(box, flag=wx.LEFT, border=20)
        return dp

    def labeled_text(self, parent, sizer, label, width):
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(wx.StaticText(parent, label=label))
        tc = wx.TextCtrl(parent, size=(width, -1))
        box.Add(tc, flag=wx.TOP, border=5)
        sizer.Add(box, flag=wx.LEFT, border=20)
        return tc

    def on_search(self, evt):
        src = self.src_combo.GetValue().strip().lower()
        dst = self.dst_combo.GetValue().strip().lower()
        date_iso = self.date_picker.GetValue().FormatISODate()
        weekday = datetime.strptime(date_iso, "%Y-%m-%d").strftime("%A")
        
        ac_only = self.ac_check.GetValue()
        sleeper_only = self.sleeper_check.GetValue()
        min_rating = self.min_rating.GetValue()
        max_fare = self.max_fare.GetValue()

        results = []
        for b in self.buses:
            if src and b["Departure"].lower() != src: continue
            if dst and b["Destination"].lower() != dst: continue
            if weekday not in b["Day of Departure"]: continue
            if ac_only and b["AC"].lower() != "yes": continue
            if sleeper_only and b["Sleeper"].lower() != "yes": continue
            if min_rating and float(b["Ratings"]) < float(min_rating): continue
            if max_fare and int(b["Fare (INR)"]) > int(max_fare): continue
            results.append(b)
        
        # Simple Sort Example
        sort_idx = self.sort_choice.GetSelection()
        if sort_idx == 0: results.sort(key=lambda x: int(x["Fare (INR)"]))
        
        self.filtered = results
        self.populate_table(results)

    def populate_table(self, results):
        self.table.DeleteAllItems()
        for b in results:
            idx = self.table.InsertItem(self.table.GetItemCount(), b["Bus Number"])
            self.table.SetItem(idx, 1, b["Bus Name"])
            self.table.SetItem(idx, 2, b["Timing"])
            self.table.SetItem(idx, 3, b["Fare (INR)"])
            self.table.SetItem(idx, 4, b["Ratings"])
            self.table.SetItem(idx, 5, b["Duration"])
            self.table.SetItem(idx, 6, b["AC"])
            self.table.SetItem(idx, 7, b["Sleeper"])
            self.table.SetItem(idx, 8, b["Seats"])
            self.table.SetItem(idx, 9, b["Departure"])
            self.table.SetItem(idx, 10, b["Destination"])

    def on_swap(self, evt):
        s, d = self.src_combo.GetValue(), self.dst_combo.GetValue()
        self.src_combo.SetValue(d), self.dst_combo.SetValue(s)

    def on_cheapest(self, evt):
        if self.filtered:
            cheapest = min(self.filtered, key=lambda x: int(x["Fare (INR)"]))
            self.populate_table([cheapest])

    def on_fastest(self, evt):
        if self.filtered:
            fastest = min(self.filtered, key=lambda x: parse_duration(x["Duration"]))
            self.populate_table([fastest])

    def on_item_activated(self, evt):
        # Placeholder for your detailed dialog logic
        pass

if __name__ == "__main__":
    app = wx.App(False)
    WayfareApp()
    app.MainLoop()
