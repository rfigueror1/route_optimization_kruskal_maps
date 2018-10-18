import React, { Component } from 'react';

var Transport = ({transport}) => {
  return (
    <div className="transport" lat={transport.lat} lng={transport.lng} text={transport.text} id={transport.id}>  
      hello
    </div>)
};

export default Transport;