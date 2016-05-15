var crypto = require('crypto');
var coArray = require('co-array');

function Jitsi(addonStore, tenant) {
  if (!(this instanceof Jitsi)) {
    return new Jitsi(addonStore, tenant);
  }
  var groupKey = crypto.createHash('sha1')
    .update(String(tenant.group))
    .update(tenant.links.capabilities)
    .digest('hex');
  this._store = addonStore.narrow(groupKey);
}

var proto = Jitsi.prototype;

module.exports = Jitsi;
