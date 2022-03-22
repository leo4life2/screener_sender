import React from "react";
import "typeface-roboto"
import logo from "./logo.png"

const Header = ({ styles }) => {

  const topBarStyle = {
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    width: "100%",
    height: styles.topBarHeight,
    backgroundColor: styles.white(),
    borderBottom: `1px solid ${styles.black(0.1)}`,
  };

  const logoBoxStyle = {
    width: 327,
    height: 117,
    display: "grid",
    gridTemplateColumns: "auto auto",
    gridGap: 0
  };

  const logoPicStyle = {
    height: logoBoxStyle.height,
    paddingRight: "14px"
  };

  const textStyle = {
    fontFamily: "Roboto",
    fontSize: 48,
    fontWeight: 900,
    color: "#333333",
  };

  return (
    <div style={topBarStyle}>

      <div style={logoBoxStyle}>

        <img src={logo} style={logoPicStyle} alt="Logo"/>

        <div style={textStyle}>
          Screener Sender
        </div>

      </div>

    </div>
  );
};

export default Header;
