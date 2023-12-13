from PySide6.QtGui import QPalette, QColor

from packages.Startup import ColorThems


def get_light_palette():
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(*ColorThems.Light_Window_Color))
    palette.setColor(QPalette.WindowText, QColor(*ColorThems.Light_WindowText_Color))
    palette.setColor(QPalette.Base, QColor(*ColorThems.Light_Base_Color))
    palette.setColor(QPalette.AlternateBase, QColor(*ColorThems.Light_AlternateBase_Color))
    palette.setColor(QPalette.ToolTipBase, QColor(*ColorThems.Light_ToolTipBase_Color))
    palette.setColor(QPalette.ToolTipText, QColor(*ColorThems.Light_ToolTipText_Color))
    palette.setColor(QPalette.Text, QColor(*ColorThems.Light_Text_Color))
    palette.setColor(QPalette.Button, QColor(*ColorThems.Light_Button_Color))
    palette.setColor(QPalette.ButtonText, QColor(*ColorThems.Light_ButtonText_Color))
    palette.setColor(QPalette.Link, QColor(*ColorThems.Light_Link_Color))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(*ColorThems.Light_Highlight_Color))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(*ColorThems.Light_HighlightedText_Color))
    palette.setColor(QPalette.PlaceholderText, QColor(*ColorThems.Light_PlaceholderText_Color))
    palette.setColor(QPalette.Active, QPalette.Button, QColor(*ColorThems.Light_Button_Color))
    palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(*ColorThems.Light_ButtonText_Color_Disabled))
    palette.setColor(QPalette.Disabled, QPalette.WindowText, QColor(*ColorThems.Light_WindowText_Color_Disabled))
    palette.setColor(QPalette.Disabled, QPalette.Base, QColor(*ColorThems.Light_Base_Color_Disabled))
    palette.setColor(QPalette.Disabled, QPalette.AlternateBase, QColor(*ColorThems.Light_AlternateBase_Color_Disabled))
    palette.setColor(QPalette.Disabled, QPalette.Text, QColor(*ColorThems.Light_Text_Color_Disabled))
    palette.setColor(QPalette.Disabled, QPalette.Light, QColor(*ColorThems.Light_Light_Color_Disabled))
    palette.setColor(QPalette.Disabled, QPalette.PlaceholderText,
                     QColor(*ColorThems.Light_PlaceholderText_Color_Disabled))
    return palette


def get_dark_palette():
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(*ColorThems.Dark_Window_Color))
    palette.setColor(QPalette.WindowText, QColor(*ColorThems.Dark_WindowText_Color))
    palette.setColor(QPalette.Base, QColor(*ColorThems.Dark_Base_Color))
    palette.setColor(QPalette.AlternateBase, QColor(*ColorThems.Dark_AlternateBase_Color))
    palette.setColor(QPalette.ToolTipBase, QColor(*ColorThems.Dark_ToolTipBase_Color))
    palette.setColor(QPalette.ToolTipText, QColor(*ColorThems.Dark_ToolTipText_Color))
    palette.setColor(QPalette.Text, QColor(*ColorThems.Dark_Text_Color))
    palette.setColor(QPalette.Button, QColor(*ColorThems.Dark_Button_Color))
    palette.setColor(QPalette.ButtonText, QColor(*ColorThems.Dark_ButtonText_Color))
    palette.setColor(QPalette.Link, QColor(*ColorThems.Dark_Link_Color))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(*ColorThems.Dark_Highlight_Color))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(*ColorThems.Dark_HighlightText_Color))
    palette.setColor(QPalette.PlaceholderText, QColor(*ColorThems.Dark_PlaceholderText_Color))
    palette.setColor(QPalette.Active, QPalette.Button, QColor(*ColorThems.Dark_Button_Color))
    palette.setColor(QPalette.Disabled, QPalette.Button, QColor(*ColorThems.Dark_Button_Color_Disabled))
    palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(*ColorThems.Dark_ButtonText_Color_Disabled))
    palette.setColor(QPalette.Disabled, QPalette.WindowText, QColor(*ColorThems.Dark_WindowText_Color_Disabled))
    palette.setColor(QPalette.Disabled, QPalette.Base, QColor(*ColorThems.Dark_Base_Color_Disabled))
    palette.setColor(QPalette.Disabled, QPalette.AlternateBase, QColor(*ColorThems.Dark_AlternateBase_Color_Disabled))
    palette.setColor(QPalette.Disabled, QPalette.Text, QColor(*ColorThems.Dark_Text_Color_Disabled))
    palette.setColor(QPalette.Disabled, QPalette.Light, QColor(*ColorThems.Dark_Light_Color_Disabled))
    palette.setColor(QPalette.Disabled, QPalette.PlaceholderText,
                     QColor(*ColorThems.Dark_PlaceholderText_Color_Disabled))
    return palette
