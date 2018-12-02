"use strict";

exports.__esModule = true;
exports.default = void 0;

var _propTypes = _interopRequireDefault(require("prop-types"));

var _reactEmotion = _interopRequireDefault(require("react-emotion"));

var _lodash = _interopRequireDefault(require("lodash.isinteger"));

var _config = _interopRequireWildcard(require("../config"));

function _interopRequireWildcard(obj) { if (obj && obj.__esModule) { return obj; } else { var newObj = {}; if (obj != null) { for (var key in obj) { if (Object.prototype.hasOwnProperty.call(obj, key)) { var desc = Object.defineProperty && Object.getOwnPropertyDescriptor ? Object.getOwnPropertyDescriptor(obj, key) : {}; if (desc.get || desc.set) { Object.defineProperty(newObj, key, desc); } else { newObj[key] = obj[key]; } } } } newObj.default = obj; return newObj; } }

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i] != null ? arguments[i] : {}; var ownKeys = Object.keys(source); if (typeof Object.getOwnPropertySymbols === 'function') { ownKeys = ownKeys.concat(Object.getOwnPropertySymbols(source).filter(function (sym) { return Object.getOwnPropertyDescriptor(source, sym).enumerable; })); } ownKeys.forEach(function (key) { _defineProperty(target, key, source[key]); }); } return target; }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

function _templateObject2() {
  var data = _taggedTemplateLiteralLoose(["\n        margin-left: ", "%;\n      "]);

  _templateObject2 = function _templateObject2() {
    return data;
  };

  return data;
}

function _templateObject() {
  var data = _taggedTemplateLiteralLoose(["", ""]);

  _templateObject = function _templateObject() {
    return data;
  };

  return data;
}

function _taggedTemplateLiteralLoose(strings, raw) { if (!raw) { raw = strings.slice(0); } strings.raw = raw; return strings; }

var ModificatorType = _propTypes.default.oneOfType([_propTypes.default.number, _propTypes.default.bool]);

var offsetProps = _config.DIMENSION_NAMES.map(function (d) {
  return d + 'Offset';
});

var DimensionPropTypes = _config.DIMENSION_NAMES.reduce(function (propTypes, dimension) {
  propTypes[dimension] = ModificatorType;
  propTypes[dimension + 'Offset'] = _propTypes.default.number;
  return propTypes;
}, {});

var Col =
/*#__PURE__*/
(0, _reactEmotion.default)("div", {
  target: "eija48a0"
})("box-sizing:border-box;flex:0 0 auto;padding-right:", function (p) {
  return (0, _config.default)(p).gutterWidth / 2;
}, "rem;padding-left:", function (p) {
  return (0, _config.default)(p).gutterWidth / 2;
}, "rem;", function (p) {
  return p.reverse && "\n    flex-direction: column-reverse;\n  ";
}, " ", function (p) {
  return Object.keys(p).filter(function (k) {
    return ~_config.DIMENSION_NAMES.indexOf(k);
  }).sort(function (k1, k2) {
    return _config.DIMENSION_NAMES.indexOf(k1) - _config.DIMENSION_NAMES.indexOf(k2);
  }).map(function (k) {
    return (0, _config.default)(p).media[k](_templateObject(), (0, _lodash.default)(p[k]) // Integer value
    ? "\n        flex-basis: " + 100 / (0, _config.default)(p).gridSize * p[k] + "%;\n        max-width: " + 100 / (0, _config.default)(p).gridSize * p[k] + "%;\n        display: block;\n      " // Boolean
    : p[k] // Auto-width
    ? "\n          flex-grow: 1;\n          flex-basis: 0;\n          max-width: 100%;\n          display: block;\n        " // Hide element
    : 'display: none;');
  });
}, " ", function (p) {
  return Object.keys(p).filter(function (k) {
    return ~offsetProps.indexOf(k);
  }).map(function (k) {
    return (0, _config.default)(p).media[k.replace(/Offset$/, '')](_templateObject2(), 100 / (0, _config.default)(p).gridSize * p[k]);
  });
});
Col.displayName = 'Col';
Col.propTypes = _objectSpread({}, DimensionPropTypes, {
  reverse: _propTypes.default.bool,
  children: _propTypes.default.node
});
var _default = Col;
exports.default = _default;