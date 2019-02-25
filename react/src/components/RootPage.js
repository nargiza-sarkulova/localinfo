import React from 'react';
import PropTypes from 'prop-types';
import LocationCard from './LocationCard';


class RootPage extends React.Component {

    constructor(props) {
        super(props);

        this.state = {
          data: []
        };
      }

    componentDidMount() {
        fetch('http://localhost:8000/ips/')
        .then(response => response.json())
        .then(data =>
        {
          this.setState({
            data: data
          })
        })
    }

    //Specifying required props format
    static propTypes = {
        loginName: PropTypes.string
    }

    storeName = React.createRef();

    fetchIpInfo = event => {
        event.preventDefault();
        console.log('event')
        console.log(event)
        this.props.history.push(`/details/1`);
    }
    render() {
        return (
            <div className="container full-height" id="ips-page-container">
              <div className="row full-height " id="ips-form-container">
                 <form className="store-selector  d-flex flex-column" onSubmit={this.fetchIpInfo}>
                     <h2>Let's dig this ip?</h2>
                     <input type="text" required placeholder="Username" defaultValue="192.168.0.1" ref={this.loginName} />
                     <div className=" d-flex justify-content-end button-container">
                        <button className="" type="submit">Send</button>
                     </div>
                     <hr/>

                    <div className="">
                        {this.state.data.map(ip =>
                            <LocationCard key={ip.id} {...ip} />
                        )}
                    </div>
                 </form>
              </div>
            </div>
        )
    }
}

export default RootPage;




