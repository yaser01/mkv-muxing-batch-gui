from packages.Startup.MainApplication import MainApplication

app_for_screen_resolution = MainApplication
screen = app_for_screen_resolution.primaryScreen()
screen_size = screen.size()
logic_dpi = screen.logicalDotsPerInch()
physic_dpi = screen.physicalDotsPerInch()
width_factor = screen_size.width() / 1366
height_factor = screen_size.height() / 768
app_for_screen_resolution.closeAllWindows()
