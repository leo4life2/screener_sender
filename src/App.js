import React, { Component } from "react";
import { Text, TextInput, View, TouchableOpacity } from 'react-native';
import Select from 'react-select'
import Header from "./Header";
import FooterMenu from "./FooterMenu";

class App extends Component {

  constructor(props) {
    super(props);
    this.state = {
      fn: localStorage.getItem("fName"),
      ln: localStorage.getItem("lName"),
      netid: localStorage.getItem("netId"),
      choice: [{value: "01234", label: "weekday"}],
      buttonDisabled: false
    };
  }

  _getOne() {
    fetch(`/getOne?fn=${this.state.fn}&ln=${this.state.ln}&netid=${this.state.netid}`, {
        'method':'GET',
        headers : {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        }
      }
    );
    window.location.href = `/screenerPage?fn=${this.state.fn}&ln=${this.state.ln}`;
    localStorage.setItem("fName", this.state.fn);
    localStorage.setItem("lName", this.state.ln);
    localStorage.setItem("netId", this.state.netid);
  };

  _subscribe() {
    if (this.state.choice.length <= 0) {alert("You did not choose any days."); return;}
    const choicesString = this.state.choice.reduce((accumulator, item) => accumulator += item.value, '')
    console.log(choicesString);
    fetch(`/subscribe?fn=${this.state.fn}&ln=${this.state.ln}&netid=${this.state.netid}&choice=${choicesString}`, {
        'method':'POST',
        headers : {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        }
      }
    )
    .then(response=>response.json())
    .then(data=> {
      alert(data.message);
     });
     localStorage.setItem("fName", this.state.fn);
     localStorage.setItem("lName", this.state.ln);
     localStorage.setItem("netId", this.state.netid);
  };

  _updateSub() {
    if (this.state.choice.length <= 0) {alert("You did not choose any days."); return;}
    const choicesString = this.state.choice.reduce((accumulator, item) => accumulator += item.value, '')
    console.log(choicesString);
    fetch(`/updateSubscription?fn=${this.state.fn}&ln=${this.state.ln}&netid=${this.state.netid}&choice=${choicesString}`, {
        'method':'PUT',
        headers : {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        }
      }
    )
    .then(response=>response.json())
    .then(data=> {
      alert(data.message);
     });
     localStorage.setItem("fName", this.state.fn);
     localStorage.setItem("lName", this.state.ln);
     localStorage.setItem("netId", this.state.netid);
  };

  _unsubscribe() {
    fetch(`/unsubscribe?fn=${this.state.fn}&ln=${this.state.ln}&netid=${this.state.netid}`, {
        'method':'DELETE',
        headers : {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        }
      }
    )
    .then(response=>response.json())
    .then(data=> {
      console.log("after unsubscribe.")
      console.log(data);
      alert(data.message);
     });
  };

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
    const getOneNowBox = {
      title: "Get one now.",
      subtitle: "No passwords needed.\nJust your name and net id.",
    };

    const subscribeBox = {
      title: "Get one every",
      choicesPlaceHolder: "choose day",
      choices: [
        {value: "01234", label: "weekday"},
        {value: "0123456", label: "day"},
        {value: "0", label: "mon"},
        {value: "1", label: "tues"},
        {value: "2", label: "wed"},
        {value: "3", label: "thurs"},
        {value: "4", label: "fri"},
        {value: "5", label: "sat"},
        {value: "6", label: "sun"}
      ],
      subtitle: "Unsubscribe at any time. \n Existing users can update send options."
    };

    const headerStyle = {
      fontFamily: "Roboto",
      fontSize: 48,
      fontWeight: 900,
      color: "#333333",
    };

