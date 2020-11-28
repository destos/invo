const URN = require("urn-lib")

export var irn = URN.create("irn", {
  components: [
    // protocol is automatically added (protocol = urn or arn or whatever)
    "ins",
    "etype",
    "nss",
  ],
  separator: ":",
  allowEmpty: true,
})
