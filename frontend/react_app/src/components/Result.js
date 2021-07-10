import React, { useState, useEffect } from "react";import PropTypes from 'prop-types';
import { CSSTransitionGroup } from 'react-transition-group';
import {Link} from "react-router-dom";
import * as settings from "../settings";
import axios from "axios";
import { Typography, AppBar, Button, Card, CardActions, CardContent, CardMedia, CssBaseline, Grid, Toolbar, Container } from '@material-ui/core';


const pics =
    ['https://storage.googleapis.com/linear-static-assets/subset/800.jpg',
   'https://storage.googleapis.com/linear-static-assets/subset/1254.jpg',
   'https://storage.googleapis.com/linear-static-assets/subset/1241.jpg',
   'https://storage.googleapis.com/linear-static-assets/subset/191.jpg',
   'https://storage.googleapis.com/linear-static-assets/subset/1301.jpg',
   'https://storage.googleapis.com/linear-static-assets/subset/1816.jpg',
   'https://storage.googleapis.com/linear-static-assets/subset/287.jpg',
   'https://storage.googleapis.com/linear-static-assets/subset/1564.jpg'];



function Result(props) {
    const [counter, setCounter] = useState(5)
    const [predImg, setPredImg] = useState(pics)
    // React hook state variable - Prediction
    // const [prediction, setPrediction] = React.useState(null)
    // const [image, setImage] = React.useState(props.quizResult)

    // It takes a function
    useEffect(() => {
    // This gets called after every render, by default
    // (the first one, and every one after that)
        console.log("Within result")
        if (props.prediction == undefined || props.prediction.length == 0) {
            setPredImg(pics)
            alert("API Success")
        }
        // else {
        //     setPredImg(props.prediction)
        //     alert("take backup")
        // }

    // If you want to implement componentWillUnmount,
    // return a function from here, and React will call
    // it prior to unmounting.
    // return () => console.log('unmounting...');
    }, []);


    // Upon start, make the predict API call and update the state variable - Prediction


    return (
    <CSSTransitionGroup
      className="container result"
      component="div"
      transitionName="fade"
      transitionEnterTimeout={800}
      transitionLeaveTimeout={500}
      transitionAppear
      transitionAppearTimeout={500}
    >
      <div>
        Returned results values: <strong>{props.quizResult}</strong>!
      </div>
      <div>
        <div>
          <Masonry
            className={"photo-list"}
            elementType={"ul"}
            options={masonryOptions}
            disableImagesLoaded={false}
            updateOnEachImageLoad={false}
          >
            {predImg.map((photo) => (
              <li className={`photo-item`}>
                <img src={photo} alt="" />
              </li>
            ))}
          </Masonry>
        </div>
      </div>

      <div>
          <Link to="/">
              <Button variant="contained" color="primary">
                  Back to Home
              </Button>
          </Link>
      </div>
    </CSSTransitionGroup>
    );
}

Result.propTypes = {
  quizResult: PropTypes.string.isRequired
};

export default Result;