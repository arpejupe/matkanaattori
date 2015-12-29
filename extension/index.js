var { ToggleButton } = require('sdk/ui/button/toggle');
var panels = require("sdk/panel");
var self = require("sdk/self");
var matkanatorUrl = "http://ec2-54-201-173-16.us-west-2.compute.amazonaws.com/";

var button = ToggleButton({
  id: "mnator-button",
  label: "Matkanaattori",
  icon: {
    "16": "./icon-16.png",
    "32": "./icon-32.png",
    "64": "./icon-64.png"
  },
  onChange: handleChange
});

var panel = require("sdk/panel").Panel({
  width: 340,
  height: 500,
  // matkanaattorin url
  contentURL: matkanatorUrl,
  contentStyle: "#matkanator {margin:0!important; border-radius:0!important} #matkanator > div {max-width:100%!important;}"
});

function handleChange(state) {
  if (state.checked) {
    panel.show({
      position: button
    });
  }
}

function handleHide() {
  button.state('window', {checked: false});
}
