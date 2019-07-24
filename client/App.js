import React, {Fragment} from 'react';
import PubNubReact from 'pubnub-react';
import {
  SafeAreaView,
  StyleSheet,
  ScrollView,
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StatusBar,
  Image,
} from 'react-native';

import {
  Header,
  LearnMoreLinks,
  Colors,
  DebugInstructions,
  ReloadInstructions,
} from 'react-native/Libraries/NewAppScreen';




export default class App extends React.Component {

  constructor(props) {
    super(props)

    this.pubnub = new PubNubReact({
      publishKey: "pub-c-65d7292f-2d66-4bcb-af81-756159a296d0",
      subscribeKey: "sub-c-35ba70c2-acae-11e9-a577-e6e01a51e1d3"
    })

    //Base State
    this.state = {
      image: require('./assets/dylan.jpg'),
      message: 'hel',
      text: '',
      count: 0,
    }

    this.pubnub.init(this);
  }

  async componentDidMount() {
    this.setUpApp()
  }

  async setUpApp(){
    this.pubnub.getMessage("global", msg => {
      this.setState({count: msg.message.ID})
      this.setState({image: msg.message.url})
    })

    this.pubnub.subscribe({
      channels: ["global"],
      withPresence: false
    });
  }

  addUser = () => {


  }

  handleText = (name) => {
    this.setState({ text: name })
 }

 publishName = (text) => {
  this.pubnub.publish({
    message: {
      ID: this.state.count,
      name: text,
    },
    channel: "ch1"
  });
}

  render() {
  return(

    <View>

      <Image
        source={{uri: this.state.image}}
        style={{width: 250, height: 250}}
      />
      <Text>{'Do You Know This Person?'}</Text>
      <TextInput style = {styles.input}
               underlineColorAndroid = "transparent"
               placeholder = "Name"
               placeholderTextColor = "#9a73ef"
               autoCapitalize = "none"
               onChangeText = {this.handleText}/>
      <TouchableOpacity
          style = {styles.submitButton}
          onPress = {
            () => this.publishName(this.state.text)
          }>
            <Text>"SUBMIT"</Text>
      </TouchableOpacity>

    </View>


  )}
}

const styles = StyleSheet.create({
  scrollView: {
    backgroundColor: Colors.lighter,
  },
  engine: {
    position: 'absolute',
    right: 0,
  },
  body: {
    backgroundColor: Colors.white,
  },
  sectionContainer: {
    marginTop: 32,
    paddingHorizontal: 24,
  },
  sectionTitle: {
    fontSize: 24,
    fontWeight: '600',
    color: Colors.black,
  },
  sectionDescription: {
    marginTop: 8,
    fontSize: 18,
    fontWeight: '400',
    color: Colors.dark,
  },
  highlight: {
    fontWeight: '700',
  },
  footer: {
    color: Colors.dark,
    fontSize: 12,
    fontWeight: '600',
    padding: 4,
    paddingRight: 12,
    textAlign: 'right',
  },
});