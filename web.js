var MongoStore = require('ac-node').MongoStore;
var track = require('ac-koa-hipchat-keenio').track;
var Notifier = require('ac-koa-hipchat-notifier').Notifier;
var crypto = require('crypto');
var Jitsi = require('./lib/jitsi');

var ack = require('ac-koa').require('hipchat');
var pkg = require('./package.json');
var app = ack(pkg, {store: 'MongoStore'});

var addon = app.addon()
  .hipchat()
  .allowGlobal(true)
  .allowRoom(true)
  .avatar('https://s3.amazonaws.com/uploads.hipchat.com/10804/1332878/ygXvYzdGdsNiAVS/upload.png')
  .scopes('send_notification');

track(addon);

var addonStore = MongoStore(process.env[app.config.MONGO_ENV], 'hiptsi');
var notifier = Notifier({format: 'html', dir: __dirname + '/messages'});
var pattern = /^r?\/jitsi/i;

addon.webhook('room_message', /^\/jitsi/i, function *() {
  var global = !this.tenant.room;
  var match = this.match;
  var room = this.room;
  var jitsi = Jitsi(addonStore, this.tenant);
  roomName = crypto.randomBytes(Math.ceil(20/2))
      .toString('hex') // convert to hexadecimal format
      .slice(0,20);   // return required number of characters

  var call_url =  process.env.JITSI_ENV + '/' + roomName
  return yield notifier.sendTemplate('call', {
    caller: this.sender.name,
    call_url: call_url
  }, { color: 'purple'});
});

app.listen();