    const chooseMenuStyle = {
      control: base => ({
        ...base,
        border: 0,
        boxShadow: 'none',
        paddingLeft: 20,
        fontFamily: "Roboto",
        fontSize: 48,
        fontWeight: 900,
        color: '#3F3CC2'
      }),

      singleValue: (styles) => {
        return {
          ...styles,
          color: '#3F3CC2',
        }
      },

      valueContainer: (provided) => ({
        ...provided,
        justifyContent: "center"
      }),

      indicatorSeparator: (styles) => ({display:'none'}),
      placeholder: (defaultStyles) => {
          return {
              ...defaultStyles,
              fontFamily: "Roboto",
              fontSize: 48,
              fontWeight: 900,
              color: '#828282',
          }
      },
      option: (styles, { data, isDisabled, isFocused, isSelected }) => {
        return {
          ...styles,
          textAlign: "center",
          fontFamily: "Roboto",
          fontSize: 24,
          fontWeight: 500,
          color: isFocused ? '#fff' : "#333333",
          backgroundColor: isFocused ? "#3F3CC2" : "#fff",
        };
      },
    };

    const subtitleStyle = {
      paddingTop: 36,
      paddingBottom: 53,

      fontFamily: "Roboto",
      fontSize: 24,
      fontWeight: 600,
      color: "#333333",
      textAlign: "center"
    };

    const containerStyle = {
      paddingTop: 36,
      paddingBottom: 50,
      marginBottom: 50,
      alignItems: "center",
      borderBottom: `1px solid #808080}`,
    };

    const inputBoxStyle = {
      paddingLeft: 20,
      paddingRight: 20,
      width: "60%",
      height: "100%",
      backgroundColor: "#fbfbfb",
      border: "0.5px solid #828282",
      borderRadius: 10
    };

    const textInputStyle = {
      width: "100%",
      height: 67,
      fontFamily: "Avenir",
      fontSize: 18,
      fontWeight: 500,
      borderBottomWidth: "0.5px",
      borderBottomColor: "#828282"
    };

    const lastInputStyle = {
      width: "100%",
      height: 67,
      fontFamily: "Avenir",
      fontSize: 18,
      fontWeight: 500,
    };

    const buttonStyles = {
      marginTop: 53,
      height: 67,
      backgroundColor: "#3F3CC2",
      borderRadius: 10,
      justifyContent: "center",
    };

    const unsubscribeStyle = {
      marginTop: 23,
      marginLeft: 5,
      marginRight: 5,
      height: 40,
      justifyContent: "center",
      borderRadius: 5,
      paddingTop: 2,
      paddingLeft: 5,
      paddingRight: 5,
      paddingBottom: 2,
      borderWidth: 0.5,
      borderColor: "#EB5757"
    };

    const updateStyle = {
      marginTop: 23,
      marginLeft: 5,
      marginRight: 5,
      width: unsubscribeStyle.width,
      height: 40,
      justifyContent: "center",
      borderRadius: 5,
      paddingTop: 2,
      paddingLeft: 20,
      paddingRight: 20,
      paddingBottom: 2,
      borderWidth: 0.5,
      borderColor: "#8684CF"
    };

    const BigButton = ({text}) => {
      return (
        <TouchableOpacity
          onPress={() => {
            console.log(text);

             if (text == "Subscribe") {this._subscribe()}
             else {this._getOne()}

             this.setState({
                buttonDisabled: true,
              });
              setTimeout(() => {
                  this.setState(() => ({
                    buttonDisabled: false,
                  }));
                }, 2000); // 2 second cooldown
           }}
          style={buttonStyles}
          disabled={this.state.buttonDisabled}
          >

          <Text
            style={{
              alignSelf: 'center',
              fontFamily: "Avenir",
              marginLeft: 10,
              marginRight: 10,
              fontSize: 24,
              fontWeight: 900,
              color: "#fff"
            }}>
            {text}
          </Text>

        </TouchableOpacity>
      );
    };

