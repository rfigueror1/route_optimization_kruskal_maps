import React, { Component } from 'react';

var Algorithms = function({options}){
	<select>
		<option selected value={options[1]}>{options[0]}</option>
  		<option value={options[2]}>{options[1]}</option>
  		<option value={options[2]}>{options[2]}</option>
	</select>
};

export default Algorithms;
