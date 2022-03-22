import React, { Component } from "react";
import Header from "./Header";
import FooterMenu from "./FooterMenu";
import Content from "./Content";

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {};
  }

  render() {
    const styles = {
      white: (opacity = 1) => `rgba(255, 255, 255, ${opacity})`,
      black: (opacity = 1) => `rgba(0, 0, 0, ${opacity})`,
      topBarHeight: 220,
      footerMenuHeight: 50
    };

    const menuItems = [
      { icon: `😀`, text: "Item 1" },
      { icon: `😉`, text: "Item 2" },
      { icon: `😎`, text: "Item 3" },
      { icon: `🤔`, text: "Item 4" },
      { icon: `😛`, text: "Item 5" }
    ];

    return (
      <div
        style={{
          backgroundColor: styles.white(),
          minHeight: "100vh",
          position: "relative"
        }}
      >
        <Header styles={styles} />
        <Content styles={styles} />
        <FooterMenu menuItems={menuItems} styles={styles} />
      </div>
    );
  }
}

export default App;
