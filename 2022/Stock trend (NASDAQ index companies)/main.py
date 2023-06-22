from pandas import Series
from get_data import get_nasdaq_index, get_company_data
import mplfinance as mpf

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.popup import Popup


def analyze_company_data(df):
    mpf.plot(df, type='candle' if len(df) <= 200 else 'line', mav=(12, 26), volume=True, style='yahoo')


class InputScreen(BoxLayout):
    PER_PAGE = 150
    COMPANIES_DF = get_nasdaq_index()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.show_new_df(self.COMPANIES_DF)
    
        # Create country and sector filters
        self.filter_widgets = {}
        def country_and_sector(title):
            widgets = []
            for name in sorted(self.df[title].drop_duplicates().dropna().values):
                checkbox = CheckBox(size_hint_x=.2)
                label = Label(text=name, halign='left', height='20dp')
                label.text_size = label.size
                box = BoxLayout(size_hint_y=None, height='20dp')
                box.add_widget(checkbox)
                box.add_widget(label)
                self.ids[title.lower() + '_filters_container'].add_widget(box)
                widgets.append(box.children)
            self.filter_widgets[title] = widgets
        country_and_sector('Country')
        country_and_sector('Sector')
        
    def show_new_df(self, df):
        # Define the new dataframe
        self.df = df

        # Create new indexes and pages
        self.current_page_idx = 0
        self.indexes = []
        self.pages = [ScrollViewContainer()]
        
        rows_amount = self.df.shape[0]

        for idx in range(self.PER_PAGE, rows_amount, self.PER_PAGE):
            self.indexes.append((idx-self.PER_PAGE, idx))
            self.pages.append(ScrollViewContainer())
        self.indexes.append((rows_amount - rows_amount%self.PER_PAGE, rows_amount))

        self.go_to_page(self.current_page_idx)

    def go_to_page(self, page_idx):
        # Remove current page
        old_page = self.ids.page_container.children[0]
        self.ids.page_container.remove_widget(old_page)
        
        # Load new page widgets
        start_idx = self.indexes[page_idx][0]
        end_idx = self.indexes[page_idx][1]
        symbols_list = self.df.iloc[start_idx:end_idx].index
        
        for symbol in symbols_list:
            name = self.df.loc[symbol].Name
            self.pages[page_idx].add_widget(CompanyWidget(symbol, name))
        
        # Add page
        self.ids.page_container.add_widget(self.pages[page_idx])
        self.current_page_idx = page_idx

        # Set disabled property for previous and next page buttons
        self.ids.previous_page_btn.disabled = self.current_page_idx == 0
        self.ids.next_page_btn.disabled = self.current_page_idx  == len(self.pages) - 1

        # Set page info
        self.ids.page_info_label.text = f'Page {page_idx} of {len(self.pages)}'

        # Scroll up if there are companies
        if symbols_list.any():
            self.ids.page_container.scroll_to(self.pages[page_idx].children[-1])

    def apply_filters(self):
        new_df = self.COMPANIES_DF
        
        # Search bar
        def search_bar(df):
            msg = self.ids.search_bar.text
            if not msg:
                return
            pattern = f'(?:{msg.replace(" ", "|")})'
            return (df['Name'].str.contains(pattern, case=False)) | (df.index.str.contains(pattern, case=False))

        # Market cap
        def market_cap(min_or_max:str, df):
            txt_input_value = self.ids[min_or_max + '_marketcap'].text
            if not txt_input_value:
                return
            value = int(txt_input_value)
            if min_or_max == 'min':
                return df['Market Cap'] >= value
            if min_or_max == 'max':
                return (df['Market Cap'] <= value) & (df['Market Cap'] > 0)

        # Country
        def country_and_sector(title, df):
            keywords = [label.text for label, checkbox in self.filter_widgets[title] if checkbox.active]
            if not keywords:
                return
            pattern = f'(?:{"|".join(keywords)})'
            return df[title].str.contains(pattern)
        
        # Get the filters
        filter_series = list(filter(lambda s: type(s) == Series, [
            search_bar(new_df),
            market_cap("min", new_df), 
            market_cap("max", new_df), 
            country_and_sector("Country", new_df), 
            country_and_sector("Sector", new_df),
        ]))
        # Return the complete companies list if there are no filters
        if not filter_series:
            return self.show_new_df(new_df) 

        # Otherwise, get and then show the new filtered dataframe
        super_filter = filter_series[0]
        for fs in filter_series:
            super_filter = super_filter & fs
        new_df = new_df[super_filter]
        self.show_new_df(new_df)


class CompanyWidget(BoxLayout):
    symbol = StringProperty()
    name = StringProperty()
    
    def __init__(self, symbol, name, **kwargs):
        super().__init__(**kwargs)
        self.symbol = symbol
        self.name = name


class TimePeriodPopup(Popup):
    TIME_PERIODS = 'M1', 'M6', 'YTD', 'Y1', 'Y5', 'Y10'
    time_period_selected = StringProperty()

    def __init__(self, symbol, **kwargs):
        super().__init__(**kwargs)
        self.symbol = symbol

        # Create labels and radio buttons
        for time_period in self.TIME_PERIODS:
            label = Label(text=time_period)
            radio_btn = CheckBox(group='time_period_radio_btn')
            radio_btn.bind(active=self.radio_btn_pressed)
            box = BoxLayout(orientation='vertical')
            box.add_widget(label)
            box.add_widget(radio_btn)
            self.ids.radio_btns_layout.add_widget(box)

    def radio_btn_pressed(self, instance, value):
        self.time_period_selected = instance.parent.children[1].text if value else ''

    def done_btn_pressed(self):
        self.dismiss()
        analyze_company_data(get_company_data(self.symbol, self.time_period_selected))


class FiltersWidget(BoxLayout):
    title = StringProperty()


class ScrollViewContainer(BoxLayout): 
    None


class MainApp(App):
    title = 'Stock Trend (NASDAQ)'
    def build(self):
        return InputScreen()


if __name__ == '__main__':
    MainApp().run()
