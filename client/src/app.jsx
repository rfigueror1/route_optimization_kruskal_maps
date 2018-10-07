import axios from 'axios';

import React from 'react';
class App extends React.Component {
  constructor(props){
    super(props);
    this.state = {
      grocery_list:{},
      company:''
    }
  }

//react suggests to use componentDidMount for assynchronous

//axios promise based api

  componentDidMount(){
    this.getAllGroceries();
  }

  //method to get all the transports from a given company
  get_transports_from_company(){
    //url is /groceries because by default is not specified. Try with ajax.
    axios.get('/groceries').then((results) => {console.log(results.data); this.setState({grocery_list:results.data})}).catch(err => console.log(err,'error fetching groceries'));

  }

  render(){
    console.log('grocery_list',this.state.grocery_list);
    return(<div>
      <div>
        <Search handleClick = {this.addGrocery.bind(this)}/>
      </div>
      <div>
        <groceryList list = {this.state.grocery_list}/>
      </div>
    </div>
    );
  }

}

export default App;
