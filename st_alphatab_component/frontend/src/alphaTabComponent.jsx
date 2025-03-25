import React from "react";
import { StreamlitComponentBase, withStreamlitConnection } from "streamlit-component-lib";
import * as alphaTab from "@coderline/alphatab";

class MyAlphaTabComponent extends StreamlitComponentBase {
  constructor(props) {
    super(props);
    this.alphaTabContainerRef = React.createRef();
    this.alphaTabApi = null;
  }

  componentDidMount() {
    this._renderAlphaTab();
    // Let Streamlit know the component is ready, which resizes the iframe
    this.setState({});
  }

  componentDidUpdate() {
    this._renderAlphaTab();
  }

  _renderAlphaTab() {
    const notationDataBase64 = this.props.args.notationDataBase64;
    const container = this.alphaTabContainerRef.current;
    if (!container || !notationDataBase64) return;

    // Convert from base64 => bytes
    const bin = window.atob(notationDataBase64);
    const bytes = new Uint8Array(bin.length);
    for (let i = 0; i < bin.length; i++) {
      bytes[i] = bin.charCodeAt(i);
    }

    // Destroy previous alphaTab instance if any
    if (this.alphaTabApi) {
      this.alphaTabApi.destroy();
      this.alphaTabApi = null;
    }
    container.innerHTML = "";

    // Initialize alphaTab
    this.alphaTabApi = new alphaTab.AlphaTabApi(container, {
      file: bytes,
      rendering: { staveProfile: "ScoreTab" },
      player: { enablePlayer: true },
    });
  }

  render() {
    return (
      <div style={{ border: "1px solid #ccc" }}>
        <div ref={this.alphaTabContainerRef}></div>
      </div>
    );
  }
}

export default withStreamlitConnection(MyAlphaTabComponent);