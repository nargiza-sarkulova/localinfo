import React from 'react';
import News from './News';
import Weather from './Weather';

class Details extends React.Component {

    constructor(props) {
        super(props);

        this.state = {
            currentIpInfo: {
                news: []
            }
        };
        this.init();
    }

    init() {
        let fetchingExistingRecord = this.props.location.pathname.match(/\d+$/);
        if (fetchingExistingRecord) {
            let number = fetchingExistingRecord[0];
            let obj = this.props.location.state.data.find(obj => obj.id == number);
            this.state.currentIpInfo = obj

        } else {
            let ipAddress = this.props.location.search.match(/\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b/)[0]
            fetch('http://52.35.232.141:8000/ips/', {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    number: ipAddress
                })
            })
            .then(response => response.json())
            .then(data =>
                this.setState({
                    currentIpInfo: data
                })
            )
        }

    }

    render() {
        return (
            <div className="container full-height" id="ips-page-container">
                <div className="row full-height " id="ips-form-container">
                    <div className="ipRow d-flex flex-column">
                        <h2 className="mt-2 mb-3"><a href="/">&#8592; Go home</a></h2>
                        <h1 className="mt-2 mb-3">IP details: </h1>
                        <p><b>IP:</b> {this.state.currentIpInfo.number}</p>
                        <p><b>Country:</b> {this.state.currentIpInfo.country_name} <img src={this.state.currentIpInfo.country_flag} alt="" /> </p>
                        <p><b>City:</b> {this.state.currentIpInfo.city}</p>
                        <p><b>Region:</b> {this.state.currentIpInfo.region_name}</p>
                        <p><b>Latitude:</b> {this.state.currentIpInfo.latitude}</p>
                        <p><b>Longitude:</b> {this.state.currentIpInfo.latitude}</p>
                        <h1 className="mt-4 mb-2">Weather: </h1>
                        <Weather {...this.state.currentIpInfo.weather} />
                        <h1 className="mt-4 mb-2">News block: </h1>
                        <div className="">
                            {
                                this.state.currentIpInfo.news.map(news =>
                                    <News key={news.id} {...news} />
                                )
                            }
                        </div>
                    </div>
                </div>
            </div>
        )
    }
}

export default Details;
