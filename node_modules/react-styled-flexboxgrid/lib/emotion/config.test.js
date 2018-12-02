"use strict";

var _chai = require("chai");

var _config = _interopRequireWildcard(require("./config"));

function _interopRequireWildcard(obj) { if (obj && obj.__esModule) { return obj; } else { var newObj = {}; if (obj != null) { for (var key in obj) { if (Object.prototype.hasOwnProperty.call(obj, key)) { var desc = Object.defineProperty && Object.getOwnPropertyDescriptor ? Object.getOwnPropertyDescriptor(obj, key) : {}; if (desc.get || desc.set) { Object.defineProperty(newObj, key, desc); } else { newObj[key] = obj[key]; } } } } newObj.default = obj; return newObj; } }

/* eslint-env mocha */
describe('config', function () {
  describe('BASE_CONF', function () {
    it('should be an object', function () {
      (0, _chai.expect)(_config.BASE_CONF).to.be.an('object');
    });
  });
  describe('DIMENSION_NAMES', function () {
    it('should be an array', function () {
      (0, _chai.expect)(_config.DIMENSION_NAMES).to.be.an('array');
    });
  });
  describe('config()', function () {
    it('should be a function', function () {
      (0, _chai.expect)(_config.default).to.be.an('function');
    });
  });
});