    return (
      <div
        style={{
          backgroundColor: "#fff",
          minHeight: "100vh",
          position: "relative"
        }}
      >
        <Header styles={styles} />
        <div>
          <View style={containerStyle}>
            <Text style={headerStyle}>{subscribeBox.title}</Text>
            <Select
              options={subscribeBox.choices}
              defaultValue={subscribeBox.choices[0]}
              isMulti
              closeMenuOnSelect={false}
              styles={chooseMenuStyle}
              placeholder="choose day"
              isSearchable={false}
              onChange={(choices) => {
                console.log(choices);
                 this.setState({choice: choices});
               }}
              >
            </Select>

            <Text style={subtitleStyle}>{subscribeBox.subtitle}</Text>
            <View style={inputBoxStyle}>
              <TextInput
                name="fn"
                style={textInputStyle}
                placeholder="First Name"
                placeholderTextColor="#828282"
                value={this.state.fn}
                onChangeText={(text) => this.setState({fn:text})}
                >
              </TextInput>
              <TextInput
                name="ln"
                style={textInputStyle}
                placeholder="Last Name"
                placeholderTextColor="#828282"
                value={this.state.ln}
                onChangeText={(text) => this.setState({ln:text})}
                >
              </TextInput>
              <TextInput
                name="netid"
                style={lastInputStyle}
                placeholder="Net ID"
                placeholderTextColor="#828282"
                value={this.state.netid}
                onChangeText={(text) => this.setState({netid:text})}
                >
              </TextInput>
            </View>

            <BigButton text="Subscribe"></BigButton>

            <View style={[styles.container, {
              flexDirection: "row",
              justifyContent: "center",
              width: "100%"
            }]}>

            <TouchableOpacity
              onPress={() => {
                this._updateSub()
                 this.setState({
                    buttonDisabled: true,
                  });
                  setTimeout(() => {
                      this.setState(() => ({
                        buttonDisabled: false,
                      }));
                    }, 2000); // 2 second cooldown
               }}
              style={updateStyle}
              disabled={this.state.buttonDisabled}
              >
              <Text
                style={{
                  alignSelf: 'center',
                  fontFamily: "Avenir",
                  fontSize: 18,
                  fontWeight: 800,
                  color: "#8684CF",
                }}>
                {"Update"}
              </Text>

            </TouchableOpacity>

            <TouchableOpacity
              onPress={() => {
                this._unsubscribe()
                 this.setState({
                    buttonDisabled: true,
                  });
                  setTimeout(() => {
                      this.setState(() => ({
                        buttonDisabled: false,
                      }));
                    }, 2000); // 2 second cooldown
               }}
              style={unsubscribeStyle}
              disabled={this.state.buttonDisabled}
              >
              <Text
                style={{
                  alignSelf: 'center',
                  fontFamily: "Avenir",
                  fontSize: 18,
                  fontWeight: 800,
                  color: "#EB5757"
                }}>
                {"Unsubscribe"}
              </Text>

            </TouchableOpacity>

            </View>
          </View>

          <View style={containerStyle}>
            <Text style={headerStyle}>{getOneNowBox.title}</Text>
            <Text style={subtitleStyle}>{getOneNowBox.subtitle}</Text>
            <View style={inputBoxStyle}>
              <TextInput
                name="fn"
                style={textInputStyle}
                placeholder="First Name"
                placeholderTextColor="#828282"
                value={this.state.fn}
                onChangeText={(text) => this.setState({fn:text})}
                >
              </TextInput>
              <TextInput
                name="ln"
                style={textInputStyle}
                placeholder="Last Name"
                placeholderTextColor="#828282"
                value={this.state.ln}
                onChangeText={(text) => this.setState({ln:text})}
                >
              </TextInput>
              <TextInput
                name="netid"
                style={lastInputStyle}
                placeholder="Net ID"
                placeholderTextColor="#828282"
                value={this.state.netid}
                onChangeText={(text) => this.setState({netid:text})}
                >
              </TextInput>
            </View>
            <BigButton text="Get it!"></BigButton>
          </View>
        </div>

        <FooterMenu menuItems={menuItems} styles={styles} />
      </div>
    );
  };

}

export default App;
