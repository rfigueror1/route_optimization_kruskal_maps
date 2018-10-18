import React, { Component } from 'react';
import {Transport} from './transport.jsx'

var TransportSummary = function({transports}){
  const listItems = transports.map((transport) =>
    <li key={transport.id}>
      {transport.text}
    </li>
  );
  return (
    <ul>{listItems}</ul>
  );
};

export default TransportSummary;
