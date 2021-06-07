import React from 'react'
import axios from 'axios';
import * as settings from '../settings';

import CssBaseline from '@material-ui/core/CssBaseline';
import { Link } from "react-router-dom";
import { withStyles, makeStyles } from '@material-ui/core/styles';
import { Container, Grid, Paper, Typography, Slider, Button } from '@material-ui/core';


// ########################################################
// Material UI inline styles
// ########################################################
const useStyles = makeStyles((theme) => ({
    container: {
        maxWidth: "75%",
        marginTop: "15vh",
        marginBottom: "10vh",
        borderRadius: '6px',
        backgroundColor: theme.palette.action.disabledBackground,
    },
    title: {
        marginTop: theme.spacing(2),
        marginBottom: theme.spacing(2),
        padding: theme.spacing(2), paddingLeft: theme.spacing(4),
        color: theme.palette.primary.main,
    },
    sliders: {
        paddingTop: theme.spacing(2),
        paddingBottom: theme.spacing(2),
        paddingLeft: theme.spacing(4),
        paddingRight: theme.spacing(4),
        marginBottom: theme.spacing(2),
    },
    slidertop: {
        marginTop: theme.spacing(4),
    }
}));

// ########################################################
// Our Custom IRIS slider. You may use the default slider instead of this
// ########################################################
const IrisSlider = withStyles({
    root: {
        color: '#751E66',
    },
    valueLabel: {
        left: 'calc(-50% -2)',
        top: -22,
        '& *': {
            background: 'transparent',
            color: '#000',
        },
    },
    mark: {
        height: 8,
        width: 1,
        marginTop: -3,
    },
    markActive: {
        opacity: 1,
        backgroundColor: 'currentColor',
    },
})(Slider);

// Marks on the slider track
const marks = [{ value: 0 }, { value: 10 }];

// ########################################################
// The main Home component returned by this Module
// ########################################################
function Home(props) {
    // Material UI Classes
    const classes = useStyles();

    // // React hook state variable - Dimensions
    // const [dimensions, setDimensions] = React.useState({
    //     sepal_length: 6,
    //     sepal_width: 6,
    //     petal_length: 6,
    //     petal_width: 6,
    // });
    // // React hook state variable - Prediction
    // const [prediction, setPrediction] = React.useState(null)
    //
    // // Function to update the Dimensions state upon slider value change
    // const handleSliderChange = name => (event, newValue) => {
    //     setDimensions(
    //         {
    //             ...dimensions,
    //             ...{ [name]: newValue }
    //         }
    //     );
    // };
    //
    // // Function to make the predict API call and update the state variable - Prediction
    // const handlePredict = event => {
    //     // Submit Iris Flower measured dimensions as form data
    //     let irisFormData = new FormData();
    //     irisFormData.append("sepal length (cm)", dimensions.sepal_length);
    //     irisFormData.append("sepal width (cm)", dimensions.sepal_width);
    //     irisFormData.append("petal length (cm)", dimensions.petal_length);
    //     irisFormData.append("petal width (cm)", dimensions.petal_width);
    //
    //     //Axios variables required to call the predict API
    //     let headers = { 'Authorization': `Token ${props.token}` };
    //     let url = settings.API_SERVER + '/api/predict/';
    //     let method = 'post';
    //     let config = { headers, method, url, data: irisFormData };
    //
    //     //Axios predict API call
    //     axios(config).then(
    //         res => {setPrediction(res.data["Predicted Iris Species"])
    //         }).catch(
    //             error => {alert(error)})
    //
    // }
    //
    // function valuetext(value) {
    //     return `${value} cm`;
    // }


    return (
        <div>
            <div>
            {'\n'}Ready to explore your taste and preference?
            {'\n'}Our AI will find out how your ideal house looks like in less than 5 minutes!
            {'\n'}Choose your favourite image, and we will create a mood board for you!
            {'\n'}don't think too much
            {'\n'}
            </div>
            <div>
                <Link to="/quiz">
                    <Button variant="contained" color="primary">
                        Let's go!
                    </Button>
                </Link>
            </div>
            <div>
                <Link to="/MLPrediction">
                    <Button variant="contained" color="primary">
                        Try ML
                    </Button>
                </Link>
            </div>
        </div>
    )
}

export default Home