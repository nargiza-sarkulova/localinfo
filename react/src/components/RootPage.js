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
        fetch('http://52.35.232.141:8000/ips/')
        .then(response => response.json())
        .then(data =>
        {
          this.setState({
            data: data
          })
        })
    }

    static propTypes = {
        ipAddress: PropTypes.string
    }

    storeName = React.createRef();

    fetchIpInfo = event => {
        event.preventDefault();
        this.props.history.push({
            pathname: '/details/',
            search: `?ip=${event.target[0].value}`,
            state: { data: this.state.data }
        })
    }

    render() {
        return (
            <div className="container full-height" id="ips-page-container">
              <div className="row full-height " id="ips-form-container">
                 <form className="d-flex flex-column" onSubmit={this.fetchIpInfo}>
                     <h2>Let's dig this ip?</h2>
                     <input type="text" required placeholder="Ip address" defaultValue="" ref={this.ipAddress} />
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
