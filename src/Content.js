import React from 'react';
import { Text, TextInput, View, TouchableOpacity } from 'react-native';
import Select from 'react-select'

const Content = ({ styles }) => {
  const getOneNowBox = {
    title: "Get one now.",
    subtitle: "No passwords needed.\nJust your name and net id.",
  };

  const subscribeBox = {
    title: "Get one every",
    choicesPlaceHolder: "choose day",
    choices: [
      {value: "weekday", label: "weekday"},
      {value: "day", label: "day"}
    ],
    subtitle: "Unsubscribe at any time."
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
      color: '#3F3CC2',
    }),

    singleValue: (styles) => {
      return {
        ...styles,
        color: '#3F3CC2',
      }
    },

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
    borderBottom: `1px solid ${styles.black(0.1)}`,
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

  const TextInputBox = () => {
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

    return (
      <View style={inputBoxStyle}>
        <TextInput
          style={textInputStyle}
          placeholder="First Name"
          placeholderTextColor="#828282"
          >
        </TextInput>
        <TextInput
          style={textInputStyle}
          placeholder="Last Name"
          placeholderTextColor="#828282"
          >
        </TextInput>
        <TextInput
          style={lastInputStyle}
          placeholder="Net ID"
          placeholderTextColor="#828282"
          >
        </TextInput>
      </View>
    );
  };

  const buttonStyles = {
    marginTop: 53,
    width: "30%",
    height: 67,
    backgroundColor: "#3F3CC2",
    borderRadius: 10,
    justifyContent: "center",
  };

  const BigButton = ({text}) => {
    return (
      <TouchableOpacity
        onPress={() => console.log(text+'Button pressed')}
        style={buttonStyles}>

        <Text
          style={{
            alignSelf: 'center',
            fontFamily: "Avenir",
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
    <div>

      <View style={containerStyle}>
        <Text style={headerStyle}>{getOneNowBox.title}</Text>
        <Text style={subtitleStyle}>{getOneNowBox.subtitle}</Text>
        <TextInputBox></TextInputBox>
        <BigButton text="Get it!"></BigButton>
      </View>

      <View style={containerStyle}>
        <Text style={headerStyle}>{subscribeBox.title}</Text>

        <Select
          options={subscribeBox.choices}
          styles={chooseMenuStyle}
          placeholder="choose day"
          isSearchable={false}
          >
        </Select>

        <Text style={subtitleStyle}>{subscribeBox.subtitle}</Text>
        <TextInputBox></TextInputBox>
        <BigButton text="Subscribe"></BigButton>
      </View>


    </div>
  );
};

export default Content;
