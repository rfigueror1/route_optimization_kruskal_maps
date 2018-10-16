import React, { Component } from 'react';

var Transport = ({transport}) => {
  return (
    <div className="transport" lat={transport.lat} lng={transport.lng} text={transport.text} id={transport.id}>  
      <img src={'http://www.hino.com/images/195_diesel_crewcab_3qtr_ghs3176_final-crop-u18340.png?crc=4010437874'} width="50"/>
    </div>)
};

export default Transport;