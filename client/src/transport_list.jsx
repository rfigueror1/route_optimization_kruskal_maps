import React, { Component } from 'react';
import Transport from './transport.jsx';

var TransportList = function({transports}){
  return(<div className="transports-list">
    {transports.map((i) =>
      <Transport  key={i.id} transport={i}/>
    )}
  </div>);
};

export default TransportList;