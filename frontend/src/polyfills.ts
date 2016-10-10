import 'core-js/es6';
import 'core-js/es7/reflect';
import 'web-animations-js';
import 'intl/index';
import 'intl/locale-data/jsonp/en.js';
require('zone.js/dist/zone');
// require('web-animations-js/web-animations.min.js');
if (process.env.ENV === 'production') {
  // Production
} else {
  // Development
  Error['stackTraceLimit'] = Infinity;
  require('zone.js/dist/long-stack-trace-zone');
}