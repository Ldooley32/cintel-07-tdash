# import requirements 
import seaborn as sns
from faicons import icon_svg

from shiny import reactive
from shiny.express import input, render, ui
from shinywidgets import render_plotly
import plotly.express as px
import palmerpenguins 

#define penguin dataset
df = palmerpenguins.load_penguins()

# add page title
ui.page_opts(title="LDooley's Penguins dashboard", fillable=True)

# Create sidebar with Mass slider and Species check boxes.
with ui.sidebar(title="Penguins Mass / Species Option Controls "):
    ui.input_slider("mass", "Mass", 2000, 6000, 6000)
    ui.input_checkbox_group(
        "species",
        "Species",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo", "Chinstrap"],
    )

# create a space to add a header for resource links to GitHub, PyShiny, etc.
    ui.hr()
    ui.h6("Resource Links")
    ui.a(
        "GitHub Source",
        href="https://github.com/denisecase/cintel-07-tdash",
        target="_blank",
    )
    ui.a(
        "GitHub App",
        href="https://denisecase.github.io/cintel-07-tdash/",
        target="_blank",
    )
    ui.a(
        "GitHub Issues",
        href="https://github.com/denisecase/cintel-07-tdash/issues",
        target="_blank",
    )
    ui.a("PyShiny", href="https://shiny.posit.co/py/", target="_blank")
    ui.a(
        "Template: Basic Dashboard",
        href="https://shiny.posit.co/py/templates/dashboard/",
        target="_blank",
    )
    ui.a(
        "See also",
        href="https://github.com/denisecase/pyshiny-penguins-dashboard-express",
        target="_blank",
    )

# Creating value boxes for penguin count, average bill length, and average bill mass using filtered df.
with ui.layout_column_wrap(fill=False):
    with ui.value_box(showcase=icon_svg("earlybirds")):
        "Number of penguins"

        @render.text
        def count():
            return filtered_df().shape[0]

    with ui.value_box(showcase=icon_svg("ruler-horizontal")):
        "Average bill length"

        @render.text
        def bill_length():
            return f"{filtered_df()['bill_length_mm'].mean():.1f} mm"

    with ui.value_box(showcase=icon_svg("ruler-vertical")):
        "Average bill depth"

        @render.text
        def bill_depth():
            return f"{filtered_df()['bill_depth_mm'].mean():.1f} mm"

# Create an interactive Plotly histogram for penguin mass using the filtered_df.
with ui.layout_columns():
    with ui.card(full_screen=True):
        ui.card_header("Bill length and depth")

        @render_plotly
        def hist():
            histogram = px.histogram(
                filtered_df(),
                x="body_mass_g",
                color="species",
                labels={"body_mass_g": "Body Mass (g)"},
                nbins=input.mass(),  # Use the input from the mass slider
            )
            return histogram

# Create a data grid using the filtered_df to select information for display.
with ui.card(full_screen=True):
    ui.card_header("Penguin data")

    @render.data_frame
    def summary_statistics():
        cols = [
            "species",
            "island",
            "bill_length_mm",
            "bill_depth_mm",
            "body_mass_g",
        ]
        return render.DataGrid(filtered_df()[cols], filters=True)

# Define reactive calc to include the mass slider and the species checkboxes.
@reactive.calc
def filtered_df():
    filt_df = df[df["species"].isin(input.species())]
    filt_df = filt_df.loc[filt_df["body_mass_g"] < input.mass()]
    return filt_df
