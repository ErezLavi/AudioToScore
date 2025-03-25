import os
import streamlit.components.v1 as components

_RELEASE = False  # set to True when you want to use the production build

if not _RELEASE:
    _component_func = components.declare_component(
        "my_alphatab_component",
        url="http://localhost:3000"  # or 3001, depending on your dev server
    )
else:
    # After building, specify the absolute path to the build directory
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend", "build")
    _component_func = components.declare_component("my_alphatab_component", path=build_dir)


def st_alphatab(notation_data_base64=None, key=None):
    """
    Show alphaTab in the Streamlit app, given base64-encoded notation data
    (MusicXML, Guitar Pro, etc.).
    """
    component_value = _component_func(
        notationDataBase64=notation_data_base64,
        key=key,
        default=None
    )
    return component_value
