"use strict";

exports.__esModule = true;
exports.default = void 0;

var _propTypes = _interopRequireDefault(require("prop-types"));

var _reactEmotion = _interopRequireWildcard(require("react-emotion"));

var _config = _interopRequireWildcard(require("../config"));

function _interopRequireWildcard(obj) { if (obj && obj.__esModule) { return obj; } else { var newObj = {}; if (obj != null) { for (var key in obj) { if (Object.prototype.hasOwnProperty.call(obj, key)) { var desc = Object.defineProperty && Object.getOwnPropertyDescriptor ? Object.getOwnPropertyDescriptor(obj, key) : {}; if (desc.get || desc.set) { Object.defineProperty(newObj, key, desc); } else { newObj[key] = obj[key]; } } } } newObj.default = obj; return newObj; } }

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _templateObject() {
  var data = _taggedTemplateLiteralLoose(["\n        width: ", "rem;\n      "]);

  _templateObject = function _templateObject() {
    return data;
  };

  return data;
}

function _taggedTemplateLiteralLoose(strings, raw) { if (!raw) { raw = strings.slice(0); } strings.raw = raw; return strings; }

var Grid =
/*#__PURE__*/
(0, _reactEmotion.default)("div", {
  target: "em22la90"
})("margin-right:auto;margin-left:auto;padding-right:", function (p) {
  return (0, _config.default)(p).outerMargin + 'rem';
}, ";padding-left:", function (p) {
  return (0, _config.default)(p).outerMargin + 'rem';
}, ";", function (p) {
  return !p.fluid &&
  /*#__PURE__*/
  (0, _reactEmotion.css)(_config.DIMENSION_NAMES.map(function (t) {
    return (0, _config.default)(p).container[t] && (0, _config.default)(p).media[t](_templateObject(), function (p) {
      return (0, _config.default)(p).container[t];
    });
  }));
});
Grid.displayName = 'Grid';
Grid.propTypes = {
  fluid: _propTypes.default.bool,
  children: _propTypes.default.node
};
var _default = Grid;
exports.default = _default;